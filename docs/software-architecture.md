# Software architecture

The repository uses a `src/` layout. Core modules are in `src/icc/`, with an additional `src/cicc/` package for conformal/inductive components. Public paths below refer to code organization, not a guarantee that every module was used in the six-cohort saved-output analysis.

- `src/icc/consensus/`: consensus-clustering implementations, including ICC variants, GAC, AutoK, and perturbation profiling. `src/icc/consensus_v2.py` is a backward-compatibility import shim.
- `src/icc/baselines/` and `src/icc/algorithms/`: baseline and algorithm implementations and compatibility interfaces. Benchmark parity with external reference implementations is not uniformly audited.
- `src/icc/benchmarks/`: benchmark runners, model wrappers, fidelity helpers, and scaling utilities.
- `src/icc/datasets/`: domain-specific dataset loaders and a registry. `configs/datasets.yaml` stores dataset identifiers, expected shapes, and preprocessing flags.
- `src/icc/data/`: compatibility and preprocessing interfaces. The registry loader applies configured imputation, optional transforms, standardization, and label encoding.
- `src/icc/evaluation/` and `src/icc/stats/`: evaluation metrics and statistical utilities.
- `configs/`: benchmark and dataset configuration.
- `scripts/`: command-line entry points for running experiments, preparing data, fetching registry datasets, evaluating results, and reproduction compatibility.
- `tests/`: unit, integration, and regression tests.

Typical flow: a script reads YAML settings, a registry loader obtains/preprocesses data into a local cache, a benchmark runner instantiates methods, and evaluation utilities compute internal or external metrics. For new work, save immutable configuration, exact input/version identifiers, sample mappings, seeds, per-fit statuses, and output hashes. The historical six-cohort partition writer was not recovered; do not assume the generic CLI recreates it.
## ICC execution path (implementation summary)

The implementation is in [`src/icc/consensus/icc.py`](../src/icc/consensus/icc.py). The following summarizes the code defaults; it is not a claim of a recovery guarantee.

1. For each nonconstant input feature, the implementation computes a score from bias-corrected sample skewness and excess kurtosis: $(g_1^2+1)/(g_2+3c_N+10^{-5})$, with a denominator floor. In the default `pool_mode="legacy"`, it selects the highest-scoring fraction `max(0.15, 100 / D)` (capped at one) of features. The `null_calibrated` threshold at $5/9$ is an optional pool mode, not the default.
2. It repeatedly samples feature subsets from that candidate pool and fits the selected base clusterer on all rows. With `base_clusterer="auto"`, the code chooses spectral clustering at $N\le100$ and k-means above that threshold. Subspace and model seeds are generated from `random_state`.
3. For $N\le$ `dense_threshold` (default 2,000), sample stability is computed from squared co-assignment frequencies across pairs of ensemble partitions, excluding the self-comparison from the denominator. For larger $N$, the implementation estimates core samples on at most 1,000 sampled rows and then sets the reported `stability_` attribute to average co-assignment with selected anchors. These branches do not compute the same sample-level estimator.
4. Core samples are selected by a quantile of that stability score; anchors are sampled from the core. The bipartite matrix $B_{ia}$ is the fraction of base partitions that assign sample $i$ and anchor $a$ to the same cluster. Rows of $B$ are normalized, anchor affinity is $W=B^\top B$, and a normalized anchor Laplacian is eigendecomposed. The `legacy` embedding is the default; `transfer_cut` is optional. k-means assigns final labels in the embedding.
5. Out-of-sample `predict` assigns to the nearest stored cluster centroid in the selected feature pool by Euclidean distance. It is a separate extension step and does not provide a clinical prediction guarantee.

The model's `stability_` attribute is not the historical experiment's mean ARI across 435 pairs of resampled assignments. The historical six-cohort result compares pairwise partition agreement with external-label ARI; its producer and result files are unavailable in this public snapshot.
