# Loop 6.0 statistical methods and evidence note

## Scope and independent reconstruction

The lead statistical audit independently read the local FYP cache arrays (`D:\Final Year Project\data\cache\{cns,colon,leukemia,ovarian,prostate,srbct}.npz`), all 4,320 partition files, all 4,320 one-row Parquet records, and `results/stability/subsample_stability_summary.csv`. The executable reconstruction is `reconstruct_loop6.py`; it writes only into this Loop 6.0 directory. It performed no clustering fits. The input aggregate hash and cache SHA-256 values are recorded in `reproduction_checks.json`; the script and CSVs retain raw cell-level calculations.

The recomputation found 72 cohort-method cells, 2,160 real-mode external ARIs (30/cell), 31,320 real pairwise intersection ARIs and 31,320 null pairwise intersection ARIs (435/cell/mode). All 4,320 partition/Parquet keys and statuses checked without error; real-mode ARI matched the saved fit record within 1e-12. All methods and both real/null modes used the same ordered subset indices within each cohort-repeat (zero split mismatches). These checks support internal consistency of the saved files, not the historical generation event or model execution.

Across 72 cell summaries, mean stability is 0.5165860621, mean external ARI is 0.0523121822, mean stability-minus-ARI is 0.4642738799, median cell gap is 0.4484068169, and mean null stability is 0.0066196808. Absolute differences from saved aggregate values are at most 1.12e-16 (stability), 9.72e-17 (external ARI), and 9.92e-17 (null stability). The gap is defined as the difference between the cell's mean 435-pair stability and its mean 30-draw external ARI. It is a descriptive contrast between two distinct summaries; no interpretation as a calibrated “excess reproducibility” score is established.

## Dependence and estimands

For each cell, stability averages ARI over every unordered pair among 30 partitions, comparing only samples common to each pair. Pairwise scores are not independent: each partition occurs in 29 pairings, and the same observations are reused across overlapping subsets. External ARI averages 30 assignment-to-reference comparisons. The two summaries use the same within-cell repeat schedule and subset design but are not 1:1 paired observations. Fixed model seed 0 means the analysis probes sensitivity to the sampled observations under one initialization setting; it does not measure initialization robustness. Repeated subsamples from the same six cohorts are not independent biological replicates.

The 80% subsets are class-stratified and K is supplied from the number of reference classes. Thus the resampling and model specification are reference-label-informed. External ARI is not fully held-out evaluation, and should not be called label-blind validation. These design choices may affect both observed stability and alignment.

The primary estimands should remain descriptive: the cell-weighted average weights each eligible cohort-method cell equally; the cohort-weighted average first averages the cells within each cohort and then weights each of the six cohorts equally. The six cohorts are not shown to be an exchangeable probability sample from a defined biomedical population. Therefore the cluster bootstrap over six cohorts is, at most, a sensitivity display; it cannot justify population-level confirmatory inference. The 435 pair scores must never be used as the bootstrap unit. Primary manuscript reporting should show all six cohort-specific summaries and the bounded overall descriptive mean, with no inferential CI. If an interval is retained in supplementary material, identify the estimand, resampling unit, seed, and non-probability-sample limitation; do not attach the equal-cohort interval to the equal-cell point estimate.

## Selection audit

The original numerical criterion `mean stability >= 0.50` and `mean external ARI <= 0.05` selects 20 cells (mean gap 0.719149). Applying the 5% minimum cluster fraction to at least 27 of 30 repeats, with the historical additional condition that predicted K cannot be below reference K, produces 18 (mean gap 0.716138). This is label-informed because the K-floor uses reference-class count. Recurrence across at least three cohorts among that 18 selects nine FCAG/FCM/FastMVC cells (mean stability 0.683764; mean ARI -0.002853; mean gap 0.686617). The thresholds and recurrence subset are post hoc; they are not confirmatory evidence. The alternative “three methods by all six cohorts” 18-cell set is different and must not be conflated.

`selection_threshold_sensitivity.csv` varies the minimum cluster fraction over 2%, 5%, and 10%, and the qualifying repeat count over 27/30 versus 30/30, while holding the two original numerical cutoffs fixed. These are explicitly exploratory sensitivities, not a search for a preferred threshold. `cohort_sensitivity.csv` shows cohort results and leave-one-cohort-out estimates. Leave-one-out is a descriptive influence check, not evidence of generalization. The Prostate cohort has the largest cohort-average gap (0.793939), and omitting it reduces the cell-weighted gap to 0.3983408; the sign remains positive in each leave-one-cohort-out calculation. This means magnitude is influenced by Prostate even though the descriptive direction is unchanged.

## Benchmark separation

The 13-dataset benchmark remains a separate external-ARI comparison. It does not contribute any observation to the six-cohort stability reconstruction. The recalculated saved-score Friedman analysis is documented in the Loop 5.9 benchmark audit; those scores are not authenticated fits and have schedule/method-fidelity issues. A nonsignificant Friedman test does not show equivalence and cannot support ICC superiority.

## Evidence classification

- **Verified for recovered bytes:** cell arithmetic, aggregate arithmetic, Parquet metadata/status consistency, the 30-repeat external ARI calculation, 435-pair calculations, and common subset index schedule.
- **Descriptive only:** cohort and method summaries, gap, null contrast, leave-one-cohort-out and threshold sensitivity.
- **Exploratory:** cohort bootstrap and post-hoc subsets.
- **Unverified:** historical producer/execution provenance, algorithm implementation fidelity of every historical fit, and population-level inference beyond these six cohorts.
- **Unsupported:** universal claims that stability lacks predictive utility or that a positive gap generalizes to all biomedical clustering.
