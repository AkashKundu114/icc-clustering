"""
ICC Evaluation Subpackage.

Provides statistical clustering evaluation metrics and partition stability diagnostics:
- evaluate_all, evaluate_all_with_ci
- adjusted_rand_score, normalized_mutual_info_score, adjusted_mutual_info_score
- v_measure_score, fowlkes_mallows_score
- partition_entropy, dominant_partition_stats, canonical
"""

from ..core import canonical
from ..diagnostics import dominant_partition_stats, partition_entropy
from ..metrics import (
    adjusted_mutual_info_score,
    adjusted_rand_score,
    evaluate_all,
    evaluate_all_with_ci,
    fowlkes_mallows_score,
    normalized_mutual_info_score,
    v_measure_score,
)

__all__ = [
    "evaluate_all",
    "evaluate_all_with_ci",
    "adjusted_rand_score",
    "normalized_mutual_info_score",
    "adjusted_mutual_info_score",
    "v_measure_score",
    "fowlkes_mallows_score",
    "canonical",
    "partition_entropy",
    "dominant_partition_stats",
]
