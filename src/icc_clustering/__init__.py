"""
Inductive Consensus Clustering (ICC): Package Alias.

This module provides the `icc_clustering` namespace alias for `icc`, ensuring
full backward and forward compatibility with both `import icc` and `import icc_clustering`.
"""

import sys

from icc import (
    ASPP_FAMILIES,
    AnchorSpacePerturbationProfiler,
    ASPPConfig,
    InvariantCoreConsensus,
    InvariantCoreConsensusV2,
    __version__,
    adjusted_mutual_info_score,
    adjusted_rand_score,
    algorithm,
    build_dataset,
    canonical,
    configuration,
    dominant_partition_stats,
    evaluate_all,
    evaluate_all_with_ci,
    evaluation,
    fowlkes_mallows_score,
    normalized_mutual_info_score,
    pairwise_coassoc,
    partition_entropy,
    preprocessing,
    run_clusterer,
    v_measure_score,
)

# Alias subpackages
sys.modules[f"{__name__}.algorithm"] = algorithm
sys.modules[f"{__name__}.preprocessing"] = preprocessing
sys.modules[f"{__name__}.evaluation"] = evaluation
sys.modules[f"{__name__}.configuration"] = configuration

__all__ = [
    "__version__",
    "algorithm",
    "preprocessing",
    "evaluation",
    "configuration",
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
