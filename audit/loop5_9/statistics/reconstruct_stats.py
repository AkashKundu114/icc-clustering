"""Independent Loop 5.9 numerical reconstruction from local saved evidence.

Reads D:\Final Year Project caches, stability partition NPYs, per-fit Parquet
records and raw benchmark score CSVs. Writes only sibling CSV/JSON outputs.
No model fits are executed. Requires NumPy, pandas, SciPy, scikit-learn, PyArrow.
"""
from pathlib import Path
from collections import defaultdict
import csv, hashlib, json, re
import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, rankdata
from sklearn.metrics import adjusted_rand_score

ROOT = Path(r"D:\Final Year Project")
OUT = Path(__file__).resolve().parent
COHORTS = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]
PARTS = ROOT / "results/stability/partitions"
RUNS = ROOT / "results/stability/runs"


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def write_rows(name, rows):
    p = OUT / name
    if not rows:
        raise ValueError(f"No rows for {name}")
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)


def parse_name(p):
    m = re.fullmatch(r"(.+?)_(.+)_(real|null)_(\d+)\.npy", p.name)
    if not m:
        raise ValueError(f"Unexpected partition name: {p.name}")
    d, method, mode, rep = m.groups()
    return d, method, mode, int(rep)


def main():
    paths = sorted(PARTS.glob("*.npy"))
    if len(paths) != 4320:
        raise SystemExit(f"Expected 4320 partition files, found {len(paths)}")
    summary = pd.read_csv(ROOT / "results/stability/subsample_stability_summary.csv")
    saved = {(str(r.dataset), str(r.model)): r for r in summary.itertuples(index=False)}
    cache_data, loaded, cell_rows, errors = {}, defaultdict(dict), [], []
    total_pairs = 0
    for d in COHORTS:
        with np.load(ROOT / f"data/cache/{d}.npz", allow_pickle=False) as z:
            X, y = z["X"], z["y"]
        cache_data[d] = (X, y)
        for m in sorted({parse_name(p)[1] for p in paths if parse_name(p)[0] == d}):
            mode_parts = {"real": [], "null": []}
            real_aris, minfracs, kcounts, fit_rows = [], [], [], []
            for mode in ("real", "null"):
                for rep in range(30):
                    stem = f"{d}_{m}_{mode}_{rep}"
                    pp, rp = PARTS / f"{stem}.npy", RUNS / f"{stem}.parquet"
                    if not pp.is_file() or not rp.is_file():
                        errors.append(f"missing:{stem}"); continue
                    obj = np.load(pp, allow_pickle=True).item()
                    idx = np.asarray(obj["sub_idx"], dtype=np.int64)
                    pred = np.asarray(obj["labels"])
                    recdf = pd.read_parquet(rp)
                    if len(recdf) != 1:
                        errors.append(f"parquet_rows:{stem}:{len(recdf)}"); continue
                    rec = recdf.iloc[0]
                    if str(rec.dataset) != d or str(rec.model) != m or str(rec["mode"]) != mode or int(rec.subsample_id) != rep:
                        errors.append(f"metadata:{stem}")
                    if str(rec.status) != "success": errors.append(f"status:{stem}:{rec.status}")
                    if len(idx) != len(pred) or len(set(idx.tolist())) != len(idx) or (idx < 0).any() or (idx >= len(y)).any():
                        errors.append(f"shape_index:{stem}")
                    if mode == "real":
                        ari = float(adjusted_rand_score(y[idx], pred)); real_aris.append(ari)
                        if abs(ari - float(rec.accuracy)) > 1e-12: errors.append(f"ari_record:{stem}")
                    uniq, cnt = np.unique(pred, return_counts=True)
                    kcounts.append(len(uniq)); minfrac = float(cnt.min() / len(pred))
                    if len(uniq) < len(np.unique(y)): minfrac = 0.0
                    if mode == "real": minfracs.append(minfrac)
                    mode_parts[mode].append((idx, pred))
                    fit_rows.append((mode, rep, idx, pred, rec))
            def mean_pair(parts):
                vals=[]
                for i in range(len(parts)):
                    ix, labs = parts[i]
                    pos = {int(v): j for j, v in enumerate(ix)}
                    for j in range(i+1, len(parts)):
                        jx, other = parts[j]
                        common = np.intersect1d(ix, jx, assume_unique=True)
                        vals.append(float(adjusted_rand_score(
                            np.fromiter((labs[pos[int(v)]] for v in common), dtype=labs.dtype),
                            np.fromiter((other[{int(v): k for k, v in enumerate(jx)}[int(v)]] for v in common), dtype=other.dtype))))
                return float(np.mean(vals)) if vals else float("nan"), vals
            stab, realpairs = mean_pair(mode_parts["real"])
            nullstab, nullpairs = mean_pair(mode_parts["null"])
            total_pairs += len(realpairs) + len(nullpairs)
            acc = float(np.mean(real_aris))
            min_count = sum(v >= .05 for v in minfracs)
            min_counts = {thr:sum(v >= thr for v in minfracs) for thr in (.02,.05,.10)}
            row = {
                "dataset": d, "method": m,
                "n_real_repeats": len(real_aris), "n_null_repeats": len(mode_parts["null"]),
                "n_real_pairwise_aris": len(realpairs), "n_null_pairwise_aris": len(nullpairs),
                "mean_stability": stab, "mean_external_ari": acc, "mean_gap": stab-acc,
                "mean_null_stability": nullstab, "nondegenerate_repeats_5pct": min_count,
                "repeats_min_cluster_ge_2pct": min_counts[.02],
                "repeats_min_cluster_ge_5pct": min_counts[.05],
                "repeats_min_cluster_ge_10pct": min_counts[.10],
                "minimum_cluster_fraction": min(minfracs) if minfracs else float("nan"),
                "predicted_k_distribution": json.dumps({str(k):kcounts.count(k) for k in sorted(set(kcounts))}),
                "rule_i": stab >= .5 and acc <= .05,
                "rule_i_prime": stab >= .5 and acc <= .05 and min_count >= 27,
                "saved_stability": float(saved[(d,m)].subsample_stability),
                "saved_external_ari": float(saved[(d,m)].subsample_accuracy),
                "stability_abs_error": abs(stab-float(saved[(d,m)].subsample_stability)),
                "ari_abs_error": abs(acc-float(saved[(d,m)].subsample_accuracy)),
                "null_abs_error": abs(nullstab-float(saved[(d,m)].null_stability)),
                "cache_sha256": digest(ROOT/f"data/cache/{d}.npz"),
            }
            cell_rows.append(row)
    if len(cell_rows) != 72: raise SystemExit(f"Expected 72 cells; got {len(cell_rows)}")
    recurring = defaultdict(set)
    for r in cell_rows:
        if r["rule_i_prime"]: recurring[r["method"]].add(r["dataset"])
    for r in cell_rows:
        r["rule_iii"] = bool(r["rule_i_prime"] and len(recurring[r["method"]]) >= 3)
        r["rule_iii_recurrence_count"] = len(recurring[r["method"]])
    write_rows("cell_reconstruction.csv", cell_rows)

    selected=[]
    for r in cell_rows:
        selected.append({"dataset":r["dataset"],"method":r["method"],"mean_stability":r["mean_stability"],"mean_external_ari":r["mean_external_ari"],"gap":r["mean_gap"],"n_successful_repeats":r["n_real_repeats"],"minimum_cluster_fraction":r["minimum_cluster_fraction"],"predicted_k_distribution_real_and_null":r["predicted_k_distribution"],"repeats_min_cluster_ge_2pct":r["repeats_min_cluster_ge_2pct"],"repeats_min_cluster_ge_5pct":r["repeats_min_cluster_ge_5pct"],"repeats_min_cluster_ge_10pct":r["repeats_min_cluster_ge_10pct"],"rule_i":r["rule_i"],"rule_i_prime":r["rule_i_prime"],"rule_iii":r["rule_iii"],"rule_iii_recurrence_count":r["rule_iii_recurrence_count"]})
    write_rows("selection_reconstruction.csv",selected)
    for rule in ("rule_i", "rule_i_prime", "rule_iii"):
        subset=[r for r in cell_rows if r[rule]]
        print(rule,len(subset),float(np.mean([r['mean_gap'] for r in subset])) if subset else np.nan)

    gaps=np.array([r["mean_gap"] for r in cell_rows]); stabs=np.array([r["mean_stability"] for r in cell_rows]); aris=np.array([r["mean_external_ari"] for r in cell_rows])
    print("six cohort results", {"mean_stability":float(stabs.mean()),"mean_ari":float(aris.mean()),"mean_gap":float(gaps.mean()),"median_gap":float(np.median(gaps)),"mean_null":float(np.mean([r['mean_null_stability'] for r in cell_rows])),"pairs":total_pairs,"errors":len(errors),"max_errors":{"stability":max(r['stability_abs_error'] for r in cell_rows),"ari":max(r['ari_abs_error'] for r in cell_rows),"null":max(r['null_abs_error'] for r in cell_rows)}})

    nd = pd.DataFrame(cell_rows); nd = nd[nd.nondegenerate_repeats_5pct >= 27].copy(); nd["gap"] = nd.mean_stability-nd.mean_external_ari
    cohort_means=nd.groupby("dataset").gap.mean().reindex(COHORTS).to_numpy(); counts=nd.groupby("dataset").gap.size().reindex(COHORTS).to_numpy()
    e1=float(nd.gap.mean()); e2=float(cohort_means.mean()); b=10000; seeds=[0,1,7,42,123,2025,99173]; brows=[]
    for seed in seeds:
        ids=np.random.default_rng(seed).integers(0,6,size=(b,6)); e1boot=(cohort_means[ids]*counts[ids]).sum(1)/counts[ids].sum(1); e2boot=cohort_means[ids].mean(1)
        for label,point,vec in [("E1_cell_weighted",e1,e1boot),("E2_equal_cohort",e2,e2boot)]:
            brows.append({"estimand":label,"seed":seed,"B":b,"point":point,"ci_lower":float(np.quantile(vec,.025)),"ci_upper":float(np.quantile(vec,.975)),"bootstrap_mean":float(vec.mean()),"unit":"cohort cluster"})
    write_rows("bootstrap_reanalysis.csv",brows)

    # Recompute the 13x12 external-ARI benchmark directly from score rows.
    a=pd.read_csv(ROOT/"results/passF/benchmark_matrix_passF.csv")
    c=pd.read_csv(ROOT/"results/exp3_cohirf_benchmark.csv")
    common=set(a.columns)&set(c.columns)
    bench=pd.concat([a,c],ignore_index=True,sort=False)
    methodcol="model" if "model" in bench else "method"
    if methodcol not in bench or "dataset" not in bench or "seed" not in bench or "ari" not in bench: raise SystemExit(f"Unexpected benchmark fields {list(bench.columns)}")
    if bench.duplicated(["dataset",methodcol,"seed"]).any(): raise SystemExit("duplicate dataset-method-seed keys")
    means=bench.groupby(["dataset",methodcol]).ari.mean().unstack(methodcol)
    if means.isna().any().any(): raise SystemExit("incomplete dataset-method cells")
    statistic,p=friedmanchisquare(*(means[m].to_numpy() for m in means.columns))
    ranks=pd.DataFrame(np.vstack([rankdata(-row,method="average") for row in means.to_numpy()]),index=means.index,columns=means.columns)
    avg=ranks.mean(axis=0).sort_values()
    icc_name = "ICC_v2" if "ICC_v2" in avg.index else "ICC-v2"
    bench_result={"passF_rows":len(a),"cohirf_rows":len(c),"combined_rows":len(bench),"datasets":len(means),"methods":len(means.columns),"cells":int(means.size),"unique_keys":int(bench.drop_duplicates(["dataset",methodcol,"seed"]).shape[0]),"duplicate_keys":int(bench.duplicated(["dataset",methodcol,"seed"]).sum()),"missing_cells":int(means.isna().sum().sum()),"friedman_chi2":float(statistic),"df":len(means.columns)-1,"pvalue":float(p),"average_ranks":{k:float(v) for k,v in avg.items()},"icc_v2_method_name":icc_name,"icc_v2_rank":int(np.where(avg.index==icc_name)[0][0]+1),"passF_sha256":digest(ROOT/"results/passF/benchmark_matrix_passF.csv"),"cohirf_sha256":digest(ROOT/"results/exp3_cohirf_benchmark.csv")}
    (OUT/"benchmark_reanalysis.json").write_text(json.dumps(bench_result,indent=2)+"\n",encoding="utf-8")
    print("benchmark",json.dumps(bench_result,sort_keys=True))
    if errors:
        (OUT/"reconstruction_errors.txt").write_text("\n".join(errors)+"\n",encoding="utf-8")
    print("completed", "cells",len(cell_rows),"pair_values",total_pairs,"validation_errors",len(errors))


if __name__ == "__main__":
    main()
