"""
Graph-based community detection: SNN graph with Leiden / Spectral clustering.
Re-exported from canonical icc.baselines.leiden_snn.
"""

from icc.baselines.leiden_snn import (
    ModelMetadata,
    _build_snn_matrix,
    run_leiden_snn,
    run_spectral_snn,
)

__all__ = [
    "run_leiden_snn",
    "run_spectral_snn",
    "_build_snn_matrix",
    "ModelMetadata",
]
