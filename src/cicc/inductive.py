"""
Inductive Consensus Clustering with Conformal Guarantees
========================================================
Combines:
1. Target-decoy / knockoff feature gating.
2. Bipartite anchor graph consensus.
3. Split-conformal calibration for out-of-sample guarantees.
"""

from typing import Optional

import numpy as np
import scipy.linalg as sla
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split

from .conformal import ConformalClusterer, ConformalResult
from .decoy import DecoyFeatureGating


class InductiveConsensusClusterer:
    """
    Inductive Consensus Clustering with Conformal Uncertainty Quantification.

    Parameters
    ----------
    n_clusters : int, default=4
        Number of clusters (K).
    n_anchors : int, default=40
        Number of candidate anchors (m).
    n_base_models : int, default=20
        Number of ensemble base partitions.
    subspace_rate : float, default=0.50
        Fraction of active features drawn per ensemble partition.
    enable_decoy_gating : bool, default=True
        Whether to perform target-decoy feature selection with FDR control.
    fdr_target : float, default=0.10
        Target FDR for decoy feature gating.
    alpha : float, default=0.10
        Target significance level for conformal coverage (1 - alpha).
    random_state : int, default=42
        Random seed for reproducibility.
    """

    def __init__(
        self,
        n_clusters: int = 4,
        n_anchors: int = 40,
        n_base_models: int = 20,
        subspace_rate: float = 0.50,
        enable_decoy_gating: bool = True,
        fdr_target: float = 0.10,
        alpha: float = 0.10,
        random_state: int = 42,
    ):
        self.n_clusters = n_clusters
        self.n_anchors = n_anchors
        self.n_base_models = n_base_models
        self.subspace_rate = subspace_rate
        self.enable_decoy_gating = enable_decoy_gating
        self.fdr_target = fdr_target
        self.alpha = alpha
        self.random_state = random_state

        self.decoy_gating_: Optional[DecoyFeatureGating] = None
        self.conformal_calibrator_: Optional[ConformalClusterer] = None
        self.anchor_indices_: Optional[np.ndarray] = None
        self.anchors_: Optional[np.ndarray] = None
        self.labels_: Optional[np.ndarray] = None
        self.selected_features_: Optional[np.ndarray] = None

    def fit(self, X: np.ndarray, cal_ratio: float = 0.30) -> "InductiveConsensusClusterer":
        """
        Fit bipartite consensus on discovery split and calibrate conformal thresholds.

        Parameters
        ----------
        X : np.ndarray of shape (N, D)
            Input feature matrix.
        cal_ratio : float, default=0.30
            Fraction of data reserved for split-conformal calibration.

        Returns
        -------
        self : InductiveConsensusClusterer
        """
        rng = np.random.default_rng(self.random_state)
        N, D = X.shape

        # Normalize features
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        X_norm = X / norms

        # Split into Discovery (1 - cal_ratio) and Calibration (cal_ratio)
        indices = np.arange(N)
        idx_disc, idx_cal = train_test_split(
            indices, test_size=cal_ratio, random_state=self.random_state
        )
        X_disc = X_norm[idx_disc]
        X_cal = X_norm[idx_cal]
        N_disc = len(X_disc)

        # 1. Ensemble subspace generation on Discovery split
        m = min(self.n_anchors, N_disc)
        self.anchor_indices_ = rng.choice(N_disc, size=m, replace=False)
        self.anchors_ = X_disc[self.anchor_indices_]

        base_partitions = []
        for b in range(self.n_base_models):
            sub_dim = max(2, int(D * self.subspace_rate))
            sub_features = rng.choice(D, size=sub_dim, replace=False)
            km = KMeans(n_clusters=self.n_clusters, n_init=1, random_state=self.random_state + b)
            preds = km.fit_predict(X_disc[:, sub_features])
            base_partitions.append(preds)

        # 2. Bipartite affinity matrix B in R^(N_disc x m)
        B = np.zeros((N_disc, m))
        for b_preds in base_partitions:
            for a_pos in range(m):
                a_idx = self.anchor_indices_[a_pos]
                a_cluster = b_preds[a_idx]
                B[:, a_pos] += (b_preds == a_cluster).astype(float)
        B /= float(self.n_base_models)

        # 3. Transfer-Cut spectral consensus
        d_row = np.sum(B, axis=1)
        d_col = np.sum(B, axis=0)
        d_row[d_row == 0] = 1e-12
        d_col[d_col == 0] = 1e-12

        D_r_inv_sqrt = np.diag(1.0 / np.sqrt(d_row))
        D_c_inv_sqrt = np.diag(1.0 / np.sqrt(d_col))

        S = D_r_inv_sqrt @ B @ D_c_inv_sqrt
        # SVD of reduced bipartite affinity
        U, s, Vt = sla.svd(S, full_matrices=False)
        k_eff = min(self.n_clusters, U.shape[1])
        U_emb = U[:, :k_eff]
        u_norms = np.linalg.norm(U_emb, axis=1, keepdims=True)
        u_norms[u_norms == 0] = 1.0
        U_norm = U_emb / u_norms

        km_final = KMeans(n_clusters=self.n_clusters, n_init=10, random_state=self.random_state)
        disc_labels = km_final.fit_predict(U_norm)

        # 4. Target-decoy feature selection via finite-sample FDR control
        if self.enable_decoy_gating:
            self.decoy_gating_ = DecoyFeatureGating(
                fdr_target=self.fdr_target, random_state=self.random_state
            )
            self.decoy_gating_.fit(X_disc, disc_labels)
            self.selected_features_ = self.decoy_gating_.selected_indices_
        else:
            self.selected_features_ = np.arange(D)

        # 5. Project calibration samples to get calibration labels
        # Compute nearest centroid labels on calibration set
        centroids = np.zeros((self.n_clusters, D))
        for k in range(self.n_clusters):
            mask = (disc_labels == k)
            if np.any(mask):
                c = np.mean(X_disc[mask], axis=0)
                norm_c = np.linalg.norm(c)
                centroids[k] = c / (norm_c if norm_c > 0 else 1.0)

        cos_cal = X_cal @ centroids.T
        cal_labels = np.argmax(cos_cal, axis=1)

        # 6. Split-conformal calibration for finite-sample coverage guarantees
        self.conformal_calibrator_ = ConformalClusterer(
            alpha=self.alpha, random_state=self.random_state
        )
        self.conformal_calibrator_.fit_calibrate(
            X_disc=X_disc,
            labels_disc=disc_labels,
            X_cal=X_cal,
            labels_cal=cal_labels,
        )

        # Assign full dataset labels for reference
        assert self.conformal_calibrator_.centroids_ is not None
        full_cos = X_norm @ self.conformal_calibrator_.centroids_.T
        self.labels_ = np.argmax(full_cos, axis=1)

        return self

    def predict_conformal(
        self,
        X_new: np.ndarray,
        y_new: Optional[np.ndarray] = None,
    ) -> ConformalResult:
        """
        Produce out-of-sample cluster assignments with finite-sample coverage guarantees.

        Parameters
        ----------
        X_new : np.ndarray of shape (N_new, D)
            Query feature embeddings.
        y_new : Optional[np.ndarray] of shape (N_new,)
            Target labels for empirical coverage evaluation.

        Returns
        -------
        result : ConformalResult
        """
        if self.conformal_calibrator_ is None:
            raise RuntimeError("Clusterer must be fitted with fit() before predicting.")
        return self.conformal_calibrator_.predict(X_new, y_test=y_new)
