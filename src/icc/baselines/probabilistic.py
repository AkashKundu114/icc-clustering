"""
Probabilistic GMM Clustering with Model Order Selection (BIC and ICL).

References:
    Biernacki, Celeux, Govaert. "Assessing a mixture model for clustering with the
    integrated completed likelihood." IEEE TPAMI 22.7 (2000): 719-725.
    Fraley, Raftery. "Model-based clustering, discriminant analysis, and density
    estimation." JASA 97.458 (2002): 611-631.
"""

import time
import warnings
from typing import Dict, List, Optional, Tuple

import numpy as np
from sklearn.mixture import GaussianMixture

from icc.baselines.classical import ModelMetadata


def run_gmm(
    X: np.ndarray,
    k: int,
    covariance_type: str = "diag",
    seed: int = 42,
    n_init: int = 3,
    max_iter: int = 100,
    **kwargs,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Execute Gaussian Mixture Model clustering with fixed K.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix.
    k : int
        Number of mixture components (fixed).
    covariance_type : str, default='diag'
        Covariance structure ('diag', 'full', 'spherical', 'tied').
    seed : int, default=42
        Random seed.
    n_init : int, default=3
        Number of initializations.
    max_iter : int, default=100
        Maximum iterations.

    Returns
    -------
    labels : np.ndarray of shape (N,)
        Cluster assignments.
    runtime_sec : float
        Elapsed time.
    metadata : ModelMetadata
        Diagnostic container.
    """
    t0 = time.perf_counter()
    X_arr = np.asarray(X, dtype=np.float64)
    N, D = X_arr.shape

    # For high-dimensional data, default to diagonal covariance to prevent singular matrices
    cov_type = covariance_type if D <= 50 else "diag"

    gmm = GaussianMixture(
        n_components=k,
        covariance_type=cov_type,
        random_state=seed,
        n_init=n_init,
        max_iter=max_iter,
    )
    labels = gmm.fit_predict(X_arr)
    probs = gmm.predict_proba(X_arr)

    bic = float(gmm.bic(X_arr))
    entropy = -float(np.sum(probs * np.log(np.fmax(probs, 1e-12))))
    icl = bic + 2.0 * entropy

    runtime_sec = time.perf_counter() - t0
    metadata = ModelMetadata(
        k,
        method="GMM (Fixed-K)",
        n_samples=N,
        n_features=D,
        n_clusters=k,
        bic=bic,
        icl=icl,
        covariance_type=cov_type,
    )
    metadata._data["bic"] = bic
    metadata._data["icl"] = icl

    return labels, runtime_sec, metadata


def run_gmm_bic(
    X: np.ndarray,
    k: Optional[int] = None,
    k_min: int = 2,
    k_max: int = 10,
    candidate_k: Optional[List[int]] = None,
    covariance_type: str = "diag",
    seed: int = 42,
    n_init: int = 3,
    max_iter: int = 100,
    **kwargs,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Execute authentic unsupervised GMM model order selection via BIC minimization.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix.
    k : int, optional
        If provided (legacy compatibility), fits a single fixed K model.
    k_min : int, default=2
        Minimum candidate K.
    k_max : int, default=10
        Maximum candidate K.
    candidate_k : list of int, optional
        Explicit list of candidate K values.
    covariance_type : str, default='diag'
        Covariance structure ('diag', 'full', 'spherical', 'tied').
    seed : int, default=42
        Random seed.

    Returns
    -------
    labels : np.ndarray of shape (N,)
        Cluster assignments from model minimizing BIC.
    runtime_sec : float
        Elapsed time across the complete model selection grid.
    metadata : ModelMetadata
        Diagnostic container with selected K, BIC curve, and search grid.
    """
    if k is not None and "k_min" not in kwargs and "k_max" not in kwargs and candidate_k is None:
        warnings.warn(
            "run_gmm_bic received a single fixed k; executing fixed-K GMM. "
            "For authentic unsupervised model selection, omit k or specify k_min/k_max.",
            UserWarning,
            stacklevel=2,
        )
        return run_gmm(
            X,
            k=k,
            covariance_type=covariance_type,
            seed=seed,
            n_init=n_init,
            max_iter=max_iter,
            **kwargs,
        )

    t0 = time.perf_counter()
    X_arr = np.asarray(X, dtype=np.float64)
    N, D = X_arr.shape

    cov_type = covariance_type if D <= 50 else "diag"

    if candidate_k is None:
        max_bound = min(k_max, max(2, N // 3))
        candidate_k = list(range(max(2, k_min), max_bound + 1))

    bic_scores: Dict[int, float] = {}
    fitted_models: Dict[int, GaussianMixture] = {}

    for cand_k in candidate_k:
        try:
            gmm = GaussianMixture(
                n_components=cand_k,
                covariance_type=cov_type,
                random_state=seed,
                n_init=n_init,
                max_iter=max_iter,
            )
            gmm.fit(X_arr)
            bic_scores[cand_k] = float(gmm.bic(X_arr))
            fitted_models[cand_k] = gmm
        except Exception as e:
            warnings.warn(f"GMM fitting failed for k={cand_k}: {e}", UserWarning, stacklevel=2)

    if not bic_scores:
        # Fallback to single component if all candidate models failed
        return run_gmm(X_arr, k=2, covariance_type=cov_type, seed=seed)

    best_k = min(bic_scores.keys(), key=lambda k: bic_scores[k])
    best_gmm = fitted_models[best_k]
    labels = best_gmm.predict(X_arr)
    probs = best_gmm.predict_proba(X_arr)

    bic_val = bic_scores[best_k]
    entropy = -float(np.sum(probs * np.log(np.fmax(probs, 1e-12))))
    icl_val = bic_val + 2.0 * entropy

    runtime_sec = time.perf_counter() - t0
    metadata = ModelMetadata(
        best_k,
        method="GMM-BIC",
        n_samples=N,
        n_features=D,
        n_clusters=best_k,
        bic=bic_val,
        icl=icl_val,
        covariance_type=cov_type,
        bic_curve=bic_scores,
        candidate_k=candidate_k,
    )
    metadata._data["bic"] = bic_val
    metadata._data["icl"] = icl_val
    metadata._data["bic_curve"] = bic_scores
    metadata._data["candidate_k"] = candidate_k

    return labels, runtime_sec, metadata


def run_gmm_icl(
    X: np.ndarray,
    k: Optional[int] = None,
    k_min: int = 2,
    k_max: int = 10,
    candidate_k: Optional[List[int]] = None,
    covariance_type: str = "diag",
    seed: int = 42,
    n_init: int = 3,
    max_iter: int = 100,
    **kwargs,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Execute authentic unsupervised GMM model order selection via ICL minimization.
    """
    if k is not None and "k_min" not in kwargs and "k_max" not in kwargs and candidate_k is None:
        return run_gmm(
            X,
            k=k,
            covariance_type=covariance_type,
            seed=seed,
            n_init=n_init,
            max_iter=max_iter,
            **kwargs,
        )

    t0 = time.perf_counter()
    X_arr = np.asarray(X, dtype=np.float64)
    N, D = X_arr.shape

    cov_type = covariance_type if D <= 50 else "diag"

    if candidate_k is None:
        max_bound = min(k_max, max(2, N // 3))
        candidate_k = list(range(max(2, k_min), max_bound + 1))

    icl_scores: Dict[int, float] = {}
    fitted_models: Dict[int, GaussianMixture] = {}

    for cand_k in candidate_k:
        try:
            gmm = GaussianMixture(
                n_components=cand_k,
                covariance_type=cov_type,
                random_state=seed,
                n_init=n_init,
                max_iter=max_iter,
            )
            gmm.fit(X_arr)
            probs = gmm.predict_proba(X_arr)
            bic = float(gmm.bic(X_arr))
            entropy = -float(np.sum(probs * np.log(np.fmax(probs, 1e-12))))
            icl_scores[cand_k] = bic + 2.0 * entropy
            fitted_models[cand_k] = gmm
        except Exception as e:
            warnings.warn(f"GMM fitting failed for k={cand_k}: {e}", UserWarning, stacklevel=2)

    if not icl_scores:
        return run_gmm(X_arr, k=2, covariance_type=cov_type, seed=seed)

    best_k = min(icl_scores.keys(), key=lambda k: icl_scores[k])
    best_gmm = fitted_models[best_k]
    labels = best_gmm.predict(X_arr)

    runtime_sec = time.perf_counter() - t0
    metadata = ModelMetadata(
        best_k,
        method="GMM-ICL",
        n_samples=N,
        n_features=D,
        n_clusters=best_k,
        icl=icl_scores[best_k],
        covariance_type=cov_type,
        icl_curve=icl_scores,
        candidate_k=candidate_k,
    )
    metadata._data["icl"] = icl_scores[best_k]
    metadata._data["icl_curve"] = icl_scores
    metadata._data["candidate_k"] = candidate_k

    return labels, runtime_sec, metadata

