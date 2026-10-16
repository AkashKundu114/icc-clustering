"""
Experiment 4.2: K-Misspecification Sensitivity & Model Degradation Profile.

Evaluates clustering robustness across mis-specified cluster counts K_input != K_true:
- Evaluates across Synthetic (K_true=3), Sonar (K_true=2), and SRBCT (K_true=4).
- Sweeps K_input around K_true across 8 benchmark clustering frameworks:
  1. K-Means
  2. Ward
  3. Spectral
  4. FCM
  5. Standard Consensus
  6. Li et al. (2019)
  7. ICC-v1
  8. ICC-v2
"""

import os
import time
from pathlib import Path
import numpy as np
import pandas as pd

from icc.core import build_dataset
from icc.datasets import load_dataset
from icc.metrics import evaluate_all
from icc.baselines.classical import run_kmeans, run_ward, run_spectral, run_fcm
from icc.baselines.consensus import (
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
    "Ward": run_ward,
    "Spectral": run_spectral,
    "FCM": run_fcm,
    "Standard_Consensus": run_standard_consensus,
    "Li_et_al_2019": run_li_et_al_2019,
    "ICC_v1": run_icc_v1,
    "ICC_v2": run_icc_v2,
}


def load_target_data(dataset_name: str, seed: int = 42):
    """Load or generate benchmark dataset."""
    if dataset_name == "Synthetic":
        X, y = build_dataset(d_noise=1000, noise_kind="scaled", noise_seed=seed, n_per_cluster=100, k=3, signal_dim=2)
        k_true = 3
    elif dataset_name == "Sonar":
        X, y, meta = load_dataset("sonar")
        k_true = meta["K"]
    elif dataset_name == "SRBCT":
        X, y, meta = load_dataset("srbct")
        k_true = meta["K"]
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")
    return X, y, k_true


def run_k_sweep_experiment(n_trials: int = 10, output_csv: Path = None):
    """
    Executes K-misspecification sweep across 3 datasets and 8 methods.
    Sweeps K_input from max(2, K_true - 3) to K_true + 5.
    """
    print(f"[*] Starting Experiment 4.2 K-Misspecification Sweep ({n_trials} trials)...")
    if output_csv is None:
        output_csv = DATA_DIR / "exp4_2_k_misspecification_results.csv"

    dataset_configs = {
        "Synthetic": {"k_true": 3},
        "Sonar":     {"k_true": 2},
        "SRBCT":     {"k_true": 4},
    }

    records = []
    t_start = time.time()

    for dname, cfg in dataset_configs.items():
        k_true = cfg["k_true"]
        k_range = list(range(max(2, k_true - 3), k_true + 5 + 1))
        print(f"\n--- Benchmarking {dname} (K_true={k_true}) across K in {k_range} ---")

        for trial in range(n_trials):
            trial_seed = 42 + trial * 101
            X, y, _ = load_target_data(dname, seed=trial_seed)

            for k_in in k_range:
                for mname, mfn in METHODS.items():
                    try:
                        labels, runtime, _ = mfn(X, k=k_in, seed=trial_seed)
                        scores = evaluate_all(y, labels)
                        records.append({
                            "dataset": dname,
                            "k_true": k_true,
                            "k_input": k_in,
                            "k_delta": k_in - k_true,
                            "method": mname,
                            "trial": trial,
                            "ari": scores["ari"],
                            "nmi": scores["nmi"],
                            "ami": scores["ami"],
                            "v_measure": scores["v_measure"],
                            "fm_index": scores["fm_index"],
                            "runtime": runtime,
                        })
                    except Exception as e:
                        print(f"[!] Error on {dname} k={k_in} {mname} trial {trial}: {e}")

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    print(f"\n[OK] Completed K-misspecification sweep in {time.time() - t_start:.2f}s")
    print(f"[+] Results saved to {output_csv} ({len(df)} evaluations)")
    return df


if __name__ == "__main__":
    run_k_sweep_experiment(n_trials=10)
