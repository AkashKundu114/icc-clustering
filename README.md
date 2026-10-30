# An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts

Official reference implementation of the manuscript:  
**"An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts"** (Springer Nature *Data Mining and Knowledge Discovery* / DAMI, Under Review).

[![CI](https://github.com/AkashKundu114/icc-clustering/actions/workflows/ci.yml/badge.svg)](https://github.com/AkashKundu114/icc-clustering/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: Passing](https://img.shields.io/badge/pytest-98%2F98%20passed-brightgreen.svg)](tests/)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Checked: Mypy](https://img.shields.io/badge/mypy-checked-blue.svg)](https://mypy-lang.org/)

---

## Overview

Consensus clustering synthesizes diverse base clusterings into an aggregated partition to discover robust latent structures without supervision. However, in extreme high-dimensional noise regimes ($D \gg N$), distance concentration severely degrades base partition fidelity, while classical $\mathcal{O}(N^2)$ co-association matrices prevent scaling to large sample sizes and preclude out-of-sample inductive inference.

**Inductive Consensus Clustering (ICC-v2)** resolves these fundamental challenges through four mathematically calibrated mechanisms:
1. **Bimodality-Gated Subspace Selection (BGSS):** Unsupervised linear $\mathcal{O}(N \cdot D)$ feature screening using Sarle's Bimodality Coefficient ($BC$) with finite-sample null correction to filter continuous unimodal distractor noise ($BC \le 5/9$) while retaining true multimodal cluster signals.
2. **Exact Linear-Memory Contingency Determinacy:** An algebraic identity that evaluates full ensemble co-association directly from base contingency tables in $\mathcal{O}(M^2 N + M^2 K^2)$ time and $\mathcal{O}(N + M K)$ memory, achieving a 99.6% reduction in memory footprint over quadratic consensus.
3. **Reduced Bipartite Spectral Transfer-Cut:** Compresses consensus optimization into an $\mathcal{O}(N \cdot L)$ rectangular bipartite graph ($L \ll N$) with generalized degree and eigenvalue normalization, yielding linear scaling in $\mathcal{O}(N L^2 + L^3)$ time.
4. **Closed-Form Inductive Inference:** Stability-weighted active centroid projection executing in $\mathcal{O}(K \cdot |\mathcal{F}_{\text{active}}|)$ operations per query instance without graph recomputation, enabling real-time clinical biopsy assignment ($22.6\,\mu\text{s}$ per query).
5. **Conformal Uncertainty Quantification (`cicc`):** Finite-sample distribution-free $(1 - \alpha)$ coverage guarantees with target-decoy False Discovery Rate (FDR) feature selection and automated point-of-care patient safety triage.

---

## When to Use and Limitations

- **Optimal Regimes:** Continuous high-dimensional data with substantial nuisance features ($D \gg N, D/N > 20$) and localized cluster structure under additive isotropic distractor noise (e.g. genomic microarrays, mass spectrometry assays, oncological expression profiles).
- **When NOT to Use:**
  - Large-sample low-dimensional data ($N \gg D$) or ultra-sparse count matrices (e.g., single-cell count matrices with high zero inflation or sparse TF-IDF text), where classical Ward or DEC is preferred.
  - Non-linear multi-feature XOR interactions (e.g., Madelon), where 1D marginal unimodality cannot detect joint multi-variable dependencies without marginal separation.
  - Very large cluster counts ($K \ge 20$) with small anchor budgets ($L < K$).

---

## Repository Architecture

```text
icc-clustering/
├── src/
│   ├── icc/                    # Core ICC-v2 package
│   │   ├── consensus_v2.py     # Main ICCv2, GAC solvers & Transfer-Cut
│   │   ├── aspp.py             # Anchor-Space Perturbation Profiling
│   │   ├── baselines/          # 11 comparative baseline solvers
│   │   ├── datasets/           # 13 benchmark dataset loaders
│   │   └── metrics.py          # Clustering evaluation metrics (ARI, NMI, etc.)
│   └── cicc/                   # Conformal Inductive Consensus Clustering
│       ├── conformal.py        # Split-conformal prediction sets
│       ├── decoy.py            # Target-decoy knockoff FDR screening
│       ├── inductive.py        # Inductive out-of-sample projection
│       └── memory.py           # Dynamic incremental memory routing
├── tests/                      # Pytest test suite (98 tests, 100% pass rate)
├── scripts/                    # Research reproduction and verification scripts
│   ├── reproduce.py            # Central reproduction CLI (smoke, verify, tables, figures)
│   ├── make_tables.py          # Programmatic LaTeX table compiler (Tables 1–21)
│   ├── sync_figures.py         # Figure synchronization across manuscript targets
│   └── check_numbers.py        # 19-point automated numerical integrity audit
├── docs/                       # Research documentation
│   ├── REPRODUCIBILITY.md      # Master table-by-table & figure reproduction guide
│   ├── THEORETICAL_FOUNDATIONS.md # Formal proofs (Propositions 1 & 2, Theorems 1 & 2)
│   ├── DATA.md                 # Dataset specifications, hashes, and download sources
│   ├── api.md                  # Python API reference
│   └── ENV.md                  # Environment setup and BLAS determinism configuration
├── paper/                      # LaTeX manuscript source (Springer Nature sn-jnl)
│   ├── main.tex                # Primary manuscript source
│   ├── numbers.tex             # Single source of truth macro registry
│   ├── references.bib          # Bibliographic citations (CrossRef/arXiv verified)
│   └── gen/                    # Programmatically generated LaTeX tables
└── results/                    # Frozen empirical results and statistical registries
    ├── stats.json              # Omnibus statistical significance tests
    └── results.json            # Complete experimental run logs
```

---

## Installation

### Prerequisites
- Python 3.10+ (tested on Python 3.10 through 3.14).
- C/C++ compiler and BLAS/LAPACK runtime (bundled with standard NumPy/SciPy wheels).

### Quick Install
```bash
# Clone the repository
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering

# Install core package in editable mode
pip install -e .

# Optional development, test, and deep learning dependencies
pip install -e ".[dev,deep]"
```

Verify the installation with the automated test battery:
```bash
python -m pytest tests/
```

---

## Quickstart

```python
import numpy as np
from icc import ICC
from icc.metrics import evaluate_all

# 1. Generate synthetic high-dimensional data (N=150, D=300, K=3) with 15 informative features
rng = np.random.default_rng(42)
X = rng.standard_normal((150, 300))
y_true = np.array([0] * 50 + [1] * 50 + [2] * 50)
X[:50, :15] += 2.5
X[50:100, :15] -= 2.5

# 2. Fit the Feature-Gated Bipartite Graph Ensemble model
model = ICC(n_clusters=3, n_base_models=25, n_anchors=30, random_state=42)
labels = model.fit_predict(X)

# 3. Evaluate partition quality
metrics = evaluate_all(y_true, labels)
print(f"Discovered Clusters ARI: {metrics['ari']:.4f}")

# 4. Out-of-sample inductive projection for unseen query instances
X_query = rng.standard_normal((5, 300))
X_query[:, :15] += 2.5
query_preds = model.predict(X_query)
print("Inductive query predictions:", query_preds.tolist())
```

---

## One-Command Paper Reproduction

All empirical results, tables, figures, and mathematical proofs can be verified using the central reproduction CLI:

```powershell
# 1. Fast smoke verification across synthetic and real cohorts (< 2 seconds)
python scripts/reproduce.py --scope smoke

# 2. Mathematical proofs & 19-point numerical integrity verification (< 5 seconds)
python scripts/reproduce.py --scope verify

# 3. Regenerate all 21 paper LaTeX tables from empirical stores (< 5 seconds)
python scripts/reproduce.py --scope tables

# 4. Synchronize and render all manuscript figures (< 10 seconds)
python scripts/reproduce.py --scope figures

# 5. Execute the complete reproduction pipeline end-to-end
python scripts/reproduce.py --scope full
```

For detailed table-by-table (Tables 1–21) and figure-by-figure (Figures 1–10) mapping, see the [Reproducibility Guide](docs/REPRODUCIBILITY.md).

---

## Empirical Benchmark Findings (Single Source of Truth)

All reported statistics strictly trace to frozen results (`results/stats.json`) and compiled macros (`paper/numbers.tex`):

Across all 13 benchmark datasets (3,000 individual model fits across 12 clustering pipelines, 30 random seeds on 6 high-D datasets and 10 seeds on 7 general datasets), omnibus Friedman testing confirms no statistically significant difference across the complete multi-domain suite (Friedman $\chi^2_F = 11.56, p = 0.40$, Nemenyi Critical Difference $\text{CD} = 4.62$). 

However, on the target ultra-high-dimensional biological cancer cohorts ($D/N > 20$), the GAC pipeline commands **Rank #1** (subgroup mean ARI = **0.217**, mean rank **2.17**):

| Method | High-D Mean ARI ($D/N > 20$) | High-D Rank (6 Datasets) | Overall Rank (13 Datasets) | Grand Mean ARI (13 Datasets) |
| :--- | :---: | :---: | :---: | :---: |
| **GAC Pipeline (Ours)** | **0.217** | **2.17** | 5.62 | **0.152** |
| **Standard K-Means** | 0.056 | 5.67 | **5.15** | 0.124 |
| **Ungated Anchor Consensus** | 0.046 | 5.67 | 6.92 | 0.091 |
| **FCM (Fuzzy C-Means)** | 0.044 | 5.83 | 7.08 | 0.070 |
| **DEC (Deep Embedded)** | 0.045 | 6.17 | 5.23 | 0.125 |
| **FastMVC** | 0.049 | 6.83 | 7.38 | 0.110 |
| **Standard Consensus** | 0.037 | 7.17 | 5.23 | 0.126 |
| **Ward Hierarchical** | 0.032 | 7.17 | 5.69 | 0.120 |
| **CoHiRF** | 0.017 | 7.67 | 7.69 | 0.085 |
| **FCAG** | 0.066 | 7.83 | 7.77 | 0.116 |
| **Core-Halo Consensus (Li et al.)** | 0.036 | 7.83 | 7.15 | 0.097 |
| **Spectral Clustering** | 0.035 | 8.00 | 7.08 | 0.105 |

When compared against classical dimension reduction baselines under an identical 30-seed protocol on the high-D subgroup ($D/N > 20$):
- **PCA + K-Means:** Mean ARI = 0.054 (Median = 0.027)
- **Sparse K-Means:** Mean ARI = 0.051 (Median = 0.004)
- **Variance Filter + K-Means:** Mean ARI = 0.046 (Median = 0.017)
- **Laplacian Score + K-Means:** Mean ARI = 0.041 (Median = 0.017)
- **PCA + Standard Consensus:** Mean ARI = 0.038 (Median = 0.019)
- **Variance Filter + Standard Consensus:** Mean ARI = 0.032 (Median = 0.019)

---

## Documentation Links

- [Reproducibility Guide](docs/REPRODUCIBILITY.md)
- [Theoretical Foundations & Mathematical Proofs](docs/THEORETICAL_FOUNDATIONS.md)
- [Benchmark Datasets Guide](docs/DATA.md)
- [Python API Reference](docs/api.md)
- [Environment & BLAS Configuration](docs/ENV.md)
- [Literature Matrix & Comparative Baselines](docs/literature/papers.md)

---

## Citation

```bibtex
@article{kundu2026featuregated,
  author    = {Akash Kundu},
  title     = {An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts},
  journal   = {Data Mining and Knowledge Discovery (Under Review)},
  year      = {2026},
  url       = {https://github.com/AkashKundu114/icc-clustering}
}
```

---

## License & Contact

- **License:** [MIT License](LICENSE)
- **Author:** Akash Kundu (`akashkundu1152@gmail.com`)
- **Institution:** Department of Computer Science and Engineering, Techno India University
