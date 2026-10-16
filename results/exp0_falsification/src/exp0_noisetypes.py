"""
Experiment 0: Robustness across 5 noise distributions at fixed D_noise = 1000.
Generates data for Figure 4 (Stability-ARI gap heatmap).
"""

import time
import os
from pathlib import Path
import numpy as np
import pandas as pd
from exp0_core import build_dataset, run_clusterer, pairwise_coassoc, adjusted_rand_score, CLUSTERERS

M_RUNS = 20
K = 3
N_PER_CLUSTER = 100
D_NOISE_FIXED = 1000
NOISE_KINDS = ["gaussian", "student_t", "correlated", "scaled", "sparse"]

def run_noisetypes_experiment(output_csv=None):
    if output_csv is None:
        data_dir = Path(__file__).resolve().parent.parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        output_csv = data_dir / "exp0_noisetypes.csv"

    rows = []
    t0 = time.time()
    print(f"Running Noise Types sweep at D_noise={D_NOISE_FIXED} across {len(NOISE_KINDS)} distributions...")

    for kind in NOISE_KINDS:
        X, y = build_dataset(D_NOISE_FIXED, noise_kind=kind, noise_seed=1,
                              n_per_cluster=N_PER_CLUSTER, k=K)
        truth_same = (y[:, None] == y[None, :])

        for clus in CLUSTERERS:
            labelings = []
            aris = []
            for seed in range(M_RUNS):
                lab = run_clusterer(clus, X, K, seed)
                labelings.append(lab)
                aris.append(adjusted_rand_score(y, lab))

            stab_vals = [adjusted_rand_score(labelings[i], labelings[j])
                         for i in range(M_RUNS) for j in range(i + 1, M_RUNS)]
            stability = float(np.mean(stab_vals))
            S = pairwise_coassoc(labelings)
            mu_within = S[truth_same & ~np.eye(len(y), dtype=bool)].mean()
            mu_between = S[~truth_same].mean()
            mean_ari = float(np.mean(aris))

            rows.append(dict(
                noise_kind=kind, clusterer=clus,
                mean_ari=mean_ari, stability=stability,
                mu_within=mu_within, mu_between=mu_between,
                gap=stability - mean_ari,
            ))
        print(f"  Noise kind '{kind}' completed in {time.time()-t0:.1f}s")

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)
    print(f"\nSaved results to {output_csv}")
    print(df.to_string(index=False))
    return df

if __name__ == "__main__":
    run_noisetypes_experiment()
