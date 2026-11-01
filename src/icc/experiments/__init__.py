"""
Backward-compatibility package for icc.experiments -> icc.benchmarks.
"""

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
