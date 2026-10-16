"""
Experiment 0: Genomics-Scale Imbalanced Regime (N=72, K=2, 47 ALL vs 25 AML).
Sweeps D_noise up to 20,000 (D/N ratio up to ~278).
Generates data for Figures 5, 6, and 7.
"""

import time
from pathlib import Path
import numpy as np
import pandas as pd
from exp0_core import build_dataset, run_clusterer, pairwise_coassoc, adjusted_rand_score, CLUSTERERS

M_RUNS = 15
SIZES = [47, 25]          # mirrors ALLAML: 47 ALL vs 25 AML, N=72 total
K = len(SIZES)
NOISE_LEVELS = [0, 100, 500, 1000, 3000, 5000, 10000, 20000]   # D/N ratio up to ~278


def run_scaled_sweep(output_dir=None):
    if output_dir is None:
        output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows, pair_rows = [], []
    t0 = time.time()
    print(f"Starting Genomics-Scale Sweep (N={sum(SIZES)}, K={K}, D_noise up to 20,000)...")

    for d_noise in NOISE_LEVELS:
        t_start = time.time()
        X, y = build_dataset(d_noise, noise_kind="gaussian", noise_seed=1, k=K, sizes=SIZES)
        truth_same = (y[:, None] == y[None, :])

        pooled_labelings = []
        for clus in CLUSTERERS:
            labelings = []
            for seed in range(M_RUNS):
                lab = run_clusterer(clus, X, K, seed)
                labelings.append(lab)
                ari = adjusted_rand_score(y, lab)
                rows.append(dict(d_noise=d_noise, clusterer=clus, seed=seed, ari=ari))
            pooled_labelings.extend(labelings)

            stab_vals = [adjusted_rand_score(labelings[i], labelings[j])
                         for i in range(M_RUNS) for j in range(i + 1, M_RUNS)]
            stability = float(np.mean(stab_vals)) if stab_vals else 1.0
            S = pairwise_coassoc(labelings)
            mu_within = float(S[truth_same & ~np.eye(len(y), dtype=bool)].mean())
            mu_between = float(S[~truth_same].mean())
            mean_ari = float(np.mean([r["ari"] for r in rows
                                       if r["d_noise"] == d_noise and r["clusterer"] == clus]))
            pair_rows.append(dict(d_noise=d_noise, clusterer=clus, scope="per_algorithm",
                                   stability=stability, mean_ari=mean_ari,
                                   mu_within=mu_within, mu_between=mu_between,
                                   gap=stability - mean_ari))

        S_pool = pairwise_coassoc(pooled_labelings)
        mu_within_pool = float(S_pool[truth_same & ~np.eye(len(y), dtype=bool)].mean())
        mu_between_pool = float(S_pool[~truth_same].mean())
        stab_vals_pool = [adjusted_rand_score(pooled_labelings[i], pooled_labelings[j])
                           for i in range(len(pooled_labelings)) for j in range(i + 1, len(pooled_labelings))]
        stability_pool = float(np.mean(stab_vals_pool))
        mean_ari_pool = float(np.mean([r["ari"] for r in rows if r["d_noise"] == d_noise]))
        pair_rows.append(dict(d_noise=d_noise, clusterer="ALL_POOLED", scope="pooled",
                               stability=stability_pool, mean_ari=mean_ari_pool,
                               mu_within=mu_within_pool, mu_between=mu_between_pool,
                               gap=stability_pool - mean_ari_pool))

        print(f"  d_noise={d_noise:6d} done in {time.time()-t_start:.1f}s (Total: {time.time()-t0:.1f}s)")

    pd.DataFrame(rows).to_csv(output_dir / "exp0_scaled_runs.csv", index=False)
    pd.DataFrame(pair_rows).to_csv(output_dir / "exp0_scaled_agg.csv", index=False)
    print(f"\nSaved exp0_scaled_runs.csv and exp0_scaled_agg.csv to {output_dir}")
    return pd.DataFrame(pair_rows)


if __name__ == "__main__":
    run_scaled_sweep()
