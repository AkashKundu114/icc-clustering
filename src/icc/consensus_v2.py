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
5. Anchor-Space Perturbation Profiling (ASPP):
   Evaluates multi-family cluster stability fingerprints and reliability certification
   in anchor space with linear O(N * L) auxiliary memory.
"""

from typing import Any, Dict, List, Optional

import numpy as np
import scipy.linalg as sla
from scipy.spatial.distance import cdist
from scipy.stats import kurtosis, skew

from .aspp import AnchorSpacePerturbationProfiler, ASPPConfig
from .core import run_clusterer


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
        Legacy parameter retained for backward API compatibility with v1 configurations.
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
        beta: Optional[float] = None,
        base_clusterer: str = "auto",
        enable_aspp: bool = False,
        aspp_config: Optional[ASPPConfig] = None,
        random_state: int = 42,
        random_seed: Optional[int] = None,
        pool_mode: str = "legacy",
        pool_mad_c: float = 3.5,
        pool_alpha: float = 0.05,
        embedding: str = "legacy",
        dense_threshold: int = 2000,
        pool_frac: float = 0.15,
    ):
        if beta is not None:
            import warnings

            warnings.warn(
                "`beta` is not used by ICC-v2 and is deprecated; it has no effect.", DeprecationWarning, stacklevel=2
            )
        if random_seed is not None:
            random_state = random_seed
        self.n_clusters = n_clusters
        self.k = n_clusters
        self.n_base_models = n_base_models
        self.M = n_base_models
        self.n_anchors = n_anchors
        self.L = n_anchors
        self.core_quantile = core_quantile
        self.subspace_rate = subspace_rate
        self.beta = beta
        self.pool_frac = pool_frac
        self.embedding = embedding
        self.dense_threshold = dense_threshold
        self.base_clusterer = base_clusterer
        self.enable_aspp = enable_aspp
        self.aspp_config = aspp_config
        self.random_state = random_state
        self.pool_mode = pool_mode
        self.pool_mad_c = pool_mad_c
        self.pool_alpha = pool_alpha

        self.labels_: Optional[np.ndarray] = None
        self.stability_: Optional[np.ndarray] = None
        self.core_mask_: Optional[np.ndarray] = None
        self.core_indices_: Optional[np.ndarray] = None
        self.anchor_indices_: Optional[np.ndarray] = None
        self.feature_scores_: Optional[np.ndarray] = None
        self.selected_features_: Optional[np.ndarray] = None
        self.anchor_centroids_: Optional[np.ndarray] = None
        self.U_emb_: Optional[np.ndarray] = None

        self.fingerprints_: Optional[Any] = None
        self.psi_: Optional[np.ndarray] = None
        self.reliability_categories_: Optional[List[str]] = None
        self.aspp_summary_: Optional[Dict[str, float]] = None
        self.aspp_profiler_: Optional[Any] = None

    def fit_predict(self, X: np.ndarray, batch_vector: Optional[np.ndarray] = None) -> np.ndarray:
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

        bimodal = np.zeros(D, dtype=np.float64)
        var = np.var(X, axis=0)
        valid_mask = var > 1e-12
        if np.any(valid_mask):
            X_valid = X[:, valid_mask]
            kurt = kurtosis(X_valid, axis=0, bias=False) if N >= 4 else kurtosis(X_valid, axis=0)
            sk = skew(X_valid, axis=0, bias=False) if N >= 3 else skew(X_valid, axis=0)

            finite_corr = 3.0 * ((N - 1) ** 2) / ((N - 2) * (N - 3)) if N >= 4 else 3.0
            denom = kurt + finite_corr + 1e-5
            denom = np.fmax(denom, 1e-5)
            bimodal[valid_mask] = (sk**2 + 1.0) / denom
        self.feature_scores_ = bimodal

        if self.pool_mode == "legacy":
            top_frac = min(1.0, max(0.15, 100.0 / D))
            pool_size = max(k, int(top_frac * D))
            candidate_pool = np.argsort(bimodal)[-pool_size:]
        elif self.pool_mode in ("bc_frac", "random_frac"):
            pool_size = min(D, max(k, 2, int(self.pool_frac * D)))
            if self.pool_mode == "bc_frac":
                candidate_pool = np.argsort(bimodal)[-pool_size:]
            else:
                candidate_pool = np.random.default_rng(self.random_state + 12345).choice(
                    D, size=pool_size, replace=False
                )
        elif self.pool_mode == "random":
            top_frac = min(1.0, max(0.15, 100.0 / D))
            pool_size = max(k, int(top_frac * D))
            candidate_pool = np.random.default_rng(self.random_state + 12345).choice(D, size=pool_size, replace=False)
        elif self.pool_mode == "robust":
            b = bimodal[valid_mask]
            med = np.median(b)
            mad = max(1.4826 * np.median(np.abs(b - med)), 1e-8)
            thr = med + self.pool_mad_c * mad
            cand = np.where(valid_mask & (bimodal > thr))[0]
            if len(cand) < max(k, 2):
                cand = np.argsort(bimodal)[-max(k, 2) :]
            candidate_pool = cand
        elif self.pool_mode == "gauss":
            from scipy.stats import norm

            rn = np.random.default_rng(0)
            Z = rn.normal(size=(N, 2000))
            kz = kurtosis(Z, axis=0, bias=False) if N >= 4 else kurtosis(Z, axis=0)
            sz = skew(Z, axis=0, bias=False) if N >= 3 else skew(Z, axis=0)
            fc = 3.0 * ((N - 1) ** 2) / ((N - 2) * (N - 3)) if N >= 4 else 3.0
            nb = (sz**2 + 1.0) / np.fmax(kz + fc + 1e-5, 1e-5)
            thr = nb.mean() + norm.ppf(1 - self.pool_alpha / max(D, 1)) * nb.std()
            cand = np.where(valid_mask & (bimodal > thr))[0]
            if len(cand) < max(k, 2):
                cand = np.argsort(bimodal)[-max(k, 2) :]
            candidate_pool = cand
        elif self.pool_mode == "null_calibrated":
            bimodal_threshold = 5.0 / 9.0
            passing_indices = np.where(bimodal >= bimodal_threshold)[0]
            min_features = min(2, D)
            max_pool = min(D, max(100, int(0.15 * D)))
            if len(passing_indices) >= min_features:
                if len(passing_indices) <= max_pool:
                    candidate_pool = passing_indices
                else:
                    top_pass = np.argsort(bimodal[passing_indices])[-max_pool:]
                    candidate_pool = passing_indices[top_pass]
            else:
                candidate_pool = np.argsort(bimodal)[-min(D, max(2, k)) :]
        else:
            raise ValueError(f"Unknown pool_mode: {self.pool_mode}")
        self.selected_features_ = candidate_pool

        sub_size = max(2, int(len(candidate_pool) * self.subspace_rate))

        if self.base_clusterer == "auto":
            base_engine = "spectral" if N <= 100 else "kmeans"
        else:
            base_engine = self.base_clusterer

        partitions = []
        for m in range(self.n_base_models):
            seed_m = int(rng.integers(0, 1000000))
            sub_idx = rng.choice(candidate_pool, size=sub_size, replace=False)
            X_sub = X[:, sub_idx]
            p = run_clusterer(base_engine, X_sub, k, seed=seed_m)
            partitions.append(p)

        P_stack = np.array(partitions)

        if N <= self.dense_threshold:
            lin_sum_sq = np.zeros(N, dtype=np.float64)
            for m1 in range(self.n_base_models):
                for m2 in range(self.n_base_models):
                    joint = P_stack[m1] * k + P_stack[m2]
                    counts = np.bincount(joint, minlength=k * k)
                    lin_sum_sq += counts[joint]

            sample_stability = np.maximum(0.0, (lin_sum_sq / (self.n_base_models**2) - 1.0) / max(1, N - 1))
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

            P_anchors = P_stack[:, anchor_idx]
            B = np.zeros((N, L), dtype=np.float64)
            for m in range(self.n_base_models):
                B += (P_stack[m, :, None] == P_anchors[m, None, :]).astype(np.float64)
            B /= self.n_base_models
        else:
            sub_n = min(N, 1000)
            cand_idx = rng.choice(N, size=sub_n, replace=False)
            P_cand = P_stack[:, cand_idx]

            P_cand_expanded = P_cand[:, :, None] == P_cand[:, None, :]
            S_sub = P_cand_expanded.mean(axis=0)
            np.fill_diagonal(S_sub, 0.0)
            sub_stab = np.sum(S_sub**2, axis=1) / max(1, sub_n - 1)

            tau_stab = np.quantile(sub_stab, self.core_quantile)
            core_cand_idx = np.where(sub_stab >= tau_stab)[0]
            if len(core_cand_idx) < k:
                core_cand_idx = np.argsort(sub_stab)[-k:]

            L = min(self.n_anchors, len(core_cand_idx))
            chosen_cand = rng.choice(core_cand_idx, size=L, replace=False)
            anchor_idx = cand_idx[chosen_cand]
            self.anchor_indices_ = anchor_idx

            self.core_indices_ = cand_idx[core_cand_idx]
            self.core_mask_ = np.zeros(N, dtype=bool)
            self.core_mask_[self.core_indices_] = True

            P_anchors = P_stack[:, anchor_idx]
            B = np.zeros((N, L), dtype=np.float64)
            for m in range(self.n_base_models):
                B += (P_stack[m, :, None] == P_anchors[m, None, :]).astype(np.float64)
            B /= self.n_base_models
            sample_stability = np.mean(B, axis=1)
            self.stability_ = sample_stability

        row_sums = B.sum(axis=1, keepdims=True)
        row_sums[row_sums < 1e-12] = 1.0
        B_norm = B / row_sums

        W_anchor = B_norm.T @ B_norm
        deg = W_anchor.sum(axis=1)
        deg_inv_sqrt = 1.0 / np.sqrt(np.fmax(deg, 1e-12))
        L_norm = np.eye(L) - (deg_inv_sqrt[:, None] * W_anchor * deg_inv_sqrt[None, :])

        evals, evecs = sla.eigh(L_norm)
        V_core = evecs[:, :k]

        if self.embedding == "transfer_cut":
            sig = np.fmax(1.0 - evals[:k], 1e-9)
            U_emb = B_norm @ (deg_inv_sqrt[:, None] * V_core) / np.sqrt(sig)
        elif self.embedding == "legacy":
            U_emb = B_norm @ V_core
        else:
            raise ValueError(f"Unknown embedding: {self.embedding}")

        emb_norm = np.linalg.norm(U_emb, axis=1, keepdims=True)
        emb_norm[emb_norm < 1e-12] = 1.0
        U_emb /= emb_norm
        self.U_emb_ = U_emb

        pred = run_clusterer("kmeans", U_emb, k, seed=self.random_state)
        self.labels_ = pred

        self.anchor_centroids_ = np.zeros((k, D))
        for c in range(k):
            mask_c = pred == c
            if np.any(mask_c):
                weights = sample_stability[mask_c]
                w_sum = weights.sum()
                if w_sum > 1e-12:
                    self.anchor_centroids_[c] = np.average(X[mask_c], axis=0, weights=weights)
                else:
                    self.anchor_centroids_[c] = np.mean(X[mask_c], axis=0)
            else:
                self.anchor_centroids_[c] = np.mean(X, axis=0)

        if self.enable_aspp:
            self.profile_perturbations(X, config=self.aspp_config, batch_vector=batch_vector)

        return self.labels_

    def fit(self, X: np.ndarray, batch_vector: Optional[np.ndarray] = None) -> "InvariantCoreConsensusV2":
        """
        Fit model on input matrix X.

        Parameters
        ----------
        X : np.ndarray of shape (N, D)
        batch_vector : Optional[np.ndarray] of shape (N,)
            Known categorical batch assignments, if available.

        Returns
        -------
        self : InvariantCoreConsensusV2
        """
        self.fit_predict(X, batch_vector=batch_vector)
        return self

    def transform(self, X: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Return the low-dimensional spectral embedding representation.

        Parameters
        ----------
        X : Optional[np.ndarray], default=None
            If None, returns fitted training embedding U_emb_ of shape (N, K).

        Returns
        -------
        embedding : np.ndarray of shape (N, K)
        """
        if self.U_emb_ is None:
            raise RuntimeError("Model has not been fitted yet. Call fit() first.")
        if X is None:
            return self.U_emb_
        return self.predict_proba(X)

    def profile_perturbations(
        self,
        X: np.ndarray,
        config: Optional[Any] = None,
        batch_vector: Optional[np.ndarray] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Execute Anchor-Space Perturbation Profiling (ASPP) on the fitted model.

        Parameters
        ----------
        X : np.ndarray of shape (N, D)
            Input feature matrix.
        config : Optional[ASPPConfig]
            ASPP configuration parameters.
        batch_vector : Optional[np.ndarray] of shape (N,)
            Known categorical batch assignments, if available.

        Returns
        -------
        fingerprints : pd.DataFrame
            Summary DataFrame indexed by cluster with multi-family stability fingerprints,
            Perturbation Sensitivity Index (PSI), and categorical reliability labels.
        """
        if self.labels_ is None:
            self.fit_predict(X, batch_vector=batch_vector)

        cfg = config or self.aspp_config
        if cfg is None and kwargs:
            cfg = ASPPConfig(**kwargs)

        profiler = AnchorSpacePerturbationProfiler(config=cfg)
        df_fingerprints = profiler.profile(self, X, batch_vector=batch_vector)

        self.fingerprints_ = df_fingerprints
        self.psi_ = profiler.psi_
        self.reliability_categories_ = profiler.reliability_categories_
        self.aspp_summary_ = profiler.aspp_summary_
        self.aspp_profiler_ = profiler

        return df_fingerprints

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

        logits = -dists / max(1e-6, temperature)
        exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))
        return exp_logits / np.sum(exp_logits, axis=1, keepdims=True)

    def predict_with_stability(
        self,
        X_new: np.ndarray,
        subspace: bool = True,
    ) -> Dict[str, Any]:
        """
        Inductive out-of-sample cluster assignment coupled with stability-calibrated confidence.

        Projects query points onto geometry-calibrated centroids and scales distance margin
        by the assigned cluster's Perturbation Sensitivity Index (PSI).

        Parameters
        ----------
        X_new : np.ndarray of shape (N_new, D)
            Unseen instances to partition.
        subspace : bool, default=True
            If True, uses active candidate pool features identified by VSSG.

        Returns
        -------
        results : dict with keys:
            - 'labels': np.ndarray of shape (N_new,) of int, assigned cluster labels.
            - 'confidence': np.ndarray of shape (N_new,) of float in [0, 1], stability-calibrated confidence.
            - 'margin': np.ndarray of shape (N_new,) of float in [0, 1], geometric distance margin.
            - 'psi': Optional[np.ndarray] of shape (N_new,), assigned cluster PSI values.
            - 'reliability': Optional[List[str]], categorical reliability labels for assigned clusters.
        """
        if self.anchor_centroids_ is None:
            raise RuntimeError("Model has not been fitted yet. Call fit_predict() first.")
        X_new = np.asarray(X_new, dtype=np.float64)

        if subspace and self.selected_features_ is not None:
            pool = self.selected_features_
            dists = cdist(X_new[:, pool], self.anchor_centroids_[:, pool], metric="euclidean")
        else:
            dists = cdist(X_new, self.anchor_centroids_, metric="euclidean")

        preds = np.argmin(dists, axis=1)

        if dists.shape[1] > 1:
            sorted_dists = np.sort(dists, axis=1)
            margin = (sorted_dists[:, 1] - sorted_dists[:, 0]) / np.fmax(sorted_dists[:, 1], 1e-9)
            margin = np.clip(margin, 0.0, 1.0)
        else:
            margin = np.ones(len(preds), dtype=np.float64)

        if self.psi_ is not None:
            psi_assigned = np.nan_to_num(self.psi_[preds], nan=0.5)
            confidence = np.nan_to_num(np.clip(margin * (1.0 - psi_assigned), 0.0, 1.0), nan=0.0)
            reliability = (
                [self.reliability_categories_[p] for p in preds] if self.reliability_categories_ is not None else None
            )
        else:
            psi_assigned = None
            confidence = margin
            reliability = None

        return {
            "labels": preds,
            "confidence": confidence,
            "margin": margin,
            "psi": psi_assigned,
            "reliability": reliability,
        }
