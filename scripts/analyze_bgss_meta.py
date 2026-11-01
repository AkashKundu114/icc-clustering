import numpy as np
import pandas as pd
from scipy import stats

df = pd.read_csv("results/exp8c_feature_gating.csv")

print("=== 1. PER-COHORT BGSS VS MATCHED RANDOM GATING ===")
cohort_records = []
for cohort, group in df.groupby("dataset"):
    d = group["diff_bgss_minus_random"].values
    n = len(d)
    mean_d = float(np.mean(d))
    sd_d = float(np.std(d, ddof=1))
    se_d = sd_d / np.sqrt(n)
    
    # Paired t-test
    t_val, p_val = stats.ttest_1samp(d, 0.0)
    
    # 95% Confidence Interval
    ci_low = mean_d - 1.96 * se_d
    ci_high = mean_d + 1.96 * se_d
    
    # Hedges' g
    hedges_g = mean_d / sd_d if sd_d > 0 else 0.0
    
    cohort_records.append({
        "cohort": cohort,
        "n_seeds": n,
        "mean_diff": mean_d,
        "sd_diff": sd_d,
        "se_diff": se_d,
        "ci_95_low": ci_low,
        "ci_95_high": ci_high,
        "t_stat": t_val,
        "p_val": p_val,
        "hedges_g": hedges_g
    })

res_df = pd.DataFrame(cohort_records).sort_values("mean_diff", ascending=False)
print(res_df.to_string(index=False))

print("\n=== 2. LEAVE-ONE-COHORT-OUT (LOCO) AND SENSITIVITY ===")
all_cohorts = list(res_df["cohort"])
for c in all_cohorts:
    sub = res_df[res_df["cohort"] != c]
    print(f"Leave-{c:10s}-out: Mean Diff = +{sub['mean_diff'].mean():.4f}")

# Leave {Leukemia, SRBCT} out
sub_no_two = res_df[~res_df["cohort"].isin(["leukemia", "srbct"])]
mean_no_two = sub_no_two["mean_diff"].mean()
print(f"\nLeave-{{Leukemia, SRBCT}}-out (n=4): Mean Diff = +{mean_no_two:.4f}")

print("\n=== 3. DER-SIMONIAN LAIRD RANDOM-EFFECTS META-ANALYSIS ===")
# Effect sizes: y_i = mean_diff, v_i = se_diff^2
yi = res_df["mean_diff"].values
vi = res_df["se_diff"].values ** 2
k = len(yi)

# Fixed-effects weights
wi = 1.0 / vi
y_fe = np.sum(wi * yi) / np.sum(wi)

# Cochran's Q
Q = float(np.sum(wi * (yi - y_fe) ** 2))
df_q = k - 1
p_q = float(1.0 - stats.chi2.cdf(Q, df_q))

# DerSimonian-Laird tau^2
denom = np.sum(wi) - (np.sum(wi ** 2) / np.sum(wi))
tau2 = max(0.0, (Q - df_q) / denom)

# I^2 heterogeneity statistic
I2 = max(0.0, 100.0 * (Q - df_q) / max(Q, 1e-12))

# Random-effects weights
wi_re = 1.0 / (vi + tau2)
y_re = np.sum(wi_re * yi) / np.sum(wi_re)
se_re = 1.0 / np.sqrt(np.sum(wi_re))
z_re = y_re / se_re
p_re = float(2.0 * (1.0 - stats.norm.cdf(abs(z_re))))

print(f"Grand Fixed-Effects Mean:  +{y_fe:.4f}")
print(f"Grand Random-Effects Mean: +{y_re:.4f} (SE={se_re:.4f}), 95% CI: [{y_re - 1.96*se_re:.4f}, {y_re + 1.96*se_re:.4f}]")
print(f"z = {z_re:.3f}, p = {p_re:.4e}")
print(f"Cochran's Q = {Q:.2f} (df={df_q}), p(Q) = {p_q:.4e}")
print(f"Tau^2 = {tau2:.6f}, I^2 = {I2:.1f}%")

print("\n=== 4. META-ANALYSIS WITHOUT LEUKEMIA AND SRBCT ===")
yi_sub = sub_no_two["mean_diff"].values
vi_sub = sub_no_two["se_diff"].values ** 2
k_sub = len(yi_sub)

wi_sub = 1.0 / vi_sub
y_fe_sub = np.sum(wi_sub * yi_sub) / np.sum(wi_sub)
Q_sub = float(np.sum(wi_sub * (yi_sub - y_fe_sub) ** 2))
df_q_sub = k_sub - 1
p_q_sub = float(1.0 - stats.chi2.cdf(Q_sub, df_q_sub))
denom_sub = np.sum(wi_sub) - (np.sum(wi_sub ** 2) / np.sum(wi_sub))
tau2_sub = max(0.0, (Q_sub - df_q_sub) / denom_sub)
I2_sub = max(0.0, 100.0 * (Q_sub - df_q_sub) / max(Q_sub, 1e-12))

wi_re_sub = 1.0 / (vi_sub + tau2_sub)
y_re_sub = np.sum(wi_re_sub * yi_sub) / np.sum(wi_re_sub)
se_re_sub = 1.0 / np.sqrt(np.sum(wi_re_sub))
z_re_sub = y_re_sub / se_re_sub
p_re_sub = float(2.0 * (1.0 - stats.norm.cdf(abs(z_re_sub))))

print(f"Leave-2 Random-Effects Mean: +{y_re_sub:.4f} (SE={se_re_sub:.4f}), 95% CI: [{y_re_sub - 1.96*se_re_sub:.4f}, {y_re_sub + 1.96*se_re_sub:.4f}]")
print(f"z = {z_re_sub:.3f}, p = {p_re_sub:.4e}")
print(f"Cochran's Q = {Q_sub:.2f} (df={df_q_sub}), p(Q) = {p_q_sub:.4e}")
print(f"Tau^2 = {tau2_sub:.6f}, I^2 = {I2_sub:.1f}%")
