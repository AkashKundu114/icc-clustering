"""
Conformal Inductive Consensus Clustering (CICC)
==============================================
A unified framework combining:
1. Bipartite anchor graph consensus clustering.
2. Target-decoy / knockoff feature gating with False Discovery Rate (FDR) control.
3. Finite-sample split-conformal cluster assignment with valid coverage guarantees.
4. Conformal abstention for novel cluster discovery and agent long-term memory.
"""

from .conformal import ConformalClusterer, ConformalResult
from .decoy import DecoyFeatureGating
from .inductive import InductiveConsensusClusterer
from .memory import InductiveConsensusMemory

__all__ = [
    "ConformalClusterer",
    "ConformalResult",
    "DecoyFeatureGating",
    "InductiveConsensusClusterer",
    "InductiveConsensusMemory",
]
