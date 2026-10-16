"""
Experiment 3.3: Downstream Inductive Generalization on Real Cancer Benchmarks.
Tests whether certified Invariant Core pseudo-labels improve downstream classifier
generalization on held-out 30% test splits compared to training on all pseudo-labels.
"""

import os
import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from experiments.exp3_real_world_benchmarks.src.dataset_loader import load_benchmark_dataset
from experiments.exp3_real_world_benchmarks.src.benchmark_models import run_icc_v2, pairwise_coassoc, run_clusterer
from icc.core import adjusted_rand_score

OUTPUT_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "exp3_3_inductive_real_world.csv")
FIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "figures", "fig16_inductive_generalization_real_world.png")

TARGET_DATASETS = ["leukemia", "prostate", "srbct", "colon"]


def evaluate_inductive_nearest_centroid(X_train, y_train_pseudo, X_test, y_test_true, k):
    """Simple robust non-parametric nearest centroid inductive classifier."""
    centroids = []
    active_classes = []
    for c in range(k):
        mask = (y_train_pseudo == c)
        if np.any(mask):
            centroids.append(X_train[mask].mean(axis=0))
            active_classes.append(c)
        else:
            centroids.append(np.zeros(X_train.shape[1]))
            active_classes.append(c)
            
    centroids = np.array(centroids)  # (K, D)
    from scipy.spatial.distance import cdist
    dists = cdist(X_test, centroids, metric="sqeuclidean")
    test_preds = np.argmin(dists, axis=1)
    
    # Evaluate via ARI to account for cluster-to-class permutation
    return adjusted_rand_score(y_test_true, test_preds)


def run_sub_exp3_3(n_trials=10):
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    os.makedirs(os.path.dirname(FIG_PATH), exist_ok=True)
    
    print("=" * 80)
    print("RUNNING SUB-EXPERIMENT 3.3: DOWNSTREAM INDUCTIVE REAL-WORLD EVALUATION")
    print(f"Datasets: {TARGET_DATASETS}")
    print("=" * 80)
    
    records = []
    
    for dname in TARGET_DATASETS:
        print(f"\n---> Dataset: {dname.upper()}")
        X, y, meta = load_benchmark_dataset(dname)
        N, D, K = meta["N"], meta["D"], meta["K"]
        
        for t in range(n_trials):
            seed = 42 + t * 23
            rng = np.random.default_rng(seed)
            
            # 70/30 Stratified Split
            train_idx = []
            test_idx = []
            for c in np.unique(y):
                c_inds = np.where(y == c)[0]
                n_tr = int(0.70 * len(c_inds))
                perm = rng.permutation(c_inds)
                train_idx.extend(perm[:n_tr])
                test_idx.extend(perm[n_tr:])
                
            train_idx = np.array(train_idx)
            test_idx = np.array(test_idx)
            
            X_train, y_train = X[train_idx], y[train_idx]
            X_test, y_test = X[test_idx], y[test_idx]
            
            # Run ICC-v2 on train split to generate pseudo-labels and stability
            pred_train, _, lc = run_icc_v2(X_train, K, seed=seed)
            
            # Identify core mask on train split
            top_frac = min(1.0, max(0.15, 100.0 / D))
            from scipy.stats import kurtosis, skew
            bimodal = (skew(X_train, axis=0)**2 + 1.0) / (kurtosis(X_train, axis=0) + 3.0 + 1e-5)
            pool = np.argsort(bimodal)[-max(K, int(top_frac * D)):]
            
            sub_size = max(2, int(len(pool) * 0.30))
            parts = [run_clusterer("spectral" if len(train_idx) <= 100 else "kmeans", X_train[:, rng.choice(pool, size=sub_size, replace=False)], K, seed=s) for s in range(20)]
            S = pairwise_coassoc(parts)
            np.fill_diagonal(S, 0)
            stab = np.sum(S**2, axis=1) / (len(train_idx) - 1)
            core_mask = (stab >= np.median(stab))
            if np.sum(core_mask) < K:
                core_mask = np.ones(len(train_idx), dtype=bool)
                
            core_indices = np.where(core_mask)[0]
            rand_indices = rng.choice(len(train_idx), size=len(core_indices), replace=False)
            
            # Strategy 1: All Train Pseudo-labels
            score_all = evaluate_inductive_nearest_centroid(X_train, pred_train, X_test, y_test, K)
            
            # Strategy 2: Core-Only Pseudo-labels
            score_core = evaluate_inductive_nearest_centroid(X_train[core_indices], pred_train[core_indices], X_test, y_test, K)
            
            # Strategy 3: Random Subset Pseudo-labels
            score_rand = evaluate_inductive_nearest_centroid(X_train[rand_indices], pred_train[rand_indices], X_test, y_test, K)
            
            records.append({
                "dataset": dname,
                "trial": t,
                "test_ari_all": score_all,
                "test_ari_core": score_core,
                "test_ari_random": score_rand,
                "core_fraction": len(core_indices) / len(train_idx)
            })
            
        sub = [r for r in records if r["dataset"] == dname]
        df_sub = pd.DataFrame(sub)
        print(f"     Test ARI: Core={df_sub['test_ari_core'].mean():.4f} | All={df_sub['test_ari_all'].mean():.4f} | Random={df_sub['test_ari_random'].mean():.4f}")
        
    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n[+] Results saved to: {OUTPUT_CSV}")
    
    plot_fig16_inductive(df)
    return df


def plot_fig16_inductive(df):
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 10.5,
        "axes.titlesize": 11.5,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 8.5,
        "figure.dpi": 300
    })
    
    datasets = TARGET_DATASETS
    x = np.arange(len(datasets))
    bar_width = 0.25
    
    fig, ax = plt.subplots(figsize=(9.8, 4.6), dpi=300)
    
    core_means = [df[df["dataset"] == d]["test_ari_core"].mean() for d in datasets]
    core_stds = [df[df["dataset"] == d]["test_ari_core"].std() for d in datasets]
    
    all_means = [df[df["dataset"] == d]["test_ari_all"].mean() for d in datasets]
    all_stds = [df[df["dataset"] == d]["test_ari_all"].std() for d in datasets]
    
    rand_means = [df[df["dataset"] == d]["test_ari_random"].mean() for d in datasets]
    rand_stds = [df[df["dataset"] == d]["test_ari_random"].std() for d in datasets]
    
    b1 = ax.bar(x - bar_width, all_means, yerr=all_stds, width=bar_width,
                label="All Pseudo-labels (100% data)", color="#1f77b4", edgecolor="black",
                hatch="//", linewidth=0.8, alpha=0.9, capsize=3.5)
    b2 = ax.bar(x, rand_means, yerr=rand_stds, width=bar_width,
                label="Random Subset Pseudo-labels (50% control)", color="#6c757d", edgecolor="black",
                hatch="..", linewidth=0.8, alpha=0.9, capsize=3.5)
    b3 = ax.bar(x + bar_width, core_means, yerr=core_stds, width=bar_width,
                label="Certified Core Pseudo-labels (50% core) [Ours]", color="#d62728", edgecolor="black",
                hatch="xx", linewidth=1.2, alpha=0.9, capsize=3.5)
                
    # Add numerical labels
    def annotate_bars(bars, stds):
        for bar, s in zip(bars, stds):
            h = bar.get_height()
            y_pos = h + s + 0.02 if h >= 0 else h - s - 0.04
            va = "bottom" if h >= 0 else "top"
            ax.annotate(f"{h:.3f}",
                        xy=(bar.get_x() + bar.get_width() / 2, y_pos),
                        xytext=(0, 0), textcoords="offset points",
                        ha="center", va=va, fontsize=8, fontweight="bold")
                        
    annotate_bars(b1, all_stds)
    annotate_bars(b2, rand_stds)
    annotate_bars(b3, core_stds)
    
    ax.axhline(0, color="black", linestyle="-", linewidth=0.8, alpha=0.7)
    ax.set_xticks(x)
    dataset_labels = [f"{d.upper()}\n({meta_str})" for d, meta_str in zip(
        datasets,
        ["D=7,129", "D=12,600", "D=2,308", "D=2,000"]
    )]
    ax.set_xticklabels(dataset_labels, fontweight="bold")
    ax.set_ylabel("Downstream Held-Out Test Recovery (ARI)", fontweight="bold")
    ax.set_title("Inductive Generalization Under 70/30 Train-Test Splits", fontweight="bold")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.92, facecolor="white", edgecolor="#cccccc")
    ax.set_ylim(-0.20, 0.82)
    
    plt.tight_layout()
    plt.savefig(FIG_PATH, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved: {FIG_PATH}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--replot", action="store_true", help="Only replot from existing CSV")
    parser.add_argument("--trials", type=int, default=10, help="Number of trials per dataset")
    args = parser.parse_args()
    
    if args.replot and os.path.exists(OUTPUT_CSV):
        print(f"[*] Re-generating Figure 16 directly from {OUTPUT_CSV}...")
        df_existing = pd.read_csv(OUTPUT_CSV)
        plot_fig16_inductive(df_existing)
    else:
        run_sub_exp3_3(n_trials=args.trials)
