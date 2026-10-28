"""
Unit tests for NullConsensus estimator and NullGateFeatureSelector.
"""

import numpy as np
import pytest
from nullconsensus import NullConsensus
from nullconsensus.data.synthetic import make_gaussian_distractor

def test_nullconsensus_fit_predict_shape():
    X, y = make_gaussian_distractor(n_samples=60, n_features=100, n_informative=10, n_clusters=3, random_state=42)
    model = NullConsensus(n_clusters=3, n_base_models=5, n_anchors=20, n_null_permutations=3, random_state=42)
    labels = model.fit_predict(X)
    
    assert len(labels) == 60
    assert len(np.unique(labels)) <= 3
    assert model.centroids_.shape == (3, len(model.active_features_))

def test_nullconsensus_inductive_predict():
    X, y = make_gaussian_distractor(n_samples=90, n_features=100, n_informative=15, n_clusters=3, separation=4.0, random_state=42)
    model = NullConsensus(n_clusters=3, n_base_models=15, n_anchors=25, n_null_permutations=5, random_state=42)
    model.fit(X)
    
    # Test on unseen query batch
    rng = np.random.default_rng(999)
    X_query = rng.standard_normal((15, 100))
    X_query[:5, :15] += 2.0 * 4.0 # Cluster 2 shift
    preds = model.predict(X_query)
    
    assert len(preds) == 15
    assert set(preds).issubset({0, 1, 2})
    # First 5 queries should share the same cluster assignment
    assert len(np.unique(preds[:5])) == 1

def test_nullconsensus_hurdle_mode():
    from nullconsensus.data.synthetic import make_zero_inflated_counts
    X, y = make_zero_inflated_counts(n_samples=60, n_features=100, n_informative=10, n_clusters=2, random_state=42)
    model = NullConsensus(n_clusters=2, n_base_models=5, n_anchors=20, mode="hurdle", random_state=42)
    labels = model.fit_predict(X)
    assert len(labels) == 60
