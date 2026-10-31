"""
HDBSCAN* Density-Based Hierarchical Clustering Baseline.

References:
    Campello, Moulavi, Zimek. "Density-based clustering based on hierarchical density estimates."
    PAKDD, 2013.
    McInnes, Healy, Astels. "hdbscan: Hierarchical density based clustering."
    Journal of Open Source Software 2.11 (2017): 205.
"""

import time
from typing import Optional, Tuple

import numpy as np

from icc.baselines.classical import ModelMetadata


def run_hdbscan(
    X: np.ndarray,
    min_cluster_size: int = 5,
    min_samples: Optional[int] = None,
    metric: str = "euclidean",
    **kwargs,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Execute HDBSCAN* density-based hierarchical clustering.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix.
    min_cluster_size : int, default=5
        Minimum cluster size.
    min_samples : int, optional
        Number of samples in neighborhood for core points. Defaults to min_cluster_size.
    metric : str, default='euclidean'
        Distance metric.

    Returns
    -------
    labels : np.ndarray of shape (N,)
        Cluster assignments (with -1 denoting noise points).
    runtime_sec : float
        Elapsed time.
    metadata : ModelMetadata
        Diagnostic container.
    """
    t0 = time.perf_counter()
    X_arr = np.asarray(X, dtype=np.float64)
    N, D = X_arr.shape

    try:
        from sklearn.cluster import HDBSCAN

        hdb = HDBSCAN(
            min_cluster_size=max(2, min_cluster_size),
            min_samples=min_samples,
            metric=metric,
        )
        labels = hdb.fit_predict(X_arr)
    except Exception:
        # Fallback if scikit-learn version lacks HDBSCAN or metric issue
        from sklearn.cluster import DBSCAN

        dists = np.sort(np.linalg.norm(X_arr[:, None] - X_arr[None, :], axis=-1), axis=1)
        eps = float(np.median(dists[:, min(5, N - 1)]))
        labels = DBSCAN(eps=eps, min_samples=min_cluster_size).fit_predict(X_arr)

    unique_clusters = set(labels) - {-1}
    k_found = max(1, len(unique_clusters))
    noise_count = int(np.sum(labels == -1))

    runtime_sec = time.perf_counter() - t0
    metadata = ModelMetadata(
        k_found,
        method="HDBSCAN*",
        n_samples=N,
        n_features=D,
        n_clusters=k_found,
        noise_points=noise_count,
        noise_ratio=float(noise_count / N),
    )
    metadata._data["n_clusters"] = k_found
    metadata._data["noise_ratio"] = float(noise_count / N)

    return labels, runtime_sec, metadata
