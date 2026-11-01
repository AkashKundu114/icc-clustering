"""
Direct Out-of-Sample Inductive Evaluation Script.

Evaluates out-of-sample inductive cluster assignment across 9 benchmark datasets:
- Direct Nystrom Subspace Projection (ICC-v2 Subspace)
- Full-Space Centroid Projection (ICC-v2 Full Centroid, Eq. 7)
- Pseudo-label Supervised NearestCentroid
- Pseudo-label Supervised RandomForest
- Direct Ambient K-Means Projection
across 10 stratified train/test splits (80% train, 20% test).

Usage:
    python scripts/run_inductive_direct.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.neighbors import NearestCentroid

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from icc.consensus_v2 import InvariantCoreConsensusV2  # noqa: E402

DATASETS = [
    "colon", "leukemia", "srbct", "cns", "lymphoma", "ovarian",
    "isolet", "har", "waveform"
]

SEEDS = [42, 101, 202, 303, 404, 505, 606, 707, 808, 909]

def main():
    out_dir = Path("results/phase2")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / "inductive_direct.csv"

    records = []

    for dname in DATASETS:
        p_npz = Path(f"experiments/exp3_real_world_benchmarks/data/cache/{dname}.npz")
        data = np.load(p_npz)
        X, y = data["X"].astype(np.float64), data["y"]
        N, D = X.shape
        K = len(np.unique(y))
        print(f"Inductive Direct Dataset {dname.upper()}: N={N}, D={D}, K={K}")

        for s_idx, seed in enumerate(SEEDS):
            try:
                sss = StratifiedShuffleSplit(n_splits=1, test_size=0.20, random_state=seed)
                train_idx, test_idx = next(sss.split(X, y))
            except ValueError:
                rng = np.random.default_rng(seed)
                perm = rng.permutation(N)
                split_pt = int(0.80 * N)
                train_idx, test_idx = perm[:split_pt], perm[split_pt:]

            X_tr = X[train_idx]
            X_te, y_te = X[test_idx], y[test_idx]

            icc = InvariantCoreConsensusV2(n_clusters=K, random_state=seed)
            y_tr_pred = icc.fit_predict(X_tr)

            pred_icc_sub = icc.predict(X_te, subspace=True)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "seed": seed, "method": "ICC_v2_NystromSubspace", "ari": adjusted_rand_score(y_te, pred_icc_sub), "nmi": normalized_mutual_info_score(y_te, pred_icc_sub)})

            pred_icc_full = icc.predict(X_te, subspace=False)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "seed": seed, "method": "ICC_v2_CentroidFull", "ari": adjusted_rand_score(y_te, pred_icc_full), "nmi": normalized_mutual_info_score(y_te, pred_icc_full)})

            nc = NearestCentroid()
            nc.fit(X_tr, y_tr_pred)
            pred_nc = nc.predict(X_te)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "seed": seed, "method": "ICC_v2_Pseudo_NearestCentroid", "ari": adjusted_rand_score(y_te, pred_nc), "nmi": normalized_mutual_info_score(y_te, pred_nc)})

            rf = RandomForestClassifier(n_estimators=30, random_state=seed)
            rf.fit(X_tr, y_tr_pred)
            pred_rf = rf.predict(X_te)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "seed": seed, "method": "ICC_v2_Pseudo_RandomForest", "ari": adjusted_rand_score(y_te, pred_rf), "nmi": normalized_mutual_info_score(y_te, pred_rf)})

            km = KMeans(n_clusters=K, n_init=5, random_state=seed)
            km.fit(X_tr)
            pred_km = km.predict(X_te)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "seed": seed, "method": "KMeans_Direct", "ari": adjusted_rand_score(y_te, pred_km), "nmi": normalized_mutual_info_score(y_te, pred_km)})

            n_comp = min(len(train_idx) - 1, D, 30)
            svd = TruncatedSVD(n_components=n_comp, random_state=seed)
            X_tr_pca = svd.fit_transform(X_tr)
            X_te_pca = svd.transform(X_te)
            km_pca = KMeans(n_clusters=K, n_init=5, random_state=seed)
            km_pca.fit(X_tr_pca)
            pred_km_pca = km_pca.predict(X_te_pca)
            records.append({"dataset": dname, "N": N, "D": D, "K": K, "seed": seed, "method": "PCA_KMeans_Direct", "ari": adjusted_rand_score(y_te, pred_km_pca), "nmi": normalized_mutual_info_score(y_te, pred_km_pca)})

    df = pd.DataFrame(records)
    df.to_csv(out_csv, index=False)
    print(f"Saved {len(df)} inductive direct records to {out_csv}")

if __name__ == "__main__":
    main()
