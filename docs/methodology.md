# Methodology and experiment scope

## Software protocol versus recovered experiment

The repository contains clustering implementations, a YAML dataset registry, benchmark utilities, and loaders. The current ICC implementation and its default feature-pool behavior are summarized in [software architecture](software-architecture.md); those implementation details must not be substituted for the historical experiment protocol below. The six-cohort protocol producer source was recovered from Git history at [commit `49f3882`](https://github.com/AkashKundu114/icc-clustering/commit/49f3882fe5385913a9af1a5b89138c6ae6d95579). This is not a contemporaneous execution record: exact historical input identity, environment, and fit invocation remain unauthenticated. A later local fresh run used that source and the available cohort caches, but its results are not publicly bundled pending data-rights review. See [reproducibility](reproducibility.md).

## Six-cohort stability analysis

The six cohorts are CNS, Colon, Leukemia, Ovarian, Prostate, and SRBCT. The reconstructed output contains 12 method labels and 72 cohort-method cells. Archived records describe 30 without-replacement draws per cohort, retaining 80% of samples, with class-stratified sampling and shared sample-index schedules across methods. The recorded model seed is fixed at 0. The labels determine the stratification proportions and the requested number of clusters. The protocol is therefore reference-label-informed, not fully label-blind.

For each cell, there are 435 unordered pairs among 30 partitions. For each pair, assignments are compared only on samples present in both subsamples; adjusted Rand index (ARI) on that intersection is averaged over the 435 comparisons. This is called pairwise subsample stability. Reuse of partitions and observations makes the pair scores dependent. It measures sensitivity to the saved row-sampling perturbations at one model-seed setting, not initialization robustness or biological reproducibility.

External alignment is calculated separately: for each real-mode partition, ARI is computed against the available reference labels for the sampled observations, then averaged over 30 draws. The 435 pairwise stability comparisons do not pair one-to-one with the 30 external ARIs. Their relationship is at the cohort-method-protocol level only.

A column-permuted control is described in the saved experiment records. Mean null stability is reported descriptively. The original partition writer and null-transformation execution trace were not recovered, so details beyond the stored metadata cannot be authenticated.

Post-hoc degeneracy summaries use several distinct rules. Rule (i) selects cells by stability and ARI thresholds (20 cells); Rule (i-prime) adds a cluster-size condition (18 cells); a method-recurrence rule selects nine cells. These criteria were not prespecified and are exploratory.

## Separate 13-dataset external benchmark

The broader benchmark evaluates external ARI separately and does not calculate resampling stability. Its saved execution lineage and method comparability are incomplete; the repository snapshot does not publish its numerical score matrix. No method-equivalence or superiority conclusion is supported here.

## Dataset preprocessing

The code-level registry is `configs/datasets.yaml`. Its default preprocessing flags specify mean imputation of missing values, optional `log1p`, feature standardization, and label encoding; individual datasets override these flags. The loader implementation applies operations according to those settings. The exact historical cache-to-experiment preprocessing lineage was not authenticated. See [Datasets](datasets.md) before downloading any third-party data.
