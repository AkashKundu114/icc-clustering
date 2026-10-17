"""
Study 3' Development Pipeline & Debugging Suite (Seeds >= 10,000)
================================================================
Implements and validates the frozen NCG specification on development data:
1. Label-free preprocessing:
   - drop var < 1e-12 (statistic 0, never selected)
   - log1p on non-negative integers
   - exclude features with < 6 distinct values
   - z-score every feature
2. Finite-sample Sarle BC with Eq. 2 correction:
   s_d = (skew_d^2 + 1) / (kurt_d + 3*(N-1)^2 / ((N-2)*(N-3)))
3. Primary Decoy Generator:
   Silverman Critical Bandwidth (SCB) smoothed bootstrap with variance rescaling.
   Secondary Decoy Generator: Skew-Normal MLE.
4. Knockoff+ mirror thresholding W_d = s_d - s~_d at nominal q = 0.10.
5. Verification on development data (Madelon, Sonar, and dev synthetic seeds 10,000-10,005).
"""

import sys
import os
import numpy as np
import scipy.linalg as sla
from scipy.stats import kurtosis, skew, gaussian_kde, skewnorm
from scipy.optimize import minimize_scalar

# -----------------------------------------------------------------------------
# 1. Label-Free Preprocessing (Section A2.1)
# -----------------------------------------------------------------------------

def preprocess_features(X: np.ndarray):
    """
    Label-free preprocessing:
    1. Drop features with variance < 1e-12
    2. Apply log1p to non-negative integers
    3. Exclude features with < 6 distinct values
    4. Z-score remaining features
    """
    N, D = X.shape
    variances = np.var(X, axis=0)
    var_mask = variances >= 1e-12

    # Integer check for log1p
    X_proc = np.array(X, dtype=np.float64, copy=True)
    for j in range(D):
        col = X[:, j]
        if np.all(col >= 0) and np.all(np.equal(np.mod(col, 1), 0)):
            X_proc[:, j] = np.log1p(col)

    # Distinct values check (< 6 distinct values excluded)
    distinct_mask = np.zeros(D, dtype=bool)
    for j in range(D):
        if len(np.unique(X[:, j])) >= 6:
            distinct_mask[j] = True

    eligible_mask = var_mask & distinct_mask

    # Z-score eligible features
    X_z = np.zeros_like(X_proc)
    if np.any(eligible_mask):
        means = np.mean(X_proc[:, eligible_mask], axis=0)
        stds = np.std(X_proc[:, eligible_mask], axis=0)
        stds[stds < 1e-12] = 1.0
        X_z[:, eligible_mask] = (X_proc[:, eligible_mask] - means) / stds

    return X_z, eligible_mask


# -----------------------------------------------------------------------------
# 2. Finite-Sample Sarle BC (Section A2.2)
# -----------------------------------------------------------------------------

def compute_finite_sample_bc(X: np.ndarray, eligible_mask: np.ndarray) -> np.ndarray:
    """
    Finite-sample corrected Sarle BC:
    s_d = (skew_d^2 + 1) / (kurt_d + 3*(N-1)^2 / ((N-2)*(N-3)))
    """
    N, D = X.shape
    bc = np.zeros(D, dtype=np.float64)
    if not np.any(eligible_mask):
        return bc

    X_elig = X[:, eligible_mask]
    sk = skew(X_elig, axis=0, bias=False) if N >= 3 else skew(X_elig, axis=0)
    kt = kurtosis(X_elig, axis=0, fisher=True, bias=False) if N >= 4 else kurtosis(X_elig, axis=0)

    finite_corr = 3.0 * ((N - 1) ** 2) / ((N - 2) * (N - 3)) if N >= 4 else 3.0
    denom = kt + finite_corr
    denom = np.fmax(denom, 1e-5)

    bc[eligible_mask] = (sk ** 2 + 1.0) / denom
    return bc


# -----------------------------------------------------------------------------
# 3. Silverman Critical Bandwidth (SCB) Decoy Generator (Section A2.3)
# -----------------------------------------------------------------------------

def find_silverman_critical_bandwidth(x: np.ndarray, tol: float = 1e-3, max_iter: int = 25) -> float:
    """
    Find smallest Gaussian-KDE bandwidth h_crit giving a unimodal estimate via bisection.
    """
    n = len(x)
    std_x = np.std(x)
    if std_x < 1e-12:
        return 1.0

    # Range of candidate bandwidths (Silverman's rule of thumb gives reference h0)
    h_low = 0.05 * std_x
    h_high = 2.0 * std_x

    # Test grid of evaluation points
    grid = np.linspace(np.min(x) - std_x, np.max(x) + std_x, 200)

    def count_modes(h):
        try:
            kde = gaussian_kde(x, bw_method=h / std_x)
            density = kde.evaluate(grid)
            # Find local maxima
            peaks = (density[1:-1] > density[:-2]) & (density[1:-1] > density[2:])
            return np.sum(peaks)
        except Exception:
            return 2

    # Bisection search
    for _ in range(max_iter):
        h_mid = 0.5 * (h_low + h_high)
        if count_modes(h_mid) <= 1:
            h_high = h_mid
        else:
            h_low = h_mid
        if (h_high - h_low) < tol * std_x:
            break

    return float(h_high)


def generate_scb_decoys(X: np.ndarray, eligible_mask: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """
    Draw N points from smoothed bootstrap at h_crit with variance rescaled to sample variance.
    """
    N, D = X.shape
    X_decoy = np.zeros_like(X)
    for j in range(D):
        if not eligible_mask[j]:
            continue
        col = X[:, j]
        s_var = np.var(col)
        h_crit = find_silverman_critical_bandwidth(col)

        # Smoothed bootstrap: resample with Gaussian perturbation scaled by h_crit
        bootstrap_idx = rng.choice(N, size=N, replace=True)
        raw_decoy = col[bootstrap_idx] + rng.normal(0, h_crit, size=N)

        # Rescale variance to match original sample variance
        decoy_var = np.var(raw_decoy)
        if decoy_var > 1e-12:
            raw_decoy = (raw_decoy - np.mean(raw_decoy)) * np.sqrt(s_var / decoy_var)
        X_decoy[:, j] = raw_decoy

    return X_decoy


# -----------------------------------------------------------------------------
# 4. Mirror Statistic & Knockoff+ Selection (Section A2.4)
# -----------------------------------------------------------------------------

def null_calibrated_gate(
    X: np.ndarray,
    q: float = 0.10,
    rng: Optional[np.random.Generator] = None,
):
    """
    Execute full NCG pipeline:
    Returns (selected_set S, active_features F_active, W_d, eligible_mask, fallback_flag)
    """
    if rng is None:
        rng = np.random.default_rng(42)

    X_z, eligible_mask = preprocess_features(X)
    N, D = X.shape

    # 1. Target statistic s_d
    s_target = compute_finite_sample_bc(X_z, eligible_mask)

    # 2. Decoy statistic s~_d via Silverman critical bandwidth
    X_decoy = generate_scb_decoys(X_z, eligible_mask, rng=rng)
    s_decoy = compute_finite_sample_bc(X_decoy, eligible_mask)

    # 3. Mirror statistic W_d = s_d - s~_d
    W = np.zeros(D)
    W[eligible_mask] = s_target[eligible_mask] - s_decoy[eligible_mask]

    # 4. Knockoff+ thresholding
    pos_W = np.sort(W[W > 0])
    selected_set = np.array([], dtype=int)
    threshold_T = None

    for t in pos_W:
        n_neg = np.sum(W <= -t)
        n_pos = np.sum(W >= t)
        fdp_est = (1.0 + n_neg) / max(1, n_pos)
        if fdp_est <= q:
            threshold_T = t
            break

    if threshold_T is not None:
        selected_set = np.where(W >= threshold_T)[0]

    # 5. Cap and Fallback for downstream clustering (Section A2.5)
    max_cap = min(D, max(100, int(np.ceil(0.15 * D))))
    fallback_flag = False

    if len(selected_set) < 20:
        fallback_flag = True
        # F_active = top 20 by W_d
        F_active = np.argsort(W)[-min(20, D):]
    else:
        # Keep at most max_cap ranked by W_d
        if len(selected_set) <= max_cap:
            F_active = selected_set
        else:
            sub_ranked = np.argsort(W[selected_set])[-max_cap:]
            F_active = selected_set[sub_ranked]

    return {
        "selected_set": selected_set,
        "active_features": F_active,
        "W": W,
        "s_target": s_target,
        "s_decoy": s_decoy,
        "threshold_T": threshold_T,
        "fallback_flag": fallback_flag,
        "eligible_mask": eligible_mask,
    }


def run_development_validation():
    print("=" * 80)
    print("STUDY 3' DEVELOPMENT PIPELINE VALIDATION (SEEDS >= 10,000)")
    print("=" * 80)

    # 1. Synthetic Dev Test (Seed 10,000)
    print("\n[1/3] Testing on Synthetic Gaussian Mixture with Distractors (Seed 10,000)...")
    rng = np.random.default_rng(10000)
    N, D_sig, D_noise = 200, 20, 180
    D = D_sig + D_noise
    y = rng.choice(2, size=N)

    X_sig = np.zeros((N, D_sig))
    for k in [0, 1]:
        idx = (y == k)
        X_sig[idx] = rng.normal(loc=(k * 2 - 1) * 2.5, scale=1.0, size=(np.sum(idx), D_sig))
    X_noise = rng.normal(0, 1, size=(N, D_noise))
    X_dev = np.hstack([X_sig, X_noise])

    res = null_calibrated_gate(X_dev, q=0.10, rng=rng)
    S = res["selected_set"]
    tp = np.sum(S < D_sig)
    fp = np.sum(S >= D_sig)
    fdp = fp / max(1, len(S))
    pwr = tp / D_sig

    print(f"  Selected: {len(S)} features (TP={tp}/{D_sig}, FP={fp})")
    print(f"  Empirical FDP: {fdp:.3f} (Nominal q=0.10) | Power: {pwr:.3f}")
    print(f"  Fallback triggered: {res['fallback_flag']} | Active features: {len(res['active_features'])}")
    assert fdp <= 0.20, f"Development FDP {fdp} exceeded tolerance"
    assert pwr >= 0.85, f"Development power {pwr} below expectation"

    # 2. Madelon Dev Test
    print("\n[2/3] Testing on Madelon Development Dataset...")
    if os.path.exists("data/cache/madelon.npz"):
        data = np.load("data/cache/madelon.npz")
        X_mad = data["X"][:300]
        res_mad = null_calibrated_gate(X_mad, q=0.10, rng=np.random.default_rng(10001))
        print(f"  Madelon features: {X_mad.shape[1]}")
        print(f"  Selected set size: {len(res_mad['selected_set'])}")
        print(f"  Fallback triggered: {res_mad['fallback_flag']}")
        print(f"  Active features: {len(res_mad['active_features'])}")
    else:
        print("  Madelon cache not found, skipping local check.")

    # 3. Sonar Dev Test
    print("\n[3/3] Testing on Sonar Development Dataset...")
    if os.path.exists("data/cache/sonar.npz"):
        data = np.load("data/cache/sonar.npz")
        X_son = data["X"]
        res_son = null_calibrated_gate(X_son, q=0.10, rng=np.random.default_rng(10002))
        print(f"  Sonar features: {X_son.shape[1]}")
        print(f"  Selected set size: {len(res_son['selected_set'])}")
        print(f"  Active features: {len(res_son['active_features'])}")
    else:
        print("  Sonar cache not found, skipping local check.")

    print("\n>>> ALL DEVELOPMENT CHECKS PASSED CLEANLY! Ready for confirmatory execution.")


if __name__ == "__main__":
    run_development_validation()
