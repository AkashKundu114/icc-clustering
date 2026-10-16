"""
Tests for Core Mechanics, Synthetic Data Generators, and Legacy Consensus Modules.

Covers:
- build_dataset across all 5 noise kinds (gaussian, student_t, correlated, scaled, sparse)
- pairwise_coassoc matrix properties (symmetry, unit diagonal, range [0, 1])
- run_clusterer engine options (kmeans, spectral, ward, fcm)
- InvariantCoreConsensus (ICC-v1 class in src.icc.consensus)
"""

import numpy as np
import pytest

from icc.core import build_dataset, run_clusterer, pairwise_coassoc, canonical
from icc.consensus import InvariantCoreConsensus


@pytest.mark.parametrize("noise_kind", ["gaussian", "student_t", "correlated", "scaled", "sparse"])
def test_build_dataset_all_noise_kinds(noise_kind):
    k = 3
    sizes = [20, 25, 30]
    total_n = sum(sizes)
    d_noise = 40
    signal_dim = 2

    X, y = build_dataset(
        d_noise=d_noise,
        noise_kind=noise_kind,
        noise_seed=42,
        sizes=sizes,
        k=k,
        signal_dim=signal_dim,
    )

    assert X.shape == (total_n, signal_dim + d_noise)
    assert y.shape == (total_n,)
    assert set(np.unique(y)) == {0, 1, 2}
    assert not np.isnan(X).any()
    assert not np.isinf(X).any()


def test_pairwise_coassoc_properties():
    # 3 partitions of 4 samples
    P = np.array([
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [1, 1, 0, 0],
    ])
    S = pairwise_coassoc(P)

    assert S.shape == (4, 4)
    # Diagonal must be 1.0
    np.testing.assert_allclose(np.diag(S), np.ones(4))
    # Symmetric
    np.testing.assert_allclose(S, S.T)
    # Samples 0 & 1 are always together (co-assoc = 1.0)
    assert S[0, 1] == 1.0
    # Samples 0 & 2 are never together (co-assoc = 0.0)
    assert S[0, 2] == 0.0


@pytest.mark.parametrize("engine", ["kmeans", "spectral", "ward", "fcm"])
def test_run_clusterer_engines(engine):
    rng = np.random.default_rng(42)
    X = np.vstack([
        rng.normal(loc=-3, size=(15, 4)),
        rng.normal(loc=3, size=(15, 4)),
    ])
    labels = run_clusterer(engine, X, k=2, seed=42)

    assert labels.shape == (30,)
    assert set(np.unique(labels)) == {0, 1}


def test_canonical_labeling():
    y = np.array([2, 2, 0, 0, 1, 1])
    c = canonical(y)
    assert list(c) == [0, 0, 1, 1, 2, 2]


def test_icc_v1_legacy_consensus():
    X, y = build_dataset(d_noise=10, k=2, sizes=[25, 25], noise_seed=42)
    model = InvariantCoreConsensus(n_clusters=2, n_base_models=10, n_anchors=15, random_state=42)
    labels = model.fit_predict(X)

    assert labels.shape == (50,)
    assert set(np.unique(labels)) == {0, 1}
    assert hasattr(model, "core_mask_")
    assert model.core_mask_ is not None
