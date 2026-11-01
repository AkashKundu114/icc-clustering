"""
Consensus clustering engines: Invariant Core Consensus (ICCv2, GAC, ICCv1) and ASPP.
"""

from .aspp import ASPP_FAMILIES, AnchorSpacePerturbationProfiler, ASPPConfig
from .autok import AutoKResult, compute_anchor_pac, run_icc_autok
from .conformal import (
    ConformalClusterer,
    ConformalResult,
    DecoyFeatureGating,
    InductiveConsensusClusterer,
    InductiveConsensusMemory,
)
from .icc import GAC, InvariantCoreConsensus, InvariantCoreConsensusV2

ICCv2 = InvariantCoreConsensusV2
ICC = InvariantCoreConsensusV2
ICCv1 = InvariantCoreConsensus

__all__ = [
    "ICC",
    "ICCv1",
    "ICCv2",
    "GAC",
    "InvariantCoreConsensus",
    "InvariantCoreConsensusV2",
    "AnchorSpacePerturbationProfiler",
    "ASPPConfig",
    "ASPP_FAMILIES",
    "run_icc_autok",
    "AutoKResult",
    "compute_anchor_pac",
    "ConformalClusterer",
    "ConformalResult",
    "DecoyFeatureGating",
    "InductiveConsensusClusterer",
    "InductiveConsensusMemory",
]
