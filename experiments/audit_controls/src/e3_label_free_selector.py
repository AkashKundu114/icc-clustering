"""
Label-Free Pool-Size Selector Evaluation across 8 Cached Real Datasets.

Evaluates unsupervised criteria for selecting pool fraction rho in:
[0.02, 0.05, 0.10, 0.15, 0.25, 0.40, 1.00]
without using ground-truth cluster labels.

Criteria evaluated:
1. Ensemble Base Model Cohesion: Mean pairwise ARI across base partitions
2. Mean Core Determinacy: Average sample-level stability sigma_i
3. Candidate Pool Silhouette: Silhouette score on the selected subspace features
4. Full Space Silhouette: Silhouette score on all D features
5. Co-association Contrast Ratio: (within-cluster S_ij) / (between-cluster S_ij)
"""

import glob
import os
import sys
from pathlib import Path
import warnings

# Ensure project root is on sys.path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score as ari_score
from sklearn.metrics import silhouette_score

warnings.filterwarnings("ignore")

from icc.consensus_v2 import InvariantCoreConsensusV2 as ICC
from icc.core import run_clusterer, pairwise_coassoc

def evaluate_pool_metrics(X, k, pool_frac, seed=42, n_base_models=25, n_anchors=30):
    N, D = X.shape
    rng = np.random.default_rng(seed)
    
    # Run ICC model with pool_mode='bc_frac'
    model = ICC(
        n_clusters=k,
        n_base_models=n_base_models,
        n_anchors=n_anchors,
        random_state=seed,
        pool_mode="bc_frac",
        pool_frac=pool_frac,
    )
    labels = model.fit_predict(X)
    pool = model.selected_features_
    
    # 1. Base ensemble partitions for pairwise agreement
    # We reconstruct the base partitions from model's candidate pool
    sub_size = max(2, int(len(pool) * model.subspace_rate))
    base_engine = "kmeans" if N > 100 else "spectral"
    partitions = []
    for m in range(n_base_models):
        seed_m = int(rng.integers(0, 1000000))
        sub_idx = rng.choice(pool, size=sub_size, replace=False)
        p = run_clusterer(base_engine, X[:, sub_idx], k, seed=seed_m)
        partitions.append(p)
        
    # Pairwise agreement between base partitions (Ensemble Cohesion)
    n_pairs = 0
    sum_ari = 0.0
    for i in range(n_base_models):
        for j in range(i + 1, n_base_models):
            sum_ari += ari_score(partitions[i], partitions[j])
            n_pairs += 1
    mean_base_ari = sum_ari / max(1, n_pairs)
    
    # 2. Mean Core Determinacy (sample stability)
    mean_determinacy = float(np.mean(model.stability_)) if model.stability_ is not None else 0.0
    
    # 3. Silhouette on candidate pool features
    if len(np.unique(labels)) > 1 and len(pool) >= 2:
        try:
            sil_pool = float(silhouette_score(X[:, pool], labels, metric="euclidean"))
        except Exception:
            sil_pool = -1.0
    else:
        sil_pool = -1.0
        
    # 4. Silhouette on all features
    if len(np.unique(labels)) > 1:
        try:
            sil_all = float(silhouette_score(X, labels, metric="euclidean"))
        except Exception:
            sil_all = -1.0
    else:
        sil_all = -1.0
        
    # 5. Co-association contrast ratio from partitions
    S = pairwise_coassoc(partitions)
    same_mask = labels[:, None] == labels[None, :]
    np.fill_diagonal(same_mask, False)
    diff_mask = ~same_mask
    np.fill_diagonal(diff_mask, False)
    
    within_s = float(np.mean(S[same_mask])) if np.any(same_mask) else 0.0
    between_s = float(np.mean(S[diff_mask])) if np.any(diff_mask) else 0.0
    coassoc_ratio = within_s / max(1e-6, between_s)
    
    return {
        "labels": labels,
        "mean_base_ari": mean_base_ari,
        "mean_determinacy": mean_determinacy,
        "sil_pool": sil_pool,
        "sil_all": sil_all,
        "coassoc_ratio": coassoc_ratio,
    }


def main():
    fractions = [0.02, 0.05, 0.10, 0.15, 0.25, 0.40, 1.00]
    datasets = sorted(glob.glob("experiments/exp3_real_world_benchmarks/data/cache/*.npz"))
    
    results = []
    
    for f in datasets:
        name = os.path.basename(f)[:-4]
        d = np.load(f)
        X, y = d["X"].astype(float), d["y"]
        k = len(np.unique(y))
        
        print(f"\nProcessing {name} (N={X.shape[0]}, D={X.shape[1]}, K={k})...")
        
        for fq in fractions:
            aris = []
            base_aris = []
            dets = []
            sil_pools = []
            sil_alls = []
            coassoc_ratios = []
            
            for s in range(5):
                metrics = evaluate_pool_metrics(X, k, pool_frac=fq, seed=s)
                ari = ari_score(y, metrics["labels"])
                aris.append(ari)
                base_aris.append(metrics["mean_base_ari"])
                dets.append(metrics["mean_determinacy"])
                sil_pools.append(metrics["sil_pool"])
                sil_alls.append(metrics["sil_all"])
                coassoc_ratios.append(metrics["coassoc_ratio"])
                
            results.append({
                "dataset": name,
                "frac": fq,
                "ari_mean": float(np.mean(aris)),
                "ari_std": float(np.std(aris)),
                "base_ari_mean": float(np.mean(base_aris)),
                "det_mean": float(np.mean(dets)),
                "sil_pool_mean": float(np.mean(sil_pools)),
                "sil_all_mean": float(np.mean(sil_alls)),
                "coassoc_ratio_mean": float(np.mean(coassoc_ratios)),
            })
            
    df = pd.DataFrame(results)
    out_csv = "experiments/audit_controls/data/e3_label_free_selector_eval.csv"
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    df.to_csv(out_csv, index=False)
    print(f"\nSaved results to {out_csv}")
    
    # Evaluate selection criteria
    print("\n" + "=" * 80)
    print("LABEL-FREE POOL-SIZE SELECTION EVALUATION")
    print("=" * 80)
    
    crit_cols = ["base_ari_mean", "det_mean", "sil_pool_mean", "sil_all_mean", "coassoc_ratio_mean"]
    crit_names = {
        "base_ari_mean": "Ensemble Base Model Cohesion (Pairwise ARI)",
        "det_mean": "Mean Core Determinacy",
        "sil_pool_mean": "Subspace Silhouette",
        "sil_all_mean": "Ambient Silhouette",
        "coassoc_ratio_mean": "Co-association Contrast Ratio",
    }
    
    eval_summary = []
    
    for dname, grp in df.groupby("dataset"):
        best_oracle_row = grp.loc[grp["ari_mean"].idxmax()]
        oracle_frac = best_oracle_row["frac"]
        oracle_ari = best_oracle_row["ari_mean"]
        
        legacy_row = grp[grp["frac"] == 0.15].iloc[0]
        legacy_ari = legacy_row["ari_mean"]
        
        row_dict = {
            "dataset": dname,
            "oracle_frac": oracle_frac,
            "oracle_ari": round(oracle_ari, 3),
            "legacy_15pct_ari": round(legacy_ari, 3),
        }
        
        for col in crit_cols:
            selected_row = grp.loc[grp[col].idxmax()]
            sel_frac = selected_row["frac"]
            sel_ari = selected_row["ari_mean"]
            row_dict[f"{col}_frac"] = sel_frac
            row_dict[f"{col}_ari"] = round(sel_ari, 3)
            
        eval_summary.append(row_dict)
        
    df_eval = pd.DataFrame(eval_summary)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 250)
    print("\nPer-Dataset Selection Performance:")
    print(df_eval.to_string())
    
    print("\n" + "-" * 80)
    print("GRAND MEAN ARI ACROSS 8 DATASETS:")
    print("-" * 80)
    print(f"Oracle Best Fraction (Upper Bound):   {df_eval['oracle_ari'].mean():.4f}")
    print(f"Legacy Fixed 15% Floor:               {df_eval['legacy_15pct_ari'].mean():.4f}")
    for col in crit_cols:
        mean_ari = df_eval[f"{col}_ari"].mean()
        print(f"Selected by {crit_names[col]:<35}: {mean_ari:.4f}")
        
    summary_path = "experiments/audit_controls/data/e3_label_free_selector_summary.csv"
    df_eval.to_csv(summary_path, index=False)
    print(f"\nSaved evaluation summary to {summary_path}")

if __name__ == "__main__":
    main()
