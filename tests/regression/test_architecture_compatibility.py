"""
Architecture Compatibility and Deduplication Regression Tests.

Verifies that backward-compatibility shims accurately preserve public interfaces,
deduplicated modules maintain parity with canonical implementations, and legacy
import paths function transparently.
"""

from pathlib import Path

import numpy as np
import pytest


def test_consensus_v2_compatibility_shim():
    """Verify icc.consensus_v2 shim correctly re-exports canonical consensus classes."""
    from icc.consensus import (
        GAC as CanonicalGAC,
    )
    from icc.consensus import (
        InvariantCoreConsensus as CanonicalICCv1,
    )
    from icc.consensus import (
        InvariantCoreConsensusV2 as CanonicalICCv2,
    )
    from icc.consensus_v2 import (
        GAC,
        ICC,
        ICCv1,
        ICCv2,
        InvariantCoreConsensus,
        InvariantCoreConsensusV2,
    )

    assert InvariantCoreConsensusV2 is CanonicalICCv2
    assert InvariantCoreConsensus is CanonicalICCv1
    assert GAC is CanonicalGAC
    assert ICC is CanonicalICCv2
    assert ICCv2 is CanonicalICCv2
    assert ICCv1 is CanonicalICCv1

    # Instantiate
    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=3, n_anchors=10)
    assert model.k == 2


def test_metrics_compatibility_shim():
    """Verify icc.metrics shim correctly delegates to icc.evaluation.metrics."""
    from icc.evaluation.metrics import (
        evaluate_all as canonical_evaluate_all,
    )
    from icc.metrics import (
        adjusted_mutual_info_score,
        adjusted_rand_score,
        evaluate_all,
        evaluate_all_with_ci,
        normalized_mutual_info_score,
    )

    y_true = np.array([0, 0, 1, 1, 2, 2])
    y_pred = np.array([1, 1, 0, 0, 2, 2])

    res1 = evaluate_all(y_true, y_pred)
    res2 = canonical_evaluate_all(y_true, y_pred)

    assert res1 == res2
    assert res1["ari"] == pytest.approx(1.0)
    assert res1["nmi"] == pytest.approx(1.0)
    assert adjusted_rand_score(y_true, y_pred) == pytest.approx(1.0)
    assert normalized_mutual_info_score(y_true, y_pred) == pytest.approx(1.0)
    assert adjusted_mutual_info_score(y_true, y_pred) == pytest.approx(1.0)

    ci_res = evaluate_all_with_ci(y_true, y_pred, n_bootstrap=10)
    assert "ari" in ci_res
    assert "mean" in ci_res["ari"]


def test_datasets_registry_compatibility_shim():
    """Verify icc.data.registry shim correctly re-exports from icc.datasets.registry."""
    from icc.data.registry import (
        list_datasets,
        load_dataset,
    )
    from icc.datasets.registry import (
        list_datasets as canonical_list_datasets,
    )
    from icc.datasets.registry import (
        load_dataset as canonical_load_dataset,
    )

    datasets1 = list_datasets()
    datasets2 = canonical_list_datasets()
    assert datasets1 == datasets2
    dataset_names = [d.name for d in datasets1]
    assert "leukemia" in dataset_names

    # Test leukemia dataset loading through both paths
    X1, y1, meta1 = load_dataset("leukemia")
    X2, y2, meta2 = canonical_load_dataset("leukemia")
    assert X1.shape == X2.shape
    assert meta1 == meta2


def test_benchmarks_experiments_shim():
    """Verify icc.experiments shim correctly re-exports from icc.benchmarks."""
    from icc.benchmarks import (
        BenchmarkResult as CanonicalBenchmarkResult,
    )
    from icc.benchmarks import (
        BenchmarkRunner as CanonicalBenchmarkRunner,
    )
    from icc.experiments import (
        BenchmarkResult,
        BenchmarkRunner,
        ExperimentResult,
        ExperimentRunner,
    )

    assert BenchmarkRunner is CanonicalBenchmarkRunner
    assert ExperimentRunner is CanonicalBenchmarkRunner
    assert BenchmarkResult is CanonicalBenchmarkResult
    assert ExperimentResult is CanonicalBenchmarkResult

    # Instantiate
    runner = ExperimentRunner(config={"algorithms": ["kmeans"], "datasets": ["synthetic"], "seeds": [42]})
    assert runner.algorithms == ["kmeans"]


def test_algorithms_baselines_reexports():
    """Verify icc.algorithms modules correctly re-export canonical baseline implementations."""
    from icc.algorithms import (
        get_algorithm,
        list_algorithms,
        list_models,
        run_kmeans,
    )
    from icc.baselines import (
        get_model as canonical_get_model,
    )
    from icc.baselines import (
        run_kmeans as canonical_run_kmeans,
    )

    assert get_algorithm is not None
    assert list_algorithms() == list_models()
    assert run_kmeans is canonical_run_kmeans

    # Verify model retrieval parity
    model_fn1 = get_algorithm("kmeans")
    model_fn2 = canonical_get_model("kmeans")
    assert model_fn1 is model_fn2

    # Verify execution
    rng = np.random.default_rng(42)
    X = rng.standard_normal((30, 5))
    labels1, rt1, meta1 = model_fn1(X, k=2, seed=42)
    labels2, rt2, meta2 = model_fn2(X, k=2, seed=42)
    assert np.array_equal(labels1, labels2)


def test_obsolete_shadowed_consensus_file_removed():
    """Ensure obsolete src/icc/consensus.py does not exist on disk to prevent shadowing."""
    consensus_py = Path(__file__).resolve().parents[2] / "src" / "icc" / "consensus.py"
    assert not consensus_py.exists(), (
        f"Obsolete duplicate {consensus_py} must not exist as it shadows src/icc/consensus/"
    )
