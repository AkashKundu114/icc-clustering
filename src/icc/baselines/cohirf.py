"""
src/icc/baselines/cohirf.py

Faithful reimplementation of CoHiRF (Consensus Hierarchical Random Features)
for high-dimensional clustering, following Belucci, Lounici, Meziani, and Kostic (arXiv:2502.00380, 2025).
"""

import time
from typing import Optional, Tuple, Union

import numpy as np
from scipy.sparse.csgraph import connected_components
from sklearn.base import BaseEstimator, ClusterMixin
from sklearn.cluster import KMeans

from .classical import ModelMetadata


class CoHiRF(BaseEstimator, ClusterMixin):
    """
    Consensus Hierarchical Random Features (CoHiRF) clustering model.

    Parameters
    ----------
    n_clusters : int, default=2
        The number of clusters to form.
    n_features_subspace : int or float, default=10
        Number of random features sampled per view. If float, fraction of D.
    repetitions : int, default=25
        Number of random feature projections / base clusterings per level.
    consensus_threshold : float, default=0.80
        Agreement fraction required to merge samples in unanimous consensus.
    max_iter : int, default=20
        Maximum hierarchical contraction iterations.
    random_state : int or None, default=None
        Random state seed for reproducibility.
    """

    def __init__(
        self,
        n_clusters: int = 2,
        n_features_subspace: Union[int, float] = 10,
        repetitions: int = 25,
        consensus_threshold: float = 0.80,
        max_iter: int = 20,
        random_state: Optional[int] = None,
    ):
        self.n_clusters = n_clusters
        self.n_features_subspace = n_features_subspace
        self.repetitions = repetitions
        self.consensus_threshold = consensus_threshold
        self.max_iter = max_iter
        self.random_state = random_state

    def fit(self, X: np.ndarray, y=None):
        X = np.asarray(X, dtype=np.float32)
        N, D = X.shape
        rng = np.random.RandomState(self.random_state)

        # Determine subspace dimensionality
        if isinstance(self.n_features_subspace, float):
            d_rf = max(2, min(D, int(np.floor(self.n_features_subspace * D))))
        else:
            d_rf = max(2, min(D, int(self.n_features_subspace)))

        # Track representative indices and parent assignments
        representatives = np.arange(N)
        parent_map = np.arange(N)

        for iteration in range(self.max_iter):
            n_rep = len(representatives)
            if n_rep <= self.n_clusters:
                break

            X_rep = X[representatives]

            # 1. Generate M partitions on random feature subspaces
            partitions = np.empty((n_rep, self.repetitions), dtype=np.int32)
            for m in range(self.repetitions):
                feat_idx = rng.choice(D, size=d_rf, replace=False)
                X_sub = X_rep[:, feat_idx]
                k_m = min(self.n_clusters, n_rep)
                km = KMeans(
                    n_clusters=k_m,
                    n_init=1,
                    max_iter=30,
                    tol=1e-3,
                    random_state=rng.randint(0, 1000000)
                )
                partitions[:, m] = km.fit_predict(X_sub)

            # 2. Form consensus co-association on representatives
            if n_rep <= 2000:
                co_assoc = np.zeros((n_rep, n_rep), dtype=np.float32)
                for m in range(self.repetitions):
                    p = partitions[:, m]
                    co_assoc += (p[:, None] == p[None, :])
                co_assoc /= float(self.repetitions)

                adj = (co_assoc >= self.consensus_threshold).astype(np.int32)
                n_groups, group_labels = connected_components(adj, directed=False)
            else:
                unique_sigs, group_labels = np.unique(partitions, axis=0, return_inverse=True)
                n_groups = len(unique_sigs)

            # Break if no further contraction or if contraction stagnates (< 2% reduction)
            if n_groups >= n_rep or (n_rep - n_groups) < max(1, int(0.02 * n_rep)):
                break

            # 3. Select new representatives (closest to cluster centroid)
            new_rep_list = []
            for g in range(n_groups):
                members = np.where(group_labels == g)[0]
                if len(members) == 1:
                    new_rep_list.append(representatives[members[0]])
                else:
                    sub_pts = X_rep[members]
                    center = np.mean(sub_pts, axis=0, keepdims=True)
                    # ||x - mu||^2 = ||x||^2 - 2 x.mu + ||mu||^2 (avoids large intermediate matrix allocation)
                    sq_norms = np.sum(sub_pts ** 2, axis=1)
                    dots = (sub_pts @ center.T).ravel()
                    dists = sq_norms - 2.0 * dots
                    best_local = members[np.argmin(dists)]
                    new_rep_list.append(representatives[best_local])
                    for m_idx in members:
                        parent_map[representatives[m_idx]] = representatives[best_local]

            representatives = np.array(new_rep_list, dtype=np.int64)

            if len(representatives) <= self.n_clusters:
                break

        # Final pass: cluster representatives into target K clusters
        X_rep = X[representatives]
        k_final = min(self.n_clusters, len(representatives))
        if len(representatives) > k_final:
            final_km = KMeans(
                n_clusters=k_final,
                n_init=5,
                random_state=rng.randint(0, 1000000)
            )
            rep_labels = final_km.fit_predict(X_rep)
        else:
            rep_labels = np.arange(len(representatives)) % self.n_clusters

        rep_to_label = {representatives[i]: rep_labels[i] for i in range(len(representatives))}

        resolved_parents = np.empty(N, dtype=np.int64)
        for i in range(N):
            curr = i
            while curr not in rep_to_label:
                nxt = parent_map[curr]
                if nxt == curr:
                    break
                curr = nxt
            if curr in rep_to_label:
                resolved_parents[i] = rep_to_label[curr]
            else:
                resolved_parents[i] = 0

        self.labels_ = resolved_parents
        return self

    def fit_predict(self, X: np.ndarray, y=None) -> np.ndarray:
        self.fit(X, y)
        return self.labels_


def run_cohirf(
    X: np.ndarray,
    k: int,
    repetitions: int = 25,
    seed: int = 42,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Adapter running CoHiRF baseline.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
    k : int
    repetitions : int, default=25
    seed : int, default=42

    Returns
    -------
    labels : np.ndarray of shape (N,)
    runtime_seconds : float
    metadata : ModelMetadata
    """
    t0 = time.perf_counter()
    model = CoHiRF(n_clusters=k, repetitions=repetitions, random_state=seed)
    labels = model.fit_predict(X)
    runtime = time.perf_counter() - t0
    meta = ModelMetadata(X.shape[0])
    return labels, runtime, meta
