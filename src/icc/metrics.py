"""
Backward-compatibility shim for icc.metrics -> icc.evaluation.metrics.

All evaluation metrics are now canonically maintained in icc.evaluation.metrics.
"""

from icc.evaluation.metrics import (
    _SCIPY_HYPERGEOM_AVAILABLE,
    _SKLEARN_AVAILABLE,
    _sk_ami,
    _sk_ari,
    _sk_fm,
    _sk_nmi,
    _sk_v_measure,
    adjusted_mutual_info_score,
    adjusted_rand_score,
    evaluate_all,
    evaluate_all_with_ci,
    fowlkes_mallows_score,
    normalized_mutual_info_score,
    v_measure_score,
)

__all__ = [
    "adjusted_rand_score",
    "normalized_mutual_info_score",
    "adjusted_mutual_info_score",
    "v_measure_score",
    "fowlkes_mallows_score",
    "evaluate_all",
    "evaluate_all_with_ci",
    "_SKLEARN_AVAILABLE",
    "_SCIPY_HYPERGEOM_AVAILABLE",
    "_sk_ari",
    "_sk_nmi",
    "_sk_ami",
    "_sk_fm",
    "_sk_v_measure",
]
