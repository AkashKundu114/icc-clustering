"""
Execution runner for EXP6: Expanded Biological Cohort Benchmark.

Evaluates clustering methods on independent public high-dimensional oncology cohorts:
- DLBCL (N=77, D=5,469, K=2) - Shipp et al. 2002
- Breast (N=97, D=24,481, K=2) - van 't Veer et al. 2002
- Su2001 (N=174, D=12,533, K=11) - Su et al. 2001
- Novartis (N=60, D=5,726, K=9) - Su et al. 2002
- GCM (N=190, D=16,063, K=14) - Ramaswamy et al. 2001
- Endometrium (N=321, D=10,936, K=2) - Risinger et al. 2003

Evaluates key pipelines:
- K-Means
- Ward Hierarchical
- Spectral Clustering
- FCM
- Standard Consensus
- GAC (ICC-v2)
- Sparse K-Means

Across 5 reproducible seeds: [42, 43, 44, 45, 46].
"""

import gzip
import os
import sys
import time
import warnings
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from icc.baselines.classical import run_kmeans, run_ward, run_spectral, run_fcm
from icc.baselines.consensus import run_standard_consensus, run_icc_v2
from icc.baselines.sparse_kmeans import run_sparse_kmeans
from icc.metrics import evaluate_all

DL_DIR = Path.home() / "scikit_learn_data" / "openml" / "openml.org" / "data" / "v1" / "download"

COHORTS_MAP = {
    "dlbcl": ("DLBCL.arff.gz", "Shipp et al. 2002 (DLBCL vs FL)"),
    "breast": ("Breast.arff.gz", "van 't Veer et al. 2002 (Metastasis 5yr)"),
    "su2001": ("11_Tumors.arff.gz", "Su et al. 2001 (11 Solid Tumors)"),
    "novartis": ("9_Tumors.arff.gz", "Su / Novartis 2002 (9 Carcinomas)"),
    "gcm": ("GCM.arff.gz", "Ramaswamy et al. 2001 (Global Cancer Map)"),
    "endometrium": ("AP_Endometrium_Kidney.arff.gz", "Risinger 2003 (Endometrium vs Kidney)"),
}

SEEDS = [42, 43, 44, 45, 46]


def parse_arff_gz(file_path: Path) -> Tuple[np.ndarray, np.ndarray]:
    """Parse gzip-compressed ARFF file extracting feature array X and labels y."""
    with gzip.open(file_path, "rt", encoding="utf-8", errors="ignore") as gz:
        in_data = False
        X_rows = []
        y_rows = []
        for line in gz:
            line_str = line.strip()
            if not line_str or line_str.startswith("%"):
                continue
            if line_str.upper().startswith("@DATA"):
                in_data = True
                continue
            if in_data:
                parts = line_str.split(",")
                features = [float(val) if val != "?" else np.nan for val in parts[:-1]]
                label = parts[-1].strip().strip("'\"")
                X_rows.append(features)
                y_rows.append(label)

    X = np.array(X_rows, dtype=np.float64)
    y = np.array(y_rows)

    # 1. Impute missing values with column mean
    col_means = np.nanmean(X, axis=0)
    inds = np.where(np.isnan(X))
    X[inds] = np.take(col_means, inds[1])

    # 2. Standardize features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # 3. Encode labels to contiguous integers
    encoder = LabelEncoder()
    y = encoder.fit_transform(y)

    return X, y


def run_expanded_benchmark(output_csv: Path) -> pd.DataFrame:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    records: List[Dict[str, Any]] = []

    print("==========================================================")
    print("Starting EXP6 Expanded Biological Cohort Benchmark...")
    print(f"Cohorts: {list(COHORTS_MAP.keys())}")
    print(f"Seeds: {SEEDS}")
    print(f"Output: {output_csv}\n")

    for cohort_name, (filename, desc) in COHORTS_MAP.items():
        matches = list(DL_DIR.glob(f"**/{filename}"))
        if not matches:
            print(f"[SKIP] Could not locate file {filename} in {DL_DIR}")
            continue

        file_path = matches[0]
        X, y_true = parse_arff_gz(file_path)
        N, D = X.shape
        k_true = len(np.unique(y_true))
        print(f"\n=== Cohort: {cohort_name} ({desc}) ===")
        print(f"  Shape: N={N}, D={D}, K={k_true}")

        for seed in SEEDS:
            models = {
                "K-Means": lambda: run_kmeans(X, k=k_true, seed=seed),
                "Ward": lambda: run_ward(X, k=k_true, seed=seed),
                "Spectral": lambda: run_spectral(X, k=k_true, seed=seed),
                "FCM": lambda: run_fcm(X, k=k_true, seed=seed),
                "Standard_Consensus": lambda: run_standard_consensus(X, k=k_true, seed=seed),
                "GAC": lambda: run_icc_v2(X, k=k_true, seed=seed),
                "Sparse_KMeans": lambda: run_sparse_kmeans(X, k=k_true, seed=seed),
            }

            for model_name, runner_fn in models.items():
                t0 = time.perf_counter()
                try:
                    labels, runtime, model_meta = runner_fn()
                    eval_metrics = evaluate_all(y_true, labels)
                    status = "OK"
                except Exception as e:
                    print(f"  [ERR] {model_name} on {cohort_name} (seed={seed}): {e}")
                    eval_metrics = {"ari": np.nan, "nmi": np.nan, "ami": np.nan, "v_measure": np.nan, "fm_index": np.nan}
                    runtime = time.perf_counter() - t0
                    status = f"ERROR: {e}"

                records.append({
                    "cohort": cohort_name,
                    "description": desc,
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
                    "status": status,
                })

            print(f"  Completed seed {seed} across 7 models.", flush=True)

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    print(f"\n[DONE] Saved {len(df)} evaluations to {output_csv}")

    summary = df.groupby(["cohort", "model"])[["ari", "nmi", "runtime_sec"]].agg(["mean", "std"])
    summary_csv = output_csv.parent / "expanded_cohort_summary.csv"
    summary.to_csv(summary_csv)
    print(f"[SUMMARY] Saved summary metrics to {summary_csv}")

    return df


if __name__ == "__main__":
    out_path = _ROOT / "experiments" / "exp6_cohort_expansion" / "data" / "expanded_cohort_benchmark.csv"
    run_expanded_benchmark(out_path)
