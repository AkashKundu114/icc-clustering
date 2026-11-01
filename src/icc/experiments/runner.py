"""Backward-compatibility shim for icc.experiments.runner -> icc.benchmarks.runner."""

from icc.benchmarks.runner import *  # noqa: F403
from icc.benchmarks.runner import (
    BenchmarkResult,
    BenchmarkRunner,
    ExperimentResult,
    ExperimentRunner,
)

__all__ = [
    "BenchmarkRunner",
    "BenchmarkResult",
    "ExperimentRunner",
    "ExperimentResult",
]
