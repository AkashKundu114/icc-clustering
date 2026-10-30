"""
Inductive query prediction latency benchmark for ICC-v2.

Measures closed-form out-of-sample query prediction latency (ms per query)
across inductive benchmark cohorts (CNS, Colon, Leukemia, Ovarian, SRBCT, ISOLET).

Mathematical and Algorithmic Rationale:
---------------------------------------
In streaming, real-time, or clinical settings (e.g., classifying a newly sequenced
patient's biopsy), standard consensus clustering algorithms lack inductive projection
mechanisms. Assigning a novel sample requires either:
1. Full ensemble retraining on (N + 1) samples with O(M * N^2 * D + N^3) cost, or
2. Out-of-sample heuristic approximations that require computing co-associations against
   all N training points in O(N * D) time.

In contrast, ICC-v2 derives K geometry-calibrated anchor centroids mu_k in the invariant
feature subspace during fit. Projecting a new query point x_new executes in closed-form:
    c*(x_new) = argmin_{k} ||x_new[S] - mu_k[S]||_2^2
requiring only O(K * |S|) arithmetic operations where |S| <= D and K << N.
This benchmark quantifies this throughput, demonstrating sub-millisecond per-query
latencies suitable for real-time edge or point-of-care deployment.

Parameters:
-----------
--datasets : list of str, optional
    Cohorts to evaluate (default: ['cns', 'colon', 'leukemia', 'ovarian', 'srbct', 'isolet']).
--repeats : int, default=50
    Number of repetitions for timing estimation.
--output-json : str, optional
    Destination JSON path for benchmark metrics (default: 'results/query_latency.json').

Outputs:
--------
- results/query_latency.json

Usage:
------
    python scripts/benchmark_latency.py
    python scripts/benchmark_latency.py --repeats 100
"""

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit

# Ensure project root is in sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from icc.consensus_v2 import InvariantCoreConsensusV2

DEFAULT_DATASETS = ["cns", "colon", "leukemia", "ovarian", "srbct", "isolet"]
DEFAULT_OUTPUT = ROOT / "results" / "query_latency.json"


def benchmark_inductive_latency(datasets=None, repeats=50, output_json=None):
    """
    Measure out-of-sample inductive query latency across benchmark datasets.

    Parameters
    ----------
    datasets : list of str, optional
        Dataset identifiers to benchmark.
    repeats : int, default=50
        Timing repetitions to average across.
    output_json : Path or str, optional
        File path to save JSON latency results.

    Returns
    -------
    dict
        Benchmark latency metrics by dataset.
    """
    if datasets is None:
        datasets = DEFAULT_DATASETS
    if output_json is None:
        output_json = DEFAULT_OUTPUT
    output_json = Path(output_json)

    results = {}
    print("=" * 75)
    print("ICC-v2 INDUCTIVE QUERY LATENCY BENCHMARK (ms / query)")
    print(f"Cohorts: {datasets} | Timing repetitions: {repeats}")
    print("=" * 75)

    for dname in datasets:
        p_npz = ROOT / "experiments" / "exp3_real_world_benchmarks" / "data" / "cache" / f"{dname}.npz"
        if not p_npz.exists():
            print(f"[SKIP] Cache file not found for '{dname}': {p_npz}")
            continue

        data = np.load(p_npz)
        X, y = data["X"].astype(np.float64), data["y"]
        N, D = X.shape
        K = len(np.unique(y))

        # 80/20 train/test stratified split
        try:
            sss = StratifiedShuffleSplit(n_splits=1, test_size=0.20, random_state=42)
            train_idx, test_idx = next(sss.split(X, y))
        except ValueError:
            rng = np.random.default_rng(42)
            perm = rng.permutation(N)
            split_pt = int(0.80 * N)
            train_idx, test_idx = perm[:split_pt], perm[split_pt:]

        X_tr = X[train_idx]
        X_te = X[test_idx]
        n_test = len(X_te)

        # Fit ICC-v2 on training split
        icc = InvariantCoreConsensusV2(n_clusters=K, random_state=42)
        icc.fit_predict(X_tr)

        # Warm-up run to ensure JIT compilation / cache warming
        icc.predict(X_te)

        # High-precision wall-clock timing
        times = []
        for _ in range(repeats):
            t0 = time.perf_counter()
            icc.predict(X_te)
            t_elap = time.perf_counter() - t0
            times.append(t_elap)

        total_time_s = float(np.mean(times))
        per_query_ms = (total_time_s / n_test) * 1000.0

        results[dname] = {
            "N": N,
            "D": D,
            "K": K,
            "n_test": n_test,
            "mean_batch_ms": total_time_s * 1000.0,
            "per_query_ms": per_query_ms,
        }
        print(f"{dname.upper():<10}: N={N:5d}, D={D:5d}, K={K:2d} | Test points: {n_test:3d} | Per-query: {per_query_ms:.4f} ms")

    output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[+] Saved inductive query latency results to {output_json}")
    return results


def main():
    parser = argparse.ArgumentParser(description="Measure ICC-v2 out-of-sample inductive query latency.")
    parser.add_argument(
        "--datasets",
        type=str,
        nargs="+",
        default=DEFAULT_DATASETS,
        help="List of datasets to benchmark.",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=50,
        help="Number of timing repetitions per cohort (default: 50).",
    )
    parser.add_argument(
        "--output-json",
        type=str,
        default=str(DEFAULT_OUTPUT),
        help="Path for output JSON file.",
    )
    args = parser.parse_args()

    benchmark_inductive_latency(datasets=args.datasets, repeats=args.repeats, output_json=args.output_json)


if __name__ == "__main__":
    main()
