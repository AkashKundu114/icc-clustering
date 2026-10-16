"""
Invariant Core Consensus (ICC): Algorithmic Package.
"""

__version__ = "2.0.0"

from .aspp import ASPP_FAMILIES, AnchorSpacePerturbationProfiler, ASPPConfig
from .consensus import InvariantCoreConsensus
from .consensus_v2 import InvariantCoreConsensusV2
from .core import build_dataset, canonical, pairwise_coassoc, run_clusterer
from .diagnostics import dominant_partition_stats, partition_entropy
from .metrics import (
    adjusted_mutual_info_score,
    adjusted_rand_score,
    evaluate_all,
    evaluate_all_with_ci,
    fowlkes_mallows_score,
    normalized_mutual_info_score,
    v_measure_score,
)

__all__ = [
    "__version__",
    "InvariantCoreConsensus",
    "InvariantCoreConsensusV2",
    "ASPPConfig",
    "AnchorSpacePerturbationProfiler",
    "ASPP_FAMILIES",
    "build_dataset",
    "run_clusterer",
    "pairwise_coassoc",
    "adjusted_rand_score",
    "normalized_mutual_info_score",
    "adjusted_mutual_info_score",
    "v_measure_score",
    "fowlkes_mallows_score",
    "evaluate_all",
    "evaluate_all_with_ci",
    "canonical",
    "partition_entropy",
    "dominant_partition_stats",
]
