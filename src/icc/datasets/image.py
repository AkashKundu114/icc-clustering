"""
Image dataset loaders for the ICC Benchmark Suite.

Datasets:
- Extended Yale B (K=38, varying illumination angles)
- COIL-20 (K=20, rotation manifold) [STUB]
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import numpy as np
import scipy.io as sio
from sklearn.preprocessing import LabelEncoder, StandardScaler

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_CACHE = _PROJECT_ROOT / "data" / "cache"
_DEFAULT_RAW = _PROJECT_ROOT / "data" / "raw" / "yale_b"


def _download_file(url: str, dest_path: str):
    """Download a file with user-agent headers and SSL verification handling."""
    import ssl
    import urllib.request

    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )
    with urllib.request.urlopen(req, timeout=45, context=ctx) as response, open(dest_path, "wb") as out_file:
        while chunk := response.read(65536):
            out_file.write(chunk)


def download_yale_b(
    raw_dir: Optional[str] = None,
    force: bool = False,
) -> str:
    """
    Download Extended Yale B 32x32 MATLAB dataset.

    Parameters
    ----------
    raw_dir : str, optional
        Target directory to store raw .mat file. Defaults to 'data/raw/yale_b'.
    force : bool, default=False
        Re-download and overwrite existing file if True.

    Returns
    -------
    str
        Absolute file path to the downloaded YaleB_32x32.mat file.
    """
    if raw_dir is None:
        target_dir = str(_DEFAULT_RAW)
    elif not os.path.isabs(raw_dir):
        target_dir = os.path.abspath(os.path.join(_PROJECT_ROOT, raw_dir))
    else:
        target_dir = os.path.abspath(raw_dir)
    os.makedirs(target_dir, exist_ok=True)

    mat_path = os.path.join(target_dir, "YaleB_32x32.mat")

    if os.path.exists(mat_path) and not force:
        return mat_path

    mirrors = [
        "http://www.cad.zju.edu.cn/home/dengcai/Data/YaleB/YaleB_32x32.mat",
    ]

    for url in mirrors:
        try:
            print(f"[*] Downloading Extended Yale B from {url}...")
            _download_file(url, mat_path)
            return mat_path
        except Exception as e:
            print(f"[!] Mirror failed ({url}): {e}. Attempting fallback...")

    raise RuntimeError(
        "Failed to download YaleB_32x32.mat from all mirrors. "
        "Please manually place 'YaleB_32x32.mat' in data/raw/yale_b/."
    )


def load_yale_b(
    cache_dir: Optional[str] = "data/cache",
    raw_dir: Optional[str] = None,
    force_download: bool = False,
) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Load Extended Yale B face image dataset (32x32 cropped, flattened to 1024D).

    Contains 2,414 face images of 38 subjects under various lighting angles.

    Parameters
    ----------
    cache_dir : str, optional, default='data/cache'
        Target directory for caching preprocessed arrays.
    raw_dir : str, optional
        Target directory where raw YaleB_32x32.mat is located or downloaded.
    force_download : bool, default=False
        Re-download and overwrite existing cache file if True.

    Returns
    -------
    X : np.ndarray of shape (2414, 1024)
        Standardized face pixel intensity vectors (float32).
    y : np.ndarray of shape (2414,)
        Subject identity labels (0 to 37, int64).
    metadata : dict
        Dataset descriptor properties.

    References
    ----------
    Georghiades et al. "From Few to Many: Illumination Cone Models for Face
    Recognition under Variable Lighting and Pose." IEEE TPAMI, 2001.
    """
    if cache_dir is None:
        c_dir = str(_DEFAULT_CACHE)
    elif not os.path.isabs(cache_dir):
        c_dir = os.path.abspath(os.path.join(_PROJECT_ROOT, cache_dir))
    else:
        c_dir = os.path.abspath(cache_dir)
    os.makedirs(c_dir, exist_ok=True)
    cache_path = os.path.join(c_dir, "yale_b.npz")

    if os.path.exists(cache_path) and not force_download:
        with np.load(cache_path) as data:
            X = data["X"]
            y = data["y"]
            metadata = {
                "name": "yale_b",
                "N": int(X.shape[0]),
                "D": int(X.shape[1]),
                "K": int(len(np.unique(y))),
                "d_over_n": round(float(X.shape[1] / X.shape[0]), 2),
                "description": "Extended Yale B cropped face images with varying illumination (N=2414, D=1024, K=38)",
            }
            return X, y, metadata

    mat_path = download_yale_b(raw_dir=raw_dir, force=force_download)

    print(f"[*] Loading raw .mat from {mat_path}...")
    mat = sio.loadmat(mat_path)
    fea = mat["fea"].astype(np.float64)
    gnd = mat["gnd"].ravel()

    print(f"[*] Preprocessing {fea.shape[0]} images ({fea.shape[1]} features, {len(np.unique(gnd))} classes)...")
    X = StandardScaler().fit_transform(fea).astype(np.float32)
    y = LabelEncoder().fit_transform(gnd).astype(np.int64)

    np.savez_compressed(cache_path, X=X, y=y)
    print(f"[+] Cached 'yale_b' to {cache_path}: shape={X.shape}, K={len(np.unique(y))}")

    metadata = {
        "name": "yale_b",
        "N": int(X.shape[0]),
        "D": int(X.shape[1]),
        "K": int(len(np.unique(y))),
        "d_over_n": round(float(X.shape[1] / X.shape[0]), 2),
        "description": "Extended Yale B cropped face images with varying illumination (N=2414, D=1024, K=38)",
    }
    return X, y, metadata


def load_coil20(
    cache_dir: Optional[str] = None,
    force_download: bool = False,
) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Load Columbia Object Image Library (COIL-20) dataset (32x32, flattened to 1024D).

    Parameters
    ----------
    cache_dir : str, optional
        Target directory for caching preprocessed arrays.
    force_download : bool, default=False
        Re-download and overwrite existing cache file if True.

    Returns
    -------
    X : np.ndarray of shape (1440, 1024)
    y : np.ndarray of shape (1440,)
    metadata : dict

    References
    ----------
    Nene et al. "Columbia Object Image Library (COIL-20)." Columbia University, 1996.
    """
    raise NotImplementedError("Dataset loader not yet implemented. Reserved interface for future benchmark extensions.")
