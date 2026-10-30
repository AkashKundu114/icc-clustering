"""
Unit and integration tests for Conformal Inductive Core Consensus (CICC).

Validates the conformal prediction and feature selection framework:
1. Decoy Feature Gating: non-parametric False Discovery Rate (FDR) control via knockoff/decoy features.
2. ConformalClusterer: finite-sample marginal coverage guarantees (1 - alpha) and prediction set sizes.
3. InductiveConsensusClusterer: end-to-end integration combining decoy gating with conformal consensus.
4. InductiveConsensusMemory: dynamic clustering, memory consolidation, and retrieval.
"""

import numpy as np

from cicc.conformal import ConformalClusterer, ConformalResult
from cicc.decoy import DecoyFeatureGating
from cicc.inductive import InductiveConsensusClusterer
from cicc.memory import InductiveConsensusMemory


def test_decoy_feature_gating():
    """
    Verify empirical False Discovery Rate (FDR) control via Decoy Feature Gating.
    
    Generates synthetic data with 10 informative signal features and 90 uninformative
    noise features. Fits DecoyFeatureGating with target FDR q=0.15.
    
    Verifies that:
    1. Most informative features are correctly discovered (high True Positive rate).
    2. Empirical FDR (FP / Total Selected) respects the target threshold with tolerance.
    """
    np.random.seed(42)
    N = 200
    D_info = 10
    D_noise = 90
    y = np.random.choice([0, 1], size=N)

    # Informative features correlated with cluster labels
    X_info = np.zeros((N, D_info))
    for j in range(D_info):
        X_info[:, j] = y * 2.0 + np.random.randn(N) * 0.5

    # Pure noise distractors
    X_noise = np.random.randn(N, D_noise)
    X = np.hstack([X_info, X_noise])

    gating = DecoyFeatureGating(fdr_target=0.15, random_state=42)
    gating.fit(X, y)

    selected = gating.selected_indices_
    assert len(selected) > 0, "Gating should select informative features"
    
    # Informative feature indices lie in [0, D_info - 1]
    tp = np.sum(selected < D_info)
    fp = np.sum(selected >= D_info)
    assert tp >= 8, f"Expected high true positive count, got {tp}"
    empirical_fdr = fp / max(1, len(selected))
    assert empirical_fdr <= 0.20, f"Empirical FDR {empirical_fdr} exceeded tolerance"


def test_conformal_clusterer_coverage():
    """
    Verify finite-sample split-conformal cluster coverage guarantees.
    
    Partitions synthetic clustered data into discovery, calibration, and test splits.
    Calibrates non-conformity threshold q_hat at miscoverage level alpha=0.10.
    
    Verifies that:
    1. Empirical test coverage >= (1 - alpha - tolerance) accounting for finite-sample variation.
    2. Average prediction set cardinality is compact (0.5 <= size <= K).
    3. Prediction sets contain valid cluster identifiers.
    """
    np.random.seed(42)
    N = 600
    K = 3
    D = 32

    # Generate synthetic clustered embeddings on hypersphere
    y = np.repeat(np.arange(K), N // K)
    centers = np.random.randn(K, D)
    centers = centers / np.linalg.norm(centers, axis=1, keepdims=True)

    X = np.zeros((N, D))
    for i in range(N):
        k = y[i]
        v = centers[k] + np.random.randn(D) * 0.2
        X[i] = v / np.linalg.norm(v)

    # Stratified split: discovery (40%), calibration (30%), test (30%)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
    X_disc, X_cal, y_disc, y_cal = train_test_split(X_train, y_train, test_size=0.4286, random_state=42, stratify=y_train)

    target_alpha = 0.10
    c_clust = ConformalClusterer(alpha=target_alpha, temperature=10.0, random_state=42)
    c_clust.fit_calibrate(X_disc, y_disc, X_cal, y_cal)

    assert c_clust.q_hat_ is not None
    assert 0.0 < c_clust.q_hat_ < 1.0

    result = c_clust.predict(X_test, y_test=y_test)
    assert isinstance(result, ConformalResult)
    assert result.empirical_coverage is not None
    # Nominal coverage is 90% (tolerance within standard binomial sample error for N=180 test samples)
    assert result.empirical_coverage >= 0.85
    assert 0.5 <= result.average_set_size <= K
    assert np.all(result.set_sizes >= 0)


def test_inductive_consensus_clusterer():
    """
    Verify end-to-end execution of InductiveConsensusClusterer.
    
    Integrates decoy feature selection, anchor-based consensus discovery, calibration split,
    and out-of-sample conformal prediction set generation.
    """
    np.random.seed(42)
    N = 300
    D = 64
    K = 3

    # Generate synthetic data with signal confined to leading dimensions
    y = np.random.choice(K, size=N)
    X = np.random.randn(N, D)
    for k in range(K):
        X[y == k, :10] += (k - 1) * 2.0

    clusterer = InductiveConsensusClusterer(
        n_clusters=K,
        n_anchors=20,
        n_base_models=10,
        enable_decoy_gating=True,
        fdr_target=0.15,
        alpha=0.10,
        random_state=42,
    )
    clusterer.fit(X, cal_ratio=0.30)

    assert clusterer.labels_ is not None
    assert len(clusterer.labels_) == N
    assert len(np.unique(clusterer.labels_)) == K

    # Test out-of-sample conformal prediction set generation
    X_unseen = np.random.randn(50, D)
    res = clusterer.predict_conformal(X_unseen)
    assert len(res.prediction_sets) == 50
    assert res.average_set_size >= 0.0


def test_inductive_consensus_memory():
    """
    Verify dynamic memory consolidation, cluster emergence, and retrieval.
    
    Tests:
    1. Seeding of initial memory cluster on first input.
    2. Consolidation of highly similar memory embedding into existing cluster centroid.
    3. Emergence of a novel cluster when encountering an orthogonal embedding.
    4. Two-stage cosine retrieval locating relevant stored memories.
    """
    np.random.seed(42)
    dim = 32
    mem_engine = InductiveConsensusMemory(dim=dim, alpha=0.10)

    # 1. Add first memory (seeds first cluster)
    m1 = mem_engine.add_memory("User likes Python", np.random.randn(dim))
    assert m1.action == "novel_cluster"
    assert len(mem_engine.centroids) == 1

    # 2. Add highly similar memory (should consolidate)
    v_similar = m1.embedding + np.random.randn(dim) * 0.05
    m2 = mem_engine.add_memory("User wrote a script in Python", v_similar)
    assert m2.action == "consolidated"
    assert m2.assigned_cluster == m1.assigned_cluster

    # 3. Add distant orthogonal memory (should spawn novel cluster)
    v_distant = np.random.randn(dim)
    # Ensure orthogonality by Gram-Schmidt projection
    v_distant = v_distant - np.dot(v_distant, m1.embedding) * m1.embedding
    mem_engine.add_memory("The weather in Tokyo is sunny", v_distant)
    assert len(mem_engine.centroids) >= 2

    # 4. Two-stage retrieval test
    retrieved = mem_engine.retrieve(v_similar, top_k=2)
    assert len(retrieved) > 0
    # Top retrieved memory should be Python-related
    assert "Python" in retrieved[0][0].text

    stats = mem_engine.get_stats()
    assert stats["total_memories"] == 3
    assert stats["consolidated_count"] >= 1
