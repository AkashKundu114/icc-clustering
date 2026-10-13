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
        random_state=42
    ):
        self.k = n_clusters
        self.M = n_base_models
        self.L = n_anchors
        self.subspace_rate = subspace_rate
        self.beta = beta
        self.base_clusterer = base_clusterer
        self.random_state = random_state

        # Fitted state
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

        # -------------------------------------------------------------
        # 1. CANDIDATE ANCHOR SELECTION (O(N L d_proj))
        # -------------------------------------------------------------
        # Project into low-dimensional space for fast, robust anchor seeding
        d_proj = min(30, D)
        proj_matrix = rng.normal(size=(D, d_proj)) / np.sqrt(d_proj)
        X_proj = X @ proj_matrix

        # Seed L anchors via k-means++ style distance sampling
        anchor_indices = [rng.choice(N)]
        for _ in range(1, min(self.L, N)):
            dist_sq = np.min(cdist(X_proj, X_proj[anchor_indices], metric='sqeuclidean'), axis=1)
            dist_sq[anchor_indices] = 0.0
            prob = dist_sq / (dist_sq.sum() + 1e-12)
            anchor_indices.append(rng.choice(N, p=prob))

        anchor_indices = np.array(anchor_indices, dtype=int)
        self.anchor_indices_ = anchor_indices
        anchors = X[anchor_indices]  # (L, D)
        L = len(anchor_indices)

        # -------------------------------------------------------------
        # 2. VARIANCE-GUIDED SUBSPACE ENSEMBLE (VSSG-lite)
        # -------------------------------------------------------------
        var_features = np.var(X, axis=0)
        p_features = var_features / (np.sum(var_features) + 1e-12)
        n_active = max(2, int(D * self.subspace_rate))

        gates = []
        partitions = []
        anchor_partitions = []

        for m in range(self.M):
            seed_m = self.random_state + m * 31
            # Sample active feature indices biased by variance prior
            active_idx = rng.choice(D, size=n_active, replace=False, p=p_features)
            gate = np.zeros(D, dtype=float)
            gate[active_idx] = 1.0
            gates.append(gate)

            # Partition in active subspace
            X_sub = X[:, active_idx]
            anchors_sub = anchors[:, active_idx]

            lab = run_clusterer(self.base_clusterer, X_sub, self.k, seed=seed_m)
            partitions.append(lab)

            # Map anchors into same partition clusters via nearest centroid
            centroids = np.array([X_sub[lab == c].mean(axis=0) if np.any(lab == c) else X_sub[c] for c in range(self.k)])
            anchor_lab = np.argmin(cdist(anchors_sub, centroids, metric='sqeuclidean'), axis=1)
            anchor_partitions.append(anchor_lab)

        gates = np.array(gates)  # (M, D)

        # -------------------------------------------------------------
        # 3. CONSTRUCT CALIBRATED ANCHOR BIPARTITE MATRIX B*
        # -------------------------------------------------------------
        B_star_num = np.zeros((N, L), dtype=float)
        B_star_den = np.zeros((N, L), dtype=float) + 1e-8

        # Precompute total pairwise distance squared to anchors in O(N L D)
        total_dist_sq = cdist(X, anchors, metric='sqeuclidean') + 1e-12

        for m in range(self.M):
            p_m = partitions[m]           # (N,)
            p_anc_m = anchor_partitions[m] # (L,)
            H_m = (p_m[:, None] == p_anc_m[None, :]).astype(float)  # (N, L)

            noise_gate = 1.0 - gates[m]    # (D,)

            # Fast vectorized distance strictly in gated-out noise dimensions via cdist
            noise_dist_sq = cdist(X * noise_gate, anchors * noise_gate, metric='sqeuclidean')

            q_m = noise_dist_sq / total_dist_sq  # (N, L) in [0, 1]
            w_m = np.exp(-self.beta * q_m)        # (N, L) in (0, 1]

            B_star_num += w_m * H_m
            B_star_den += w_m

        B_star = B_star_num / B_star_den  # (N, L) calibrated co-association

        # -------------------------------------------------------------
        # 4. TOPOLOGICAL TAXONOMY IN (C_i, R_i) SPACE
        # -------------------------------------------------------------
        # C_i: Local consensus determinacy over anchors in [0, 1].
        # Highly determined instances have associations close to 0 or 1 (C -> 1),
        # while ambiguous boundary points near 0.5 yield C -> 0.
        C = 4.0 * np.mean((B_star - 0.5)**2, axis=1)
        self.stability_ = C

        # R_i: Residual noise fraction
        mean_noise_gate = np.mean(1.0 - gates, axis=0)  # (D,)
        R = np.sum(X**2 * mean_noise_gate, axis=1) / (np.sum(X**2, axis=1) + 1e-12)
        self.noise_fraction_ = R

        # Dynamic quantile thresholding
        tau_R = np.quantile(R, 0.70)
        tau_C = np.quantile(C[R <= tau_R], 0.50) if np.any(R <= tau_R) else np.median(C)

        is_core = (C >= tau_C) & (R <= tau_R)
        self.core_mask_ = is_core

        # Filter candidate anchors to certified Invariant Core anchors
        core_anchor_mask = is_core[anchor_indices]
        core_anchors = np.where(core_anchor_mask)[0]

        # Safety fallback: ensure at least K anchors
        if len(core_anchors) < self.k:
            core_anchors = np.argsort(C[anchor_indices] * (1.0 - R[anchor_indices]))[-self.k:]

        self.core_anchor_indices_ = anchor_indices[core_anchors]
        L_c = len(core_anchors)

        # -------------------------------------------------------------
        # 5. REDUCED CORE-ANCHOR SPECTRAL GRAPH PARTITIONING
        # -------------------------------------------------------------
        B_core = B_star[:, core_anchors]  # (N, L_c)

        # Row-normalize bipartite graph
        row_sums = B_core.sum(axis=1, keepdims=True)
        row_sums[row_sums < 1e-12] = 1.0
        B_norm = B_core / row_sums

        # Form reduced L_c x L_c affinity matrix in O(N L_c^2)
        W_core = B_norm.T @ B_norm  # (L_c, L_c)

        # Graph Laplacian: D^(-1/2) W D^(-1/2)
        d_vec = W_core.sum(axis=1)
        d_inv_sqrt = 1.0 / np.sqrt(np.fmax(d_vec, 1e-12))
        L_sym = np.eye(L_c) - (d_inv_sqrt[:, None] * W_core * d_inv_sqrt[None, :])

        # Eigendecomposition on small L_c x L_c matrix in O(L_c^3)
        evals, evecs = sla.eigh(L_sym)
        V_core = evecs[:, :self.k]  # (L_c, K) smallest eigenvectors

        # Project all N samples back into spectral space in O(N L_c K)
        U_emb = B_norm @ V_core  # (N, K)
        emb_norm = np.linalg.norm(U_emb, axis=1, keepdims=True)
        emb_norm[emb_norm < 1e-12] = 1.0
        U_emb /= emb_norm

        # Final assignment via Lloyd's k-means on normalized embedding
        final_labels = run_clusterer("kmeans", U_emb, self.k, seed=self.random_state)
        self.labels_ = final_labels

        return final_labels
