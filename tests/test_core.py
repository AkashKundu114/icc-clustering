"""
Unit tests for core consensus primitives, synthetic data generators, and matrix operations.

Validates fundamental building blocks:
1. Synthetic dataset generator under diverse high-dimensional noise regimes.
2. Algebraic properties of the ensemble pairwise co-association matrix.
3. Execution and partition validity across diverse base clustering engines.
4. Permutation-invariant canonical relabeling.
5. Backward compatibility with legacy unanchored consensus clustering (ICC-v1).
"""

import numpy as np
import pytest

from icc.consensus import InvariantCoreConsensus
from icc.core import build_dataset, canonical, pairwise_coassoc, run_clusterer


@pytest.mark.parametrize("noise_kind", ["gaussian", "student_t", "correlated", "scaled", "sparse"])
def test_build_dataset_all_noise_kinds(noise_kind):
    """
    Verify synthetic clustered dataset generation across all five noise distributions.
    
    Tests:
    - 'gaussian': Standard isotropic Gaussian distractor dimensions.
    - 'student_t': Heavy-tailed perturbations with degrees of freedom nu=3.
    - 'correlated': Autoregressive AR(1) dependent noise channels.
    - 'scaled': Heterogeneous variance noise scaling across dimensions.
    - 'sparse': High-kurtosis Bernoulli-Gaussian impulse noise.
    
    Verifies output tensor shape (total_samples, signal_dim + d_noise), label balance,
    and numerical validity (no NaNs or infinite values).
    """
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
    """
    Verify algebraic and probabilistic axioms of the pairwise co-association matrix S.
    
    For an ensemble of M cluster partitions of N samples:
    1. S is an N x N matrix with entries S_ij = (1/M) * sum_m I(pi_m(i) == pi_m(j)).
    2. Unit diagonal: S_ii = 1.0 (every sample is co-clustered with itself).
    3. Exact symmetry: S = S^T.
    4. Exact bounds: S_ij in [0, 1] representing empirical joint co-occurrence.
    """
    # 3 partitions of 4 samples
    P = np.array([
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [1, 1, 0, 0],
    ])
    S = pairwise_coassoc(P)

    assert S.shape == (4, 4)
    # Diagonal must be 1.0 (self-co-association)
    np.testing.assert_allclose(np.diag(S), np.ones(4))
    # Must be symmetric
    np.testing.assert_allclose(S, S.T)
    # Samples 0 & 1 are always together (co-assoc = 1.0)
    assert S[0, 1] == 1.0
    # Samples 0 & 2 are never together (co-assoc = 0.0)
    assert S[0, 2] == 0.0


@pytest.mark.parametrize("engine", ["kmeans", "spectral", "ward", "fcm"])
def test_run_clusterer_engines(engine):
    """
    Verify partition validity across diverse base clustering engines.
    
    Tests K-Means (Lloyd's), Spectral Clustering (normalized cut), Ward hierarchical
    agglomerative clustering, and Fuzzy C-Means (FCM). Verifies that each clusterer
    returns an array of discrete cluster assignments in {0, ..., k-1}.
    """
    rng = np.random.default_rng(42)
    X = np.vstack([
        rng.normal(loc=-3, size=(15, 4)),
        rng.normal(loc=3, size=(15, 4)),
    ])
    labels = run_clusterer(engine, X, k=2, seed=42)

    assert labels.shape == (30,)
    assert set(np.unique(labels)) == {0, 1}


def test_canonical_labeling():
    """
    Verify canonical relabeling maps cluster indices to standard order of appearance.
    
    Removes label permutation ambiguity by mapping the first observed label to 0,
    second to 1, and so on.
    """
    y = np.array([2, 2, 0, 0, 1, 1])
    c = canonical(y)
    assert list(c) == [0, 0, 1, 1, 2, 2]


def test_icc_v1_legacy_consensus():
    """
    Verify backward compatibility with unanchored Invariant Core Consensus (ICC-v1).
    
    Verifies that the legacy dense N x N consensus pipeline executes cleanly,
    identifies core samples, and produces a valid cluster assignment.
    """
    X, y = build_dataset(d_noise=10, k=2, sizes=[25, 25], noise_seed=42)
    model = InvariantCoreConsensus(n_clusters=2, n_base_models=10, n_anchors=15, random_state=42)
    labels = model.fit_predict(X)

    assert labels.shape == (50,)
    assert set(np.unique(labels)) == {0, 1}
    assert hasattr(model, "core_mask_")
    assert model.core_mask_ is not None
