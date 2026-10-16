import os
import json
import hashlib
import time
import pandas as pd

commit_hash = "879fd96a282e88f5491826dd7355d24d9490661b"
now_ts = int(time.time())
records = []
run_counter = 0

def make_rec(exp, ds, n, d, k, meth, var, seed, m_name, m_val, wall_t=None, rss_mb=None, cfg=None):
    global run_counter
    run_counter += 1
    rid = f"run_{run_counter:07d}"
    c_hash = hashlib.sha256(json.dumps(cfg or {}, sort_keys=True).encode()).hexdigest()[:12]
    return {
        "run_id": rid,
        "experiment": exp,
        "dataset": ds,
        "N": int(n) if n is not None else None,
        "D": int(d) if d is not None else None,
        "K": int(k) if k is not None else None,
        "method": meth,
        "variant": var,
        "seed": int(seed) if seed is not None else None,
        "metric_name": m_name,
        "metric_value": float(m_val) if m_val is not None else None,
        "wall_time_s": float(wall_t) if wall_t is not None else None,
        "peak_rss_mb": float(rss_mb) if rss_mb is not None else None,
        "config_hash": c_hash,
        "commit_hash": commit_hash,
        "timestamp": now_ts
    }

p_exp3 = "experiments/exp3_real_world_benchmarks/data/exp3_1_benchmark_matrix_v2.csv"
if os.path.exists(p_exp3):
    df = pd.read_csv(p_exp3)
    for _, r in df.iterrows():
        records.append(make_rec("exp3_1", r["dataset"], r["N"], r["D"], r["K"], r["model"], r["model"], r["seed"], "ari", r["ari"], r.get("elapsed_sec"), r.get("peak_memory_mb"), {"trial": r.get("trial")}))
        records.append(make_rec("exp3_1", r["dataset"], r["N"], r["D"], r["K"], r["model"], r["model"], r["seed"], "nmi", r["nmi"], r.get("elapsed_sec"), r.get("peak_memory_mb"), {"trial": r.get("trial")}))

p_exp2_real = "experiments/exp2_ablation/data/exp2_real_ablation_results.csv"
if os.path.exists(p_exp2_real):
    df = pd.read_csv(p_exp2_real)
    for _, r in df.iterrows():
        records.append(make_rec("exp2_ablation_real", r["dataset"], r["N"], r["D"], r["K"], "ICC-v2", r["variant"], None, "mean_ari", r["mean_ari"], cfg={"std_ari": r.get("std_ari")}))

p_exp2_syn = "experiments/exp2_ablation/data/exp2_ablation_results.csv"
if os.path.exists(p_exp2_syn):
    df = pd.read_csv(p_exp2_syn)
    for _, r in df.iterrows():
        records.append(make_rec("exp2_ablation_synthetic", "synthetic", 300, r["d_noise"] + 2, 3, "ICC-v2", r["variant"], None, "mean_ari", r["mean_ari"], cfg={"d_noise": r["d_noise"], "noise_kind": r.get("noise_kind")}))

p_mad = "experiments/exp2_ablation/data/exp2_1_madelon_pr.csv"
if os.path.exists(p_mad):
    df = pd.read_csv(p_mad)
    for _, r in df.iterrows():
        cut = int(r["K_cutoff"])
        records.append(make_rec("exp2_1_vssg_madelon", "madelon", 500, 500, 2, "VSSG", "BC", r.get("trial"), f"precision_at_{cut}", r["precision"]))
        records.append(make_rec("exp2_1_vssg_madelon", "madelon", 500, 500, 2, "VSSG", "BC", r.get("trial"), f"recall_at_{cut}", r["recall"]))

p_syn_pr = "experiments/exp2_ablation/data/exp2_1_synthetic_10kd_pr.csv"
if os.path.exists(p_syn_pr):
    df = pd.read_csv(p_syn_pr)
    for _, r in df.iterrows():
        cut = int(r["K_cutoff"])
        records.append(make_rec("exp2_1_vssg_syn10k", "synthetic_10kd", 500, 10000, 3, "VSSG", "BC", r.get("trial"), f"precision_at_{cut}", r["precision"]))
        records.append(make_rec("exp2_1_vssg_syn10k", "synthetic_10kd", 500, 10000, 3, "VSSG", "BC", r.get("trial"), f"recall_at_{cut}", r["recall"]))

p_exp1 = "experiments/exp1_generalization/data/exp1_multiclassifier_results.csv"
if os.path.exists(p_exp1):
    df = pd.read_csv(p_exp1)
    for _, r in df.iterrows():
        records.append(make_rec("exp1_generalization", "synthetic", 300, r["d_noise"] + 2, 3, r["classifier"], r["training_set"], r["trial"], "test_accuracy", r["test_accuracy"], cfg={"d_noise": r["d_noise"]}))

p_exp4_fid = "experiments/exp4_scalability_and_sensitivity/data/exp4_3_anchor_fidelity_results.csv"
if os.path.exists(p_exp4_fid):
    df = pd.read_csv(p_exp4_fid)
    for _, r in df.iterrows():
        records.append(make_rec("exp4_3_fidelity", "synthetic", r["N"], r["D"], 3, "ICC-v2_reduced", "L40", r["trial"], "ari", r["ari_reduced"], r["time_reduced"], r["mem_reduced_mb"]))
        records.append(make_rec("exp4_3_fidelity", "synthetic", r["N"], r["D"], 3, "ICC-v2_exact", "Exact", r["trial"], "ari", r["ari_exact"], r["time_exact"], r["mem_exact_mb"]))

p_exp5_s = "experiments/exp5_extreme_scale/data/exp5_sample_scaling_results.csv"
if os.path.exists(p_exp5_s):
    df = pd.read_csv(p_exp5_s)
    for _, r in df.iterrows():
        records.append(make_rec("exp5_sample_scaling", "synthetic", r["N"], r["D"], r["K"], "ICC-v2", "L40", r["trial"], "ari", r["ari_icc"], r["time_icc"], r["mem_icc_mb"]))
        records.append(make_rec("exp5_sample_scaling", "synthetic", r["N"], r["D"], r["K"], "MiniBatchKMeans", "Default", r["trial"], "ari", r["ari_mbk"], r["time_mbk"], r["mem_mbk_mb"]))

p_exp5_d = "experiments/exp5_extreme_scale/data/exp5_dimension_scaling_results.csv"
if os.path.exists(p_exp5_d):
    df = pd.read_csv(p_exp5_d)
    for _, r in df.iterrows():
        records.append(make_rec("exp5_dimension_scaling", "synthetic", r["N"], r["D"], r["K"], "ICC-v2", "L40", r["trial"], "time", r["time_icc"], r["time_icc"], r["mem_icc_mb"]))

os.makedirs("results", exist_ok=True)
with open("results/results.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2)

with open("results/results.json", "rb") as f:
    h = hashlib.sha256(f.read()).hexdigest()

print(f"Consolidated {len(records)} records into results/results.json.")
print(f"SHA256(results/results.json) = {h}")
