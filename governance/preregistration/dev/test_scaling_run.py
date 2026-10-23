import sys
import time
import os
from pathlib import Path
import psutil
import numpy as np

# Add project root
root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root))

from icc.baselines.consensus import run_standard_consensus, run_icc_v2

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

if __name__ == "__main__":
    X, y = generate_benchmark_synthetic(2000, 200, k=3, seed=42)
    t0 = time.perf_counter()
    p, t, m = run_icc_v2(X, 3, seed=42)
    print("ICC_v2 runtime:", time.perf_counter() - t0)
    t0 = time.perf_counter()
    p, t, m = run_standard_consensus(X, 3, seed=42)
    print("StdCons runtime:", time.perf_counter() - t0)
