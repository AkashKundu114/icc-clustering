"""
tests/test_scaling_timing.py
Unit tests for computational scaling benchmark and pipeline stage execution (Item 1b).
Asserts:
1. Runtime is measured end-to-end wrapping feature gating through final labels.
2. Every stage of GAC pipeline executes and populates diagnostic attributes.
3. Memory tracing (tracemalloc) is run separately from wall-clock timing.
"""

import time
import tracemalloc

import numpy as np

from icc.benchmarks.benchmark_models import run_icc_v2, run_standard_consensus
from icc.benchmarks.scaling import generate_benchmark_synthetic
from icc.consensus_v2 import InvariantCoreConsensusV2


def test_gac_pipeline_stage_execution_and_counters():
    """Verify that every stage of GAC executes and populates required attributes."""
    N = 300
    D = 50
    K = 3
    L = 20
    M = 10
    seed = 42

    X, y = generate_benchmark_synthetic(N, D, k=K, seed=seed)

    model = InvariantCoreConsensusV2(
        n_clusters=K,
        n_base_models=M,
        n_anchors=L,
        random_state=seed,
    )

    t0 = time.perf_counter()
    labels = model.fit_predict(X)
    elapsed = time.perf_counter() - t0

    # 1. Timer sanity
    assert elapsed > 0.0, "Execution elapsed time must be strictly positive"

    # 2. Stage 1: Feature screening (BGSS)
    assert model.feature_scores_ is not None, "Stage 1 (BGSS): feature_scores_ must be populated"
    assert len(model.feature_scores_) == D, f"feature_scores_ length must equal D={D}"
    assert np.all(np.isfinite(model.feature_scores_)), "feature_scores_ must be finite"

    # 3. Stage 2: Feature gating / candidate pool selection
    assert model.selected_features_ is not None, "Stage 2: selected_features_ must be populated"
    assert len(model.selected_features_) >= K, "Selected features pool must have at least K features"
    assert len(model.selected_features_) <= D, "Selected features pool cannot exceed D"

    # 4. Stage 3 & 4: Anchor certification and anchor selection
    assert model.core_indices_ is not None, "Stage 3: core_indices_ must be populated"
    assert len(model.core_indices_) >= K, "Core indices must contain at least K instances"
    assert model.anchor_indices_ is not None, "Stage 4: anchor_indices_ must be populated"
    assert len(model.anchor_indices_) == min(L, len(model.core_indices_)), "Anchor count must match min(L, core_count)"

    # 5. Stage 5: Bipartite graph embedding
    assert model.U_emb_ is not None, "Stage 5: U_emb_ spectral embedding must be populated"
    assert model.U_emb_.shape == (N, K), f"U_emb_ shape must be (N={N}, K={K})"

    # 6. Stage 6: Final cluster label assignment
    assert model.labels_ is not None, "Stage 6: labels_ must be populated"
    assert len(model.labels_) == N, f"labels_ length must equal N={N}"
    assert len(np.unique(model.labels_)) == K, f"labels_ must contain exactly K={K} clusters"
    assert np.array_equal(labels, model.labels_), "fit_predict return value must match model.labels_"

    # 7. Stage 7: Centroid calculation in feature space
    assert model.anchor_centroids_ is not None, "Stage 7: anchor_centroids_ must be populated"
    assert model.anchor_centroids_.shape == (K, D), f"anchor_centroids_ shape must be (K={K}, D={D})"


def test_run_icc_v2_wrapper_end_to_end():
    """Verify that run_icc_v2 wraps the complete pipeline end-to-end with timing."""
    N = 200
    D = 40
    K = 3
    seed = 101

    X, y = generate_benchmark_synthetic(N, D, k=K, seed=seed)
    actual_N = X.shape[0]

    t_before = time.perf_counter()
    labels, runtime, meta = run_icc_v2(X, k=K, seed=seed)
    t_after = time.perf_counter()

    outer_time = t_after - t_before

    assert len(labels) == actual_N
    assert len(np.unique(labels)) == K
    assert runtime > 0.0
    # runtime reported by wrapper must be within reasonable bounds of outer timer
    assert runtime <= outer_time + 0.05
    assert meta["n_samples"] == actual_N
    assert meta["n_clusters"] == K


def test_tracemalloc_separation_from_timing():
    """Verify that pure timing is executed with tracemalloc inactive."""
    # Ensure tracemalloc is NOT running during untraced timing
    if tracemalloc.is_tracing():
        tracemalloc.stop()

    assert not tracemalloc.is_tracing(), "tracemalloc must be inactive before timing test"

    X = np.random.randn(100, 20)
    t0 = time.perf_counter()
    labels, runtime, _ = run_icc_v2(X, k=2, seed=42)
    elapsed = time.perf_counter() - t0

    assert not tracemalloc.is_tracing(), "tracemalloc must remain inactive during pure timing pass"
    assert elapsed > 0.0

    # Traced memory in a dedicated separate pass
    tracemalloc.start()
    assert tracemalloc.is_tracing(), "tracemalloc should be active only in dedicated memory pass"
    labels_mem, _, _ = run_icc_v2(X, k=2, seed=42)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    assert peak > 0, "Peak memory tracing must record positive memory usage"
    assert not tracemalloc.is_tracing(), "tracemalloc must be stopped after memory pass"


def test_standard_consensus_end_to_end():
    """Verify Standard Consensus executes end-to-end and reports positive runtime."""
    N = 100
    D = 20
    K = 2
    seed = 42

    X, y = generate_benchmark_synthetic(N, D, k=K, seed=seed)
    labels, runtime, meta = run_standard_consensus(X, k=K, seed=seed)

    assert len(labels) == X.shape[0]
    assert len(np.unique(labels)) == K
    assert runtime > 0.0
    assert meta["n_samples"] == X.shape[0]

