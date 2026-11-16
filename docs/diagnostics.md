# Partition diagnostics

The package exposes two lightweight summaries from `icc.diagnostics`:

- `partition_entropy(partitions)` measures the Shannon entropy, in bits, of the observed distribution of distinct partition outcomes.
- `dominant_partition_stats(partitions, aris=None)` reports the share and identity of the most frequently observed partition, and optionally the ARI value associated with its first occurrence.

## Example

```python
from icc.diagnostics import dominant_partition_stats, partition_entropy

# Each item represents one complete partition outcome, not one sample label.
partitions = ["partition-A", "partition-A", "partition-B", "partition-A"]

entropy = partition_entropy(partitions)
share, dominant, _ = dominant_partition_stats(partitions)

print(f"Partition entropy: {entropy:.3f} bits")
print(f"Dominant partition: {dominant} ({share:.1%})")
```

## Interpretation

For observed outcome probabilities `p_i`, entropy is `-sum(p_i * log2(p_i))`. It is zero when every run produced the same partition and increases as the observed outcomes become more diverse. The value describes diversity in the supplied run-level outcomes; it is not a measure of per-sample assignment uncertainty, external-label accuracy, or initialization robustness by itself.

`dominant_partition_stats` selects the most frequent observed partition. If two outcomes tie, Python's insertion ordering means the first one encountered is selected. When `aris` is supplied, it must contain exactly one score per partition observation, in the same order. The returned dominant ARI is the score at the first occurrence of the selected dominant partition, not the mean ARI across all runs with that partition.

Partition values must be hashable because the implementation groups distinct outcomes using their hash identity. Use a stable tuple or another immutable representation for a full label vector, for example `tuple(labels.tolist())`.

Empty input and a length mismatch between `partitions` and `aris` raise `ValueError`. These diagnostics are descriptive summaries and do not replace paired statistical analysis or uncertainty intervals.
