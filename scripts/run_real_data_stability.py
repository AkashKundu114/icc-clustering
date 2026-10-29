"""
scripts/run_real_data_stability.py

Real-Data Stability Test across 13 benchmark datasets and 12 clustering methods:
- Canonical seeds: 30 seeds (0..29) for 6 high-D datasets (D/N > 20),
                   10 seeds (0..9) for 7 other datasets.
- Saves per-seed label vectors into results/stability/labels/{dataset}_{model}_seed_{seed}.npy.
- Computes:
    - Mean Accuracy: ARI(y_pred_s, y_true) averaged across seeds.
    - Stability: Mean pairwise ARI(y_pred_i, y_pred_j) across all i < j.
    - Stability-Accuracy Gap: Stability - Mean Accuracy.
- Outputs:
    - results/stability/real_data_stability_summary.csv
    - paper/gen/table_real_data_stability.tex
    - springer_manuscript/gen/table_real_data_stability.tex
    - paper/figures/fig_real_data_stability.png
    - springer_manuscript/figures/fig_real_data_stability.png
"""

import os
import sys
import time
from pathlib import Path
from itertools import combinations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import adjusted_rand_score

# Ensure root in sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from icc.datasets.registry import load_dataset
from icc.baselines import (
    run_kmeans,
    run_ward,
    run_spectral,
    run_fcm,
    run_standard_consensus,
    run_li_et_al_2019,
    run_icc_v1,
    run_icc_v2,
    run_fcag,
    run_fastmvc,
    run_cohirf,
    run_dec,
)

HIGH_D_DATASETS = ["colon", "srbct", "cns", "leukemia", "prostate", "ovarian"]
OTHER_DATASETS = ["sonar", "madelon", "isolet", "zheng68k", "newsgroups20", "indian_pines", "yale_b"]
ALL_DATASETS = HIGH_D_DATASETS + OTHER_DATASETS

DISPLAY_NAMES = {
    "cns": "CNS",
    "colon": "Colon",
    "leukemia": "Leukemia",
    "ovarian": "Ovarian",
    "prostate": "Prostate",
    "srbct": "SRBCT",
    "sonar": "Sonar",
    "madelon": "Madelon",
    "isolet": "Isolet",
    "zheng68k": "PBMC68k-red",
    "newsgroups20": "20 News",
    "indian_pines": "Indian Pines",
    "yale_b": "Ext. Yale B",
}

MODELS = {
    "K-Means": run_kmeans,
    "Ward": run_ward,
    "Spectral": run_spectral,
    "FCM": run_fcm,
    "Standard_Consensus": run_standard_consensus,
    "Core_Halo_Consensus": run_li_et_al_2019,
    "FCAG": run_fcag,
    "FastMVC": run_fastmvc,
    "CoHiRF": run_cohirf,
    "Ungated_Anchor": run_icc_v1,       # Formerly ICC-v1
    "GAC_Pipeline": run_icc_v2,         # Formerly ICC-v2
    "DEC": run_dec,
}

LABELS_DIR = ROOT / "results" / "stability" / "labels"
LABELS_DIR.mkdir(parents=True, exist_ok=True)


def get_seeds(dataset_name: str):
    if dataset_name in HIGH_D_DATASETS:
        return list(range(30))
    return list(range(10))


def run_model_seed(model_name: str, fn, X: np.ndarray, k: int, seed: int, dataset_name: str) -> np.ndarray:
    """Run model on seed with caching."""
    save_path = LABELS_DIR / f"{dataset_name}_{model_name}_seed_{seed}.npy"
    if save_path.exists():
        return np.load(save_path)

    # Optimization: Ward is deterministic across seeds
    if model_name == "Ward" and seed > 0:
        seed0_path = LABELS_DIR / f"{dataset_name}_{model_name}_seed_0.npy"
        if seed0_path.exists():
            labels = np.load(seed0_path)
            np.save(save_path, labels)
            return labels

    labels, _, _ = fn(X, k, seed=seed)
    np.save(save_path, labels)
    return labels


def compute_metrics(labels_list, y_true):
    S = len(labels_list)
    # Mean accuracy (ARI vs ground truth)
    aris = [adjusted_rand_score(y_true, pred) for pred in labels_list]
    mean_ari = float(np.mean(aris))
    std_ari = float(np.std(aris, ddof=1)) if S > 1 else 0.0

    # Stability: pairwise ARI across seeds
    if S > 1:
        pair_aris = [
            adjusted_rand_score(labels_list[i], labels_list[j])
            for i, j in combinations(range(S), 2)
        ]
        mean_stab = float(np.mean(pair_aris))
        std_stab = float(np.std(pair_aris, ddof=1))
    else:
        mean_stab = 1.0
        std_stab = 0.0

    gap = mean_stab - mean_ari
    return {
        "mean_ari": mean_ari,
        "std_ari": std_ari,
        "stability": mean_stab,
        "std_stability": std_stab,
        "gap": gap,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-dec", action="store_true", help="Skip DEC to run faster")
    parser.add_argument("--only-dataset", type=str, default=None, help="Run single dataset")
    args = parser.parse_args()

    models_to_run = dict(MODELS)
    if args.skip_dec:
        models_to_run.pop("DEC", None)

    datasets = [args.only_dataset] if args.only_dataset else ALL_DATASETS

    records = []
    print(f"[*] Starting Real-Data Stability Benchmark ({len(datasets)} datasets, {len(models_to_run)} models)...")

    for d_idx, d_name in enumerate(datasets, 1):
        print(f"\n[{d_idx}/{len(datasets)}] Loading dataset: {d_name} ({DISPLAY_NAMES.get(d_name, d_name)})")
        X, y, meta = load_dataset(d_name)
        k = len(np.unique(y))
        seeds = get_seeds(d_name)
        print(f"    Shape: {X.shape}, K={k}, Seeds={len(seeds)}")

        for m_name, fn in models_to_run.items():
            t0 = time.time()
            labels_list = []
            for s in seeds:
                lbls = run_model_seed(m_name, fn, X, k, s, d_name)
                labels_list.append(lbls)
            elapsed = time.time() - t0

            met = compute_metrics(labels_list, y)
            print(f"    {m_name:18s} | Acc={met['mean_ari']:+.3f} | Stab={met['stability']:.3f} | Gap={met['gap']:+.3f} ({elapsed:.1f}s)")

            records.append({
                "dataset": d_name,
                "dataset_display": DISPLAY_NAMES.get(d_name, d_name),
                "is_high_d": d_name in HIGH_D_DATASETS,
                "N": X.shape[0],
                "D": X.shape[1],
                "K": k,
                "n_seeds": len(seeds),
                "model": m_name,
                "mean_ari": met["mean_ari"],
                "std_ari": met["std_ari"],
                "stability": met["stability"],
                "std_stability": met["std_stability"],
                "gap": met["gap"],
            })

    df = pd.DataFrame(records)
    out_csv = ROOT / "results" / "stability" / "real_data_stability_summary.csv"
    df.to_csv(out_csv, index=False)
    print(f"\n[+] Saved stability summary to: {out_csv}")


if __name__ == "__main__":
    main()
