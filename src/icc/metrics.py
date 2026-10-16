"""
Comprehensive clustering evaluation module for Invariant Core Consensus (ICC).

Provides dual-backend implementations (scikit-learn preferred, pure NumPy/SciPy fallback)
for external cluster validation metrics:
- Adjusted Rand Index (ARI)
- Normalized Mutual Information (NMI)
- Adjusted Mutual Information (AMI)
- V-Measure (harmonic mean of homogeneity and completeness)
- Fowlkes-Mallows Index (FM Index)
- Composite evaluators with bootstrap confidence intervals
"""

from typing import Dict

import numpy as np

try:
    import sklearn.metrics as _skm

    _sk_ari = _skm.adjusted_rand_score
    _sk_nmi = _skm.normalized_mutual_info_score
    _sk_ami = _skm.adjusted_mutual_info_score
    _sk_v_measure = _skm.v_measure_score
    _sk_fm = _skm.fowlkes_mallows_score
    _test = _sk_ari([0, 1], [0, 1])
    _SKLEARN_AVAILABLE = True
except (ImportError, Exception):
    _sk_ari = None
    _sk_nmi = None
    _sk_ami = None
    _sk_v_measure = None
    _sk_fm = None
    _SKLEARN_AVAILABLE = False

try:
    from scipy.stats import hypergeom as _sp_hypergeom

    _SCIPY_HYPERGEOM_AVAILABLE = True
except (ImportError, Exception):
    _SCIPY_HYPERGEOM_AVAILABLE = False


def adjusted_rand_score(labels_true: np.ndarray, labels_pred: np.ndarray) -> float:
    """
    Computes Adjusted Rand Index (ARI) between ground-truth and predicted labels.

    Mathematical Definition:
        Let U = {u_1, ..., u_R} and V = {v_1, ..., v_C} be two clusterings of N points.
        Let n_{ij} = |u_i ∩ v_j|, a_i = ∑_j n_{ij}, b_j = ∑_i n_{ij}.

        ARI = [ ∑_{ij} C(n_{ij}, 2) - E[Index] ] / [ 1/2 (∑_i C(a_i, 2) + ∑_j C(b_j, 2)) - E[Index] ]
        where E[Index] = [ ∑_i C(a_i, 2) ∑_j C(b_j, 2) ] / C(N, 2)
        and C(n, 2) = n(n - 1) / 2.

    Range:
        [-0.5, 1.0]. 1.0 represents identical clusterings up to permutation;
        0.0 corresponds to chance assignment according to the generalized hypergeometric model.
    """
    if _SKLEARN_AVAILABLE and _sk_ari is not None:
        return float(_sk_ari(labels_true, labels_pred))

    labels_true = np.asarray(labels_true)
    labels_pred = np.asarray(labels_pred)
    n = len(labels_true)
    if n <= 1:
        return 1.0

    classes, class_idx = np.unique(labels_true, return_inverse=True)
    clusters, cluster_idx = np.unique(labels_pred, return_inverse=True)
    contingency = np.zeros((len(classes), len(clusters)), dtype=np.int64)
    np.add.at(contingency, (class_idx, cluster_idx), 1)

    sum_comb_c = np.sum(contingency * (contingency - 1) // 2)
    a = contingency.sum(axis=1)
    b = contingency.sum(axis=0)
    sum_comb_a = np.sum(a * (a - 1) // 2)
    sum_comb_b = np.sum(b * (b - 1) // 2)
    total_comb = n * (n - 1) // 2

    expected = (sum_comb_a * sum_comb_b) / total_comb
    max_idx = (sum_comb_a + sum_comb_b) / 2.0
    denom = max_idx - expected
    return 1.0 if denom == 0 else float((sum_comb_c - expected) / denom)


def normalized_mutual_info_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Computes Normalized Mutual Information (NMI) using arithmetic mean normalization.

    Mathematical Definition:
        Let H(U) = - ∑_i P(u_i) log P(u_i) and H(V) = - ∑_j P(v_j) log P(v_j).
        Let I(U; V) = ∑_{ij} P(u_i, v_j) log [ P(u_i, v_j) / (P(u_i) P(v_j)) ].

        NMI(U, V) = 2 * I(U; V) / [ H(U) + H(V) ]

    Range:
        [0.0, 1.0]. 1.0 denotes perfect information concordance; 0.0 indicates statistical independence.
    """
    if _SKLEARN_AVAILABLE and _sk_nmi is not None:
        return float(_sk_nmi(y_true, y_pred))

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    n = len(y_true)
    if n <= 1:
        return 1.0

    classes, c_idx = np.unique(y_true, return_inverse=True)
    clusters, cl_idx = np.unique(y_pred, return_inverse=True)
    contingency = np.zeros((len(classes), len(clusters)), dtype=np.float64)
    np.add.at(contingency, (c_idx, cl_idx), 1.0)

    p_ij = contingency / n
    p_i = p_ij.sum(axis=1)
    p_j = p_ij.sum(axis=0)

    h_u = -np.sum(p_i * np.log(p_i + 1e-12))
    h_v = -np.sum(p_j * np.log(p_j + 1e-12))

    denom = np.outer(p_i, p_j)
    mask = p_ij > 0
    mi = np.sum(p_ij[mask] * np.log(p_ij[mask] / (denom[mask] + 1e-12)))

    if h_u + h_v == 0:
        return 1.0
    val = float(2.0 * mi / (h_u + h_v))
    if abs(val) < 1e-10:
        return 0.0
    return float(np.clip(val, 0.0, 1.0))


def adjusted_mutual_info_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Computes Adjusted Mutual Information (AMI) under the generalized hypergeometric model.

    Mathematical Definition:
        AMI(U, V) = [ I(U; V) - E[I(U; V)] ] / [ (H(U) + H(V)) / 2 - E[I(U; V)] ]

        where E[I(U; V)] is the expected mutual information between two random clusterings
        with fixed marginal cluster sizes (Vinh et al., 2010):
        E[I] = ∑_{i=1}^R ∑_{j=1}^C ∑_{n_{ij}} (n_{ij}/N) log( (N n_{ij}) / (a_i b_j) ) P(n_{ij})
        with P(n_{ij}) being Hypergeometric(N, a_i, b_j).

    Range:
        [-0.5, 1.0]. 1.0 indicates perfect agreement; 0.0 corresponds to expected chance overlap.
    """
    if _SKLEARN_AVAILABLE and _sk_ami is not None:
        return float(_sk_ami(y_true, y_pred))

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    n = len(y_true)
    if n <= 1:
        return 1.0

    classes, c_idx = np.unique(y_true, return_inverse=True)
    clusters, cl_idx = np.unique(y_pred, return_inverse=True)
    R, C = len(classes), len(clusters)
    contingency = np.zeros((R, C), dtype=np.int64)
    np.add.at(contingency, (c_idx, cl_idx), 1)

    a = contingency.sum(axis=1)
    b = contingency.sum(axis=0)

    p_ij = contingency.astype(np.float64) / n
    p_i = a.astype(np.float64) / n
    p_j = b.astype(np.float64) / n

    h_u = -np.sum(p_i * np.log(p_i + 1e-12))
    h_v = -np.sum(p_j * np.log(p_j + 1e-12))

    denom = np.outer(p_i, p_j)
    mask = p_ij > 0
    mi = np.sum(p_ij[mask] * np.log(p_ij[mask] / (denom[mask] + 1e-12)))

    emi = 0.0
    if _SCIPY_HYPERGEOM_AVAILABLE:
        for i in range(R):
            for j in range(C):
                ai, bj = int(a[i]), int(b[j])
                nij_min = max(1, ai + bj - n)
                nij_max = min(ai, bj)
                for nij in range(nij_min, nij_max + 1):
                    p = _sp_hypergeom.pmf(nij, n, ai, bj)
                    if p > 0:
                        emi += (nij / n) * np.log((n * nij) / (ai * bj)) * p
    else:
        emi = max(0.0, float((R - 1) * (C - 1)) / (2.0 * n))

    mean_h = (h_u + h_v) / 2.0
    denom_adj = mean_h - emi
    if denom_adj <= 0:
        return 1.0
    val = float((mi - emi) / denom_adj)
    if abs(val) < 1e-10:
        return 0.0
    return val


def v_measure_score(y_true: np.ndarray, y_pred: np.ndarray, beta: float = 1.0) -> float:
    """
    Computes V-Measure score (Rosenberg & Hirschberg, 2007).
    Harmonic mean of homogeneity (h) and completeness (c) weighted by beta.

    Mathematical Definition:
        h = 1 - H(C | K) / H(C) = I(C; K) / H(C)
        c = 1 - H(K | C) / H(K) = I(C; K) / H(K)

        V_beta = (1 + beta) * h * c / (beta * h + c)

    Range:
        [0.0, 1.0]. 1.0 represents clusters that are both fully homogeneous and complete.
    """
    if _SKLEARN_AVAILABLE and _sk_v_measure is not None:
        return float(_sk_v_measure(y_true, y_pred, beta=beta))

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    n = len(y_true)
    if n <= 1:
        return 1.0

    classes, c_idx = np.unique(y_true, return_inverse=True)
    clusters, cl_idx = np.unique(y_pred, return_inverse=True)
    contingency = np.zeros((len(classes), len(clusters)), dtype=np.float64)
    np.add.at(contingency, (c_idx, cl_idx), 1.0)

    p_ij = contingency / n
    p_i = p_ij.sum(axis=1)
    p_j = p_ij.sum(axis=0)

    h_u = -np.sum(p_i * np.log(p_i + 1e-12))
    h_v = -np.sum(p_j * np.log(p_j + 1e-12))

    denom = np.outer(p_i, p_j)
    mask = p_ij > 0
    mi = np.sum(p_ij[mask] * np.log(p_ij[mask] / (denom[mask] + 1e-12)))

    homogeneity = (mi / h_u) if h_u > 0 else 1.0
    completeness = (mi / h_v) if h_v > 0 else 1.0

    if homogeneity + completeness == 0.0:
        return 0.0
    val = float((1.0 + beta) * homogeneity * completeness / (beta * homogeneity + completeness))
    if abs(val) < 1e-10:
        return 0.0
    return float(np.clip(val, 0.0, 1.0))


def fowlkes_mallows_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Computes Fowlkes-Mallows Index (FM Index; Fowlkes & Mallows, 1983).
    Geometric mean of pairwise precision and recall between two clusterings.

    Mathematical Definition:
        FM = TP / sqrt( (TP + FP) * (TP + FN) )
           = ∑_{ij} C(n_{ij}, 2) / sqrt( [∑_i C(a_i, 2)] * [∑_j C(b_j, 2)] )

    Range:
        [0.0, 1.0]. 1.0 indicates identical clusterings; 0.0 indicates no pairwise overlap.
    """
    if _SKLEARN_AVAILABLE and _sk_fm is not None:
        return float(_sk_fm(y_true, y_pred))

    labels_true = np.asarray(y_true)
    labels_pred = np.asarray(y_pred)
    n = len(labels_true)
    if n <= 1:
        return 1.0

    classes, class_idx = np.unique(labels_true, return_inverse=True)
    clusters, cluster_idx = np.unique(labels_pred, return_inverse=True)
    contingency = np.zeros((len(classes), len(clusters)), dtype=np.int64)
    np.add.at(contingency, (class_idx, cluster_idx), 1)

    sum_comb_c = np.sum(contingency * (contingency - 1) // 2)
    a = contingency.sum(axis=1)
    b = contingency.sum(axis=0)
    sum_comb_a = np.sum(a * (a - 1) // 2)
    sum_comb_b = np.sum(b * (b - 1) // 2)

    if sum_comb_a == 0 or sum_comb_b == 0:
        return 0.0

    return float(sum_comb_c / np.sqrt(float(sum_comb_a) * float(sum_comb_b)))


def evaluate_all(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Computes all 5 standard external clustering metrics in a single pass.

    Returns:
        dict: Keys {"ari", "nmi", "ami", "v_measure", "fm_index"}.
    """
    return {
        "ari": adjusted_rand_score(y_true, y_pred),
        "nmi": normalized_mutual_info_score(y_true, y_pred),
        "ami": adjusted_mutual_info_score(y_true, y_pred),
        "v_measure": v_measure_score(y_true, y_pred),
        "fm_index": fowlkes_mallows_score(y_true, y_pred),
    }


def evaluate_all_with_ci(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    n_bootstrap: int = 1000,
    alpha: float = 0.05,
    random_seed: int = 42,
) -> Dict[str, Dict[str, float]]:
    """
    Computes all clustering metrics with empirical bootstrap confidence intervals.

    Args:
        y_true: Ground truth cluster assignments.
        y_pred: Predicted cluster assignments.
        n_bootstrap: Number of bootstrap resamples (default: 1000).
        alpha: Two-tailed significance level (default: 0.05 for 95% CI).
        random_seed: RNG seed for reproducible sampling.

    Returns:
        dict: Mapping each metric name to {"mean": float, "ci_low": float, "ci_high": float}.
    """
    rng = np.random.default_rng(random_seed)
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    n = len(y_true)

    base_scores = evaluate_all(y_true, y_pred)
    bootstraps = {m: np.empty(n_bootstrap, dtype=np.float64) for m in base_scores}

    for b in range(n_bootstrap):
        idx = rng.choice(n, size=n, replace=True)
        yt_boot = y_true[idx]
        yp_boot = y_pred[idx]
        bootstraps["ari"][b] = adjusted_rand_score(yt_boot, yp_boot)
        bootstraps["nmi"][b] = normalized_mutual_info_score(yt_boot, yp_boot)
        bootstraps["ami"][b] = adjusted_mutual_info_score(yt_boot, yp_boot)
        bootstraps["v_measure"][b] = v_measure_score(yt_boot, yp_boot)
        bootstraps["fm_index"][b] = fowlkes_mallows_score(yt_boot, yp_boot)

    lower_pct = (alpha / 2.0) * 100.0
    upper_pct = (1.0 - alpha / 2.0) * 100.0

    results = {}
    for metric, base_val in base_scores.items():
        arr = bootstraps[metric]
        results[metric] = {
            "mean": float(base_val),
            "ci_low": float(np.percentile(arr, lower_pct)),
            "ci_high": float(np.percentile(arr, upper_pct)),
        }

    return results
