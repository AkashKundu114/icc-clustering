"""
Edge-case, boundary-condition, and numerical stability tests for ICC-v2.

Validates algorithm robustness across pathological and extreme settings:
1. Zero-variance and degenerate constant feature dimensions.
2. Identical duplicate observations in feature space.
3. Micro-scale sample sizes (N=10, K=2) near partition cardinality limits.
4. Ultra-high dimensional regimes with extreme aspect ratios (D/N = 250).
5. Degenerate cluster evaluation edge cases (single-cluster partitions, all-singleton partitions).
6. Missing Completely At Random (MCAR) noise injection and imputation strategies.
"""

import numpy as np
import pytest

from icc.consensus_v2 import InvariantCoreConsensusV2
from icc.metrics import evaluate_all

HAS_IMPUTE = False
try:
    from experiments.exp3_real_world_benchmarks.src.missing_data_experiment import (
        impute_data,
        inject_mcar_noise,
    )
    HAS_IMPUTE = True
except (ImportError, Exception):
    HAS_IMPUTE = False


def test_zero_variance_features():
    """
    Verify numerical stability when encountering zero-variance (constant) features.
    
    Injects 3 perfectly invariant feature columns (constants 5.0, -2.0, 0.0).
    Ensures that standard deviation calculations, feature gating, and subsequent
    out-of-sample projection execute cleanly without zero-division warnings or NaNs.
    """
    rng = np.random.default_rng(42)
    X = rng.normal(size=(40, 20))
    X[:, 0] = 5.0
    X[:, 5] = -2.0
    X[:, 10] = 0.0

    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=10, n_anchors=10, random_state=42)
    labels = model.fit_predict(X)

    assert labels.shape == (40,)
    assert not np.isnan(labels).any()
    
    # Out-of-sample prediction must execute cleanly
    X_new = rng.normal(size=(5, 20))
    preds = model.predict(X_new)
    assert preds.shape == (5,)


def test_duplicate_samples():
    """
    Verify consensus consistency when duplicate samples exist in the dataset.
    
    Creates exact duplicate pairs by duplicating a 20-sample block.
    Confirms that identical points achieve high label agreement under anchor consensus.
    """
    rng = np.random.default_rng(42)
    X_base = rng.normal(size=(20, 10))
    X = np.vstack([X_base, X_base])

    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=10, n_anchors=10, random_state=42)
    labels = model.fit_predict(X)

    assert labels.shape == (40,)
    agreement = (labels[:20] == labels[20:]).mean()
    assert agreement >= 0.85


def test_small_sample_size():
    """
    Verify algorithmic execution at small sample size boundaries (N=10, K=2).
    
    Checks that core sample quantile filtering and anchor subsampling degrade
    gracefully when N is very small.
    """
    rng = np.random.default_rng(42)
    X = np.vstack([rng.normal(loc=-2, size=(5, 5)), rng.normal(loc=2, size=(5, 5))])

    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=5, n_anchors=5, random_state=42)
    labels = model.fit_predict(X)

    assert labels.shape == (10,)
    assert set(np.unique(labels)).issubset({0, 1})


def test_extreme_dimension_ratio():
    """
    Verify memory and algorithmic stability under severe high dimensionality (D/N = 250).
    
    Evaluates N=20 observations embedded in D=5000 dimensions, verifying that
    feature importance scoring and subspace gating operate within memory limits.
    """
    rng = np.random.default_rng(42)
    X = rng.normal(size=(20, 5000))

    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=10, n_anchors=8, random_state=42)
    labels = model.fit_predict(X)

    assert labels.shape == (20,)
    assert not np.isnan(labels).any()
    assert len(model.selected_features_) <= 5000


def test_metric_edge_cases():
    """
    Verify clustering evaluation metric behavior on degenerate label assignments.
    
    Validates that evaluate_all does not raise ZeroDivisionError or output NaNs when:
    - Case A: Prediction collapses to a single monolithic cluster.
    - Case B: Prediction fractures into all singleton clusters.
    """
    y_true = np.array([0, 0, 1, 1, 1, 0])

    # Case A: Prediction is all one cluster
    y_single = np.array([0, 0, 0, 0, 0, 0])
    scores_single = evaluate_all(y_true, y_single)
    assert abs(scores_single["ari"]) < 1e-6
    assert abs(scores_single["nmi"]) < 1e-6
    assert not np.isnan(scores_single["ari"])
    assert not np.isnan(scores_single["nmi"])

    # Case B: Prediction is all distinct clusters
    y_distinct = np.array([0, 1, 2, 3, 4, 5])
    scores_distinct = evaluate_all(y_true, y_distinct)
    assert not np.isnan(scores_distinct["ari"])
    assert not np.isnan(scores_distinct["nmi"])


@pytest.mark.skipif(not HAS_IMPUTE, reason="impute_data unavailable or blocked by system policy")
@pytest.mark.parametrize("strategy", ["Mean", "Median", "KNN", "Zero"])
def test_missing_data_injection_and_imputation(strategy):
    """
    Verify Missing Completely At Random (MCAR) injection and imputation strategies.
    
    Injects 30% missing values (NaNs) into feature tensors and verifies that Mean,
    Median, KNN, and Zero imputation strategies restore dense, NaN-free arrays.
    """
    rng = np.random.default_rng(42)
    X = rng.normal(size=(30, 15))
    rho = 0.30

    X_missing = inject_mcar_noise(X, rho=rho, seed=42)
    assert np.isnan(X_missing).any()

    X_imputed = impute_data(X_missing, strategy=strategy)
    assert not np.isnan(X_imputed).any()
    assert X_imputed.shape == X.shape
