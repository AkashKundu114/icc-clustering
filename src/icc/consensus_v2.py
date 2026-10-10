"""
Invariant Core Consensus Version 2 (ICC-v2):
Variance-Guided Subspace Generation (VSSG) + Geometry-Calibrated Anchor Consensus.

Specifically engineered for high-dimensional noise regimes (D >> N) where
uninformative passenger features induce distance concentration and spurious
stability attractors.

Mathematical Architecture:
1. Variance-Stabilized Subspace Gating (VSSG):
   Feature saliency scoring using bimodality coefficient:
       b_d = (skew_d^2 + 1) / (kurtosis_d + 3 + eps)
   Adaptive candidate pool:
       rho_pool = min(1.0, max(0.15, 100 / D))
   Subspace drawing:
       d_sub = max(2, int(|P| * subspace_rate))
2. Statistical Anchor Certification:
   Core identification via sample-level co-association stability:
       tau_core = quantile(stability, core_quantile)
   Anchor subset sampling:
       L anchors drawn uniformly at random from certified core instances.
3. Bipartite Spectral Consensus:
   Reduced bipartite affinity matrix B in R^(N x L).
   Normalized bipartite graph Laplacian L_norm in R^(L x L).
4. Inductive Extension (Out-of-sample projection):
   Projects unseen query samples onto geometry-calibrated centroids in R^(K x D).
"""

import time
from typing import Optional, Union, Dict, Any
import numpy as np
import scipy.linalg as sla
from scipy.spatial.distance import cdist
from scipy.stats import kurtosis, skew

from .core import run_clusterer, pairwise_coassoc, canonical


class InvariantCoreConsensusV2:
    """
    ICC-v2: Full Invariant Core Consensus with Variance-Guided Subspace Generation.

    Parameters
    ----------
    n_clusters : int, default=3
        Target number of clusters (K).
    n_base_models : int, default=25
        Number of ensemble partitions (M).
    n_anchors : int, default=40
        Number of candidate core anchors (L).
    core_quantile : float, default=0.50
        Quantile threshold tau_core for certifying invariant core samples.
    subspace_rate : float, default=0.30
        Fraction of active candidate pool features drawn per subspace.
    beta : float, default=2.0
        Noise penalization decay parameter.
    base_clusterer : str, default="auto"
        Base clustering algorithm family ('auto', 'kmeans', 'spectral', 'ward', 'fcm').
        If 'auto', chooses 'spectral' for N <= 100 and 'kmeans' for N > 100.
    random_state : int, default=42
        Random seed for reproducibility.

    Attributes
    ----------
    labels_ : np.ndarray of shape (N,)
        Consensus cluster assignments.
    stability_ : np.ndarray of shape (N,)
        Sample-level co-association stability scores.
    core_mask_ : np.ndarray of shape (N,) of bool
        Boolean mask denoting certified core instances.
    core_indices_ : np.ndarray
        Indices of certified core instances.
    anchor_indices_ : np.ndarray
        Indices of selected core anchors.
    feature_scores_ : np.ndarray of shape (D,)
        Saliency / bimodality scores for all input features (used in Exp 2.1 interpretability).
    selected_features_ : np.ndarray
        Feature indices included in the active candidate pool (used in Exp 2.1 interpretability).
    anchor_centroids_ : np.ndarray of shape (K, D)
        Cluster centroids in feature space for out-of-sample inductive projection.
    U_emb_ : np.ndarray of shape (N, K)
        Normalized spectral embeddings in R^K.
    """

    def __init__(
        self,
        n_clusters: int = 3,
        n_base_models: int = 25,
        n_anchors: int = 40,
        core_quantile: float = 0.50,
        subspace_rate: float = 0.30,
        beta: float = 2.0,
        base_clusterer: str = "auto",
        random_state: int = 42,
        random_seed: Optional[int] = None,
    ):
        if random_seed is not None:
            random_state = random_seed
        self.n_clusters = n_clusters
        self.k = n_clusters  # Backward compatibility alias
        self.n_base_models = n_base_models
        self.M = n_base_models  # Backward compatibility alias
        self.n_anchors = n_anchors
        self.L = n_anchors  # Backward compatibility alias
        self.core_quantile = core_quantile
        self.subspace_rate = subspace_rate
        self.beta = beta
        self.base_clusterer = base_clusterer
        self.random_state = random_state

        # Fitted attributes
        self.labels_: Optional[np.ndarray] = None
        self.stability_: Optional[np.ndarray] = None
        self.core_mask_: Optional[np.ndarray] = None
        self.core_indices_: Optional[np.ndarray] = None
        self.anchor_indices_: Optional[np.ndarray] = None
        self.feature_scores_: Optional[np.ndarray] = None
        self.selected_features_: Optional[np.ndarray] = None
        self.anchor_centroids_: Optional[np.ndarray] = None
        self.U_emb_: Optional[np.ndarray] = None

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """
        Fit ICC-v2 on input matrix X and return cluster labels.

        Parameters
        ----------
        X : np.ndarray of shape (N, D)
            Input feature matrix.

        Returns
        -------
        labels : np.ndarray of shape (N,)
            Cluster label assignments in [0, K-1].
        """
        X = np.asarray(X, dtype=np.float64)
        N, D = X.shape
        k = self.n_clusters
        rng = np.random.default_rng(self.random_state)

        # ---------------------------------------------------------------------
        # 1. Feature Saliency Scoring (Bimodality & Dispersion Prior)
        # ---------------------------------------------------------------------
        bimodal = np.zeros(D, dtype=np.float64)
        var = np.var(X, axis=0)
        valid_mask = var > 1e-12
        if np.any(valid_mask):
            X_valid = X[:, valid_mask]
            kurt = kurtosis(X_valid, axis=0, bias=False) if N >= 4 else kurtosis(X_valid, axis=0)
            sk = skew(X_valid, axis=0, bias=False) if N >= 3 else skew(X_valid, axis=0)
            # Finite-sample Sarle Bimodality Coefficient:
            # Fisher excess kurtosis converted to Pearson kurtosis with finite-sample null correction
            finite_corr = 3.0 * ((N - 1) ** 2) / ((N - 2) * (N - 3)) if N >= 4 else 3.0
            denom = kurt + finite_corr + 1e-5
            denom = np.fmax(denom, 1e-5)
            bimodal[valid_mask] = (sk**2 + 1.0) / denom
        self.feature_scores_ = bimodal

        # ---------------------------------------------------------------------
        # 2. Adaptive Candidate Pool
        # ---------------------------------------------------------------------
        top_frac = min(1.0, max(0.15, 100.0 / D))
        pool_size = max(k, int(top_frac * D))
        candidate_pool = np.argsort(bimodal)[-pool_size:]
        self.selected_features_ = candidate_pool

        # Subspace drawing size
        sub_size = max(2, int(len(candidate_pool) * self.subspace_rate))

        # Determine base clusterer engine
        if self.base_clusterer == "auto":
            base_engine = "spectral" if N <= 100 else "kmeans"
        else:
            base_engine = self.base_clusterer

        # ---------------------------------------------------------------------
        # 3. Base Clusterers on Diverse Guided Subspaces
        # ---------------------------------------------------------------------
        partitions = []
        for m in range(self.n_base_models):
            seed_m = int(rng.integers(0, 1000000))
            sub_idx = rng.choice(candidate_pool, size=sub_size, replace=False)
            X_sub = X[:, sub_idx]
            p = run_clusterer(base_engine, X_sub, k, seed=seed_m)
            partitions.append(p)

        # ---------------------------------------------------------------------
        # 4. Certified Core Anchors & Bipartite Graph Construction
        # ---------------------------------------------------------------------
        if N <= 2000:
            S = pairwise_coassoc(partitions)
            np.fill_diagonal(S, 0.0)
            sample_stability = np.sum(S**2, axis=1) / max(1, N - 1)
            np.fill_diagonal(S, 1.0)
            self.stability_ = sample_stability

            tau_stab = np.quantile(sample_stability, self.core_quantile)
            core_idx = np.where(sample_stability >= tau_stab)[0]
            if len(core_idx) < k:
                core_idx = np.argsort(sample_stability)[-k:]

            self.core_indices_ = core_idx
            self.core_mask_ = np.zeros(N, dtype=bool)
            self.core_mask_[core_idx] = True

            L = min(self.n_anchors, len(core_idx))
            anchor_idx = rng.choice(core_idx, size=L, replace=False)
            self.anchor_indices_ = anchor_idx
            B = S[:, anchor_idx]
        else:
            # Scalable O(N L) direct bipartite co-association for massive scale (N > 2000)
            P_stack = np.array(partitions)  # shape (M, N)
            sub_n = min(N, 1000)
            cand_idx = rng.choice(N, size=sub_n, replace=False)
            P_cand = P_stack[:, cand_idx]   # shape (M, sub_n)

            cand_S = np.zeros((sub_n, sub_n), dtype=np.float32)
            for m in range(self.n_base_models):
                cand_S += (P_cand[m, :, None] == P_cand[m, None, :]).astype(np.float32)
            cand_S /= self.n_base_models
            np.fill_diagonal(cand_S, 0.0)
            cand_stability = np.sum(cand_S**2, axis=1) / max(1, sub_n - 1)

            tau_stab = np.quantile(cand_stability, self.core_quantile)
            core_cand = np.where(cand_stability >= tau_stab)[0]
            if len(core_cand) < k:
                core_cand = np.argsort(cand_stability)[-k:]

            L = min(self.n_anchors, len(core_cand))
            anchor_local = rng.choice(core_cand, size=L, replace=False)
            anchor_idx = cand_idx[anchor_local]
            self.anchor_indices_ = anchor_idx
            self.core_indices_ = anchor_idx
            self.core_mask_ = np.zeros(N, dtype=bool)
            self.core_mask_[anchor_idx] = True

            P_anchors = P_stack[:, anchor_idx]  # shape (M, L)
            B = np.zeros((N, L), dtype=np.float32)
            for m in range(self.n_base_models):
                B += (P_stack[m, :, None] == P_anchors[m, None, :]).astype(np.float32)
            sample_stability = np.mean(B**2, axis=1)
            self.stability_ = sample_stability

        # ---------------------------------------------------------------------
        # 5. Bipartite Spectral Decomposition
        # ---------------------------------------------------------------------
        row_sums = B.sum(axis=1, keepdims=True)
        row_sums[row_sums < 1e-12] = 1.0
        B_norm = B / row_sums

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
        self.U_emb_ = U_emb

        pred = run_clusterer("kmeans", U_emb, k, seed=self.random_state)
        self.labels_ = pred

        # ---------------------------------------------------------------------
        # 6. Geometry-Calibrated Inductive Centroids in Feature Space
        # ---------------------------------------------------------------------
        self.anchor_centroids_ = np.zeros((k, D))
        for c in range(k):
            mask_c = (pred == c)
            if np.any(mask_c):
                # Weighted by sample stability to prioritize certified core points
                weights = sample_stability[mask_c]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    self.anchor_centroids_[c] = np.average(X[mask_c], axis=0, weights=weights)
                else:
                    self.anchor_centroids_[c] = np.mean(X[mask_c], axis=0)
            else:
                self.anchor_centroids_[c] = np.mean(X, axis=0)

        return self.labels_

    def fit(self, X: np.ndarray) -> "InvariantCoreConsensusV2":
        """
        Fit model on input matrix X.

        Parameters
        ----------
        X : np.ndarray of shape (N, D)

        Returns
        -------
        self : InvariantCoreConsensusV2
        """
        self.fit_predict(X)
        return self

    def predict(self, X_new: np.ndarray, subspace: bool = True) -> np.ndarray:
        """
        Inductive out-of-sample cluster assignment.
        Projects unseen instances onto the fitted geometry-calibrated centroids.

        Parameters
        ----------
        X_new : np.ndarray of shape (N_new, D)
            Unseen instances to partition.
        subspace : bool, default=True
            If True, computes distance within the active VSSG candidate pool features;
            if False, uses the full D-dimensional feature space.

        Returns
        -------
        preds : np.ndarray of shape (N_new,)
            Assigned cluster indices in [0, K-1].
        """
        if self.anchor_centroids_ is None:
            raise RuntimeError("Model has not been fitted yet. Call fit_predict() first.")
        X_new = np.asarray(X_new, dtype=np.float64)

        if subspace and self.selected_features_ is not None:
            pool = self.selected_features_
            dists = cdist(X_new[:, pool], self.anchor_centroids_[:, pool], metric="euclidean")
        else:
            dists = cdist(X_new, self.anchor_centroids_, metric="euclidean")

        return np.argmin(dists, axis=1)

    def predict_proba(self, X_new: np.ndarray, subspace: bool = True, temperature: float = 1.0) -> np.ndarray:
        """
        Compute soft cluster posterior probabilities for out-of-sample instances.

        Parameters
        ----------
        X_new : np.ndarray of shape (N_new, D)
        subspace : bool, default=True
        temperature : float, default=1.0

        Returns
        -------
        proba : np.ndarray of shape (N_new, K)
        """
        if self.anchor_centroids_ is None:
            raise RuntimeError("Model has not been fitted yet. Call fit_predict() first.")
        X_new = np.asarray(X_new, dtype=np.float64)

        if subspace and self.selected_features_ is not None:
            pool = self.selected_features_
            dists = cdist(X_new[:, pool], self.anchor_centroids_[:, pool], metric="euclidean")
        else:
            dists = cdist(X_new, self.anchor_centroids_, metric="euclidean")

        # Softmax over negative distances
        logits = -dists / max(1e-6, temperature)
        exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))
        return exp_logits / np.sum(exp_logits, axis=1, keepdims=True)
