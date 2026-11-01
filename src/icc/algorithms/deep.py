"""
Deep clustering baselines: DEC, IDEC, Contrastive Clustering, SCAN.
Re-exported from canonical icc.baselines.deep.
"""

from icc.baselines.deep import (
    ModelMetadata,
    _check_tensorflow,
    build_autoencoder,
    run_contrastive_clustering,
    run_dec,
    run_idec,
    run_scan,
    target_distribution,
)

__all__ = [
    "run_dec",
    "run_idec",
    "run_contrastive_clustering",
    "run_scan",
    "build_autoencoder",
    "target_distribution",
    "_check_tensorflow",
    "ModelMetadata",
]
