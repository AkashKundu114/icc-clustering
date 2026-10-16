"""
ICC Datasets: Unified multi-domain dataset registry and loading system.

Supports 13 benchmark datasets across 7 domains:
  - Genomics (Sonar, Madelon, Colon, SRBCT, CNS, Leukemia, Prostate, Ovarian)
  - Text/NLP (20 Newsgroups, RCV1)
  - Image (Extended Yale B, COIL-20)
  - Hyperspectral (Indian Pines, Pavia University)
  - Audio/Speech (Isolet)
  - scRNA-seq (Zheng68k PBMC, Tabula Muris)

Usage:
    from src.icc.datasets import load_dataset, list_datasets
    X, y, meta = load_dataset("leukemia")
"""

from .registry import DatasetInfo, get_dataset_info, list_datasets, load_dataset, preprocess_dataset

__all__ = ["load_dataset", "list_datasets", "get_dataset_info", "DatasetInfo", "preprocess_dataset"]
