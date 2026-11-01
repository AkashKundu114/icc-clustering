"""
Preprocessing and synthetic benchmark generation primitives.
"""

from typing import List, Optional, Tuple

import numpy as np
from scipy.stats import kurtosis, skew

RNG_DATA_SEED = 42


def inject_mcar_noise(X: np.ndarray, rho: float, seed: int = 42) -> np.ndarray:
    """
    Inject Missing Completely At Random (MCAR) NaN values with rate rho.

    Parameters
    ----------
    X : np.ndarray
        Data matrix.
    rho : float
        Fraction of entries to replace with NaN (0.0 to 1.0).
    seed : int, default=42
        Random seed.

    Returns
    -------
    np.ndarray
        Array with NaNs injected.
    """
    rng = np.random.default_rng(seed)
    X_nan = np.copy(X).astype(np.float64)
    mask = rng.uniform(0.0, 1.0, size=X.shape) < rho
    X_nan[mask] = np.nan
    return X_nan


def impute_data(X_nan: np.ndarray, strategy: str = "mean") -> np.ndarray:
    """
    Impute missing NaN values using SimpleImputer.

    Parameters
    ----------
    X_nan : np.ndarray
        Array containing NaN values.
    strategy : str, default="mean"
        Imputation strategy ("mean", "median").

    Returns
    -------
    np.ndarray
        Imputed data array.
    """
    from sklearn.impute import SimpleImputer

    strat = strategy.lower()
    if strat not in ("mean", "median", "most_frequent", "constant"):
        strat = "mean"
    imp = SimpleImputer(strategy=strat)
    return imp.fit_transform(X_nan)


def bimodality_coefficient(x: np.ndarray, finite_sample_correction: bool = True) -> float:
    """
    Calculates Sarle's Bimodality Coefficient (BC) for a 1D continuous array.

    BC = (gamma^2 + 1) / (kappa_excess + 3)

    Parameters
    ----------
    x : array-like of shape (N,)
        1D feature vector.
    finite_sample_correction : bool, default=True
        Apply finite-sample bias correction.

    Returns
    -------
    float
        BC value in [0, 1]. For normal distributions, BC ~ 0.333.
        For uniform distributions, BC = 5/9 (~0.555).
        Values > 5/9 indicate potential bimodality/multimodality.
    """
    x_arr = np.asarray(x, dtype=np.float64)
    n = len(x_arr)
    if n < 4:
        return 0.0

    if finite_sample_correction and n >= 4:
        s = float(skew(x_arr, bias=False))
        k = float(kurtosis(x_arr, fisher=True, bias=False))
        sample_penalty = 3.0 * ((n - 1) ** 2) / ((n - 2) * (n - 3))
    else:
        s = float(skew(x_arr))
        k = float(kurtosis(x_arr, fisher=True))
        sample_penalty = 3.0

    denom = k + sample_penalty
    if denom <= 0:
        return 1.0
    bc = (s**2 + 1.0) / denom
    return float(np.clip(bc, 0.0, 1.0))


def make_signal(
    n_per_cluster: int = 100,
    k: int = 3,
    signal_dim: int = 2,
    seed: int = RNG_DATA_SEED,
    sizes: Optional[List[int]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates well-separated Gaussian clusters in `signal_dim` space.
    """
    rng = np.random.default_rng(seed)
    if sizes is None:
        sizes = [n_per_cluster] * k
    else:
        sizes = list(sizes)
        k = len(sizes)

    centers = rng.normal(scale=6.0, size=(k, signal_dim))

    while True:
        d = np.linalg.norm(centers[:, None, :] - centers[None, :, :], axis=-1)
        np.fill_diagonal(d, np.inf)
        if np.min(d) > 8.0:
            break
        centers = rng.normal(scale=6.0, size=(k, signal_dim))

    S, y = [], []
    for c, n_c in enumerate(sizes):
        pts = centers[c] + rng.normal(scale=1.0, size=(n_c, signal_dim))
        S.append(pts)
        y.append(np.full(n_c, c, dtype=int))

    return np.vstack(S), np.concatenate(y)


def make_noise(n: int, d_noise: int, kind: str = "gaussian", seed: int = 0) -> np.ndarray:
    """
    Generates nuisance dimensions independent of cluster identity across 5 noise regimes.
    """
    rng = np.random.default_rng(seed)
    if d_noise == 0:
        return np.zeros((n, 0))

    if kind == "gaussian":
        return rng.normal(scale=1.0, size=(n, d_noise))

    if kind == "student_t":
        return rng.standard_t(df=3, size=(n, d_noise))

    if kind == "correlated":
        block = 20
        n_blocks = int(np.ceil(d_noise / block))
        out = np.zeros((n, n_blocks * block))
        for b in range(n_blocks):
            factor = rng.normal(size=(n, 1))
            out[:, b * block : (b + 1) * block] = 0.7 * factor + 0.3 * rng.normal(size=(n, block))
        return out[:, :d_noise]

    if kind == "scaled":
        sigmas = rng.uniform(0.1, 10.0, size=d_noise)
        return rng.normal(size=(n, d_noise)) * sigmas

    if kind == "sparse":
        mask = rng.binomial(1, 0.05, size=(n, d_noise))
        vals = rng.normal(scale=3.0, size=(n, d_noise))
        return mask * vals

    raise ValueError(f"Unknown noise kind: {kind}")


def build_dataset(
    n_per_cluster: int = 100,
    k: int = 3,
    signal_dim: int = 2,
    noise_dim: int = 0,
    noise_kind: str = "gaussian",
    seed: int = 0,
    sizes: Optional[List[int]] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Combines true cluster signal dimensions with uninformative nuisance noise dimensions.
    """
    S, y = make_signal(n_per_cluster, k, signal_dim, seed=RNG_DATA_SEED, sizes=sizes)
    n = len(y)
    if noise_dim > 0:
        E = make_noise(n, noise_dim, kind=noise_kind, seed=seed)
        X = np.hstack([S, E])
    else:
        X = S

    return X, y


def canonical(labels: np.ndarray) -> np.ndarray:
    """
    Maps cluster labels to canonical consecutive integers 0, 1, ..., K-1 in order of first appearance.
    """
    labels = np.asarray(labels)
    mapping = {}
    out = np.empty_like(labels)
    nxt = 0
    for i, lb in enumerate(labels):
        if lb not in mapping:
            mapping[lb] = nxt
            nxt += 1
        out[i] = mapping[lb]
    return out


def pairwise_coassoc(labels: np.ndarray) -> np.ndarray:
    """
    Computes exact binary co-association matrix in R^(N x N) where A_ij = 1 if labels[i] == labels[j].
    """
    labels = np.asarray(labels)
    return (labels[:, None] == labels[None, :]).astype(float)
