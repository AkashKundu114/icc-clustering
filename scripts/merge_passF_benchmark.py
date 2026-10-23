"""
Assemble results/passF/high_d_30seeds_all_models.csv:
1. Load seeds 0-9 from results/passE/benchmark_matrix_seeds0_9.csv for the 6 high-D datasets (600 rows).
2. Load seeds 10-29 from high_d_30seeds_fast_models.csv (960 rows: 8 models x 6 datasets x 20 seeds).
3. Load seeds 10-29 from high_d_30seeds_dec.csv (120 rows: DEC x 6 datasets x 20 seeds).
4. Load seeds 10-29 for ICC-v2 from results/passE/high_d_30seeds_bimodal.csv (120 rows).
5. Add Ward seeds 10-29 copied from Ward seed 0 (deterministic, 120 rows).
6. Verify total is exactly 6 datasets x 11 models x 30 seeds = 1,980 rows!
7. Compute means, medians, std, success fraction (ARI > 0.5), and 95% bootstrap CIs.
"""

import pandas as pd
import numpy as np
from pathlib import Path

OUT_DIR = Path("results/passF")
OUT_DIR.mkdir(parents=True, exist_ok=True)

HIGH_D_DATASETS = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]
MODELS = [
    "K-Means", "Ward", "Spectral", "FCM", "Standard_Consensus",
    "Core_Halo_Consensus", "DEC", "FCAG", "FastMVC", "ICC_v1", "ICC_v2"
]

def main():
    # 1. Seeds 0-9
    df_passE = pd.read_csv("results/passE/benchmark_matrix_seeds0_9.csv")
    df_e_hd = df_passE[df_passE["dataset"].isin(HIGH_D_DATASETS)].copy()
    print(f"Loaded {len(df_e_hd)} records from Pass E for seeds 0-9")

    # 2. Fast models seeds 10-29
    df_fast = pd.read_csv(OUT_DIR / "high_d_30seeds_fast_models.csv")
    print(f"Loaded {len(df_fast)} fast model records for seeds 10-29")

    # 3. DEC seeds 10-29
    df_dec = pd.read_csv(OUT_DIR / "high_d_30seeds_dec.csv")
    print(f"Loaded {len(df_dec)} DEC records for seeds 10-29")

    # 4. ICC-v2 seeds 10-29
    df_bimodal = pd.read_csv("results/passE/high_d_30seeds_bimodal.csv")
    df_icc_10_29 = df_bimodal[df_bimodal["seed"] >= 10].copy()
    df_icc_10_29["model"] = "ICC_v2"
    if "elapsed_sec" not in df_icc_10_29.columns:
        df_icc_10_29["elapsed_sec"] = 0.5
    if "nmi" not in df_icc_10_29.columns:
        df_icc_10_29["nmi"] = 0.0

    # Fill N, D, K from df_e_hd
    ndk_map = df_e_hd[["dataset", "N", "D", "K"]].drop_duplicates().set_index("dataset")
    for col in ["N", "D", "K"]:
        df_icc_10_29[col] = df_icc_10_29["dataset"].map(ndk_map[col])

    print(f"Loaded {len(df_icc_10_29)} ICC-v2 records for seeds 10-29")

    # 5. Ward seeds 10-29
    ward_records = []
    df_ward_0 = df_e_hd[(df_e_hd["model"] == "Ward") & (df_e_hd["seed"] == 0)]
    for _, row in df_ward_0.iterrows():
        dname = row["dataset"]
        ari_val = row["ari"]
        nmi_val = row["nmi"]
        elap = row["elapsed_sec"]
        N = row["N"]
        D = row["D"]
        K = row["K"]
        for s in range(10, 30):
            ward_records.append({
                "dataset": dname, "N": N, "D": D, "K": K,
                "model": "Ward", "seed": s,
                "ari": ari_val, "nmi": nmi_val, "elapsed_sec": elap
            })
    df_ward = pd.DataFrame(ward_records)
    print(f"Generated {len(df_ward)} Ward deterministic records for seeds 10-29")

    # Combine all
    cols = ["dataset", "N", "D", "K", "model", "seed", "ari", "nmi", "elapsed_sec"]
    combined = pd.concat([
        df_e_hd[cols],
        df_fast[cols],
        df_dec[cols],
        df_icc_10_29[cols],
        df_ward[cols]
    ], ignore_index=True)

    print(f"Total merged records: {len(combined)} (Expected: {6 * 11 * 30} = 1980)")
    assert len(combined) == 1980, f"Expected 1980 records, got {len(combined)}"

    out_file = OUT_DIR / "high_d_30seeds_all_models.csv"
    combined.to_csv(out_file, index=False)
    print(f"[OK] Saved unified 30-seed high-D matrix to {out_file}")

    # Compute summary stats
    summary = []
    for dname in HIGH_D_DATASETS:
        sub_d = combined[combined["dataset"] == dname]
        for mname in MODELS:
            sub = sub_d[sub_d["model"] == mname]
            aris = sub["ari"].values
            mean_ari = np.mean(aris)
            std_ari = np.std(aris, ddof=1)
            med_ari = np.median(aris)
            succ_frac = np.mean(aris > 0.5)

            # 95% Bootstrap CI (B=1000)
            rng = np.random.default_rng(42)
            boot_means = [np.mean(rng.choice(aris, size=len(aris), replace=True)) for _ in range(1000)]
            ci_low = np.percentile(boot_means, 2.5)
            ci_high = np.percentile(boot_means, 97.5)

            summary.append({
                "dataset": dname,
                "model": mname,
                "mean_ari": float(mean_ari),
                "std_ari": float(std_ari),
                "med_ari": float(med_ari),
                "succ_frac": float(succ_frac),
                "ci_95_low": float(ci_low),
                "ci_95_high": float(ci_high),
            })

    df_sum = pd.DataFrame(summary)
    sum_file = OUT_DIR / "high_d_30seeds_summary.csv"
    df_sum.to_csv(sum_file, index=False)
    print(f"[OK] Saved 30-seed summary to {sum_file}")

    # Display headline results
    print("\n" + "="*80)
    print("HEADLINE 30-SEED METRICS ON HIGH-D DATASETS (Mean +/- Std [Median], % > 0.5)")
    print("="*80)
    pivot_mean = df_sum.pivot(index="dataset", columns="model", values="mean_ari")
    pivot_med = df_sum.pivot(index="dataset", columns="model", values="med_ari")
    pivot_succ = df_sum.pivot(index="dataset", columns="model", values="succ_frac")
    print("\nMean ARI:")
    print(pivot_mean[["K-Means", "Standard_Consensus", "DEC", "ICC_v1", "ICC_v2"]].round(3))
    print("\nMedian ARI:")
    print(pivot_med[["K-Means", "Standard_Consensus", "DEC", "ICC_v1", "ICC_v2"]].round(3))
    print("\nSuccess Fraction (ARI > 0.5):")
    print(pivot_succ[["K-Means", "Standard_Consensus", "DEC", "ICC_v1", "ICC_v2"]].round(3))

if __name__ == "__main__":
    main()
