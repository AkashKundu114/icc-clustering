"""
Invariant Core Consensus (ICC): Algorithmic Package.
"""

__version__ = "2.2.0"

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

ICC = InvariantCoreConsensusV2
ICCv2 = InvariantCoreConsensusV2
ICCv1 = InvariantCoreConsensus

__all__ = [
    "__version__",
    "ICC",
    "ICCv1",
    "ICCv2",
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
