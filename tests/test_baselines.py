"""
Unit tests for the ICC baselines registry and wrappers (src/icc/baselines).
"""

import numpy as np
import pytest

from experiments.exp3_real_world_benchmarks.src.benchmark_models import MODELS
from src.icc.baselines import ModelMetadata, get_model, list_models

try:
    import tensorflow  # noqa: F401
    import keras  # noqa: F401
    HAS_DEEP = True
except (ImportError, Exception):
    HAS_DEEP = False


def test_list_models_categories():
    all_models = list_models()
    assert len(all_models) == 14

    single = list_models(category="single")
    assert single == ["K-Means", "Ward", "Spectral", "FCM"]

    consensus = list_models(category="consensus")
    assert consensus == ["Standard_Consensus", "Li_et_al_2019", "ICC_v1", "ICC_v2"]

    deep = list_models(category="deep")
    assert deep == ["DEC", "IDEC", "CC", "SCAN"]

    anchor = list_models(category="anchor")
    assert anchor == ["FCAG", "FastMVC"]


def test_get_model_dispatch():
    kmeans_fn = get_model("kmeans")
    assert callable(kmeans_fn)

    standard_fn = get_model("Standard_Consensus")
    assert callable(standard_fn)

    with pytest.raises(KeyError):
        get_model("non_existent_clustering_algo_999")


def test_stubs_raise_not_implemented():
    for name in ["IDEC", "CC", "SCAN"]:
        fn = get_model(name)
        with pytest.raises(NotImplementedError):
            fn(np.zeros((10, 5)), 2)


def test_run_fcag_direct():
    from src.icc.baselines.anchor import run_fcag
    rng = np.random.default_rng(42)
    X = rng.normal(size=(50, 10))
    labels, elapsed, meta = run_fcag(X, k=2, n_anchors=20, seed=42)
    assert labels.shape == (50,)
    assert set(labels).issubset({0, 1})
    assert elapsed > 0.0
    assert isinstance(meta, int)
    assert meta["method"] == "FCAG"
    assert meta["n_clusters"] == 2
    assert meta["n_anchors"] == 20


def test_run_fastmvc_direct():
    from src.icc.baselines.anchor import run_fastmvc
    rng = np.random.default_rng(42)
    X = rng.normal(size=(50, 10))
    labels, elapsed, meta = run_fastmvc(X, k=2, n_anchors=20, n_views=5, seed=42)
    assert labels.shape == (50,)
    assert set(labels).issubset({0, 1})
    assert elapsed > 0.0
    assert isinstance(meta, int)
    assert meta["method"] == "FastMVC"
    assert meta["n_clusters"] == 2
    assert meta["n_anchors"] == 20
    assert meta["n_views"] == 5




@pytest.mark.skipif(not HAS_DEEP, reason="tensorflow/keras not installed")
def test_run_dec_direct():
    from src.icc.baselines.deep import run_dec
    rng = np.random.default_rng(42)
    X = rng.normal(size=(40, 8)).astype(np.float32)
    labels, elapsed, meta = run_dec(
        X, k=2, seed=42, pretrain_epochs=5, finetune_epochs=5, dims=[8, 64, 10]
    )
    assert labels.shape == (40,)
    assert set(labels).issubset({0, 1})
    assert elapsed > 0.0
    assert isinstance(meta, int)
    assert meta["method"] == "DEC"
    assert meta["n_clusters"] == 2
    assert meta["device"] in ("cpu", "gpu")


def test_dec_missing_tensorflow_error(monkeypatch):
    import sys
    monkeypatch.setitem(sys.modules, "tensorflow", None)
    monkeypatch.setitem(sys.modules, "keras", None)
    from src.icc.baselines.deep import _check_tensorflow
    with pytest.raises(ImportError, match="TensorFlow and Keras are required for the DEC baseline"):
        _check_tensorflow()



def test_models_dict_execution():
    rng = np.random.default_rng(123)
    X = rng.normal(size=(30, 10))
    K = 2

    for name, model_fn in MODELS.items():
        if name.lower() == "dec" and not HAS_DEEP:
            continue
        try:
            pred, elapsed, lc = model_fn(X, K, seed=42)
        except (ImportError, ModuleNotFoundError) as err:
            if not HAS_DEEP and ("tensorflow" in str(err).lower() or "keras" in str(err).lower()):
                continue
            raise

        assert pred.shape == (30,)
        assert elapsed >= 0.0
        assert isinstance(lc, int)
        assert lc > 0
        assert isinstance(lc, ModelMetadata)
        assert "method" in lc


def test_model_metadata_hybrid():
    meta = ModelMetadata(42, method="test", n_samples=100)
    assert isinstance(meta, int)
    assert meta == 42
    assert int(meta) == 42
    assert meta["method"] == "test"
    assert meta.get("n_samples") == 100
    assert "method" in meta
