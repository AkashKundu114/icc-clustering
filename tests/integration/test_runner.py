"""
Integration test for BenchmarkRunner and backward-compatible ExperimentRunner.
"""

import tempfile
from pathlib import Path

from icc.benchmarks.runner import BenchmarkRunner, ExperimentRunner


def test_benchmark_runner_end_to_end():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = {
            "name": "test_run",
            "algorithms": ["icc_v2", "kmeans"],
            "datasets": ["synthetic_test"],
            "seeds": [42],
            "synthetic_noise_dim": 20,
            "output_dir": tmpdir,
        }

        runner = BenchmarkRunner(config, output_dir=tmpdir)
        results = runner.run_all()

        assert len(results) == 2
        for r in results:
            assert r.status == "SUCCESS"
            assert "ari" in r.metrics
            assert r.runtime_seconds > 0.0

        out_files = list(Path(tmpdir).glob("*.json"))
        assert len(out_files) == 1


def test_legacy_experiment_runner_alias():
    """Verify ExperimentRunner is an exact functional alias of BenchmarkRunner."""
    assert ExperimentRunner is BenchmarkRunner

    with tempfile.TemporaryDirectory() as tmpdir:
        config = {
            "name": "test_legacy_run",
            "algorithms": ["kmeans"],
            "datasets": ["synthetic_test"],
            "seeds": [42],
            "synthetic_noise_dim": 10,
            "output_dir": tmpdir,
        }

        runner = ExperimentRunner(config, output_dir=tmpdir)
        results = runner.run_all()
        assert len(results) == 1
        assert results[0].status == "SUCCESS"
