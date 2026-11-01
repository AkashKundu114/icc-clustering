"""
HDBSCAN* and DBSCAN Density-Based Clustering Baselines.

References:
    Campello, Moulavi, Zimek. "Density-based clustering based on hierarchical density estimates."
    PAKDD, 2013.
    McInnes, Healy, Astels. "hdbscan: Hierarchical density based clustering."
    Journal of Open Source Software 2.11 (2017): 205.
"""

import time
from typing import Any, Dict, Optional, Tuple

import numpy as np
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

from icc.baselines.classical import ModelMetadata


def evaluate_hdbscan_metrics(
    y_true: np.ndarray,
    labels: np.ndarray,
) -> Dict[str, Any]:
    """
    Compute both full-sample (noise-as-cluster) and conditional core metrics for HDBSCAN*.

    Parameters
    ----------
    y_true : np.ndarray of shape (N,)
        Ground truth reference labels.
    labels : np.ndarray of shape (N,)
        Predicted labels, with -1 denoting noise/unassigned points.

    Returns
    -------
    dict
        Dictionary containing:
        - 'ari_full': standard ARI with noise points treated as a distinct cluster.
        - 'ari_core': conditional ARI computed strictly on core points (labels != -1).
        - 'nmi_full': standard NMI with noise points treated as a distinct cluster.
        - 'nmi_core': conditional NMI on core points.
        - 'noise_count': count of noise points.
        - 'noise_ratio': fraction of points assigned to noise.
        - 'coverage': fraction of points assigned to non-noise clusters (1 - noise_ratio).
        - 'n_clusters': number of discovered core clusters.
    """
    y_true_arr = np.asarray(y_true)
    labels_arr = np.asarray(labels)
    N = len(labels_arr)

    noise_mask = labels_arr == -1
    noise_count = int(np.sum(noise_mask))
    noise_ratio = float(noise_count / N) if N > 0 else 0.0
    coverage = float(1.0 - noise_ratio)

    unique_clusters = set(labels_arr) - {-1}
    k_found = len(unique_clusters)

    # Standard full-sample ARI (noise treated as -1)
    ari_full = float(adjusted_rand_score(y_true_arr, labels_arr))
    nmi_full = float(normalized_mutual_info_score(y_true_arr, labels_arr))

    # Core-only conditional metrics (if at least 2 points and >= 1 cluster)
    core_mask = ~noise_mask
    if np.sum(core_mask) >= 2 and len(set(labels_arr[core_mask])) >= 1 and len(set(y_true_arr[core_mask])) >= 1:
        ari_core = float(adjusted_rand_score(y_true_arr[core_mask], labels_arr[core_mask]))
        nmi_core = float(normalized_mutual_info_score(y_true_arr[core_mask], labels_arr[core_mask]))
    else:
        ari_core = float("nan")
        nmi_core = float("nan")

    return {
        "ari_full": ari_full,
        "ari_core": ari_core,
        "nmi_full": nmi_full,
        "nmi_core": nmi_core,
        "noise_count": noise_count,
        "noise_ratio": noise_ratio,
        "coverage": coverage,
        "n_clusters": k_found,
    }


def run_hdbscan(
    X: np.ndarray,
    min_cluster_size: int = 5,
    min_samples: Optional[int] = None,
    metric: str = "euclidean",
    n_pca_components: Optional[int] = None,
    seed: int = 42,
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
    n_pca_components : int, optional
        If provided, reduces ambient dimension before clustering to combat distance concentration.
    seed : int, default=42
        Random seed for dimensionality reduction.

    Returns
    -------
    labels : np.ndarray of shape (N,)
        Cluster assignments (with -1 denoting noise points).
    runtime_sec : float
        Elapsed time.
    metadata : ModelMetadata
        Diagnostic container with noise statistics and coverage.
    """
    t0 = time.perf_counter()
    X_arr = np.asarray(X, dtype=np.float64)
    N, D = X_arr.shape

    # Combat ambient distance concentration if requested
    if n_pca_components is not None and D > n_pca_components and N > n_pca_components:
        from sklearn.decomposition import PCA

        pca = PCA(n_components=n_pca_components, random_state=seed)
        X_clust = pca.fit_transform(X_arr)
    else:
        X_clust = X_arr

    try:
        from sklearn.cluster import HDBSCAN

        hdb = HDBSCAN(
            min_cluster_size=max(2, min_cluster_size),
            min_samples=min_samples,
            metric=metric,
        )
        labels = hdb.fit_predict(X_clust)
    except Exception:
        # Fallback if scikit-learn version lacks HDBSCAN
        from sklearn.cluster import DBSCAN

        dists = np.sort(np.linalg.norm(X_clust[:, None] - X_clust[None, :], axis=-1), axis=1)
        eps = float(np.median(dists[:, min(5, N - 1)]))
        labels = DBSCAN(eps=eps, min_samples=min_cluster_size).fit_predict(X_clust)

    unique_clusters = set(labels) - {-1}
    k_found = max(1, len(unique_clusters))
    noise_count = int(np.sum(labels == -1))
    noise_ratio = float(noise_count / N)
    coverage = float(1.0 - noise_ratio)

    runtime_sec = time.perf_counter() - t0
    metadata = ModelMetadata(
        k_found,
        method="HDBSCAN*",
        n_samples=N,
        n_features=D,
        n_clusters=k_found,
        noise_points=noise_count,
        noise_ratio=noise_ratio,
        coverage=coverage,
        reduced_dim=X_clust.shape[1],
    )
    metadata._data["n_clusters"] = k_found
    metadata._data["noise_ratio"] = noise_ratio
    metadata._data["coverage"] = coverage

    return labels, runtime_sec, metadata


def run_dbscan(
    X: np.ndarray,
    k: Optional[int] = None,
    eps: float = 0.5,
    min_samples: int = 5,
    seed: int = 42,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Run standard DBSCAN density-based clustering.
    """
    t0 = time.perf_counter()
    N, D = X.shape
    from sklearn.cluster import DBSCAN

    model = DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(X)
    runtime_sec = time.perf_counter() - t0
    unique_clusters = set(labels) - {-1}
    k_found = max(1, len(unique_clusters))
    noise_count = int(np.sum(labels == -1))
    noise_ratio = float(noise_count / N)
    coverage = float(1.0 - noise_ratio)
    metadata = ModelMetadata(
        k_found,
        method="DBSCAN",
        n_samples=N,
        n_features=D,
        n_clusters=k_found,
        noise_points=noise_count,
        noise_ratio=noise_ratio,
        coverage=coverage,
    )
    return labels, runtime_sec, metadata


__all__ = [
    "evaluate_hdbscan_metrics",
    "run_hdbscan",
    "run_dbscan",
]
