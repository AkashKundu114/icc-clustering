"""
Image dataset loaders for the ICC Benchmark Suite.

Datasets:
- Extended Yale B (K=38, varying illumination angles)
- COIL-20 (K=20, rotation manifold) [STUB]
"""

import os
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import numpy as np
import scipy.io as sio
from sklearn.preprocessing import LabelEncoder, StandardScaler

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_CACHE = _PROJECT_ROOT / "data" / "cache"
_DEFAULT_RAW = _PROJECT_ROOT / "data" / "raw" / "yale_b"
_YALE_B_SHAPE = (2414, 1024)


def _validate_yale_b_mat(mat_path: str) -> None:
    """Check the expected feature and label arrays before accepting a MAT file."""
    mat = sio.loadmat(mat_path, variable_names=["fea", "gnd"])
    if "fea" not in mat or "gnd" not in mat:
        raise ValueError("MAT file must contain 'fea' and 'gnd' arrays")
    fea = np.asarray(mat["fea"])
    gnd = np.asarray(mat["gnd"])
    if fea.shape != _YALE_B_SHAPE:
        raise ValueError(f"Expected Yale B fea shape {_YALE_B_SHAPE}, got {fea.shape}")
    if gnd.size != _YALE_B_SHAPE[0]:
        raise ValueError(f"Expected {_YALE_B_SHAPE[0]} Yale B labels, got {gnd.size}")


def _download_file(url: str, dest_path: str):
    """Download a complete, structurally valid Yale B MAT file atomically."""
    import urllib.request

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )
    temp_path = f"{dest_path}.part"
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            content_length = response.headers.get("Content-Length")
            expected_bytes = int(content_length) if content_length else None
            received_bytes = 0
            with open(temp_path, "wb") as out_file:
                while chunk := response.read(65536):
                    out_file.write(chunk)
                    received_bytes += len(chunk)
        if received_bytes == 0:
            raise OSError("Yale B download returned an empty response")
        if expected_bytes is not None and received_bytes != expected_bytes:
            raise OSError(
                f"Incomplete Yale B download: received {received_bytes} of {expected_bytes} bytes"
            )
        _validate_yale_b_mat(temp_path)
        os.replace(temp_path, dest_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


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
        try:
            _validate_yale_b_mat(mat_path)
            return mat_path
        except Exception as e:
            raise RuntimeError(
                f"Existing Yale B file is incomplete or invalid: {mat_path}. "
                "Remove the invalid file or call with force=True to download a validated copy."
            ) from e

    mirrors = [
        "http://www.cad.zju.edu.cn/home/dengcai/Data/YaleB/YaleB_32x32.mat",
    ]

    for url in mirrors:
        for attempt in range(1, 4):
            try:
                print(f"[*] Downloading Extended Yale B from {url} (attempt {attempt}/3)...")
                _download_file(url, mat_path)
                return mat_path
            except Exception as e:
                print(f"[!] Download attempt {attempt} failed ({url}): {e}")
                if attempt < 3:
                    time.sleep(attempt)

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
