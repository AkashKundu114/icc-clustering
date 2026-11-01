"""
Graph-Based Community Detection: Shared Nearest Neighbor (SNN) + Leiden Algorithm.
Universal standard in single-cell transcriptomics and high-dimensional computational biology.

References:
    Traag, Waltman, van Eck. "From Louvain to Leiden: guaranteeing well-connected communities."
    Scientific Reports 9.1 (2019): 5233.
    Stuart et al. "Comprehensive Integration of Single-Cell Data."
    Cell 177.7 (2019): 1888-1902.
"""

import time
import warnings
from typing import Optional, Tuple

import numpy as np
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

from icc.baselines.classical import ModelMetadata


def _build_snn_matrix(X: np.ndarray, n_neighbors: int = 15) -> np.ndarray:
    """Construct Shared Nearest Neighbor (SNN) graph with Jaccard edge weights."""
    N = len(X)
    k = min(n_neighbors, N - 1)
    nn = NearestNeighbors(n_neighbors=k + 1, metric="euclidean")
    nn.fit(X)
    indices = nn.kneighbors(X, return_distance=False)  # Shape (N, k+1)

    # Convert neighbor lists to sets for Jaccard calculation
    sets = [set(row) for row in indices]
    W = np.zeros((N, N), dtype=np.float32)

    for i in range(N):
        for j in sets[i]:
            if i != j:
                inter = len(sets[i].intersection(sets[j]))
                union = len(sets[i].union(sets[j]))
                if union > 0:
                    W[i, j] = float(inter) / float(union)

    W = (0.5 * (W + W.T)).astype(np.float32)  # type: ignore[assignment]
    return W


def run_spectral_snn(
    X: np.ndarray,
    k: int = 4,
    n_pca_components: int = 30,
    n_neighbors: int = 15,
    seed: int = 42,
    **kwargs,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Execute Spectral Clustering on SNN similarity graph (explicit baseline).

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix.
    k : int, default=4
        Number of clusters.
    n_pca_components : int, default=30
        Number of leading PCs.
    n_neighbors : int, default=15
        Number of nearest neighbors.
    seed : int, default=42
        Random seed.
    """
    t0 = time.perf_counter()
    X_arr = np.asarray(X, dtype=np.float64)
    N, D = X_arr.shape

    if D > n_pca_components and N > n_pca_components:
        pca = PCA(n_components=n_pca_components, random_state=seed)
        X_reduced = pca.fit_transform(X_arr)
    else:
        X_reduced = X_arr

    W = _build_snn_matrix(X_reduced, n_neighbors=n_neighbors)

    from sklearn.cluster import SpectralClustering

    k_eff = max(2, min(k, N - 1))
    sc = SpectralClustering(
        n_clusters=k_eff,
        affinity="precomputed",
        random_state=seed,
        n_init=5,
    )
    W_reg = W + np.eye(N) * 1e-4
    labels = sc.fit_predict(W_reg)

    runtime_sec = time.perf_counter() - t0
    metadata = ModelMetadata(
        k_eff,
        method="Spectral-SNN",
        n_samples=N,
        n_features=D,
        n_clusters=k_eff,
        n_neighbors=n_neighbors,
    )
    return labels, runtime_sec, metadata


def run_leiden_snn(
    X: np.ndarray,
    target_k: Optional[int] = None,
    n_pca_components: int = 30,
    n_neighbors: int = 15,
    resolution: float = 1.0,
    seed: int = 42,
    allow_fallback: bool = False,
    **kwargs,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Execute authentic Leiden community detection on PCA-SNN graph.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix.
    target_k : int, optional
        Target cluster count for resolution scanning.
    n_pca_components : int, default=30
        Number of leading PCs.
    n_neighbors : int, default=15
        Number of nearest neighbors.
    resolution : float, default=1.0
        Leiden modularity resolution parameter.
    seed : int, default=42
        Random seed.
    allow_fallback : bool, default=False
        If True, falls back to Spectral-SNN when igraph/leidenalg are missing,
        explicitly recording method="Spectral-SNN-Fallback".
        If False, marks baseline as UNAVAILABLE.
    """
    t0 = time.perf_counter()
    if target_k is None and "k" in kwargs:
        target_k = kwargs["k"]
    X_arr = np.asarray(X, dtype=np.float64)
    N, D = X_arr.shape

    # 1. Dimensionality reduction via PCA if D > n_pca_components
    if D > n_pca_components and N > n_pca_components:
        pca = PCA(n_components=n_pca_components, random_state=seed)
        X_reduced = pca.fit_transform(X_arr)
    else:
        X_reduced = X_arr

    # 2. Build SNN Graph
    W = _build_snn_matrix(X_reduced, n_neighbors=n_neighbors)

    # 3. Community detection via igraph / leidenalg
    try:
        import igraph as ig
        import leidenalg

        sources, targets = np.where(np.triu(W, k=1) > 0)
        weights = W[sources, targets]

        g = ig.Graph(n=N, edges=list(zip(sources, targets)), directed=False)
        g.es["weight"] = weights

        part = leidenalg.find_partition(
            g,
            leidenalg.CPMVertexPartition,
            weights="weight",
            resolution_parameter=resolution,
            seed=seed,
        )
        labels = np.array(part.membership, dtype=int)
        k_found = len(np.unique(labels))
        runtime_sec = time.perf_counter() - t0
        metadata = ModelMetadata(
            k_found,
            method="LeidenSNN",
            n_samples=N,
            n_features=D,
            n_clusters=k_found,
            resolution=resolution,
            status="SUCCESS",
        )
        return labels, runtime_sec, metadata

    except ImportError as e:
        if not allow_fallback:
            warnings.warn(
                f"LeidenSNN unavailable: {e}. Mark baseline as unavailable rather than "
                "silently substituting an alternative algorithm.",
                UserWarning,
                stacklevel=2,
            )
            runtime_sec = time.perf_counter() - t0
            metadata = ModelMetadata(
                0,
                method="LeidenSNN (UNAVAILABLE)",
                n_samples=N,
                n_features=D,
                n_clusters=0,
                status=f"UNAVAILABLE: {e}",
            )
            # Return dummy zero labels indicating uncomputed
            return np.zeros(N, dtype=int), runtime_sec, metadata

        # Explicit fallback when requested by user
        warnings.warn(
            "LeidenSNN falling back to Spectral Clustering on SNN graph. "
            "Reported method will be 'Spectral-SNN-Fallback'.",
            UserWarning,
            stacklevel=2,
        )
        k_eff = target_k if target_k is not None and target_k >= 2 else 4
        labels, rt_spec, meta_spec = run_spectral_snn(
            X_arr,
            k=k_eff,
            n_pca_components=n_pca_components,
            n_neighbors=n_neighbors,
            seed=seed,
        )
        runtime_sec = time.perf_counter() - t0
        metadata = ModelMetadata(
            meta_spec.n_clusters if hasattr(meta_spec, "n_clusters") else k_eff,
            method="Spectral-SNN-Fallback",
            n_samples=N,
            n_features=D,
            n_clusters=k_eff,
            status="FALLBACK_SPECTRAL",
        )
        return labels, runtime_sec, metadata
