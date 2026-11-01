# -*- coding: utf-8 -*-
"""
Exports Vargha-Delaney A12, Shapiro-Wilk/CV, and Component Contributions
to CSV files in results/passF/ to ensure full reproducibility and automatic
allowlist inclusion.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

passf_dir = Path("results/passF")

# 1. Vargha-Delaney A12 Table
def vargha_delaney_a12(x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    n1, n2 = len(x), len(y)
    more = sum((x[:, None] > y[None, :]).ravel())
    eq = sum((x[:, None] == y[None, :]).ravel())
    return (more + 0.5 * eq) / (n1 * n2)

df_all = pd.read_csv("results/passF/high_d_30seeds_all_models.csv")
models = [m for m in df_all["model"].unique() if m != "ICC_v2"]
datasets = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]

results = {}
for d in datasets:
    results[d] = {}
    x = df_all[(df_all["dataset"] == d) & (df_all["model"] == "ICC_v2")]["ari"].values
    for m in models:
        y = df_all[(df_all["dataset"] == d) & (df_all["model"] == m)]["ari"].values
        results[d][m] = vargha_delaney_a12(x, y)

vd_df = pd.DataFrame(results).T
vd_df.to_csv(passf_dir / "vargha_delaney_a12_passF.csv", index_label="dataset")
print(f"Exported {passf_dir / 'vargha_delaney_a12_passF.csv'}")

# 2. Shapiro-Wilk and CV Table
icc = df_all[df_all["model"] == "ICC_v2"]
sw_data = []
for d in datasets:
    vals = icc[icc["dataset"] == d]["ari"].values
    mean = vals.mean()
    std = vals.std(ddof=1)
    cv = std / abs(mean) if abs(mean) > 1e-6 else 0.0
    w, p = stats.shapiro(vals)
    gt_half = np.sum(vals > 0.5)
    sw_data.append({
        "dataset": d,
        "mean": mean,
        "std": std,
        "cv": cv,
        "shapiro_w": w,
        "p_value": p,
        "gt_half_count": int(gt_half),
        "gt_half_frac": float(gt_half / len(vals))
    })

sw_df = pd.DataFrame(sw_data)
sw_df.to_csv(passf_dir / "shapiro_wilk_cv_passF.csv", index=False)
print(f"Exported {passf_dir / 'shapiro_wilk_cv_passF.csv'}")

# 3. Component Contributions Table
df_abl = pd.read_csv("results/passF/ablation_30seeds_passF.csv")
piv = df_abl.pivot(index=["dataset", "seed"], columns="variant", values="ari")

var_mapping = {
    "Remove_BGSS": ("Full_ICC_v2", "Ambient_AnchorConsensus"),
    "Remove_Bipartite": ("Full_ICC_v2", "BGSS_StdConsensus"),
    "Remove_Ensembling": ("Full_ICC_v2", "BGSS_KMeans"),
    "Remove_Anchor_Cert": ("Full_ICC_v2", "BGSS_RandomAnchors"),
    "Remove_All": ("Full_ICC_v2", "Ambient_StdConsensus")
}

np.random.seed(42)
B = 10000
comp_rows = []
for name, (v_full, v_abl) in var_mapping.items():
    diff_per_dataset = []
    for d in datasets:
        sub = piv.loc[d]
        diff_per_dataset.append((sub[v_full] - sub[v_abl]).mean())
    diff_arr = np.array(diff_per_dataset)
    mean_diff = diff_arr.mean()
    
    boot_means = []
    for _ in range(B):
        idx = np.random.choice(len(datasets), size=len(datasets), replace=True)
        boot_means.append(diff_arr[idx].mean())
    ci_low, ci_high = np.percentile(boot_means, [2.5, 97.5])
    comp_rows.append({
        "component": name,
        "mean_delta": mean_diff,
        "ci_low": ci_low,
        "ci_high": ci_high
    })

comp_df = pd.DataFrame(comp_rows)
comp_df.to_csv(passf_dir / "component_contributions_passF.csv", index=False)
print(f"Exported {passf_dir / 'component_contributions_passF.csv'}")
