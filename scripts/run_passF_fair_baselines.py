"""
Compute 30-seed Table 5 (Fair Feature-Matched Baselines) for Pass F:
Datasets: cns, colon, leukemia, ovarian, prostate, srbct
Models:
- K-Means_All
- K-Means_VarFilt
- K-Means_PCA
- K-Means_LapScore
- SparseKMeans
- StdCons_All
- StdCons_VarFilt
- StdCons_PCA
- ICC_v2
Seeds: 0-29 (30 seeds)
"""

import sys
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import adjusted_rand_score

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from icc.datasets.registry import load_dataset
from icc.consensus_v2 import InvariantCoreConsensusV2
from icc.baselines.consensus import run_standard_consensus
from scripts.run_passE_all import compute_laplacian_score, run_sparse_kmeans

OUT_DIR = Path("results/passF")
OUT_DIR.mkdir(parents=True, exist_ok=True)

HIGH_D_DATASETS = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]

def main():
    out_file = OUT_DIR / "fair_baselines_30seeds_passF.csv"
    existing_records = []
    done_keys = set()
    if out_file.exists():
        existing_records = pd.read_csv(out_file).to_dict(orient="records")
        done_keys = set((r['dataset'], r['model'], r['seed']) for r in existing_records)
        print(f"Found {len(existing_records)} existing records in {out_file}")

    if not existing_records and Path("results/passE/fair_baselines_seeds0_9.csv").exists():
        df_e = pd.read_csv("results/passE/fair_baselines_seeds0_9.csv")
        existing_records = df_e.to_dict(orient="records")
        done_keys = set((r['dataset'], r['model'], r['seed']) for r in existing_records)
        print(f"Loaded {len(existing_records)} seeds 0-9 records from Pass E")

    records = list(existing_records)

    for dname in HIGH_D_DATASETS:
        X, y, _ = load_dataset(dname)
        N, D = X.shape
        K = len(np.unique(y))

        n_top = max(2, int(np.ceil(0.15 * D)))
        var_indices = np.argsort(X.var(axis=0))[-n_top:]
        X_var = X[:, var_indices]

        n_comp = min(N - 1, D, 50)
        svd = TruncatedSVD(n_components=n_comp, random_state=42)
        X_pca = svd.fit_transform(X)

        lap_scores = compute_laplacian_score(X)
        lap_indices = np.argsort(lap_scores)[:n_top]
        X_lap = X[:, lap_indices]

        for seed in range(10, 30):
            # K-Means All
            if (dname, "K-Means_All", seed) not in done_keys:
                pred_km_all = KMeans(n_clusters=K, n_init=10, random_state=seed).fit_predict(X)
                records.append({"dataset": dname, "model": "K-Means_All", "seed": seed, "ari": adjusted_rand_score(y, pred_km_all)})

            # K-Means VarFilt
            if (dname, "K-Means_VarFilt", seed) not in done_keys:
                pred_km_var = KMeans(n_clusters=K, n_init=10, random_state=seed).fit_predict(X_var)
                records.append({"dataset": dname, "model": "K-Means_VarFilt", "seed": seed, "ari": adjusted_rand_score(y, pred_km_var)})

            # K-Means PCA
            if (dname, "K-Means_PCA", seed) not in done_keys:
                pred_km_pca = KMeans(n_clusters=K, n_init=10, random_state=seed).fit_predict(X_pca)
                records.append({"dataset": dname, "model": "K-Means_PCA", "seed": seed, "ari": adjusted_rand_score(y, pred_km_pca)})

            # K-Means LapScore
            if (dname, "K-Means_LapScore", seed) not in done_keys:
                pred_km_lap = KMeans(n_clusters=K, n_init=10, random_state=seed).fit_predict(X_lap)
                records.append({"dataset": dname, "model": "K-Means_LapScore", "seed": seed, "ari": adjusted_rand_score(y, pred_km_lap)})

            # Sparse K-Means
            if (dname, "SparseKMeans", seed) not in done_keys:
                pred_sparse_km = run_sparse_kmeans(X, K, random_state=seed)
                records.append({"dataset": dname, "model": "SparseKMeans", "seed": seed, "ari": adjusted_rand_score(y, pred_sparse_km)})

            # StdCons All
            if (dname, "StdCons_All", seed) not in done_keys:
                pred_std_all, _, _ = run_standard_consensus(X, K, n_base_models=25, seed=seed)
                records.append({"dataset": dname, "model": "StdCons_All", "seed": seed, "ari": adjusted_rand_score(y, pred_std_all)})

            # StdCons VarFilt
            if (dname, "StdCons_VarFilt", seed) not in done_keys:
                pred_std_var, _, _ = run_standard_consensus(X_var, K, n_base_models=25, seed=seed)
                records.append({"dataset": dname, "model": "StdCons_VarFilt", "seed": seed, "ari": adjusted_rand_score(y, pred_std_var)})

            # StdCons PCA
            if (dname, "StdCons_PCA", seed) not in done_keys:
                pred_std_pca, _, _ = run_standard_consensus(X_pca, K, n_base_models=25, seed=seed)
                records.append({"dataset": dname, "model": "StdCons_PCA", "seed": seed, "ari": adjusted_rand_score(y, pred_std_pca)})

            # ICC-v2
            if (dname, "ICC_v2", seed) not in done_keys:
                icc = InvariantCoreConsensusV2(n_clusters=K, random_state=seed)
                pred_icc = icc.fit_predict(X)
                records.append({"dataset": dname, "model": "ICC_v2", "seed": seed, "ari": adjusted_rand_score(y, pred_icc)})

        pd.DataFrame(records).to_csv(out_file, index=False)
        print(f"Processed {dname.upper()}: total records {len(records)}")

    df = pd.DataFrame(records)
    df.to_csv(out_file, index=False)
    print(f"\n[OK] Saved {len(df)} records to {out_file} (Expected: {6 * 9 * 30} = 1620)")

    # Compute Table 5 summary
    grouped = df.groupby(["model", "dataset"])["ari"].mean().unstack()
    print("\nTable 5 Mean ARI per model per dataset (30 seeds):")
    print(grouped.round(3).to_string())

    mean_per_model = grouped.mean(axis=1)
    med_per_model = df.groupby("model")["ari"].median()
    print("\nOverall High-D Subgroup Mean & Median ARI (30 seeds):")
    for m in grouped.index:
        print(f"{m:20s} | Mean: {mean_per_model[m]:.3f} | Median: {med_per_model[m]:.3f}")

    with open(OUT_DIR / "fair_baselines_summary_passF.json", "w", encoding="utf-8") as fp:
        json.dump({
            "means": mean_per_model.to_dict(),
            "medians": med_per_model.to_dict()
        }, fp, indent=2)

if __name__ == "__main__":
    main()
