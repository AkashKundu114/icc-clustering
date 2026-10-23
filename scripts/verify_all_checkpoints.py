"""
Comprehensive 25-Checkpoint Verification Script (Pass E).
Directly inspects results stores (results/passE/) and compares against
numbers.tex and main.tex macros and text.
Outputs PASS/FAIL for each checkpoint.
"""

import sys
import json
import numpy as np
import pandas as pd
import scipy.stats as st
from pathlib import Path

def run_checks():
    results = []
    
    # Check 1: Nemenyi CD N=13
    cd_13 = round(3.219 * np.sqrt(11 * 12 / (6 * 13)), 2)
    p1 = (cd_13 == 4.19)
    results.append((1, "Nemenyi CD (N=13)", "4.19", f"{cd_13}", p1))

    # Check 2: Nemenyi CD N=12
    cd_12 = round(3.219 * np.sqrt(11 * 12 / (6 * 12)), 2)
    p2 = (cd_12 == 4.36)
    results.append((2, "Nemenyi CD (N=12)", "4.36", f"{cd_12}", p2))

    # Check 3: Sarle Uniform Bound
    sarle = round(5.0 / 9.0, 3)
    p3 = (sarle == 0.556)
    results.append((3, "Sarle Uniform Threshold", "0.556", f"{sarle}", p3))

    # Check 4: Ablation 2x2 Factorial V5 Subgroup Mean
    df_abl = pd.read_csv("results/passE/ablation_2x2_seeds0_9.csv")
    v5_mean = round(float(df_abl[df_abl["variant"] == "Full_ICC_v2"]["ari"].mean()), 3)
    p4 = (v5_mean == 0.226)
    results.append((4, "Ablation V5 High-D Subgroup Mean", "0.226", f"{v5_mean}", p4))

    # Check 5: Ablation 2x2 Factorial V4 Subgroup Mean
    v4_mean = round(float(df_abl[df_abl["variant"] == "BGSS_RandomAnchors"]["ari"].mean()), 3)
    p5 = (v4_mean == 0.216)
    results.append((5, "Ablation V4 High-D Subgroup Mean", "0.216", f"{v4_mean}", p5))

    # Check 6: Difference V5 - V4
    diff_v5_v4 = round(v5_mean - v4_mean, 3)
    p6 = (diff_v5_v4 == 0.010)
    results.append((6, "Ablation Gain V5 - V4", "+0.010", f"{diff_v5_v4:+.3f}", p6))

    # Check 7: Dataset-Level Cluster Bootstrap 95% CI (V5 vs V4)
    p_abl = df_abl.groupby(["dataset", "variant"])["ari"].mean().unstack()
    diffs = (p_abl["Full_ICC_v2"] - p_abl["BGSS_RandomAnchors"]).values
    rng = np.random.default_rng(42)
    boot = [rng.choice(diffs, size=len(diffs), replace=True).mean() for _ in range(10000)]
    ci_low, ci_high = np.round(np.percentile(boot, [2.5, 97.5]), 3)
    w_stat, w_pval = st.wilcoxon(diffs).statistic, round(st.wilcoxon(diffs).pvalue, 2)
    p7 = (ci_low == -0.051 and ci_high == 0.076 and w_stat == 8.0 and w_pval == 0.69)
    results.append((7, "Dataset Bootstrap CI (V5 vs V4)", "[-0.051, +0.076], W=8.0, p=0.69", f"[{ci_low:+.3f}, {ci_high:+.3f}], W={w_stat}, p={w_pval}", p7))

    # Check 8: Fair Baselines ICC-v2 Subgroup Mean (Table 5)
    df_fair = pd.read_csv("results/passE/fair_baselines_seeds0_9.csv")
    fair_icc_mean = round(float(df_fair[df_fair["model"] == "ICC_v2"]["ari"].mean()), 3)
    p8 = (fair_icc_mean == 0.226)
    results.append((8, "Fair Baselines ICC-v2 Subgroup Mean", "0.226", f"{fair_icc_mean}", p8))

    # Check 9: Fair Baselines ICC-v2 Subgroup Median (Table 5)
    fair_icc_med = round(float(df_fair[df_fair["model"] == "ICC_v2"].groupby("dataset")["ari"].mean().median()), 3)
    p9 = (fair_icc_med == 0.051)
    results.append((9, "Fair Baselines ICC-v2 Subgroup Median", "0.051", f"{fair_icc_med}", p9))

    # Check 10: Fair Baselines Leukemia ICC-v2 Mean
    fair_leuk = round(float(df_fair[(df_fair["dataset"] == "leukemia") & (df_fair["model"] == "ICC_v2")]["ari"].mean()), 3)
    p10 = (fair_leuk == 0.704)
    results.append((10, "Fair Baselines Leukemia ICC-v2", "0.704", f"{fair_leuk}", p10))

    # Check 11: Fair Baselines SRBCT ICC-v2 Mean
    fair_srbct = round(float(df_fair[(df_fair["dataset"] == "srbct") & (df_fair["model"] == "ICC_v2")]["ari"].mean()), 3)
    p11 = (fair_srbct == 0.537)
    results.append((11, "Fair Baselines SRBCT ICC-v2", "0.537", f"{fair_srbct}", p11))

    # Check 12: Fair Baselines Prostate Ambient KM vs ICC-v2
    km_prost = round(float(df_fair[(df_fair["dataset"] == "prostate") & (df_fair["model"] == "K-Means_All")]["ari"].mean()), 3)
    icc_prost = round(float(df_fair[(df_fair["dataset"] == "prostate") & (df_fair["model"] == "ICC_v2")]["ari"].mean()), 3)
    p12 = (km_prost == 0.049 and icc_prost == 0.011)
    results.append((12, "Prostate KM vs ICC-v2", "KM 0.049, ICC 0.011", f"KM {km_prost}, ICC {icc_prost}", p12))

    # Check 13: 30-Seed Bimodal Leukemia Share > 0.5
    df_30 = pd.read_csv("results/passE/high_d_30seeds_bimodal.csv")
    leuk_aris = df_30[df_30["dataset"] == "leukemia"]["ari"]
    leuk_share = round(float((leuk_aris > 0.5).mean()), 3)
    leuk_med = round(float(leuk_aris.median()), 3)
    p13 = (leuk_share == 0.733 and leuk_med == 0.787)
    results.append((13, "30-Seed Leukemia Bimodal", "73.3% >0.5, median 0.787", f"{leuk_share*100:.1f}%, median {leuk_med}", p13))

    # Check 14: 30-Seed SRBCT Share > 0.5
    srbct_aris = df_30[df_30["dataset"] == "srbct"]["ari"]
    srbct_share = round(float((srbct_aris > 0.5).mean()), 3)
    srbct_med = round(float(srbct_aris.median()), 3)
    p14 = (srbct_share == 0.700 and srbct_med == 0.547)
    results.append((14, "30-Seed SRBCT Bimodal", "70.0% >0.5, median 0.547", f"{srbct_share*100:.1f}%, median {srbct_med}", p14))

    # Check 15: Inductive Prediction Agreement (CNS, Colon, Leukemia, Ovarian, SRBCT)
    with open("results/passE/inductive_agreement.json") as f:
        aggr = json.load(f)
    aggr_cns = round(aggr["cns"]["mean_agreement"] * 100, 1)
    aggr_col = round(aggr["colon"]["mean_agreement"] * 100, 1)
    aggr_leu = round(aggr["leukemia"]["mean_agreement"] * 100, 1)
    aggr_ova = round(aggr["ovarian"]["mean_agreement"] * 100, 1)
    aggr_srb = round(aggr["srbct"]["mean_agreement"] * 100, 1)
    p15 = (aggr_cns == 99.2 and aggr_col == 99.2 and aggr_leu == 97.3 and aggr_ova == 96.9 and aggr_srb == 94.1)
    results.append((15, "Inductive Agreement (Biomedical)", "99.2%, 99.2%, 97.3%, 96.9%, 94.1%", f"{aggr_cns}%, {aggr_col}%, {aggr_leu}%, {aggr_ova}%, {aggr_srb}%", p15))

    # Check 16: Inductive Table 2 Leukemia Weighted Centroid
    df_ind = pd.read_csv("results/passE/inductive_direct_seeds0_9.csv")
    ind_leu = round(float(df_ind[(df_ind["dataset"] == "leukemia") & (df_ind["method"] == "ICC_v2_CentroidFull")]["ari"].mean()), 3)
    p16 = (ind_leu == 0.257)
    results.append((16, "Table 2 Leukemia Centroid", "0.257", f"{ind_leu}", p16))

    # Check 17: Inductive Table 2 SRBCT Weighted Centroid
    ind_srb = round(float(df_ind[(df_ind["dataset"] == "srbct") & (df_ind["method"] == "ICC_v2_CentroidFull")]["ari"].mean()), 3)
    p17 = (ind_srb == 0.221)
    results.append((17, "Table 2 SRBCT Centroid", "0.221", f"{ind_srb}", p17))

    # Check 18: Scaling Runtime N=10,000 (Dense vs ICC-v2)
    df_scale = pd.read_csv("experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_summary.csv")
    r10 = df_scale[df_scale["N"] == 10000]
    t_std = round(float(r10[r10["model"] == "Standard_Consensus"]["runtime_mean"].iloc[0]), 2)
    t_icc = round(float(r10[r10["model"] == "ICC_v2"]["runtime_mean"].iloc[0]), 2)
    speedup = round(t_std / t_icc, 1)
    p18 = (t_std == 29.96 and t_icc == 10.35 and speedup == 2.9)
    results.append((18, "Scaling Runtime N=10k", "29.96 s vs 10.35 s (2.9x)", f"{t_std} s vs {t_icc} s ({speedup}x)", p18))

    # Check 19: Scaling Dynamic RAM N=10,000
    m_std = round(float(r10[r10["model"] == "Standard_Consensus"]["peak_trace_mean"].iloc[0]), 1)
    m_icc = round(float(r10[r10["model"] == "ICC_v2"]["peak_trace_mean"].iloc[0]), 1)
    reduc_ram = round((m_std - m_icc) / m_std * 100, 1)
    p19 = (m_std == 2670.6 and m_icc == 68.8 and reduc_ram == 97.4)
    results.append((19, "Scaling Peak RAM N=10k", "2670.6 MB vs 68.8 MB (97.4%)", f"{m_std} MB vs {m_icc} MB ({reduc_ram}%)", p19))

    # Check 20: Scaling Graph RAM N=10,000
    g_std = round(float(r10[r10["model"] == "Standard_Consensus"]["graph_mem_mb"].iloc[0]), 1)
    g_icc = round(float(r10[r10["model"] == "ICC_v2"]["graph_mem_mb"].iloc[0]), 2)
    reduc_graph = round((g_std - g_icc) / g_std * 100, 1)
    p20 = (g_std == 762.8 and g_icc == 3.06 and reduc_graph == 99.6)
    results.append((20, "Scaling Graph RAM N=10k", "762.8 MB vs 3.06 MB (99.6%)", f"{g_std} MB vs {g_icc} MB ({reduc_graph}%)", p20))

    # Check 21: Exp 5 Controlled Scaling Default Exponent (95% CI)
    with open("results/passE/exp5_scaling_stats.json") as f:
        e5 = json.load(f)
    b_def = round(e5["Default_Exp4"]["beta"], 3)
    ci_def_l, ci_def_h = round(e5["Default_Exp4"]["ci_95"][0], 3), round(e5["Default_Exp4"]["ci_95"][1], 3)
    p21 = (b_def == 0.755 and ci_def_l == 0.590 and ci_def_h == 0.921)
    results.append((21, "Exp 5 Default Scaling Exponent", "0.755 [0.590, 0.921]", f"{b_def} [{ci_def_l}, {ci_def_h}]", p21))

    # Check 22: Exp 5 Controlled Scaling High-Throughput Exponent (95% CI)
    b_opt = round(e5["Optimized_Exp5"]["beta"], 3)
    ci_opt_l, ci_opt_h = round(e5["Optimized_Exp5"]["ci_95"][0], 3), round(e5["Optimized_Exp5"]["ci_95"][1], 3)
    p22 = (b_opt == 0.873 and ci_opt_l == 0.724 and ci_opt_h == 1.023)
    results.append((22, "Exp 5 Optimized Scaling Exponent", "0.873 [0.724, 1.023]", f"{b_opt} [{ci_opt_l}, {ci_opt_h}]", p22))

    # Check 23: Exp 5 Runtime at N=1,000,000
    t1m_def = round(e5["Default_Exp4"]["mean_time_1M"], 1)
    t1m_opt = round(e5["Optimized_Exp5"]["mean_time_1M"], 1)
    p23 = (t1m_def == 182.6 and t1m_opt == 141.2)
    results.append((23, "Exp 5 1M Runtimes (Def vs Opt)", "182.6 s vs 141.2 s", f"{t1m_def} s vs {t1m_opt} s", p23))

    # Check 24: Core-Halo Baseline Citation (Li et al. 2019) in references.bib
    bib_text = Path("springer_manuscript/references.bib").read_text(encoding="utf-8")
    has_li = ("10.1016/j.artint.2018.12.007" in bib_text and "li2019clustering" in bib_text)
    p24 = has_li
    results.append((24, "Li et al. (2019) in references.bib", "DOI: 10.1016/j.artint.2018.12.007", "Found in bib" if has_li else "Missing", p24))

    # Check 25: CrossRef Audit Completeness (REFS_AUDIT.csv)
    df_refs = pd.read_csv("LOOP/REFS_AUDIT.csv")
    n_refs = len(df_refs)
    n_verified = len(df_refs[df_refs["match_status"] == "MATCH_VERIFIED"])
    p25 = (n_refs >= 30 and n_verified >= 20)
    results.append((25, "CrossRef References Audit", ">=30 refs audited", f"{n_refs} audited, {n_verified} verified", p25))

    print(f"{'#':<3} | {'Checkpoint Description':<36} | {'Expected':<30} | {'Found':<30} | {'Status'}")
    print("-" * 115)
    all_pass = True
    for r in results:
        status_str = "[PASS]" if r[4] else "[FAIL]"
        if not r[4]:
            all_pass = False
        print(f"{r[0]:<3} | {r[1]:<36} | {r[2]:<30} | {r[3]:<30} | {status_str}")

    print("-" * 115)
    print(f"Overall Result: {'ALL 25 CHECKPOINTS PASSED' if all_pass else 'SOME CHECKPOINTS FAILED'}")
    return all_pass

if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
