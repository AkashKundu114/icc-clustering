# Reproduction instructions and scope

## Tier 1 available now

Clone the repository at the cited immutable commit and run:

```text
python audit/loop5_6/minimum_aggregate_package/reproduce_aggregate.py
```

This recalculates arithmetic from a tracked aggregate CSV. It does not reconstruct repeated observations.

## Tier 2 unavailable from public clone

The current public repository does not provide the six feature caches, stable sample-ID manifest, saved partition arrays or per-fit records. A researcher cannot independently recompute 30 external ARIs and 435 pairwise overlap ARIs from the clone. Do not use private local paths or ignored files as acquisition instructions. Release Tier 2 only after rights clearance and input/partition linkage are documented.

## Tier 3 not demonstrated

No authoritative original partition producer, complete immutable protocol/configuration, run-level input hashes or execution environment has been recovered. Do not attempt a purported historical rerun until these are defined. A future prospective run must use a new experiment identifier and per-fit provenance schema; it cannot authenticate historical results.

For third-party data, obtain each dataset directly from its authorized upstream and honor accession-specific terms and attribution. Dataset-specific version, retrieval date and locally computed hash must be recorded. A computed hash identifies retrieved bytes but is not upstream certification.
