"""
Unit tests for Experiment 4.3: Anchor Approximation Fidelity Suite.
"""

import numpy as np

from experiments.exp4_scalability_and_sensitivity.src.anchor_fidelity_benchmark import (
    run_fidelity_sweep,
    run_icc_v2_exact,
)
from icc.consensus_v2 import InvariantCoreConsensusV2
from icc.core import build_dataset


def test_icc_v2_exact_output_shape_and_clustering():
    """Verify ICC-v2-Exact produces valid cluster assignments and reasonable timing."""
    X, y = build_dataset(d_noise=50, signal_dim=2, n_per_cluster=30, k=3, noise_seed=42)
    N, D = X.shape

    labels, elapsed = run_icc_v2_exact(X, k=3, n_base_models=10, seed=42)

    assert isinstance(labels, np.ndarray)
    assert labels.shape == (N,)
    assert len(np.unique(labels)) == 3
    assert elapsed > 0.0


def test_anchor_fidelity_gap_bounded():
    """Verify that Reduced and Exact have close clustering accuracy (small delta_ari)."""
    X, y = build_dataset(d_noise=50, signal_dim=2, n_per_cluster=40, k=3, noise_seed=42)
    from icc.metrics import evaluate_all

    model_red = InvariantCoreConsensusV2(n_clusters=3, n_base_models=10, n_anchors=20, random_state=42)
    labels_red = model_red.fit_predict(X)

    labels_exact, _ = run_icc_v2_exact(X, k=3, n_base_models=10, seed=42)

    sc_red = evaluate_all(y, labels_red)
    sc_exact = evaluate_all(y, labels_exact)

    delta_ari = abs(sc_exact["ari"] - sc_red["ari"])
    # Approximation error should be well bounded on this clean synthetic setup
    assert delta_ari < 0.25


def test_fidelity_sweep_smoke(tmp_path):
    """Run a small 1-trial smoke sweep across N=[60, 90] to verify end-to-end execution."""
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
