# Stability–accuracy reconstruction

The FYP recovery added the lowest-level available artifacts. Recomputed from 4,320 saved partitions and per-fit records: 6 cohorts × 12 methods × 30 real/null repeats. For each real cell, stability is the mean of 435 pairwise intersection ARIs; external ARI is the mean of 30 repeat-specific ARIs. Cell gap is **cell mean stability minus cell mean external ARI**. The reported aggregate gap averages the 72 cell gaps equally (cell-weighted); it is not a single paired-replicate subtraction or “excess validity” quantity.

- Mean cell stability: 0.5165860621
- Mean cell external ARI: 0.0523121822
- Mean cell gap: 0.4642738799
- Median cell gap: 0.4484068169
- Independently recalculated null stability: 0.0066196808
- Per-cell underlying observations: 30 repeat ARIs and 435 dependent pairwise ARIs; all methods share cohort/repeat partitions.

All 72 saved summary cells agree with partition recomputation within 1.12e-16 for stability and 9.72e-17 for ARI; per-repeat ARIs match saved fit records exactly. All 4,320 fit statuses are success; no malformed records or split mismatches. Thus the previous reported mean gap 0.464274 and median 0.448407 are **numerically confirmed from recovered local run-level artifacts**, subject to unverified cache-to-run lineage and non-public availability. This did not rerun model fits.

Equal-cell mean gap is also equal-weight across datasets and methods because the grid is balanced (6×12). Dataset-weighted and method-weighted means therefore equal the cell-weighted mean here; that coincidence would not hold with missing cells. Per-cohort and per-method means are in `cohort_and_method_results.csv`; every cell with repeat counts and source agreement is in `recomputed_stability_accuracy.csv`. Leave-one-out descriptive sensitivities are in `statistical_sensitivity_results.csv`.
