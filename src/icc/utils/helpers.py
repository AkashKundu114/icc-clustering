"""
Shared utilities for ICC: seed control, timing, memory measurement, and logging.
"""

import contextlib
import logging
import os
import random
import time
from typing import Dict, Generator

import numpy as np


def set_seed(seed: int = 42) -> None:
    """
    Set random seeds across Python, NumPy, and optional libraries for reproducibility.

    Parameters
    ----------
    seed : int
        Integer random seed.
    """
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    # Optional torch seeding
    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass


@contextlib.contextmanager
def Timer() -> Generator[Dict[str, float], None, None]:
    """
    Context manager for measuring elapsed execution time in seconds.

    Yields
    ------
    Dict[str, float]
        Dictionary with key 'elapsed' updated when context exits.
    """
    state: Dict[str, float] = {"elapsed": 0.0}
    start = time.perf_counter()
    try:
        yield state
    finally:
        state["elapsed"] = time.perf_counter() - start


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a standard logger for ICC.

    Parameters
    ----------
    level : int
        Logging level (e.g. logging.INFO).

    Returns
    -------
    logging.Logger
    """
    logger = logging.getLogger("icc")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
