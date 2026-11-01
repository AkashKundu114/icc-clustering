"""
Base interfaces, protocols, and validation for clustering algorithms.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import numpy as np


@dataclass
class AlgorithmMetadata:
    """Standard metadata container returned alongside clustering results."""

    name: str
    category: str
    n_clusters: int
    n_samples: int
    n_features: int
    runtime_seconds: float
    converged: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


def validate_clustering_input(
    X: np.ndarray,
    k: Optional[int] = None,
    min_samples: int = 2,
    min_features: int = 1,
) -> np.ndarray:
    """
    Validate input data matrix and target cluster count.

    Parameters
    ----------
    X : array-like of shape (N, D)
        Input features.
    k : int, optional
        Target number of clusters. Must be >= 2 and <= N.
    min_samples : int, default=2
        Minimum allowed samples.
    min_features : int, default=1
        Minimum allowed features.

    Returns
    -------
    np.ndarray
        Validated contiguous 2D float64 array.

    Raises
    ------
    ValueError
        If dimensions, sample count, or cluster count are invalid.
    """
    X_arr = np.asarray(X, dtype=np.float64)
    if X_arr.ndim != 2:
        raise ValueError(f"Input X must be 2D array, got ndim={X_arr.ndim}")

    n_samples, n_features = X_arr.shape
    if n_samples < min_samples:
        raise ValueError(f"n_samples={n_samples} is less than required minimum {min_samples}")
    if n_features < min_features:
        raise ValueError(f"n_features={n_features} is less than required minimum {min_features}")

    if np.isnan(X_arr).any():
        raise ValueError("Input data contains NaN values.")
    if np.isinf(X_arr).any():
        raise ValueError("Input data contains infinite values.")

    if k is not None:
        if not isinstance(k, (int, np.integer)):
            raise TypeError(f"Target cluster count k must be an integer, got {type(k)}")
        if k < 2:
            raise ValueError(f"Target cluster count k={k} must be >= 2.")
        if k > n_samples:
            raise ValueError(f"Target cluster count k={k} cannot exceed sample size N={n_samples}.")

    return np.ascontiguousarray(X_arr)


class BaseClusterer(ABC):
    """Abstract base class for all clustering algorithms in ICC."""

    def __init__(self, n_clusters: int = 3, random_state: Optional[int] = None):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.labels_: Optional[np.ndarray] = None
        self.metadata_: Optional[AlgorithmMetadata] = None

    @abstractmethod
    def fit(self, X: np.ndarray) -> "BaseClusterer":
        """Fit clustering model on data matrix X."""
        pass

    def fit_predict(self, X: np.ndarray) -> np.ndarray:
        """Fit and return cluster assignments."""
        self.fit(X)
        assert self.labels_ is not None
        return self.labels_
