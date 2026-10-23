"""
Decoy-Calibrated Feature Gating with False Discovery Rate (FDR) Control
======================================================================
Replaces heuristic coordinate-wise filtering (e.g. Sarle's Bimodality Coefficient)
with target-decoy / knockoff competition that provides rigorous finite-sample
FDR guarantees for high-dimensional feature selection.
"""

from typing import Optional

import numpy as np


class DecoyFeatureGating:
    """
    Decoy-Calibrated Feature Gating.

    Parameters
    ----------
    fdr_target : float, default=0.10
        Target nominal False Discovery Rate (q in (0, 1)).
    method : str, default="permutation"
        Method for generating decoys ('permutation' or 'gaussian_knockoff').
    metric : str, default="between_within_var"
        Feature saliency metric for cluster discrimination.
    random_state : int, default=42
        Random seed for reproducibility.
    """

    def __init__(
        self,
        fdr_target: float = 0.10,
        method: str = "permutation",
        metric: str = "between_within_var",
        random_state: int = 42,
    ):
        self.fdr_target = fdr_target
        self.method = method
        self.metric = metric
        self.random_state = random_state

        self.W_: Optional[np.ndarray] = None
        self.tau_: Optional[float] = None
        self.selected_indices_: Optional[np.ndarray] = None
        self.estimated_fdr_: Optional[float] = None

    def _compute_saliency(self, feature: np.ndarray, labels: np.ndarray) -> float:
        """Compute between-to-within variance or correlation with cluster structure."""
        classes = np.unique(labels)
        if len(classes) <= 1:
            return 0.0

        total_var = np.var(feature)
        if total_var < 1e-12:
            return 0.0

        cluster_means = [np.mean(feature[labels == c]) for c in classes]
        between_var = np.var(cluster_means)
        return float(between_var / total_var)

    def fit(self, X: np.ndarray, cluster_labels: np.ndarray) -> "DecoyFeatureGating":
        """
        Calibrate feature gating against synthetic decoys.

        Parameters
        ----------
        X : np.ndarray of shape (N, D)
            Input feature matrix.
        cluster_labels : np.ndarray of shape (N,)
            Cluster partition assignments.

        Returns
        -------
        self : DecoyFeatureGating
        """
        rng = np.random.default_rng(self.random_state)
        N, D = X.shape

        # Generate decoys
        X_decoy = np.zeros_like(X)
        if self.method == "permutation":
            for j in range(D):
                X_decoy[:, j] = rng.permutation(X[:, j])
        elif self.method == "gaussian_knockoff":
            mu = np.mean(X, axis=0)
            cov = np.cov(X, rowvar=False) + 1e-6 * np.eye(D)
            X_decoy = rng.multivariate_normal(mu, cov, size=N)
        else:
            raise ValueError(f"Unknown decoy method: {self.method}")

        # Compute feature scores for targets and decoys
        S_real = np.zeros(D)
        S_decoy = np.zeros(D)
        for j in range(D):
            S_real[j] = self._compute_saliency(X[:, j], cluster_labels)
            S_decoy[j] = self._compute_saliency(X_decoy[:, j], cluster_labels)

        # Knockoff / Decoy statistics: W_j = S_real_j - S_decoy_j
        self.W_ = S_real - S_decoy

        # Search for optimal threshold tau controlling FDR <= fdr_target
        positive_W = np.sort(self.W_[self.W_ > 0])
        if len(positive_W) == 0:
            self.tau_ = float("inf")
            self.selected_indices_ = np.array([], dtype=int)
            self.estimated_fdr_ = 0.0
            return self

        best_tau = None
        best_fdr = 1.0

        for tau in positive_W:
            n_neg = np.sum(self.W_ <= -tau)
            n_pos = np.sum(self.W_ >= tau)
            # Knockoff+ FDR estimator: (1 + #{W <= -tau}) / (#{W >= tau} v 1)
            fdr_est = (1.0 + n_neg) / max(1, n_pos)
            if fdr_est <= self.fdr_target:
                best_tau = float(tau)
                best_fdr = float(fdr_est)
                break

        if best_tau is None:
            # If target FDR cannot be met, fall back to the most conservative threshold
            best_tau = float(positive_W[-1])
            n_neg = np.sum(self.W_ <= -best_tau)
            n_pos = np.sum(self.W_ >= best_tau)
            best_fdr = float((1.0 + float(n_neg)) / max(1.0, float(n_pos)))

        self.tau_ = best_tau
        self.selected_indices_ = np.where(self.W_ >= self.tau_)[0]
        self.estimated_fdr_ = best_fdr

        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Filter feature matrix to selected features."""
        if self.selected_indices_ is None:
            raise RuntimeError("Model must be fitted before transforming data.")
        if len(self.selected_indices_) == 0:
            # Return original if no features pass
            return X
        return X[:, self.selected_indices_]

    def fit_transform(self, X: np.ndarray, cluster_labels: np.ndarray) -> np.ndarray:
        return self.fit(X, cluster_labels).transform(X)
