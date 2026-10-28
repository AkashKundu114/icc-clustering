"""
Scalability and Computational Complexity Benchmark for Experiment 4.
Evaluates empirical runtime (seconds) and peak memory footprint (MB) across
scaling sample sizes N in [200, 10000] and feature dimensions D in [100, 20000].
"""

import os
import sys
import time
import tracemalloc
from pathlib import Path
import numpy as np
import pandas as pd

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from icc.core import run_clusterer, pairwise_coassoc
from sklearn.metrics import adjusted_rand_score
from experiments.exp3_real_world_benchmarks.src.benchmark_models import (
    run_standard_consensus,
    run_li_et_al_2019,
    run_icc_v1,
    run_icc_v2
)

SAMPLE_SCALING_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "exp4_sample_scaling_results.csv")
DIM_SCALING_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "exp4_dim_scaling_results.csv")


def generate_benchmark_synthetic(n_samples, n_features, k=3, seed=42):
    rng = np.random.default_rng(seed)
    n_per_cluster = n_samples // k
    X_list = []
    y_list = []
    
    # Generate 3 cluster centers in first 5 dimensions, rest noise
    centers = rng.uniform(-3.0, 3.0, size=(k, min(5, n_features)))
    for c in range(k):
        pts = rng.normal(loc=0.0, scale=1.0, size=(n_per_cluster, n_features))
        pts[:, :centers.shape[1]] += centers[c]
        X_list.append(pts)
        y_list.append(np.full(n_per_cluster, c, dtype=int))
        
    X = np.vstack(X_list)
    y = np.concatenate(y_list)
    return X, y


def benchmark_model_execution(model_name, model_fn, X, k, seed=42):
    """
    Executes model with tracemalloc to capture peak memory (MB) and wall-clock time (sec).
    """
    tracemalloc.start()
    t0 = time.perf_counter()
    try:
        pred, elapsed, lc = model_fn(X, k, seed=seed)
        t_total = time.perf_counter() - t0
        current, peak = tracemalloc.get_traced_memory()
        peak_mb = peak / (1024.0 * 1024.0)
        oom = False
    except MemoryError:
        t_total = np.nan
        peak_mb = np.nan
        pred = None
        lc = 0
        oom = True
    finally:
        tracemalloc.stop()
        
    return t_total, peak_mb, lc, oom


def run_sample_scaling_experiment(
    n_values=[200, 500, 1000, 2000, 5000, 8000],
    fixed_dim=200,
    k=3,
    n_trials=3
):
    print("=" * 80)
    print("EXPERIMENT 4A: SAMPLE COMPLEXITY SCALING BENCHMARK (N in [200, 8000])")
    print(f"Fixed Dimension: D = {fixed_dim}, Target Clusters: K = {k}")
    print("=" * 80)
    
    models = {
        "Standard_Consensus": run_standard_consensus,
        "Li_et_al_2019": run_li_et_al_2019,
        "ICC_v1": run_icc_v1,
        "ICC_v2": run_icc_v2,
    }
    
    records = []
    
    for n in n_values:
        print(f"\n---> Testing N = {n} samples...")
        for trial in range(n_trials):
            seed = 42 + trial * 101
            X, y = generate_benchmark_synthetic(n, fixed_dim, k=k, seed=seed)
            
            for mname, mfn in models.items():
                # Avoid quadratic explosion beyond 5000 for standard consensus if memory permits
                if n > 5000 and mname in ["Standard_Consensus", "Li_et_al_2019"] and trial > 0:
                    # Skip duplicate slow runs on large N
                    continue
                    
                t_sec, peak_mb, lc, oom = benchmark_model_execution(mname, mfn, X, k, seed=seed)
                records.append({
                    "N": n,
                    "D": fixed_dim,
                    "K": k,
                    "model": mname,
                    "trial": trial,
                    "seed": seed,
                    "runtime_sec": t_sec,
                    "peak_memory_mb": peak_mb,
                    "lc": lc,
                    "oom": oom
                })
                print(f"     {mname:<20}: Time = {t_sec:6.3f}s | Peak RAM = {peak_mb:6.2f} MB | Anchors Lc = {lc}")
                
    df = pd.DataFrame(records)
    df.to_csv(SAMPLE_SCALING_CSV, index=False)
    print(f"\n[+] Sample scaling results saved to: {SAMPLE_SCALING_CSV}")
    return df


def run_dimension_scaling_experiment(
    d_values=[100, 500, 2000, 5000, 10000, 20000],
    fixed_n=500,
    k=3,
    n_trials=3
):
    print("\n" + "=" * 80)
    print("EXPERIMENT 4B: FEATURE DIMENSION SCALING BENCHMARK (D in [100, 20000])")
    print(f"Fixed Sample Size: N = {fixed_n}, Target Clusters: K = {k}")
    print("=" * 80)
    
    models = {
        "Standard_Consensus": run_standard_consensus,
        "Li_et_al_2019": run_li_et_al_2019,
        "ICC_v1": run_icc_v1,
        "ICC_v2": run_icc_v2,
    }
    
    records = []
    
    for d in d_values:
        print(f"\n---> Testing D = {d} features...")
        for trial in range(n_trials):
            seed = 42 + trial * 101
            X, y = generate_benchmark_synthetic(fixed_n, d, k=k, seed=seed)
            
            for mname, mfn in models.items():
                t_sec, peak_mb, lc, oom = benchmark_model_execution(mname, mfn, X, k, seed=seed)
                records.append({
                    "N": fixed_n,
                    "D": d,
                    "K": k,
                    "model": mname,
                    "trial": trial,
                    "seed": seed,
                    "runtime_sec": t_sec,
                    "peak_memory_mb": peak_mb,
                    "lc": lc,
                    "oom": oom
                })
                print(f"     {mname:<20}: Time = {t_sec:6.3f}s | Peak RAM = {peak_mb:6.2f} MB")
                
    df = pd.DataFrame(records)
    df.to_csv(DIM_SCALING_CSV, index=False)
    print(f"\n[+] Dimension scaling results saved to: {DIM_SCALING_CSV}")
    return df


if __name__ == "__main__":
    run_sample_scaling_experiment()
    run_dimension_scaling_experiment()
