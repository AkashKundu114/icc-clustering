"""
Experiment 3.5: Missing Data Robustness & Imputation Resilience Suite.

Investigates cluster recovery degradation under Missing Completely At Random (MCAR)
regimes across diverse high-dimensional genomics cohorts (Colon, Leukemia, SRBCT):
- Datasets: [Colon, Leukemia, SRBCT]
- Missingness rates rho in {0.0, 0.10, 0.20, 0.30, 0.50, 0.70}
- Imputation: Mean, Median, KNN (n_neighbors=5), Zero
- Methods: KMeans, Standard_Consensus, Li_et_al_2019, ICC_v1, ICC_v2
- 10 trials per condition
- Records: dataset, rho, imputation, method, trial, seed, ari, nmi, ami, v_measure, runtime
"""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer, SimpleImputer
from tqdm import tqdm

# Add project root to sys.path
root_dir = Path(__file__).resolve().parents[3]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from icc.baselines.classical import run_kmeans
from icc.baselines.consensus import (
    run_icc_v1,
    run_icc_v2,
    run_li_et_al_2019,
    run_standard_consensus,
)
from icc.datasets.registry import load_dataset
from icc.metrics import evaluate_all

EXP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = EXP_DIR / "data"
FIGURES_DIR = EXP_DIR / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_OUTPUT_CSV = DATA_DIR / "exp3_5_missing_data_results.csv"

METHODS = {
    "K-Means": run_kmeans,
    "Standard_Consensus": run_standard_consensus,
    "Li_et_al_2019": run_li_et_al_2019,
    "ICC_v1": run_icc_v1,
    "ICC_v2": run_icc_v2,
}

DATASETS = ["colon", "leukemia", "srbct"]
RHO_LEVELS = [0.0, 0.10, 0.20, 0.30, 0.50, 0.70]
IMPUTATION_STRATEGIES = ["Mean", "Median", "KNN", "Zero"]

CSV_COLUMNS = [
    "dataset",
    "rho",
    "imputation",
    "method",
    "trial",
    "seed",
    "ari",
    "nmi",
    "ami",
    "v_measure",
    "runtime",
]


def inject_mcar_noise(X: np.ndarray, rho: float, seed: int = 42) -> np.ndarray:
    """
    Inject Missing Completely At Random (MCAR) NaN entries into feature matrix X.
    Guarantees no entire sample row or column is 100% NaN to allow valid imputation.
    """
    if rho <= 0.0:
        return X.copy()

    rng = np.random.default_rng(seed)
    X_missing = X.copy()
    mask = rng.random(size=X.shape) < rho

    # Ensure no row is entirely NaN
    row_all_nan = np.all(mask, axis=1)
    if np.any(row_all_nan):
        for r_idx in np.where(row_all_nan)[0]:
            # Keep at least 2 random features non-NaN
            keep_cols = rng.choice(X.shape[1], size=min(2, X.shape[1]), replace=False)
            mask[r_idx, keep_cols] = False

    # Ensure no column is entirely NaN
    col_all_nan = np.all(mask, axis=0)
    if np.any(col_all_nan):
        for c_idx in np.where(col_all_nan)[0]:
            keep_row = rng.choice(X.shape[0])
            mask[keep_row, c_idx] = False

    X_missing[mask] = np.nan
    return X_missing


def impute_data(X_nan: np.ndarray, strategy: str = "Mean") -> np.ndarray:
    """
    Impute missing entries in X_nan via specified statistical strategy:
    - Mean: mean of observed values in each column
    - Median: median of observed values in each column
    - Zero: constant fill with 0.0
    - KNN: Euclidean k-nearest neighbor weighted average (k=5)
    """
    if not np.isnan(X_nan).any():
        return X_nan.copy()

    strat_lower = strategy.strip().lower()

    if strat_lower == "mean":
        imp = SimpleImputer(strategy="mean")
        return imp.fit_transform(X_nan)
    elif strat_lower == "median":
        imp = SimpleImputer(strategy="median")
        return imp.fit_transform(X_nan)
    elif strat_lower == "zero":
        imp = SimpleImputer(strategy="constant", fill_value=0.0)
        return imp.fit_transform(X_nan)
    elif strat_lower == "knn":
        imp = KNNImputer(n_neighbors=5)
        return imp.fit_transform(X_nan)
    else:
        raise ValueError(f"Unknown imputation strategy: {strategy}")


def run_missing_data_sweep(
    datasets: Optional[List[str]] = None,
    rho_levels: Optional[List[float]] = None,
    strategies: Optional[List[str]] = None,
    n_trials: int = 10,
    resume: bool = True,
    output_csv: Optional[Path] = None,
) -> pd.DataFrame:
    """
    Executes the comprehensive missing data benchmark matrix across datasets,
    missingness fractions rho, imputation schemes, models, and stochastic trials.
    """
    if datasets is None:
        datasets = DATASETS
    if rho_levels is None:
        rho_levels = RHO_LEVELS
    if strategies is None:
        strategies = IMPUTATION_STRATEGIES
    if output_csv is None:
        output_csv = DEFAULT_OUTPUT_CSV

    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("RUNNING SUB-EXPERIMENT 3.5: MISSING DATA ROBUSTNESS & IMPUTATION RESILIENCE")
    print(f"Datasets ({len(datasets)}): {datasets}")
    print(f"Missingness Rates rho ({len(rho_levels)}): {rho_levels}")
    print(f"Imputation Strategies ({len(strategies)}): {strategies}")
    print(f"Methods ({len(METHODS)}): {list(METHODS.keys())}")
    print(f"Trials per condition: {n_trials}")
    print(f"Target Output: {output_csv}")
    print("=" * 80)

    # 1. Initialize or load pre-existing runs for resume capability
    completed_set: Set[Tuple[str, float, str, str, int]] = set()
    if resume and output_csv.exists():
        try:
            existing_df = pd.read_csv(output_csv)
            if not existing_df.empty:
                col_strat = "imputation" if "imputation" in existing_df.columns else "strategy"
                for _, r in existing_df.iterrows():
                    completed_set.add((
                        str(r["dataset"]).lower(),
                        round(float(r["rho"]), 3),
                        str(r[col_strat]).capitalize(),
                        str(r["method"]),
                        int(r["trial"]),
                    ))
                print(f"[+] Loaded {len(completed_set)} pre-existing evaluations from {output_csv}")
        except Exception as e:
            print(f"[!] Warning reading existing CSV: {e}")

    if not output_csv.exists() or not resume:
        empty_df = pd.DataFrame(columns=CSV_COLUMNS)
        empty_df.to_csv(output_csv, index=False)

    total_conditions = len(datasets) * len(rho_levels) * len(strategies) * len(METHODS) * n_trials
    pbar = tqdm(total=total_conditions, desc="Missing Data Grid", unit="run")
    pbar.update(len(completed_set))

    t_start = time.perf_counter()

    for dname in datasets:
        X_orig, y_true, meta = load_dataset(dname)
        K = meta.get("K", len(np.unique(y_true)))
        N, D = X_orig.shape

        for rho in rho_levels:
            rho_key = round(float(rho), 3)

            for strat in strategies:
                strat_key = strat.capitalize()

                for trial in range(n_trials):
                    trial_seed = 42 + trial * 37 + int(rho * 1000)

                    # Check if all models already completed for this tuple
                    all_done = True
                    for mname in METHODS:
                        if (dname.lower(), rho_key, strat_key, mname, trial) not in completed_set:
                            all_done = False
                            break
                    if all_done:
                        continue

                    # Corrupt and impute feature matrix
                    X_corrupted = inject_mcar_noise(X_orig, rho=rho, seed=trial_seed)
                    X_imputed = impute_data(X_corrupted, strategy=strat)

                    # Evaluate each clustering method
                    for mname, mfn in METHODS.items():
                        key = (dname.lower(), rho_key, strat_key, mname, trial)
                        if key in completed_set:
                            continue

                        try:
                            labels, rtime, _ = mfn(X_imputed, k=K, seed=trial_seed)
                            scores = evaluate_all(y_true, labels)
                        except Exception as e:
                            print(f"\n[!] Error running {mname} on {dname} (rho={rho}, strat={strat}): {e}")
                            labels = np.zeros(N, dtype=int)
                            rtime = 0.0
                            scores = {"ari": 0.0, "nmi": 0.0, "ami": 0.0, "v_measure": 0.0}

                        row_dict = {
                            "dataset": dname.lower(),
                            "rho": rho,
                            "imputation": strat_key,
                            "method": mname,
                            "trial": trial,
                            "seed": trial_seed,
                            "ari": scores["ari"],
                            "nmi": scores["nmi"],
                            "ami": scores["ami"],
                            "v_measure": scores["v_measure"],
                            "runtime": rtime,
                        }

                        # Append to disk immediately
                        pd.DataFrame([row_dict]).to_csv(output_csv, mode="a", header=False, index=False)
                        completed_set.add(key)

                        pbar.set_postfix({"ds": dname, "rho": f"{rho:.2f}", "strat": strat_key, "m": mname, "ari": f"{scores['ari']:.3f}"})
                        pbar.update(1)

    pbar.close()

    final_df = pd.read_csv(output_csv)
    print(f"\n[+] Exp 3.5 completed in {time.perf_counter() - t_start:.2f}s")
    print(f"[+] Total records in {output_csv}: {len(final_df)}")
    return final_df


def main():
    parser = argparse.ArgumentParser(description="Exp 3.5 Missing Data Robustness Benchmark")
    parser.add_argument("--trials", type=int, default=10, help="Number of trials per condition (default: 10)")
    parser.add_argument("--no-resume", action="store_true", help="Overwrite and restart from scratch")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT_CSV), help="Output CSV path")

    args = parser.parse_args()

    run_missing_data_sweep(
        n_trials=args.trials,
        resume=not args.no_resume,
        output_csv=Path(args.output),
    )


if __name__ == "__main__":
    main()
