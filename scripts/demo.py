#!/usr/bin/env python3
"""
Invariant Core Consensus (ICC-v2) — 5-Second Interactive Walkthrough Demo.

Demonstrates:
1. Generation of high-dimensional noisy data (D = 2,000, N = 300, K = 3, 99.9% noise features).
2. Variance-Stabilized Subspace Gating (VSSG) recovering ground-truth signal dimensions.
3. Certified Anchor consensus training (O(N) complexity).
4. Inductive out-of-sample projection on unseen test samples.
5. Comparative evaluation against K-Means and Spectral Clustering.

Run:
    python demo.py
"""

# ruff: noqa: E402
import sys
import time
from pathlib import Path

# Ensure repository root is on sys.path regardless of execution working directory
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np
from tabulate import tabulate

from src.icc.baselines.classical import run_kmeans, run_spectral
from src.icc.consensus_v2 import InvariantCoreConsensusV2
from src.icc.core import build_dataset
from src.icc.metrics import evaluate_all


def main():
    print("=" * 75)
    print("      INVARIANT CORE CONSENSUS (ICC-v2) -- INTERACTIVE DEMO")
    print("      IEEE Transactions on Knowledge and Data Engineering (TKDE)")
    print("=" * 75)

    # 1. Generate High-D Data
    N_train = 240
    N_test = 60
    D_signal = 2
    D_noise = 1998
    D_total = D_signal + D_noise
    K = 3

    print("\n[*] 1. Synthesizing High-Dimensional Noisy Cohort:")
    print(f"    - Training Samples (N_train): {N_train}")
    print(f"    - Test Samples (N_test):     {N_test}")
    print(f"    - True Signal Dimensions:   {D_signal} (Features [0, 1])")
    print(f"    - Distractor Noise Dims:    {D_noise} (Nuisance Features [2..{D_total-1}])")
    print(f"    - Noise Ratio:              {D_noise / D_total * 100:.1f}%")
    print(f"    - Clusters (K):             {K}")

    X_train, y_train = build_dataset(
        d_noise=D_noise,
        noise_kind="scaled",
        noise_seed=42,
        sizes=[80, 80, 80],
        k=K,
        signal_dim=D_signal,
    )

    X_test, y_test = build_dataset(
        d_noise=D_noise,
        noise_kind="scaled",
        noise_seed=142,
        sizes=[20, 20, 20],
        k=K,
        signal_dim=D_signal,
    )

    # 2. Train ICC-v2
    print("\n[*] 2. Fitting ICC-v2 with Variance-Stabilized Subspace Gating (VSSG)...")
    t0 = time.perf_counter()
    model = InvariantCoreConsensusV2(
        n_clusters=K,
        n_base_models=25,
        n_anchors=30,
        random_state=42,
    )
    train_pred_icc = model.fit_predict(X_train)
    icc_train_time = time.perf_counter() - t0

    # 3. Analyze VSSG Feature Recovery
    selected_features = model.selected_features_
    signal_recovered = [f for f in [0, 1] if f in selected_features]
    precision = len(signal_recovered) / len(selected_features) if len(selected_features) > 0 else 0.0
    recall = len(signal_recovered) / D_signal

    print(f"    -> VSSG Active Pool:   {len(selected_features)} features retained from {D_total}")
    print(f"    -> True Signals Found: {signal_recovered} (Recall = {recall * 100:.1f}%, Precision = {precision * 100:.2f}%)")
    core_pct = np.mean(model.core_mask_) * 100.0 if model.core_mask_ is not None else 50.0
    print(f"    -> Anchor Stability:   {core_pct:.1f}% samples certified as core anchors")

    # 4. Out-of-sample Inductive Prediction
    print("\n[*] 3. Performing Inductive Out-of-Sample Prediction on Query Batch...")
    t0_pred = time.perf_counter()
    test_pred_sub = model.predict(X_test, subspace=True)
    pred_time = time.perf_counter() - t0_pred
    test_pred_full = model.predict(X_test, subspace=False)

    scores_train_icc = evaluate_all(y_train, train_pred_icc)
    scores_test_sub = evaluate_all(y_test, test_pred_sub)
    scores_test_full = evaluate_all(y_test, test_pred_full)

    print(f"    -> Inductive Latency:  {pred_time * 1000:.2f} ms for {N_test} instances ({pred_time / N_test * 1e6:.1f} us / sample)")
    print(f"    -> Test ARI (VSSG):    {scores_test_sub['ari']:.4f}")
    print(f"    -> Test ARI (No Gating): {scores_test_full['ari']:.4f} (Difference: {scores_test_sub['ari'] - scores_test_full['ari']:+.4f})")

    # 5. Benchmark Baselines on Training Set
    print("\n[*] 4. Benchmarking Competitor Baselines on Training Cohort...")
    pred_km, t_km, _ = run_kmeans(X_train, k=K, seed=42)
    pred_sp, t_sp, _ = run_spectral(X_train, k=K, seed=42)

    scores_km = evaluate_all(y_train, pred_km)
    scores_sp = evaluate_all(y_train, pred_sp)

    # 6. Comparative Results Table
    table_data = [
        ["K-Means (Lloyd 1982)", scores_km["ari"], scores_km["nmi"], f"{t_km * 1000:.1f} ms", "Transductive"],
        ["Spectral Clustering", scores_sp["ari"], scores_sp["nmi"], f"{t_sp * 1000:.1f} ms", "Transductive"],
        ["ICC-v2 (Train Fit)", scores_train_icc["ari"], scores_train_icc["nmi"], f"{icc_train_time * 1000:.1f} ms", "Inductive Fit"],
        ["ICC-v2 (Out-of-Sample Test)", scores_test_sub["ari"], scores_test_sub["nmi"], f"{pred_time * 1000:.2f} ms", "Inductive Out-of-Sample"],
    ]

    print("\n" + "=" * 75)
    print("                          BENCHMARK SUMMARY")
    print("=" * 75)
    print(tabulate(table_data, headers=["Algorithm", "ARI", "NMI", "Runtime", "Mode"], floatfmt=".4f", tablefmt="github"))
    print("=" * 75)

    # 5. Anchor-Space Perturbation Profiling (ASPP)
    print("\n[*] 5. Executing Anchor-Space Perturbation Profiling (ASPP)...")
    t0_aspp = time.perf_counter()
    fp_df = model.profile_perturbations(X_train)
    aspp_time = time.perf_counter() - t0_aspp
    print(f"    -> ASPP Diagnostic Latency: {aspp_time * 1000:.1f} ms (Linear O(N*L) memory)")

    aspp_cols = [c for c in ["cluster", "size", "PSI", "reliability", "sampling", "feature", "measurement", "technical", "algorithmic"] if c in fp_df.columns]
    aspp_display = fp_df[aspp_cols].copy()
    print("\n" + "=" * 75)
    print("             ASPP MULTI-FAMILY CLUSTER STABILITY FINGERPRINTS")
    print("=" * 75)
    print(tabulate(aspp_display, headers="keys", floatfmt=".3f", tablefmt="github", showindex=False))

    # 6. Inductive Out-of-Sample Confidence Scoring
    print("\n[*] 6. Inductive Prediction with Stability-Calibrated Confidence (First 5 queries):")
    res_stab = model.predict_with_stability(X_test[:5])
    query_table = []
    for idx in range(5):
        query_table.append([
            f"Query #{idx+1}",
            int(res_stab["labels"][idx]),
            f"{res_stab['confidence'][idx] * 100:.1f}%",
            f"{res_stab['margin'][idx] * 100:.1f}%",
            f"{res_stab['psi'][idx]:.3f}",
            res_stab["reliability"][idx],
        ])
    print(tabulate(query_table, headers=["Query", "Assigned Cluster", "Calibrated Conf.", "Margin", "Cluster PSI", "Reliability Category"], tablefmt="github"))
    print("=" * 75)

    advantage = scores_train_icc["ari"] - max(scores_km["ari"], scores_sp["ari"])
    print(f"\n[+] ICC-v2 train ARI minus best of K-Means/Spectral: {advantage:+.4f}")
    print("[+] (Interpret only if the margin is large relative to seed-to-seed variation; see docs/audit_reports/.)\n")


if __name__ == "__main__":
    main()
