"""
Unit tests for the ICC baselines registry, dispatchers, and external model wrappers.

Validates the baseline model evaluation infrastructure:
1. Taxonomy completeness across single, consensus, deep, and anchor clustering categories.
2. Dispatch mechanisms: dynamic registry lookup by canonical name or alias.
3. FastMVC and FCAG anchor-graph clustering wrappers.
4. Deep Embedded Clustering (DEC) integration and dependency isolation.
5. Benchmark runner execution parity and ModelMetadata encapsulation.
"""

import numpy as np
import pytest

from experiments.exp3_real_world_benchmarks.src.benchmark_models import MODELS
from icc.baselines import ModelMetadata, get_model, list_models

try:
    import keras  # noqa: F401
    import tensorflow  # noqa: F401
    HAS_DEEP = True
except (ImportError, Exception):
    HAS_DEEP = False


def test_list_models_categories():
    """
    Verify model registry categorization and algorithm enumeration.
    
    Validates that:
    - Exactly 14 total baseline methods are registered.
    - 'single' category contains K-Means, Ward, Spectral, and FCM.
    - 'consensus' category contains Standard Consensus, Li et al. (2019), ICC-v1, and ICC-v2.
    - 'deep' category contains DEC, IDEC, CC, and SCAN.
    - 'anchor' category contains FCAG and FastMVC.
    """
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
    """
    Verify model resolution by string key and error handling for unknown keys.
    
    Confirms that get_model returns callable clusterer wrappers for known names
    and raises KeyError when queried with an unregistered identifier.
    """
    kmeans_fn = get_model("kmeans")
    assert callable(kmeans_fn)

    standard_fn = get_model("Standard_Consensus")
    assert callable(standard_fn)

    with pytest.raises(KeyError):
        get_model("non_existent_clustering_algo_999")


def test_stubs_raise_not_implemented():
    """
    Verify placeholder stub methods raise NotImplementedError when invoked.
    """
    for name in ["IDEC", "CC", "SCAN"]:
        fn = get_model(name)
        with pytest.raises(NotImplementedError):
            fn(np.zeros((10, 5)), 2)


def test_run_fcag_direct():
    """
    Verify Fast Constrained Anchor Graph (FCAG) execution and output signature.
    
    Checks that run_fcag returns discrete cluster assignments in {0, ..., k-1},
    non-negative wall-clock execution time, and valid ModelMetadata.
    """
    from icc.baselines.anchor import run_fcag
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
    """
    Verify Fast Multi-View Clustering (FastMVC) anchor graph execution.
    
    Validates bipartite multi-view graph construction, partition validity,
    and metadata tracking across random subspaces/views.
    """
    from icc.baselines.anchor import run_fastmvc
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
    """
    Verify Deep Embedded Clustering (DEC) autoencoder pretraining and clustering.
    
    Validates end-to-end autoencoder initialization, reconstruction pretraining,
    KL-divergence cluster refinement, and device allocation metadata.
    """
    from icc.baselines.deep import run_dec
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
    """
    Verify informative ImportError is raised when deep dependencies are missing.
    """
    import sys
    monkeypatch.setitem(sys.modules, "tensorflow", None)
    monkeypatch.setitem(sys.modules, "keras", None)
    from icc.baselines.deep import _check_tensorflow
    with pytest.raises(ImportError, match="TensorFlow and Keras are required for the DEC baseline"):
        _check_tensorflow()


def test_models_dict_execution():
    """
    Verify benchmark dictionary execution parity across all available models.
    
    Iterates through the central MODELS dictionary used in real-world benchmarks,
    verifying consistent return signatures (preds, runtime, metadata) across methods.
    """
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
    """
    Verify ModelMetadata hybrid class behaves both as int and as metadata dict.
    
    Supports backward-compatible integer casting (legacy anchor count L) while
    providing rich dictionary-style metadata access (method, parameters).
    """
    meta = ModelMetadata(42, method="test", n_samples=100)
    assert isinstance(meta, int)
    assert meta == 42
    assert int(meta) == 42
    assert meta["method"] == "test"
    assert meta.get("n_samples") == 100
    assert "method" in meta
