"""
Anchor-based scalable clustering algorithms: FastMVC and FCAG.
Re-exported from canonical icc.baselines.anchor.
"""

from icc.baselines.anchor import (
    ModelMetadata,
    construct_anchor_bipartite_graph,
    run_fastmvc,
    run_fcag,
)

__all__ = [
    "construct_anchor_bipartite_graph",
    "run_fcag",
    "run_fastmvc",
    "ModelMetadata",
]
