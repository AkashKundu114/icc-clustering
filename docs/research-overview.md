# Research overview

Clustering methods produce groups without requiring a target label during fitting. Researchers often perturb the input data and ask whether the resulting assignments remain similar. Such repeatability is useful information, but it is different from whether assignments agree with an available reference classification.

This project examines that distinction in high-dimensional biomedical clustering. The central question is bounded: under a specified row-subsampling protocol, can partitions show substantial agreement with one another while having low adjusted Rand index (ARI) against the supplied cohort labels? A positive observation would show that stability and reference-label alignment answer different questions; it would not establish that one metric is a universal measure of clustering quality.

Two experiments must be kept separate:

1. **Six-cohort stability analysis.** Saved assignments from six biomedical cohorts were used to calculate pairwise subsample stability and reference-label ARI. The historical writer and execution chain are not authenticated, and the local partitions are not included in this public repository snapshot.
2. **Thirteen-dataset external-ARI benchmark.** A separate benchmark compares saved external-ARI score summaries. It does not measure stability across 13 datasets and does not expand the six-cohort stability analysis. Its execution provenance and method comparability are insufficient for a superiority claim.

Invariant Core Consensus (ICC) is the method explored by this project. The public aliases `ICC` and `ICCv2` resolve to the same `InvariantCoreConsensusV2` estimator; they do not represent separate methods. The older `InvariantCoreConsensus` class is a distinct legacy implementation. The available benchmark does not establish universal or statistical superiority. The repository is best used as a research codebase for inspecting and extending consensus-clustering methods, with empirical claims interpreted under the evidence limitations documented here.
