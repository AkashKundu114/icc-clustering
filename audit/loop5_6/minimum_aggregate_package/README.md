# Minimum aggregate-level reproduction package

This package reproduces arithmetic summaries from one aggregate CSV (72 dataset-method rows). It does **not** reproduce clustering, resampling, null controls, partition-level pairing, or uncertainty. The CSV is a derived result table; upstream data redistribution is intentionally excluded. Rights to redistribute the aggregate result still require author/source clearance before public release.

## Run

Requires Python 3.9+ and the standard library only:

```bash
python reproduce_aggregate.py
```

The script verifies the input CSV against the dynamically generated SHA-256 in `manifest.csv` and writes `recomputed.json`. A mismatch is fatal.

The six-cohort experimental protocol, recoverable historically from Git, was 30 class-stratified 80% subsamples per method/cohort, split seeds 5000-5029, fit seed 0, and pairwise ARI over intersections. This package does not reproduce that experiment because its per-fit partitions and records are unavailable.
