"""
Experiment 5: Extreme Asymptotic Scaling Stress Test.

Pushes ICC-v2 to large-scale data science and high-dimensional limits:
- Test A (Massive Sample Scaling):
  N in {10k, 50k, 100k, 500k, 1M}, D=100, K=5.
  Compares: ICC-v2 vs MiniBatchKMeans vs KMeans.
  Skips O(N^2) methods for N >= 100k.
  Uses chunked generation and float32 precision for N=1M.
  Measures: wall-clock time, peak memory (tracemalloc), and ARI/NMI recovery.

- Test B (Ultra-High Feature Dimension):
  D in {1k, 5k, 10k, 50k, 100k}, N=1,000, K=3.
  Compares: ICC-v2 vs KMeans vs PCA+KMeans.
  Measures: wall-clock time, peak memory, and ARI/NMI recovery.
"""

import os
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import PCA

# Add project root to sys.path
root_dir = Path(__file__).resolve().parents[3]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.icc.consensus_v2 import InvariantCoreConsensusV2
from src.icc.metrics import evaluate_all

EXP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = EXP_DIR / "data"
FIGURES_DIR = EXP_DIR / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def generate_synthetic_data(
    N: int,
    D: int,
    K: int = 5,
    seed: int = 42,
    chunk_size: int = 250000,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Memory-efficient generation of synthetic clustering benchmark data.
    Uses chunked generation and float32 precision to scale to N=1,000,000+
    without memory spikes or OOM errors.

    Signal: 2 informative dimensions with separated Gaussian cluster centers.
    Noise: D - 2 uninformative distractor dimensions.
    """
    rng = np.random.default_rng(seed)
    X = np.empty((N, D), dtype=np.float32)
    y = np.empty(N, dtype=np.int64)

    # 2 informative signal dimensions with well-separated Gaussian centers
    centers = rng.normal(scale=3.5, size=(K, 2)).astype(np.float32)

    n_per_cluster = N // K
    for k_idx in range(K):
        start_idx = k_idx * n_per_cluster
        end_idx = (k_idx + 1) * n_per_cluster if k_idx < K - 1 else N
        n_cluster = end_idx - start_idx
        y[start_idx:end_idx] = k_idx

        # Generate in chunks to avoid intermediate array allocation spikes
        c_offset = 0
        while c_offset < n_cluster:
            c_len = min(chunk_size, n_cluster - c_offset)
            c_start = start_idx + c_offset
            c_end = c_start + c_len

            # Signal dimensions (clusters + intra-cluster variance)
            X[c_start:c_end, :2] = centers[k_idx] + rng.normal(scale=0.75, size=(c_len, 2)).astype(np.float32)

            # Noise distractor dimensions
            if D > 2:
                X[c_start:c_end, 2:] = rng.normal(scale=1.0, size=(c_len, D - 2)).astype(np.float32)

            c_offset += c_len

    # In-place column standardization (zero mean, unit variance)
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    std[std < 1e-7] = 1.0
    X -= mean
    X /= std

    return X, y


def run_sample_scale_test(
    sample_sizes: Optional[list] = None,
    n_trials: int = 3,
) -> pd.DataFrame:
    """
    Test A: Massive Sample Scaling N in {10k, 50k, 100k, 500k, 1M}, D=100, K=5.
    Compares: ICC-v2 vs MiniBatchKMeans vs KMeans.
    Skips O(N^2) methods for N >= 100k.
    """
    if sample_sizes is None:
        sample_sizes = [10000, 50000, 100000, 500000, 1000000]

    print("=" * 80)
    print(f"[*] Running Exp 5 Test A: Sample Scaling N in {sample_sizes} (D=100, K=5)...")
    print("=" * 80)

    records = []
    K = 5
    D = 100

    for N in sample_sizes:
        print(f"\n--- Benchmark N = {N:,} (D={D}, K={K}) ---")

        for trial in range(n_trials):
            seed = 42 + trial * 31

            # Generate synthetic data with float32 precision
            t_gen_start = time.perf_counter()
            X, y = generate_synthetic_data(N=N, D=D, K=K, seed=seed)
            t_gen = time.perf_counter() - t_gen_start
            print(f"  [Gen] Data generated in {t_gen:.2f}s ({X.nbytes / (1024*1024):.1f} MB in RAM)")

            # -------------------------------------------------------------
            # 1. ICC-v2 (Scalable Anchor Consensus)
            # -------------------------------------------------------------
            tracemalloc.start()
            t0 = time.perf_counter()
            icc = InvariantCoreConsensusV2(
                n_clusters=K,
                n_base_models=15,
                n_anchors=60,
                random_state=seed,
            )
            labels_icc = icc.fit_predict(X)
            t_icc = time.perf_counter() - t0
            _, peak_mem_icc = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            scores_icc = evaluate_all(y, labels_icc)
            ari_icc = scores_icc["ari"]
            nmi_icc = scores_icc["nmi"]
            mem_icc_mb = peak_mem_icc / (1024 * 1024)

            # -------------------------------------------------------------
            # 2. MiniBatchKMeans (Streaming Baseline)
            # -------------------------------------------------------------
            tracemalloc.start()
            t0 = time.perf_counter()
            batch_sz = min(2048, N)
            mbk = MiniBatchKMeans(
                n_clusters=K,
                batch_size=batch_sz,
                random_state=seed,
                n_init=1,
            )
            labels_mbk = mbk.fit_predict(X)
            t_mbk = time.perf_counter() - t0
            _, peak_mem_mbk = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            scores_mbk = evaluate_all(y, labels_mbk)
            ari_mbk = scores_mbk["ari"]
            nmi_mbk = scores_mbk["nmi"]
            mem_mbk_mb = peak_mem_mbk / (1024 * 1024)

            # -------------------------------------------------------------
            # 3. Standard KMeans (Full-Space Baseline)
            # Skip O(N^2) or heavy batch algorithms for N >= 500k
            # -------------------------------------------------------------
            if N <= 100000:
                tracemalloc.start()
                t0 = time.perf_counter()
                km = KMeans(
                    n_clusters=K,
                    n_init=1,
                    max_iter=60,
                    random_state=seed,
                )
                labels_km = km.fit_predict(X)
                t_km = time.perf_counter() - t0
                _, peak_mem_km = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                scores_km = evaluate_all(y, labels_km)
                ari_km = scores_km["ari"]
                nmi_km = scores_km["nmi"]
                mem_km_mb = peak_mem_km / (1024 * 1024)
            else:
                # Explicitly skip standard full-batch KMeans for N >= 500k
                t_km = np.nan
                mem_km_mb = np.nan
                ari_km = np.nan
                nmi_km = np.nan

            print(
                f"  Trial {trial+1}/{n_trials}: "
                f"ICC-v2={t_icc:.2f}s (RAM={mem_icc_mb:.1f}MB, ARI={ari_icc:.3f}) | "
                f"MiniBatchKMeans={t_mbk:.2f}s (RAM={mem_mbk_mb:.1f}MB, ARI={ari_mbk:.3f}) | "
                f"KMeans={'SKIPPED' if np.isnan(t_km) else f'{t_km:.2f}s (ARI={ari_km:.3f})'}"
            )

            records.append({
                "N": N,
                "D": D,
                "K": K,
                "trial": trial,
                "seed": seed,
                "time_icc": t_icc,
                "time_mbk": t_mbk,
                "time_km": t_km,
                "mem_icc_mb": mem_icc_mb,
                "mem_mbk_mb": mem_mbk_mb,
                "mem_km_mb": mem_km_mb,
                "ari_icc": ari_icc,
                "ari_mbk": ari_mbk,
                "ari_km": ari_km,
                "nmi_icc": nmi_icc,
                "nmi_mbk": nmi_mbk,
                "nmi_km": nmi_km,
            })

    df = pd.DataFrame(records)
    out_csv = DATA_DIR / "exp5_sample_scaling_results.csv"
    df.to_csv(out_csv, index=False)
    print(f"\n[+] Saved Sample Scaling results to {out_csv}")
    return df


def run_dimension_scale_test(
    dims_list: Optional[list] = None,
    n_trials: int = 3,
) -> pd.DataFrame:
    """
    Test B: Ultra-High Feature Dimension D in {1k, 5k, 10k, 50k, 100k}, N=1,000, K=3.
    Compares: ICC-v2 vs KMeans vs PCA+KMeans.
    """
    if dims_list is None:
        dims_list = [1000, 5000, 10000, 50000, 100000]

    print("=" * 80)
    print(f"[*] Running Exp 5 Test B: Dimension Scaling D in {dims_list} (N=1,000, K=3)...")
    print("=" * 80)

    records = []
    N = 1000
    K = 3

    for D in dims_list:
        print(f"\n--- Benchmark D = {D:,} (N={N}, K={K}) ---")

        for trial in range(n_trials):
            seed = 42 + trial * 37

            t_gen_start = time.perf_counter()
            X, y = generate_synthetic_data(N=N, D=D, K=K, seed=seed)
            t_gen = time.perf_counter() - t_gen_start

            # -------------------------------------------------------------
            # 1. ICC-v2 (Variance-Guided Subspace Gating + Anchors)
            # -------------------------------------------------------------
            tracemalloc.start()
            t0 = time.perf_counter()
            icc = InvariantCoreConsensusV2(
                n_clusters=K,
                n_base_models=15,
                n_anchors=50,
                random_state=seed,
            )
            labels_icc = icc.fit_predict(X)
            t_icc = time.perf_counter() - t0
            _, peak_mem_icc = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            scores_icc = evaluate_all(y, labels_icc)
            ari_icc = scores_icc["ari"]
            nmi_icc = scores_icc["nmi"]
            mem_icc_mb = peak_mem_icc / (1024 * 1024)

            # -------------------------------------------------------------
            # 2. Standard KMeans (Full Space)
            # -------------------------------------------------------------
            tracemalloc.start()
            t0 = time.perf_counter()
            km = KMeans(
                n_clusters=K,
                n_init=1,
                max_iter=50,
                random_state=seed,
            )
            labels_km = km.fit_predict(X)
            t_km = time.perf_counter() - t0
            _, peak_mem_km = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            scores_km = evaluate_all(y, labels_km)
            ari_km = scores_km["ari"]
            nmi_km = scores_km["nmi"]
            mem_km_mb = peak_mem_km / (1024 * 1024)

            # -------------------------------------------------------------
            # 3. PCA + KMeans (Classical Dimensionality Reduction)
            # -------------------------------------------------------------
            tracemalloc.start()
            t0 = time.perf_counter()
            pca = PCA(n_components=min(10, N, D), random_state=seed)
            X_pca = pca.fit_transform(X)
            km_pca = KMeans(n_clusters=K, n_init=1, random_state=seed)
            labels_pca = km_pca.fit_predict(X_pca)
            t_pca = time.perf_counter() - t0
            _, peak_mem_pca = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            scores_pca = evaluate_all(y, labels_pca)
            ari_pca = scores_pca["ari"]
            nmi_pca = scores_pca["nmi"]
            mem_pca_mb = peak_mem_pca / (1024 * 1024)

            print(
                f"  Trial {trial+1}/{n_trials}: "
                f"ICC-v2={t_icc:.2f}s (ARI={ari_icc:.3f}) | "
                f"KMeans={t_km:.2f}s (ARI={ari_km:.3f}) | "
                f"PCA+KM={t_pca:.2f}s (ARI={ari_pca:.3f})"
            )

            records.append({
                "N": N,
                "D": D,
                "K": K,
                "trial": trial,
                "seed": seed,
                "time_icc": t_icc,
                "time_km": t_km,
                "time_pca": t_pca,
                "mem_icc_mb": mem_icc_mb,
                "mem_km_mb": mem_km_mb,
                "mem_pca_mb": mem_pca_mb,
                "ari_icc": ari_icc,
                "ari_km": ari_km,
                "ari_pca": ari_pca,
                "nmi_icc": nmi_icc,
                "nmi_km": nmi_km,
                "nmi_pca": nmi_pca,
            })

    df = pd.DataFrame(records)
    out_csv = DATA_DIR / "exp5_dimension_scaling_results.csv"
    df.to_csv(out_csv, index=False)
    print(f"\n[+] Saved Dimension Scaling results to {out_csv}")
    return df


def run_all(n_trials: int = 3):
    t0 = time.time()
    run_sample_scale_test(
        sample_sizes=[10000, 50000, 100000, 500000, 1000000],
        n_trials=n_trials,
    )
    run_dimension_scale_test(
        dims_list=[1000, 5000, 10000, 50000, 100000],
        n_trials=n_trials,
    )
    print(f"\n[OK] Exp 5 execution completed successfully in {time.time() - t0:.2f}s")


if __name__ == "__main__":
    run_all(n_trials=3)
