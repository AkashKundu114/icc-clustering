"""
Probabilistic clustering algorithms: GMM, GMM-BIC, GMM-ICL.
Re-exported from canonical icc.baselines.probabilistic.
"""

from icc.baselines.probabilistic import (
    ModelMetadata,
    run_gmm,
    run_gmm_bic,
    run_gmm_icl,
)

__all__ = [
    "run_gmm",
    "run_gmm_bic",
    "run_gmm_icl",
    "ModelMetadata",
]
