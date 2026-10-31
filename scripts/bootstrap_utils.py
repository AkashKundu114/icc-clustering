import numpy as np
import pandas as pd
from scipy import stats

def compute_cohort_bootstrap_ci(diffs_by_cohort, B=10000, seed=42):
    """
    Cohort-clustered bootstrap: resamples cohorts with replacement.
    diffs_by_cohort: list of mean differences for each cohort (length n_cohorts)
    """
    diffs = np.array(diffs_by_cohort)
    n = len(diffs)
    rng = np.random.default_rng(seed)
    boot_means = np.zeros(B)
    for b in range(B):
        idx = rng.choice(n, size=n, replace=True)
        boot_means[b] = np.mean(diffs[idx])
    ci_low = np.percentile(boot_means, 2.5)
    ci_high = np.percentile(boot_means, 97.5)
    return float(np.mean(diffs)), float(ci_low), float(ci_high)
