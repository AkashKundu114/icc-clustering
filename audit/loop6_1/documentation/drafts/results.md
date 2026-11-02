# Verified results and scope

## Six-cohort stability and reference-label alignment

A direct reconstruction from locally recovered saved assignments and accompanying records produced 72 cohort-method cells across CNS, Colon, Leukemia, Ovarian, Prostate, and SRBCT. For each cell, pairwise stability is the average ARI over 435 partition pairs on their overlapping samples; external alignment is the average ARI to reference labels over 30 partitions.

| Quantity | Reconstructed value | Interpretation
|---|---:|---|
| Mean pairwise subsample stability | 0.516586 | Equal-cell descriptive average over 72 cells. |
| Mean external reference-label ARI | 0.052312 | Equal-cell descriptive average over the same 72 cells. |
| Mean cell difference (stability − ARI) | 0.464274 | Arithmetic contrast between distinct summaries, not a calibrated validity scale. |
| Median cell difference | 0.448407 | Median of 72 cell-level differences. |
| Mean column-permuted-null stability | 0.006620 | Descriptive null-arm summary. |

Each cohort contributes 12 of the 72 method-cells, so the arithmetic means are also equal-weighted across the six observed cohorts. Cells and pairwise scores are dependent. The values support a bounded observation under the saved protocol; they do not establish a population-wide law, clinical validity, or that stability is generally useless. Reference labels informed sample stratification and requested K. The historical fit producer remains unauthenticated.

The nine-cell result is post-hoc and exploratory: it was selected using thresholds and recurrence after examining the same cohort-method outcomes. It is not independent confirmation and is not used here as a primary result.

## Separate 13-dataset external-ARI benchmark

The separate saved-score matrix contains 3,000 rows for 13 datasets and 12 methods, with 156 complete dataset-method cells. Recalculation of dataset-wise ranks gives a Friedman statistic of 11.556213 (11 degrees of freedom; p = 0.397908); ICC-v2 has average rank 5.615385 (rank 4 of 12). This calculation is based on saved score rows, not 3,000 authenticated fit events. Some rows were copied or imported; implementations and budgets differ; the comparison does not establish superiority, equivalence, robustness, or generalization. It is not a 13-dataset stability analysis.

## Availability caveat

These detailed calculations were reconstructed locally. The clean public clone tested in the current release state can reproduce aggregate arithmetic only; the saved partitions, fit records, and caches needed for independent partition-level reproduction are absent.
