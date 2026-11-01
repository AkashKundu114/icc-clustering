"""
Unified Experiment Runner for ICC benchmark evaluations.
"""

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
import yaml

from ..algorithms import get_algorithm
from ..consensus.icc import InvariantCoreConsensusV2
from ..data.preprocessing import build_dataset
from ..data.registry import load_dataset
from ..evaluation.metrics import evaluate_all
from ..utils.helpers import Timer, configure_logging, set_seed

logger = configure_logging()


@dataclass
class BenchmarkResult:
    """Container for a single benchmark evaluation run."""

    dataset: str
    algorithm: str
    seed: int
    n_samples: int
    n_features: int
    k_clusters: int
    runtime_seconds: float
    metrics: Dict[str, float]
    status: str = "SUCCESS"
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)



class BenchmarkRunner:
    """
    Executes benchmark clustering evaluations across algorithms, datasets, and seeds.

    Parameters
    ----------
    config : dict or str or Path
        Configuration dictionary or path to a YAML configuration file.
    output_dir : str or Path, optional
        Directory where experiment results will be serialized.
    """

    def __init__(
        self,
        config: Union[Dict[str, Any], str, Path],
        output_dir: Optional[Union[str, Path]] = None,
    ):
        if isinstance(config, (str, Path)):
            with open(config, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f) or {}
        else:
            self.config = dict(config)

        self.output_dir = Path(output_dir or self.config.get("output_dir", "results/experiments"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.algorithms = self.config.get("algorithms", ["icc_v2", "kmeans", "spectral", "ward"])
        self.datasets = self.config.get("datasets", ["synthetic_gaussian"])
        self.seeds = self.config.get("seeds", [42])

    def run_single(
        self,
        dataset_name: str,
        algorithm_name: str,
        seed: int,
    ) -> BenchmarkResult:
        """Execute a single combination of dataset, algorithm, and seed."""
        set_seed(seed)

        # 1. Load or generate dataset
        try:
            if dataset_name.startswith("synthetic"):
                # e.g., synthetic_d1000
                noise_dim = self.config.get("synthetic_noise_dim", 500)
                X, y = build_dataset(
                    n_per_cluster=50,
                    k=3,
                    signal_dim=2,
                    noise_dim=noise_dim,
                    noise_kind="gaussian",
                    seed=seed,
                )
                k = 3
            else:
                X, y, meta = load_dataset(dataset_name)
                k = meta.get("n_classes", len(np.unique(y)))
        except Exception as e:
            logger.error(f"Failed to load dataset '{dataset_name}': {e}")
            return ExperimentResult(
                dataset=dataset_name,
                algorithm=algorithm_name,
                seed=seed,
                n_samples=0,
                n_features=0,
                k_clusters=0,
                runtime_seconds=0.0,
                metrics={},
                status="FAILED_DATA_LOAD",
                error_message=str(e),
            )

        n_samples, n_features = X.shape

        # 2. Execute algorithm
        try:
            with Timer() as timer:
                if algorithm_name in ("icc_v2", "icc", "gac"):
                    icc_kwargs = dict(self.config.get("icc_v2", {})) if isinstance(self.config, dict) else {}
                    model = InvariantCoreConsensusV2(
                        n_clusters=k,
                        random_state=seed,
                        **icc_kwargs,
                    )
                    labels = model.fit_predict(X)
                    model_meta = {"n_anchors": model.n_anchors, "n_base": model.n_base_models}
                else:
                    algo_fn = get_algorithm(algorithm_name)
                    res = algo_fn(X, k, seed=seed)
                    if isinstance(res, tuple):
                        labels = res[0]
                        model_meta = res[2] if len(res) > 2 else {}
                    else:
                        labels = res
                        model_meta = {}

            runtime = timer["elapsed"]

            # 3. Compute evaluation metrics
            metrics = evaluate_all(y, labels)

            return ExperimentResult(
                dataset=dataset_name,
                algorithm=algorithm_name,
                seed=seed,
                n_samples=n_samples,
                n_features=n_features,
                k_clusters=k,
                runtime_seconds=runtime,
                metrics=metrics,
                status="SUCCESS",
                metadata=model_meta,
            )
        except Exception as e:
            logger.exception(f"Algorithm '{algorithm_name}' failed on '{dataset_name}' with seed {seed}")
            return ExperimentResult(
                dataset=dataset_name,
                algorithm=algorithm_name,
                seed=seed,
                n_samples=n_samples,
                n_features=n_features,
                k_clusters=k,
                runtime_seconds=0.0,
                metrics={},
                status="FAILED_EXECUTION",
                error_message=str(e),
            )

    def run_all(self) -> List[BenchmarkResult]:
        """Execute all configured combinations and save results."""
        results: List[BenchmarkResult] = []
        total = len(self.datasets) * len(self.algorithms) * len(self.seeds)
        logger.info(f"Starting benchmark run: {total} total configurations.")

        for d_name in self.datasets:
            for a_name in self.algorithms:
                for seed in self.seeds:
                    logger.info(f"Running dataset={d_name}, algorithm={a_name}, seed={seed}")
                    res = self.run_single(d_name, a_name, seed)
                    results.append(res)

        self.save_results(results)
        return results

    def save_results(self, results: List[BenchmarkResult]) -> Path:
        """Serialize benchmark results to JSON."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        out_file = self.output_dir / f"run_{timestamp}.json"
        data = [asdict(r) for r in results]
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved {len(results)} results to {out_file}")
        return out_file


# Backward-compatibility aliases
ExperimentResult = BenchmarkResult
ExperimentRunner = BenchmarkRunner

