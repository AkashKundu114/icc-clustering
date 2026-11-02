# Statistical analysis

## Estimands

For each cohort-method cell in the reconstructed six-cohort design, stability was defined as the mean of ARIs across all unordered pairs of saved partitions, comparing assignments only on samples shared by both partitions. External reference alignment was calculated as the mean ARI between each real-mode partition and the reference labels for its sampled observations. The summaries share cohort, method, and sampling design, but are not paired one-to-one. Pairwise values reuse partitions and observations and must not be treated as independent measurements.

A descriptive cell contrast is mean pairwise stability minus mean external ARI. The contrast subtracts summaries over different comparison populations; it is not a calibrated general-purpose validity score. The public snapshot does not include an authorized numerical result table for these calculations.

## Weighting and uncertainty

A cell-weighted mean averages the cohort-method summaries. In a balanced design, with an equal number of method cells per cohort, it also gives each cohort equal total weight. A cell median remains a median over the individual cell differences. The six available biomedical cohorts are not established as a probability sample from a target population, and the public documentation does not present bootstrap intervals as confirmatory inference. Repeated partitions and pairwise comparisons are not substitutes for independent cohorts.

## Post-hoc analyses

Threshold-based non-degeneracy and recurrence subsets were selected after the original analysis and are exploratory. The saved-output verifier reports the non-degeneracy screen separately from its intersection with the original stability/ARI rule. The repeat screen uses a 5% minimum cluster fraction in at least 27 of 30 repeats and requires predicted K to be no smaller than the reference-class count; this makes the screen label-informed. Subset statistics must not be interpreted as independent confirmation or used to choose the primary result.

## Separate external benchmark

The broader external-ARI benchmark is a different experiment from the six-cohort stability analysis. It ranks saved dataset-method score summaries; it does not calculate resampling stability. Without a public authorized score matrix, matched execution records, and comparable method implementations/budgets, no inferential ranking or superiority claim is presented here.
