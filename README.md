# Invariant Core Consensus (ICC)

A high-performance Python framework for scalable, noise-robust consensus clustering and inductive out-of-sample inference in high-dimensional regimes.

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: Passing](https://img.shields.io/badge/pytest-118%2F118%20passing-brightgreen.svg)](tests/)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Checked: Mypy](https://img.shields.io/badge/mypy-checked-blue.svg)](https://mypy-lang.org/)

---

## Overview

Consensus clustering synthesizes diverse base clusterings into an aggregated partition to discover robust latent structures without supervision. However, in extreme high-dimensional noise regimes ($D \gg N$), distance concentration severely degrades base partition fidelity, while classical $\mathcal{O}(N^2)$ co-association matrices prevent scaling to large sample sizes and preclude out-of-sample inductive inference.

**Invariant Core Consensus (ICC-v2)** resolves these challenges through five core mechanisms:

1. **Bimodality-Gated Subspace Selection (BGSS):** Unsupervised linear $\mathcal{O}(N \cdot D)$ feature screening using Sarle's Bimodality Coefficient ($BC$) with finite-sample null calibration to filter continuous unimodal distractor noise ($BC \le 5/9$) while retaining discriminative multimodal cluster signals.
2. **Exact Linear-Memory Contingency Determinacy:** An algebraic formulation that evaluates ensemble co-association directly from base contingency tables in $\mathcal{O}(M^2 N + M^2 K^2)$ time and $\mathcal{O}(N + M K)$ memory, achieving a 99.6% reduction in memory footprint over quadratic consensus.
3. **Reduced Bipartite Spectral Transfer-Cut:** Compresses consensus optimization into an $\mathcal{O}(N \cdot L)$ rectangular bipartite graph ($L \ll N$) with generalized degree and eigenvalue normalization, yielding linear scaling in $\mathcal{O}(N L^2 + L^3)$ time.
4. **Closed-Form Inductive Inference:** Stability-weighted active centroid projection executing in $\mathcal{O}(K \cdot |\mathcal{F}_{\text{active}}|)$ operations per query instance without graph recomputation, enabling real-time out-of-sample cluster assignment.
5. **Conformal Uncertainty Quantification (`cicc`):** Finite-sample distribution-free $(1 - \alpha)$ coverage guarantees with target-decoy False Discovery Rate (FDR) feature selection and automated sample triage.

---

## When to Use and Limitations

- **Optimal Regimes:** Continuous high-dimensional data with substantial nuisance features ($D \gg N, D/N > 20$) and localized cluster structure under additive isotropic distractor noise (e.g. genomic microarrays, mass spectrometry assays, oncological expression profiles, hyperspectral data).
- **When NOT to Use:**
  - Large-sample low-dimensional data ($N \gg D$) or ultra-sparse count matrices (e.g., single-cell count matrices with high zero inflation or sparse TF-IDF text), where classical Ward or DEC is preferred.
  - Non-linear multi-feature XOR interactions, where 1D marginal unimodality cannot detect joint multi-variable dependencies without marginal separation.
  - Very large cluster counts ($K \ge 20$) with small anchor budgets ($L < K$).

---

## Repository Architecture

```text
icc-clustering/
├── src/
│   ├── icc/                    # Core ICC framework
│   │   ├── algorithms/         # Clustering algorithm implementations (Anchor, Cohirf, Deep, etc.)
│   │   ├── consensus/          # Consensus engines (ICC-v2, GAC, ASPP, Auto-K, CICC)
│   │   ├── data/               # Dataset loaders, cohorts, and preprocessing (BGSS)
│   │   ├── evaluation/         # Clustering evaluation metrics (ARI, NMI, AMI, ACC, FM)
│   │   ├── experiments/        # Experiment runner and benchmarking harnesses
│   │   ├── stats/              # Statistical tests (Hodges-Lehmann, TOST, Friedman)
│   │   └── utils/              # Logging, timer, and seeding utilities
│   └── cicc/                   # Conformal Inductive Consensus Clustering
│       ├── conformal.py        # Split-conformal prediction sets
│       ├── decoy.py            # Target-decoy knockoff FDR screening
│       ├── inductive.py        # Inductive out-of-sample projection
│       └── memory.py           # Dynamic incremental memory routing
├── tests/                      # Modular test suite (118 tests, 100% pass rate)
│   ├── unit/                   # Fast algorithmic unit tests
│   ├── integration/            # Dataset loading and pipeline integration tests
│   └── regression/             # Scalability, anchor fidelity, and boundary tests
├── scripts/                    # Command-line utility and benchmarking scripts
│   ├── run.py                  # CLI experiment runner
│   ├── prepare_data.py         # Data preparation and preprocessing CLI
│   ├── evaluate.py             # Results evaluation and metrics computation CLI
│   └── fetch_data.py           # Benchmark dataset fetcher
├── configs/                    # YAML configuration files
│   ├── default.yaml            # Default execution configuration
│   └── examples/               # Example configuration presets
└── docs/                       # Framework documentation
    ├── setup.md                # Installation and environment guide
    ├── usage.md                # Usage tutorials and examples
    ├── api.md                  # Python API reference
    ├── THEORETICAL_FOUNDATIONS.md # Mathematical formulations and proofs
    ├── DATA.md                 # Benchmark dataset specifications
    ├── REPRODUCIBILITY.md      # Determinism and reproduction guide
    └── development.md          # Development and contribution guide
```

---

## Installation

### Standard Installation
```bash
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering
pip install -e .
```

### Optional Dependencies
```bash
# Deep learning baselines (DEC, IDEC)
pip install -e ".[deep]"

# Single-cell & genomics tools (Scanpy, AnnData)
pip install -e ".[bio]"

# Development, testing, and linting
pip install -e ".[dev]"
```

Verify installation:
```bash
python -m pytest tests/
```

---

## Quick Start

### 1. Python API

```python
import numpy as np
from icc import ICC, evaluate_all

# Synthesize sample high-dimensional data (N=150, D=1000, K=3)
rng = np.random.default_rng(42)
X_signal = np.repeat([[0.0, 0.0], [3.0, 3.0], [-3.0, 3.0]], 50, axis=0)
X_noise = rng.normal(scale=1.0, size=(150, 998))
X = np.hstack([X_signal + rng.normal(scale=0.5, size=(150, 2)), X_noise])
y_true = np.repeat([0, 1, 2], 50)

# Fit ICC-v2 model
model = ICC(n_clusters=3, n_base_models=20, n_anchors=30, random_state=42)
labels = model.fit_predict(X)

# Evaluate performance
metrics = evaluate_all(y_true, labels)
print(f"ARI: {metrics['ari']:.4f}")

# Out-of-sample inductive prediction on new samples
X_new = rng.normal(scale=1.0, size=(10, 1000))
new_labels = model.predict(X_new)
```

### 2. Command-Line Interface

Run an experiment via configuration file:
```bash
python scripts/run.py --config configs/examples/synthetic.yaml
```

Evaluate experimental results:
```bash
python scripts/evaluate.py --results results/experiments/<run_name>.json
```

Prepare and inspect datasets:
```bash
python scripts/prepare_data.py --dataset colon --visualize
```

---

## Documentation

Detailed documentation is available in the [`docs/`](docs/) directory:
- [Setup and Installation Guide](docs/setup.md)
- [Usage Guide & Code Examples](docs/usage.md)
- [Python API Reference](docs/api.md)
- [Theoretical Formulations & Proofs](docs/THEORETICAL_FOUNDATIONS.md)
- [Benchmark Dataset Specifications](docs/DATA.md)
- [Reproducibility & Determinism Guide](docs/REPRODUCIBILITY.md)
- [Development and Contributing Guide](docs/development.md)

---

## Citation

If you use this software in your research, please cite:

```bibtex
@software{icc_clustering,
  author    = {Kundu, Akash and Das, Kalyan Kumar and Mukhopadhyay, Anirban},
  title     = {Invariant Core Consensus (ICC): High-Dimensional Consensus Clustering},
  year      = {2026},
  url       = {https://github.com/AkashKundu114/icc-clustering},
  version   = {2.2.0}
}
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
