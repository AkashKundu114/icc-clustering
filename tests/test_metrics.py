"""
Unit tests for the ICC consensus evaluation metrics suite (src/icc/metrics.py).

Validates information-theoretic and pair-counting clustering metrics:
1. Exact metric calculation under perfect label isomorphism / permutation.
2. Expected null behavior (metric ~ 0.0) under statistical independence / random noise.
3. Dual-backend parity: verifies numerical agreement between scikit-learn metrics
   and the pure NumPy/SciPy fallback implementations.
4. Non-parametric bootstrap percentile confidence intervals (alpha=0.05).
"""

import numpy as np
import pytest

import icc.metrics as metrics_mod
from icc.metrics import (
    evaluate_all,
    evaluate_all_with_ci,
)


def test_perfect_agreement():
    """
    Verify metric invariance under bijective label permutations.
    
    When predictions are an exact permutation of ground truth labels:
    - Adjusted Rand Index (ARI) == 1.0
    - Normalized Mutual Information (NMI) == 1.0
    - Adjusted Mutual Information (AMI) == 1.0
    - V-Measure == 1.0
    - Fowlkes-Mallows Index (FM) == 1.0
    """
    y_true = np.array([0, 0, 1, 1, 2, 2])
    y_pred = np.array([2, 2, 0, 0, 1, 1])  # Arbitrary permutation: 0->2, 1->0, 2->1

    results = evaluate_all(y_true, y_pred)
    assert pytest.approx(results["ari"], 1e-6) == 1.0
    assert pytest.approx(results["nmi"], 1e-6) == 1.0
    assert pytest.approx(results["ami"], 1e-6) == 1.0
    assert pytest.approx(results["v_measure"], 1e-6) == 1.0
    assert pytest.approx(results["fm_index"], 1e-6) == 1.0


def test_random_independence():
    """
    Verify chance-adjusted metrics cluster near zero under statistical independence.
    
    Generates two mutually independent random categorical vectors.
    Confirms that chance-corrected metrics (ARI, AMI) remain close to 0.0 (|score| < 0.1).
    """
    rng = np.random.default_rng(123)
    y_true = rng.integers(0, 3, size=200)
    y_pred = rng.integers(0, 3, size=200)

    results = evaluate_all(y_true, y_pred)
    assert abs(results["ari"]) < 0.1
    assert abs(results["ami"]) < 0.1


def test_dual_backend_fallback_parity():
    """
    Verify numerical equivalence between scikit-learn and pure NumPy/SciPy backends.
    
    Evaluates both engines on identical non-trivial label vectors. Confirms that the
    pure Python/NumPy fallback reproduces scikit-learn's optimized C implementations
    within high numerical precision across ARI, NMI, AMI, V-Measure, and FM-Index.
    """
    if not (metrics_mod._SKLEARN_AVAILABLE and metrics_mod._sk_ari is not None):
        pytest.skip("scikit-learn backend not available on this platform")

    rng = np.random.default_rng(42)
    y_true = rng.integers(0, 4, size=60)
    y_pred = rng.integers(0, 4, size=60)

    # Scikit-learn backend results
    sk_results = evaluate_all(y_true, y_pred)

    # Pure NumPy/SciPy fallback backend results
    original_state = metrics_mod._SKLEARN_AVAILABLE
    try:
        metrics_mod._SKLEARN_AVAILABLE = False
        fb_results = evaluate_all(y_true, y_pred)
    finally:
        metrics_mod._SKLEARN_AVAILABLE = original_state

    assert pytest.approx(sk_results["ari"], 1e-5) == fb_results["ari"]
    assert pytest.approx(sk_results["nmi"], 1e-5) == fb_results["nmi"]
    assert pytest.approx(sk_results["ami"], 1e-4) == fb_results["ami"]
    assert pytest.approx(sk_results["v_measure"], 1e-5) == fb_results["v_measure"]
    assert pytest.approx(sk_results["fm_index"], 1e-5) == fb_results["fm_index"]


def test_evaluate_all_with_ci():
    """
    Verify bootstrap percentile confidence interval estimation for clustering metrics.
    
    Generates non-parametric bootstrap resampling replicates, verifying that
    point estimates and lower/upper bounds [ci_low, ci_high] are computed
    consistently and obey monotonicity (ci_low <= ci_high).
    """
    y_true = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2, 2])
    y_pred = np.array([0, 0, 1, 1, 1, 2, 2, 2, 2, 0])

    ci_results = evaluate_all_with_ci(y_true, y_pred, n_bootstrap=100, alpha=0.05, random_seed=42)
    for m in ["ari", "nmi", "ami", "v_measure", "fm_index"]:
        assert m in ci_results
        entry = ci_results[m]
        assert "mean" in entry
        assert "ci_low" in entry
        assert "ci_high" in entry
        assert entry["ci_low"] <= entry["ci_high"]
