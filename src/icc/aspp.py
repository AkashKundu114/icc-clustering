"""
Backward-compatibility shim for icc.aspp -> icc.consensus.aspp.

Anchor-Space Perturbation Profiling (ASPP) is now canonically maintained in
the icc.consensus package.
"""

from icc.consensus.aspp import (
    ASPP_FAMILIES,
    AnchorSpacePerturbationProfiler,
    ASPPConfig,
)

__all__ = [
    "AnchorSpacePerturbationProfiler",
    "ASPPConfig",
    "ASPP_FAMILIES",
]
