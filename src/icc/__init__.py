"""
Invariant Core Consensus (ICC): High-Dimensional Consensus Clustering & Benchmarking Suite.
"""

from .algorithms import (
    get_algorithm,
    list_algorithms,
)
from .baselines import (
    get_model,
    list_models,
)
from .benchmarks import (
    BenchmarkResult,
    BenchmarkRunner,
    ExperimentResult,
    ExperimentRunner,
)
from .consensus import (
    GAC,
    InvariantCoreConsensus,
    InvariantCoreConsensusV2,
)
from .consensus.aspp import ASPP_FAMILIES, AnchorSpacePerturbationProfiler, ASPPConfig
from .consensus.autok import AutoKResult, compute_anchor_pac, run_icc_autok
from .core import run_clusterer
from .data import (
    bimodality_coefficient,
    build_dataset,
    canonical,
    list_datasets,
    load_dataset,
    make_noise,
    make_signal,
    pairwise_coassoc,
)
from .diagnostics import dominant_partition_stats, partition_entropy
from .evaluation import (
    adjusted_mutual_info_score,
    adjusted_rand_score,
    evaluate_all,
    evaluate_all_with_ci,
    fowlkes_mallows_score,
    normalized_mutual_info_score,
    v_measure_score,
)

__version__ = "2.2.2"

ICC = InvariantCoreConsensusV2
ICCv2 = InvariantCoreConsensusV2
ICCv1 = InvariantCoreConsensus

__all__ = [
    "__version__",
    "ICC",
    "ICCv1",
    "ICCv2",
    "GAC",
    "InvariantCoreConsensus",
    "InvariantCoreConsensusV2",
    "ASPPConfig",
    "AnchorSpacePerturbationProfiler",
    "ASPP_FAMILIES",
    "AutoKResult",
    "run_icc_autok",
    "compute_anchor_pac",
    "bimodality_coefficient",
    "build_dataset",
    "make_signal",
    "make_noise",
    "canonical",
    "pairwise_coassoc",
    "run_clusterer",
    "adjusted_rand_score",
    "normalized_mutual_info_score",
    "adjusted_mutual_info_score",
    "v_measure_score",
    "fowlkes_mallows_score",
    "evaluate_all",
    "evaluate_all_with_ci",
    "partition_entropy",
    "dominant_partition_stats",
    "get_algorithm",
    "list_algorithms",
    "get_model",
    "list_models",
    "load_dataset",
    "list_datasets",
    "BenchmarkRunner",
    "BenchmarkResult",
    "ExperimentRunner",
    "ExperimentResult",
]
