"""
Experiment 4.3: Anchor Approximation Fidelity & O(N) vs O(N^2) Complexity Tradeoff.

Rigorous theoretical and empirical comparison between:
1. ICC-v2-Exact (Dense O(N^2) co-association with VSSG feature gating)
2. ICC-v2-Reduced (Bipartite O(NL) anchor graph consensus)

Quantifies:
- Fidelity gap Delta_ARI = ARI_exact - ARI_reduced
- Runtime speedup ratio T_exact / T_reduced
- Memory footprint delta M_exact vs M_reduced
"""

import os
import time
import tracemalloc
from pathlib import Path
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch
import scipy.linalg as sla
from scipy.stats import kurtosis, skew

from src.icc.core import build_dataset, run_clusterer, pairwise_coassoc
from src.icc.metrics import evaluate_all
from src.icc.consensus_v2 import InvariantCoreConsensusV2

EXP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = EXP_DIR / "data"
FIGURES_DIR = EXP_DIR / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def run_icc_v2_exact(X, k, n_base_models=25, seed=42):
    """
    Exact O(N^2) baseline: Uses full pairwise co-association matrix S,
    identical VSSG feature gating, and dense spectral decomposition.
    """
    t0 = time.perf_counter()
    N, D = X.shape
    rng = np.random.default_rng(seed)

    # VSSG feature scoring
    kurt = kurtosis(X, axis=0)
    sk = skew(X, axis=0)
    bimodal = (sk**2 + 1.0) / (kurt + 3.0 + 1e-5)
    top_frac = min(1.0, max(0.15, 100.0 / D))
    pool_size = max(k, int(top_frac * D))
    candidate_pool = np.argsort(bimodal)[-pool_size:]
    sub_size = max(2, int(len(candidate_pool) * 0.30))

    # Base models
    partitions = []
    base_engine = "spectral" if N <= 100 else "kmeans"
    for m in range(n_base_models):
        seed_m = int(rng.integers(0, 1000000))
        sub_idx = rng.choice(candidate_pool, size=sub_size, replace=False)
        p = run_clusterer(base_engine, X[:, sub_idx], k, seed=seed_m)
        partitions.append(p)

    # Dense N x N co-association matrix
    H = np.zeros((N, n_base_models * k), dtype=np.float32)
    for m, p in enumerate(partitions):
        H[np.arange(N), m * k + p] = 1.0
    S = (H @ H.T) / float(n_base_models)

    # Dense Normalized Laplacian Spectral Embedding
    deg = S.sum(axis=1)
    deg_inv_sqrt = 1.0 / np.sqrt(np.fmax(deg, 1e-12))
    L_norm = np.eye(N, dtype=np.float32) - (deg_inv_sqrt[:, None] * S * deg_inv_sqrt[None, :])

    evals, evecs = sla.eigh(L_norm, subset_by_index=[0, k - 1])
    U_emb = evecs[:, :k]
    emb_norm = np.linalg.norm(U_emb, axis=1, keepdims=True)
    emb_norm[emb_norm < 1e-12] = 1.0
    U_emb /= emb_norm

    pred = run_clusterer("kmeans", U_emb, k, seed=seed)
    return pred, time.perf_counter() - t0


def run_fidelity_sweep(n_samples_list=None, n_trials=5, output_csv=None):
    """
    Sweeps sample size N and compares Reduced vs Exact.
    """
    if n_samples_list is None:
        n_samples_list = [200, 500, 1000, 2000, 5000, 10000]

    if output_csv is None:
        output_csv = DATA_DIR / "exp4_3_anchor_fidelity_results.csv"

    print(f"[*] Starting Exp 4.3 Anchor Fidelity Sweep across N in {n_samples_list} ({n_trials} trials per N)...")
    records = []
    t_start = time.time()

    for N in n_samples_list:
        rem = N % 3
        sizes = [N // 3 + (1 if i < rem else 0) for i in range(3)]
        print(f"\n--- Testing N = {N} (sizes = {sizes}, D = 200, K = 3) ---")

        for trial in range(n_trials):
            seed = 42 + trial * 17
            X, y = build_dataset(
                d_noise=198,
                noise_kind="scaled",
                noise_seed=seed,
                sizes=sizes,
                k=3,
                signal_dim=2,
            )

            # 1. Benchmark ICC-v2 Reduced (O(N))
            tracemalloc.start()
            t0 = time.perf_counter()
            model_red = InvariantCoreConsensusV2(n_clusters=3, n_base_models=25, n_anchors=40, random_state=seed)
            labels_red = model_red.fit_predict(X)
            t_red = time.perf_counter() - t0
            _, peak_mem_red = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # 2. Benchmark ICC-v2 Exact (O(N^2))
            tracemalloc.start()
            t0 = time.perf_counter()
            labels_exact, t_exact = run_icc_v2_exact(X, k=3, n_base_models=25, seed=seed)
            _, peak_mem_exact = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Metrics
            scores_red = evaluate_all(y, labels_red)
            scores_exact = evaluate_all(y, labels_exact)

            delta_ari = scores_exact["ari"] - scores_red["ari"]
            delta_nmi = scores_exact["nmi"] - scores_red["nmi"]
            speedup = t_exact / max(t_red, 1e-6)
            mem_red_mb = peak_mem_red / (1024 * 1024)
            mem_exact_mb = peak_mem_exact / (1024 * 1024)
            mem_savings = ((mem_exact_mb - mem_red_mb) / max(mem_exact_mb, 1e-6)) * 100

            print(f"  Trial {trial+1}/{n_trials}: ARI_red={scores_red['ari']:.4f}, ARI_exact={scores_exact['ari']:.4f}, "
                  f"Delta_ARI={delta_ari:+.4f}, Speedup={speedup:.2f}x, MemSavings={mem_savings:.1f}%")

            records.append({
                "N": X.shape[0],
                "D": X.shape[1],
                "trial": trial,
                "ari_reduced": scores_red["ari"],
                "ari_exact": scores_exact["ari"],
                "delta_ari": delta_ari,
                "nmi_reduced": scores_red["nmi"],
                "nmi_exact": scores_exact["nmi"],
                "delta_nmi": delta_nmi,
                "time_reduced": t_red,
                "time_exact": t_exact,
                "speedup": speedup,
                "mem_reduced_mb": mem_red_mb,
                "mem_exact_mb": mem_exact_mb,
                "mem_savings_pct": mem_savings,
            })

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    print(f"\n[OK] Exp 4.3 completed in {time.time() - t_start:.2f}s")
    print(f"[+] Saved results to {output_csv} ({len(df)} total runs)")
    return df


def run_fidelity_experiment(trials_per_n=5, n_samples_list=None, output_csv=None):
    """Alias for run_fidelity_sweep for standard experiment invocation."""
    return run_fidelity_sweep(n_samples_list=n_samples_list, n_trials=trials_per_n, output_csv=output_csv)


if __name__ == "__main__":
    run_fidelity_sweep(n_samples_list=[200, 500, 1000], n_trials=2)

