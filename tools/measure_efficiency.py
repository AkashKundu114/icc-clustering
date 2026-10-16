"""
Comprehensive Resource Efficiency Benchmark Suite for ICC-v2.

Measures:
1. Large sample cohort (N=5000, D=50, K=3)
2. High dimensional regime (N=500, D=5000, K=3)
3. Standard benchmark regime (N=1000, D=2000, K=3)
4. ASPP profiling (N=500, D=200, K=3)
5. Streaming query throughput (10,000 queries)
"""

# ruff: noqa: E402
import json
import os
import sys
import time
import tracemalloc
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import numpy as np
import psutil

from src.icc.aspp import ASPPConfig
from src.icc.consensus_v2 import InvariantCoreConsensusV2


def measure_scenario_1_large_n():
    N, D, K = 5000, 50, 3
    rng = np.random.default_rng(42)
    X = rng.normal(size=(N, D))

    tracemalloc.start()
    t0 = time.perf_counter()
    m = InvariantCoreConsensusV2(n_clusters=K, n_base_models=20, n_anchors=50, random_state=42)
    labels = m.fit_predict(X)
    t1 = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "scenario": "Large N (N=5000, D=50, K=3)",
        "elapsed_sec": round(t1 - t0, 4),
        "peak_ram_mb": round(peak / (1024 * 1024), 2),
        "n_unique_labels": int(len(np.unique(labels))),
    }


def measure_scenario_2_high_d():
    N, D, K = 500, 5000, 3
    rng = np.random.default_rng(42)
    X = rng.normal(size=(N, D))

    tracemalloc.start()
    t0 = time.perf_counter()
    m = InvariantCoreConsensusV2(n_clusters=K, n_base_models=20, n_anchors=50, random_state=42)
    labels = m.fit_predict(X)
    t1 = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "scenario": "High D (N=500, D=5000, K=3)",
        "elapsed_sec": round(t1 - t0, 4),
        "peak_ram_mb": round(peak / (1024 * 1024), 2),
        "n_unique_labels": int(len(np.unique(labels))),
    }


def measure_scenario_3_standard():
    N, D, K = 1000, 2000, 3
    rng = np.random.default_rng(42)
    X = rng.normal(size=(N, D))

    tracemalloc.start()
    t0 = time.perf_counter()
    m = InvariantCoreConsensusV2(n_clusters=K, n_base_models=25, n_anchors=40, random_state=42)
    labels = m.fit_predict(X)
    t1 = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "scenario": "Standard (N=1000, D=2000, K=3)",
        "elapsed_sec": round(t1 - t0, 4),
        "peak_ram_mb": round(peak / (1024 * 1024), 2),
        "n_unique_labels": int(len(np.unique(labels))),
    }


def measure_scenario_4_aspp():
    N, D, K = 500, 200, 3
    rng = np.random.default_rng(42)
    X = rng.normal(size=(N, D))

    m = InvariantCoreConsensusV2(n_clusters=K, n_base_models=15, n_anchors=30, random_state=42)
    m.fit_predict(X)

    cfg = ASPPConfig(repetitions=1, n_base_models=3, random_state=42)
    tracemalloc.start()
    t0 = time.perf_counter()
    df_fp = m.profile_perturbations(X, config=cfg)
    t1 = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "scenario": "ASPP Diagnostic (N=500, D=200, K=3)",
        "elapsed_sec": round(t1 - t0, 4),
        "peak_ram_mb": round(peak / (1024 * 1024), 2),
        "psi_mean": round(float(df_fp["PSI"].mean()), 4),
    }


def measure_scenario_5_streaming_query():
    N_train, D, K = 1000, 50, 3
    rng = np.random.default_rng(42)
    X_train = rng.normal(size=(N_train, D))
    m = InvariantCoreConsensusV2(n_clusters=K, n_base_models=20, n_anchors=40, random_state=42)
    m.fit_predict(X_train)

    n_queries = 10000
    X_queries = rng.normal(size=(n_queries, D))

    # Warmup
    _ = m.predict(X_queries[:10])

    tracemalloc.start()
    t0 = time.perf_counter()
    _ = m.predict(X_queries)
    t1 = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    throughput = n_queries / (t1 - t0) if (t1 - t0) > 0 else 0
    return {
        "scenario": "Streaming Query (10,000 queries)",
        "elapsed_sec": round(t1 - t0, 4),
        "peak_ram_mb": round(peak / (1024 * 1024), 2),
        "throughput_sps": round(throughput, 1),
    }


def run_all(save_path: str = "results/baseline_resource_profile.json"):
    proc = psutil.Process(os.getpid())
    init_rss = proc.memory_info().rss / (1024 * 1024)

    s1 = measure_scenario_1_large_n()
    s2 = measure_scenario_2_high_d()
    s3 = measure_scenario_3_standard()
    s4 = measure_scenario_4_aspp()
    s5 = measure_scenario_5_streaming_query()

    end_rss = proc.memory_info().rss / (1024 * 1024)
    res = {
        "initial_rss_mb": round(init_rss, 2),
        "final_rss_mb": round(end_rss, 2),
        "scenarios": [s1, s2, s3, s4, s5],
    }

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)

    print(json.dumps(res, indent=2))
    return res


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "results/baseline_resource_profile.json"
    run_all(out)
