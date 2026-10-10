"""
Genomics and tabular benchmark dataset loader (OpenML-based).

Refactored from experiments/exp3_real_world_benchmarks/src/dataset_loader.py.
Supports all 8 high-dimensional benchmark datasets:
- Sonar (N=208, D=60, K=2)
- Madelon (N=500, D=500, K=2)
- Colon (N=62, D=2000, K=2)
- SRBCT (N=83, D=2308, K=4)
- CNS (N=60, D=7129, K=2)
- Leukemia (N=72, D=7129, K=2)
- Prostate (N=102, D=12600, K=2)
- Ovarian (N=253, D=15154, K=2)
"""

import os
from pathlib import Path
from typing import Dict, Any, Tuple
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Project root resolution (3 levels up from src/icc/datasets/genomics.py)
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
CACHE_DIR = os.path.abspath(os.path.join(_PROJECT_ROOT, "data", "cache"))
os.makedirs(CACHE_DIR, exist_ok=True)

DATASET_CONFIGS: Dict[str, Dict[str, Any]] = {
    "sonar": {
        "name": "sonar",
        "openml_name": "sonar",
        "version": 1,
        "as_frame": False,
        "description": "Sonar acoustic returns (N=208, D=60, K=2)",
    },
    "madelon": {
        "name": "madelon",
        "openml_name": "madelon",
        "version": 1,
        "as_frame": False,
        "subsample_n": 500,  # 500 stratified samples for fast multi-trial sweeps
        "description": "Madelon XOR + distractor noise (N=500, D=500, K=2)",
    },
    "colon": {
        "name": "colon",
        "openml_name": "colon",
        "version": 1,
        "as_frame": True,
        "description": "Colon cancer gene expression (N=62, D=2000, K=2)",
    },
    "srbct": {
        "name": "srbct",
        "openml_name": "srbct",
        "version": 1,
        "as_frame": True,
        "description": "Small round blue cell tumors (N=83, D=2308, K=4)",
    },
    "cns": {
        "name": "cns",
        "openml_name": "cns",
        "version": 1,
        "as_frame": True,
        "description": "Central nervous system embryonal tumors (N=60, D=7129, K=2)",
    },
    "leukemia": {
        "name": "leukemia",
        "openml_name": "leukemia",
        "version": 1,
        "as_frame": False,
        "description": "ALLAML leukemia gene expression (N=72, D=7129, K=2)",
    },
    "prostate": {
        "name": "prostate",
        "openml_name": "prostate",
        "version": 1,
        "as_frame": True,
        "description": "Prostate cancer microarray (N=102, D=12600, K=2)",
    },
    "ovarian": {
        "name": "ovarian",
        "openml_name": "ovarian",
        "version": 1,
        "as_frame": True,
        "description": "Ovarian cancer MS/microarray (N=253, D=15154, K=2)",
    },
}


def get_cached_path(dataset_name: str, cache_dir: str = None) -> str:
    """Return the absolute file path to the cached .npz file."""
    c_dir = cache_dir or CACHE_DIR
    return os.path.join(c_dir, f"{dataset_name}.npz")


def load_genomics_dataset(
    dataset_name: str,
    cache_dir: str = None,
    force_download: bool = False,
) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Load a benchmark dataset, using local disk cache if available or OpenML if not.
    
    Preprocessing Pipeline:
        1. Subsample points if subsample_n configured
        2. Impute NaNs with column-wise means
        3. Standardize features via StandardScaler (mean=0, var=1)
        4. Encode ground-truth labels into contiguous integer IDs [0, K-1]
        5. Cache preprocessed (X, y) to .npz file
    
    Returns:
        X (np.ndarray): Standardized feature matrix (N, D)
        y (np.ndarray): Integer cluster ground-truth labels (N,)
        metadata (dict): Dataset properties (N, D, K, d_over_n, name, description)
    """
    if dataset_name not in DATASET_CONFIGS:
        raise KeyError(
            f"Dataset '{dataset_name}' not recognized in genomics suite. "
            f"Available: {list(DATASET_CONFIGS.keys())}"
        )

    cfg = DATASET_CONFIGS[dataset_name]
    c_dir = cache_dir or CACHE_DIR
    os.makedirs(c_dir, exist_ok=True)
    cache_path = get_cached_path(dataset_name, cache_dir=c_dir)

    # 1. Check local cache
    if os.path.exists(cache_path) and not force_download:
        data = np.load(cache_path)
        X = data["X"]
        y = data["y"]
        metadata = {
            "name": dataset_name,
            "N": int(X.shape[0]),
            "D": int(X.shape[1]),
            "K": int(len(np.unique(y))),
            "d_over_n": round(float(X.shape[1] / X.shape[0]), 2),
            "description": cfg["description"],
        }
        return X, y, metadata

    # 2. Fetch raw dataset from OpenML
    print(f"[*] Downloading '{dataset_name}' from OpenML...")
    raw = fetch_openml(
        cfg["name"],
        version=cfg.get("version", 1),
        as_frame=cfg.get("as_frame", False),
        parser="auto",
    )

    if cfg.get("as_frame", False):
        raw_X = raw.data.to_numpy(dtype=np.float64)
        raw_y = raw.target.to_numpy()
    else:
        raw_X = np.asarray(raw.data, dtype=np.float64)
        raw_y = np.asarray(raw.target)

    # 3. Subsample if configured
    if "subsample_n" in cfg and cfg["subsample_n"] < raw_X.shape[0]:
        rng = np.random.default_rng(42)
        indices = []
        unique_classes = np.unique(raw_y)
        per_class = cfg["subsample_n"] // len(unique_classes)
        for c in unique_classes:
            c_idx = np.where(raw_y == c)[0]
            sampled = rng.choice(c_idx, size=min(per_class, len(c_idx)), replace=False)
            indices.extend(sampled)
        indices = np.array(indices)
        raw_X = raw_X[indices]
        raw_y = raw_y[indices]

    # 4. Impute NaNs if any
    if np.isnan(raw_X).any():
        col_means = np.nanmean(raw_X, axis=0)
        inds = np.where(np.isnan(raw_X))
        raw_X[inds] = np.take(col_means, inds[1])

    # 5. Standardize & Label Encode
    X = StandardScaler().fit_transform(raw_X)
    y = LabelEncoder().fit_transform(raw_y)

    # 6. Save compressed cache
    np.savez_compressed(cache_path, X=X, y=y)
    print(f"[+] Cached '{dataset_name}': shape={X.shape}, classes={len(np.unique(y))}")

    metadata = {
        "name": dataset_name,
        "N": int(X.shape[0]),
        "D": int(X.shape[1]),
        "K": int(len(np.unique(y))),
        "d_over_n": round(float(X.shape[1] / X.shape[0]), 2),
        "description": cfg["description"],
    }
    return X, y, metadata


def load_benchmark_dataset(dataset_name: str, force_download: bool = False):
    """Backward-compatible loader matching experiments/exp3 interface."""
    return load_genomics_dataset(dataset_name, force_download=force_download)
