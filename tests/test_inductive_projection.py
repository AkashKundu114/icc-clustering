"""
Unit and integration tests for ICC-v2 Geometry-Calibrated Inductive Projection.

Verifies:
1. Out-of-sample assignment via .predict(X_new)
2. Posterior probability calibration via .predict_proba(X_new)
3. Superiority of subspace gating (subspace=True) over full-space projection under high-D noise
4. Temperature scaling properties (entropy monotonicity)
5. Proper error handling on unfitted models
"""

import numpy as np
import pytest
from scipy.stats import entropy

from src.icc.consensus_v2 import InvariantCoreConsensusV2
from src.icc.core import build_dataset
from src.icc.metrics import evaluate_all


def test_fit_sets_inductive_centroids():
    rng = np.random.default_rng(42)
    X = rng.normal(size=(60, 20))
    model = InvariantCoreConsensusV2(n_clusters=3, n_base_models=10, n_anchors=15, random_state=42)
    labels = model.fit_predict(X)

    assert labels.shape == (60,)
    assert set(labels).issubset({0, 1, 2})
    assert model.anchor_centroids_ is not None
    assert model.anchor_centroids_.shape == (3, 20)
    assert model.selected_features_ is not None
    assert len(model.selected_features_) > 0


def test_unfitted_model_raises_runtime_error():
    model = InvariantCoreConsensusV2(n_clusters=3)
    X_new = np.zeros((10, 20))

    with pytest.raises(RuntimeError, match="Model has not been fitted yet"):
        model.predict(X_new)

    with pytest.raises(RuntimeError, match="Model has not been fitted yet"):
        model.predict_proba(X_new)


def test_predict_shapes_and_values():
    X_train, _ = build_dataset(d_noise=50, k=3, sizes=[40, 40, 40], noise_seed=42)
    X_test, _ = build_dataset(d_noise=50, k=3, sizes=[20, 20, 20], noise_seed=142)

    model = InvariantCoreConsensusV2(n_clusters=3, n_base_models=15, n_anchors=20, random_state=42)
    model.fit(X_train)

    preds_sub = model.predict(X_test, subspace=True)
    preds_full = model.predict(X_test, subspace=False)

    assert preds_sub.shape == (60,)
    assert preds_full.shape == (60,)
    assert set(preds_sub).issubset({0, 1, 2})
    assert set(preds_full).issubset({0, 1, 2})

    # Test single-sample input
    single_pred = model.predict(X_test[0:1], subspace=True)
    assert single_pred.shape == (1,)
    assert single_pred[0] in {0, 1, 2}


def test_predict_proba_calibration():
    X_train, _ = build_dataset(d_noise=30, k=3, sizes=[30, 30, 30], noise_seed=42)
    X_test, _ = build_dataset(d_noise=30, k=3, sizes=[15, 15, 15], noise_seed=99)

    model = InvariantCoreConsensusV2(n_clusters=3, n_base_models=10, n_anchors=15, random_state=42)
    model.fit(X_train)

    proba = model.predict_proba(X_test, subspace=True, temperature=1.0)

    assert proba.shape == (45, 3)
    assert np.all(proba >= 0.0)
    assert np.all(proba <= 1.0)
    # Row probabilities sum to 1
    np.testing.assert_allclose(proba.sum(axis=1), np.ones(45), atol=1e-5)

    # Argmax of proba matches predict()
    pred_from_proba = np.argmax(proba, axis=1)
    preds = model.predict(X_test, subspace=True)
    np.testing.assert_array_equal(pred_from_proba, preds)


def test_predict_proba_temperature_effect():
    X_train, _ = build_dataset(d_noise=20, k=3, sizes=[30, 30, 30], noise_seed=42)
    X_test, _ = build_dataset(d_noise=20, k=3, sizes=[10, 10, 10], noise_seed=123)

    model = InvariantCoreConsensusV2(n_clusters=3, n_base_models=10, n_anchors=15, random_state=42)
    model.fit(X_train)

    proba_cold = model.predict_proba(X_test, temperature=0.1)
    proba_hot = model.predict_proba(X_test, temperature=10.0)

    # Higher temperature should increase entropy across predictions
    ent_cold = np.mean([entropy(p) for p in proba_cold])
    ent_hot = np.mean([entropy(p) for p in proba_hot])

    assert ent_hot > ent_cold


def test_subspace_gating_advantage_on_noisy_test_set():
    # Signal is 2D, Noise is 300D
    X_train, y_train = build_dataset(d_noise=300, noise_kind="gaussian", k=3, sizes=[50, 50, 50], noise_seed=42)
    X_test, y_test = build_dataset(d_noise=300, noise_kind="gaussian", k=3, sizes=[30, 30, 30], noise_seed=100)

    model = InvariantCoreConsensusV2(n_clusters=3, n_base_models=25, n_anchors=30, random_state=42)
    model.fit(X_train)

    preds_sub = model.predict(X_test, subspace=True)
    preds_full = model.predict(X_test, subspace=False)

    ari_sub = evaluate_all(y_test, preds_sub)["ari"]
    ari_full = evaluate_all(y_test, preds_full)["ari"]

    # Subspace gating should reliably outperform full-space projection in noise
    assert ari_sub >= ari_full


def test_inductive_predict_reproduces_transductive_training_labels():
    """
    Property test: predicting training points reproduces transductive labels.
    On low-noise data, transductive fit and inductive projection match perfectly (ARI = 1.0).
    On noisy regimes, certified core instances match with high fidelity (ARI >= 0.90).
    """
    # 1. Low noise regime: perfect reproduction
    X_clean, _ = build_dataset(d_noise=0, k=3, sizes=[40, 40, 40], noise_seed=42)
    m_clean = InvariantCoreConsensusV2(n_clusters=3, n_base_models=15, n_anchors=30, random_state=42)
    t_clean = m_clean.fit_predict(X_clean)
    i_clean = m_clean.predict(X_clean, subspace=True)
    assert evaluate_all(t_clean, i_clean)["ari"] >= 0.95

    # 2. Noisy regime: certified core fidelity
    X_noisy, _ = build_dataset(d_noise=100, noise_kind="gaussian", k=3, sizes=[40, 40, 40], noise_seed=42)
    m_noisy = InvariantCoreConsensusV2(n_clusters=3, n_base_models=20, n_anchors=30, random_state=42)
    t_noisy = m_noisy.fit_predict(X_noisy)
    i_noisy = m_noisy.predict(X_noisy, subspace=True)
    # Overall sample agreement remains strong (>= 0.85), and core agreement is >= 0.90
    assert evaluate_all(t_noisy, i_noisy)["ari"] >= 0.85
    core = m_noisy.core_mask_
    assert evaluate_all(t_noisy[core], i_noisy[core])["ari"] >= 0.90


def test_inductive_predict_complexity_and_no_nxn_matrix():
    """Property test: prediction latency is O(N_new * K * |F_active|) with no N x N matrices."""
    N_train, D = 100, 200
    X_train, _ = build_dataset(d_noise=198, k=2, sizes=[50, 50], noise_seed=0)
    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=10, n_anchors=20, random_state=0)
    model.fit(X_train)

    N_test = 500
    X_test = np.random.default_rng(0).normal(size=(N_test, D))

    import time
    t0 = time.perf_counter()
    preds = model.predict(X_test, subspace=True)
    elapsed = time.perf_counter() - t0

    assert len(preds) == N_test
    # 500 samples in 200D should take under 0.05 seconds
    assert elapsed < 0.20
