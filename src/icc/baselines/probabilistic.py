"""
Probabilistic GMM Clustering with Model Order Selection (BIC and ICL).

References:
    Biernacki, Celeux, Govaert. "Assessing a mixture model for clustering with the
    integrated completed likelihood." IEEE TPAMI 22.7 (2000): 719-725.
    Fraley, Raftery. "Model-based clustering, discriminant analysis, and density
    estimation." JASA 97.458 (2002): 611-631.
"""

import time
from typing import Optional, Tuple

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
    Execute Gaussian Mixture Model clustering.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix.
    k : int
        Number of mixture components.
    covariance_type : str, default='diag'
        Covariance structure ('diag', 'full', 'spherical', 'tied').
    seed : int, default=42
        Random seed.
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
        method="GMM",
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


# Aliases for baseline benchmark runner
run_gmm_bic = run_gmm
run_gmm_icl = run_gmm

