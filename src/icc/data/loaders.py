"""
Benchmark dataset loaders for high-dimensional clustering evaluations.
"""


from .registry import list_datasets, load_dataset

__all__ = [
    "load_dataset",
    "list_datasets",
]
