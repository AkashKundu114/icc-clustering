"""
Resource and Performance Benchmarking for ICC-v2.

Measures:
1. Training wall-clock time and peak memory (RAM) across varying sample sizes N.
2. Training wall-clock time and peak memory across varying feature dimensions D.
3. Out-of-sample query latency (predict / transform) across batch sizes N_test.
4. Process peak memory and CPU utilization.
"""

# ruff: noqa: E402
import json
import os
import sys
import time
import tracemalloc

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import psutil

from src.icc.consensus_v2 import InvariantCoreConsensusV2


def benchmark_n_scaling():
    print("--- Benchmarking N Scaling (D=50, K=3, M=20, m=50) ---")
    results = []
    D = 50
    K = 3
    M = 20
    m = 50
    Ns = [100, 500, 1000, 2500, 5000]

    for N in Ns:
        rng = np.random.default_rng(42)
        X = rng.normal(size=(N, D))
        
        tracemalloc.start()
        t0 = time.perf_counter()
        
        model = InvariantCoreConsensusV2(
            n_clusters=K,
            n_base_models=M,
            n_anchors=m,
            random_state=42,
        )
        labels = model.fit_predict(X)
        
        t1 = time.perf_counter()
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        elapsed = t1 - t0
        peak_mb = peak_mem / (1024 * 1024)
        print(f"N={N:5d} | Elapsed: {elapsed:6.3f}s | Peak Traced RAM: {peak_mb:6.2f} MB | Unique labels: {len(np.unique(labels))}")
        results.append({
            "N": N,
            "D": D,
            "elapsed_sec": round(elapsed, 4),
            "peak_ram_mb": round(peak_mb, 2),
        })
    return results


def benchmark_d_scaling():
    print("\n--- Benchmarking D Scaling (N=500, K=3, M=20, m=50) ---")
    results = []
    N = 500
    K = 3
    M = 20
    m = 50
    Ds = [20, 100, 500, 2000, 5000]

    for D in Ds:
        rng = np.random.default_rng(42)
        X = rng.normal(size=(N, D))
        
        tracemalloc.start()
        t0 = time.perf_counter()
        
        model = InvariantCoreConsensusV2(
            n_clusters=K,
            n_base_models=M,
            n_anchors=m,
            random_state=42,
        )
        _ = model.fit_predict(X)
        
        t1 = time.perf_counter()
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        elapsed = t1 - t0
        peak_mb = peak_mem / (1024 * 1024)
        print(f"D={D:5d} | Elapsed: {elapsed:6.3f}s | Peak Traced RAM: {peak_mb:6.2f} MB | Features Selected: {len(model.selected_features_)}")
        results.append({
            "N": N,
            "D": D,
            "elapsed_sec": round(elapsed, 4),
            "peak_ram_mb": round(peak_mb, 2),
            "features_selected": len(model.selected_features_),
        })
    return results


def benchmark_inductive_throughput():
    print("\n--- Benchmarking Inductive Query Latency (N_train=1000, D=50, K=3) ---")
    results = []
    N_train = 1000
    D = 50
    K = 3
    rng = np.random.default_rng(42)
    X_train = rng.normal(size=(N_train, D))
    
    model = InvariantCoreConsensusV2(n_clusters=K, n_base_models=20, n_anchors=50, random_state=42)
    model.fit_predict(X_train)

    query_sizes = [10, 100, 1000, 5000, 20000]
    for q_size in query_sizes:
        X_query = rng.normal(size=(q_size, D))
        
        # Warmup
        _ = model.predict(X_query[:5])
        
        t0 = time.perf_counter()
        _ = model.predict(X_query)
        t1 = time.perf_counter()
        
        elapsed_ms = (t1 - t0) * 1000
        throughput_sps = q_size / (t1 - t0) if (t1 - t0) > 0 else 0
        print(f"Batch={q_size:6d} | Latency: {elapsed_ms:8.2f} ms | Throughput: {throughput_sps:10.1f} samples/sec")
        results.append({
            "batch_size": q_size,
            "latency_ms": round(elapsed_ms, 2),
            "throughput_sps": round(throughput_sps, 1),
        })
    return results


def main():
    process = psutil.Process(os.getpid())
    baseline_rss_mb = process.memory_info().rss / (1024 * 1024)
    print(f"Process PID: {os.getpid()} | Initial Process RSS: {baseline_rss_mb:.2f} MB")

    n_results = benchmark_n_scaling()
    d_results = benchmark_d_scaling()
    query_results = benchmark_inductive_throughput()

    final_rss_mb = process.memory_info().rss / (1024 * 1024)
    print(f"\nFinal Process RSS: {final_rss_mb:.2f} MB (Delta: {final_rss_mb - baseline_rss_mb:+.2f} MB)")

    out_file = "results/resource_benchmarks.json"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "n_scaling": n_results,
            "d_scaling": d_results,
            "query_throughput": query_results,
            "baseline_rss_mb": round(baseline_rss_mb, 2),
            "final_rss_mb": round(final_rss_mb, 2),
        }, f, indent=2)
    print(f"Benchmarks recorded to {out_file}")


if __name__ == "__main__":
    main()
