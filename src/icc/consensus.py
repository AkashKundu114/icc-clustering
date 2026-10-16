"""
Invariant Core Consensus (ICC-v1):
Feature-Reliability-Calibrated Stability for High-Dimensional Cluster Ensembles.

Specifically designed for D >> N regimes where distance concentration and
spurious passenger variance induce hallucinated consensus stability.
"""

import numpy as np
import scipy.linalg as sla
from scipy.spatial.distance import cdist

from .core import run_clusterer


class InvariantCoreConsensus:
    """
    ICC-v1: Calibrated Anchor-Graph Consensus Clustering.

    Parameters:
    -----------
    n_clusters : int
        Number of target clusters (K).
    n_base_models : int (M)
        Number of subspace ensemble members (default: 25).
    n_anchors : int (L)
        Number of candidate anchors to sample (default: 100, L << N).
    subspace_rate : float
        Fraction of active features sampled per base model (default: 0.25).
    beta : float
        Noise penalization decay parameter (default: 2.0).
    base_clusterer : str
        Algorithm family for base clustering ('fcm', 'spectral', 'kmeans', 'ward').
    random_state : int
        Seed for reproducibility.
    """

    def __init__(
        self,
        n_clusters=3,
        n_base_models=25,
        n_anchors=100,
        subspace_rate=0.25,
        beta=2.0,
        base_clusterer="kmeans",
        random_state=42,
    ):
        self.k = n_clusters
        self.M = n_base_models
        self.L = n_anchors
        self.subspace_rate = subspace_rate
        self.beta = beta
        self.base_clusterer = base_clusterer
        self.random_state = random_state

        self.labels_ = None
        self.stability_ = None
        self.noise_fraction_ = None
        self.core_mask_ = None
        self.anchor_indices_ = None
        self.core_anchor_indices_ = None

    def fit_predict(self, X):
        """
        Executes ICC-v1 clustering on data matrix X in R^(N x D).
        """
        N, D = X.shape
        rng = np.random.default_rng(self.random_state)

        d_proj = min(30, D)
        proj_matrix = rng.normal(size=(D, d_proj)) / np.sqrt(d_proj)
        X_proj = X @ proj_matrix

        anchor_indices = [rng.choice(N)]
        for _ in range(1, min(self.L, N)):
            dist_sq = np.min(cdist(X_proj, X_proj[anchor_indices], metric="sqeuclidean"), axis=1)
            dist_sq[anchor_indices] = 0.0
            prob = dist_sq / (dist_sq.sum() + 1e-12)
            anchor_indices.append(rng.choice(N, p=prob))

        anchor_indices = np.array(anchor_indices, dtype=int)
        self.anchor_indices_ = anchor_indices
        anchors = X[anchor_indices]
        L = len(anchor_indices)

        var_features = np.var(X, axis=0)
        p_features = var_features / (np.sum(var_features) + 1e-12)
        n_active = max(2, int(D * self.subspace_rate))

        gates = []
        partitions = []
        anchor_partitions = []

        for m in range(self.M):
            seed_m = self.random_state + m * 31

            active_idx = rng.choice(D, size=n_active, replace=False, p=p_features)
            gate = np.zeros(D, dtype=float)
            gate[active_idx] = 1.0
            gates.append(gate)

            X_sub = X[:, active_idx]
            anchors_sub = anchors[:, active_idx]

            lab = run_clusterer(self.base_clusterer, X_sub, self.k, seed=seed_m)
            partitions.append(lab)

            centroids = np.array(
                [X_sub[lab == c].mean(axis=0) if np.any(lab == c) else X_sub[c] for c in range(self.k)]
            )
            anchor_lab = np.argmin(cdist(anchors_sub, centroids, metric="sqeuclidean"), axis=1)
            anchor_partitions.append(anchor_lab)

        gates = np.array(gates)

        B_star_num = np.zeros((N, L), dtype=float)
        B_star_den = np.zeros((N, L), dtype=float) + 1e-8

        total_dist_sq = cdist(X, anchors, metric="sqeuclidean") + 1e-12

        for m in range(self.M):
            p_m = partitions[m]
            p_anc_m = anchor_partitions[m]
            H_m = (p_m[:, None] == p_anc_m[None, :]).astype(float)

            noise_gate = 1.0 - gates[m]

            noise_dist_sq = cdist(X * noise_gate, anchors * noise_gate, metric="sqeuclidean")

            q_m = noise_dist_sq / total_dist_sq
            w_m = np.exp(-self.beta * q_m)

            B_star_num += w_m * H_m
            B_star_den += w_m

        B_star = B_star_num / B_star_den

        C = 1.0 - 4.0 * np.mean((B_star - 0.5) ** 2, axis=1)
        self.stability_ = C

        mean_noise_gate = np.mean(1.0 - gates, axis=0)
        R = np.sum(X**2 * mean_noise_gate, axis=1) / (np.sum(X**2, axis=1) + 1e-12)
        self.noise_fraction_ = R

        tau_R = np.quantile(R, 0.70)
        tau_C = np.quantile(C[R <= tau_R], 0.50) if np.any(R <= tau_R) else np.median(C)

        is_core = (C >= tau_C) & (R <= tau_R)
        self.core_mask_ = is_core

        core_anchor_mask = is_core[anchor_indices]
        core_anchors = np.where(core_anchor_mask)[0]

        if len(core_anchors) < self.k:
            core_anchors = np.argsort(C[anchor_indices] * (1.0 - R[anchor_indices]))[-self.k :]

        self.core_anchor_indices_ = anchor_indices[core_anchors]
        L_c = len(core_anchors)

        B_core = B_star[:, core_anchors]

        row_sums = B_core.sum(axis=1, keepdims=True)
        row_sums[row_sums < 1e-12] = 1.0
        B_norm = B_core / row_sums

        W_core = B_norm.T @ B_norm

        d_vec = W_core.sum(axis=1)
        d_inv_sqrt = 1.0 / np.sqrt(np.fmax(d_vec, 1e-12))
        L_sym = np.eye(L_c) - (d_inv_sqrt[:, None] * W_core * d_inv_sqrt[None, :])

        evals, evecs = sla.eigh(L_sym)
        V_core = evecs[:, : self.k]

        U_emb = B_norm @ V_core
        emb_norm = np.linalg.norm(U_emb, axis=1, keepdims=True)
        emb_norm[emb_norm < 1e-12] = 1.0
        U_emb /= emb_norm

        final_labels = run_clusterer("kmeans", U_emb, self.k, seed=self.random_state)
        self.labels_ = final_labels

        return final_labels
