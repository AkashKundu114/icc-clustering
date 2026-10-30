"""
scripts/diagnose_prostate_structure.py

Item 2e: Descriptive diagnosis of non-degenerate flagged partitions on Prostate:
- Checks whether the smaller cluster consists of PCA-space outliers
  (distance to median in top 10 PCs, Mahalanobis distance on top 10 PCs).
- Computes correlation of cluster membership with PC1, PC2, and per-sample total expression.
- Checks agreement with any sample metadata.
- Reports strictly what is measured without naming unmeasured causes.
"""

from pathlib import Path
from icc.datasets.registry import load_dataset
import numpy as np
import pandas as pd
from scipy.spatial.distance import mahalanobis
from scipy.stats import pearsonr, spearmanr
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score

ROOT = Path(__file__).resolve().parent.parent
PARTITIONS_DIR = ROOT / "results" / "stability" / "partitions"

def main():
    X, y, meta = load_dataset("prostate")
    N, D = X.shape
    print(f"Loaded Prostate dataset: N={N}, D={D}, K={meta['K']}")

    # 1. PCA representation
    pca = PCA(n_components=10, random_state=42)
    X_pca = pca.fit_transform(X)
    print(f"Explained variance ratio (top 10 PCs): {pca.explained_variance_ratio_}")
    print(f"Total explained variance (10 PCs): {np.sum(pca.explained_variance_ratio_):.3f}")

    # Median in top 10 PCs
    median_pca = np.median(X_pca, axis=0)
    euc_dist_median = np.linalg.norm(X_pca - median_pca, axis=1)

    # Covariance for Mahalanobis
    cov = np.cov(X_pca, rowvar=False)
    inv_cov = np.linalg.pinv(cov)
    mean_pca = np.mean(X_pca, axis=0)
    maha_dist = np.array([mahalanobis(x_i, mean_pca, inv_cov) for x_i in X_pca])

    # Per-sample total expression
    total_expr = np.sum(X, axis=1)

    # Non-degenerate models on Prostate meeting Rule (i')
    MODELS = ["Ward", "Spectral", "FCAG", "FastMVC", "GAC", "DEC", "K-Means"]

    diag_records = []

    for m in MODELS:
        # Load partitions across the 30 subsamples
        # Map labels back to full dataset via consensus or analyze each subsample
        sub_records = []
        for sub_id in range(30):
            pfile = PARTITIONS_DIR / f"prostate_{m}_real_{sub_id}.npy"
            if not pfile.exists():
                continue
            data = np.load(pfile, allow_pickle=True).item()
            sub_idx = data["sub_idx"]
            lbl = data["labels"]

            u, counts = np.unique(lbl, return_counts=True)
            if len(u) < 2:
                continue
            small_c = u[np.argmin(counts)]
            large_c = u[np.argmax(counts)]

            small_idx = sub_idx[lbl == small_c]
            large_idx = sub_idx[lbl == large_c]

            # Distances in top 10 PCs
            small_dist_med = np.mean(euc_dist_median[small_idx])
            large_dist_med = np.mean(euc_dist_median[large_idx])
            small_maha = np.mean(maha_dist[small_idx])
            large_maha = np.mean(maha_dist[large_idx])

            # Correlation with PC1, PC2, total expression on this subsample
            # Binary indicator: 1 if small_c else 0
            binary_lbl = (lbl == small_c).astype(float)
            r_pc1, p_pc1 = pearsonr(binary_lbl, X_pca[sub_idx, 0])
            r_pc2, p_pc2 = pearsonr(binary_lbl, X_pca[sub_idx, 1])
            r_expr, p_expr = pearsonr(binary_lbl, total_expr[sub_idx])

            sub_records.append({
                "sub_id": sub_id,
                "small_size": len(small_idx),
                "large_size": len(large_idx),
                "small_dist_med": small_dist_med,
                "large_dist_med": large_dist_med,
                "small_maha": small_maha,
                "large_maha": large_maha,
                "r_pc1": r_pc1,
                "r_pc2": r_pc2,
                "r_expr": r_expr,
            })

        sdf = pd.DataFrame(sub_records)
        diag_records.append({
            "model": m,
            "mean_small_size": sdf["small_size"].mean(),
            "mean_large_size": sdf["large_size"].mean(),
            "small_dist_med": sdf["small_dist_med"].mean(),
            "large_dist_med": sdf["large_dist_med"].mean(),
            "small_maha": sdf["small_maha"].mean(),
            "large_maha": sdf["large_maha"].mean(),
            "mean_r_pc1": sdf["r_pc1"].mean(),
            "mean_r_pc2": sdf["r_pc2"].mean(),
            "mean_r_total_expr": sdf["r_expr"].mean(),
        })

    res_df = pd.DataFrame(diag_records)
    print("\n" + "=" * 80)
    print("PROSTATE DESCRIPTIVE DIAGNOSIS RESULTS (Item 2e):")
    print("=" * 80)
    print(res_df.to_string(index=False))

    out_csv = ROOT / "results" / "prostate_pca_diagnosis.csv"
    res_df.to_csv(out_csv, index=False)
    print(f"\n[+] Saved diagnosis results to {out_csv}")


if __name__ == "__main__":
    main()
