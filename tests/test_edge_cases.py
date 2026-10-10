"""
Edge Case and Numerical Stability Tests for ICC-v2.

Verifies robustness against:
1. Zero-variance / constant features
2. Duplicate samples
3. Small sample size limits (N=10, K=2)
4. Extreme dimension ratio (D/N = 500)
5. Metric edge cases (single-cluster partitions, all-distinct partitions)
6. Missing data injection and imputation mechanics
"""

import numpy as np
import pytest

from src.icc.consensus_v2 import InvariantCoreConsensusV2
from src.icc.metrics import evaluate_all
from experiments.exp3_real_world_benchmarks.exp3_5_missing_data.src.missing_data_experiment import (
    inject_mcar_noise,
    impute_data,
)


def test_zero_variance_features():
    rng = np.random.default_rng(42)
    # 40 samples, 20 features: features 0, 5, 10 are completely constant
    X = rng.normal(size=(40, 20))
    X[:, 0] = 5.0
    X[:, 5] = -2.0
    X[:, 10] = 0.0

    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=10, n_anchors=10, random_state=42)
    labels = model.fit_predict(X)

    assert labels.shape == (40,)
    assert not np.isnan(labels).any()
    # Out-of-sample prediction works without error
    X_new = rng.normal(size=(5, 20))
    preds = model.predict(X_new)
    assert preds.shape == (5,)


def test_duplicate_samples():
    rng = np.random.default_rng(42)
    # 20 unique points, duplicated to 40
    X_base = rng.normal(size=(20, 10))
    X = np.vstack([X_base, X_base])

    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=10, n_anchors=10, random_state=42)
    labels = model.fit_predict(X)

    assert labels.shape == (40,)
    # Duplicated instances should receive consistent labels
    np.testing.assert_array_equal(labels[:20], labels[20:])


def test_small_sample_size():
    rng = np.random.default_rng(42)
    # N=10, D=5, K=2
    X = np.vstack([rng.normal(loc=-2, size=(5, 5)), rng.normal(loc=2, size=(5, 5))])

    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=5, n_anchors=5, random_state=42)
    labels = model.fit_predict(X)

    assert labels.shape == (10,)
    assert set(np.unique(labels)).issubset({0, 1})


def test_extreme_dimension_ratio():
    rng = np.random.default_rng(42)
    # N=20, D=5000 -> D/N = 250
    X = rng.normal(size=(20, 5000))

    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=10, n_anchors=8, random_state=42)
    labels = model.fit_predict(X)

    assert labels.shape == (20,)
    assert not np.isnan(labels).any()
    assert len(model.selected_features_) <= 5000


def test_metric_edge_cases():
    y_true = np.array([0, 0, 1, 1, 1, 0])

    # Case A: Prediction is all one cluster
    y_single = np.array([0, 0, 0, 0, 0, 0])
    scores_single = evaluate_all(y_true, y_single)
    assert scores_single["ari"] == 0.0
    assert scores_single["nmi"] == 0.0
    assert not np.isnan(scores_single["ari"])
    assert not np.isnan(scores_single["nmi"])

    # Case B: Prediction is all distinct clusters
    y_distinct = np.array([0, 1, 2, 3, 4, 5])
    scores_distinct = evaluate_all(y_true, y_distinct)
    assert not np.isnan(scores_distinct["ari"])
    assert not np.isnan(scores_distinct["nmi"])


@pytest.mark.parametrize("strategy", ["Mean", "Median", "KNN", "Zero"])
def test_missing_data_injection_and_imputation(strategy):
    rng = np.random.default_rng(42)
    X = rng.normal(size=(30, 15))
    rho = 0.30

    X_missing = inject_mcar_noise(X, rho=rho, seed=42)
    assert np.isnan(X_missing).any()

    X_imputed = impute_data(X_missing, strategy=strategy)
    assert not np.isnan(X_imputed).any()
    assert X_imputed.shape == X.shape
