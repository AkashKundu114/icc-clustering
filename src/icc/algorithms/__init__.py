"""
Clustering Algorithms: Baseline and comparative algorithms for benchmark evaluations.
"""

from typing import Callable, Dict, List

from .anchor import run_fastmvc, run_fcag
from .base import AlgorithmMetadata, BaseClusterer, validate_clustering_input
from .classical import (
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
from .cohirf import CoHiRF, run_cohirf
from .deep import run_dec
from .density import run_dbscan, run_hdbscan
from .leiden import run_leiden_snn
from .monti import (
    run_icc_v1,
    run_icc_v2,
    run_li_et_al_2019,
    run_standard_consensus,
)
from .probabilistic import run_gmm
from .sparse_kmeans import run_sparse_kmeans

_DISPATCH: Dict[str, Callable] = {
    "kmeans": run_kmeans,
    "k-means": run_kmeans,
    "run_kmeans": run_kmeans,
    "run_single_kmeans": run_single_kmeans,
    "ward": run_ward,
    "run_ward": run_ward,
    "run_single_ward": run_single_ward,
    "spectral": run_spectral,
    "run_spectral": run_spectral,
    "run_single_spectral": run_single_spectral,
    "fcm": run_fcm,
    "run_fcm": run_fcm,
    "run_single_fcm": run_single_fcm,
    "gmm": run_gmm,
    "run_gmm": run_gmm,
    "dbscan": run_dbscan,
    "run_dbscan": run_dbscan,
    "hdbscan": run_hdbscan,
    "run_hdbscan": run_hdbscan,
    "sparse_kmeans": run_sparse_kmeans,
    "sparse-kmeans": run_sparse_kmeans,
    "run_sparse_kmeans": run_sparse_kmeans,
    "leiden": run_leiden_snn,
    "leiden_snn": run_leiden_snn,
    "run_leiden_snn": run_leiden_snn,
    "fcag": run_fcag,
    "run_fcag": run_fcag,
    "fastmvc": run_fastmvc,
    "run_fastmvc": run_fastmvc,
    "dec": run_dec,
    "run_dec": run_dec,
    "cohirf": run_cohirf,
    "run_cohirf": run_cohirf,
    "standard_consensus": run_standard_consensus,
    "run_standard_consensus": run_standard_consensus,
    "li_et_al_2019": run_li_et_al_2019,
    "run_li_et_al_2019": run_li_et_al_2019,
    "icc_v1": run_icc_v1,
    "run_icc_v1": run_icc_v1,
    "icc_v2": run_icc_v2,
    "run_icc_v2": run_icc_v2,
}


def list_algorithms() -> List[str]:
    """Return all registered algorithm identifiers."""
    return sorted(list(_DISPATCH.keys()))


def get_algorithm(name: str) -> Callable:
    """Retrieve algorithm runner function by name."""
    norm = name.strip().lower().replace("-", "_").replace(" ", "_")
    if norm in _DISPATCH:
        return _DISPATCH[norm]
    raise KeyError(f"Unknown algorithm '{name}'. Available: {list_algorithms()}")


# Baselines aliases for backward compatibility
get_model = get_algorithm
list_models = list_algorithms

__all__ = [
    "BaseClusterer",
    "AlgorithmMetadata",
    "validate_clustering_input",
    "get_algorithm",
    "list_algorithms",
    "get_model",
    "list_models",
    "run_kmeans",
    "run_ward",
    "run_spectral",
    "run_fcm",
    "run_single_kmeans",
    "run_single_ward",
    "run_single_spectral",
    "run_single_fcm",
    "run_gmm",
    "run_dbscan",
    "run_hdbscan",
    "run_sparse_kmeans",
    "run_leiden_snn",
    "run_fcag",
    "run_fastmvc",
    "run_dec",
    "run_cohirf",
    "run_standard_consensus",
    "run_li_et_al_2019",
    "run_icc_v1",
    "run_icc_v2",
    "CoHiRF",
    "ModelMetadata",
]
