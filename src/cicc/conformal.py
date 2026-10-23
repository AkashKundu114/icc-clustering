"""
Split-Conformal Prediction for Inductive Cluster Assignment
==========================================================
Provides distribution-free finite-sample coverage guarantees for out-of-sample
cluster assignments, set-valued predictions, and principled abstention for
novel cluster and out-of-distribution (OOD) discovery.
"""

from dataclasses import dataclass
from typing import List, Optional

import numpy as np


@dataclass
class ConformalResult:
    """
    Output of conformal inductive cluster prediction.

    Attributes
    ----------
    prediction_sets : List[List[int]]
        List of cluster index sets C(x) for each query instance.
    probabilities : np.ndarray of shape (N, K)
        Calibrated posterior probabilities for each cluster.
    set_sizes : np.ndarray of shape (N,)
        Number of candidate clusters in each prediction set |C(x)|.
    is_singleton : np.ndarray of shape (N,) of bool
        True if exactly one cluster was predicted with high confidence (|C(x)| == 1).
    is_ambiguous : np.ndarray of shape (N,) of bool
        True if the point lies on a cluster boundary (|C(x)| > 1).
    is_abstention : np.ndarray of shape (N,) of bool
        True if the point is an outlier or novel cluster candidate (|C(x)| == 0).
    empirical_coverage : Optional[float]
        Holdout empirical coverage, if ground truth / consensus labels were provided.
    average_set_size : float
        Mean prediction set cardinality across query instances.
    """
    prediction_sets: List[List[int]]
    probabilities: np.ndarray
    set_sizes: np.ndarray
    is_singleton: np.ndarray
    is_ambiguous: np.ndarray
    is_abstention: np.ndarray
    empirical_coverage: Optional[float]
    average_set_size: float


class ConformalClusterer:
    """
    Conformal Inductive Cluster Calibrator.

    Parameters
    ----------
    alpha : float, default=0.10
        Significance level; ensures 1 - alpha marginal coverage guarantee.
    temperature : float, default=10.0
        Softmax scaling temperature on cosine affinities.
    random_state : int, default=42
        Random seed for calibration splits.
    """

    def __init__(
        self,
        alpha: float = 0.10,
        temperature: float = 10.0,
        random_state: int = 42,
    ):
        self.alpha = alpha
        self.temperature = temperature
        self.random_state = random_state

        self.centroids_: Optional[np.ndarray] = None
        self.n_clusters_: Optional[int] = None
        self.q_hat_: Optional[float] = None
        self.cal_scores_: Optional[np.ndarray] = None

    def fit_calibrate(
        self,
        X_disc: np.ndarray,
        labels_disc: np.ndarray,
        X_cal: np.ndarray,
        labels_cal: np.ndarray,
    ) -> "ConformalClusterer":
        """
        Fit cluster prototypes on discovery set and calibrate non-conformity on calibration set.

        Parameters
        ----------
        X_disc : np.ndarray of shape (N_disc, D)
            Feature embeddings for discovery / training.
        labels_disc : np.ndarray of shape (N_disc,)
            Cluster labels on discovery set.
        X_cal : np.ndarray of shape (N_cal, D)
            Feature embeddings for conformal calibration.
        labels_cal : np.ndarray of shape (N_cal,)
            Target cluster labels on calibration set.

        Returns
        -------
        self : ConformalClusterer
        """
        unique_labels = np.unique(labels_disc)
        self.n_clusters_ = len(unique_labels)
        D = X_disc.shape[1]

        # Calculate unit-normalized cluster centroids
        self.centroids_ = np.zeros((self.n_clusters_, D))
        for k in range(self.n_clusters_):
            mask = (labels_disc == unique_labels[k])
            if np.any(mask):
                c = np.mean(X_disc[mask], axis=0)
                norm_c = np.linalg.norm(c)
                self.centroids_[k] = c / (norm_c if norm_c > 0 else 1.0)

        # Compute posterior probabilities on calibration set
        cos_sim = np.clip(X_cal @ self.centroids_.T, -1.0, 1.0)
        logits = cos_sim * self.temperature
        exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))
        probs_cal = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)

        # Non-conformity scores: s_i = 1 - P(y_true | x_i)
        N_cal = len(labels_cal)
        self.cal_scores_ = np.zeros(N_cal)
        for i in range(N_cal):
            c_true = int(labels_cal[i])
            self.cal_scores_[i] = 1.0 - probs_cal[i, c_true]

        # Finite-sample conformal quantile: ceil((N_cal + 1) * (1 - alpha)) / N_cal
        q_level = min(1.0, np.ceil((N_cal + 1) * (1.0 - self.alpha)) / N_cal)
        self.q_hat_ = float(np.quantile(self.cal_scores_, q_level, method="higher"))

        return self

    def predict(
        self,
        X_test: np.ndarray,
        y_test: Optional[np.ndarray] = None,
    ) -> ConformalResult:
        """
        Compute conformal prediction sets and uncertainty metrics for unseen instances.

        Parameters
        ----------
        X_test : np.ndarray of shape (N_test, D)
            Query feature embeddings.
        y_test : Optional[np.ndarray] of shape (N_test,)
            Ground truth or consensus labels, if available for coverage evaluation.

        Returns
        -------
        result : ConformalResult
        """
        if self.centroids_ is None or self.q_hat_ is None:
            raise RuntimeError("Model must be calibrated with fit_calibrate() first.")

        # Unit-normalize test samples if not already normalized
        norms = np.linalg.norm(X_test, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        X_norm = X_test / norms

        if self.centroids_ is None or self.n_clusters_ is None or self.q_hat_ is None:
            raise RuntimeError("Calibrator must be fitted before predicting.")

        cos_sim = np.clip(X_norm @ self.centroids_.T, -1.0, 1.0)
        logits = cos_sim * self.temperature
        exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))
        probs = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)

        N_test = X_test.shape[0]
        prediction_sets: List[List[int]] = []
        for i in range(N_test):
            included = [k for k in range(self.n_clusters_) if (1.0 - probs[i, k]) <= self.q_hat_]
            prediction_sets.append(included)

        set_sizes = np.array([len(s) for s in prediction_sets], dtype=int)
        is_singleton = (set_sizes == 1)
        is_ambiguous = (set_sizes > 1)
        is_abstention = (set_sizes == 0)

        empirical_cov = None
        if y_test is not None:
            covered = [int(y_test[i]) in prediction_sets[i] for i in range(N_test)]
            empirical_cov = float(np.mean(covered))

        return ConformalResult(
            prediction_sets=prediction_sets,
            probabilities=probs,
            set_sizes=set_sizes,
            is_singleton=is_singleton,
            is_ambiguous=is_ambiguous,
            is_abstention=is_abstention,
            empirical_coverage=empirical_cov,
            average_set_size=float(np.mean(set_sizes)),
        )
