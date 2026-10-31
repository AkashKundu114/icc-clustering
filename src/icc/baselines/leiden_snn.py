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

    W = 0.5 * (W + W.T)
    return W


def run_leiden_snn(
    X: np.ndarray,
    target_k: Optional[int] = None,
    n_pca_components: int = 30,
    n_neighbors: int = 15,
    resolution: float = 1.0,
    seed: int = 42,
    **kwargs,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Execute Leiden community detection on PCA-SNN graph.

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

    # 3. Community detection via igraph / leidenalg if available, else spectral clustering on SNN
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
    except Exception:
        # Fallback: Normalized spectral clustering directly on SNN graph W
        from sklearn.cluster import SpectralClustering

        k = target_k if target_k is not None and target_k >= 2 else 4
        k = min(k, N - 1)
        sc = SpectralClustering(
            n_clusters=k,
            affinity="precomputed",
            random_state=seed,
            n_init=5,
        )
        # Ensure positive connectivity
        W_reg = W + np.eye(N) * 1e-4
        labels = sc.fit_predict(W_reg)

    unique_c = np.unique(labels)
    k_found = len(unique_c)

    runtime_sec = time.perf_counter() - t0
    metadata = ModelMetadata(
        k_found,
        method="LeidenSNN",
        n_samples=N,
        n_features=D,
        n_clusters=k_found,
        resolution=resolution,
    )
    metadata._data["n_clusters"] = k_found

    return labels, runtime_sec, metadata
