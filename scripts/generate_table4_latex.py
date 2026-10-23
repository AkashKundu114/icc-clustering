"""
Generate LaTeX tables for Table 4, Table 5, and Table 2 directly from Pass F data stores.
"""

import pandas as pd
import numpy as np

# Table 4
sum_df = pd.read_csv("results/passF/benchmark_matrix_summary_passF.csv")
piv_mean = sum_df.pivot(index="dataset", columns="model", values="mean")
piv_std = sum_df.pivot(index="dataset", columns="model", values="std")

MODELS = [
    "K-Means", "Ward", "Spectral", "FCM", "Standard_Consensus",
    "Core_Halo_Consensus", "DEC", "FCAG", "FastMVC", "ICC_v1", "ICC_v2"
]

ds_meta = {
    "cns": r"CNS ($60, 7.1\text{k}, 2$)$^\dagger$",
    "colon": r"Colon ($62, 2.0\text{k}, 2$)$^\dagger$",
    "indian_pines": r"Indian Pines ($10.2\text{k}, 200, 16$)",
    "isolet": r"Isolet ($7.8\text{k}, 617, 26$)",
    "leukemia": r"Leukemia ($72, 7.1\text{k}, 2$)$^\dagger$",
    "madelon": r"Madelon ($500, 500, 2$)",
    "newsgroups20": r"20 Newsgroups ($18.8\text{k}, 10\text{k}, 20$)",
    "ovarian": r"Ovarian ($253, 15.1\text{k}, 2$)$^\dagger$",
    "prostate": r"Prostate ($102, 12.6\text{k}, 2$)$^\dagger$",
    "sonar": r"Sonar ($208, 60, 2$)",
    "srbct": r"SRBCT ($83, 2.3\text{k}, 4$)$^\dagger$",
    "yale_b": r"Yale B ($2.4\text{k}, 1.0\text{k}, 38$)",
    "zheng68k": r"PBMC68k-reduced ($700, 765, 10$)$^*$"
}

print("--- PART I ROWS ---")
for dname in ["cns", "colon", "indian_pines", "isolet", "leukemia", "madelon", "newsgroups20", "ovarian", "prostate", "sonar", "srbct", "yale_b", "zheng68k"]:
    label = ds_meta[dname]
    vals = []
    # Find max mean across all 11 models for this dataset
    all_means = [piv_mean.loc[dname, m] for m in MODELS]
    max_m = max(all_means)

    for m in ["K-Means", "Ward", "Spectral", "FCM"]:
        mu = piv_mean.loc[dname, m]
        sd = piv_std.loc[dname, m]
        sign = "+" if mu >= 0 else ""
        s = f"{sign}{mu:.3f} \\pm {sd:.3f}"
        if abs(mu - max_m) < 1e-5 and mu > 0:
            s = f"\\mathbf{{{s}}}"
        vals.append(f"${s}$")
    print(f"{label} & {' & '.join(vals)} \\\\")

print("\n--- PART II ROWS ---")
for dname in ["cns", "colon", "indian_pines", "isolet", "leukemia", "madelon", "newsgroups20", "ovarian", "prostate", "sonar", "srbct", "yale_b", "zheng68k"]:
    label = ds_meta[dname]
    vals = []
    all_means = [piv_mean.loc[dname, m] for m in MODELS]
    max_m = max(all_means)

    for m in ["Standard_Consensus", "Core_Halo_Consensus", "DEC", "FCAG"]:
        mu = piv_mean.loc[dname, m]
        sd = piv_std.loc[dname, m]
        sign = "+" if mu >= 0 else ""
        s = f"{sign}{mu:.3f} \\pm {sd:.3f}"
        if abs(mu - max_m) < 1e-5 and mu > 0:
            s = f"\\mathbf{{{s}}}"
        vals.append(f"${s}$")
    print(f"{label} & {' & '.join(vals)} \\\\")

print("\n--- PART III ROWS ---")
for dname in ["cns", "colon", "indian_pines", "isolet", "leukemia", "madelon", "newsgroups20", "ovarian", "prostate", "sonar", "srbct", "yale_b", "zheng68k"]:
    label = ds_meta[dname]
    vals = []
    all_means = [piv_mean.loc[dname, m] for m in MODELS]
    max_m = max(all_means)

    for m in ["FastMVC", "ICC_v1", "ICC_v2"]:
        mu = piv_mean.loc[dname, m]
        sd = piv_std.loc[dname, m]
        sign = "+" if mu >= 0 else ""
        s = f"{sign}{mu:.3f} \\pm {sd:.3f}"
        if abs(mu - max_m) < 1e-5 and mu > 0:
            s = f"\\mathbf{{{s}}}"
        vals.append(f"${s}$")
    print(f"{label} & {' & '.join(vals)} \\\\")
