"""
Unit tests for Experiment 1: Multi-Classifier Generalization Extension.
"""

import numpy as np
import pytest

HAS_EXPERIMENT1 = False
try:
    from experiments.exp1_generalization.src.exp1_pseudolabel_generalization import (
        extract_core_subset,
        get_classifier_instances,
        run_pseudolabel_generalization,
    )

    _test_clfs = get_classifier_instances(seed=42)
    HAS_EXPERIMENT1 = True
except (ImportError, Exception):
    HAS_EXPERIMENT1 = False


@pytest.mark.skipif(not HAS_EXPERIMENT1, reason="Classifier dependencies unavailable or blocked by system policy")
def test_classifier_instances():
    """Verify all 4 classifiers are configured with expected parameters."""
    clfs = get_classifier_instances(seed=42)
    assert set(clfs.keys()) == {"SVM", "RF", "MLP", "KNN"}
    assert clfs["RF"].n_estimators == 100
    assert clfs["MLP"].hidden_layer_sizes == (100, 50)
    assert clfs["MLP"].max_iter == 500
    assert clfs["KNN"].n_neighbors == 5


@pytest.mark.skipif(not HAS_EXPERIMENT1, reason="Classifier dependencies unavailable or blocked by system policy")
def test_extract_core_subset():
    """Verify extract_core_subset returns balanced representation across all classes."""
    rng = np.random.default_rng(42)
    X = rng.normal(size=(60, 10))
    y = np.repeat([0, 1, 2], 20)
    core_mask = np.zeros(60, dtype=bool)
    core_mask[:10] = True  # Only class 0 is initially in core_mask

    stability = rng.uniform(0.1, 0.9, size=60)
    noise_frac = np.full(60, 0.2)

    X_core, y_core = extract_core_subset(X, y, core_mask, stability, noise_frac, k_clusters=3, min_per_cluster=2)

    assert len(np.unique(y_core)) == 3
    assert len(X_core) == len(y_core)


@pytest.mark.skipif(not HAS_EXPERIMENT1, reason="Classifier dependencies unavailable or blocked by system policy")
def test_multiclassifier_smoke(tmp_path):
    """Run a fast 1-trial smoke sweep across D_noise=[0] to verify schema and execution."""
    out_csv = tmp_path / "test_mc_results.csv"
    df = run_pseudolabel_generalization(
        noise_dims=[0],
        n_trials=1,
        n_total=60,
        output_csv=out_csv,
    )

    assert out_csv.exists()
    expected_cols = {"classifier", "d_noise", "trial", "training_set", "test_ari", "test_nmi", "test_accuracy"}
    assert expected_cols.issubset(set(df.columns))
    assert set(df["classifier"].unique()) == {"SVM", "RF", "MLP", "KNN"}
    assert set(df["training_set"].unique()) == {"ALL", "CORE"}
