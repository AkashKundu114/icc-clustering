"""
ICC-AutoK: Genuinely Unsupervised Model Order Selection via Linear-Memory Anchor PAC.

Formulation:
    Discovers the optimal cluster count K in [K_min, K_max] without external reference labels
    by evaluating the Proportion of Ambiguous Clustering (PAC; Senbabaoglu et al., Sci Rep 2014)
    on the bipartite anchor consensus graph.

    PAC(k) = F_k(u_2) - F_k(u_1), with u_1 = 0.10, u_2 = 0.90
    Optimal K = argmin_{k} PAC(k)

References:
    Senbabaoglu, Michailidis, Li. "Critical limitations of consensus clustering in
    class discovery." Scientific Reports 4.1 (2014): 6207.
    Monti, Tamayo, Mesirov, Golub. "Consensus clustering: a resampling-based method
    for class discovery and clustering validation." Machine Learning 52.1 (2003): 91-118.
"""

import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score

from icc.consensus_v2 import InvariantCoreConsensusV2


@dataclass
class AutoKResult:
    """Container for unsupervised model order discovery results."""

    best_k_pac: int
    best_k_silhouette: int
    best_labels_pac: np.ndarray
    best_labels_silhouette: np.ndarray
    candidate_ks: List[int]
    pac_scores: Dict[int, float]
    silhouette_scores: Dict[int, float]
    ch_scores: Dict[int, float]
    db_scores: Dict[int, float]
    delta_areas: Dict[int, float]
    runtime_sec: float


def compute_anchor_pac(
    B: np.ndarray,
    n_pairs: int = 10000,
    u1: float = 0.10,
    u2: float = 0.90,
    random_state: int = 42,
) -> Tuple[float, float]:
    """
    Compute Proportion of Ambiguous Clustering (PAC) in O(n_pairs * L) time and O(1) memory.

    Parameters
    ----------
    B : np.ndarray of shape (N, L)
        Row-normalized sample-to-anchor bipartite projection matrix.
    n_pairs : int, default=10000
        Number of instance pairs to sample uniformly.
    u1, u2 : float
        Ambiguity threshold bounds (standard: 0.10, 0.90).

    Returns
    -------
    pac : float
        Fraction of sampled co-associations falling in [u1, u2].
    cdf_area : float
        Numerical integral of the empirical consensus CDF.
    """
    N, L = B.shape
    rng = np.random.default_rng(random_state)

    if N * (N - 1) // 2 <= n_pairs:
        # Full pairwise evaluation
        i_idx, j_idx = np.triu_indices(N, k=1)
    else:
        # Uniform random pair sampling
        i_idx = rng.integers(0, N, size=n_pairs)
        j_idx = rng.integers(0, N, size=n_pairs)
        # Exclude self-pairs
        valid = i_idx != j_idx
        i_idx, j_idx = i_idx[valid], j_idx[valid]

    # Compute dot products between sample pairs in anchor space: S_ij = B_i @ B_j^T
    co_assoc = np.sum(B[i_idx] * B[j_idx], axis=1)
    co_assoc = np.clip(co_assoc, 0.0, 1.0)

    # PAC: fraction of pairs with ambiguous co-clustering in (u1, u2)
    ambiguous = (co_assoc >= u1) & (co_assoc <= u2)
    pac = float(np.mean(ambiguous))

    # CDF Area under empirical distribution
    cdf_area = float(np.mean(co_assoc))

    return pac, cdf_area


def run_icc_autok(
    X: np.ndarray,
    k_min: int = 2,
    k_max: int = 8,
    n_base_models: int = 25,
    n_anchors: int = 40,
    subspace_rate: float = 0.30,
    pool_frac: float = 0.15,
    seed: int = 42,
    n_pairs: int = 10000,
) -> AutoKResult:
    """
    Execute ICC-AutoK to automatically discover K and assign clusters.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix.
    k_min : int, default=2
        Minimum candidate cluster count.
    k_max : int, default=8
        Maximum candidate cluster count.
    n_base_models : int, default=25
        Number of base partitions per candidate K.
    n_anchors : int, default=40
        Anchor budget L.
    subspace_rate : float, default=0.30
        Subspace feature rate.
    pool_frac : float, default=0.15
        BGSS feature gating retention fraction.
    seed : int, default=42
        Random seed for reproducibility.

    Returns
    -------
    AutoKResult dataclass with discovered K, labels, and diagnostic trajectories.
    """
    t0 = time.perf_counter()
    X_arr = np.asarray(X, dtype=np.float64)
    N, D = X_arr.shape

    candidate_ks = list(range(k_min, min(k_max + 1, N)))
    pac_scores: Dict[int, float] = {}
    silhouette_scores: Dict[int, float] = {}
    ch_scores: Dict[int, float] = {}
    db_scores: Dict[int, float] = {}
    cdf_areas: Dict[int, float] = {}
    delta_areas: Dict[int, float] = {}
    all_labels: Dict[int, np.ndarray] = {}

    prev_area = 0.0

    for idx, k in enumerate(candidate_ks):
        model = InvariantCoreConsensusV2(
            n_clusters=k,
            n_base_models=n_base_models,
            n_anchors=n_anchors,
            subspace_rate=subspace_rate,
            pool_frac=pool_frac,
            random_state=seed + idx,
        )
        labels = model.fit_predict(X_arr)
        all_labels[k] = labels

        # Extract anchor embedding projection if available, or compute nearest anchor matrix
        if model.U_emb_ is not None and model.U_emb_.shape[0] == N:
            # Normalized spectral embedding in R^k
            U = model.U_emb_
            U_norm = U / (np.linalg.norm(U, axis=1, keepdims=True) + 1e-12)
            pac, area = compute_anchor_pac(U_norm, n_pairs=n_pairs, random_state=seed)
        else:
            # Fallback to one-hot assignment co-association
            one_hot = np.zeros((N, k), dtype=np.float64)
            one_hot[np.arange(N), labels] = 1.0
            pac, area = compute_anchor_pac(one_hot, n_pairs=n_pairs, random_state=seed)

        pac_scores[k] = pac
        cdf_areas[k] = area

        if idx == 0:
            delta_areas[k] = area
        else:
            delta_areas[k] = (area - prev_area) / max(prev_area, 1e-6)
        prev_area = area

        # Compute internal cluster validity indices if >1 cluster present
        unique_c = np.unique(labels)
        if len(unique_c) > 1 and len(unique_c) < N:
            try:
                # Subsample for silhouette if N > 2000 for compute efficiency
                if N > 2000:
                    sub_idx = np.random.default_rng(seed).choice(N, size=2000, replace=False)
                    silhouette_scores[k] = float(silhouette_score(X_arr[sub_idx], labels[sub_idx]))
                else:
                    silhouette_scores[k] = float(silhouette_score(X_arr, labels))
                ch_scores[k] = float(calinski_harabasz_score(X_arr, labels))
                db_scores[k] = float(davies_bouldin_score(X_arr, labels))
            except Exception:
                silhouette_scores[k] = -1.0
                ch_scores[k] = 0.0
                db_scores[k] = 999.0
        else:
            silhouette_scores[k] = -1.0
            ch_scores[k] = 0.0
            db_scores[k] = 999.0

    # Model selection decision rule: minimum PAC with Occam's parsimony tolerance (+0.02)
    min_pac = min(pac_scores.values())
    best_k_pac = min(k for k, p in pac_scores.items() if p <= min_pac + 0.02)

    # Secondary decision rule: maximum Silhouette
    best_k_sil = max(silhouette_scores.keys(), key=lambda k: silhouette_scores[k])

    runtime_sec = time.perf_counter() - t0

    return AutoKResult(
        best_k_pac=best_k_pac,
        best_k_silhouette=best_k_sil,
        best_labels_pac=all_labels[best_k_pac],
        best_labels_silhouette=all_labels[best_k_sil],
        candidate_ks=candidate_ks,
        pac_scores=pac_scores,
        silhouette_scores=silhouette_scores,
        ch_scores=ch_scores,
        db_scores=db_scores,
        delta_areas=delta_areas,
        runtime_sec=runtime_sec,
    )
