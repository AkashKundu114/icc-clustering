# Expanded statistical analysis

## Scope and recomputation

Executed `python audit/loop5_5/run_loop5_5_audit.py` against the local bytes of `subsample_stability_summary.csv` and `results.json`. Hashes are calculated in the script, not embedded as assumed evidence. Outputs: `stability_recomputed_statistics.json`, `stability_recomputed_per_dataset.csv`, `stability_leave_one_out.csv`, `friedman_recomputed.json`, and `friedman_raw_cell_recomputation.csv`.

The 72-cell descriptive values recompute exactly: mean stability 0.516586, mean external ARI 0.052312, direct mean difference 0.464274. The difference is calculated cellwise as stored subsample stability minus stored subsample external ARI, then averaged equally over 72 dataset–method aggregates. Median direct difference is **0.448407**, not the 0.4700 asserted in Loop 5.4. Dataset and method weighted means coincide because this table is balanced. There is one aggregate per cell, not 72 independent repetitions and not raw uncertainty observations.

The published “nine-cell” claim is not reproduced by the stored Boolean `rule_i_stable_but_wrong`: the file marks 20 rows true. Its exact selection rule and nine-row derivation therefore require reconciliation; it remains a selected conditional description and cannot confirm the primary result independently.

## Sensitivity and inference limits

The script recomputes every leave-one-dataset and leave-one-method mean gap. These are deterministic descriptive sensitivities on the same 72 aggregate cells. Since additional datasets lack stability, no biomedical/non-biomedical heterogeneity comparison, expanded dataset-level relationship, label-semantics sensitivity, or consistent-method expansion is estimable. No cell-level significance test or dataset bootstrap is warranted from this artifact. Dataset count for the paired aggregate analysis remains six, but raw repeated observations and hierarchical uncertainty are unavailable.

## Finding

The direction and magnitude of the six-cohort *aggregate table* remain materially as previously reported. This is descriptive replication from a local ignored summary, not independent reproduction from raw partitions or subsamples. Expansion to 13 is unsupported. Statistical evidence status: DESCRIPTIVE ONLY; population-level inference and repeated-observation uncertainty are UNVERIFIED.
