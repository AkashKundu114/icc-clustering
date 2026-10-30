"""
Unit and integration tests for geometry-calibrated inductive out-of-sample projection.

Validates the mathematical rationale for out-of-sample projection:
1. Computation and caching of geometry-calibrated anchor centroids during fit().
2. Safe failure on unfitted models (fail-fast guardrails).
3. Discrete cluster assignment via closed-form nearest-centroid projection in O(K * D).
4. Posterior probability calibration: simplex constraints and argmax consistency.
5. Monotonic entropy scaling via temperature scaling parameter T.
6. Theoretical superiority of invariant subspace gating over full-space projection
   under high-dimensional noise regimes (d_noise >> signal_dim).
"""

import numpy as np
import pytest
from scipy.stats import entropy

from icc.consensus_v2 import InvariantCoreConsensusV2
from icc.core import build_dataset
from icc.metrics import evaluate_all


def test_fit_sets_inductive_centroids():
    """
    Verify model calibration initializes anchor centroids and feature masks.
    
    Ensures that fitting the model derives K centroid coordinates in the full D-dimensional
    space and selects the informative feature subset used for gated projection.
    """
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
    """
    Verify fail-fast guardrails prevent inference on uncalibrated models.
    
    Both predict() and predict_proba() must raise RuntimeError when called before fit().
    """
    model = InvariantCoreConsensusV2(n_clusters=3)
    X_new = np.zeros((10, 20))

    with pytest.raises(RuntimeError, match="Model has not been fitted yet"):
        model.predict(X_new)

    with pytest.raises(RuntimeError, match="Model has not been fitted yet"):
        model.predict_proba(X_new)


def test_predict_shapes_and_values():
    """
    Verify output dimensions and label space for batch and single-sample inputs.
    
    Tests out-of-sample inference under both subspace-gated projection (subspace=True)
    and unmasked projection (subspace=False), ensuring valid discrete cluster labels.
    """
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

    # Validate single-sample out-of-sample inference
    single_pred = model.predict(X_test[0:1], subspace=True)
    assert single_pred.shape == (1,)
    assert single_pred[0] in {0, 1, 2}


def test_predict_proba_calibration():
    """
    Verify mathematical properties of probabilistic inductive projection.
    
    Validates that:
    1. Output probabilities are bounded in [0, 1].
    2. Posterior distribution satisfies unit simplex normalization: sum_k P(c_k|x) = 1.0.
    3. Discrete prediction matches argmax of posterior probabilities.
    """
    X_train, _ = build_dataset(d_noise=30, k=3, sizes=[30, 30, 30], noise_seed=42)
    X_test, _ = build_dataset(d_noise=30, k=3, sizes=[15, 15, 15], noise_seed=99)

    model = InvariantCoreConsensusV2(n_clusters=3, n_base_models=10, n_anchors=15, random_state=42)
    model.fit(X_train)

    proba = model.predict_proba(X_test, subspace=True, temperature=1.0)

    assert proba.shape == (45, 3)
    assert np.all(proba >= 0.0)
    assert np.all(proba <= 1.0)
    # Unit simplex normalization check
    np.testing.assert_allclose(proba.sum(axis=1), np.ones(45), atol=1e-5)

    # Consistency check: argmax(predict_proba) must equal predict()
    pred_from_proba = np.argmax(proba, axis=1)
    preds = model.predict(X_test, subspace=True)
    np.testing.assert_array_equal(pred_from_proba, preds)


def test_predict_proba_temperature_effect():
    """
    Verify monotonic entropy modulation via the temperature hyperparameter T.
    
    In the softmax assignment P(c_k|x) = exp(-d(x, mu_k) / T) / sum_j exp(-d(x, mu_j) / T):
    - Low temperature (T -> 0) sharpens distributions towards one-hot Dirac distributions (low entropy).
    - High temperature (T -> inf) diffuses distributions towards uniform uncertainty (high entropy).
    """
    X_train, _ = build_dataset(d_noise=20, k=3, sizes=[30, 30, 30], noise_seed=42)
    X_test, _ = build_dataset(d_noise=20, k=3, sizes=[10, 10, 10], noise_seed=123)

    model = InvariantCoreConsensusV2(n_clusters=3, n_base_models=10, n_anchors=15, random_state=42)
    model.fit(X_train)

    proba_cold = model.predict_proba(X_test, temperature=0.1)
    proba_hot = model.predict_proba(X_test, temperature=10.0)

    ent_cold = np.mean([entropy(p) for p in proba_cold])
    ent_hot = np.mean([entropy(p) for p in proba_hot])

    assert ent_hot > ent_cold


def test_subspace_gating_advantage_on_noisy_test_set():
    """
    Verify noise resilience of invariant subspace gating under severe noise (D_noise >> D_signal).
    
    When signal is confined to d=2 dimensions and contaminated by d_noise=300 noise features,
    projecting onto the invariant subspace filtered by core sample stability isolates
    informative coordinates from noise accumulation, yielding equal or superior ARI
    compared to unguided full-space Euclidean distance.
    """
    # Signal is 2D, Noise is 300D (D/d_signal = 151)
    X_train, y_train = build_dataset(d_noise=300, noise_kind="gaussian", k=3, sizes=[50, 50, 50], noise_seed=42)
    X_test, y_test = build_dataset(d_noise=300, noise_kind="gaussian", k=3, sizes=[30, 30, 30], noise_seed=100)

    model = InvariantCoreConsensusV2(n_clusters=3, n_base_models=25, n_anchors=30, random_state=42)
    model.fit(X_train)

    preds_sub = model.predict(X_test, subspace=True)
    preds_full = model.predict(X_test, subspace=False)

    ari_sub = evaluate_all(y_test, preds_sub)["ari"]
    ari_full = evaluate_all(y_test, preds_full)["ari"]

    # Subspace gating should reliably outperform or match full-space projection in noise
    assert ari_sub >= ari_full
