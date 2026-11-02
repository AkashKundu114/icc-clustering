"""Audit saved benchmark schedules and source assembly without rerunning fits.

Input: local Final Year Project results/passF/benchmark_matrix_passF.csv,
results/exp3_cohirf_benchmark.csv, passE benchmark files, and historical
source at commit 7f74f6842ae02bc8fd9203fab18a56b7c68035c.
Outputs: seed_provenance_matrix.csv, fairness_matrix.csv,
benchmark_assembly_check.json. This script does not fit clustering models.
"""
from pathlib import Path
import hashlib, json, subprocess
import pandas as pd

FYP = Path(r"D:\Final Year Project")
OUT = Path(__file__).resolve().parent
PASSF = FYP / "results/passF/benchmark_matrix_passF.csv"
COHIRF = FYP / "results/exp3_cohirf_benchmark.csv"
PASS_E = FYP / "results/passE/benchmark_matrix_seeds0_9.csv"
HIGH_D = FYP / "results/passF/high_d_30seeds_all_models.csv"
FAST = FYP / "results/passF/high_d_30seeds_fast_models.csv"
DEC = FYP / "results/passF/high_d_30seeds_dec.csv"
ICC_V2 = FYP / "results/passE/high_d_30seeds_bimodal.csv"
MERGER = "scripts/merge_passF_benchmark.py"
PASSF_COMMIT = "7f74f6842ae02bc8fd9203fab18a56b7c68035c"
COHIRF_COMMIT = "567c5260972f1ce29124ce8449a907bebe8b3983"
HD = {"cns", "colon", "leukemia", "ovarian", "prostate", "srbct"}


def file_sha(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def show(commit, path):
    return subprocess.check_output(["git", "-C", str(FYP), "show", f"{commit}:{path}"], stderr=subprocess.DEVNULL)


def main():
    for p in (PASSF, COHIRF, PASS_E, HIGH_D, FAST, DEC, ICC_V2):
        if not p.is_file():
            raise SystemExit(f"Required local source artifact missing: {p}")
    a, b, pe, hd, fast, dec, icc = [pd.read_csv(p) for p in (PASSF, COHIRF, PASS_E, HIGH_D, FAST, DEC, ICC_V2)]
    all_rows = pd.concat([a, b], ignore_index=True)
    seeds = []
    for (dataset, method), g in all_rows.groupby(["dataset", "model"], sort=True):
        if method == "CoHiRF":
            row_source = str(COHIRF)
            source_commit = COHIRF_COMMIT
            source_rule = "historical scripts/run_phase3_experiments.py; CoHiRF-specific generator lineage matches raw seed column"
            execution = "saved score CSV; execution not attested"
        else:
            row_source = str(PASSF)
            source_commit = PASSF_COMMIT
            if dataset not in HD:
                source_rule = "merged from results/passE/benchmark_matrix_seeds0_9.csv (seeds 0-9)"
            elif method == "Ward":
                source_rule = "seeds 0-9 from Pass E; seeds 10-29 copied from seed 0 by merge_passF_benchmark.py"
            elif method == "ICC_v2":
                source_rule = "seeds 0-9 from Pass E benchmark; seeds 10-29 copied from Pass E high_d_30seeds_bimodal.csv"
            elif method == "DEC":
                source_rule = "seeds 0-9 from Pass E; seeds 10-29 from run_passF_dec.py"
            else:
                source_rule = "seeds 0-9 from Pass E; seeds 10-29 from run_passF_fast_models.py"
            execution = "saved score row; source merge trace available; fit execution still not authenticated"
        seed_values = sorted(map(int, g.seed.unique()))
        seeds.append({
            "dataset": dataset, "method": method, "rows": len(g), "unique_seed_count": len(seed_values),
            "seeds": ";".join(map(str, seed_values)), "min_seed": min(seed_values), "max_seed": max(seed_values),
            "source_file": row_source, "source_artifact_commit": source_commit, "source_rule": source_rule,
            "same_seed_schedule_as_other_methods": "NO" if method == "CoHiRF" else "PassF family only; does not establish paired random draws",
            "execution_status": execution,
        })
    pd.DataFrame(seeds).to_csv(OUT / "seed_provenance_matrix.csv", index=False)

    # Rebuild the Pass-F matrix exactly from its committed merge inputs.
    std = pe[~pe.dataset.isin(HD)].copy()
    rebuilt = pd.concat([hd, std], ignore_index=True)
    cols = list(a.columns)
    same_shape = rebuilt[cols].shape == a[cols].shape
    same_records = False
    if same_shape:
        aa = a[cols].sort_values(["dataset", "model", "seed"]).reset_index(drop=True)
        rr = rebuilt[cols].sort_values(["dataset", "model", "seed"]).reset_index(drop=True)
        same_records = True
        for c in cols:
            if c in {"ari", "nmi", "elapsed_sec"}:
                import numpy as np
                same_records = same_records and bool(np.allclose(aa[c], rr[c], rtol=1e-12, atol=1e-12, equal_nan=True))
            else:
                same_records = same_records and bool(aa[c].equals(rr[c]))

    # Audit copied Ward block and zero/ambiguous score rows.
    ward = hd[hd.model.eq("Ward")]
    ward_copy_mismatches = 0
    for d, g in ward.groupby("dataset"):
        ref = g[g.seed.eq(0)].iloc[0]
        copied = g[g.seed.between(10, 29)]
        ward_copy_mismatches += int(((copied.ari != ref.ari) | (copied.nmi != ref.nmi) | (copied.elapsed_sec != ref.elapsed_sec)).sum())
    zeros = a.groupby("model").apply(lambda g: pd.Series({
        "ari_zero": int((g.ari == 0).sum()),
        "nmi_zero": int((g.nmi == 0).sum()),
        "both_zero": int(((g.ari == 0) & (g.nmi == 0)).sum()),
        "both_zero_runtime_zero": int(((g.ari == 0) & (g.nmi == 0) & (g.elapsed_sec == 0)).sum()),
    }), include_groups=False).to_dict(orient="index")

    # Method implementation / fairness inspection matrix.
    method_rows = [
        ("K-Means", "run_clusterer('kmeans')", "n_init=1, random init; seed passed", "One clustering fit", "Same standardized X and externally set K; seed schedule PassF only", "One seed does not represent repeated initialization well; budget differs from ensembles"),
        ("Ward", "run_clusterer('ward')", "adds Gaussian jitter scale 1e-4 using seed then Ward", "One hierarchical fit", "PassF high-D seeds 10-29 copied from seed 0", "Copied rows are not 20 independent seed runs; jitter implementation conflicts with ‘deterministic’ label"),
        ("Spectral", "run_clusterer('spectral')", "nearest-neighbor affinity, 10 neighbors, seeded assignment", "One spectral fit", "Same X/K, PassF seeds", "Different computational budget and affinity from Euclidean methods"),
        ("FCM", "custom _fcm_like", "random Dirichlet membership, up to 100 iterations", "One FCM fit", "Same X/K, PassF seeds", "Custom implementation; no independent reference implementation validation in this audit"),
        ("Standard_Consensus", "25 KMeans base partitions + dense coassociation average linkage", "25 derived internal seeds; base KMeans init n_init=1", "25 base fits + consensus", "Same X/K, PassF seeds", "More compute than single-fit baselines; no matched compute budget"),
        ("Core_Halo_Consensus", "local Li et al. 2019 implementation; 25 KMeans base partitions", "25 derived internal seeds", "25 base fits + core/halo postprocessing", "Same X/K, PassF seeds", "42 exact zero ARI and NMI records; saved file has no status/error field, so failure vs outcome is unresolved"),
        ("ICC_v1", "25 KMeans base partitions + core anchor spectral consensus", "25 derived internal seeds", "25 base fits + consensus", "Same X/K, PassF seeds", "Local implementation; no external implementation parity check"),
        ("ICC_v2", "InvariantCoreConsensusV2; M=25, L=40, pool_frac=.15; auto base engine spectral when N<=100 else KMeans", "seeded internal subspace/base seeds", "25 base fits + anchor consensus", "Same X/K; 10-29 ARIs imported from separate PassE score file", "In small high-D cohorts uses Spectral bases while Standard Consensus uses KMeans; not a matched-base ablation"),
        ("DEC", "custom Deep Embedded Clustering; auto backend, AE 200 epochs + fine tune 100 max", "seed passed to numpy/backend; hardware backend may differ", "Neural training, potentially GPU/CPU", "Same X/K, PassF seed rows", "High cost and backend variation; exceptions are converted to zero metrics in PassF helper"),
        ("FCAG", "local anchor-guided spectral method; default 100 anchors, kmeans++ and final KMeans n_init=10", "seeded anchor selection and final discretization", "Anchor graph/eigendecomposition", "Same X/K, PassF seeds", "Custom local implementation; no implementation parity evidence for cited method in this audit"),
        ("FastMVC", "run_fastmvc explicitly documents itself as internal FastMVC-Surrogate, not official FastMICE/FastMVC", "seeded anchor/subspace views; default 15 views", "15 view graph construction + eigensolve", "Same X/K, PassF seeds", "Must not be presented as faithful published FastMVC baseline or used for attributed method ranking"),
        ("CoHiRF", "local CoHiRF implementation, run_phase3_experiments: 25 reps, feature subspace=.15, threshold=.80", "saved seeds 42-71/42-51", "25 internal resampling/base fits", "Same X/K but seed ids differ from PassF methods", "Not seed-paired across methods; no execution log/status/input hash in CSV"),
    ]
    frows = []
    for method, impl, rng, budget, same, concern in method_rows:
        frows.append({"method": method, "implementation_and_configuration": impl, "randomness": rng,
                      "nominal_compute_budget": budget, "input_and_K_comparability": same,
                      "fairness_or_validity_issue": concern, "implementation_verification": "source inspected; fresh fit not rerun"})
    pd.DataFrame(frows).to_csv(OUT / "fairness_matrix.csv", index=False)

    # Output lineage file hashes and key checks for an execution manifest/report.
    inputs = [PASSF, COHIRF, PASS_E, HIGH_D, FAST, DEC, ICC_V2]
    result = {
        "target_repo_baseline": "d0c4665af327ec284d931c94f9658309ec13763c",
        "FYP_head": subprocess.check_output(["git", "-C", str(FYP), "rev-parse", "HEAD"], text=True).strip(),
        "passF_source_commit": PASSF_COMMIT,
        "cohirf_source_commit": COHIRF_COMMIT,
        "passF_rows": len(a), "cohirf_rows": len(b), "combined_rows": len(all_rows),
        "dataset_method_cells": int(all_rows.groupby(["dataset", "model"]).ngroups),
        "duplicate_dataset_method_seed_keys": int(all_rows.duplicated(["dataset", "model", "seed"]).sum()),
        "passF_matrix_rebuilt_from_committed_merge_inputs_shape_matches": same_shape,
        "passF_matrix_rebuilt_from_committed_merge_inputs_all_values_match": bool(same_records),
        "assembly_numeric_tolerance": "rtol=1e-12, atol=1e-12 for ARI/NMI/runtime; exact for identifiers, dimensions, K, seed",
        "highD_rows": len(hd), "passE_rows": len(pe), "passF_ward_copy_mismatches_against_seed0": int(ward_copy_mismatches),
        "passF_zero_metric_counts_by_method": zeros,
        "input_artifacts": [{"path": str(p), "bytes": p.stat().st_size, "sha256": file_sha(p)} for p in inputs],
        "historical_merge_script_present_at_passF_commit": True,
        "passF_fit_execution_attestation": "UNVERIFIED; score construction lineage recovered but no independent logs/environment/input digest per fit",
        "CoHiRF_fit_execution_attestation": "UNVERIFIED",
        "model_fits_rerun": False,
    }
    (OUT / "benchmark_assembly_check.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ["passF_rows", "cohirf_rows", "combined_rows", "dataset_method_cells", "duplicate_dataset_method_seed_keys", "passF_matrix_rebuilt_from_committed_merge_inputs_all_values_match", "passF_ward_copy_mismatches_against_seed0"]}, indent=2))


if __name__ == "__main__":
    main()
