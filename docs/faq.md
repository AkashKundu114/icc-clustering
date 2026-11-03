# FAQ

### What does this repository implement?
A Python research codebase for consensus clustering, ICC variants, baseline wrappers, benchmark utilities, data loading, and evaluation. See [Software architecture](software-architecture.md).

### What is stability–accuracy discordance?
It is the possibility that partitions agree with one another under a specified perturbation but align poorly with available external reference labels. Stability and external ARI are distinct properties; the term does not mean clustering has a universal trade-off.

### How are external labels used?
In the reconstructed six-cohort protocol, labels informed class-stratified sampling and requested K, then served as the reference for ARI. This is not a fully label-blind evaluation.

### Which data are required?
The software registry covers 13 named benchmark datasets, but the six-cohort stability calculation requires local cohort caches, exact saved partitions, fit records, and sample-index alignment. These files are not included in the clean public clone. Obtain datasets only from source providers and check terms; do not redistribute uncleared data.

### How can results be reproduced?
The supported `smoke` command runs a synthetic software example only. A full six-cohort experiment was run locally, but its inputs, outputs, and detailed results are not included in this public snapshot because data and derived-output rights have not been cleared. Tier 2 reconstruction is unavailable from a clean clone; Tier 3 local execution has occurred but is not independently reproducible here. See [Reproducibility](reproducibility.md).

### Can methods be extended?
Yes, the package APIs and benchmark wrappers are extensible. New comparisons should document implementation fidelity, parameters, budgets, preprocessing, failures, and seed schedules. Do not infer that a wrapper exactly matches a published baseline without validation.

### What are the current limitations?
Six convenience cohorts, fixed model seed, label-informed sampling/K, dependent method cells, unauthenticated historical outputs, unresolved duplicate partitions, benchmark fairness limits, dataset-rights restrictions, and no public partition-level reproduction.

### Where can I find the associated publication?
The manuscript is not included or linked in this software repository. No publication DOI is asserted here. The v2.2.2 software source archive has a verified version DOI, [10.5281/zenodo.23891237](https://doi.org/10.5281/zenodo.23891237). It does not contain the research evidence needed to reproduce paper results; no reproduction archive DOI is available. See [citation status](citation.md).
