"""
Experiment 0: Core Building Blocks for High-Dimensional Stability Testing.

Features:
- Parametric synthetic benchmark generator with signal manifold + 5 nuisance noise regimes
- Support for balanced and imbalanced cluster size distributions (e.g. ALLAML N=72, 47 vs 25)
- Standardized clusterer wrappers: KMeans, GMM, Ward, Spectral, FCM
- Resilient dual-backend architecture: prefers scikit-learn, with automated seamless
  fallback to high-performance NumPy/SciPy if scikit-learn C-extensions are blocked or unavailable
- Canonical partition encoding and co-association matrix calculation
"""

import numpy as np
import scipy.cluster.hierarchy as sch
import scipy.linalg as sla
from scipy.spatial.distance import cdist

# Try importing sklearn; fallback if DLLs or modules are blocked
_SKLEARN_AVAILABLE = False
try:
    from sklearn.cluster import KMeans as _SkKMeans
    from sklearn.cluster import AgglomerativeClustering as _SkAgg
    from sklearn.cluster import SpectralClustering as _SkSpectral
    from sklearn.mixture import GaussianMixture as _SkGMM
    from sklearn.metrics import adjusted_rand_score as _sk_ari
    # Test if underlying cython modules load without policy blocks
    _test = _sk_ari([0, 1], [0, 1])
    _SKLEARN_AVAILABLE = True
except (ImportError, Exception):
    _SKLEARN_AVAILABLE = False
# Metrics re-exported from .metrics for backward compatibility
from .metrics import (
    adjusted_rand_score,
    normalized_mutual_info_score,
    adjusted_mutual_info_score,
    v_measure_score,
    fowlkes_mallows_score,
    evaluate_all,
    evaluate_all_with_ci,
)

RNG_DATA_SEED = 42
CLUSTERERS = ["kmeans", "gmm", "ward", "spectral", "fcm"]


def make_signal(n_per_cluster=100, k=3, signal_dim=2, seed=RNG_DATA_SEED, sizes=None):
    """
    Generates well-separated Gaussian clusters in `signal_dim` space.
    Supports either balanced sizes (n_per_cluster * k) or explicit `sizes` list.
    """
    rng = np.random.default_rng(seed)
    if sizes is None:
        sizes = [n_per_cluster] * k
    else:
        sizes = list(sizes)
        k = len(sizes)

    centers = rng.normal(scale=6.0, size=(k, signal_dim))
    # Enforce minimum separation margin
    while True:
        d = np.linalg.norm(centers[:, None, :] - centers[None, :, :], axis=-1)
        np.fill_diagonal(d, np.inf)
        if d.min() > 8.0:
            break
        centers = rng.normal(scale=6.0, size=(k, signal_dim))

    S, y = [], []
    for c, n_c in enumerate(sizes):
        pts = centers[c] + rng.normal(scale=1.0, size=(n_c, signal_dim))
        S.append(pts)
        y.append(np.full(n_c, c, dtype=int))

    return np.vstack(S), np.concatenate(y)


def make_noise(n, d_noise, kind="gaussian", seed=0):
    """
    Generates nuisance dimensions independent of cluster identity across 5 noise regimes:
    - 'gaussian': pure isotropic white noise N(0, I)
    - 'student_t': heavy-tailed Student-t (df=3)
    - 'correlated': low-rank latent factor passenger pathways
    - 'scaled': heteroscedastic noise with feature variances spanning two orders of magnitude
    - 'sparse': zero-inflated noise with sparse bursts
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
            out[:, b * block:(b + 1) * block] = 0.7 * factor + 0.3 * rng.normal(size=(n, block))
        return out[:, :d_noise]

    if kind == "scaled":
        sigmas = rng.uniform(0.1, 10.0, size=d_noise)
        return rng.normal(size=(n, d_noise)) * sigmas

    if kind == "sparse":
        base = np.zeros((n, d_noise))
        mask = rng.random((n, d_noise)) < 0.05
        base[mask] = rng.normal(scale=8.0, size=mask.sum())
        return base

    raise ValueError(f"Unknown noise kind: {kind}")


def build_dataset(d_noise, noise_kind="gaussian", noise_seed=0,
                   n_per_cluster=100, k=3, signal_dim=2, sizes=None):
    """Constructs dataset X = [S, N] and labels y with Z-score column standardization."""
    S, y = make_signal(n_per_cluster=n_per_cluster, k=k, signal_dim=signal_dim, sizes=sizes)
    N = make_noise(S.shape[0], d_noise, kind=noise_kind, seed=noise_seed)
    X = np.hstack([S, N]) if d_noise > 0 else S

    # Standardize column-wise
    std = np.std(X, axis=0)
    std[std < 1e-12] = 1.0
    X = (X - np.mean(X, axis=0)) / std
    return X, y


def _fcm_like(X, k, seed, m=2.0, n_iter=100, tol=1e-5):
    """Lightweight vector-accelerated Fuzzy C-Means (Bezdek update rules)."""
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    u = rng.dirichlet(np.ones(k), size=n)
    for _ in range(n_iter):
        um = u ** m
        denom = um.sum(axis=0)[:, None]
        denom[denom < 1e-12] = 1e-12
        centers = (um.T @ X) / denom
        d2 = cdist(X, centers, metric="sqeuclidean")
        d2 = np.fmax(d2, 1e-12)
        inv = d2 ** (-1.0 / (m - 1))
        inv_sum = inv.sum(axis=1, keepdims=True)
        inv_sum[inv_sum < 1e-12] = 1e-12
        u_new = inv / inv_sum
        if np.max(np.abs(u_new - u)) < tol:
            u = u_new
            break
        u = u_new
    return np.argmax(u, axis=1)


def _kmeans_numpy(X, k, seed=0, max_iter=100):
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    idx = rng.choice(n, size=k, replace=False)
    centers = X[idx].copy()
    labels = np.zeros(n, dtype=int)
    for _ in range(max_iter):
        dists = cdist(X, centers, metric='sqeuclidean')
        new_labels = np.argmin(dists, axis=1)
        if np.array_equal(labels, new_labels):
            break
        labels = new_labels
        for c in range(k):
            mask = (labels == c)
            if np.any(mask):
                centers[c] = X[mask].mean(axis=0)
    return labels


def _gmm_numpy(X, k, seed=0, max_iter=40, reg_covar=1e-4):
    rng = np.random.default_rng(seed)
    n, d = X.shape
    # Initialize with kmeans
    init_labels = _kmeans_numpy(X, k, seed=seed)
    weights = np.ones(k) / k
    means = np.array([X[init_labels == c].mean(axis=0) if np.any(init_labels == c) else X[c] for c in range(k)])
    vars_ = np.array([X[init_labels == c].var(axis=0) + reg_covar if np.any(init_labels == c) else np.ones(d) for c in range(k)])

    for _ in range(max_iter):
        # E-step
        log_resp = np.zeros((n, k))
        for c in range(k):
            var_c = vars_[c]
            diff = X - means[c]
            log_prob = -0.5 * (np.sum(np.log(var_c)) + np.sum((diff ** 2) / var_c, axis=1) + d * np.log(2 * np.pi))
            log_resp[:, c] = np.log(weights[c] + 1e-12) + log_prob
        max_log = np.max(log_resp, axis=1, keepdims=True)
        resp = np.exp(log_resp - max_log)
        resp /= resp.sum(axis=1, keepdims=True)

        # M-step
        Nk = resp.sum(axis=0) + 1e-12
        weights = Nk / n
        means = (resp.T @ X) / Nk[:, None]
        for c in range(k):
            diff = X - means[c]
            vars_[c] = (resp[:, c] @ (diff ** 2)) / Nk[c] + reg_covar

    return np.argmax(resp, axis=1)


def _spectral_scipy(X, k, seed=0, n_neighbors=10):
    dists = cdist(X, X, metric='sqeuclidean')
    n = X.shape[0]
    W = np.zeros((n, n))
    for i in range(n):
        nn_idx = np.argsort(dists[i])[:n_neighbors + 1]
        W[i, nn_idx] = 1.0
        W[nn_idx, i] = 1.0
    deg = W.sum(axis=1)
    deg_inv_sqrt = 1.0 / np.sqrt(np.fmax(deg, 1e-12))
    L_norm = np.eye(n) - (deg_inv_sqrt[:, None] * W * deg_inv_sqrt[None, :])
    evals, evecs = sla.eigh(L_norm)
    embedding = evecs[:, :k]
    emb_norm = np.linalg.norm(embedding, axis=1, keepdims=True)
    emb_norm[emb_norm < 1e-12] = 1.0
    embedding /= emb_norm
    return _kmeans_numpy(embedding, k, seed=seed)


def run_clusterer(name, X, k, seed):
    """Executes base clustering algorithm with seed control and dual-backend safety."""
    if _SKLEARN_AVAILABLE:
        try:
            if name == "kmeans":
                return _SkKMeans(n_clusters=k, init="random", n_init=1, random_state=seed).fit_predict(X)
            if name == "gmm":
                return _SkGMM(n_components=k, covariance_type="diag", random_state=seed, n_init=1, reg_covar=1e-4).fit_predict(X)
            if name == "ward":
                rng = np.random.default_rng(seed)
                jitter = rng.normal(scale=1e-4, size=X.shape)
                return _SkAgg(n_clusters=k, linkage="ward").fit_predict(X + jitter)
            if name == "spectral":
                return _SkSpectral(n_clusters=k, affinity="nearest_neighbors", n_neighbors=10, random_state=seed, assign_labels="kmeans").fit_predict(X)
            if name == "fcm":
                return _fcm_like(X, k, seed)
        except Exception:
            pass  # fallback below

    # Fallback NumPy/SciPy engine
    if name == "kmeans":
        return _kmeans_numpy(X, k, seed=seed)
    if name == "gmm":
        return _gmm_numpy(X, k, seed=seed)
    if name == "ward":
        rng = np.random.default_rng(seed)
        jitter = rng.normal(scale=1e-4, size=X.shape)
        Z = sch.linkage(X + jitter, method="ward")
        return sch.fcluster(Z, t=k, criterion="maxclust") - 1
    if name == "spectral":
        return _spectral_scipy(X, k, seed=seed)
    if name == "fcm":
        return _fcm_like(X, k, seed)

    raise ValueError(f"Unknown clusterer: {name}")


def pairwise_coassoc(labelings):
    """Computes sample-by-sample consensus co-association matrix in [0, 1]."""
    n = len(labelings[0])
    S = np.zeros((n, n), dtype=float)
    for lab in labelings:
        S += (lab[:, None] == lab[None, :]).astype(float)
    S /= len(labelings)
    return S


def canonical(labels):
    """
    Maps cluster labels to a canonical tuple invariant to index permutation.
    Ensures identical partitions with different cluster IDs map to the same hashable key.
    """
    mapping = {}
    canonical_labels = []
    for l in labels:
        if l not in mapping:
            mapping[l] = len(mapping)
        canonical_labels.append(mapping[l])
    return tuple(canonical_labels)
