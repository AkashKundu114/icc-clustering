"""
ICC Preprocessing Subpackage.

Provides feature screening, subspace gating, and dataset preprocessing utilities:
- compute_bimodality_coefficient: Sarle's finite-sample Bimodality Coefficient for VSSG
- load_dataset, preprocess_dataset, list_datasets, get_dataset_info, DatasetInfo
"""

import numpy as np
from scipy.stats import kurtosis, skew

from ..datasets.registry import (
    DatasetInfo,
    get_dataset_info,
    list_datasets,
    load_dataset,
    preprocess_dataset,
)


def compute_bimodality_coefficient(
    X: np.ndarray,
    low_memory: bool = False,
    chunk_size: int = 1000,
) -> np.ndarray:
    """Compute Sarle's finite-sample Bimodality Coefficient (BC) for each feature.

    Formula:
        BC_j = (skew_j^2 + 1) / (kurtosis_j + 3 * (N-1)^2 / ((N-2)*(N-3)) + 1e-5)

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix.
    low_memory : bool, default=False
        If True, chunk computations along columns to cap peak memory.
    chunk_size : int, default=1000
        Number of columns processed per chunk when low_memory=True.

    Returns
    -------
    bimodal : np.ndarray of shape (D,)
        Finite-sample bimodality coefficient per feature. Constant features receive 0.0.
    """
    X = np.asarray(X, dtype=np.float64)
    N, D = X.shape
    bimodal = np.zeros(D, dtype=np.float64)
    var = np.var(X, axis=0)
    valid_mask = var > 1e-12

    if not np.any(valid_mask):
        return bimodal

    valid_indices = np.where(valid_mask)[0]
    n_valid = len(valid_indices)
    finite_corr = 3.0 * ((N - 1) ** 2) / ((N - 2) * (N - 3)) if N >= 4 else 3.0
    actual_chunk = chunk_size if (n_valid > chunk_size or low_memory) else n_valid

    for ch_start in range(0, n_valid, actual_chunk):
        ch_idx = valid_indices[ch_start : min(ch_start + actual_chunk, n_valid)]
        X_chunk = X[:, ch_idx]
        kurt = kurtosis(X_chunk, axis=0, bias=False) if N >= 4 else kurtosis(X_chunk, axis=0)
        sk = skew(X_chunk, axis=0, bias=False) if N >= 3 else skew(X_chunk, axis=0)
        denom = np.fmax(kurt + finite_corr + 1e-5, 1e-5)
        bimodal[ch_idx] = (sk**2 + 1.0) / denom

    return bimodal


__all__ = [
    "compute_bimodality_coefficient",
    "load_dataset",
    "preprocess_dataset",
    "list_datasets",
    "get_dataset_info",
    "DatasetInfo",
]
