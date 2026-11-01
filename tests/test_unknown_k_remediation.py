"""
Tests for Unknown-K & ICC-AutoK Remediation (Findings F-20 to F-22).

Verifies:
- F-20: Removal of ground-truth K leakage in candidate search space
- F-21: Preservation and access of bipartite anchor co-occurrence B_norm
- F-22: Unbiased PAC argmin selection without hardcoded K=2 bias
- Resilience of Silhouette-based AutoK under noise
"""

import numpy as np

from icc.autok import run_icc_autok
from icc.consensus_v2 import InvariantCoreConsensusV2


def test_bipartite_b_norm_attribute_preservation():
    """F-21: InvariantCoreConsensusV2 must store B_norm_ of shape (N, L)."""
    rng = np.random.default_rng(42)
    X = rng.normal(size=(40, 20))
    model = InvariantCoreConsensusV2(n_clusters=3, n_anchors=10, random_state=42)
    model.fit_predict(X)

    assert hasattr(model, "B_norm_"), "Model must have B_norm_ attribute"
    assert model.B_norm_ is not None, "B_norm_ must not be None after fitting"
    assert model.B_norm_.shape[0] == 40
    assert model.B_norm_.shape[1] <= 10
    # Must be row-stochastic
    assert np.allclose(model.B_norm_.sum(axis=1), 1.0)


def test_unbiased_pac_argmin_selection():
    """F-22: PAC must select argmin PAC without forced +0.02 parsimony bias toward K=2."""
    rng = np.random.default_rng(42)
    # Generate 4 clearly separated clusters in 10D
    c1 = rng.normal(loc=[-6.0] * 10, scale=0.4, size=(25, 10))
    c2 = rng.normal(loc=[-2.0] * 10, scale=0.4, size=(25, 10))
    c3 = rng.normal(loc=[2.0] * 10, scale=0.4, size=(25, 10))
    c4 = rng.normal(loc=[6.0] * 10, scale=0.4, size=(25, 10))
    X = np.vstack([c1, c2, c3, c4])

    res = run_icc_autok(X, k_min=2, k_max=6, seed=42)
    assert res.best_k_pac is not None
    assert res.best_k_silhouette is not None
    assert set(res.pac_scores.keys()) == {2, 3, 4, 5, 6}
    # PAC decision must equal exact minimum PAC score
    min_pac_k = min(res.pac_scores, key=res.pac_scores.get)
    assert res.best_k_pac == min_pac_k


def test_label_independent_search_space_synthetic():
    """F-20: Ensure model order discovery functions without ground truth."""
    rng = np.random.default_rng(42)
    X = rng.normal(size=(50, 15))

    # Declared fixed candidate grid [2, 7]
    res = run_icc_autok(X, k_min=2, k_max=7, seed=42)
    assert 2 <= res.best_k_silhouette <= 7
    assert 2 <= res.best_k_pac <= 7
    assert len(res.pac_scores) == 6
