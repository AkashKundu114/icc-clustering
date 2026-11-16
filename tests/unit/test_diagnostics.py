import pytest

from icc.diagnostics import dominant_partition_stats, partition_entropy


def test_partition_entropy_rejects_empty_observations():
    with pytest.raises(ValueError, match="at least one observation"):
        partition_entropy([])


def test_dominant_partition_stats_rejects_empty_observations():
    with pytest.raises(ValueError, match="at least one observation"):
        dominant_partition_stats([])


def test_dominant_partition_stats_rejects_misaligned_ari_values():
    with pytest.raises(ValueError, match="one score per partition"):
        dominant_partition_stats(["a", "b", "a"], aris=[0.4, 0.7])


def test_partition_entropy_and_dominant_share_for_two_partition_outcomes():
    partitions = ["a", "a", "b", "a"]
    assert partition_entropy(partitions) == pytest.approx(0.811278, abs=1e-5)

    share, dominant, dominant_ari = dominant_partition_stats(partitions, aris=[0.9, 0.8, 0.5, 0.7])
    assert share == pytest.approx(0.75)
    assert dominant == "a"
    assert dominant_ari == pytest.approx(0.9)
