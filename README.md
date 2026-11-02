# ICC Clustering Research Software

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/AkashKundu114/icc-clustering/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/AkashKundu114/icc-clustering/actions/workflows/ci.yml)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Types: Mypy](https://img.shields.io/badge/types-mypy-blue.svg)](https://mypy-lang.org/)
[![XERJ Corpus Hub contributor](https://hub.xerj.org/contributors/AkashKundu114/badge.svg)](https://hub.xerj.org/contributors/AkashKundu114)

Python research software for consensus clustering, clustering baselines, dataset loading, evaluation, and experiment configuration. The repository is intended for researchers who want to inspect or extend the software; it does not contain the private research paper or the complete evidence needed to reproduce its six-cohort analysis.

**ICC** stands for **Invariant Core Consensus**. In this codebase, the public aliases `ICC` and `ICCv2` resolve to the same `InvariantCoreConsensusV2` estimator; they do not select different algorithms. This estimator is exploratory, and its versioned class name does not imply a verified performance advantage.

## Research question

The associated research investigates whether two properties can differ: **resampling stability**, meaning agreement among partitions after a specified sampling perturbation, and **external reference-label alignment**, meaning agreement with supplied reference categories. A stable partition need not align with those categories. Sampling robustness is distinct from sensitivity to model initialization.

ICC is an exploratory method in this research codebase. The repository does not establish universal algorithmic superiority, clinical utility, causal mechanisms, or generalization guarantees.

## Software capabilities

- Consensus-clustering implementations and baseline wrappers under `src/icc/`.
- Additional inductive and conformal components under `src/cicc/`.
- Dataset registry/configuration and local acquisition/preprocessing helpers.
- Evaluation metrics, benchmark runners, command-line scripts, examples, and tests.

See [the documentation index](docs/index.md) for the software and methodology guides.

## Research scope and available evidence

The research has two separate experiments: a six-cohort biomedical stability analysis and a 13-dataset external-ARI benchmark. The first concerns resampling stability versus reference alignment; the second concerns saved external-ARI scores only. They must not be combined as one 13-dataset stability result.

No numerical result table or run-level evidence package is included in this repository snapshot. Portable scripts under [`reproduction/`](reproduction/README.md) can recalculate summaries if a researcher supplies the saved evidence, but those inputs are not distributed here. A local saved-output reconstruction found descriptive stability/alignment differences; its historical producer and exact input ordering were not authenticated, and derived artifacts are not cleared for redistribution. See [results and evidence status](docs/results.md) and [reproducibility](docs/reproducibility.md).

## Repository layout

```text
src/          Python packages (`icc`, `cicc`)
configs/      dataset and experiment configuration
scripts/      command-line utilities
tests/        automated tests
examples/     usage examples
docs/         public software and methodology documentation
data/         registry and acquisition guidance; no research matrices
```

The package paths are retained to avoid breaking imports. There is no public manuscript, submission, or internal-audit directory in the current repository snapshot.

## Installation

Python 3.10 or newer is declared in package metadata. In a virtual environment, install the repository and its core dependencies:

```bash
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering
python -m pip install -e .
```

Some optional methods require additional dependencies. Consult `pyproject.toml` and [setup documentation](docs/setup.md). Installation does not acquire the datasets or reproduce the research analyses.

## Quick start

```python
import numpy as np
from icc import ICC

rng = np.random.default_rng(42)
X = rng.normal(size=(120, 40))
model = ICC(n_clusters=3, n_base_models=20, n_anchors=30, random_state=42)
labels = model.fit_predict(X)
print(labels.shape)  # (120,)
```

This synthetic example demonstrates the API. It is not a reproduction of either research experiment. Check the selected model's documentation and parameters before applying it to data.

## Datasets and results

The registry describes 13 dataset variants, but upstream availability does not imply permission to redistribute raw data, transformed matrices, sample identifiers, or partitions. Dataset-specific terms and exact variant identities remain unresolved for most sources. **Do not redistribute datasets or derived sample-level artifacts from this repository without confirming the applicable provider terms.** Yale B images require permission before redistribution. See [dataset access and rights](docs/datasets.md).

The current public snapshot includes no authorized numerical research-result package. The previously tested aggregate checker and its input are not included because they were located with internal audit material and the derived result is not cleared for redistribution. Tier 2 partition reproduction is unavailable; Tier 3 full experimental reproduction has not been run.

## Limitations

The saved-output stability analysis uses six convenience cohorts, reference-label-informed subsampling and a reference-derived cluster count. The model seed was fixed, so it assesses sampling sensitivity rather than initialization robustness. Cohort-method cells and pairwise comparisons are dependent. The historical partition producer is unknown, duplicate assignments remain unexplained, and public partition-level reproduction is unavailable. The broader benchmark has different methods and saved-score limitations. These restrictions preclude broad performance or clinical claims.

## Citation and publication status

For the software citation metadata, see [CITATION.cff](CITATION.cff). The repository license covers software files only, not third-party data. This software repository does not contain or link to a manuscript. Version 2.2.1 is the current tagged software release and has a verified software archive DOI, [10.5281/zenodo.23888368](https://doi.org/10.5281/zenodo.23888368). That archive contains software only, not the research-result evidence. A separate older Zenodo record is empty and has stale metadata; see [citation and release notes](docs/citation.md).

## License

The software is distributed under the MIT License; see [LICENSE](LICENSE). External datasets, resources, and derived data have separate terms.
