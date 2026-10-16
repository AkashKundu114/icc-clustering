"""
Experiment 0: Fine-Grid Sweep on FCM, KMeans, and GMM (D_noise in [500, 5000]).
Isolates the first-order phase transition of Fuzzy C-Means and dominant partition share.
Generates data for Figure 8.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from exp0_core import build_dataset, run_clusterer, pairwise_coassoc, adjusted_rand_score
from exp0_diagnose import canonical

M_RUNS = 30
K = 3
N_PER_CLUSTER = 100
GRID = [500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750,
        3000, 3500, 4000, 4500, 5000]
CLUSTERERS_FOCUS = ["fcm", "kmeans", "gmm"]


def run_finegrid_sweep(output_csv=None):
    if output_csv is None:
        data_dir = Path(__file__).resolve().parent.parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        output_csv = data_dir / "exp0_finegrid.csv"

    rows = []
    print(f"Starting Fine-Grid Sweep across {len(GRID)} noise levels (M={M_RUNS} seeds)...")

    for d_noise in GRID:
        X, y = build_dataset(d_noise, noise_kind="gaussian", noise_seed=1,
                              n_per_cluster=N_PER_CLUSTER, k=K)
        truth_same = (y[:, None] == y[None, :])
        for clus in CLUSTERERS_FOCUS:
            labelings, partitions, aris = [], [], []
            for seed in range(M_RUNS):
                lab = run_clusterer(clus, X, K, seed)
                labelings.append(lab)
                partitions.append(canonical(lab))
                aris.append(adjusted_rand_score(y, lab))

            stab_vals = [adjusted_rand_score(labelings[i], labelings[j])
                         for i in range(M_RUNS) for j in range(i + 1, M_RUNS)]
            stability = float(np.mean(stab_vals))
            mean_ari = float(np.mean(aris))

            S = pairwise_coassoc(labelings)
            mu_within = float(S[truth_same & ~np.eye(len(y), dtype=bool)].mean())
            mu_between = float(S[~truth_same].mean())

            distinct = list(dict.fromkeys(partitions))
            counts = {p: partitions.count(p) for p in distinct}
            dominant_share = max(counts.values()) / M_RUNS
            dominant_partition = max(counts, key=counts.get)
            dominant_ari = aris[partitions.index(dominant_partition)]

            rows.append(dict(
                d_noise=d_noise, clusterer=clus,
                mean_ari=mean_ari, stability=stability, gap=stability - mean_ari,
                mu_within=mu_within, mu_between=mu_between,
                n_distinct_partitions=len(distinct),
                dominant_partition_share=dominant_share,
                dominant_partition_ari=dominant_ari,
            ))
        print(f"  d_noise={d_noise} done")

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)
    print(f"\nSaved finegrid results to {output_csv}")
    return df


if __name__ == "__main__":
    run_finegrid_sweep()
