"""
Diagnostic utilities for partition tracking, entropy, and canonicalization.
"""

from .core import canonical


def partition_entropy(partitions):
    """
    Computes Shannon entropy (in bits) over the distinct partition distribution.
    A score of 0.0 indicates 100% deterministic collapse to a single partition.
    """
    import numpy as np
    distinct = list(dict.fromkeys(partitions))
    counts = np.array([partitions.count(p) for p in distinct], dtype=float)
    probs = counts / counts.sum()
    return -np.sum(probs * np.log2(probs + 1e-12))


def dominant_partition_stats(partitions, aris=None):
    """
    Returns (dominant_share, dominant_partition, dominant_ari)
    """
    distinct = list(dict.fromkeys(partitions))
    counts = {p: partitions.count(p) for p in distinct}
    dominant_p = max(counts, key=counts.get)
    share = counts[dominant_p] / len(partitions)
    dominant_ari = None
    if aris is not None:
        idx = partitions.index(dominant_p)
        dominant_ari = aris[idx]
    return share, dominant_p, dominant_ari
