"""
Classical single-model clustering baselines: K-Means, Ward, Spectral, FCM.
"""

from icc.baselines.classical import (
    ModelMetadata,
    run_fcm,
    run_kmeans,
    run_single_fcm,
    run_single_kmeans,
    run_single_spectral,
    run_single_ward,
    run_spectral,
    run_ward,
)

__all__ = [
    "ModelMetadata",
    "run_kmeans",
    "run_ward",
    "run_spectral",
    "run_fcm",
    "run_single_kmeans",
    "run_single_ward",
    "run_single_spectral",
    "run_single_fcm",
]
