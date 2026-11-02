# Loop 5.8 limited reproduction package

This package supports **Tier 1 aggregate verification only**. It recalculates the six-cohort descriptive arithmetic from an included aggregate CSV. It does not contain the 4,320 partition arrays, 4,320 fit records, six feature caches, 13-dataset raw benchmark scores, or complete original environment. It cannot reproduce partition-level metrics or rerun clustering.

## Contents

- `inputs/subsample_stability_summary.csv`: aggregate summary already present in the public repository's Loop 5.6 minimum package.
- `scripts/reproduce_aggregate.py`: standard-library-only aggregate arithmetic verification.
- `SHA256SUMS`: SHA-256 of package files, calculated from bytes.

## Run

From this directory, use Python 3.9 or later:

```text
python scripts/reproduce_aggregate.py
```

The script prints row/cell counts, average stability, average external ARI, average gap, and median gap. Those values summarize stored aggregate rows; they are not repeated-run reconstruction. The source inputs are derived summary records, and their original execution linkage is not authenticated.

## Coverage

- Tier 1 aggregate verification: supported.
- Tier 2 partition-level verification: unavailable in this package.
- Tier 3 full experimental reproduction: unavailable in this package.

Third-party datasets are not bundled. See the Loop 5.8 `data_rights_matrix.csv` and `reproducibility_release_plan.md` before attempting acquisition or redistribution.
