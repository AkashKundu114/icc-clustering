"""
Dataset loader wrapper for Experiment 3 Real-World Benchmarks.

Thin compatibility wrapper around the unified src.icc.datasets package.
Delegates dataset loading and cache lookups to src.icc.datasets.genomics.
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

try:
    from src.icc.datasets.genomics import (
        DATASET_CONFIGS,
        CACHE_DIR,
        get_cached_path,
        load_benchmark_dataset,
        load_genomics_dataset,
    )
    from src.icc.datasets import (
        load_dataset,
        list_datasets,
        get_dataset_info,
        DatasetInfo,
    )
except ImportError:
    from icc.datasets.genomics import (
        DATASET_CONFIGS,
        CACHE_DIR,
        get_cached_path,
        load_benchmark_dataset,
        load_genomics_dataset,
    )
    from icc.datasets import (
        load_dataset,
        list_datasets,
        get_dataset_info,
        DatasetInfo,
    )

__all__ = [
    "DATASET_CONFIGS",
    "CACHE_DIR",
    "get_cached_path",
    "load_benchmark_dataset",
    "load_genomics_dataset",
    "load_dataset",
    "list_datasets",
    "get_dataset_info",
    "DatasetInfo",
]

if __name__ == "__main__":
    for dname in DATASET_CONFIGS:
        X, y, meta = load_benchmark_dataset(dname)
        print(f"Loaded {dname}: N={meta['N']}, D={meta['D']}, K={meta['K']}")
