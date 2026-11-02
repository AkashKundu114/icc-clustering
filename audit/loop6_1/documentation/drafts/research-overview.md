# Research overview

Clustering methods produce groups without requiring a target label during fitting. Researchers often perturb the input data and ask whether the resulting assignments remain similar. Such repeatability is useful information, but it is different from whether assignments agree with an available reference classification.

This project examines that distinction in high-dimensional biomedical clustering. The central question is bounded: under a specified row-subsampling protocol, can partitions show substantial agreement with one another while having low adjusted Rand index (ARI) against the supplied cohort labels? A positive observation would show that stability and reference-label alignment answer different questions; it would not establish that one metric is a universal measure of clustering quality.

Two experiments must be kept separate:

1. **Six-cohort stability analysis.** Six biomedical cohorts, 12 method labels, and saved assignments are used to calculate pairwise subsample stability and reference-label ARI. The calculation has been reconstructed from local saved outputs. The historical writer and execution chain are not authenticated, and the raw partitions are not present in a clean public clone.
2. **Thirteen-dataset external-ARI benchmark.** A separate collection of saved score rows compares external ARI across 13 datasets and 12 methods. It does not measure stability on 13 datasets and does not expand the stability analysis. Its score rows include copied or imported entries and methods with different implementations and computational budgets.

ICC and ICC-v2 are software methods explored by this project. The available benchmark does not establish universal or statistical superiority. The repository is best used as a research codebase for inspecting and extending consensus-clustering methods, with empirical claims interpreted under the evidence limitations documented here.
