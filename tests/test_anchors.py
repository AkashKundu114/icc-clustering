"""
Unit and integration tests for anchor approximation fidelity and spectral convergence.

Validates the mathematical bounds and empirical performance of anchor bipartite graphs:
1. Exact N x N consensus graph execution and output characteristics.
2. Bounded approximation error: verifies that replacing the full dense co-association
   matrix S with the bipartite sample-anchor matrix B preserves cluster partition
   accuracy (|delta ARI| < 0.25 on synthetic benchmarks).
3. Smoke testing the scalability and sensitivity sweep across increasing sample sizes.
"""

import numpy as np

from experiments.exp4_scalability_and_sensitivity.src.anchor_fidelity_benchmark import (
    run_fidelity_sweep,
    run_icc_v2_exact,
)
from icc.consensus_v2 import InvariantCoreConsensusV2
from icc.core import build_dataset
from icc.metrics import evaluate_all


def test_icc_v2_exact_output_shape_and_clustering():
    """
    Verify exact uncompressed ICC-v2 produces valid cluster assignments.
    
    Runs the full N x N co-association formulation without anchor compression,
    confirming partition validity and positive execution latency.
    """
    X, y = build_dataset(d_noise=50, signal_dim=2, n_per_cluster=30, k=3, noise_seed=42)
    N, D = X.shape

    labels, elapsed = run_icc_v2_exact(X, k=3, n_base_models=10, seed=42)

    assert isinstance(labels, np.ndarray)
    assert labels.shape == (N,)
    assert len(np.unique(labels)) == 3
    assert elapsed > 0.0


def test_anchor_fidelity_gap_bounded():
    """
    Verify bounded approximation discrepancy between Reduced and Exact consensus.
    
    Calculates the delta ARI between:
    - Reduced model: O(N * L) bipartite graph with L anchors.
    - Exact model: O(N^2) full co-association graph.
    
    Verifies that anchor subsampling introduces negligible distortion on well-conditioned
    synthetic clusters (|delta ARI| < 0.25).
    """
    X, y = build_dataset(d_noise=50, signal_dim=2, n_per_cluster=40, k=3, noise_seed=42)

    model_red = InvariantCoreConsensusV2(n_clusters=3, n_base_models=10, n_anchors=20, random_state=42)
    labels_red = model_red.fit_predict(X)

    labels_exact, _ = run_icc_v2_exact(X, k=3, n_base_models=10, seed=42)

    sc_red = evaluate_all(y, labels_red)
    sc_exact = evaluate_all(y, labels_exact)

    delta_ari = abs(sc_exact["ari"] - sc_red["ari"])
    assert delta_ari < 0.25


def test_fidelity_sweep_smoke(tmp_path):
    """
    Smoke test the anchor fidelity benchmarking pipeline across sample sizes.
    
    Executes a fast 1-trial benchmark across N=[60, 90], ensuring output CSV schema,
    speedup computation, and memory footprint tracking are preserved.
    """
    out_csv = tmp_path / "test_fidelity.csv"
    df = run_fidelity_sweep(n_samples_list=[60, 90], n_trials=1, output_csv=out_csv)

    assert out_csv.exists()
    assert len(df) == 2
    for col in [
        "ari_reduced",
        "ari_exact",
        "delta_ari",
        "nmi_reduced",
        "nmi_exact",
        "time_reduced",
        "time_exact",
        "speedup",
        "mem_reduced_mb",
        "mem_exact_mb",
    ]:
        assert col in df.columns
