# Statistical analysis

## Estimands

For each cohort-method cell, stability is the mean of 435 ARIs calculated from all unordered pairs of 30 saved partitions after restricting each pair to shared samples. External alignment is the mean of 30 ARIs comparing each real-mode partition with reference labels on its sampled observations. The summaries share cohort, method, and resampling design, but they are not one-to-one paired observations. The 435 values are not independent: each partition appears in 29 pairs and sample identities recur across overlapping subsets.

The cell-level difference is defined as mean stability minus mean external ARI. The overall mean difference averages the 72 cell differences. Every cohort contributes 12 cells, so equal-cell weighting in this balanced matrix gives each of the six cohorts equal total weight. The median is calculated across all 72 cell differences. This difference is a descriptive contrast between different comparison populations; it has not been validated as a universal metric.

## Uncertainty and cohort sensitivity

A six-cluster bootstrap is not used as confirmatory inference because these six cohorts are not established as an exchangeable probability sample from a target biomedical population; only six clusters are available, and interval endpoints were sensitive to seed/order. The earlier cell-weighted point estimate of 0.485376 and equal-cohort point estimate of 0.499925 are distinct estimands; an interval for one must not be attached to the other. The public-facing primary summary therefore reports descriptive cohort-specific values and no inferential confidence interval.

Leave-one-cohort-out analysis is an influence diagnostic, not a generalization test. The mean gap remains positive across omissions, ranging from 0.398341 after omitting Prostate to 0.497300 after omitting Leukemia. The gap magnitude is strongly influenced by Prostate (its 12-cell mean gap is 0.793939).

## Post-hoc selection

Rule (i) selected 20 cells using mean stability ≥0.50 and external ARI ≤0.05. Rule (i-prime) adds a requirement that the minimum cluster fraction is at least 5% in at least 27/30 repeats, with the recorded K-floor condition, and selected 18. A recurrence rule selected nine cells across methods appearing in at least three cohorts. The rules are not prespecified; all selected-subset statistics are exploratory. The Rule(i-prime) 18 cells differ from the 18 cells formed by three recurrent methods across all six cohorts.

## Separate Friedman calculation

The 13-dataset benchmark averages saved ARI rows within each dataset-method cell and ranks the 12 method means within each dataset, then computes a Friedman test over the 13 dataset blocks. Reported p≈0.398 does not establish equality or superiority. Saved rows include copied/imported entries and uneven method configurations, so inferential assumptions and independent fit replication are not established. This benchmark is kept separate from the stability analysis.
