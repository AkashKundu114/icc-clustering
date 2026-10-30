"""
Empirical stability and accuracy evaluation across real-world benchmark datasets.

Investigates the "stability-accuracy trap" in unsupervised clustering across
13 benchmark datasets and 12 clustering algorithms:
- Canonical Seeds: 30 random seeds (0..29) for 6 high-dimensional datasets (D/N > 20)
  and 10 random seeds (0..9) for 7 lower-dimensional benchmarks.
- Per-Seed Caching: Persists partition label vectors into
  `results/stability/labels/{dataset}_{model}_seed_{seed}.npy` for reproducible auditing.

Mathematical Metrics:
---------------------
1. Mean Accuracy:
   Mean ground-truth agreement: (1/S) * sum_{s=1}^S ARI(y_pred^(s), y_true)
2. Partition Stability:
   Mean pairwise agreement across distinct random seeds:
   (2 / (S * (S - 1))) * sum_{i < j} ARI(y_pred^(i), y_pred^(j))
3. Stability-Accuracy Gap:
   Delta = Stability - Mean Accuracy
   A large positive gap reveals the stability trap: the algorithm produces highly
   reproducible partitions that nonetheless align poorly with true biological/data classes.

Outputs:
--------
- results/stability/real_data_stability_summary.csv
- results/stability/labels/*.npy

Usage:
------
    python scripts/reproduce_stability.py
    python scripts/reproduce_stability.py --only-dataset colon --skip-dec
"""

import argparse
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

# Ensure project root is in sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from icc.baselines import (
    run_cohirf,
    run_dec,
    run_fastmvc,
    run_fcag,
    run_fcm,
    run_icc_v1,
    run_icc_v2,
    run_kmeans,
    run_li_et_al_2019,
    run_spectral,
    run_standard_consensus,
    run_ward,
)
from icc.datasets.registry import load_dataset

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
    "Ungated_Anchor": run_icc_v1,       # Unanchored/ungated anchor baseline
    "GAC_Pipeline": run_icc_v2,         # Geometry-calibrated consensus (ICC-v2)
    "DEC": run_dec,
}

LABELS_DIR = ROOT / "results" / "stability" / "labels"


def get_seeds(dataset_name: str, max_seeds: int = None):
    """
    Get evaluation random seeds for a dataset.
    
    High-dimensional datasets (D/N > 20) receive 30 seeds; others receive 10 seeds.
    """
    if dataset_name in HIGH_D_DATASETS:
        seeds = list(range(30))
    else:
        seeds = list(range(10))
    if max_seeds is not None:
        return seeds[:max_seeds]
    return seeds


def run_model_seed(model_name: str, fn, X: np.ndarray, k: int, seed: int, dataset_name: str) -> np.ndarray:
    """
    Execute a single model run with disk caching for reproducible partition reuse.
    """
    LABELS_DIR.mkdir(parents=True, exist_ok=True)
    save_path = LABELS_DIR / f"{dataset_name}_{model_name}_seed_{seed}.npy"
    if save_path.exists():
        return np.load(save_path)

    # Ward's hierarchical agglomeration is strictly deterministic across seeds
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
    """
    Compute mean ground truth accuracy, pairwise stability, and stability gap.

    Parameters
    ----------
    labels_list : list of np.ndarray
        List of cluster assignment vectors across random seeds.
    y_true : np.ndarray
        Ground-truth class label vector.

    Returns
    -------
    dict
        Dictionary containing mean_ari, std_ari, stability, std_stability, and gap.
    """
    S = len(labels_list)
    # Ground truth accuracy across seeds
    aris = [adjusted_rand_score(y_true, pred) for pred in labels_list]
    mean_ari = float(np.mean(aris))
    std_ari = float(np.std(aris, ddof=1)) if S > 1 else 0.0

    # Pairwise partition stability across distinct seeds
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


def evaluate_stability(datasets=None, models_dict=None, max_seeds=None):
    """
    Run real data stability benchmark across datasets and models.
    """
    if datasets is None:
        datasets = ALL_DATASETS
    if models_dict is None:
        models_dict = dict(MODELS)

    records = []
    print(f"[*] Starting Real-Data Stability Benchmark ({len(datasets)} datasets, {len(models_dict)} models)...")

    for d_idx, d_name in enumerate(datasets, 1):
        print(f"\n[{d_idx}/{len(datasets)}] Loading dataset: {d_name} ({DISPLAY_NAMES.get(d_name, d_name)})")
        X, y, meta = load_dataset(d_name)
        k = len(np.unique(y))
        seeds = get_seeds(d_name, max_seeds=max_seeds)
        print(f"    Shape: {X.shape}, K={k}, Seeds={len(seeds)}")

        for m_name, fn in models_dict.items():
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
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    print(f"\n[+] Saved stability summary to: {out_csv}")
    return df


def main():
    parser = argparse.ArgumentParser(description="Evaluate real-data stability and accuracy across clustering methods.")
    parser.add_argument("--skip-dec", action="store_true", help="Skip Deep Embedded Clustering to reduce execution time.")
    parser.add_argument("--only-dataset", type=str, default=None, help="Evaluate a single dataset by name.")
    parser.add_argument("--max-seeds", type=int, default=None, help="Cap the number of seeds per dataset for fast runs.")
    args = parser.parse_args()

    models_to_run = dict(MODELS)
    if args.skip_dec:
        models_to_run.pop("DEC", None)

    target_datasets = [args.only_dataset] if args.only_dataset else ALL_DATASETS
    evaluate_stability(datasets=target_datasets, models_dict=models_to_run, max_seeds=args.max_seeds)


if __name__ == "__main__":
    main()
