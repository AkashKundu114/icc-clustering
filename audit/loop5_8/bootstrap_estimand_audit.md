# Bootstrap estimand audit

## Evidence inspected

The exact current repository has no `paper/manuscript/main.tex`; the file referenced in prior loops is unavailable in this checkout. The reviewed archived manuscript is `paper/archive/main_dami_revision_historical.tex` (historical manuscript, not authenticated as the target final). Its abstract and contribution claim report a cell-weighted nondegenerate gap of 0.485376 with cohort-bootstrap 95% CI [0.379, 0.662]. Historical code inspected: `D:/Final Year Project/scripts/audit_degeneracy.py` and `scripts/make_stability_outputs.py`; aggregate inputs used: `audit/loop5_7/recomputed_cell_results.csv` (60 eligible cells derived from recovered partitions). No model reruns were done.

The nondegenerate population is Rule (i′): a method-cohort cell is retained when its smallest cluster is at least 5% of the sampled partition in at least 27 of 30 repeats (`degenerate_repeats_5pct <= 3`). It contains 60 cells: CNS 8, Colon 11, Leukemia 11, Ovarian 11, Prostate 9, SRBCT 10. The gap is `mean_stability - mean_external_ARI`, with each component first computed as the cell's mean over its saved pairwise (435) and repeat (30) values.

## Estimands and results

Estimand 1 weights every eligible cohort-method cell equally: the descriptive point estimate is **0.485376**. For a cluster bootstrap that targets this cell-weighted estimand, each draw samples six cohort labels and pools all selected cohort copies' cells before averaging. With seed 42 and 10,000 resamples, its percentile interval is **[0.377121, 0.644985]**. This gives greater weight to cohorts contributing more eligible methods.

Estimand 2 computes the mean of each cohort's eligible-method mean, then weights the six cohorts equally: **0.499925**. Its seed-42, 10,000-resample cohort-cluster percentile interval is **[0.378581, 0.661716]**. This targets the mean of the represented cohort means, but a broader cohort-population interpretation requires a defensible sampling frame/exchangeability assumption that is not established. The historical sequential-RNG path gives **[0.381104, 0.653002]** for this same equal-cohort estimand.

Estimand 3 is the cohort-cluster resampling procedure, not a third target quantity: use the cell-weighted ratio statistic for E1 or the mean of cohort means for E2, keeping each sampled cohort's complete eligible-method structure. Results for E1, E2 and the historical RNG variant are shown separately in the CSV. This avoids treating methods or the 435 dependent pairwise comparisons as independent units. Six clusters make percentile intervals coarse and model-dependent. Neither provides confirmatory population-level inference.

## Historical code mismatch

`make_stability_outputs.py` uses one seed-42 array of integer cohort resamples for both all-cell and nondegenerate intervals. Its nondegenerate interval reproduces the archived manuscript rounding [0.379, 0.662], but the bootstrap statistic is equal-cohort average while the printed point estimate is an equal-cell mean (0.485376). `audit_degeneracy.py` separately uses a single RNG across two sequential `rng.choice` loops; its equal-cohort interval is [0.381104, 0.653002] and depends on this call order. The two implementations therefore do not define a stable published CI workflow. Loop 5.7's sequential-RNG reconstruction and the manuscript output should not be conflated; this audit exposes source-level implementation variants.

## Recommendation

**Remove the inferential interval from the primary manuscript.** Report the six cohort-specific descriptive results and, if desired, the 0.485376 equal-cell summary labelled as descriptive over the 60 eligible cells. State explicitly that the six cohorts are not a random sample of biomedical cohorts. If an interval is retained in supplementary exploratory material, name the estimand, give the exact resampling statistic/seed/code, and call it a cohort-clustered sensitivity interval rather than confirmatory evidence. Do not infer zero predictive utility from correlation tests, or treat a positive interval as universal generalization.

## Limitations

The calculations bootstrap reconstructed cell aggregates; they do not propagate uncertainty from repeated partitions, nor model the dependence among the 435 pairwise ARIs. The saved partitions support reconstructing each cell's descriptive metrics, but only six datasets are available. The currently reviewed manuscript source is an archive copy, so these corrections must be reconciled against the true intended manuscript before editing.
