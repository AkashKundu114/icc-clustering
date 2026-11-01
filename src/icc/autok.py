"""
Automated Model Order Selection (Unknown-K) for Invariant Core Consensus.
"""

from .consensus.autok import AutoKResult, compute_anchor_pac, run_icc_autok

__all__ = [
    "AutoKResult",
    "compute_anchor_pac",
    "run_icc_autok",
]
