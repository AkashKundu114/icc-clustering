"""
Integration test for the shared ExperimentRunner.
"""

import tempfile
from pathlib import Path

from icc.experiments.runner import ExperimentRunner


def test_experiment_runner_end_to_end():
    with tempfile.TemporaryDirectory() as tmpdir:
        config = {
            "name": "test_run",
            "algorithms": ["icc_v2", "kmeans"],
            "datasets": ["synthetic_test"],
            "seeds": [42],
            "synthetic_noise_dim": 20,
            "output_dir": tmpdir,
        }

        runner = ExperimentRunner(config, output_dir=tmpdir)
        results = runner.run_all()

        assert len(results) == 2
        for r in results:
            assert r.status == "SUCCESS"
            assert "ari" in r.metrics
            assert r.runtime_seconds > 0.0

        out_files = list(Path(tmpdir).glob("*.json"))
        assert len(out_files) == 1
