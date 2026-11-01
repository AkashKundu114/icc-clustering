"""
Conformal Inductive Consensus Clustering (CICC) wrapper.
"""

from cicc.conformal import ConformalClusterer, ConformalResult
from cicc.decoy import DecoyFeatureGating
from cicc.inductive import InductiveConsensusClusterer
from cicc.memory import InductiveConsensusMemory

__all__ = [
    "ConformalClusterer",
    "ConformalResult",
    "DecoyFeatureGating",
    "InductiveConsensusClusterer",
    "InductiveConsensusMemory",
]
