# Supplementary methods — Loop 6.0 candidate

## Experimental unit and saved records
The primary analysis contains six cohorts and 12 method labels, yielding 72 cohort-method cells. Each cell has 30 saved real-mode partitions and 30 column-permuted-null partitions. Archived metadata indicate the same 80% without-replacement, class-stratified sample-index schedule across methods for each cohort and repeat, repeat seeds 5000–5029, null seeds 6000–6029, and fixed model seed 0. This metadata does not authenticate the missing producer.

## Stability
For every unordered pair among 30 partitions (435 pairs), retain only sample indices shared by both partitions, then compute the adjusted Rand index (ARI) between their cluster assignments on that intersection. The cell stability is the arithmetic mean of those 435 ARIs. Pairwise values are dependent because partitions and samples recur.

## External reference alignment
For each real-mode partition, compute ARI between predicted assignments and reference labels for its sampled observations; average over 30 draws. The same sampling schedule links both summaries at protocol level, but the 435 pair scores do not pair one-to-one with the 30 external ARIs. Labels informed class-stratified sampling and the requested number of clusters.

## Descriptive contrast and weighting
For each cell, difference = mean pairwise stability − mean external ARI. Aggregate mean is the arithmetic mean of 72 cell differences; because each cohort contributes exactly 12 cells, the resulting mean gives each cohort equal total weight. The reported median is the median of 72 cell differences. This arithmetic contrast has not been calibrated as a universal validity measure.

## Selection and inference
Threshold and recurrence subsets are post-hoc. The 20-cell Rule (i), 18-cell Rule (i-prime), and nine-cell recurrence subset are distinct and exploratory. No pair-level inferential test is performed. Six convenience cohorts do not support confirmatory population inference; the main candidate omits a confidence interval.

## Reproduction status
The results are recomputed from locally recovered saved arrays and record files. No original fit was rerun, the historical output producer is not authenticated, and public Tier 2 access is unavailable.
