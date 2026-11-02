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
