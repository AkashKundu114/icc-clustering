"""
Sparse K-Means Clustering Baseline (Witten & Tibshirani, JASA 2010).

Formulation:
    Maximizes the between-cluster sum of squares (BCSS) with an L1 lasso penalty
    on feature weights w in R^D:
        max_{C, w} sum_{j=1}^D w_j * BCSS_j(C)
        subject to ||w||_2 <= 1, ||w||_1 <= s, w_j >= 0 for all j

Reference:
    Daniela M. Witten and Robert Tibshirani. "A framework for feature selection in
    clustering." Journal of the American Statistical Association 105.490 (2010): 713-726.
"""

import time
from typing import Optional, Tuple

import numpy as np
from sklearn.cluster import KMeans

from icc.baselines.classical import ModelMetadata


def _soft_threshold(a: np.ndarray, delta: float) -> np.ndarray:
    """Soft thresholding operator: S(a, delta) = sign(a) * max(0, |a| - delta)."""
    return np.sign(a) * np.fmax(0.0, np.abs(a) - delta)


def _solve_l1_l2_weights(a: np.ndarray, s: float, max_iter: int = 100, tol: float = 1e-5) -> np.ndarray:
    """
    Find non-negative w such that ||w||_2 = 1, ||w||_1 = s, maximizing a^T w.

    Parameters
    ----------
    a : np.ndarray of shape (D,)
        Feature-wise between-cluster sum of squares (BCSS_j >= 0).
    s : float
        L1 sparsity parameter, 1 <= s <= sqrt(D).
    """
    D = len(a)
    s = min(max(s, 1.0), np.sqrt(D))

    if s >= np.sqrt(D) or np.all(a <= 1e-12):
        w = np.ones(D, dtype=np.float64) / np.sqrt(D)
        return w

    # Binary search for delta > 0
    delta_low = 0.0
    delta_high = float(np.max(a))
    delta = 0.5 * delta_high

    for _ in range(max_iter):
        w_cand = _soft_threshold(a, delta)
        norm2 = np.linalg.norm(w_cand)
        if norm2 < 1e-12:
            delta_high = delta
            delta = 0.5 * (delta_low + delta_high)
            continue

        l1_norm = np.sum(w_cand) / norm2
        if np.abs(l1_norm - s) < tol:
            break
        elif l1_norm > s:
            delta_low = delta
        else:
            delta_high = delta
        delta = 0.5 * (delta_low + delta_high)

    w_final = _soft_threshold(a, delta)
    norm2 = np.linalg.norm(w_final)
    if norm2 > 1e-12:
        w_final /= norm2
    else:
        w_final = np.ones(D, dtype=np.float64) / np.sqrt(D)

    return w_final


def _compute_bcss(X: np.ndarray, labels: np.ndarray, k: int) -> np.ndarray:
    """Compute between-cluster sum of squares per feature."""
    N, D = X.shape
    grand_mean = np.mean(X, axis=0)
    tss = np.sum((X - grand_mean) ** 2, axis=0)

    wcss = np.zeros(D, dtype=np.float64)
    for c in range(k):
        mask = labels == c
        if np.any(mask):
            c_mean = np.mean(X[mask], axis=0)
            wcss += np.sum((X[mask] - c_mean) ** 2, axis=0)

    bcss = np.fmax(0.0, tss - wcss)
    return bcss


def run_sparse_kmeans(
    X: np.ndarray,
    k: int,
    s: Optional[float] = None,
    max_iter: int = 15,
    seed: int = 42,
    n_init: int = 5,
    **kwargs,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Execute Sparse K-Means (Witten & Tibshirani, JASA 2010).

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix. Should be centered and standardized.
    k : int
        Number of clusters.
    s : float, optional
        L1 sparsity parameter in [1.1, sqrt(D)]. Defaults to 0.15 * sqrt(D) + 1.0.
    max_iter : int, default=15
        Alternating optimization iterations.
    seed : int, default=42
        Random seed.
    n_init : int, default=5
        Number of k-means initializations.

    Returns
    -------
    labels : np.ndarray of shape (N,)
        Discrete cluster assignments.
    runtime_sec : float
        Elapsed wall-clock time in seconds.
    metadata : ModelMetadata
        Diagnostic container including selected feature weights.
    """
    t0 = time.perf_counter()
    X_arr = np.asarray(X, dtype=np.float64)
    N, D = X_arr.shape

    if s is None:
        s = max(1.1, 0.15 * np.sqrt(D) + 1.0)
    s = min(max(float(s), 1.0), np.sqrt(D))

    # Initial uniform weights
    w = np.ones(D, dtype=np.float64) / np.sqrt(D)

    # Initial K-Means on unweighted data
    km = KMeans(n_clusters=k, n_init=n_init, random_state=seed)
    labels = km.fit_predict(X_arr)

    # Alternating optimization
    for it in range(max_iter):
        old_labels = np.copy(labels)
        bcss = _compute_bcss(X_arr, labels, k)
        w = _solve_l1_l2_weights(bcss, s=s)

        # Weighted distance clustering: scale X by sqrt(w)
        X_weighted = X_arr * np.sqrt(w)[np.newaxis, :]
        km = KMeans(n_clusters=k, n_init=n_init, random_state=seed + it + 1)
        labels = km.fit_predict(X_weighted)

        # Check convergence
        if np.array_equal(labels, old_labels):
            break

    runtime_sec = time.perf_counter() - t0
    metadata = ModelMetadata(
        k,
        method="SparseKMeans",
        n_samples=N,
        n_features=D,
        n_clusters=k,
        sparsity_param=s,
        active_features=int(np.sum(w > 1e-5)),
    )
    metadata._data["feature_weights"] = w

    return labels, runtime_sec, metadata
