import os
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, wilcoxon

def holm_bonferroni(p_vals):
    m = len(p_vals)
    sorted_indices = np.argsort(p_vals)
    adj_p = np.zeros(m)
    cum_max = 0.0
    for rank_idx, orig_idx in enumerate(sorted_indices):
        multiplier = m - rank_idx
        raw_adj = p_vals[orig_idx] * multiplier
        cum_max = max(cum_max, raw_adj)
        adj_p[orig_idx] = min(1.0, cum_max)
    return adj_p

def main():
    p_res = Path("results/results.json")
    with open(p_res, "r", encoding="utf-8") as f:
        recs = json.load(f)

    exp3_recs = [r for r in recs if r["experiment"] == "exp3_1" and r["metric_name"] == "ari"]
    df = pd.DataFrame(exp3_recs)

    piv = df.groupby(["dataset", "method"])["metric_value"].mean().unstack()

    models = piv.columns.tolist()
    datasets = piv.index.tolist()

    f_stat, f_p = friedmanchisquare(*[piv[m].values for m in models])

    ranks_df = piv.rank(axis=1, ascending=False)
    mean_ranks = ranks_df.mean(axis=0).to_dict()

    wilc_results = {}
    p_vals_raw = []
    comp_models = [m for m in models if m != "ICC_v2"]

    for m in comp_models:
        diffs = piv["ICC_v2"].values - piv[m].values
        if np.all(diffs == 0):
            stat, p = 0.0, 1.0
        else:
            stat, p = wilcoxon(piv["ICC_v2"].values, piv[m].values, zero_method="wilcox")
        p_vals_raw.append(p)
        wilc_results[m] = {"statistic": float(stat), "raw_p": float(p)}

    adj_p_vals = holm_bonferroni(p_vals_raw)
    for idx, m in enumerate(comp_models):
        wilc_results[m]["holm_adj_p"] = float(adj_p_vals[idx])
        wilc_results[m]["significant_alpha_05"] = bool(adj_p_vals[idx] < 0.05)

    high_d_datasets = ["prostate", "cns", "leukemia", "ovarian", "colon", "srbct"]
    low_d_datasets = [d for d in datasets if d not in high_d_datasets]

    ranks_high_d = ranks_df.loc[high_d_datasets].mean(axis=0).to_dict()
    ranks_low_d = ranks_df.loc[low_d_datasets].mean(axis=0).to_dict()

    wilc_high_d = {}
    p_high_raw = []
    for m in comp_models:
        diffs = piv.loc[high_d_datasets, "ICC_v2"].values - piv.loc[high_d_datasets, m].values
        if np.all(diffs == 0):
            stat, p = 0.0, 1.0
        else:
            stat, p = wilcoxon(piv.loc[high_d_datasets, "ICC_v2"].values, piv.loc[high_d_datasets, m].values, zero_method="wilcox")
        p_high_raw.append(p)
        wilc_high_d[m] = {"statistic": float(stat), "raw_p": float(p)}

    adj_p_high = holm_bonferroni(p_high_raw)
    for idx, m in enumerate(comp_models):
        wilc_high_d[m]["holm_adj_p"] = float(adj_p_high[idx])
        wilc_high_d[m]["significant_alpha_05"] = bool(adj_p_high[idx] < 0.05)

    k = len(models)
    n = len(datasets)
    q_alpha_05 = 3.219
    cd_val = q_alpha_05 * np.sqrt((k * (k + 1.0)) / (6.0 * n))

    stats_output = {
        "omnibus_test": {
            "test_name": "Friedman Chi-Square",
            "k_models": k,
            "n_datasets": n,
            "statistic": float(f_stat),
            "p_value": float(f_p),
            "is_significant": bool(f_p < 0.05)
        },
        "critical_difference": {
            "formula": "q_alpha * sqrt(k*(k+1)/(6*N))",
            "k": k,
            "N": n,
            "q_alpha_05": float(q_alpha_05),
            "critical_difference_alpha_05": float(cd_val),
            "published_claim_erroneous_cd": 2.62,
            "correction_note": "Published CD=2.62 corresponded to k=9, N=21. Correct CD for k=11, N=13 is 4.21."
        },
        "overall_mean_ranks": mean_ranks,
        "pairwise_wilcoxon_vs_iccv2": wilc_results,
        "subgroup_high_d_over_20": {
            "datasets": high_d_datasets,
            "mean_ranks": ranks_high_d,
            "pairwise_wilcoxon": wilc_high_d
        },
        "subgroup_low_d_under_20": {
            "datasets": low_d_datasets,
            "mean_ranks": ranks_low_d
        }
    }

    p_fair = Path("results/phase2/fair_baselines.csv")
    if p_fair.exists():
        df_fair = pd.read_csv(p_fair)
        fair_piv = df_fair.groupby(["dataset", "model"])["ari"].mean().unstack()
        fair_models = fair_piv.columns.tolist()
        fair_ranks = fair_piv.rank(axis=1, ascending=False).mean(axis=0).to_dict()
        stats_output["fair_baselines_analysis"] = {
            "mean_ari": fair_piv.mean(axis=0).to_dict(),
            "mean_ranks": fair_ranks,
            "high_d_mean_ari": fair_piv.loc[[d for d in high_d_datasets if d in fair_piv.index]].mean(axis=0).to_dict()
        }

    out_p = Path("results/phase2/stats.json")
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with open(out_p, "w", encoding="utf-8") as f:
        json.dump(stats_output, f, indent=2)

    print(f"Computed statistical analysis. Wrote {out_p}")
    print(f"Friedman chi2={f_stat:.4f}, p={f_p:.4f}")
    print(f"Nemenyi CD (k={k}, N={n}) = {cd_val:.4f}")

if __name__ == "__main__":
    main()
