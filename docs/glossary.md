# Glossary

- **Adjusted Rand Index (ARI):** An external partition similarity measure that adjusts pair agreement for chance, calculated between a clustering assignment and a supplied reference partition. It evaluates alignment to that reference; it does not establish that the reference is complete biological truth.
- **Consensus clustering:** A procedure that combines information from multiple partitions, often through pairwise co-assignment frequencies or a related consensus representation.
- **Degenerate partition:** A clustering output with a pathological structure for the intended analysis, such as one cluster or a tiny cluster under a prespecified rule. The exact rule must be reported.
- **External reference alignment:** Agreement between a clustering output and labels supplied independently of the clustering objective. If labels affect preprocessing, K, or sampling, the evaluation is not fully label-blind.
- **ICC:** Invariant Core Consensus, the consensus-clustering method implemented in this repository.
- **ICCv2:** A compatibility alias for the same `InvariantCoreConsensusV2` estimator exported as `ICC`; it does not select a different algorithm. The older `InvariantCoreConsensus` class is a distinct legacy implementation.
- **Initialization robustness:** Reproducibility when model initialization changes. This differs from resampling stability.
- **Resampling stability:** Agreement among clustering outputs generated after changing the sampled observations according to a specified protocol. It is conditional on that protocol and model settings.
- **Sampling robustness:** Sensitivity to changes in which observations are included.
- **Stability-accuracy discordance:** The empirical possibility that a partition is reproducible under a stated perturbation protocol while showing weak alignment with available external labels. The phrase does not imply a universal trade-off or law.
