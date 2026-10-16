"""
ICC Configuration Subpackage.

Provides configuration loading, schema resolution, and parameter defaults:
- load_config(name_or_path): Load arbitrary YAML configuration
- load_dataset_config(): Load configs/datasets.yaml
- load_baseline_config(): Load configs/baselines.yaml
- load_experiment_defaults(): Load configs/experiment_defaults.yaml
- get_config_dir(): Return Path to the configs directory
"""

from pathlib import Path
from typing import Any, Dict

import yaml

CONFIG_DIR = Path(__file__).resolve().parents[3] / "configs"


def get_config_dir() -> Path:
    """Return the absolute path to the repository configs directory."""
    if CONFIG_DIR.exists():
        return CONFIG_DIR
    # Fallback to local working directory
    local = Path("configs").resolve()
    if local.exists():
        return local
    return CONFIG_DIR


def load_config(filename: str) -> Dict[str, Any]:
    """Load a YAML configuration file by name or relative path."""
    cfg_dir = get_config_dir()
    path = cfg_dir / filename if not Path(filename).is_absolute() else Path(filename)
    if not path.suffix:
        path = path.with_suffix(".yaml")
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_dataset_config() -> Dict[str, Any]:
    """Load declarative dataset configurations (configs/datasets.yaml)."""
    return load_config("datasets.yaml")


def load_baseline_config() -> Dict[str, Any]:
    """Load baseline algorithm configurations (configs/baselines.yaml)."""
    return load_config("baselines.yaml")


def load_experiment_defaults() -> Dict[str, Any]:
    """Load global experiment hyperparameters (configs/experiment_defaults.yaml)."""
    return load_config("experiment_defaults.yaml")


__all__ = [
    "CONFIG_DIR",
    "get_config_dir",
    "load_config",
    "load_dataset_config",
    "load_baseline_config",
    "load_experiment_defaults",
]
