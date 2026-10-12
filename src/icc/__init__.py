"""
Invariant Core Consensus (ICC): Algorithmic Package.
"""

__version__ = "2.0.0"

from .consensus import InvariantCoreConsensus
from .consensus_v2 import InvariantCoreConsensusV2
from .aspp import ASPPConfig, AnchorSpacePerturbationProfiler, ASPP_FAMILIES
from .core import build_dataset, run_clusterer, pairwise_coassoc
from .metrics import (
    adjusted_rand_score,
    normalized_mutual_info_score,
    adjusted_mutual_info_score,
    v_measure_score,
    fowlkes_mallows_score,
    evaluate_all,
    evaluate_all_with_ci,
)
from .diagnostics import canonical, partition_entropy, dominant_partition_stats

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
