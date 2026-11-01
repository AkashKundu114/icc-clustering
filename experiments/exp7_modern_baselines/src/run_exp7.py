"""
Execution runner for EXP7: Modern Baselines Benchmark Matrix.

Evaluates 10 clustering methods:
- Classical Single: K-Means, Ward, Spectral, FCM
- Consensus/Ensemble: Standard_Consensus, GAC (ICC-v2)
- Modern Specialized: Sparse_KMeans, HDBSCAN*, Leiden_SNN, GMM_BIC

Across 6 high-dimensional biological cohorts:
- Colon (N=62, D=2,000, K=2)
- SRBCT (N=83, D=2,308, K=4)
- CNS (N=60, D=7,129, K=2)
- Leukemia (N=72, D=7,129, K=2)
- Prostate (N=102, D=12,600, K=2)
- Ovarian (N=253, D=15,154, K=2)

Across 5 reproducible seeds: [42, 43, 44, 45, 46].
Total model evaluations: 6 cohorts * 10 models * 5 seeds = 300 runs.
"""

import os
import sys
import time
import warnings
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd

# Suppress expected library warnings during high-dimensional sweeps
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from icc.baselines.classical import run_kmeans, run_ward, run_spectral, run_fcm
from icc.baselines.consensus import run_standard_consensus, run_icc_v2
from icc.baselines.sparse_kmeans import run_sparse_kmeans
from icc.baselines.density import run_hdbscan
from icc.baselines.leiden_snn import run_leiden_snn
from icc.baselines.probabilistic import run_gmm
from icc.datasets.registry import load_dataset
from icc.metrics import evaluate_all

DATASETS = ["colon", "srbct", "cns", "leukemia", "prostate", "ovarian"]
SEEDS = [42, 43, 44, 45, 46]


def run_benchmark(output_csv: Path) -> pd.DataFrame:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    records: List[Dict[str, Any]] = []

    print(f"Starting EXP7 Modern Baselines Benchmark...")
    print(f"Cohorts: {DATASETS}")
    print(f"Seeds: {SEEDS}")
    print(f"Output: {output_csv}\n")

    for ds_name in DATASETS:
        print(f"=== Loading dataset: {ds_name} ===")
        X, y_true, meta = load_dataset(ds_name)
        N, D = X.shape
        k_true = len(np.unique(y_true))
        print(f"  Shape: N={N}, D={D}, K={k_true}")

        for seed in SEEDS:
            # Model dispatch dict
            models = {
                "K-Means": lambda: run_kmeans(X, k=k_true, seed=seed),
                "Ward": lambda: run_ward(X, k=k_true, seed=seed),
                "Spectral": lambda: run_spectral(X, k=k_true, seed=seed),
                "FCM": lambda: run_fcm(X, k=k_true, seed=seed),
                "Standard_Consensus": lambda: run_standard_consensus(X, k=k_true, seed=seed),
                "GAC": lambda: run_icc_v2(X, k=k_true, seed=seed),
                "Sparse_KMeans": lambda: run_sparse_kmeans(X, k=k_true, seed=seed),
                "HDBSCAN*": lambda: run_hdbscan(X, seed=seed),
                "Leiden_SNN": lambda: run_leiden_snn(X, target_k=k_true, seed=seed),
                "GMM_BIC": lambda: run_gmm(X, k=k_true, seed=seed),
            }

            for model_name, runner_fn in models.items():
                t0 = time.perf_counter()
                try:
                    labels, runtime, model_meta = runner_fn()
                    eval_metrics = evaluate_all(y_true, labels)
                    n_clusters_found = len(np.unique(labels))
                    status = "OK"
                except Exception as e:
                    print(f"  [ERROR] {model_name} on {ds_name} (seed={seed}): {e}")
                    eval_metrics = {"ari": np.nan, "nmi": np.nan, "ami": np.nan, "v_measure": np.nan, "fm_index": np.nan}
                    runtime = time.perf_counter() - t0
                    n_clusters_found = 0
                    status = f"ERROR: {e}"

                record = {
                    "cohort": ds_name,
                    "N": N,
                    "D": D,
                    "true_k": k_true,
                    "model": model_name,
                    "seed": seed,
                    "ari": eval_metrics.get("ari", np.nan),
                    "nmi": eval_metrics.get("nmi", np.nan),
                    "ami": eval_metrics.get("ami", np.nan),
                    "v_measure": eval_metrics.get("v_measure", np.nan),
                    "fm_index": eval_metrics.get("fm_index", np.nan),
                    "runtime_sec": runtime,
                    "n_clusters_found": n_clusters_found,
                    "status": status,
                }
                records.append(record)

            print(f"  Completed seed {seed} across 10 models.")

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    print(f"\n[DONE] Saved {len(df)} runs to {output_csv}")

    # Generate and print aggregate summary
    summary = df.groupby(["cohort", "model"])[["ari", "nmi", "runtime_sec"]].agg(["mean", "std"])
    summary_path = output_csv.parent / "modern_baselines_summary.csv"
    summary.to_csv(summary_path)
    print(f"[SUMMARY] Saved aggregate metrics to {summary_path}")

    return df


if __name__ == "__main__":
    out_file = _ROOT / "experiments" / "exp7_modern_baselines" / "data" / "modern_baselines_benchmark.csv"
    run_benchmark(out_file)
