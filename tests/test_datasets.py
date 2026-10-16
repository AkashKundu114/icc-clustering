"""
Unit tests for the ICC dataset registry and loaders (src/icc/datasets).
"""

import numpy as np
import pytest

from src.icc.datasets import (
    DatasetInfo,
    get_dataset_info,
    list_datasets,
    load_dataset,
    preprocess_dataset,
)
from src.icc.datasets.image import load_coil20
from src.icc.datasets.scrnaseq import load_tabula_muris
from src.icc.datasets.text import load_rcv1

try:
    import scanpy  # noqa: F401
    HAS_SCANPY = True
except (ImportError, Exception):
    HAS_SCANPY = False


def _is_zheng68k_cached():
    from src.icc.datasets.scrnaseq import _DEFAULT_CACHE
    return (_DEFAULT_CACHE / "zheng68k.npz").exists()


def test_list_datasets():
    enabled = list_datasets(enabled_only=True)
    all_ds = list_datasets(enabled_only=False)

    assert len(enabled) == 13
    assert len(all_ds) == 13

    enabled_names = {d.name for d in enabled}
    expected_enabled = {
        "sonar", "madelon", "colon", "srbct", "cns", "leukemia", "prostate", "ovarian",
        "newsgroups20", "isolet", "indian_pines", "yale_b", "zheng68k"
    }
    assert enabled_names == expected_enabled


def test_get_dataset_info():
    info = get_dataset_info("leukemia")
    assert isinstance(info, DatasetInfo)
    assert info.name == "leukemia"
    assert info.domain == "genomics"
    assert info.expected_N == 72
    assert info.expected_D == 7129
    assert info.expected_K == 2
    assert info.enabled is True

    info_ng = get_dataset_info("newsgroups20")
    assert info_ng.name == "newsgroups20"
    assert info_ng.domain == "text"
    assert info_ng.expected_N == 18846
    assert info_ng.expected_D == 10000
    assert info_ng.expected_K == 20
    assert info_ng.enabled is True

    info_isolet = get_dataset_info("isolet")
    assert info_isolet.name == "isolet"
    assert info_isolet.domain == "audio"
    assert info_isolet.expected_N == 7797
    assert info_isolet.expected_D == 617
    assert info_isolet.expected_K == 26
    assert info_isolet.enabled is True

    info_ip = get_dataset_info("indian_pines")
    assert info_ip.name == "indian_pines"
    assert info_ip.domain == "hyperspectral"
    assert info_ip.expected_N == 10249
    assert info_ip.expected_D == 200
    assert info_ip.expected_K == 16
    assert info_ip.enabled is True

    info_yb = get_dataset_info("yale_b")
    assert info_yb.name == "yale_b"
    assert info_yb.domain == "image"
    assert info_yb.expected_N == 2414
    assert info_yb.expected_D == 1024
    assert info_yb.expected_K == 38
    assert info_yb.enabled is True

    info_zheng = get_dataset_info("zheng68k")
    assert info_zheng.name == "zheng68k"
    assert info_zheng.domain == "scrnaseq"
    assert info_zheng.expected_N == 700
    assert info_zheng.expected_D == 765
    assert info_zheng.expected_K == 10
    assert info_zheng.enabled is True

    with pytest.raises(KeyError):
        get_dataset_info("non_existent_dataset_12345")


def test_load_cached_genomics():
    # Load colon from existing cache
    X, y, meta = load_dataset("colon")
    assert X.shape == (62, 2000)
    assert len(y) == 62
    assert meta["K"] == 2
    assert meta["name"] == "colon"


def test_load_20newsgroups():
    # Load newsgroups20 via unified registry loader
    X, y, meta = load_dataset("newsgroups20")
    assert isinstance(X, np.ndarray)
    assert isinstance(y, np.ndarray)
    assert X.shape == (18846, 10000)
    assert len(y) == 18846
    assert meta["K"] == 20
    assert meta["name"] == "newsgroups20"
    assert meta["d_over_n"] == 0.53


def test_load_isolet():
    # Load isolet via unified registry loader
    X, y, meta = load_dataset("isolet")
    assert isinstance(X, np.ndarray)
    assert isinstance(y, np.ndarray)
    assert X.shape == (7797, 617)
    assert len(y) == 7797
    assert meta["K"] == 26
    assert meta["name"] == "isolet"
    assert meta["d_over_n"] == 0.08


def test_load_indian_pines():
    # Load indian_pines via unified registry loader
    X, y, meta = load_dataset("indian_pines")
    assert isinstance(X, np.ndarray)
    assert isinstance(y, np.ndarray)
    assert X.shape == (10249, 200)
    assert len(y) == 10249
    assert meta["K"] == 16
    assert meta["name"] == "indian_pines"
    assert meta["d_over_n"] == 0.02


def test_load_yale_b():
    # Load yale_b via unified registry loader
    X, y, meta = load_dataset("yale_b")
    assert isinstance(X, np.ndarray)
    assert isinstance(y, np.ndarray)
    assert X.shape == (2414, 1024)
    assert len(y) == 2414
    assert meta["K"] == 38
    assert meta["name"] == "yale_b"
    assert meta["d_over_n"] == 0.42


@pytest.mark.skipif(
    not HAS_SCANPY and not _is_zheng68k_cached(),
    reason="scanpy not installed and zheng68k not cached",
)
def test_load_zheng68k():
    # Load zheng68k via unified registry loader
    X, y, meta = load_dataset("zheng68k")
    assert isinstance(X, np.ndarray)
    assert isinstance(y, np.ndarray)
    assert X.shape == (700, 765)
    assert len(y) == 700
    assert meta["K"] == 10
    assert meta["name"] == "zheng68k"
    assert meta["d_over_n"] == 1.09


def test_stubs_raise_not_implemented():
    with pytest.raises(NotImplementedError):
        load_rcv1()
    with pytest.raises(NotImplementedError):
        load_coil20()
    with pytest.raises(NotImplementedError):
        load_tabula_muris()



def test_preprocess_dataset():
    raw_X = np.array([
        [1.0, np.nan, 3.0],
        [2.0, 4.0, np.nan],
        [3.0, 6.0, 9.0],
    ])
    raw_y = np.array(["a", "b", "a"])

    X, y = preprocess_dataset(raw_X, raw_y, impute_nan=True, standardize=True)
    assert not np.isnan(X).any()
    assert X.shape == (3, 3)
    assert set(np.unique(y)) == {0, 1}


def test_scanpy_not_installed_error(monkeypatch):
    import sys
    monkeypatch.setitem(sys.modules, "scanpy", None)
    from src.icc.datasets.scrnaseq import _check_scanpy
    with pytest.raises(ImportError, match="scanpy is required for scRNA-seq datasets"):
        _check_scanpy()

