# ICC clustering research software

Python software for consensus-clustering research, including ICC and related experimental methods, baseline wrappers, dataset-loading utilities, and benchmark tools. The project studies how partition stability under resampling differs from agreement with external reference labels.

## Research question

A clustering can remain similar under a chosen sampling perturbation while agreeing poorly with available reference categories. Resampling stability is not the same as external reference-label alignment, and neither by itself establishes clinical or biological validity. Sampling robustness is also distinct from sensitivity to model initialization.

## Scope and evidence

Two benchmark efforts must be read separately:

- **Six-cohort stability analysis:** CNS, Colon, Leukemia, Ovarian, Prostate, and SRBCT; 12 method labels; 72 cohort-method cells. Reconstructed from locally recovered saved partitions, it yielded mean stability 0.516586, mean reference-label ARI 0.052312, mean cell difference 0.464274, median difference 0.448407, and mean column-permuted-null stability 0.006620. These are descriptive results from saved outputs. The original execution producer was not authenticated, and the required partitions and caches are not present in a clean public clone.
- **Thirteen-dataset external-ARI benchmark:** a separate saved-score comparison across 13 datasets and 12 methods. Its Friedman calculation is not stability evidence and does not establish ICC superiority.

ICC/ICC-v2 is an exploratory method in this research. This project does not claim universal superiority, clinical utility, causal mechanisms, or guarantees of generalization.

## Software capabilities

- Configurable consensus-clustering implementations and baseline wrappers.
- Dataset registry and loaders with preprocessing options.
- Benchmark, evaluation, and statistical utilities.
- CLI scripts for configuration-driven runs and result evaluation.

See [docs/index.md](docs/index.md) for the full guide.

## Installation

Python >= 3.10 is declared in package metadata. Install the project and its core dependencies with:

```bash
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering
python -m pip install -e .
```

Optional groups are listed in `pyproject.toml`; some methods require additional packages. Installation does not download all datasets or reproduce the published empirical analyses.

## Quick start

```python
import numpy as np
from icc import ICC

rng = np.random.default_rng(42)
X = rng.normal(size=(120, 40))
model = ICC(n_clusters=3, n_base_models=10, n_anchors=20, random_state=42)
labels = model.fit_predict(X)
print(labels.shape)  # (120,)
```

This is an API smoke example using synthetic data, not a reproduction of either benchmark. The public API and parameters may vary by method; consult the code and documentation.

## Reproduction

Only Tier 1 aggregate arithmetic was tested successfully in a fresh clone. Tier 2 partition-level reproduction is unavailable because partitions, fit records, and caches are absent. Tier 3 full experimental reproduction was not run; the historical partition producer and execution lineage were not recovered. See [docs/reproducibility.md](docs/reproducibility.md).

## Dataset access

The repository does not include benchmark raw data or caches. Source locations, registry dimensions, and unresolved rights are summarized in [docs/datasets.md](docs/datasets.md). Dataset terms are source-specific and may restrict redistribution of processed data and derived records. Yale B images must not be redistributed absent permission.

## Limitations

The six-cohort result is descriptive and based on locally recovered outputs; its historical generation is unauthenticated. Sampling was class-stratified and K was reference-derived. Pairwise comparisons are dependent; the nine-cell subset is post-hoc. The 13-dataset ARI benchmark is separate and has saved-row provenance and method-comparability limitations. See [docs/limitations.md](docs/limitations.md).

## Citation and publication status

Citation metadata are in [CITATION.cff](CITATION.cff). The software is MIT-licensed; this licence does not apply to third-party datasets. No verified publication DOI is currently asserted.
