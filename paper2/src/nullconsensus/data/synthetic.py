"""
Synthetic benchmark generator for controlled failure mode evaluations.
"""

import numpy as np
from typing import Tuple

def make_gaussian_distractor(
    n_samples: int = 150,
    n_features: int = 500,
    n_informative: int = 15,
    n_clusters: int = 3,
    separation: float = 3.0,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates localized Gaussian clusters embedded in isotropic Gaussian noise.
    """
    rng = np.random.default_rng(random_state)
    X = rng.standard_normal((n_samples, n_features))
    y = np.zeros(n_samples, dtype=int)
    
    samples_per_cluster = n_samples // n_clusters
    for k in range(n_clusters):
        start = k * samples_per_cluster
        end = (k + 1) * samples_per_cluster if k < n_clusters - 1 else n_samples
        y[start:end] = k
        if k > 0:
            # Shift informative coordinates
            shift = (k - (n_clusters - 1) / 2.0) * separation
            X[start:end, :n_informative] += shift
            
    return X, y

def make_xor_parity(
    n_samples: int = 400,
    n_distractors: int = 400,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates non-linear 2D XOR interaction with isotropic distractor noise.
    Marginals on features 0 and 1 are identical standard Gaussians across classes.
    """
    rng = np.random.default_rng(random_state)
    n_sub = n_samples // 4
    
    # Four quadrants
    q1 = rng.standard_normal((n_sub, 2)) + np.array([2.0, 2.0])   # Class 0
    q2 = rng.standard_normal((n_sub, 2)) + np.array([-2.0, -2.0]) # Class 0
    q3 = rng.standard_normal((n_sub, 2)) + np.array([2.0, -2.0])  # Class 1
    q4 = rng.standard_normal((n_sub, 2)) + np.array([-2.0, 2.0])  # Class 1
    
    X_info = np.vstack([q1, q2, q3, q4])
    y = np.array([0] * (2 * n_sub) + [1] * (2 * n_sub))
    
    # Distractors
    X_noise = rng.standard_normal((len(y), n_distractors))
    X = np.hstack([X_info, X_noise])
    
    # Shuffle order
    perm = rng.permutation(len(y))
    return X[perm], y[perm]

def make_zero_inflated_counts(
    n_samples: int = 300,
    n_features: int = 500,
    n_informative: int = 20,
    n_clusters: int = 3,
    dropout_rate: float = 0.70,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates zero-inflated count data mimicking single-cell RNA-seq dropouts.
    """
    rng = np.random.default_rng(random_state)
    y = np.zeros(n_samples, dtype=int)
    X = np.zeros((n_samples, n_features))
    
    samples_per_cluster = n_samples // n_clusters
    for k in range(n_clusters):
        start = k * samples_per_cluster
        end = (k + 1) * samples_per_cluster if k < n_clusters - 1 else n_samples
        y[start:end] = k
        # Base Poisson expression
        lambda_val = 2.0 + (k + 1) * 3.0
        X[start:end, :n_informative] = rng.poisson(lambda_val, size=(end - start, n_informative))
        # Uninformative background Poisson
        X[start:end, n_informative:] = rng.poisson(1.5, size=(end - start, n_features - n_informative))

    # Apply dropout mask
    mask = rng.uniform(0, 1, size=X.shape) < dropout_rate
    X[mask] = 0.0
    
    return X, y
