"""
src/icc/confirmatory/statistical_analyzer.py
Statistical Inference Engine for DMKD Gate G2 Confirmatory Analysis.

Implements exact pre-registered statistical procedures:
- Hierarchical two-stage aggregation (within-cohort median -> cross-cohort inference).
- Multiplicity control via Hochberg step-up procedure (Family 1).
- Two One-Sided Tests (TOST) with +/-0.02 equivalence margin (H3).
- Spearman rank correlation and discordance gap inference (H1a and H1b).
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from scipy import stats


def hodges_lehmann_estimator(diffs: np.ndarray) -> Tuple[float, Tuple[float, float]]:
    """
    Computes Hodges-Lehmann pseudomedian estimator and asymptotic 95% CI.
    """
    diffs = np.asarray(diffs, dtype=np.float64)
    n = len(diffs)
    # Pairwise Walsh averages (x_i + x_j) / 2 for i <= j
    walsh = []
    for i in range(n):
        for j in range(i, n):
            walsh.append(0.5 * (diffs[i] + diffs[j]))
    walsh = np.sort(walsh)
    estimate = float(np.median(walsh))

    # Standard normal approximation for rank sum critical values
    alpha = 0.05
    z_crit = stats.norm.ppf(1 - alpha / 2)
    # Total Walsh averages N_w = n*(n+1)/2
    nw = len(walsh)
    sigma_w = np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    k_lower = max(int(np.floor(0.5 * nw - z_crit * sigma_w)), 0)
    k_upper = min(int(np.ceil(0.5 * nw + z_crit * sigma_w)) - 1, nw - 1)

    ci_lower = float(walsh[k_lower])
    ci_upper = float(walsh[k_upper])
    return estimate, (ci_lower, ci_upper)


def tost_equivalence_test(
    diffs: np.ndarray,
    margin: float = 0.02,
    alpha: float = 0.05,
) -> Dict[str, Any]:
    """
    Executes Two One-Sided Tests (TOST) for operational equivalence within [-margin, +margin].
    Uses the 100*(1 - 2*alpha)% (i.e. 90% for alpha=0.05) Hodges-Lehmann CI as decision standard.
    """
    diffs = np.asarray(diffs, dtype=np.float64)
    n = len(diffs)

    # Test 1: H01: mean <= -margin vs H11: mean > -margin
    diffs_lower = diffs - (-margin)
    try:
        res_lower = stats.wilcoxon(diffs_lower, alternative="greater")
        p1 = float(res_lower.pvalue)
    except Exception:
        p1 = 1.0

    # Test 2: H02: mean >= +margin vs H12: mean < +margin
    diffs_upper = diffs - (+margin)
    try:
        res_upper = stats.wilcoxon(diffs_upper, alternative="less")
        p2 = float(res_upper.pvalue)
    except Exception:
        p2 = 1.0

    p_tost = max(p1, p2)

    # Compute 90% Hodges-Lehmann confidence interval
    # Using z_crit for 90% CI (alpha=0.05 on each side)
    z_crit = stats.norm.ppf(0.95)
    walsh = []
    for i in range(n):
        for j in range(i, n):
            walsh.append(0.5 * (diffs[i] + diffs[j]))
    walsh = np.sort(walsh)
    nw = len(walsh)
    sigma_w = np.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    k_lower = max(int(np.floor(0.5 * nw - z_crit * sigma_w)), 0)
    k_upper = min(int(np.ceil(0.5 * nw + z_crit * sigma_w)) - 1, nw - 1)

    ci_90_lower = float(walsh[k_lower])
    ci_90_upper = float(walsh[k_upper])
    hl_estimate = float(np.median(walsh))

    # Three-way decision rule
    if ci_90_lower > -margin and ci_90_upper < margin:
        decision = "EQUIVALENT"
    elif ci_90_upper < -margin or ci_90_lower > margin:
        decision = "NON_EQUIVALENT"
    else:
        decision = "INCONCLUSIVE"

    return {
        "hypothesis_id": "H3",
        "hl_estimate": hl_estimate,
        "ci_90": (ci_90_lower, ci_90_upper),
        "margin": margin,
        "p_lower": p1,
        "p_upper": p2,
        "p_tost": p_tost,
        "decision": decision,
    }


def holm_step_down(p_values: List[float], alpha: float = 0.05) -> List[float]:
    """
    Computes Holm-Bonferroni step-down adjusted p-values to control FWER at alpha.
    """
    m = len(p_values)
    indexed_p = sorted(enumerate(p_values), key=lambda x: x[1])
    adj_p = [0.0] * m
    running_max = 0.0
    for rank, (orig_idx, p_val) in enumerate(indexed_p):
        mult = m - rank
        val = min(1.0, mult * p_val)
        running_max = max(running_max, val)
        adj_p[orig_idx] = running_max
    return adj_p


def hochberg_step_up(p_values: List[float], alpha: float = 0.05) -> List[float]:
    """
    Computes Hochberg step-up adjusted p-values to control FWER at alpha.
    """
    m = len(p_values)
    indexed_p = sorted(enumerate(p_values), key=lambda x: x[1])
    adj_p = [0.0] * m

    # Step-up calculation: p_adj(i) = min_{j >= i} (m - j + 1) * p(j)
    running_min = 1.0
    for rank in range(m - 1, -1, -1):
        orig_idx, p_val = indexed_p[rank]
        multiplier = m - rank
        val = min(1.0, multiplier * p_val)
        running_min = min(running_min, val)
        adj_p[orig_idx] = running_min

    return adj_p


def evaluate_family_1(
    cohort_results: Dict[str, pd.DataFrame],
    baseline_names: List[str],
    target_model: str = "Full_GAC",
) -> pd.DataFrame:
    """
    Evaluates Family 1: 8 Primary Baseline Comparisons under Holm-Bonferroni FWER control (Primary)
    and Hochberg step-up (Secondary Sensitivity). Two-sided paired Wilcoxon signed-rank tests.
    """
    rows = []
    p_raw_list = []

    for bname in baseline_names:
        diffs = []
        for cohort_id, df in cohort_results.items():
            gac_med = df[df["model_name"] == target_model]["ari"].median()
            base_med = df[df["model_name"] == bname]["ari"].median()
            diffs.append(gac_med - base_med)

        diffs_arr = np.array(diffs, dtype=np.float64)
        med_diff = float(np.median(diffs_arr))
        mean_diff = float(np.mean(diffs_arr))
        hl_est, (ci_low, ci_high) = hodges_lehmann_estimator(diffs_arr)

        # Two-sided Wilcoxon signed-rank test (Preregistered standard)
        try:
            res = stats.wilcoxon(diffs_arr, alternative="two-sided")
            p_val = float(res.pvalue)
        except Exception:
            p_val = 1.0

        p_raw_list.append(p_val)
        rows.append({
            "baseline_model": bname,
            "n_cohorts": len(diffs_arr),
            "median_diff": round(med_diff, 4),
            "mean_diff": round(mean_diff, 4),
            "hl_estimate": round(hl_est, 4),
            "ci_95_lower": round(ci_low, 4),
            "ci_95_upper": round(ci_high, 4),
            "p_raw_twosided": p_val,
        })

    p_holm = holm_step_down(p_raw_list, alpha=0.05)
    p_hochberg = hochberg_step_up(p_raw_list, alpha=0.05)
    for i, r in enumerate(rows):
        r["p_adj_holm"] = round(p_holm[i], 5)
        r["p_adj_hochberg"] = round(p_hochberg[i], 5)
        r["reject_h0"] = (p_holm[i] < 0.05 and r["median_diff"] > 0)

    return pd.DataFrame(rows)


def evaluate_family_2(cohort_results: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Evaluates Family 2: Architectural Component Attribution (H2a, H2b)
    under Holm-Bonferroni FWER control across M=2 tests, with H3 evaluated
    independently via TOST operational equivalence.
    """
    rows = []
    
    # 1. H2a: BGSS vs Budget-Matched Random Feature Gating
    diffs_h2a = []
    for c_id, df in cohort_results.items():
        gac_med = df[df["model_name"] == "Full_GAC"]["ari"].median()
        rand_med = df[df["model_name"] == "Matched_Random"]["ari"].median()
        diffs_h2a.append(gac_med - rand_med)
    
    arr_2a = np.array(diffs_h2a, dtype=np.float64)
    hl_2a, (ci_low_2a, ci_high_2a) = hodges_lehmann_estimator(arr_2a)
    try:
        p_2a = float(stats.wilcoxon(arr_2a, alternative="greater").pvalue)
    except Exception:
        p_2a = 1.0

    rows.append({
        "hypothesis_id": "H2a",
        "comparison": "Full_GAC vs Matched_Random",
        "description": "Primary Bimodality Gating Advantage (Bipartite)",
        "n_cohorts": len(arr_2a),
        "median_diff": round(float(np.median(arr_2a)), 4),
        "hl_estimate": round(hl_2a, 4),
        "ci_lower": round(ci_low_2a, 4),
        "ci_upper": round(ci_high_2a, 4),
        "p_raw": p_2a,
        "test_type": "Wilcoxon signed-rank (one-sided)",
    })

    # 2. H2b: Dense-Consensus Attenuation Interaction
    diffs_h2b = []
    for c_id, df in cohort_results.items():
        gac_med = df[df["model_name"] == "Full_GAC"]["ari"].median()
        rand_med = df[df["model_name"] == "Matched_Random"]["ari"].median()
        dense_med = df[df["model_name"] == "Dense_GAC"]["ari"].median()
        delta_bip = gac_med - rand_med
        delta_dense = dense_med - rand_med
        diffs_h2b.append(delta_bip - delta_dense)
        
    arr_2b = np.array(diffs_h2b, dtype=np.float64)
    hl_2b, (ci_low_2b, ci_high_2b) = hodges_lehmann_estimator(arr_2b)
    try:
        p_2b = float(stats.wilcoxon(arr_2b, alternative="greater").pvalue)
    except Exception:
        p_2b = 1.0

    rows.append({
        "hypothesis_id": "H2b",
        "comparison": "Delta_Bip - Delta_Dense",
        "description": "Dense Consensus Attenuation Interaction",
        "n_cohorts": len(arr_2b),
        "median_diff": round(float(np.median(arr_2b)), 4),
        "hl_estimate": round(hl_2b, 4),
        "ci_lower": round(ci_low_2b, 4),
        "ci_upper": round(ci_high_2b, 4),
        "p_raw": p_2b,
        "test_type": "Wilcoxon signed-rank (one-sided)",
    })

    # Holm-Bonferroni correction across the 2 structural tests (H2a, H2b)
    p_h2 = holm_step_down([rows[0]["p_raw"], rows[1]["p_raw"]], alpha=0.05)
    for i in range(2):
        rows[i]["p_adj"] = round(p_h2[i], 5)
        rows[i]["reject_h0"] = (p_h2[i] < 0.05 and rows[i]["median_diff"] > 0)
        rows[i]["decision"] = "CONFIRMED" if rows[i]["reject_h0"] else "NOT_CONFIRMED"

    # 3. H3: Core Determinacy Anchor Certification (TOST Operational Equivalence +/-0.02)
    # Evaluated independently as an equivalence standard with 90% HL CI
    diffs_h3 = []
    for c_id, df in cohort_results.items():
        gac_med = df[df["model_name"] == "Full_GAC"]["ari"].median()
        ko4_med = df[df["model_name"] == "Knockout_4"]["ari"].median()
        diffs_h3.append(gac_med - ko4_med)
    
    arr_h3 = np.array(diffs_h3, dtype=np.float64)
    tost_res = tost_equivalence_test(arr_h3, margin=0.02, alpha=0.05)
    
    rows.append({
        "hypothesis_id": "H3",
        "comparison": "Full_GAC (Core) vs Knockout_4 (RandomLandmarks)",
        "description": "Core Determinacy Anchor Equivalence (TOST +/-0.02)",
        "n_cohorts": len(arr_h3),
        "median_diff": round(float(np.median(arr_h3)), 4),
        "hl_estimate": round(tost_res["hl_estimate"], 4),
        "ci_lower": round(tost_res["ci_90"][0], 4),
        "ci_upper": round(tost_res["ci_90"][1], 4),
        "p_raw": tost_res["p_tost"],
        "p_adj": tost_res["p_tost"],  # Independent TOST decision
        "test_type": "TOST Equivalence (90% HL CI)",
        "decision": tost_res["decision"],
        "reject_h0": (tost_res["decision"] == "EQUIVALENT"),
    })

    return pd.DataFrame(rows)

    return pd.DataFrame(rows)


def run_full_statistical_analysis(results_dir: Any) -> Dict[str, pd.DataFrame]:
    """
    Scans results_dir for {cohort_id}_raw_results.csv, aggregates within-cohort medians,
    executes Family 1 and Family 2 multiplicity-controlled analyses, and writes summaries.
    """
    from pathlib import Path
    results_dir = Path(results_dir)

    raw_files = list(results_dir.glob("*_raw_results.csv"))
    if not raw_files:
        print(f"[!] No raw result files found in {results_dir}")
        return {}

    cohort_results = {}
    for f in raw_files:
        c_id = f.name.replace("_raw_results.csv", "")
        df = pd.read_csv(f)
        cohort_results[c_id] = df

    print(f"[STAT] Found {len(cohort_results)} cohorts for statistical inference: {list(cohort_results.keys())}")

    # Family 1
    baseline_models = [
        "StdCons_All",
        "K-Means_All",
        "K-Means_VarFilt",
        "K-Means_PCA",
        "SparseKMeans",
        "FCAG",
        "FastMVC-Surrogate",
        "Li_et_al_2019",
    ]
    df_fam1 = evaluate_family_1(cohort_results, baseline_models, target_model="Full_GAC")
    f1_path = results_dir / "statistical_summary_family1.csv"
    df_fam1.to_csv(f1_path, index=False)
    print(f"[STAT] Saved Family 1 analysis to {f1_path}")

    # Family 2
    df_fam2 = evaluate_family_2(cohort_results)
    f2_path = results_dir / "statistical_summary_family2.csv"
    df_fam2.to_csv(f2_path, index=False)
    print(f"[STAT] Saved Family 2 analysis to {f2_path}")

    return {
        "family1": df_fam1,
        "family2": df_fam2,
    }
