"""
Data loading, preprocessing, and synthetic high-dimensional generator pipelines.
"""

from .preprocessing import (
    bimodality_coefficient,
    build_dataset,
    canonical,
    make_noise,
    make_signal,
    pairwise_coassoc,
)
from .registry import list_datasets, load_dataset

__all__ = [
    "bimodality_coefficient",
    "build_dataset",
    "make_signal",
    "make_noise",
    "canonical",
    "pairwise_coassoc",
    "load_dataset",
    "list_datasets",
]
