"""
Statistical hypothesis testing, effect sizes, and multi-algorithm comparison tests.
"""

from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from scipy import stats


def hodges_lehmann_estimator(diffs: np.ndarray, alpha: float = 0.05) -> Tuple[float, Tuple[float, float]]:
    """
    Computes Hodges-Lehmann pseudomedian estimator and asymptotic (1 - alpha) CI.
    """
    diffs = np.asarray(diffs, dtype=np.float64)
    n = len(diffs)
    if n == 0:
        return 0.0, (0.0, 0.0)

    walsh_list: List[float] = []
    for i in range(n):
        for j in range(i, n):
            walsh_list.append(float(0.5 * (diffs[i] + diffs[j])))
    walsh = np.sort(np.asarray(walsh_list, dtype=np.float64))
    estimate = float(np.median(walsh))

    z_crit = float(stats.norm.ppf(1 - alpha / 2))
    nw = len(walsh)
    sigma_w = float(np.sqrt(n * (n + 1) * (2 * n + 1) / 24))
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
    """
    diffs = np.asarray(diffs, dtype=np.float64)
    n = len(diffs)
    if n < 2:
        return {
            "p_tost": 1.0,
            "hl_estimate": float(np.mean(diffs)) if n == 1 else 0.0,
            "ci_90_lower": -margin,
            "ci_90_upper": margin,
            "decision": "INCONCLUSIVE",
            "margin": margin,
        }

    diffs_lower = diffs - (-margin)
    try:
        res_lower = stats.wilcoxon(diffs_lower, alternative="greater")
        p1 = float(res_lower.pvalue)
    except Exception:
        p1 = 1.0

    diffs_upper = diffs - (+margin)
    try:
        res_upper = stats.wilcoxon(diffs_upper, alternative="less")
        p2 = float(res_upper.pvalue)
    except Exception:
        p2 = 1.0

    p_tost = max(p1, p2)

    z_crit = float(stats.norm.ppf(1 - alpha))
    walsh_list: List[float] = []
    for i in range(n):
        for j in range(i, n):
            walsh_list.append(float(0.5 * (diffs[i] + diffs[j])))
    walsh = np.sort(np.asarray(walsh_list, dtype=np.float64))
    nw = len(walsh)
    sigma_w = float(np.sqrt(n * (n + 1) * (2 * n + 1) / 24))
    k_lower = max(int(np.floor(0.5 * nw - z_crit * sigma_w)), 0)
    k_upper = min(int(np.ceil(0.5 * nw + z_crit * sigma_w)) - 1, nw - 1)

    ci_90_lower = float(walsh[k_lower])
    ci_90_upper = float(walsh[k_upper])
    hl_estimate = float(np.median(walsh))

    if ci_90_lower > -margin and ci_90_upper < margin:
        decision = "EQUIVALENT"
    elif ci_90_upper < -margin or ci_90_lower > margin:
        decision = "NON_EQUIVALENT"
    else:
        decision = "INCONCLUSIVE"

    return {
        "p_tost": p_tost,
        "hl_estimate": hl_estimate,
        "ci_90_lower": ci_90_lower,
        "ci_90_upper": ci_90_upper,
        "decision": decision,
        "margin": margin,
    }


def friedman_test(*args: np.ndarray) -> Dict[str, float]:
    """
    Computes the Friedman non-parametric two-way ANOVA by ranks.
    """
    res = stats.friedmanchisquare(*args)
    return {"statistic": float(res.statistic), "pvalue": float(res.pvalue)}


def nemenyi_critical_distance(k: int, n: int, alpha: float = 0.05) -> float:
    """
    Computes the Nemenyi post-hoc critical distance for comparing mean ranks of k classifiers across n datasets.
    """
    q_table = {
        2: 1.960,
        3: 2.343,
        4: 2.569,
        5: 2.728,
        6: 2.850,
        7: 2.949,
        8: 3.031,
        9: 3.102,
        10: 3.164,
        11: 3.219,
        12: 3.268,
        13: 3.313,
        14: 3.354,
    }
    q = q_table.get(k, 3.4)
    return float(q * np.sqrt(k * (k + 1) / (6.0 * n)))


def wilcoxon_signed_rank_test(x: np.ndarray, y: Optional[np.ndarray] = None) -> Dict[str, float]:
    """
    Computes Wilcoxon signed-rank test for paired samples or one sample vs zero.
    """
    x = np.asarray(x, dtype=np.float64)
    if y is not None:
        y = np.asarray(y, dtype=np.float64)
        d = x - y
    else:
        d = x
    d_nonzero = d[d != 0]
    if len(d_nonzero) == 0:
        return {"statistic": 0.0, "pvalue": 1.0}
    res = stats.wilcoxon(d_nonzero)
    return {"statistic": float(res.statistic), "pvalue": float(res.pvalue)}


def bonferroni_correction(p_values: np.ndarray) -> np.ndarray:
    """
    Applies Bonferroni multiple testing correction, capping adjusted p-values at 1.0.
    """
    p_arr = np.asarray(p_values, dtype=np.float64)
    m = len(p_arr)
    return np.minimum(p_arr * m, 1.0)
