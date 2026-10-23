"""
Compute ranks, Friedman, Nemenyi, and Grand Means for:
1. High-D subgroup (6 datasets, 30 seeds) across all 11 models
2. Full 13-dataset omnibus (6 high-D with 30 seeds, 7 standard benchmarks with 10 seeds)
3. 12-dataset omnibus (excluding PBMC68k-reduced)
"""

import json
import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, wilcoxon
from pathlib import Path

OUT_DIR = Path("results/passF")

HIGH_D_DATASETS = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]
STANDARD_DATASETS = ["indian_pines", "isolet", "madelon", "newsgroups20", "sonar", "yale_b", "zheng68k"]
ALL_DATASETS = sorted(HIGH_D_DATASETS + STANDARD_DATASETS)

MODELS = [
    "K-Means", "Ward", "Spectral", "FCM", "Standard_Consensus",
    "Core_Halo_Consensus", "DEC", "FCAG", "FastMVC", "ICC_v1", "ICC_v2"
]

def main():
    df_hd_30 = pd.read_csv(OUT_DIR / "high_d_30seeds_all_models.csv")
    df_passE = pd.read_csv("results/passE/benchmark_matrix_seeds0_9.csv")
    df_std_10 = df_passE[df_passE["dataset"].isin(STANDARD_DATASETS)].copy()

    # Combine into unified matrix
    cols = ["dataset", "N", "D", "K", "model", "seed", "ari", "nmi", "elapsed_sec"]
    df_unified = pd.concat([df_hd_30[cols], df_std_10[cols]], ignore_index=True)
    unified_csv = OUT_DIR / "benchmark_matrix_passF.csv"
    df_unified.to_csv(unified_csv, index=False)
    print(f"Saved unified benchmark matrix ({len(df_unified)} records) to {unified_csv}")

    # Compute mean ARI per dataset-model
    grouped = df_unified.groupby(["dataset", "model"])["ari"].agg(["mean", "std", "median", "count"]).reset_index()
    grouped.to_csv(OUT_DIR / "benchmark_matrix_summary_passF.csv", index=False)

    # Pivot table of mean ARI
    pivot_mean = grouped.pivot(index="dataset", columns="model", values="mean")[MODELS]
    pivot_std = grouped.pivot(index="dataset", columns="model", values="std")[MODELS]
    pivot_med = grouped.pivot(index="dataset", columns="model", values="median")[MODELS]

    print("\n" + "="*80)
    print("TABLE 4: MEAN ARI MATRIX (PASS F)")
    print("="*80)
    print(pivot_mean.round(3).to_string())

    # Compute ranks per dataset (higher ARI = better rank = 1)
    ranks_df = pivot_mean.rank(axis=1, ascending=False, method="average")

    print("\n" + "="*80)
    print("RANKS PER DATASET")
    print("="*80)
    print(ranks_df.round(2).to_string())

    # High-D Subgroup stats (6 datasets)
    hd_ranks = ranks_df.loc[HIGH_D_DATASETS].mean(axis=0)
    hd_mean_ari = pivot_mean.loc[HIGH_D_DATASETS].mean(axis=0)
    hd_med_ari = pivot_med.loc[HIGH_D_DATASETS].median(axis=0)

    print("\n" + "="*80)
    print("HIGH-D SUBGROUP METRICS (6 DATASETS, 30 SEEDS)")
    print("="*80)
    for m in MODELS:
        print(f"{m:22s} | Mean Rank: {hd_ranks[m]:.2f} | Subgroup Mean ARI: {hd_mean_ari[m]:.3f} | Subgroup Med ARI: {hd_med_ari[m]:.3f}")

    # Omnibus stats (All 13 datasets)
    omni_ranks = ranks_df.mean(axis=0)
    omni_mean_ari = pivot_mean.mean(axis=0)
    omni_med_ari = pivot_med.median(axis=0)

    print("\n" + "="*80)
    print("OMNIBUS METRICS (ALL 13 DATASETS)")
    print("="*80)
    for m in MODELS:
        print(f"{m:22s} | Mean Rank: {omni_ranks[m]:.2f} | Grand Mean ARI: {omni_mean_ari[m]:.3f} | Grand Med ARI: {omni_med_ari[m]:.3f}")

    # 12 Datasets (Excluding PBMC / zheng68k)
    ds_12 = [d for d in ALL_DATASETS if d != "zheng68k"]
    ranks_12 = pivot_mean.loc[ds_12].rank(axis=1, ascending=False, method="average").mean(axis=0)

    # Friedman tests
    # 13 datasets
    mat_13 = pivot_mean.values  # shape (13, 11)
    k = 11
    N_13 = 13
    stat_13, p_13 = friedmanchisquare(*[mat_13[:, j] for j in range(k)])
    cd_13 = 3.219 * np.sqrt((k * (k + 1)) / (6.0 * N_13))

    # 12 datasets
    mat_12 = pivot_mean.loc[ds_12].values
    N_12 = 12
    stat_12, p_12 = friedmanchisquare(*[mat_12[:, j] for j in range(k)])
    cd_12 = 3.219 * np.sqrt((k * (k + 1)) / (6.0 * N_12))

    # 6 High-D datasets
    mat_6 = pivot_mean.loc[HIGH_D_DATASETS].values
    N_6 = 6
    stat_6, p_6 = friedmanchisquare(*[mat_6[:, j] for j in range(k)])
    cd_6 = 3.219 * np.sqrt((k * (k + 1)) / (6.0 * N_6))

    stats_dict = {
        "N13": {
            "friedman_stat": float(stat_13), "friedman_p": float(p_13), "nemenyi_cd": float(cd_13),
            "ranks": {m: float(omni_ranks[m]) for m in MODELS},
            "grand_mean": {m: float(omni_mean_ari[m]) for m in MODELS},
            "grand_median": {m: float(omni_med_ari[m]) for m in MODELS}
        },
        "N12": {
            "friedman_stat": float(stat_12), "friedman_p": float(p_12), "nemenyi_cd": float(cd_12),
            "ranks": {m: float(ranks_12[m]) for m in MODELS}
        },
        "HighD_N6": {
            "friedman_stat": float(stat_6), "friedman_p": float(p_6), "nemenyi_cd": float(cd_6),
            "ranks": {m: float(hd_ranks[m]) for m in MODELS},
            "subgroup_mean": {m: float(hd_mean_ari[m]) for m in MODELS},
            "subgroup_median": {m: float(hd_med_ari[m]) for m in MODELS}
        }
    }

    with open(OUT_DIR / "friedman_nemenyi_passF.json", "w", encoding="utf-8") as fp:
        json.dump(stats_dict, fp, indent=2)

    print(f"\nSaved stats to {OUT_DIR / 'friedman_nemenyi_passF.json'}")
    print(f"\n13 Datasets: Friedman chi2 = {stat_13:.2f}, p = {p_13:.4f}, CD = {cd_13:.2f}")
    print(f"12 Datasets: Friedman chi2 = {stat_12:.2f}, p = {p_12:.4f}, CD = {cd_12:.2f}")
    print(f"6 High-D Datasets: Friedman chi2 = {stat_6:.2f}, p = {p_6:.4f}, CD = {cd_6:.2f}")

if __name__ == "__main__":
    main()
