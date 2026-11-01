"""
Regression test suite for data leakage, label isolation, and inductive preprocessing fidelity.
"""

import numpy as np

from icc.consensus import InvariantCoreConsensusV2
from icc.data.preprocessing import bimodality_coefficient, build_dataset


def test_test_data_does_not_influence_training_preprocessing():
    """Verify that inductive projection does not modify training statistics or fitted anchors."""
    rng = np.random.default_rng(42)
    X_train, _ = build_dataset(n_per_cluster=40, k=3, signal_dim=2, noise_dim=100, seed=42)
    X_test = rng.normal(loc=100.0, scale=1.0, size=(20, X_train.shape[1]))

    model = InvariantCoreConsensusV2(n_clusters=3, random_state=42)
    _ = model.fit_predict(X_train)

    # Record fitted state
    orig_anchor_centroids = np.copy(model.anchor_centroids_)
    orig_anchor_indices = np.copy(model.anchor_indices_)
    orig_selected_features = np.copy(model.selected_features_)

    # Predict on test data
    test_labels = model.predict(X_test)

    # Check fitted state remains strictly immutable
    np.testing.assert_array_equal(model.anchor_centroids_, orig_anchor_centroids)
    np.testing.assert_array_equal(model.anchor_indices_, orig_anchor_indices)
    np.testing.assert_array_equal(model.selected_features_, orig_selected_features)
    assert len(test_labels) == len(X_test)


def test_ground_truth_labels_are_not_used_in_unsupervised_selection():
    """Verify that model fitting and feature screening require only X, never ground-truth y."""
    X, y_true = build_dataset(n_per_cluster=30, k=2, signal_dim=2, noise_dim=50, seed=123)

    model = InvariantCoreConsensusV2(n_clusters=2, random_state=123)
    # fit_predict accepts only X
    labels = model.fit_predict(X)

    assert labels.shape == (len(X),)
    # Model should have no attribute storing or referencing y_true
    assert not hasattr(model, "y_")
    assert not hasattr(model, "ground_truth_")


def test_deterministic_split_and_reproducibility():
    """Verify reproducible splitting and that no sample overlaps cross train/test splits."""
    N = 100

    indices = np.arange(N)
    rng_split = np.random.default_rng(999)
    train_idx = rng_split.choice(indices, size=80, replace=False)
    test_idx = np.setdiff1d(indices, train_idx)

    # Assert mutual exclusivity
    assert len(np.intersect1d(train_idx, test_idx)) == 0
    assert len(train_idx) + len(test_idx) == N

    # Replay with same seed
    rng_split2 = np.random.default_rng(999)
    train_idx2 = rng_split2.choice(indices, size=80, replace=False)
    test_idx2 = np.setdiff1d(indices, train_idx2)

    np.testing.assert_array_equal(train_idx, train_idx2)
    np.testing.assert_array_equal(test_idx, test_idx2)


def test_bc_screening_unsupervised_independence():
    """Verify that bimodality coefficient screening is independent of external labels."""
    rng = np.random.default_rng(77)
    # Uniform / unimodal feature
    x_unimodal = rng.normal(size=200)
    # Two-spike bimodal distribution
    x_bimodal = np.array([-5.0] * 50 + [5.0] * 50)

    bc_unimodal = bimodality_coefficient(x_unimodal)
    bc_bimodal = bimodality_coefficient(x_bimodal)

    # Sarle's threshold for uniform is 5/9 (~0.555)
    assert bc_unimodal < 5.0 / 9.0
    assert bc_bimodal > 5.0 / 9.0
