"""
Generate Table 5 LaTeX code directly from results/passF/fair_baselines_30seeds_passF.csv
"""

import pandas as pd
import numpy as np

df = pd.read_csv("results/passF/fair_baselines_30seeds_passF.csv")
piv_mean = df.groupby(["dataset", "model"])["ari"].mean().unstack()
piv_std = df.groupby(["dataset", "model"])["ari"].std().unstack()

MODELS = [
    "K-Means_All", "K-Means_VarFilt", "K-Means_PCA", "K-Means_LapScore", "SparseKMeans",
    "StdCons_All", "StdCons_VarFilt", "StdCons_PCA", "ICC_v2"
]

ds_meta = {
    "cns": r"CNS ($60, 7.1\text{k}, 2$)",
    "colon": r"Colon ($62, 2.0\text{k}, 2$)",
    "leukemia": r"Leukemia ($72, 7.1\text{k}, 2$)",
    "ovarian": r"Ovarian ($253, 15.1\text{k}, 2$)",
    "prostate": r"Prostate ($102, 12.6\text{k}, 2$)",
    "srbct": r"SRBCT ($83, 2.3\text{k}, 4$)"
}

max_models = {}
for d in ds_meta:
    max_models[d] = max([piv_mean.loc[d, m] for m in MODELS])

print("=== PART I ===")
p1_models = ["K-Means_All", "K-Means_VarFilt", "K-Means_PCA", "K-Means_LapScore", "SparseKMeans"]
for d in ds_meta:
    vals = []
    for m in p1_models:
        mu = piv_mean.loc[d, m]
        sd = piv_std.loc[d, m]
        sign = "+" if mu >= 0 else ""
        s = f"{sign}{mu:.3f} \\pm {sd:.3f}"
        if abs(mu - max_models[d]) < 1e-5 and mu > 0:
            s = f"\\mathbf{{{s}}}"
        vals.append(f"${s}$")
    print(f"{ds_meta[d]} & " + " & ".join(vals) + r" \\")

mean_p1 = [f"{piv_mean[m].mean():.3f}" for m in p1_models]
med_p1 = [f"{df[df['model']==m]['ari'].median():.3f}" for m in p1_models]
print(r"\textbf{Subgroup Mean ARI} & " + " & ".join(mean_p1) + r" \\")
print(r"\textbf{Subgroup Median ARI} & " + " & ".join(med_p1) + r" \\")

print("\n=== PART II ===")
p2_models = ["StdCons_All", "StdCons_VarFilt", "StdCons_PCA", "ICC_v2"]
for d in ds_meta:
    vals = []
    for m in p2_models:
        mu = piv_mean.loc[d, m]
        sd = piv_std.loc[d, m]
        sign = "+" if mu >= 0 else ""
        s = f"{sign}{mu:.3f} \\pm {sd:.3f}"
        if abs(mu - max_models[d]) < 1e-5 and mu > 0:
            s = f"\\mathbf{{{s}}}"
        vals.append(f"${s}$")
    print(f"{ds_meta[d]} & " + " & ".join(vals) + r" \\")

mean_p2 = [f"{piv_mean[m].mean():.3f}" for m in p2_models]
med_p2 = [f"{df[df['model']==m]['ari'].median():.3f}" for m in p2_models]
print(r"\textbf{Subgroup Mean ARI} & " + " & ".join(mean_p2) + r" \\")
print(r"\textbf{Subgroup Median ARI} & " + " & ".join(med_p2) + r" \\")
