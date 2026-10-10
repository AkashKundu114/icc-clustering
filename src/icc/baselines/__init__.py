"""
ICC Baselines: Pluggable baseline clustering method registry.

Auto-discovers algorithms, metadata, and entrypoints from configs/baselines.yaml.
Supports 14 methods across 4 categories:
  - Classical single-model: K-Means, Ward, Spectral, FCM
  - Consensus/Ensemble: Standard Consensus, Li et al. 2019, ICC-v1, ICC-v2
  - Deep Clustering: DEC, IDEC, Contrastive Clustering, SCAN
  - Anchor-Based Scalable: FCAG, FastMVC

Usage:
    from src.icc.baselines import get_model, list_models
    model_fn = get_model("K-Means")
    labels, runtime, meta = model_fn(X, k, seed=42)
"""

import importlib
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import yaml

from .anchor import run_fastmvc, run_fcag
from .classical import (
    ModelMetadata,
    run_fcm,
    run_kmeans,
    run_single_fcm,
    run_single_kmeans,
    run_single_spectral,
    run_single_ward,
    run_spectral,
    run_ward,
)
from .consensus import (
    run_icc_v1,
    run_icc_v2,
    run_li_et_al_2019,
    run_standard_consensus,
)
from .deep import run_dec

# Project root resolution (3 levels up from src/icc/baselines/__init__.py)
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_CONFIG_PATH = _PROJECT_ROOT / "configs" / "baselines.yaml"


def _load_baselines_yaml() -> Dict[str, Any]:
    """Parse configs/baselines.yaml registry."""
    if not _CONFIG_PATH.exists():
        return {}
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


# Static direct lookup table for fast execution without overhead
_STATIC_DISPATCH: Dict[str, Callable] = {
    "kmeans": run_kmeans,
    "k-means": run_kmeans,
    "run_kmeans": run_kmeans,
    "run_single_kmeans": run_single_kmeans,
    "ward": run_ward,
    "run_ward": run_ward,
    "run_single_ward": run_single_ward,
    "spectral": run_spectral,
    "run_spectral": run_spectral,
    "run_single_spectral": run_single_spectral,
    "fcm": run_fcm,
    "run_fcm": run_fcm,
    "run_single_fcm": run_single_fcm,
    "standard_consensus": run_standard_consensus,
    "run_standard_consensus": run_standard_consensus,
    "li_et_al_2019": run_li_et_al_2019,
    "run_li_et_al_2019": run_li_et_al_2019,
    "icc_v1": run_icc_v1,
    "run_icc_v1": run_icc_v1,
    "icc_v2": run_icc_v2,
    "run_icc_v2": run_icc_v2,
    "dec": run_dec,
    "run_dec": run_dec,
    "fcag": run_fcag,
    "run_fcag": run_fcag,
    "fastmvc": run_fastmvc,
    "run_fastmvc": run_fastmvc,
}


def list_models(category: Optional[str] = None) -> List[str]:
    """
    List available baseline model names discovered from configs/baselines.yaml.

    Parameters
    ----------
    category : str, optional
        Filter by category: 'single', 'consensus', 'deep', or 'anchor'.
        If None, returns all registered models.

    Returns
    -------
    List[str]: Display names or keys of registered methods.
    """
    cfg = _load_baselines_yaml()
    methods = cfg.get("methods", {})
    if not methods:
        # Fallback to static registry keys
        return list(_STATIC_DISPATCH.keys())

    matched: List[str] = []
    for key, entry in methods.items():
        cat = entry.get("category", "")
        if category is None or cat == category:
            matched.append(entry.get("display_name", key))
    return matched


def get_model(name: str) -> Callable:
    """
    Retrieve baseline clustering callable by algorithm name or key.

    Auto-resolves through configs/baselines.yaml and dynamic module loading.

    Parameters
    ----------
    name : str
        Algorithm identifier (e.g. 'K-Means', 'kmeans', 'Standard_Consensus', 'DEC').

    Returns
    -------
    Callable: Clustering function accepting (X, k, seed=...).

    Raises
    -------
    KeyError if the algorithm is not recognized in the registry.
    """
    norm = name.strip().lower().replace("-", "_").replace(" ", "_")

    # Fast path: check static dispatch table
    if norm in _STATIC_DISPATCH:
        return _STATIC_DISPATCH[norm]

    # Dynamic path: query configs/baselines.yaml
    cfg = _load_baselines_yaml()
    methods = cfg.get("methods", {})

    target_entry = None
    for key, entry in methods.items():
        raw_display = str(entry.get("display_name", ""))
        display = raw_display.strip().lower().replace("-", "_").replace(" ", "_")
        key_norm = str(key).strip().lower().replace("-", "_").replace(" ", "_")
        if norm in (key_norm, display):
            target_entry = entry
            break

    if target_entry is not None:
        mod_path = target_entry.get("module_path", target_entry.get("module"))
        func_name = target_entry.get("function_name", target_entry.get("function"))
        if mod_path and func_name:
            mod = importlib.import_module(mod_path)
            return getattr(mod, func_name)

    raise KeyError(
        f"Unknown baseline algorithm '{name}'. "
        f"Available models: {list_models()}"
    )


__all__ = [
    "get_model",
    "list_models",
    "run_kmeans",
    "run_ward",
    "run_spectral",
    "run_fcm",
    "run_single_kmeans",
    "run_single_ward",
    "run_single_spectral",
    "run_single_fcm",
    "run_standard_consensus",
    "run_li_et_al_2019",
    "run_icc_v1",
    "run_icc_v2",
    "run_dec",
    "run_fcag",
    "run_fastmvc",
    "ModelMetadata",
]
