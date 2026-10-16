"""
Unit tests for InvariantCoreConsensusV2 (src/icc/consensus_v2.py).
"""

import numpy as np
import pytest

from experiments.exp3_real_world_benchmarks.src.benchmark_models import InvariantCoreConsensusV2 as Exp3ICC2
from experiments.exp3_real_world_benchmarks.src.benchmark_models import run_icc_v2
from src.icc import InvariantCoreConsensusV2 as RootICC2
from src.icc.consensus_v2 import InvariantCoreConsensusV2


def test_icc_v2_initialization():
    model = InvariantCoreConsensusV2(
        n_clusters=3,
        n_base_models=15,
        n_anchors=20,
        core_quantile=0.50,
        subspace_rate=0.25,
        beta=2.0,
        random_state=42,
    )
    assert model.n_clusters == 3
    assert model.k == 3
    assert model.n_base_models == 15
    assert model.M == 15
    assert model.n_anchors == 20
    assert model.L == 20
    assert model.core_quantile == 0.50
    assert model.subspace_rate == 0.25
    assert model.beta == 2.0


def test_icc_v2_fit_predict_and_attributes():
    rng = np.random.default_rng(42)
    # Synthetic cluster structure with signal + noise features
    X_signal = np.vstack([
        rng.normal(loc=[-4, 0], scale=0.5, size=(20, 2)),
        rng.normal(loc=[4, 0], scale=0.5, size=(20, 2)),
        rng.normal(loc=[0, 4], scale=0.5, size=(20, 2)),
    ])
    X_noise = rng.normal(size=(60, 18))
    X = np.hstack([X_signal, X_noise])  # (60, 20)
    N, D = X.shape

    model = InvariantCoreConsensusV2(
        n_clusters=3,
        n_base_models=10,
        n_anchors=15,
        random_state=42,
    )
    labels = model.fit_predict(X)

    # 1. Output shapes and types
    assert isinstance(labels, np.ndarray)
    assert labels.shape == (N,)
    assert len(np.unique(labels)) == 3
    assert np.array_equal(labels, model.labels_)

    # 2. Core attributes
    assert model.stability_ is not None and model.stability_.shape == (N,)
    assert model.core_mask_ is not None and model.core_mask_.shape == (N,)
    assert model.core_mask_.dtype == bool
    assert model.core_indices_ is not None and len(model.core_indices_) > 0
    assert model.anchor_indices_ is not None and len(model.anchor_indices_) <= 15

    # 3. VSSG interpretability attributes (Requirement 3)
    assert model.feature_scores_ is not None
    assert model.feature_scores_.shape == (D,)
    assert model.selected_features_ is not None
    assert len(model.selected_features_) > 0
    assert all(0 <= f < D for f in model.selected_features_)

    # 4. Geometry-calibrated centroids and embeddings
    assert model.anchor_centroids_ is not None
    assert model.anchor_centroids_.shape == (3, D)
    assert model.U_emb_ is not None
    assert model.U_emb_.shape == (N, 3)


def test_icc_v2_predict_inductive():
    rng = np.random.default_rng(123)
    X_train = rng.normal(size=(40, 10))
    X_test = rng.normal(size=(15, 10))

    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=5, n_anchors=10, random_state=42)

    # Unfitted predict should fail
    with pytest.raises(RuntimeError):
        model.predict(X_test)

    model.fit(X_train)
    preds_test = model.predict(X_test)
    assert isinstance(preds_test, np.ndarray)
    assert preds_test.shape == (15,)
    assert set(np.unique(preds_test)).issubset({0, 1})

    # Test soft probabilities
    proba = model.predict_proba(X_test)
    assert proba.shape == (15, 2)
    assert np.allclose(proba.sum(axis=1), 1.0)


def test_exp3_run_icc_v2_wrapper():
    rng = np.random.default_rng(42)
    X = rng.normal(size=(30, 8))
    pred, elapsed, lc = run_icc_v2(X, k=2, n_base_models=5, n_anchors=10, seed=42)

    assert pred.shape == (30,)
    assert elapsed >= 0.0
    assert isinstance(lc, int)
    assert lc > 0


def test_export_parity():
    assert RootICC2 is InvariantCoreConsensusV2
    assert Exp3ICC2 is InvariantCoreConsensusV2
