"""
Experiment 2.1: Variance-Guided Subspace Generation (VSSG) Interpretability & Feature Selection Audit.

Quantifies the fidelity of VSSG feature scoring:
1. Test Case A: Madelon real-world distractor benchmark (500 features, 20 informative).
2. Test Case B: Ultra-high-dimensional synthetic benchmark (D=10,000, 50 informative signal features).
3. Test Case C: Dimensional noise stress sweep (D_noise in [0, 50, 200, 500, 1000, 5000, 10000]).
"""

import os
import time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew
from sklearn.feature_selection import mutual_info_classif

from icc.core import build_dataset
from icc.consensus_v2 import InvariantCoreConsensusV2
from icc.datasets import load_dataset

EXP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = EXP_DIR / "data"
FIGURES_DIR = EXP_DIR / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def compute_vssg_scores(X: np.ndarray) -> np.ndarray:
    """Compute VSSG bimodality / dispersion saliency scores across features."""
    kurt = kurtosis(X, axis=0)
    sk = skew(X, axis=0)
    bimodal = (sk**2 + 1.0) / (kurt + 3.0 + 1e-5)
    return bimodal


def evaluate_precision_recall(selected_indices, true_indices, k_cutoff):
    """Compute Precision@K and Recall@K."""
    top_k = set(selected_indices[:k_cutoff])
    true_set = set(true_indices)
    tp = len(top_k.intersection(true_set))
    precision = tp / k_cutoff if k_cutoff > 0 else 0.0
    recall = tp / len(true_set) if len(true_set) > 0 else 0.0
    return precision, recall, tp


def run_madelon_audit(n_trials=10, random_seed=42):
    """
    Test Case A: Madelon feature recovery.
    Madelon has 500 features with exactly 20 informative non-linear features.
    """
    print("[*] Running Test Case A: Madelon Feature Selection Audit...")
    X, y, meta = load_dataset("madelon")
    N, D = X.shape

    # Determine ground-truth informative features using mutual info
    mi = mutual_info_classif(X, y, random_state=random_seed)
    true_informative_idx = np.argsort(mi)[-20:]

    k_cutoffs = [10, 20, 30, 50, 100]
    records = []

    rng = np.random.default_rng(random_seed)
    for trial in range(n_trials):
        seed_trial = int(rng.integers(0, 100000))
        # Bootstrapped subsample of 85% N for variance estimation across trials
        sub_idx = rng.choice(N, size=int(0.85 * N), replace=False)
        X_sub = X[sub_idx]
        
        # Run ICC-v2's VSSG feature scoring (use consensus_v2.feature_scores_)
        icc = InvariantCoreConsensusV2(n_clusters=2, n_base_models=10, random_state=seed_trial)
        icc.fit(X_sub)
        scores = icc.feature_scores_
        ranked_features = np.argsort(scores)[::-1]  # Highest scores first

        for k in k_cutoffs:
            prec, rec, tp = evaluate_precision_recall(ranked_features, true_informative_idx, k)
            records.append({
                "test_case": "Madelon",
                "trial": trial,
                "K_cutoff": k,
                "precision": prec,
                "recall": rec,
                "true_positives": tp,
                "total_true": len(true_informative_idx),
                "D_total": D,
            })

    df = pd.DataFrame(records)
    out_csv = DATA_DIR / "exp2_1_madelon_pr.csv"
    df.to_csv(out_csv, index=False)
    print(f"[+] Saved Madelon audit results to {out_csv}")
    return df


def run_synthetic_high_d_audit(n_trials=10, signal_dim=50, d_noise=9950, random_seed=42):
    """
    Test Case B: Synthetic D=10,000 feature recovery (N=500, K=3, 50 informative).
    """
    print(f"[*] Running Test Case B: Synthetic High-D Audit (N=500, D={signal_dim + d_noise}, Signal={signal_dim})...")
    k_cutoffs = [25, 50, 75, 100, 200]
    true_signal_indices = list(range(signal_dim))
    records = []

    rng = np.random.default_rng(random_seed)
    for trial in range(n_trials):
        seed_trial = int(rng.integers(0, 100000))
        X, y = build_dataset(
            d_noise=d_noise,
            noise_kind="scaled",
            noise_seed=seed_trial,
            sizes=[167, 167, 166],  # N=500
            k=3,
            signal_dim=signal_dim,
        )
        
        # Run ICC-v2's VSSG feature scoring (use consensus_v2.feature_scores_)
        icc = InvariantCoreConsensusV2(n_clusters=3, n_base_models=10, random_state=seed_trial)
        icc.fit(X)
        scores = icc.feature_scores_
        ranked_features = np.argsort(scores)[::-1]

        for k in k_cutoffs:
            prec, rec, tp = evaluate_precision_recall(ranked_features, true_signal_indices, k)
            records.append({
                "test_case": "Synthetic_10kD",
                "trial": trial,
                "K_cutoff": k,
                "precision": prec,
                "recall": rec,
                "true_positives": tp,
                "total_true": signal_dim,
                "D_total": X.shape[1],
            })

    df = pd.DataFrame(records)
    out_csv = DATA_DIR / "exp2_1_synthetic_10kd_pr.csv"
    df.to_csv(out_csv, index=False)
    print(f"[+] Saved Synthetic High-D audit results to {out_csv}")
    return df


def run_noise_sweep_audit(n_trials=10, signal_dim=50, random_seed=42):
    """
    Test Case C: Noise dimension sweep D_noise in [0, 50, 200, 500, 1000, 5000].
    Tracks how Recall@50 degrades as noise increases.
    """
    print("[*] Running Test Case C: Noise Dimension Sweep Audit...")
    noise_dims = [0, 50, 200, 500, 1000, 5000]
    true_signal_indices = list(range(signal_dim))
    records = []

    rng = np.random.default_rng(random_seed)
    for d_noise in noise_dims:
        for trial in range(n_trials):
            seed_trial = int(rng.integers(0, 100000))
            if d_noise == 0:
                X, y = build_dataset(
                    d_noise=0,
                    noise_seed=seed_trial,
                    sizes=[167, 167, 166],
                    k=3,
                    signal_dim=signal_dim,
                )
            else:
                X, y = build_dataset(
                    d_noise=d_noise,
                    noise_kind="scaled",
                    noise_seed=seed_trial,
                    sizes=[167, 167, 166],
                    k=3,
                    signal_dim=signal_dim,
                )

            # Run ICC-v2's VSSG feature scoring (use consensus_v2.feature_scores_)
            icc = InvariantCoreConsensusV2(n_clusters=3, n_base_models=10, random_state=seed_trial)
            icc.fit(X)
            scores = icc.feature_scores_
            ranked_features = np.argsort(scores)[::-1]

            # Evaluate at K = signal_dim (Recall@50) and K = 2 * signal_dim (Recall@100)
            prec50, rec50, tp50 = evaluate_precision_recall(ranked_features, true_signal_indices, signal_dim)
            prec100, rec100, tp100 = evaluate_precision_recall(
                ranked_features, true_signal_indices, min(X.shape[1], 2 * signal_dim)
            )

            records.append({
                "test_case": "Noise_Sweep",
                "d_noise": d_noise,
                "d_total": signal_dim + d_noise,
                "trial": trial,
                "precision_at_50": prec50,
                "recall_at_50": rec50,
                "precision_at_k": prec50,
                "recall_at_k": rec50,
                "recall_at_2k": rec100,
            })

    df = pd.DataFrame(records)
    out_csv = DATA_DIR / "exp2_1_noise_sweep_pr.csv"
    df.to_csv(out_csv, index=False)
    print(f"[+] Saved Noise Sweep audit results to {out_csv}")
    return df


def run_all(n_trials=10):
    t0 = time.time()
    df_mad = run_madelon_audit(n_trials=n_trials)
    df_syn = run_synthetic_high_d_audit(n_trials=n_trials)
    df_swp = run_noise_sweep_audit(n_trials=n_trials)
    print(f"[OK] Exp 2.1 completed in {time.time() - t0:.2f}s")


if __name__ == "__main__":
    run_all(n_trials=5)
