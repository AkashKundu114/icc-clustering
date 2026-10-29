"""Shared statistical and evaluation utilities for clustering research pipelines."""

import numpy as np
import scipy.stats as stats
from typing import Dict, List, Tuple, Any

def compute_friedman_nemenyi(ranks_matrix: np.ndarray, alpha: float = 0.05) -> Dict[str, Any]:
    """
    Compute omnibus Friedman test and Nemenyi Critical Difference (CD).
    
    Args:
        ranks_matrix: (n_datasets, n_methods) matrix of ranks or metric values.
        alpha: significance level (default 0.05).
        
    Returns:
        Dict with chi2, p_value, cd, and mean_ranks.
    """
    n_datasets, n_methods = ranks_matrix.shape
    
    # Compute rank per dataset if metric values passed
    ranks = np.zeros_like(ranks_matrix, dtype=float)
    for i in range(n_datasets):
        # Higher is better, so rank descending
        ranks[i] = stats.rankdata(-ranks_matrix[i], method="average")
        
    mean_ranks = np.mean(ranks, axis=0)
    
    chi2_stat, p_val = stats.friedmanchisquare(*[ranks_matrix[:, j] for j in range(n_methods)])
    
    # Studentized range q_alpha for two-tailed Nemenyi test
    # Common q_alpha critical values for alpha=0.05
    q_table = {
        2: 1.960, 3: 2.343, 4: 2.569, 5: 2.728, 6: 2.850, 7: 2.949,
        8: 3.031, 9: 3.102, 10: 3.164, 11: 3.219, 12: 3.268, 13: 3.313,
        14: 3.354, 15: 3.391, 16: 3.426, 20: 3.535, 25: 3.637, 30: 3.712
    }
    q_val = q_table.get(n_methods, 3.268 if n_methods <= 12 else 3.50)
    cd = q_val * np.sqrt((n_methods * (n_methods + 1)) / (6.0 * n_datasets))
    
    return {
        "chi2": float(chi2_stat),
        "p_value": float(p_val),
        "mean_ranks": mean_ranks.tolist(),
        "nemenyi_cd": float(cd)
    }

def vargha_delaney_a12(x: np.ndarray, y: np.ndarray) -> float:
    """
    Compute Vargha-Delaney A12 effect size statistic.
    A12 = (R1 / m - (m + 1) / 2) / n
    """
    m = len(x)
    n = len(y)
    r = stats.rankdata(np.concatenate([x, y]))
    r1 = np.sum(r[:m])
    return float((r1 - m * (m + 1) / 2.0) / (m * n))

def paired_cluster_bootstrap_ci(
    diffs: np.ndarray,
    n_boot: int = 10000,
    ci: float = 0.95,
    seed: int = 42
) -> Tuple[float, float, float]:
    """
    Dataset-clustered paired bootstrap confidence interval.
    
    Args:
        diffs: 1D array of paired differences across datasets.
        n_boot: bootstrap replicates.
        ci: confidence level.
        seed: random seed.
        
    Returns:
        (mean, ci_lower, ci_upper)
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
