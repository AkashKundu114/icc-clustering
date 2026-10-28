"""
scripts/measure_query_latency.py

Measures closed-form inductive query prediction latency (ms/query) across the 6
inductive benchmark cohorts from Table 3 (CNS, Colon, Leukemia, Ovarian, SRBCT, Isolet).
Outputs results to results/query_latency.json.
"""

import json
import time
from pathlib import Path
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit

# Add project root
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from icc.consensus_v2 import InvariantCoreConsensusV2

DATASETS = ["cns", "colon", "leukemia", "ovarian", "srbct", "isolet"]


def measure_latencies():
    results = {}
    print("=" * 70)
    print("MEASURING INDUCTIVE QUERY LATENCY (ms / query)")
    print("=" * 70)

    for dname in DATASETS:
        p_npz = ROOT / "experiments" / "exp3_real_world_benchmarks" / "data" / "cache" / f"{dname}.npz"
        if not p_npz.exists():
            continue

        data = np.load(p_npz)
        X, y = data["X"].astype(np.float64), data["y"]
        N, D = X.shape
        K = len(np.unique(y))

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

        icc = InvariantCoreConsensusV2(n_clusters=K, random_state=42)
        icc.fit_predict(X_tr)

        # Warm up
        icc.predict(X_te)

        # Timing runs
        times = []
        n_repeats = 50
        for _ in range(n_repeats):
            t0 = time.perf_counter()
            icc.predict(X_te)
            t_elap = time.perf_counter() - t0
            times.append(t_elap)

        total_time_s = np.mean(times)
        per_query_ms = (total_time_s / n_test) * 1000.0

        results[dname] = {
            "N": N, "D": D, "K": K, "n_test": n_test,
            "mean_batch_ms": total_time_s * 1000.0,
            "per_query_ms": per_query_ms
        }
        print(f"{dname.upper():<10}: N={N:5d}, D={D:5d}, K={K:2d} | Test={n_test:4d} | Per-query: {per_query_ms:.4f} ms")

    out_json = ROOT / "results" / "query_latency.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved query latency results to {out_json}")


if __name__ == "__main__":
    measure_latencies()
