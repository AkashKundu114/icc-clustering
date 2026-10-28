"""
Permutation-Null Calibrated Subspace Consensus (NullGate).
"""

import numpy as np
import scipy.stats as stats
from sklearn.cluster import KMeans
from typing import Optional, Tuple, Dict, Any

def compute_sarle_bc(x: np.ndarray) -> float:
    """Computes Sarle's Bimodality Coefficient: (skew^2 + 1) / (kurt + 3)."""
    n = len(x)
    if n < 4:
        return 5.0 / 9.0
    var = np.var(x, ddof=1)
    if var < 1e-12:
        return 0.0
    skew = float(stats.skew(x, bias=False))
    kurt = float(stats.kurtosis(x, bias=False, fisher=True)) # excess kurtosis
    denom = kurt + 3.0
    if denom <= 0.0:
        return 1.0
    bc = (skew ** 2 + 1.0) / denom
    return float(np.clip(bc, 0.0, 1.0))

class NullGateFeatureSelector:
    """
    Computes permutation-null calibrated saliency z-scores for feature screening.
    """
    def __init__(self, n_permutations: int = 10, random_state: int = 42):
        self.n_permutations = n_permutations
        self.random_state = random_state
        self.saliency_scores_: Optional[np.ndarray] = None
        self.sampling_probs_: Optional[np.ndarray] = None

    def fit(self, X: np.ndarray, temperature: float = 1.0) -> "NullGateFeatureSelector":
        N, D = X.shape
        rng = np.random.default_rng(self.random_state)
        
        # 1. Compute empirical Sarle BC for all features
        bc_emp = np.array([compute_sarle_bc(X[:, d]) for d in range(D)])
        
        # 2. Compute permutation-null baseline for each feature
        bc_null_mean = np.zeros(D)
        bc_null_std = np.zeros(D)
        
        for d in range(D):
            col = X[:, d]
            null_bcs = np.zeros(self.n_permutations)
            for b in range(self.n_permutations):
                perm_col = rng.permutation(col)
                null_bcs[b] = compute_sarle_bc(perm_col)
            bc_null_mean[d] = np.mean(null_bcs)
            bc_null_std[d] = max(1e-4, np.std(null_bcs))
            
        # 3. Z-score relative to permutation null
        z_scores = (bc_emp - bc_null_mean) / bc_null_std
        self.saliency_scores_ = np.maximum(0.0, z_scores)
        
        # 4. Saliency-weighted soft probabilities
        scaled_z = self.saliency_scores_ / max(1e-3, temperature)
        # Shift for numerical stability
        exp_z = np.exp(scaled_z - np.max(scaled_z))
        self.sampling_probs_ = exp_z / np.sum(exp_z)
        
        return self
