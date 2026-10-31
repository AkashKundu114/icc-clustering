import numpy as np
import pandas as pd
from scipy import stats
from bootstrap_utils import compute_cohort_bootstrap_ci

# Load passF canonical ablation data
df_passf = pd.read_csv('results/passF/ablation_30seeds_passF.csv')

# Per-dataset means for canonical variants
pvt = df_passf.groupby(['dataset', 'variant'])['ari'].mean().unstack()

# V5 (Full GAC) and V4 (BGSS + Random Anchors), V2 (BGSS + Dense), V0 (Ambient Dense), V3 (Ambient Bip)
v5 = pvt['Full_ICC_v2']
v4 = pvt['BGSS_RandomAnchors']
v2 = pvt['BGSS_StdConsensus']
v0 = pvt['Ambient_StdConsensus']
v3 = pvt['Ambient_AnchorConsensus']

# Random gating arms (from 30 seeds)
rand_bip_core = pd.Series({
    'cns': -0.0329, 'colon': -0.0059, 'leukemia': 0.2022,
    'ovarian': 0.0149, 'prostate': 0.0083, 'srbct': 0.0981
})

rand_bip_uniform = pd.Series({
    'cns': 0.0004, 'colon': -0.0130, 'leukemia': 0.1727,
    'ovarian': 0.0094, 'prostate': 0.0444, 'srbct': 0.1020
})

rand_dense = pd.Series({
    'cns': -0.0178, 'colon': -0.0062, 'leukemia': 0.1896,
    'ovarian': 0.0090, 'prostate': 0.0491, 'srbct': 0.0548
})

print("=================================================================")
print("RECONCILED TABLE ACROSS ALL ARMS (30 SEEDS, N=6 HIGH-D COHORTS)")
print("=================================================================")
table_all = pd.DataFrame({
    'V0 (Amb Dense)': v0,
    'V3 (Amb Bip)': v3,
    'Rand+Dense (Post hoc)': rand_dense,
    'Rand+Bip Core': rand_bip_core,
    'Rand+Bip Uniform': rand_bip_uniform,
    'V2 (BGSS Dense)': v2,
    'V4 (BGSS Uniform)': v4,
    'V5 (Full GAC)': v5
})
print(table_all.round(3))
print("-" * 65)
print("SUBGROUP MEANS:")
print(table_all.mean().round(3))

print("\n=================================================================")
print("STATISTICAL COMPARISONS (COHORT BOOTSTRAP CI & WILCOXON)")
print("=================================================================")

# 1. Full GAC (V5) vs Random Bipartite Gating
diff_v5_rand = v5 - rand_bip_core
mean_diff1, ci_low1, ci_high1 = compute_cohort_bootstrap_ci(diff_v5_rand.values)
w1, p1 = stats.wilcoxon(diff_v5_rand.values)
print(f"V5 vs Rand+Bip Core: Mean Diff = +{mean_diff1:.3f}, 95% CI: [{ci_low1:+.3f}, {ci_high1:+.3f}], Wilcoxon W={w1}, p={p1:.4f}")

# 2. V4 (BGSS Uniform) vs Rand Bip Uniform
diff_v4_rand = v4 - rand_bip_uniform
mean_diff2, ci_low2, ci_high2 = compute_cohort_bootstrap_ci(diff_v4_rand.values)
w2, p2 = stats.wilcoxon(diff_v4_rand.values)
print(f"V4 vs Rand+Bip Uniform: Mean Diff = +{mean_diff2:.3f}, 95% CI: [{ci_low2:+.3f}, {ci_high2:+.3f}], Wilcoxon W={w2}, p={p2:.4f}")

# 3. V2 (BGSS Dense) vs Rand Dense
diff_v2_rand = v2 - rand_dense
mean_diff3, ci_low3, ci_high3 = compute_cohort_bootstrap_ci(diff_v2_rand.values)
w3, p3 = stats.wilcoxon(diff_v2_rand.values)
print(f"V2 vs Rand+Dense: Mean Diff = +{mean_diff3:.3f}, 95% CI: [{ci_low3:+.3f}, {ci_high3:+.3f}], Wilcoxon W={w3}, p={p3:.4f}")

# 4. V5 vs V2 (Interaction of Bipartite Graph with BGSS)
diff_v5_v2 = v5 - v2
mean_diff4, ci_low4, ci_high4 = compute_cohort_bootstrap_ci(diff_v5_v2.values)
w4, p4 = stats.wilcoxon(diff_v5_v2.values)
print(f"V5 vs V2 (Interaction): Mean Diff = +{mean_diff4:.3f}, 95% CI: [{ci_low4:+.3f}, {ci_high4:+.3f}], Wilcoxon W={w4}, p={p4:.4f}")
print("Per-cohort V5 - V2 diffs:")
for d, val in diff_v5_v2.items():
    print(f"  {d:10s}: {val:+.3f}")

# 5. V5 vs V4 (Core Anchors vs Uniform Anchors)
diff_v5_v4 = v5 - v4
mean_diff5, ci_low5, ci_high5 = compute_cohort_bootstrap_ci(diff_v5_v4.values)
w5, p5 = stats.wilcoxon(diff_v5_v4.values)
print(f"V5 vs V4 (Core vs Uniform): Mean Diff = +{mean_diff5:.3f}, 95% CI: [{ci_low5:+.3f}, {ci_high5:+.3f}], Wilcoxon W={w5}, p={p5:.4f}")
