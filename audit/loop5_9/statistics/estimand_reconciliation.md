# Loop 5.9 statistical estimand reconciliation

## Inputs and execution

Lead independently ran `statistics/reconstruct_stats.py` against `D:\Final Year Project\data\cache`, `results/stability/partitions`, `results/stability/runs`, the saved stability summary, Pass F score CSV and CoHiRF score CSV. The script recalculated 72 cohort-method cells, 62,640 pairwise real/null stability values, 30 real external ARIs per cell and null pair values; it wrote `cell_reconstruction.csv`, `selection_reconstruction.csv`, `bootstrap_reanalysis.csv`, `benchmark_reanalysis.json`. No clustering models were fit. Input hashes are in the output JSON/manifests.

## Stability and external alignment

For each cohort-method cell, stability is the average ARI across all 435 unordered pairs of 30 partitions, calculated only on the intersection of sample indices present in the two partitions. Each observation therefore reuses partitions and samples; the 435 scores are dependent. External ARI is averaged over 30 partition-vs-reference-label comparisons. Both summaries derive from the same saved real-mode subsamples within a cohort-method, which gives protocol-level correspondence; one stability scalar is not paired to one specific external ARI draw. The real and column-permuted arms share split indices by design. Reported `stability - external ARI` is a descriptive difference between two distinct averages, not a validated scalar of “excess reproducibility over validity.”

Observed protocol: 30 overlapping, without-replacement 80% class-stratified subsets, same cohort/repeat split across methods, fixed model seed recorded as 0, repeat sub-seeds 5000–5029; null seeds 6000–6029. Since label proportions guide subset selection, this is not label-blind. Fixed model seed means sample-subset sensitivity under one initialization setting, not initialization robustness or biological replication. `K` is set from reference class count in this protocol, which is also label-informed.

## Reconstructed descriptive quantities

Direct reconstruction yielded 72/72 cells, 62,640 pair values, zero validation errors. Maximum absolute cell discrepancies versus saved aggregates: stability 1.1102e-16, external ARI 9.7145e-17, null stability 9.9150e-17. The means across the 72 cell summaries are stability 0.516586, external ARI 0.052312, mean gap 0.464274, median cell gap 0.448407, and mean null stability 0.006620. This is a local saved-partition reconstruction, not an authenticated historical fit or clean-clone reproduction.

## Selection rules

Rule (i): `mean_stability >= 0.50` and `mean_external_ARI <= 0.05`, yielding 20 cells, mean gap 0.719149. Rule (i′) adds minimum cluster fraction at least 5% in at least 27/30 real repeats, yielding 18 cells, mean gap 0.716138. Rule (iii) method recurrence among Rule(i′) cells (at least 3 cohorts) selects nine cells across FCAG, FCM and FastMVC; mean stability 0.683764, external ARI −0.002853, gap 0.686617. The threshold and Rule(i′) are post hoc. These results are exploratory; they are not independent confirmation. Separately, “18 recurrent-method × six cohort cells” is a distinct 18-cell population and must not be called the Rule(i′) 18-cell population.

## Bootstrap

E1 equal-weight cell point estimate: 0.485376. E2 equal-weight cohort mean: 0.499925. The executed script resamples six cohort labels as clusters, retaining the complete within-cohort eligible method set; it uses 10,000 draws, percentile endpoints and seed-specific results in `bootstrap_reanalysis.csv`. Its cohort order is `cns, colon, leukemia, ovarian, prostate, srbct`; seed 42 yields E2 [.378581,.653002]. Loop 5.8 used `colon, srbct, cns, leukemia, prostate, ovarian`; its seed-42 E2 endpoint was [.378581,.661716]. The independent adjudicator replicated this finite-B endpoint difference by assigning the same RNG index draws to cohort labels in different orders. It is implementation-order sensitivity, not a change in E2 point estimand. Other tested seeds also change endpoints. These intervals are sensitivity summaries over six observed cohorts, not confirmatory population inference: cohorts were not shown to be a probability sample; n=6 makes bootstrap tails coarse; cell metrics are treated as fixed and do not propagate repeat or pair uncertainty. The historical manuscript interval is equal-cohort, while its point .485 is cell-weighted. It must not be presented as an interval for E1. Recommended primary treatment: omit inferential CI and report cohort-specific descriptive values plus explicitly descriptive overall summaries.

## Broad benchmark

Separately, 3,000 local saved score rows produce 156 complete dataset-method means. Friedman on 13 dataset blocks and 12 method average ranks gives χ²=11.556213, df=11, p=0.397908; ICC-v2 rank 4/12, average rank 5.615385. This is a recalculation from saved score rows, not 3,000 authenticated fit events. The benchmark is not stability evidence and has copied/imported values and unmatched seed schedules described in `benchmark/benchmark_claim_verdict.md`.

## Scope of inference

The six convenience biomedical cohorts support a bounded descriptive observation: high pairwise agreement under this particular resampling procedure can coexist with poor ARI to the available reference labels. They do not establish that stability is generally uninformative, that ARI is complete biological truth, or that a population-level relationship holds. No cell-wise Pearson/Spearman significance or pair-level test is used as independent evidence. “Non-significant” Friedman does not demonstrate method equality.
