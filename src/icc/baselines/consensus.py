"""
Consensus clustering baselines and ICC variants.

Refactored from experiments/exp3_real_world_benchmarks/src/benchmark_models.py.
Methods:
- Standard Consensus: Fred & Jain (IEEE TPAMI 2005)
- Li et al. 2019: Determinacy Core Spectral Ensemble (AI 2019)
- ICC-v1: Invariant Core Anchor Consensus (Full space)
- ICC-v2: Variance-Guided Subspace Generation (VSSG) + Invariant Core Consensus
"""

import time
from typing import Tuple

import numpy as np
import scipy.cluster.hierarchy as sch
import scipy.linalg as sla

from src.icc.core import pairwise_coassoc, run_clusterer

from .classical import ModelMetadata


def run_standard_consensus(
    X: np.ndarray,
    k: int,
    n_base_models: int = 25,
    seed: int = 42,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Fred & Jain (2005) Dense Co-association Consensus.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
    k : int
    n_base_models : int, default=25
    seed : int, default=42

    Returns
    -------
    labels : np.ndarray of shape (N,)
    runtime_seconds : float
    metadata : ModelMetadata
        Diagnostic container (n_core = N).
    """
    t0 = time.perf_counter()
    N = X.shape[0]
    rng = np.random.default_rng(seed)
    partitions = []
    for m in range(n_base_models):
        seed_m = int(rng.integers(0, 100000))
        p = run_clusterer("kmeans", X, k, seed=seed_m)
        partitions.append(p)

    S = pairwise_coassoc(partitions)
    dist_mat = 1.0 - S
    np.fill_diagonal(dist_mat, 0.0)

    condensed_dist = dist_mat[np.triu_indices(N, k=1)]
    condensed_dist = np.clip(condensed_dist, 0.0, 1.0)
    Z = sch.linkage(condensed_dist, method="average")
    pred = sch.fcluster(Z, t=k, criterion="maxclust") - 1
    runtime = time.perf_counter() - t0
    meta = ModelMetadata(
        N,
        method="standard_consensus",
        n_samples=N,
        n_clusters=k,
        n_base_models=n_base_models,
        n_core=N,
    )
    return pred, runtime, meta


def run_li_et_al_2019(
    X: np.ndarray,
    k: int,
    n_base_models: int = 25,
    seed: int = 42,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Li et al. (Artificial Intelligence, 2019) Core-Halo Consensus.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
    k : int
    n_base_models : int, default=25
    seed : int, default=42

    Returns
    -------
    labels : np.ndarray of shape (N,)
    runtime_seconds : float
    metadata : ModelMetadata
        Diagnostic container with integer value = len(core_idx).
    """
    t0 = time.perf_counter()
    N = X.shape[0]
    rng = np.random.default_rng(seed)
    partitions = []
    for m in range(n_base_models):
        seed_m = int(rng.integers(0, 100000))
        p = run_clusterer("kmeans", X, k, seed=seed_m)
        partitions.append(p)

    S = pairwise_coassoc(partitions)  # (N, N)

    # Compute sample-level stability
    np.fill_diagonal(S, 0.0)
    sample_stability = np.sum(S**2, axis=1) / max(1, N - 1)
    np.fill_diagonal(S, 1.0)

    tau_stab = np.median(sample_stability)
    is_core = sample_stability >= tau_stab
    core_idx = np.where(is_core)[0]
    halo_idx = np.where(~is_core)[0]

    if len(core_idx) < k:
        core_idx = np.argsort(sample_stability)[-k:]
        halo_idx = np.setdiff1d(np.arange(N), core_idx)

    # Step 1: Pre-structure on Core
    S_core = S[np.ix_(core_idx, core_idx)]
    dist_core = 1.0 - S_core
    np.fill_diagonal(dist_core, 0.0)
    condensed_dist = dist_core[np.triu_indices(len(core_idx), k=1)]
    condensed_dist = np.clip(condensed_dist, 0.0, 1.0)

    Z = sch.linkage(condensed_dist, method="average")
    core_labels = sch.fcluster(Z, t=k, criterion="maxclust") - 1

    final_labels = np.zeros(N, dtype=int)
    final_labels[core_idx] = core_labels

    # Step 2: Assign Halo
    if len(halo_idx) > 0:
        for h in halo_idx:
            affinities = []
            for c in range(k):
                c_pts = core_idx[core_labels == c]
                if len(c_pts) > 0:
                    affinities.append(np.mean(S[h, c_pts]))
                else:
                    affinities.append(0.0)
            final_labels[h] = int(np.argmax(affinities))

    runtime = time.perf_counter() - t0
    meta = ModelMetadata(
        len(core_idx),
        method="li_et_al_2019",
        n_samples=N,
        n_clusters=k,
        n_core=len(core_idx),
    )
    return final_labels, runtime, meta


def run_icc_v1(
    X: np.ndarray,
    k: int,
    n_base_models: int = 25,
    n_anchors: int = 40,
    seed: int = 42,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    ICC-v1: Invariant Core Anchor Consensus on full feature space (no VSSG).

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
    k : int
    n_base_models : int, default=25
    n_anchors : int, default=40
    seed : int, default=42

    Returns
    -------
    labels : np.ndarray of shape (N,)
    runtime_seconds : float
    metadata : ModelMetadata
        Diagnostic container with integer value = len(core_idx).
    """
    t0 = time.perf_counter()
    N, D = X.shape
    rng = np.random.default_rng(seed)

    partitions = []
    for m in range(n_base_models):
        seed_m = int(rng.integers(0, 100000))
        p = run_clusterer("kmeans", X, k, seed=seed_m)
        partitions.append(p)

    S = pairwise_coassoc(partitions)

    # Core identification
    np.fill_diagonal(S, 0.0)
    sample_stability = np.sum(S**2, axis=1) / max(1, N - 1)
    np.fill_diagonal(S, 1.0)

    tau_stab = np.quantile(sample_stability, 0.50)
    core_idx = np.where(sample_stability >= tau_stab)[0]
    if len(core_idx) < k:
        core_idx = np.argsort(sample_stability)[-k:]

    L = min(n_anchors, len(core_idx))
    anchor_idx = rng.choice(core_idx, size=L, replace=False)

    # Bipartite co-association graph
    B = S[:, anchor_idx]
    row_sums = B.sum(axis=1, keepdims=True)
    row_sums[row_sums < 1e-12] = 1.0
    B_norm = B / row_sums

    # Fast reduced spectral decomposition
    W_anchor = B_norm.T @ B_norm
    deg = W_anchor.sum(axis=1)
    deg_inv_sqrt = 1.0 / np.sqrt(np.fmax(deg, 1e-12))
    L_norm = np.eye(L) - (deg_inv_sqrt[:, None] * W_anchor * deg_inv_sqrt[None, :])

    evals, evecs = sla.eigh(L_norm)
    V_core = evecs[:, :k]

    U_emb = B_norm @ V_core
    emb_norm = np.linalg.norm(U_emb, axis=1, keepdims=True)
    emb_norm[emb_norm < 1e-12] = 1.0
    U_emb /= emb_norm

    pred = run_clusterer("kmeans", U_emb, k, seed=seed)
    runtime = time.perf_counter() - t0
    meta = ModelMetadata(
        len(core_idx),
        method="icc_v1",
        n_samples=N,
        n_clusters=k,
        n_anchors=L,
        n_core=len(core_idx),
    )
    return pred, runtime, meta


def run_icc_v2(
    X: np.ndarray,
    k: int,
    n_base_models: int = 25,
    n_anchors: int = 40,
    seed: int = 42,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    ICC-v2: Variance-Guided Subspace Generation (VSSG) + Invariant Core Anchor Consensus.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
    k : int
    n_base_models : int, default=25
    n_anchors : int, default=40
    seed : int, default=42

    Returns
    -------
    labels : np.ndarray of shape (N,)
    runtime_seconds : float
    metadata : ModelMetadata
        Diagnostic container with integer value = len(core_idx).
    """
    t0 = time.perf_counter()
    from src.icc.consensus_v2 import InvariantCoreConsensusV2
    model = InvariantCoreConsensusV2(
        n_clusters=k,
        n_base_models=n_base_models,
        n_anchors=n_anchors,
        random_state=seed,
    )
    labels = model.fit_predict(X)
    runtime = time.perf_counter() - t0
    n_core = len(model.core_indices_) if model.core_indices_ is not None else 0
    meta = ModelMetadata(
        n_core,
        method="icc_v2",
        n_samples=X.shape[0],
        n_clusters=k,
        n_anchors=n_anchors,
        n_core=n_core,
    )
    return labels, runtime, meta
