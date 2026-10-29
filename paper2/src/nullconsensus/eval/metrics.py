"""
Evaluation metrics for nullconsensus.
"""

import numpy as np
from sklearn.metrics import (
    adjusted_rand_score,
    normalized_mutual_info_score,
    adjusted_mutual_info_score,
    v_measure_score,
    fowlkes_mallows_score
)
from typing import Dict, Any

def evaluate_clustering(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Computes primary and secondary clustering agreement metrics.
    """
    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()
    
    return {
        "ari": float(adjusted_rand_score(y_true, y_pred)),
        "nmi": float(normalized_mutual_info_score(y_true, y_pred, average_method="arithmetic")),
        "ami": float(adjusted_mutual_info_score(y_true, y_pred, average_method="arithmetic")),
        "v_measure": float(v_measure_score(y_true, y_pred)),
        "fowlkes_mallows": float(fowlkes_mallows_score(y_true, y_pred))
    }
