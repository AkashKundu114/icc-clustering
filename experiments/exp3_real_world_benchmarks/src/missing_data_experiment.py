"""
Experiment 3.5: Missing Data Robustness & Imputation Resilience Suite.

Investigates cluster recovery degradation under Missing Completely At Random (MCAR)
regimes across diverse high-dimensional genomics cohorts (Colon, Leukemia, SRBCT):
- Missingness rates: rho in [0.0, 0.10, 0.20, 0.30, 0.50, 0.70]
- Imputation strategies: Mean, Median, Zero, and KNN (k=5)
- Evaluated models: K-Means, Standard Consensus, Li et al. (2019), ICC-v1, ICC-v2
"""

import os
import time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer, KNNImputer

from src.icc.datasets import load_dataset
from src.icc.metrics import evaluate_all
from src.icc.baselines.classical import run_kmeans
from src.icc.baselines.consensus import (
    run_standard_consensus,
    run_li_et_al_2019,
    run_icc_v1,
    run_icc_v2,
)

EXP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = EXP_DIR / "data"
FIGURES_DIR = EXP_DIR / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

METHODS = {
    "K-Means": run_kmeans,
    "Standard_Consensus": run_standard_consensus,
    "Li_et_al_2019": run_li_et_al_2019,
    "ICC_v1": run_icc_v1,
    "ICC_v2": run_icc_v2,
}


def inject_mcar_noise(X: np.ndarray, rho: float, seed: int = 42) -> np.ndarray:
    """Inject Missing Completely At Random (MCAR) NaN masks at rate rho."""
    if rho <= 0.0:
        return X.copy()
    rng = np.random.default_rng(seed)
    X_missing = X.copy()
    mask = rng.random(size=X.shape) < rho
    # Ensure no row is 100% NaN
    row_all_nan = np.all(mask, axis=1)
    if np.any(row_all_nan):
        mask[row_all_nan, rng.choice(X.shape[1], size=np.sum(row_all_nan))] = False
    X_missing[mask] = np.nan
    return X_missing


def impute_data(X_nan: np.ndarray, strategy: str = "mean") -> np.ndarray:
    """Impute NaN entries via specified statistical strategy."""
    if not np.isnan(X_nan).any():
        return X_nan

    if strategy == "mean":
        imp = SimpleImputer(strategy="mean")
        return imp.fit_transform(X_nan)
    elif strategy == "median":
        imp = SimpleImputer(strategy="median")
        return imp.fit_transform(X_nan)
    elif strategy == "zero":
        imp = SimpleImputer(strategy="constant", fill_value=0.0)
        return imp.fit_transform(X_nan)
    elif strategy == "knn":
        imp = KNNImputer(n_neighbors=5)
        return imp.fit_transform(X_nan)
    else:
        raise ValueError(f"Unknown imputation strategy: {strategy}")


def run_missing_data_sweep(
    datasets=None,
    rho_levels=None,
    strategies=None,
    n_trials=3,
    output_csv=None,
):
    if datasets is None:
        datasets = ["colon", "leukemia", "srbct"]
    if rho_levels is None:
        rho_levels = [0.0, 0.10, 0.20, 0.30, 0.50, 0.70]
    if strategies is None:
        strategies = ["mean", "median", "knn", "zero"]
    if output_csv is None:
        output_csv = DATA_DIR / "exp3_5_missing_data_results.csv"

    print(f"[*] Starting Exp 3.5 Missing Data Robustness Sweep ({n_trials} trials)...")
    records = []
    t_start = time.time()

    for dname in datasets:
        X_orig, y_true, meta = load_dataset(dname)
        K = meta["K"]
        print(f"\n---> Dataset: {dname.upper()} (N={meta['N']}, D={meta['D']}, K={K})")

        for rho in rho_levels:
            print(f"  Rate rho={rho:.2f}:", end=" ", flush=True)

            for strat in strategies:
                # If rho=0, running multiple imputation strategies is redundant
                if rho == 0.0 and strat != "mean":
                    continue

                for trial in range(n_trials):
                    trial_seed = 42 + trial * 31
                    X_corrupted = inject_mcar_noise(X_orig, rho=rho, seed=trial_seed)
                    X_imputed = impute_data(X_corrupted, strategy=strat)

                    for mname, mfn in METHODS.items():
                        try:
                            labels, rtime, _ = mfn(X_imputed, k=K, seed=trial_seed)
                            scores = evaluate_all(y_true, labels)
                            records.append({
                                "dataset": dname,
                                "rho": rho,
                                "strategy": strat,
                                "method": mname,
                                "trial": trial,
                                "ari": scores["ari"],
                                "nmi": scores["nmi"],
                                "ami": scores["ami"],
                                "v_measure": scores["v_measure"],
                                "runtime": rtime,
                            })
                        except Exception as e:
                            pass
            print("OK", flush=True)

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    print(f"\n[OK] Exp 3.5 completed in {time.time() - t_start:.2f}s")
    print(f"[+] Saved results to {output_csv} ({len(df)} evaluations)")
    return df


if __name__ == "__main__":
    run_missing_data_sweep(n_trials=2)
