"""
Statistical tests and effect size estimators for nullconsensus.
"""

import numpy as np
import scipy.stats as stats
from typing import Dict, Tuple, Any

def paired_wilcoxon_holm(diffs_dict: Dict[str, np.ndarray]) -> Dict[str, Any]:
    """
    Computes paired Wilcoxon signed-rank test with Holm-Bonferroni correction.
    """
    results = {}
    p_values = []
    names = list(diffs_dict.keys())
    
    for name in names:
        diffs = diffs_dict[name]
        diffs = diffs[diffs != 0.0]
        if len(diffs) < 5:
            p_val = 1.0
            stat = 0.0
        else:
            stat, p_val = stats.wilcoxon(diffs, alternative="two-sided")
        results[name] = {"stat": float(stat), "raw_p": float(p_val)}
        p_values.append(p_val)
        
    # Holm step-down correction
    sorted_indices = np.argsort(p_values)
    m = len(p_values)
    adj_p = np.zeros(m)
    for rank, idx in enumerate(sorted_indices):
        adj_p[idx] = min(1.0, (m - rank) * p_values[idx])
        
    for i, name in enumerate(names):
        results[name]["holm_p"] = float(adj_p[i])
        
    return results

def bootstrap_confidence_interval(
    diffs: np.ndarray,
    n_boot: int = 10000,
    ci: float = 0.95,
    seed: int = 42
) -> Tuple[float, float, float]:
    """
    Clustered paired bootstrap confidence interval.
    """
    rng = np.random.default_rng(seed)
    n = len(diffs)
    boot_means = np.zeros(n_boot)
    for b in range(n_boot):
        sample = rng.choice(diffs, size=n, replace=True)
        boot_means[b] = np.mean(sample)
        
    alpha = 1.0 - ci
    lower = float(np.percentile(boot_means, 100.0 * (alpha / 2.0)))
    upper = float(np.percentile(boot_means, 100.0 * (1.0 - alpha / 2.0)))
    return float(np.mean(diffs)), lower, upper
