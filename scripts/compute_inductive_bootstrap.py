"""
Compute Table 2 paired differences with dataset-level bootstrap CIs:
- CentroidFull (Eq. 7) vs KMeans_Direct
- CentroidFull vs NystromSubspace
- CentroidFull vs Pseudo_RandomForest
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path

OUT_DIR = Path("results/passF")
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv("results/passE/inductive_direct_seeds0_9.csv")

# Pivot by dataset and seed
piv = df.pivot_table(index=["dataset", "seed"], columns="method", values="ari").reset_index()

# Compute paired differences per split
piv["diff_km"] = piv["ICC_v2_CentroidFull"] - piv["KMeans_Direct"]
piv["diff_nystrom"] = piv["ICC_v2_CentroidFull"] - piv["ICC_v2_NystromSubspace"]
piv["diff_rf"] = piv["ICC_v2_CentroidFull"] - piv["ICC_v2_Pseudo_RandomForest"]

# Per-dataset means
ds_means = piv.groupby("dataset")[["ICC_v2_CentroidFull", "KMeans_Direct", "ICC_v2_NystromSubspace", "ICC_v2_Pseudo_RandomForest", "diff_km", "diff_nystrom", "diff_rf"]].mean()
print("="*80)
print("TABLE 2 SUMMARY & PAIRED DIFFERENCES PER DATASET")
print("="*80)
print(ds_means.round(3).to_string())

# Dataset-level bootstrap (B=2000 resamples of datasets)
datasets = ds_means.index.values
rng = np.random.default_rng(42)

boot_diffs = {col: [] for col in ["diff_km", "diff_nystrom", "diff_rf"]}
for _ in range(2000):
    sampled_ds = rng.choice(datasets, size=len(datasets), replace=True)
    sample_mean = ds_means.loc[sampled_ds].mean()
    for col in boot_diffs:
        boot_diffs[col].append(sample_mean[col])

stats = {}
print("\n" + "="*80)
print("DATASET-LEVEL BOOTSTRAP 95% CONFIDENCE INTERVALS (B=2,000)")
print("="*80)
for col, name in [("diff_km", "Centroid vs Ambient K-Means"), ("diff_nystrom", "Centroid vs Nystrom Subspace"), ("diff_rf", "Centroid vs Random Forest")]:
    arr = np.array(boot_diffs[col])
    mean_val = float(ds_means[col].mean())
    ci_low = float(np.percentile(arr, 2.5))
    ci_high = float(np.percentile(arr, 97.5))
    stats[col] = {
        "comparison": name,
        "mean_diff": mean_val,
        "ci_95": [ci_low, ci_high]
    }
    print(f"{name:32s}: Mean Diff = {mean_val:+.4f}, 95% CI = [{ci_low:+.4f}, {ci_high:+.4f}]")

# Save outputs
with open(OUT_DIR / "inductive_bootstrap_stats.json", "w", encoding="utf-8") as fp:
    json.dump({
        "per_dataset": ds_means.to_dict(),
        "bootstrap_cis": stats
    }, fp, indent=2)

piv.to_csv(OUT_DIR / "inductive_paired_splits.csv", index=False)
print(f"\n[OK] Saved results to {OUT_DIR / 'inductive_bootstrap_stats.json'}")
