"""
Experiment 0: Baseline Sweep across Noise Dimensions (D_noise in [0, 10000]).
Evaluates K-Means, GMM, Ward, Spectral, and FCM on N=300, K=3 balanced dataset.
Generates data for Figures 1, 2, and 3.
"""

import time
from pathlib import Path
import numpy as np
import pandas as pd
import sys

# Ensure project root is accessible
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from exp0_core import build_dataset, run_clusterer, pairwise_coassoc, adjusted_rand_score, CLUSTERERS
from icc.metrics import evaluate_all

M_RUNS = 20          # independent runs per (clusterer, condition)
K = 3
N_PER_CLUSTER = 100
NOISE_LEVELS = [0, 10, 50, 100, 500, 1000, 3000, 5000, 10000]


def run_baseline_sweep(output_dir=None):
    if output_dir is None:
        output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    pair_rows = []
    t0 = time.time()
    print("Starting Baseline Experiment 0 Sweep (D_noise in [0, 10000])...")

    for d_noise in NOISE_LEVELS:
        t_start = time.time()
        X, y = build_dataset(d_noise, noise_kind="gaussian", noise_seed=1,
                              n_per_cluster=N_PER_CLUSTER, k=K)
        truth_same = (y[:, None] == y[None, :])

        pooled_labelings = []
        for clus in CLUSTERERS:
            labelings = []
            for seed in range(M_RUNS):
                lab = run_clusterer(clus, X, K, seed)
                labelings.append(lab)
                metrics = evaluate_all(y, lab)
                rows.append(dict(
                    d_noise=d_noise, clusterer=clus, seed=seed,
                    ari=metrics["ari"],
                    nmi=metrics["nmi"],
                    ami=metrics["ami"],
                    v_measure=metrics["v_measure"],
                    fm_index=metrics["fm_index"]
                ))
            pooled_labelings.extend(labelings)

            # Per-algorithm ensemble stability = mean pairwise ARI between its own runs
            stab_vals = []
            for i in range(M_RUNS):
                for j in range(i + 1, M_RUNS):
                    stab_vals.append(adjusted_rand_score(labelings[i], labelings[j]))
            stability = float(np.mean(stab_vals)) if stab_vals else 1.0

            S = pairwise_coassoc(labelings)
            mu_within = float(S[truth_same & ~np.eye(len(y), dtype=bool)].mean())
            mu_between = float(S[~truth_same].mean())
            clus_rows = [r for r in rows if r["d_noise"] == d_noise and r["clusterer"] == clus]
            mean_ari = float(np.mean([r["ari"] for r in clus_rows]))
            mean_nmi = float(np.mean([r["nmi"] for r in clus_rows]))
            mean_ami = float(np.mean([r["ami"] for r in clus_rows]))
            mean_v_measure = float(np.mean([r["v_measure"] for r in clus_rows]))
            mean_fm_index = float(np.mean([r["fm_index"] for r in clus_rows]))

            pair_rows.append(dict(
                d_noise=d_noise, clusterer=clus, scope="per_algorithm",
                stability=stability, mean_ari=mean_ari, mean_nmi=mean_nmi,
                mean_ami=mean_ami, mean_v_measure=mean_v_measure, mean_fm_index=mean_fm_index,
                mu_within=mu_within, mu_between=mu_between,
                gap=stability - mean_ari,
            ))

        # Pooled cross-algorithm consensus
        S_pool = pairwise_coassoc(pooled_labelings)
        mu_within_pool = float(S_pool[truth_same & ~np.eye(len(y), dtype=bool)].mean())
        mu_between_pool = float(S_pool[~truth_same].mean())
        stab_vals_pool = []
        for i in range(len(pooled_labelings)):
            for j in range(i + 1, len(pooled_labelings)):
                stab_vals_pool.append(adjusted_rand_score(pooled_labelings[i], pooled_labelings[j]))
        stability_pool = float(np.mean(stab_vals_pool))
        d_rows = [r for r in rows if r["d_noise"] == d_noise]
        mean_ari_pool = float(np.mean([r["ari"] for r in d_rows]))
        mean_nmi_pool = float(np.mean([r["nmi"] for r in d_rows]))
        mean_ami_pool = float(np.mean([r["ami"] for r in d_rows]))
        mean_v_measure_pool = float(np.mean([r["v_measure"] for r in d_rows]))
        mean_fm_index_pool = float(np.mean([r["fm_index"] for r in d_rows]))

        pair_rows.append(dict(
            d_noise=d_noise, clusterer="ALL_POOLED", scope="pooled",
            stability=stability_pool, mean_ari=mean_ari_pool, mean_nmi=mean_nmi_pool,
            mean_ami=mean_ami_pool, mean_v_measure=mean_v_measure_pool, mean_fm_index=mean_fm_index_pool,
            mu_within=mu_within_pool, mu_between=mu_between_pool,
            gap=stability_pool - mean_ari_pool,
        ))

        print(f"  d_noise={d_noise:6d} done in {time.time()-t_start:.1f}s (Total: {time.time()-t0:.1f}s)")

    df_runs = pd.DataFrame(rows)
    df_agg = pd.DataFrame(pair_rows)

    df_runs.to_csv(output_dir / "exp0_runs.csv", index=False)
    df_agg.to_csv(output_dir / "exp0_agg.csv", index=False)
    print(f"\nSaved exp0_runs.csv and exp0_agg.csv to {output_dir}")
    return df_agg


if __name__ == "__main__":
    run_baseline_sweep()
