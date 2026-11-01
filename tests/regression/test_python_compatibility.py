"""
tests/regression/test_python_compatibility.py

Compatibility test suite verifying runtime behavior, standard library enhancements,
typing resolution, and numerical determinacy under Python 3.13 and Python 3.14.
"""

import sys
import tarfile
import tempfile
import typing
from pathlib import Path

import numpy as np

from cicc.inductive import InductiveConsensusClusterer
from icc.benchmarks.runner import BenchmarkResult
from icc.consensus.icc import InvariantCoreConsensusV2
from icc.data.preprocessing import build_dataset
from icc.evaluation.metrics import adjusted_rand_score
from icc.stats.testing import (
    bonferroni_correction,
    hodges_lehmann_estimator,
    tost_equivalence_test,
    wilcoxon_signed_rank_test,
)


def test_python_runtime_version_support():
    """Verify that current runtime is >= Python 3.10 and supported by pyproject metadata."""
    major, minor = sys.version_info.major, sys.version_info.minor
    assert major == 3, f"Expected Python 3.x, got major={major}"
    assert minor >= 10, f"Minimum supported version is 3.10, current is 3.{minor}"
    
    # Read pyproject.toml classifiers
    pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
    assert pyproject_path.exists(), "pyproject.toml must exist"
    content = pyproject_path.read_text(encoding="utf-8")
    assert "Programming Language :: Python :: 3.13" in content, "Python 3.13 classifier missing in pyproject.toml"
    assert "Programming Language :: Python :: 3.14" in content, "Python 3.14 classifier missing in pyproject.toml"


def test_python_313_tarfile_safety_and_pep706():
    """Verify PEP 706 safe tar extraction handling under Python 3.13+."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        tar_path = tmp_path / "test_archive.tar.gz"
        extract_dir = tmp_path / "extracted"
        extract_dir.mkdir()

        # Create a test tar archive containing a benign file
        test_file = tmp_path / "sample.txt"
        test_file.write_text("ICC Python 3.13/3.14 Compatibility Test", encoding="utf-8")
        
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(test_file, arcname="sample.txt")

        # Test extraction using data_filter (mandatory or standard on Python 3.12+)
        with tarfile.open(tar_path, "r:gz") as tar:
            if hasattr(tarfile, "data_filter"):
                tar.extractall(path=extract_dir, filter="data")
            else:
                tar.extractall(path=extract_dir)

        result_file = extract_dir / "sample.txt"
        assert result_file.exists(), "Extracted file must exist"
        assert result_file.read_text(encoding="utf-8") == "ICC Python 3.13/3.14 Compatibility Test"


def test_python_314_annotation_semantics_and_type_hints():
    """
    Verify that PEP 649 / PEP 749 deferred annotation evaluation in Python 3.14
    resolves cleanly across all core classes and dataclasses.
    """
    # 1. BenchmarkResult dataclass type hints
    hints_result = typing.get_type_hints(BenchmarkResult)
    assert "dataset" in hints_result
    assert "algorithm" in hints_result
    assert "metrics" in hints_result

    # 2. InvariantCoreConsensusV2 estimator annotations
    hints_icc = typing.get_type_hints(InvariantCoreConsensusV2.__init__)
    assert "n_clusters" in hints_icc
    assert "n_base_models" in hints_icc

    # 3. InductiveConsensusClusterer annotations
    hints_cicc = typing.get_type_hints(InductiveConsensusClusterer.__init__)
    assert "alpha" in hints_cicc
    assert "fdr_target" in hints_cicc

    # 4. Statistical testing functions annotations
    hints_wilcoxon = typing.get_type_hints(wilcoxon_signed_rank_test)
    assert "x" in hints_wilcoxon
    assert "return" in hints_wilcoxon

    hints_bonferroni = typing.get_type_hints(bonferroni_correction)
    assert "p_values" in hints_bonferroni
    assert "return" in hints_bonferroni


def test_python_313_314_core_algorithm_execution():
    """Verify that InvariantCoreConsensusV2 fits, predicts, and projects without error."""
    X, y = build_dataset(n_per_cluster=40, k=3, signal_dim=2, noise_dim=50, seed=42)
    assert X.shape == (120, 52)
    assert len(np.unique(y)) == 3

    model = InvariantCoreConsensusV2(
        n_clusters=3,
        n_base_models=15,
        n_anchors=25,
        random_state=42,
    )
    labels = model.fit_predict(X)

    assert len(labels) == 120
    assert len(np.unique(labels)) == 3
    ari = adjusted_rand_score(y, labels)
    assert ari > 0.50, f"Expected strong clustering performance under 3.13/3.14 runtime, got ARI={ari}"

    # Test inductive projection on unseen points
    X_unseen = np.random.randn(10, 52)
    pred_unseen = model.predict(X_unseen)
    assert len(pred_unseen) == 10
    assert np.all(pred_unseen >= 0) and np.all(pred_unseen < 3)


def test_python_313_314_conformal_inductive_pipeline():
    """Verify CICC split-conformal prediction set generation under modern Python runtime."""
    X, y = build_dataset(n_per_cluster=30, k=3, signal_dim=2, noise_dim=20, seed=101)
    
    cicc = InductiveConsensusClusterer(
        n_clusters=3,
        n_anchors=20,
        n_base_models=10,
        alpha=0.10,
        random_state=101,
    )
    cicc.fit(X, cal_ratio=0.30)
    
    # Query prediction sets
    X_query = X[:15]
    res = cicc.predict_conformal(X_query)
    
    assert len(res.prediction_sets) == 15
    for pset in res.prediction_sets:
        assert isinstance(pset, list)
        assert len(pset) >= 1, "Prediction set cannot be empty for reasonable nonconformity thresholds"
        assert all(c in [0, 1, 2] for c in pset)


def test_python_313_314_statistical_testing_and_bonferroni():
    """Verify statistical hypothesis testing helpers execute cleanly on modern Python."""
    diffs = np.array([0.05, 0.08, 0.03, 0.06, 0.04, 0.07, 0.05, 0.06])
    est, (ci_low, ci_high) = hodges_lehmann_estimator(diffs)
    assert ci_low <= est <= ci_high
    assert est > 0.0

    tost = tost_equivalence_test(diffs, margin=0.10)
    assert "p_tost" in tost
    assert "decision" in tost

    # Test wilcoxon and bonferroni
    w_res = wilcoxon_signed_rank_test(diffs)
    assert "statistic" in w_res
    assert "pvalue" in w_res
    assert 0.0 <= w_res["pvalue"] <= 1.0

    p_raw = np.array([0.01, 0.04, 0.50])
    p_adj = bonferroni_correction(p_raw)
    assert len(p_adj) == 3
    assert np.all(p_adj <= 1.0)
    assert np.all(p_adj >= p_raw)


def test_python_313_314_backward_compatibility_shims():
    """Verify that all backward-compatibility shims import and execute seamlessly."""
    # 1. ASPP shim
    from icc.aspp import AnchorSpacePerturbationProfiler as ASPPProfilerShim
    from icc.aspp import ASPPConfig as ASPPConfigShim
    cfg = ASPPConfigShim(repetitions=2)
    profiler = ASPPProfilerShim(config=cfg)
    assert profiler is not None

    # 2. Consensus shim
    from icc.consensus_v2 import InvariantCoreConsensusV2 as ICCv2Shim
    m_shim = ICCv2Shim(n_clusters=2, random_state=42)
    assert m_shim.n_clusters == 2

    # 3. Metrics shim
    from icc.metrics import adjusted_rand_score as ari_shim
    assert ari_shim([0, 0, 1, 1], [0, 0, 1, 1]) == 1.0

    # 4. Data shim
    from icc.data.registry import list_datasets as list_ds_shim
    ds_list = list_ds_shim()
    assert len(ds_list) > 0

    # 5. Benchmarks runner shim
    from icc.experiments.runner import BenchmarkRunner as RunnerShim
    runner = RunnerShim(config={'datasets': [], 'algorithms': []})
    assert runner is not None
