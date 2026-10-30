# Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes

Official reference implementation of the manuscript:  
**"Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes"** (Springer Nature *Data Mining and Knowledge Discovery* / DAMI, Under Review).

[![CI](https://github.com/AkashKundu114/icc-clustering/actions/workflows/ci.yml/badge.svg)](https://github.com/AkashKundu114/icc-clustering/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: Passing](https://img.shields.io/badge/pytest-84%2F84%20passed-brightgreen.svg)]()
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![XERJ Corpus Hub contributor](https://hub.xerj.org/contributors/AkashKundu114/badge.svg)](https://hub.xerj.org/contributors/AkashKundu114)

---

## Overview

Consensus clustering synthesizes diverse base clusterings into a unified partition. However, in high-dimensional noise regimes ($D \gg N$), distance concentration degrades base partition quality, while classical $O(N^2)$ co-association matrices prevent out-of-sample inference.

**Inductive Consensus Clustering (ICC-v2)** resolves these challenges through four coupled mechanisms:
- **Bimodality-Gated Subspace Selection (BGSS):** Unsupervised linear $O(N \cdot D)$ feature screening using Sarle's Bimodality Coefficient ($BC$) with finite-sample null correction to separate multimodal signals from unimodal background distractor noise.
- **Bipartite Anchor Consensus:** Compresses $O(N^2)$ co-association into an $O(N \cdot L)$ rectangular bipartite graph ($L \ll N$) with Transfer-Cut degree and eigenvalue normalization.
- **Closed-Form Inductive Inference:** Stability-weighted active centroid projection requiring only $O(K \cdot |\mathcal{F}_{\text{active}}|)$ operations per query instance without graph recomputation.
- **Anchor-Space Perturbation Profiling (ASPP):** Multi-family cluster reliability certification yielding cluster fingerprints and query confidence bounds in linear $O(N \cdot L)$ memory.
- **Conformal Uncertainty Quantification (`cicc`):** Finite-sample distribution-free $(1 - \alpha)$ coverage guarantees with target-decoy FDR feature selection and automated point-of-care patient safety triage.

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

All reported values trace directly to frozen Pass F execution stores (`results/passF/` and `results/stats.json`):

Across all 13 benchmark datasets (3,000 individual model fits across 12 clustering pipelines, 30 random seeds on 6 high-D datasets and 10 seeds on 7 general datasets), omnibus Friedman testing indicates no statistically significant difference across the complete heterogeneous benchmark suite (Friedman $\chi^2_F = 11.56, p = 0.40$, Nemenyi Critical Difference $CD = 4.62$). 

However, on the target ultra-high-dimensional biological cancer assays ($D/N > 20$), the GAC pipeline commands **Rank #1** (subgroup mean ARI = 0.217, mean rank 2.17):

| Method | High-D Mean ARI (D/N > 20) | High-D Rank (6 Datasets) | Overall Rank (13 Datasets) | Grand Mean ARI (13 Datasets) |
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

When compared against classical dimension reduction baselines under identical 30-seed protocol on the high-D subgroup ($D/N > 20$):
- **PCA + K-Means:** Mean ARI = 0.054 (Median = 0.027)
- **Sparse K-Means:** Mean ARI = 0.051 (Median = 0.004)
- **Variance Filter + K-Means:** Mean ARI = 0.046 (Median = 0.017)
- **Laplacian Score + K-Means:** Mean ARI = 0.041 (Median = 0.017)
- **PCA + Standard Consensus:** Mean ARI = 0.038 (Median = 0.019)
- **Variance Filter + Standard Consensus:** Mean ARI = 0.032 (Median = 0.019)

Detailed per-dataset metrics, pre-registration specifications, and bootstrap confidence intervals are available in `results/passF/` and `experiments/PRE_REGISTRATION_v1.0.md`.

---

## Reproducing the Paper

```bash
# Fast smoke verification (synthetic + real leukemia/srbct benchmarks, < 3 seconds)
python scripts/reproduce.py --scope smoke

# Automated repository, data, and scientific invariant consistency check
python tools/check_consistency.py

# Interactive CLI walkthrough
python demo.py

# Fetch and verify benchmark datasets
python scripts/fetch_data.py

# Offline synthetic quickstart
python examples/quickstart.py

# Real Leukemia out-of-sample evaluation
python examples/leukemia_inductive.py

# Real-world clinical oncology subtyping (Leukemia & SRBCT)
python examples/clinical_cancer_subtyping.py

# Real-time point-of-care patient biopsy projection with conformal triage
python examples/realtime_patient_projection.py
```

Expected smoke runtime: < 3 seconds on modern CPU. Determinism is enforced with `OMP_NUM_THREADS=1`.

---

## AI Assistance Disclosure

The authors used AI assistance solely for grammatical checking and English language copy-editing. All concepts, analyses, code, mathematical formulations, experimental pipelines, and conclusions were developed and verified entirely by the authors.

---

## Reproducibility & Verification

To reproduce benchmark evaluations and verify theoretical identities:
- **Smoke Reproduction Suite:** `python scripts/reproduce.py --scope smoke`
- **Real-Data Stability Audit:** `python scripts/run_real_data_stability.py`
- **Theoretical Identity Verification:** `python scripts/verify_determinacy_identity.py`
- **Inductive Query Latency Benchmark:** `python scripts/measure_query_latency.py`
- **Bimodality Null Calibration Check:** `python scripts/verify_bc.py`

---

## Documentation

- [API Reference](docs/api.md)
- [Dataset Guide & Verified Licenses](docs/DATA.md)
- [Theoretical Foundations](docs/THEORETICAL_FOUNDATIONS.md)
- [Hardware & Software Environment](docs/ENV.md)
- [AI Usage Declaration](docs/AI_USE.md)

---

## Citation

```bibtex
@article{das2026featuregated,
  author    = {Kalyan Kumar Das and Akash Kundu and Anirban Mukhopadhyay},
  title     = {Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes},
  journal   = {Data Mining and Knowledge Discovery (Under Review)},
  year      = {2026},
  url       = {https://github.com/AkashKundu114/icc-clustering}
}
```

---

## License & Authors

- **License:** [MIT License](LICENSE)
- **Prof. Kalyan Kumar Das** (Corresponding Author, Research Supervisor: `kalyan.biltu@gmail.com`)  
  Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India
- **Akash Kundu** (Lead Developer, Code & Reproduction Materials Contact: `akashkundu1152@gmail.com`)  
  Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India
- **Prof. Anirban Mukhopadhyay** (Senior Collaborator: `anirban@klyuniv.ac.in`)  
  Department of Computer Science and Engineering, University of Kalyani, Nadia, West Bengal, India
