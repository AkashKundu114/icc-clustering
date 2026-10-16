# Inductive Consensus Clustering (ICC-v2)

Official reference implementation of the manuscript:  
**"Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes"** (Under Review).

[![CI](https://github.com/AkashKundu114/icc-clustering/actions/workflows/ci.yml/badge.svg)](https://github.com/AkashKundu114/icc-clustering/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: Passing](https://img.shields.io/badge/pytest-77%2F77%20passed-brightgreen.svg)]()
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

---

## Overview

Consensus clustering synthesizes diverse base clusterings into a unified partition. However, in high-dimensional noise regimes (D >> N), distance concentration degrades base partition quality, while classical O(N^2) co-association matrices prevent out-of-sample inference.

**Inductive Consensus Clustering (ICC-v2)** resolves these challenges:
- **Variance-Stabilized Subspace Gating (VSSG):** Unsupervised linear O(N * D) feature screening using Sarle's Bimodality Coefficient to separate multimodal signals from unimodal background noise.
- **Bipartite Anchor Consensus:** Compresses O(N^2) co-association into an O(N * L) rectangular bipartite graph (L << N) with Transfer-Cut degree and eigenvalue normalization.
- **Closed-Form Inductive Inference:** Stability-weighted active centroid projection requiring only O(K * |F_active|) operations per query instance without graph recomputation.
- **Anchor-Space Perturbation Profiling (ASPP):** Multi-family cluster reliability certification yielding cluster fingerprints and query confidence bounds in linear O(NL) memory.

---

## When to Use and Limitations

- **Optimal Regimes:** Small-sample, continuous high-dimensional data (D >> N, D/N > 20) with localized cluster separation under additive isotropic distractor noise (e.g. genomic microarrays, mass spectrometry assays).
- **When NOT to Use:**
  - Large-sample low-dimensional data (N >> D) or ultra-sparse count matrices (e.g. single-cell count matrices with high zero inflation or sparse TF-IDF text), where classical Ward or DEC is preferred.
  - Non-linear multi-feature XOR interactions (e.g. Madelon), where 1D marginal unimodality cannot detect joint multi-variable dependencies.
  - Very large cluster counts (K >= 20) with small anchor budgets (L < K).

---

## Installation

```bash
# Clone the repository
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering

# Install core package in editable mode
pip install -e .

# Optional development tools
pip install -e ".[dev]"
```

Run tests to verify installation:
```bash
python -m pytest tests/ -v
```

---

## Quickstart (Offline Synthetic Example)

```python
import numpy as np
from icc import ICC
from icc.metrics import evaluate_all

# 1. Generate synthetic data (N=150, D=300, K=3) with 15 informative features
rng = np.random.default_rng(42)
X = rng.standard_normal((150, 300))
y_true = np.array([0] * 50 + [1] * 50 + [2] * 50)
X[:50, :15] += 2.5
X[50:100, :15] -= 2.5

# 2. Fit estimator
model = ICC(n_clusters=3, n_base_models=25, n_anchors=30, random_state=42)
labels = model.fit_predict(X)

# 3. Evaluate clustering
metrics = evaluate_all(y_true, labels)
print(f"Training ARI: {metrics['ari']:.4f}")

# 4. Inductive prediction for unseen queries
X_query = rng.standard_normal((5, 300))
X_query[:, :15] += 2.5
print("Out-of-sample predictions:", model.predict(X_query).tolist())
```

---

## Results Summary (Single Source of Truth)

All numbers are generated directly from frozen evaluation runs (`results/results.json` and `results/phase2/stats.json`):

Across all 13 benchmark datasets (1,430 model executions), omnibus Friedman testing indicates no statistically significant difference across the complete heterogeneous benchmark suite (Friedman chi^2 = 11.34, p = 0.33, Critical Difference = 4.21). However, on the target ultra-high-dimensional biological cancer assays (D/N > 20), ICC-v2 commands Rank #1:

| Method | High-D Mean ARI (D/N > 20) | High-D Rank | Overall 13-Dataset Rank |
| :--- | :---: | :---: | :---: |
| **ICC-v2 (Proposed)** | **0.258** | **2.33** | 5.46 |
| **Variance Filter + K-Means** | 0.050 | - | - |
| **Sparse K-Means** | 0.044 | - | - |
| **PCA + K-Means** | 0.042 | - | - |
| **Laplacian Score + K-Means** | 0.041 | - | - |
| **Standard K-Means** | 0.044 | 5.83 | 5.31 |
| **Standard Consensus** | 0.039 | 6.33 | 5.08 |
| **DEC (Deep Embedded)** | - | 5.00 | 4.31 |

Detailed per-dataset metrics, baselines, and ablation tables are available in the manuscript and `results/phase2/`.

---

## Reproducing the Paper

```bash
# Fast smoke verification (synthetic + real leukemia/srbct benchmarks)
python scripts/reproduce.py --scope smoke

# Fetch and verify benchmark datasets
python scripts/fetch_data.py

# Offline synthetic quickstart
python examples/quickstart.py

# Real Leukemia out-of-sample evaluation
python examples/leukemia_inductive.py
```

Expected smoke runtime: < 3 seconds on modern multi-core CPU. Determinism is enforced with `OMP_NUM_THREADS=1`.

---

## Documentation

- [API Reference](docs/api.md)
- [Dataset Guide & Licenses](docs/DATA.md)
- [Theoretical Foundations](docs/THEORETICAL_FOUNDATIONS.md)
- [Claims Audit & Ledger](REMEDIATION/CLAIMS_AUDIT.md)

---

## Citation

```bibtex
@article{kundu2026inductive,
  author    = {Akash Kundu and Trinankur Guha and Rupankar Ghatak and Anubhab Naskar and Kalyan Kumar Das},
  title     = {Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes},
  journal   = {Preprint / Submitted for Peer Review},
  year      = {2026},
  url       = {https://github.com/AkashKundu114/icc-clustering}
}
```

---

## License & Contact

- **License:** [MIT License](LICENSE)
- **Corresponding Author:** Akash Kundu (`akash231001001449@technoindiaeducation.com`)
- **Institution:** Department of Computer Science and Engineering, Techno India University
