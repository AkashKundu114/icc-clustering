"""
Backward-compatibility shim for icc.data.registry -> icc.datasets.registry.

All benchmark dataset registry and loading facilities are now canonically
maintained in the icc.datasets package.
"""

from icc.datasets.registry import (
    DatasetInfo,
    get_dataset_info,
    list_datasets,
    load_dataset,
    preprocess_dataset,
)

__all__ = [
    "load_dataset",
    "list_datasets",
    "get_dataset_info",
    "DatasetInfo",
    "preprocess_dataset",
]
