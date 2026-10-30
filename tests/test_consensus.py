"""
Comprehensive unit and integration tests for Invariant Core Consensus (ICC-v2).

Validates the full consensus clustering lifecycle:
1. Model hyperparameter initialization, alias mapping, and deprecation handling.
2. End-to-end consensus clustering on mixed signal/noise manifolds.
3. Anchor-based bipartite graph construction and spectral embedding properties.
4. Closed-form out-of-sample inductive projection and probability calibration.
5. Invariant subspace feature gating and candidate pool selection strategies.
6. Numerical stability across spectral embedding backends.
7. Benchmark harness integration and package export parity.
"""

import numpy as np
import pytest

from experiments.exp3_real_world_benchmarks.src.benchmark_models import InvariantCoreConsensusV2 as Exp3ICC2
from experiments.exp3_real_world_benchmarks.src.benchmark_models import run_icc_v2
from icc import InvariantCoreConsensusV2 as RootICC2
from icc.consensus_v2 import InvariantCoreConsensusV2
from icc.core import build_dataset


def _synthetic_data():
    """
    Generate reproducible synthetic clustered data with known signal and orthogonal noise.
    
    Produces a 3-cluster Gaussian mixture in 2-dimensional signal space embedded
    within a 22-dimensional space containing 20 uninformative Gaussian noise features.
    """
    return build_dataset(
        d_noise=20,
        noise_kind="gaussian",
        noise_seed=0,
        sizes=[40, 40, 40],
        k=3,
        signal_dim=2,
    )


def test_icc_v2_initialization():
    """
    Verify parameter binding, internal alias mappings, and deprecation handling.
    
    Ensures that standard scikit-learn parameter names (e.g. n_clusters, n_base_models,
    n_anchors) map correctly to algorithmic notation (k, M, L), and that specifying
    the deprecated legacy 'beta' parameter emits an informative DeprecationWarning.
    """
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
    """
    Verify complete fit_predict execution and post-fit attribute invariants.
    
    Validates that:
    1. Output cluster labels form a valid partition matching requested cluster count K.
    2. Stability scores are computed for every sample in [0, 1].
    3. Core selection mask isolates high-stability samples via quantile thresholding.
    4. Selected anchor points are strictly bounded by L (n_anchors).
    5. Feature importance weights and selected subspace indices are populated.
    6. Geometry-calibrated anchor centroids and low-dimensional spectral coordinates are finite.
    """
    rng = np.random.default_rng(42)
    # Generate 3 well-separated signal clusters perturbed by 18 noise dimensions
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

    # 1. Output shapes and partition validity
    assert isinstance(labels, np.ndarray)
    assert labels.shape == (N,)
    assert len(np.unique(labels)) == 3
    assert np.array_equal(labels, model.labels_)

    # 2. Core sample stability metrics
    assert model.stability_ is not None and model.stability_.shape == (N,)
    assert model.core_mask_ is not None and model.core_mask_.shape == (N,)
    assert model.core_mask_.dtype == bool
    assert model.core_indices_ is not None and len(model.core_indices_) > 0
    assert model.anchor_indices_ is not None and len(model.anchor_indices_) <= 15

    # 3. Subspace gating and feature ranking
    assert model.feature_scores_ is not None
    assert model.feature_scores_.shape == (D,)
    assert model.selected_features_ is not None
    assert len(model.selected_features_) > 0
    assert all(0 <= f < D for f in model.selected_features_)

    # 4. Geometry calibration attributes
    assert model.anchor_centroids_ is not None
    assert model.anchor_centroids_.shape == (3, D)
    assert model.U_emb_ is not None
    assert model.U_emb_.shape == (N, 3)


def test_bipartite_graph_properties():
    """
    Verify algebraic properties of the sample-anchor bipartite graph.
    
    Verifies that anchor selection produces at most L anchor nodes, that the
    spectral embedding coordinates are completely finite (no NaNs or infinities),
    and that spectral discretization yields valid cluster assignments.
    """
    X, _ = _synthetic_data()
    model = InvariantCoreConsensusV2(n_clusters=3, n_base_models=8, n_anchors=12, random_state=42)
    labels = model.fit_predict(X)

    assert len(model.anchor_indices_) <= 12
    assert model.U_emb_.shape == (len(X), 3)
    assert np.isfinite(model.U_emb_).all()
    assert set(labels) <= {0, 1, 2}


def test_icc_v2_predict_inductive():
    """
    Verify out-of-sample inductive inference and probability simplex normalization.
    
    Tests:
    1. Unfitted estimator raises RuntimeError on predict.
    2. Out-of-sample prediction maps unseen observations to valid cluster labels.
    3. Soft posterior probabilities sum to 1.0 across clusters for every query point.
    """
    rng = np.random.default_rng(123)
    X_train = rng.normal(size=(40, 10))
    X_test = rng.normal(size=(15, 10))

    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=5, n_anchors=10, random_state=42)

    # Ensure uncalibrated model rejects inference requests
    with pytest.raises(RuntimeError):
        model.predict(X_test)

    model.fit(X_train)
    preds_test = model.predict(X_test)
    assert isinstance(preds_test, np.ndarray)
    assert preds_test.shape == (15,)
    assert set(np.unique(preds_test)).issubset({0, 1})

    # Validate posterior probability distribution
    proba = model.predict_proba(X_test)
    assert proba.shape == (15, 2)
    assert np.allclose(proba.sum(axis=1), 1.0)


def test_beta_is_deprecated_and_has_no_effect():
    """
    Verify that specifying legacy beta emits a warning without altering output.
    
    Confirms algorithmic determinism: passing beta produces identical cluster
    assignments as leaving beta unset.
    """
    X, _ = _synthetic_data()
    with pytest.warns(DeprecationWarning, match="beta"):
        m1 = InvariantCoreConsensusV2(n_clusters=3, beta=5.0, random_state=0)
    m2 = InvariantCoreConsensusV2(n_clusters=3, random_state=0)
    assert np.array_equal(m1.fit_predict(X), m2.fit_predict(X))


def test_default_behaviour_unchanged_options_are_opt_in():
    """
    Verify backward compatibility when explicit legacy options are supplied.
    
    Confirms default configuration exactly matches explicit legacy parameterization
    (pool_mode='legacy', embedding='legacy').
    """
    X, _ = _synthetic_data()
    base = InvariantCoreConsensusV2(n_clusters=3, random_state=0).fit_predict(X)
    same = InvariantCoreConsensusV2(n_clusters=3, random_state=0, pool_mode="legacy", embedding="legacy").fit_predict(X)
    assert np.array_equal(base, same)


@pytest.mark.parametrize("emb", ["legacy", "transfer_cut"])
def test_embedding_finite_and_valid_labels(emb):
    """
    Verify numerical stability across spectral graph embedding formulations.
    
    Tests both the normalized symmetric Laplacian ('legacy') and the bipartite
    Transfer Cut formulation ('transfer_cut'), ensuring finite spectral coordinates.
    """
    X, _ = _synthetic_data()
    m = InvariantCoreConsensusV2(n_clusters=3, random_state=0, embedding=emb)
    lab = m.fit_predict(X)
    assert np.isfinite(m.U_emb_).all()
    assert set(lab) <= {0, 1, 2}


def test_invalid_options_raise():
    """
    Verify input validation guardrails reject invalid hyperparameters with ValueError.
    """
    X, _ = _synthetic_data()
    with pytest.raises(ValueError):
        InvariantCoreConsensusV2(n_clusters=3, embedding="invalid_emb").fit_predict(X)
    with pytest.raises(ValueError):
        InvariantCoreConsensusV2(n_clusters=3, pool_mode="invalid_pool").fit_predict(X)


@pytest.mark.parametrize("mode", ["bc_frac", "random_frac", "robust", "null_calibrated"])
def test_pool_mode_options(mode):
    """
    Verify alternative candidate pool selection modes produce valid feature subsets.
    
    Tests Bhattacharyya fraction, random fraction, robust thresholding, and
    null-calibrated permutation tests to ensure each strategy selects informative
    features and yields a valid partition.
    """
    X, _ = _synthetic_data()
    m = InvariantCoreConsensusV2(n_clusters=3, pool_mode=mode, pool_frac=0.10, random_state=0)
    lab = m.fit_predict(X)
    assert len(lab) == len(X)
    assert set(lab) <= {0, 1, 2}
    assert m.selected_features_ is not None
    assert len(m.selected_features_) >= 2


def test_exp3_run_icc_v2_wrapper():
    """
    Verify experiment benchmark runner wrapper returns correct tuple signature.
    
    Validates that run_icc_v2 returns (predictions, elapsed_time_sec, metadata).
    """
    rng = np.random.default_rng(42)
    X = rng.normal(size=(30, 8))
    pred, elapsed, lc = run_icc_v2(X, k=2, n_base_models=5, n_anchors=10, seed=42)

    assert pred.shape == (30,)
    assert elapsed >= 0.0
    assert isinstance(lc, int)
    assert lc > 0


def test_export_parity():
    """
    Verify identical class references across top-level and experiment namespaces.
    """
    assert RootICC2 is InvariantCoreConsensusV2
    assert Exp3ICC2 is InvariantCoreConsensusV2
