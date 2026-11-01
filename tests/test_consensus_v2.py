"""
Unit tests for InvariantCoreConsensusV2 (src/icc/consensus_v2.py).

Covers:
1. Core ICC-v2 algorithm initialization, fit, attributes, and bipartite graph representation.
2. Inductive out-of-sample projection (predict and predict_proba).
3. Option coverage: candidate pool modes (legacy, bc_frac, random_frac, robust, null_calibrated)
   and spectral embedding backends (legacy, transfer_cut).
4. Deprecation validation for legacy beta parameter.
5. Benchmark runner wrapper and export parity.
"""

import numpy as np
import pytest

from experiments.exp3_real_world_benchmarks.src.benchmark_models import InvariantCoreConsensusV2 as Exp3ICC2
from experiments.exp3_real_world_benchmarks.src.benchmark_models import run_icc_v2
from icc import InvariantCoreConsensusV2 as RootICC2
from icc.consensus_v2 import InvariantCoreConsensusV2
from icc.core import build_dataset


def _synthetic_data():
    """Generate reproducible synthetic clustered data with noise features."""
    return build_dataset(d_noise=20, noise_kind="gaussian", noise_seed=0, sizes=[40, 40, 40], k=3, signal_dim=2)


def test_icc_v2_initialization():
    """Verify initialization attributes and deprecation warning on legacy beta."""
    with pytest.warns(DeprecationWarning, match="beta"):
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
    """Verify fit_predict produces expected labels, stability scores, and centroids."""
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

    # 3. Feature selection interpretability attributes
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


def test_bipartite_graph_properties():
    """Verify bipartite graph construction, anchor dimension, and finite embedding."""
    X, _ = _synthetic_data()
    model = InvariantCoreConsensusV2(n_clusters=3, n_base_models=8, n_anchors=12, random_state=42)
    labels = model.fit_predict(X)

    assert len(model.anchor_indices_) <= 12
    assert model.U_emb_.shape == (len(X), 3)
    assert np.isfinite(model.U_emb_).all()
    assert set(labels) <= {0, 1, 2}


def test_icc_v2_predict_inductive():
    """Verify out-of-sample inductive predict and predict_proba behaviors."""
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


def test_beta_is_deprecated_and_has_no_effect():
    """Verify passing beta triggers DeprecationWarning and produces identical assignments."""
    X, _ = _synthetic_data()
    with pytest.warns(DeprecationWarning, match="beta"):
        m1 = InvariantCoreConsensusV2(n_clusters=3, beta=5.0, random_state=0)
    m2 = InvariantCoreConsensusV2(n_clusters=3, random_state=0)
    assert np.array_equal(m1.fit_predict(X), m2.fit_predict(X))


def test_default_behaviour_unchanged_options_are_opt_in():
    """Verify explicit legacy parameterization matches default initialization."""
    X, _ = _synthetic_data()
    base = InvariantCoreConsensusV2(n_clusters=3, random_state=0).fit_predict(X)
    same = InvariantCoreConsensusV2(n_clusters=3, random_state=0, pool_mode="legacy", embedding="legacy").fit_predict(X)
    assert np.array_equal(base, same)


@pytest.mark.parametrize("emb", ["legacy", "transfer_cut"])
def test_embedding_finite_and_valid_labels(emb):
    """Verify both legacy and transfer_cut spectral embeddings produce finite coordinates and valid labels."""
    X, _ = _synthetic_data()
    m = InvariantCoreConsensusV2(n_clusters=3, random_state=0, embedding=emb)
    lab = m.fit_predict(X)
    assert np.isfinite(m.U_emb_).all()
    assert set(lab) <= {0, 1, 2}


def test_invalid_options_raise():
    """Verify invalid embedding or pool_mode arguments raise ValueError."""
    X, _ = _synthetic_data()
    with pytest.raises(ValueError):
        InvariantCoreConsensusV2(n_clusters=3, embedding="invalid_emb").fit_predict(X)
    with pytest.raises(ValueError):
        InvariantCoreConsensusV2(n_clusters=3, pool_mode="invalid_pool").fit_predict(X)


@pytest.mark.parametrize("mode", ["bc_frac", "random_frac", "robust", "null_calibrated"])
def test_pool_mode_options(mode):
    """Verify candidate pool modes select features and output valid cluster labels."""
    X, _ = _synthetic_data()
    m = InvariantCoreConsensusV2(n_clusters=3, pool_mode=mode, pool_frac=0.10, random_state=0)
    lab = m.fit_predict(X)
    assert len(lab) == len(X)
    assert set(lab) <= {0, 1, 2}
    assert m.selected_features_ is not None
    assert len(m.selected_features_) >= 2


def test_exp3_run_icc_v2_wrapper():
    """Verify the Experiment 3 benchmark runner wrapper returns predictions and metadata."""
    rng = np.random.default_rng(42)
    X = rng.normal(size=(30, 8))
    pred, elapsed, lc = run_icc_v2(X, k=2, n_base_models=5, n_anchors=10, seed=42)

    assert pred.shape == (30,)
    assert elapsed >= 0.0
    assert isinstance(lc, int)
    assert lc > 0


def test_export_parity():
    """Verify export parity across top-level and experiment namespaces."""
    assert RootICC2 is InvariantCoreConsensusV2
    assert Exp3ICC2 is InvariantCoreConsensusV2
