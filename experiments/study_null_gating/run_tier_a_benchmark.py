"""
Study 3' Real-Data Tier-A Benchmark Harness (Accelerated)
=========================================================
Frozen Pre-Registration Specification: experiments/PRE_REGISTRATION_v1.0.md
Section A5 (Real data and downstream protocol) & A6 (Outcomes and decision rules).

Datasets (Tier-A, D/N > 20):
- CNS (N=60, D=7,129, K=2)
- Colon (N=62, D=2,000, K=2)
- Leukemia (N=72, D=7,129, K=3)
- Ovarian (N=253, D=15,154, K=2)
- Prostate (N=102, D=12,600, K=2)
- SRBCT (N=63, D=2,308, K=4)

Comparators evaluated at matched feature count k = |F_active|:
- G_prop: NCG-BC (Null-Calibrated Gating)
- G2: Current fixed BC rule (BC >= 5/9, capped at max(100, ceil(0.15*D)))
- G4: Hartigan Dip test with Benjamini-Hochberg (matched-k)

Protocol:
- Seeds 0 to 9 per dataset (Section 0.3).
- Label-free gating computed on all samples (transductive).
- Downstream partitioners: ICC-v2 (frozen config), K-Means, and Ward.
- Primary Outcome: Paired ARI differences against G2 and G4 over Tier-A datasets.
- Confirmatory Decision Rule for H4 (Section A6):
  (i) Mean difference >= +0.02 ARI
  (ii) Bootstrap 95% CI lower bound > 0
  (iii) At least 5 of 6 datasets non-negative
  (iv) One-sided exact sign-flip test p <= 0.025 (Holm-corrected)
"""

import gc
import itertools
import json
import os
import sys
import time

# Enforce single-threaded OpenBLAS to prevent memory paging exhaustion on Windows
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"

import numpy as np
import torch
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import adjusted_rand_score

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.icc.consensus_v2 import InvariantCoreConsensusV2
from experiments.study_null_gating.run_confirmatory_grid import (
    preprocess_features,
    compute_finite_sample_bc,
    evaluate_dip_pvalues,
)
from experiments.study_null_gating.gpu_scb import ncg_bc_gate_accelerated


def load_tier_a_dataset(name: str):
    path = f"data/cache/{name.lower()}.npz"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Cache file {path} not found.")
    data = np.load(path)
    X = data["X"].astype(np.float32)
    y = data["y"]
    return X, y


def compute_exact_sign_flip_p(diffs: np.ndarray) -> float:
    """Exact one-sided sign-flip test for H0: mean <= 0 vs H1: mean > 0."""
    obs_stat = np.sum(diffs)
    n = len(diffs)
    # Enumerate all 2^n sign assignments
    count_geq = 0
    total = 2 ** n
    for signs in itertools.product([-1, 1], repeat=n):
        s = np.array(signs)
        if np.sum(s * np.abs(diffs)) >= obs_stat:
            count_geq += 1
    return float(count_geq / total)


def bootstrap_ci(diffs: np.ndarray, n_boot: int = 10000, alpha: float = 0.05, rng=None):
    """Percentile bootstrap 95% CI of the mean across datasets."""
    if rng is None:
        rng = np.random.default_rng(42)
    n = len(diffs)
    boot_means = np.zeros(n_boot)
    for b in range(n_boot):
        idx = rng.choice(n, size=n, replace=True)
        boot_means[b] = np.mean(diffs[idx])
    ci_lower = np.percentile(boot_means, 100 * (alpha / 2))
    ci_upper = np.percentile(boot_means, 100 * (1 - alpha / 2))
    return float(ci_lower), float(ci_upper)


def run_tier_a_benchmark():
    datasets = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]
    seeds = list(range(10))  # Seeds 0 to 9 (Section 0.3)

    from experiments.study_null_gating.gpu_scb import get_safe_device
    safe_dev = get_safe_device()
    device_str = "CUDA (RTX 5060)" if safe_dev.type == "cuda" else "Vectorized CPU Tensors"
    print("=" * 80)
    print(f"STARTING ACCELERATED REAL-DATA TIER-A BENCHMARK: STUDY 3' (H4)")
    print(f"Device: {device_str}")
    print(f"Datasets: {len(datasets)} ({', '.join(datasets)}) | Seeds: {len(seeds)} (0-9)")
    print("=" * 80)

    out_file = "results/study_null_gating/tier_a_results.json"
    os.makedirs("results/study_null_gating", exist_ok=True)

    # Load existing results if resuming
    results = {}
    if os.path.exists(out_file):
        try:
            with open(out_file, "r") as f:
                results = json.load(f)
            print(f"Loaded existing progress for datasets: {list(results.keys())}")
        except Exception:
            results = {}

    for d_name in datasets:
        if d_name in results and len(results[d_name]["NCG_BC"]["icc"]) == 10:
            print(f"\n>>> Dataset {d_name.upper()} already completed (10 seeds). Skipping.")
            continue

        print(f"\n>>> Processing Tier-A Dataset: {d_name.upper()} ...")
        t_start_d = time.time()
        X, y = load_tier_a_dataset(d_name)
        N, D = X.shape
        K = len(np.unique(y))
        print(f"  Shape: N={N}, D={D}, K={K} (D/N = {D/N:.1f})")

        d_results = {
            "Raw": {"icc": [], "km": [], "ward": []},
            "NCG_BC": {"icc": [], "km": [], "ward": [], "n_active": [], "fallback": []},
            "G2_FixedBC": {"icc": [], "km": [], "ward": [], "n_selected": []},
            "G4_DipMatched": {"icc": [], "km": [], "ward": []},
        }

        # 1. Preprocess features label-free once per dataset (Section A2.1)
        X_z, eligible_mask = preprocess_features(X)

        # 2. Compute G2 (Fixed-cutoff BC) once (deterministic on X)
        bc_scores = compute_finite_sample_bc(X_z, eligible_mask)
        S_g2 = np.where(bc_scores >= 5.0 / 9.0)[0]
        max_cap = min(D, max(100, int(np.ceil(0.15 * D))))
        if len(S_g2) > max_cap:
            top_idx = np.argsort(bc_scores[S_g2])[-max_cap:]
            F_g2 = S_g2[top_idx]
        elif len(S_g2) >= 20:
            F_g2 = S_g2
        else:
            F_g2 = np.argsort(bc_scores)[-20:]

        # 3. Compute G4 Dip test statistics once (deterministic on X)
        _, dip_stats = evaluate_dip_pvalues(X_z, eligible_mask)

        for s in seeds:
            rng = np.random.default_rng(s)

            # G_prop: NCG-BC Gate (stochastic smoothed bootstrap decoy)
            t_gate_0 = time.time()
            ncg_res = ncg_bc_gate_accelerated(X, q=0.10, rng=rng)
            t_gate_1 = time.time()
            F_ncg = ncg_res["F_active"]
            k_matched = len(F_ncg)

            # G4: Dip test matched to k = |F_active|
            F_dip_matched = np.argsort(dip_stats)[-k_matched:]

            # Downstream clusterers
            km = KMeans(n_clusters=K, n_init=5, random_state=s)
            ward = AgglomerativeClustering(n_clusters=K, linkage="ward")
            icc = InvariantCoreConsensusV2(
                n_clusters=K,
                n_base_models=25,
                n_anchors=40,
                subspace_rate=0.25,
                core_quantile=0.5,
                random_state=s,
            )

            # Raw baseline
            d_results["Raw"]["km"].append(float(adjusted_rand_score(y, km.fit_predict(X))))
            d_results["Raw"]["ward"].append(float(adjusted_rand_score(y, ward.fit_predict(X))))
            d_results["Raw"]["icc"].append(float(adjusted_rand_score(y, icc.fit_predict(X))))

            # NCG-BC
            X_ncg = X[:, F_ncg]
            d_results["NCG_BC"]["km"].append(float(adjusted_rand_score(y, km.fit_predict(X_ncg))))
            d_results["NCG_BC"]["ward"].append(float(adjusted_rand_score(y, ward.fit_predict(X_ncg))))
            d_results["NCG_BC"]["icc"].append(float(adjusted_rand_score(y, icc.fit_predict(X_ncg))))
            d_results["NCG_BC"]["n_active"].append(int(len(F_ncg)))
            d_results["NCG_BC"]["fallback"].append(bool(ncg_res["fallback"]))

            # G2 (Fixed BC)
            X_g2 = X[:, F_g2]
            d_results["G2_FixedBC"]["km"].append(float(adjusted_rand_score(y, km.fit_predict(X_g2))))
            d_results["G2_FixedBC"]["ward"].append(float(adjusted_rand_score(y, ward.fit_predict(X_g2))))
            d_results["G2_FixedBC"]["icc"].append(float(adjusted_rand_score(y, icc.fit_predict(X_g2))))
            d_results["G2_FixedBC"]["n_selected"].append(int(len(F_g2)))

            # G4 (Dip matched-k)
            X_dip = X[:, F_dip_matched]
            d_results["G4_DipMatched"]["km"].append(float(adjusted_rand_score(y, km.fit_predict(X_dip))))
            d_results["G4_DipMatched"]["ward"].append(float(adjusted_rand_score(y, ward.fit_predict(X_dip))))
            d_results["G4_DipMatched"]["icc"].append(float(adjusted_rand_score(y, icc.fit_predict(X_dip))))

            print(
                f"    [Seed {s+1}/10] Gate: {t_gate_1 - t_gate_0:.2f}s | "
                f"NCG ARI={d_results['NCG_BC']['icc'][-1]:.3f} (k={k_matched}) | "
                f"G2 ARI={d_results['G2_FixedBC']['icc'][-1]:.3f} | "
                f"Dip ARI={d_results['G4_DipMatched']['icc'][-1]:.3f}",
                flush=True,
            )

        mean_ncg = np.mean(d_results["NCG_BC"]["icc"])
        mean_g2 = np.mean(d_results["G2_FixedBC"]["icc"])
        mean_dip = np.mean(d_results["G4_DipMatched"]["icc"])
        mean_raw = np.mean(d_results["Raw"]["icc"])
        t_elapsed_d = time.time() - t_start_d

        print(f"  Summary {d_name.upper()} ({t_elapsed_d:.1f}s total):")
        print(f"    ICC-v2 ARI: Raw={mean_raw:.3f} | NCG-BC={mean_ncg:.3f} | G2={mean_g2:.3f} | Dip-Matched={mean_dip:.3f}")
        print(f"    Diff vs G2: {mean_ncg - mean_g2:+.4f} | Diff vs Dip: {mean_ncg - mean_dip:+.4f}")

        results[d_name] = d_results

        # Checkpoint to disk after each dataset
        with open(out_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"  --> Checkpointed to {out_file}", flush=True)

        gc.collect()

    print("\n" + "=" * 80)
    print("EVALUATING CONFIRMATORY HYPOTHESIS H4 DECISION RULES")
    print("=" * 80)

    # Hypothesis H4 Evaluation across Tier-A Datasets
    diffs_vs_g2 = np.array([np.mean(results[d]["NCG_BC"]["icc"]) - np.mean(results[d]["G2_FixedBC"]["icc"]) for d in datasets])
    diffs_vs_dip = np.array([np.mean(results[d]["NCG_BC"]["icc"]) - np.mean(results[d]["G4_DipMatched"]["icc"]) for d in datasets])

    mean_diff_g2 = float(np.mean(diffs_vs_g2))
    ci_lower_g2, ci_upper_g2 = bootstrap_ci(diffs_vs_g2)
    non_neg_g2 = int(np.sum(diffs_vs_g2 >= 0))
    p_sign_g2 = compute_exact_sign_flip_p(diffs_vs_g2)

    mean_diff_dip = float(np.mean(diffs_vs_dip))
    ci_lower_dip, ci_upper_dip = bootstrap_ci(diffs_vs_dip)
    non_neg_dip = int(np.sum(diffs_vs_dip >= 0))
    p_sign_dip = compute_exact_sign_flip_p(diffs_vs_dip)

    # Holm-Bonferroni correction over the 2 comparisons:
    # Sort p-values: min_p checked at alpha/2 = 0.025, max_p checked at alpha = 0.05
    raw_p = [p_sign_g2, p_sign_dip]
    sorted_order = np.argsort(raw_p)
    holm_p = np.zeros(2)
    holm_p[sorted_order[0]] = min(1.0, raw_p[sorted_order[0]] * 2.0)
    holm_p[sorted_order[1]] = min(1.0, max(holm_p[sorted_order[0]], raw_p[sorted_order[1]]))

    print("\n--- Comparator 1: G2 (Fixed BC Rule) ---")
    print(f"Per-dataset paired ARI differences: {dict(zip(datasets, [round(x, 4) for x in diffs_vs_g2]))}")
    print(f"1. Mean ARI difference: {mean_diff_g2:+.4f} (Required: >= +0.02) -> {'PASS' if mean_diff_g2 >= 0.02 else 'FAIL'}")
    print(f"2. Bootstrap 95% CI: [{ci_lower_g2:+.4f}, {ci_upper_g2:+.4f}] (Required lower > 0) -> {'PASS' if ci_lower_g2 > 0 else 'FAIL'}")
    print(f"3. Non-negative datasets: {non_neg_g2}/6 (Required: >= 5) -> {'PASS' if non_neg_g2 >= 5 else 'FAIL'}")
    print(f"4. Exact sign-flip test: p = {p_sign_g2:.4f} (Holm-corrected p = {holm_p[0]:.4f}, Required <= 0.025) -> {'PASS' if p_sign_g2 <= 0.025 else 'FAIL'}")
    h4_g2_pass = (mean_diff_g2 >= 0.02) and (ci_lower_g2 > 0) and (non_neg_g2 >= 5) and (p_sign_g2 <= 0.025)
    print(f"==> H4 Supported vs G2: {h4_g2_pass}")

    print("\n--- Comparator 2: G4 (Hartigan Dip Matched-k) ---")
    print(f"Per-dataset paired ARI differences: {dict(zip(datasets, [round(x, 4) for x in diffs_vs_dip]))}")
    print(f"1. Mean ARI difference: {mean_diff_dip:+.4f} (Required: >= +0.02) -> {'PASS' if mean_diff_dip >= 0.02 else 'FAIL'}")
    print(f"2. Bootstrap 95% CI: [{ci_lower_dip:+.4f}, {ci_upper_dip:+.4f}] (Required lower > 0) -> {'PASS' if ci_lower_dip > 0 else 'FAIL'}")
    print(f"3. Non-negative datasets: {non_neg_dip}/6 (Required: >= 5) -> {'PASS' if non_neg_dip >= 5 else 'FAIL'}")
    print(f"4. Exact sign-flip test: p = {p_sign_dip:.4f} (Holm-corrected p = {holm_p[1]:.4f}, Required <= 0.025) -> {'PASS' if p_sign_dip <= 0.025 else 'FAIL'}")
    h4_dip_pass = (mean_diff_dip >= 0.02) and (ci_lower_dip > 0) and (non_neg_dip >= 5) and (p_sign_dip <= 0.025)
    print(f"==> H4 Supported vs G4: {h4_dip_pass}")

    # Summary decision
    summary_report = {
        "h4_supported_vs_g2": bool(h4_g2_pass),
        "h4_supported_vs_g4": bool(h4_dip_pass),
        "mean_diff_vs_g2": mean_diff_g2,
        "ci_vs_g2": [ci_lower_g2, ci_upper_g2],
        "non_neg_vs_g2": non_neg_g2,
        "p_sign_vs_g2": p_sign_g2,
        "mean_diff_vs_dip": mean_diff_dip,
        "ci_vs_dip": [ci_lower_dip, ci_upper_dip],
        "non_neg_vs_dip": non_neg_dip,
        "p_sign_vs_dip": p_sign_dip,
    }
    with open("results/study_null_gating/tier_a_h4_summary.json", "w") as f:
        json.dump(summary_report, f, indent=2)
    print(f"\nFinal H4 Decision Summary serialized to results/study_null_gating/tier_a_h4_summary.json")


if __name__ == "__main__":
    run_tier_a_benchmark()
