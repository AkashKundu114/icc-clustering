"""
Clean Scalability Benchmark for Task B5.
Runs sample scaling across N in [200, 500, 1000, 2000, 5000, 8000, 10000]
across 5 random seeds under a unified protocol.
Measures wall-clock runtime, tracemalloc peak, process RSS, and theoretical graph memory.
"""

import sys
import time
import os
import tracemalloc
from pathlib import Path
import psutil
import numpy as np
import pandas as pd

# Add project root
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))

from icc.baselines.consensus import (
    run_standard_consensus,
    run_li_et_al_2019,
    run_icc_v1,
    run_icc_v2,
)

DATA_DIR = root / "experiments" / "exp4_scalability_and_sensitivity" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_CSV = DATA_DIR / "exp4_sample_scaling_results.csv"
SUMMARY_CSV = DATA_DIR / "exp4_sample_scaling_summary.csv"


def generate_benchmark_synthetic(n_samples, n_features=200, k=3, seed=42):
    rng = np.random.default_rng(seed)
    n_per_cluster = n_samples // k
    X_list = []
    y_list = []
    centers = rng.uniform(-3.0, 3.0, size=(k, min(5, n_features)))
    for c in range(k):
        pts = rng.normal(loc=0.0, scale=1.0, size=(n_per_cluster, n_features))
        pts[:, :centers.shape[1]] += centers[c]
        X_list.append(pts)
        y_list.append(np.full(n_per_cluster, c, dtype=int))
    X = np.vstack(X_list)
    y = np.concatenate(y_list)
    return X, y


def benchmark_single(model_name, model_fn, X, k, seed, L=40):
    proc = psutil.Process(os.getpid())
    rss_before = proc.memory_info().rss / (1024.0 * 1024.0)

    tracemalloc.start()
    t0 = time.perf_counter()
    pred, elapsed, meta = model_fn(X, k, seed=seed)
    runtime = time.perf_counter() - t0
    current, peak_trace = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_trace_mb = peak_trace / (1024.0 * 1024.0)
    rss_after = proc.memory_info().rss / (1024.0 * 1024.0)
    peak_rss_mb = max(rss_after, rss_before + peak_trace_mb)

    N = X.shape[0]
    if model_name == "ICC_v2":
        graph_mem_mb = (N * L + L * L) * 8.0 / (1024.0 * 1024.0)
    else:
        graph_mem_mb = (N * N) * 8.0 / (1024.0 * 1024.0)

    n_core = getattr(meta, "n_core", 0) if meta else 0

    return {
        "runtime_sec": runtime,
        "peak_trace_mb": peak_trace_mb,
        "peak_rss_mb": peak_rss_mb,
        "graph_mem_mb": graph_mem_mb,
        "n_core": n_core,
    }


def main():
    n_values = [200, 500, 1000, 2000, 5000, 8000, 10000]
    seeds = [42, 101, 202, 303, 404]
    fixed_dim = 200
    k = 3
    L = 40

    models = {
        "Standard_Consensus": run_standard_consensus,
        "Li_et_al_2019": run_li_et_al_2019,
        "ICC_v1": run_icc_v1,
        "ICC_v2": run_icc_v2,
    }

    records = []
    print("=" * 80)
    print("EXPERIMENT 4: SINGLE-PROTOCOL SAMPLE SCALING BENCHMARK (5 SEEDS)")
    print(f"Sample sizes: {n_values}")
    print(f"Features: D={fixed_dim}, Clusters: K={k}, Anchors: L={L}")
    print("=" * 80)

    for n in n_values:
        print(f"\n---> Evaluating N = {n} ...")
        for s_idx, seed in enumerate(seeds):
            X, y = generate_benchmark_synthetic(n, fixed_dim, k=k, seed=seed)
            for mname, mfn in models.items():
                res = benchmark_single(mname, mfn, X, k, seed, L=L)
                rec = {
                    "N": n,
                    "D": fixed_dim,
                    "K": k,
                    "model": mname,
                    "trial": s_idx,
                    "seed": seed,
                    "runtime_sec": res["runtime_sec"],
                    "peak_memory_mb": res["peak_trace_mb"],
                    "peak_rss_mb": res["peak_rss_mb"],
                    "graph_mem_mb": res["graph_mem_mb"],
                    "lc": res["n_core"],
                    "oom": False,
                }
                records.append(rec)
                print(f"   [Seed {seed}] {mname:<18} | Time: {res['runtime_sec']:6.3f}s | "
                      f"Trace: {res['peak_trace_mb']:6.2f} MB | Graph: {res['graph_mem_mb']:6.2f} MB")

    df = pd.DataFrame(records)
    df.to_csv(RAW_CSV, index=False)
    print(f"\n[+] Raw results written to: {RAW_CSV}")

    # Compute aggregation
    summary = df.groupby(["N", "model"]).agg({
        "runtime_sec": ["mean", "std"],
        "peak_memory_mb": ["mean", "std"],
        "peak_rss_mb": ["mean", "std"],
        "graph_mem_mb": ["mean"],
    }).reset_index()

    summary.columns = [
        "N", "model",
        "runtime_mean", "runtime_std",
        "peak_trace_mean", "peak_trace_std",
        "peak_rss_mean", "peak_rss_std",
        "graph_mem_mb",
    ]
    summary.to_csv(SUMMARY_CSV, index=False)
    print(f"[+] Summary written to: {SUMMARY_CSV}")


if __name__ == "__main__":
    main()
