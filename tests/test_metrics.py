"""
Unit tests for the ICC metrics evaluation module (src/icc/metrics.py).
"""

import numpy as np
import pytest
from src.icc.metrics import (
    adjusted_rand_score,
    normalized_mutual_info_score,
    adjusted_mutual_info_score,
    v_measure_score,
    fowlkes_mallows_score,
    evaluate_all,
    evaluate_all_with_ci,
)
import src.icc.metrics as metrics_mod


def test_perfect_agreement():
    y_true = np.array([0, 0, 1, 1, 2, 2])
    y_pred = np.array([2, 2, 0, 0, 1, 1])  # Permutation of labels

    results = evaluate_all(y_true, y_pred)
    assert pytest.approx(results["ari"], 1e-6) == 1.0
    assert pytest.approx(results["nmi"], 1e-6) == 1.0
    assert pytest.approx(results["ami"], 1e-6) == 1.0
    assert pytest.approx(results["v_measure"], 1e-6) == 1.0
    assert pytest.approx(results["fm_index"], 1e-6) == 1.0


def test_random_independence():
    rng = np.random.default_rng(123)
    y_true = rng.integers(0, 3, size=200)
    y_pred = rng.integers(0, 3, size=200)

    results = evaluate_all(y_true, y_pred)
    assert abs(results["ari"]) < 0.1
    assert abs(results["ami"]) < 0.1


def test_dual_backend_fallback_parity():
    if not (metrics_mod._SKLEARN_AVAILABLE and metrics_mod._sk_ari is not None):
        pytest.skip("scikit-learn backend not available on this platform")

    rng = np.random.default_rng(42)
    y_true = rng.integers(0, 4, size=60)
    y_pred = rng.integers(0, 4, size=60)

    # Sklearn results
    sk_results = evaluate_all(y_true, y_pred)

    # Pure NumPy/SciPy fallback results
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
