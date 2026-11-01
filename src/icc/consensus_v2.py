"""
Backward-compatibility shim for icc.consensus_v2 -> icc.consensus.

All consensus clustering implementations are now maintained in the canonical
icc.consensus package.
"""

from icc.consensus.icc import (
    GAC,
    InvariantCoreConsensus,
    InvariantCoreConsensusV2,
)

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
]
