# When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? (ICC-v2)

Official reference implementation of the manuscript:  
**"When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"** (Under Review).

[![CI](https://github.com/AkashKundu114/icc-clustering/actions/workflows/ci.yml/badge.svg)](https://github.com/AkashKundu114/icc-clustering/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: Passing](https://img.shields.io/badge/pytest-84%2F84%20passed-brightgreen.svg)]()
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

---

## Overview

Consensus clustering synthesizes diverse base clusterings into a unified partition. However, in high-dimensional noise regimes ($D \gg N$), distance concentration degrades base partition quality, while classical $O(N^2)$ co-association matrices prevent out-of-sample inference.

**Inductive Consensus Clustering (ICC-v2)** resolves these challenges through four coupled mechanisms:
- **Bimodality-Gated Subspace Selection (BGSS):** Unsupervised linear $O(N \cdot D)$ feature screening using Sarle's Bimodality Coefficient ($BC$) with finite-sample null correction to separate multimodal signals from unimodal background distractor noise.
- **Bipartite Anchor Consensus:** Compresses $O(N^2)$ co-association into an $O(N \cdot L)$ rectangular bipartite graph ($L \ll N$) with Transfer-Cut degree and eigenvalue normalization.
- **Closed-Form Inductive Inference:** Stability-weighted active centroid projection requiring only $O(K \cdot |\mathcal{F}_{\text{active}}|)$ operations per query instance without graph recomputation.
- **Anchor-Space Perturbation Profiling (ASPP):** Multi-family cluster reliability certification yielding cluster fingerprints and query confidence bounds in linear $O(N \cdot L)$ memory.

---

## When to Use and Limitations

- **Optimal Regimes:** Small-sample, continuous high-dimensional data ($D \gg N, D/N > 20$) with localized cluster separation under additive isotropic distractor noise (e.g. genomic microarrays, mass spectrometry assays).
- **When NOT to Use:**
  - Large-sample low-dimensional data ($N \gg D$) or ultra-sparse count matrices (e.g. single-cell count matrices with high zero inflation or sparse TF-IDF text), where classical Ward or DEC is preferred.
  - Non-linear multi-feature XOR interactions (e.g. Madelon), where 1D marginal unimodality cannot detect joint multi-variable dependencies without marginal separation.
  - Very large cluster counts ($K \ge 20$) with small anchor budgets ($L < K$).

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

All reported values trace directly to frozen Pass F execution stores (`results/passF/` and `springer_manuscript/numbers.tex`):

Across all 13 benchmark datasets (2,750 individual model fits across 11 methods, 30 random seeds on 6 high-D datasets and 10 seeds on 7 general datasets), omnibus Friedman testing indicates no statistically significant difference across the complete heterogeneous benchmark suite (Friedman $\chi^2_F = 9.59, p = 0.48$, Nemenyi Critical Difference $CD = 4.19$). 

However, on the target ultra-high-dimensional biological cancer assays ($D/N > 20$), ICC-v2 commands **Rank #1**:

| Method | High-D Mean ARI ($D/N > 20$) | High-D Rank (6 Datasets) | Overall Rank (13 Datasets) | Grand Mean ARI (13 Datasets) |
| :--- | :---: | :---: | :---: | :---: |
| **ICC-v2 (Proposed)** | **0.217** | **2.00** | 5.23 | **0.152** |
| **Standard Consensus** | 0.037 | 6.67 | 4.85 | 0.126 |
| **Standard K-Means** | 0.056 | 5.50 | 5.00 | 0.124 |
| **DEC (Deep Embedded)** | 0.045 | 6.00 | 5.08 | 0.125 |
| **Ward Hierarchical** | 0.032 | 6.67 | 5.31 | 0.120 |
| **FCM (Fuzzy C-Means)** | 0.044 | 5.67 | 6.77 | 0.070 |
| **FastMVC** | 0.049 | 6.33 | 6.92 | 0.110 |
| **FCAG** | 0.066 | 7.17 | 7.23 | 0.116 |
| **Core-Halo Consensus (Li et al.)** | 0.036 | 7.33 | 6.62 | 0.097 |
| **Spectral Clustering** | 0.035 | 7.50 | 6.62 | 0.105 |
| **ICC-v1 (Uncalibrated)** | 0.046 | 5.17 | 6.38 | 0.091 |

When compared against classical dimension reduction baselines under identical 30-seed protocol on the high-D subgroup ($D/N > 20$):
- **PCA + K-Means:** Mean ARI = 0.054 (Median = 0.027)
- **Sparse K-Means:** Mean ARI = 0.051 (Median = 0.004)
- **Variance Filter + K-Means:** Mean ARI = 0.046 (Median = 0.017)
- **Laplacian Score + K-Means:** Mean ARI = 0.041 (Median = 0.017)
- **PCA + Standard Consensus:** Mean ARI = 0.038 (Median = 0.019)
- **Variance Filter + Standard Consensus:** Mean ARI = 0.032 (Median = 0.019)

Detailed per-dataset metrics, pre-registration specifications, and bootstrap confidence intervals are available in `results/passF/` and `LOOP/PREREG_F.md`.

---

## Reproducing the Paper

```bash
# Fast smoke verification (synthetic + real leukemia/srbct benchmarks, < 3 seconds)
python scripts/reproduce.py --scope smoke

# Interactive CLI walkthrough
python demo.py

# Verify numbers.tex macros against Pass F store
python tests/test_macro_consistency.py

# Verify compiled PDF decimals against Pass F numerical allowlist
python tests/test_pdf_allowlist.py

# Fetch and verify benchmark datasets
python scripts/fetch_data.py

# Offline synthetic quickstart
python examples/quickstart.py

# Real Leukemia out-of-sample evaluation
python examples/leukemia_inductive.py
```

Expected smoke runtime: < 3 seconds on modern CPU. Determinism is enforced with `OMP_NUM_THREADS=1`.

---

## AI Assistance Disclosure

During the preparation of this manuscript and software repository, the authors utilized an agentic AI coding assistant (Google Antigravity, utilizing Gemini models including experimental flash/pro checkpoints) to assist with iterative drafting and textual refactoring (including revision of title, abstract, and conclusion framing), automated script execution, bibliographic checking against CrossRef APIs, figure plotting, LaTeX table formatting, and proofreading text. All conceptual formulations, empirical designs, and theoretical derivations were directed by the human authors. The authors have conducted extensive cross-checks of the generated text, tables, figures, and code, and take full responsibility for the scientific integrity and reproducibility of all reported findings.

---

## Documentation

- [API Reference](docs/api.md)
- [Dataset Guide & Verified Licenses](docs/DATA.md)
- [Theoretical Foundations](docs/THEORETICAL_FOUNDATIONS.md)
- [Pre-Registration Protocol (Pass F)](LOOP/PREREG_F.md)
- [Claims Audit Ledger](REMEDIATION/CLAIMS_AUDIT.md)

---

## Citation

```bibtex
@article{kundu2026when,
  author    = {Akash Kundu and Trinankur Guha and Rupankar Ghatak and Anubhab Naskar and Kalyan Kumar Das},
  title     = {When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination},
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
