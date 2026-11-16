"""
Diagnostic utilities for partition tracking, entropy, and canonicalization.
"""


def partition_entropy(partitions):
    """Compute Shannon entropy in bits over distinct partition outcomes.

    Raises ValueError when no observations are supplied.
    """
    import numpy as np

    if partitions is None or len(partitions) == 0:
        raise ValueError("partitions must contain at least one observation")

    distinct = list(dict.fromkeys(partitions))
    counts = np.array([partitions.count(p) for p in distinct], dtype=float)
    probs = counts / counts.sum()
    return float(-np.sum(probs * np.log2(probs)))


def dominant_partition_stats(partitions, aris=None):
    """Return dominant share, partition, and its first associated ARI.

    Raises ValueError for empty observations or misaligned ARI scores.
    """
    if partitions is None or len(partitions) == 0:
        raise ValueError("partitions must contain at least one observation")
    if aris is not None and len(aris) != len(partitions):
        raise ValueError("aris must contain one score per partition observation")

    distinct = list(dict.fromkeys(partitions))
    counts = {p: partitions.count(p) for p in distinct}
    dominant_p = max(counts, key=counts.get)
    share = counts[dominant_p] / len(partitions)
    dominant_ari = None
    if aris is not None:
        dominant_ari = aris[partitions.index(dominant_p)]
    return share, dominant_p, dominant_ari
