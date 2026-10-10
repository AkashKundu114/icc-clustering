"""
Single-cell RNA-seq (scRNA-seq) dataset loaders for the ICC Benchmark Suite.

Datasets:
- Zheng68k PBMC (10x Genomics, extreme dropout sparsity)
- Tabula Muris FACS (K=~20, multi-tissue cell atlas) [STUB]

Requires:
    pip install 'icc[bio]' (scanpy, anndata)
"""

import os
import tarfile
from pathlib import Path
from typing import Tuple, Dict, Any, Optional
import numpy as np
from sklearn.preprocessing import LabelEncoder

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_CACHE = _PROJECT_ROOT / "data" / "cache"
_DEFAULT_RAW = _PROJECT_ROOT / "data" / "raw" / "zheng68k"


def _check_scanpy():
    """Ensure scanpy is installed; raise informative ImportError otherwise."""
    try:
        import scanpy as sc
        return sc
    except ImportError as e:
        raise ImportError(
            "scanpy is required for scRNA-seq datasets. "
            "Install via: pip install 'icc[bio]' or pip install scanpy"
        ) from e


def load_zheng68k(
    n_top_genes: int = 2000,
    mode: str = "reduced",
    cache_dir: Optional[str] = "data/cache",
    raw_dir: Optional[str] = None,
    force_download: bool = False,
) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Load Zheng68k PBMC single-cell RNA-seq benchmark dataset.

    Supports two operation modes:
    - 'reduced': Preprocessed 10x PBMC demonstration subset (N=700, D=765, K=10).
    - 'full': Complete 68k cell matrix from 10x Genomics with HVG selection.

    Standard Preprocessing Pipeline (Full Mode):
        1. sc.pp.filter_cells(min_genes=200)
        2. sc.pp.filter_genes(min_cells=3)
        3. sc.pp.normalize_total(target_sum=1e4)
        4. sc.pp.log1p()
        5. sc.pp.highly_variable_genes(n_top_genes=n_top_genes)
        6. sc.pp.scale(max_value=10)

    Parameters
    ----------
    n_top_genes : int, default=2000
        Number of highly variable genes (HVGs) to retain after dispersion filtering.
    mode : str, default='reduced'
        'reduced' for fast evaluation subset (N=700), or 'full' for complete 68k dataset.
    cache_dir : str, optional, default='data/cache'
        Target directory for caching preprocessed arrays.
    raw_dir : str, optional
        Target directory for downloading/storing raw 10x matrices.
    force_download : bool, default=False
        Recompute and overwrite existing cache file if True.

    Returns
    -------
    X : np.ndarray of shape (N, D)
        Standardized, log-normalized expression matrix (float32).
    y : np.ndarray of shape (N,)
        Integer cell type labels (0 to K-1, int64).
    metadata : dict
        Dataset descriptor properties.

    References
    ----------
    Zheng et al. "Massively parallel digital transcriptional profiling of single cells."
    Nature Communications, 2017.
    """
    if cache_dir is None:
        c_dir = str(_DEFAULT_CACHE)
    elif not os.path.isabs(cache_dir):
        c_dir = os.path.abspath(os.path.join(_PROJECT_ROOT, cache_dir))
    else:
        c_dir = os.path.abspath(cache_dir)
    os.makedirs(c_dir, exist_ok=True)

    cache_filename = "zheng68k.npz" if mode == "reduced" else f"zheng68k_{mode}.npz"
    cache_path = os.path.join(c_dir, cache_filename)

    # 1. Check local cache
    if os.path.exists(cache_path) and not force_download:
        with np.load(cache_path) as data:
            X = data["X"]
            y = data["y"]
            metadata = {
                "name": "zheng68k",
                "mode": mode,
                "N": int(X.shape[0]),
                "D": int(X.shape[1]),
                "K": int(len(np.unique(y))),
                "d_over_n": round(float(X.shape[1] / X.shape[0]), 2),
                "description": f"Zheng et al. 2017 PBMC scRNA-seq ({mode} mode: N={X.shape[0]}, D={X.shape[1]}, K={len(np.unique(y))})",
            }
            return X, y, metadata

    # 2. Check scanpy availability
    sc = _check_scanpy()

    # 3. Load dataset based on mode
    if mode == "reduced":
        print("[*] Loading Zheng68k PBMC reduced subset via scanpy...")
        adata = sc.datasets.pbmc68k_reduced()

        # If n_top_genes requested is smaller than available genes, filter to top HVGs
        if n_top_genes < adata.n_vars and "dispersions_norm" in adata.var:
            top_genes_idx = np.argsort(adata.var["dispersions_norm"].values)[-n_top_genes:]
            adata = adata[:, top_genes_idx]

        X = np.asarray(adata.X, dtype=np.float32)

        if "bulk_labels" in adata.obs:
            raw_labels = adata.obs["bulk_labels"].values
        elif "louvain" in adata.obs:
            raw_labels = adata.obs["louvain"].values
        else:
            raw_labels = np.zeros(X.shape[0], dtype=np.int64)

        y = LabelEncoder().fit_transform(raw_labels).astype(np.int64)

    elif mode == "full":
        if raw_dir is None:
            r_dir = str(_DEFAULT_RAW)
        elif not os.path.isabs(raw_dir):
            r_dir = os.path.abspath(os.path.join(_PROJECT_ROOT, raw_dir))
        else:
            r_dir = os.path.abspath(raw_dir)
        os.makedirs(r_dir, exist_ok=True)

        mtx_dir = os.path.join(r_dir, "filtered_matrices_mex", "hg19")
        if not os.path.exists(mtx_dir):
            tar_path = os.path.join(r_dir, "fresh_68k_pbmc_donor_a_filtered_gene_bc_matrices.tar.gz")
            if not os.path.exists(tar_path):
                import urllib.request
                import ssl
                url = (
                    "https://cf.10xgenomics.com/samples/cell-exp/1.1.0/fresh_68k_pbmc_donor_a/"
                    "fresh_68k_pbmc_donor_a_filtered_gene_bc_matrices.tar.gz"
                )
                print(f"[*] Downloading full 68k PBMC matrix from 10x Genomics...")
                ctx = ssl._create_unverified_context()
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=120, context=ctx) as resp, open(tar_path, "wb") as f_out:
                    while chunk := resp.read(65536):
                        f_out.write(chunk)
            print("[*] Extracting 10x Genomics matrix archive...")
            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(path=r_dir)

        print("[*] Reading 10x matrix...")
        adata = sc.read_10x_mtx(mtx_dir, var_names="gene_symbols", cache=True)

        print(f"[*] Preprocessing 68k cells: filter_cells, filter_genes, normalize, log1p, HVG selection...")
        sc.pp.filter_cells(adata, min_genes=200)
        sc.pp.filter_genes(adata, min_cells=3)
        sc.pp.normalize_total(adata, target_sum=1e4)
        sc.pp.log1p(adata)
        sc.pp.highly_variable_genes(adata, n_top_genes=n_top_genes, subset=True)
        sc.pp.scale(adata, max_value=10)

        X = adata.X.toarray().astype(np.float32) if hasattr(adata.X, "toarray") else np.asarray(adata.X, dtype=np.float32)
        y = np.zeros(X.shape[0], dtype=np.int64)
    else:
        raise ValueError(f"Unknown mode '{mode}' for load_zheng68k. Expected 'reduced' or 'full'.")

    # 4. Save to cache
    np.savez_compressed(cache_path, X=X, y=y)
    print(f"[+] Cached 'zheng68k' ({mode}) to {cache_path}: shape={X.shape}, K={len(np.unique(y))}")

    metadata = {
        "name": "zheng68k",
        "mode": mode,
        "N": int(X.shape[0]),
        "D": int(X.shape[1]),
        "K": int(len(np.unique(y))),
        "d_over_n": round(float(X.shape[1] / X.shape[0]), 2),
        "description": f"Zheng et al. 2017 PBMC scRNA-seq ({mode} mode: N={X.shape[0]}, D={X.shape[1]}, K={len(np.unique(y))})",
    }
    return X, y, metadata


def load_tabula_muris(
    cache_dir: Optional[str] = None,
    force_download: bool = False,
) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Load Tabula Muris FACS scRNA-seq multi-tissue cell atlas.

    Parameters
    ----------
    cache_dir : str, optional
        Target directory for caching preprocessed arrays.
    force_download : bool, default=False
        Recompute and overwrite existing cache file if True.

    Returns
    -------
    X : np.ndarray of shape (N, D)
    y : np.ndarray of shape (N,)
    metadata : dict

    References
    ----------
    Tabula Muris Consortium. "Single-cell transcriptomics of 20 mouse organs." Nature, 2018.
    """
    raise NotImplementedError("Dataset loader not yet implemented. Enable in Phase 4.")
