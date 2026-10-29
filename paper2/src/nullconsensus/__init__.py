"""
nullconsensus: Permutation-Null Calibrated Consensus Clustering for High-Dimensional Manifolds.
"""

from nullconsensus.api import NullConsensus
from nullconsensus.methods.nullgate import NullGateFeatureSelector
from nullconsensus.methods.hurdlegate import HurdleGateFeatureSelector

__version__ = "0.1.0"
__all__ = ["NullConsensus", "NullGateFeatureSelector", "HurdleGateFeatureSelector"]
