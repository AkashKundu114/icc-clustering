"""
Hurdle-Bimodality Gating (HurdleGate) for zero-inflated count data (scRNA-seq / text).
"""

import numpy as np
import scipy.stats as stats
from typing import Optional

class HurdleGateFeatureSelector:
    """
    Two-part hurdle decomposition:
    Part 1: Bernoulli dropout frequency deviation.
    Part 2: Sarle bimodality coefficient on non-zero positive continuous support.
    """
    def __init__(self, min_positive_samples: int = 10, random_state: int = 42):
        self.min_positive_samples = min_positive_samples
        self.random_state = random_state
        self.hurdle_scores_: Optional[np.ndarray] = None
        self.sampling_probs_: Optional[np.ndarray] = None

    def fit(self, X: np.ndarray, temperature: float = 1.0) -> "HurdleGateFeatureSelector":
        N, D = X.shape
        scores = np.zeros(D)
        
        for d in range(D):
            col = X[:, d]
            pos_mask = col > 0.0
            n_pos = np.sum(pos_mask)
            dropout_frac = 1.0 - (n_pos / N)
            
            # Positive support bimodality
            if n_pos >= self.min_positive_samples:
                pos_vals = col[pos_mask]
                var_pos = np.var(pos_vals, ddof=1)
                if var_pos > 1e-12:
                    skew_pos = float(stats.skew(pos_vals, bias=False))
                    kurt_pos = float(stats.kurtosis(pos_vals, bias=False, fisher=True))
                    denom = kurt_pos + 3.0
                    bc_pos = (skew_pos**2 + 1.0) / denom if denom > 0.0 else 0.55
                else:
                    bc_pos = 0.0
            else:
                bc_pos = 0.0
                
            # Combine positive support multimodality with intermediate dropout variance
            # Features with extreme dropout (near 0 or near 1) carry less clustering signal
            # than features with balanced expression across groups (dropout ~ 0.3 - 0.7)
            dropout_entropy = - (dropout_frac * np.log2(max(1e-4, dropout_frac)) + 
                                 (1.0 - dropout_frac) * np.log2(max(1e-4, 1.0 - dropout_frac))) if (0.0 < dropout_frac < 1.0) else 0.0
                                 
            scores[d] = bc_pos * (1.0 + dropout_entropy)

        self.hurdle_scores_ = np.maximum(0.0, scores)
        
        # Soft sampling probabilities
        scaled = self.hurdle_scores_ / max(1e-3, temperature)
        exp_s = np.exp(scaled - np.max(scaled))
        self.sampling_probs_ = exp_s / np.sum(exp_s)
        
        return self
