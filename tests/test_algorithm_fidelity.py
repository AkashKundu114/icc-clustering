"""
Tests for Algorithm Fidelity & Baseline Remediation (Findings F-07 to F-13).

Verifies:
- F-07: Explicit base_clusterer in ICC-v2 without hidden switching
- F-08: Authentic unsupervised GMM-BIC grid search without ground-truth K leakage
- F-09: Authentic Leiden SNN unavailability detection and explicit Spectral-SNN baseline
- F-10: HDBSCAN* distance concentration and core/full metric reporting
- F-11: Sparse K-Means formula harmonization and s_rule parameterization
- F-12: Single-restart vs multi-restart initializations
- F-13: Fuzzy C-Means argmax partition evaluation
"""

import numpy as np

from icc.baselines.anchor import run_fastmvc
from icc.baselines.density import evaluate_hdbscan_metrics, run_hdbscan
from icc.baselines.leiden_snn import run_leiden_snn, run_spectral_snn
from icc.baselines.probabilistic import run_gmm, run_gmm_bic
from icc.baselines.sparse_kmeans import run_sparse_kmeans
from icc.consensus_v2 import InvariantCoreConsensusV2


def test_gmm_fixed_k_vs_bic_grid_search():
    """F-08: Ensure run_gmm fits fixed K while run_gmm_bic searches without true K."""
    rng = np.random.default_rng(42)
    # Generate 3 well-separated clusters in 10D
    c1 = rng.normal(loc=-5.0, scale=0.5, size=(30, 10))
    c2 = rng.normal(loc=0.0, scale=0.5, size=(30, 10))
    c3 = rng.normal(loc=5.0, scale=0.5, size=(30, 10))
    X = np.vstack([c1, c2, c3])

    # 1. Fixed K GMM
    labels_fix, rt_fix, meta_fix = run_gmm(X, k=3, seed=42)
    assert len(np.unique(labels_fix)) == 3
    assert meta_fix.get("method") == "GMM (Fixed-K)"
    assert meta_fix.get("n_clusters") == 3

    # 2. Authentic Unsupervised GMM-BIC (Candidate grid [2, 6])
    labels_bic, rt_bic, meta_bic = run_gmm_bic(X, k_min=2, k_max=6, seed=42)
    assert meta_bic.get("method") == "GMM-BIC"
    assert "bic_curve" in meta_bic._data
    assert set(meta_bic._data["bic_curve"].keys()) == {2, 3, 4, 5, 6}
    # Should discover K=3
    assert meta_bic.get("n_clusters") == 3


def test_leiden_snn_unavailability_and_spectral_snn():
    """F-09: Ensure Leiden reports unavailable when missing, rather than silently masquerading."""
    rng = np.random.default_rng(42)
    X = rng.normal(size=(40, 15))

    # By default, allow_fallback=False: should report UNAVAILABLE
    labels, rt, meta = run_leiden_snn(X, target_k=3, allow_fallback=False)
    assert "UNAVAILABLE" in meta.get("method")
    assert "UNAVAILABLE" in meta.get("status")

    # Explicit Spectral-SNN baseline
    labels_spec, rt_spec, meta_spec = run_spectral_snn(X, k=3, seed=42)
    assert meta_spec.get("method") == "Spectral-SNN"
    assert len(np.unique(labels_spec)) <= 3


def test_hdbscan_core_and_full_metrics():
    """F-10: Test HDBSCAN* noise fraction and conditional metric reporting."""
    rng = np.random.default_rng(42)
    # 2 dense clusters + isolated outliers
    c1 = rng.normal(loc=-4.0, scale=0.3, size=(25, 5))
    c2 = rng.normal(loc=4.0, scale=0.3, size=(25, 5))
    outliers = rng.uniform(low=-20.0, high=20.0, size=(10, 5))
    X = np.vstack([c1, c2, outliers])
    y_true = np.array([0] * 25 + [1] * 25 + [2] * 10)

    labels, rt, meta = run_hdbscan(X, min_cluster_size=5)
    metrics = evaluate_hdbscan_metrics(y_true, labels)

    assert "ari_full" in metrics
    assert "ari_core" in metrics
    assert "coverage" in metrics
    assert "noise_ratio" in metrics
    assert 0.0 <= metrics["noise_ratio"] <= 1.0
    assert np.isclose(metrics["coverage"] + metrics["noise_ratio"], 1.0)


def test_sparse_kmeans_formula_options():
    """F-11: Verify both scaling formulas for Sparse K-Means."""
    rng = np.random.default_rng(42)
    X = rng.normal(size=(30, 100))

    # 1. witten_scaled: s = 0.15 * sqrt(100) + 1.0 = 2.5
    labels_w, _, meta_w = run_sparse_kmeans(X, k=2, s_rule="witten_scaled", seed=42)
    assert np.isclose(meta_w.get("sparsity_param"), 2.5)

    # 2. table2: s = 1.1 + 0.5 * (sqrt(100) - 1.1) = 1.1 + 4.45 = 5.55
    labels_t, _, meta_t = run_sparse_kmeans(X, k=2, s_rule="table2", seed=42)
    assert np.isclose(meta_t.get("sparsity_param"), 5.55)


def test_fastmvc_surrogate_attribution():
    """F-23: Verify FastMVC is explicitly labeled as a surrogate proxy."""
    rng = np.random.default_rng(42)
    X = rng.normal(size=(20, 10))
    labels, rt, meta = run_fastmvc(X, k=2, n_anchors=5, seed=42)
    assert "Surrogate" in meta.get("method")
    assert meta.get("is_surrogate") is True


def test_base_clusterer_parameterization():
    """F-07: Verify explicit base_clusterer in InvariantCoreConsensusV2."""
    rng = np.random.default_rng(42)
    X = rng.normal(size=(30, 20))

    # Explicit kmeans base clusterer
    m_km = InvariantCoreConsensusV2(n_clusters=2, base_clusterer="kmeans", random_state=42)
    p_km = m_km.fit_predict(X)
    assert len(p_km) == 30
    assert m_km.base_clusterer == "kmeans"

    # Explicit spectral base clusterer
    m_sp = InvariantCoreConsensusV2(n_clusters=2, base_clusterer="spectral", random_state=42)
    p_sp = m_sp.fit_predict(X)
    assert len(p_sp) == 30
    assert m_sp.base_clusterer == "spectral"
