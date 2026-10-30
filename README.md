# Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes

Official reference implementation of the manuscript:  
**"Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes"** (Springer Nature *Data Mining and Knowledge Discovery* / DAMI, Under Review).

[![CI](https://github.com/AkashKundu114/icc-clustering/actions/workflows/ci.yml/badge.svg)](https://github.com/AkashKundu114/icc-clustering/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: Passing](https://img.shields.io/badge/pytest-84%2F84%20passed-brightgreen.svg)]()
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

---

## 1. Overview & Theoretical Architecture

Consensus clustering synthesizes diverse base clusterings into an aggregated partition to improve stability and robustness. However, in high-dimensional noise regimes ($D \gg N$), distance concentration degrades base partition quality, while classical $O(N^2)$ co-association matrices prevent out-of-sample inductive inference.

**Inductive Consensus Clustering (ICC-v2)** resolves these challenges through five mathematically coupled mechanisms:

1. **Bimodality-Gated Subspace Selection (BGSS):**  
   Performs unsupervised linear $O(N \cdot D)$ feature screening via Sarle's Bimodality Coefficient ($BC$) with finite-sample null correction:
   $$\text{BC} = \frac{\gamma^2 + 1}{\kappa + 3 \cdot \frac{(N-1)^2}{(N-2)(N-3)}}$$
   where $\gamma$ is sample skewness and $\kappa$ is excess kurtosis. Features with $\text{BC} \le \text{BC}_{\text{unif}} \approx 5/9$ represent unimodal distractor noise and are excluded, isolating the multi-modal cluster manifold.
2. **Bipartite Anchor Consensus:**  
   Compresses the classical $O(N^2)$ co-association graph into an $O(N \cdot L)$ rectangular bipartite graph $B \in \mathbb{R}^{N \times L}$ ($L \ll N$) linking sample instances to representative anchor centroids. Partitioning is solved via Transfer-Cut normalized Laplacian SVD with left-singular vector clustering.
3. **Closed-Form Inductive Inference:**  
   Provides exact out-of-sample prediction requiring only $O(K \cdot |\mathcal{F}_{\text{active}}|)$ operations per query point by projecting new observations directly onto the stability-weighted active subspace centroids without graph reconstruction.
4. **Anchor-Space Perturbation Profiling (ASPP):**  
   Certifies multi-family cluster reliability in $O(N \cdot L)$ space, generating cluster fingerprints, boundary stability coefficients, and query confidence bounds.
5. **Conformal Uncertainty Quantification (`cicc`):**  
   Delivers finite-sample distribution-free $(1 - \alpha)$ coverage guarantees using split-conformal non-conformity scores, coupled with target-decoy false discovery rate (FDR) feature screening for safe automated clinical triage.

---

## 2. Push-Button Reproduction

For peer reviewers and researchers, the repository provides push-button commands to verify empirical claims:

```bash
# Fast smoke verification across synthetic and real biological benchmarks (< 3 seconds)
python scripts/reproduce.py --scope smoke

# Regenerate all 16 manuscript LaTeX tables from raw empirical stores (~2 seconds)
python scripts/reproduce.py --scope tables

# Verify theoretical proofs and statistical invariants (~3 seconds)
python scripts/reproduce.py --scope verify

# Automated consistency checker (dataset counts, 3,000 fits arithmetic, stats.json)
python tools/check_consistency.py

# Run complete test suite (84 passing tests)
python -m pytest tests/ -q
```

> **Determinism Note:** To ensure bitwise reproducibility across CPU architectures, BLAS thread concurrency is pinned to single-threaded execution (`OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`).

For an exhaustive mapping of every manuscript table (Table 1 through 16) and figure (Figure 1 through 9) to underlying data files in `results/passF`, see the [Peer Reviewer & Reproducibility Guide](docs/REPRODUCIBILITY.md).

---

## 3. Empirical Results (Single Source of Truth)

All reported values trace directly to frozen Pass F execution logs (`results/passF/` and `results/stats.json`):

Across all 13 benchmark datasets (3,000 individual model fits across 12 clustering pipelines, 30 random seeds on 6 high-D datasets and 10 seeds on 7 general datasets), omnibus Friedman testing confirms no statistically significant difference across the heterogeneous benchmark suite as a whole (Friedman $\chi^2_F = 11.56, p = 0.40$, Nemenyi Critical Difference $CD = 4.62$).

However, on the target ultra-high-dimensional biological cancer cohorts ($D/N > 20$), the ICC-v2 pipeline achieves **Rank #1** (subgroup mean ARI = 0.217, mean rank 2.17):

| Method | High-D Mean ARI ($D/N > 20$) | High-D Median ARI | High-D Rank (6 Datasets) | Overall Rank (13 Datasets) | Grand Mean ARI (13 Datasets) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **ICC-v2 (Ours)** | **0.217** | **0.061** | **2.17** | 5.62 | **0.152** |
| **FCAG** | 0.066 | -0.0004 | 7.83 | 7.77 | 0.116 |
| **Standard K-Means** | 0.056 | 0.053 | 5.67 | **5.15** | 0.124 |
| **FastMVC** | 0.049 | 0.004 | 6.83 | 7.38 | 0.110 |
| **ICC-v1 (Ungated Anchor)** | 0.046 | 0.021 | 5.67 | 6.92 | 0.091 |
| **DEC (Deep Embedded)** | 0.045 | 0.025 | 6.17 | 5.23 | 0.125 |
| **FCM (Fuzzy C-Means)** | 0.044 | 0.029 | 5.83 | 7.08 | 0.070 |
| **Standard Consensus** | 0.037 | 0.026 | 7.17 | 5.23 | 0.126 |
| **Core-Halo Consensus** | 0.036 | 0.005 | 7.83 | 7.15 | 0.097 |
| **Spectral Clustering** | 0.035 | 0.008 | 8.00 | 7.08 | 0.105 |
| **Ward Hierarchical** | 0.032 | 0.019 | 7.17 | 5.69 | 0.120 |
| **CoHiRF** | 0.017 | 0.003 | 7.67 | 7.69 | 0.085 |

### Matched-Budget Feature Selection Baselines
Under an identical 30-seed matched feature budget ($\lfloor 0.15 D \rfloor$ selected dimensions) across the 6 high-D cohorts:
- **PCA + K-Means:** Mean ARI = 0.054 (Median = 0.027)
- **Sparse K-Means:** Mean ARI = 0.051 (Median = 0.004)
- **Variance Filter + K-Means:** Mean ARI = 0.046 (Median = 0.017)
- **Laplacian Score + K-Means:** Mean ARI = 0.041 (Median = 0.017)
- **PCA + Standard Consensus:** Mean ARI = 0.038 (Median = 0.019)
- **Variance Filter + Standard Consensus:** Mean ARI = 0.032 (Median = 0.019)

---

## 4. Quickstart Guide (4 Steps)

The following self-contained snippet reproduces synthetic high-dimensional data generation, estimator fitting, cluster recovery evaluation, and inductive out-of-sample inference:

```python
import numpy as np
from icc import ICC
from icc.metrics import evaluate_all

# Step 1: Generate synthetic high-dimensional data (N=150, D=300, K=3)
# 15 informative features, 285 uninformative isotropic noise features
rng = np.random.default_rng(42)
X_train = rng.standard_normal((150, 300))
y_train = np.array([0] * 50 + [1] * 50 + [2] * 50)
X_train[:50, :15] += 2.5
X_train[50:100, :15] -= 2.5

# Step 2: Fit the ICC estimator
model = ICC(n_clusters=3, n_base_models=25, n_anchors=30, random_state=42)
labels = model.fit_predict(X_train)

# Step 3: Evaluate clustering recovery
metrics = evaluate_all(y_train, labels)
print(f"Training Partition ARI: {metrics['ari']:.4f}")

# Step 4: Inductive inference for unseen out-of-sample queries
X_query = rng.standard_normal((5, 300))
X_query[:, :15] += 2.5  # Matches cluster 0 signal profile
query_predictions = model.predict(X_query)
print("Inductive query predictions:", query_predictions.tolist())
```

---

## 5. Repository Layout

```
icc-clustering/
├── configs/                     # Experiment configurations and baseline parameters
│   ├── baselines.yaml           # Baseline algorithm hyperparameters
│   ├── datasets.yaml            # Dataset metadata & specifications
│   └── experiment_defaults.yaml # Benchmark defaults (M=25, L=40, pool_frac=0.15)
├── data/                        # Dataset registry and cached standardized arrays
│   ├── cache/                   # Cryptographically verified .npz benchmark files
│   └── registry.yaml            # 13 verified dataset definitions (N, D, K, D/N)
├── docs/                        # Comprehensive technical documentation & guides
│   ├── REPRODUCIBILITY.md       # Step-by-step reviewer & reproducibility guide
│   ├── DATA.md                  # Dataset licenses, metadata, and SHA-256 signatures
│   ├── api.md                   # Full Python API reference
│   ├── THEORETICAL_FOUNDATIONS.md # Formal proofs (Transfer-Cut, Sarle's BC, Centroid)
│   └── ENV.md                   # Host hardware, OS, and runtime specifications
├── examples/                    # End-to-end runnable demonstration scripts
│   ├── quickstart.py            # Minimal offline synthetic demo
│   ├── leukemia_inductive.py    # Out-of-sample evaluation on Leukemia microarray
│   ├── clinical_cancer_subtyping.py # Oncogenic subtyping on Leukemia & SRBCT
│   └── realtime_patient_projection.py # Conformal triage with confidence intervals
├── experiments/                 # Benchmark battery and empirical evaluations
│   ├── audit_controls/          # Label-free feature selector audits
│   ├── exp0_falsification/      # Synthetic noise falsification experiments
│   ├── exp1_generalization/     # Inductive generalization experiments
│   ├── exp2_ablation/           # Stepwise architectural ablation (V0-V5)
│   ├── exp3_real_world_benchmarks/ # Real-world cancer and multi-domain benchmarks
│   ├── exp4_scalability_and_sensitivity/ # Timing and memory scaling vs N and K
│   └── exp5_extreme_scale/      # Extreme scalability benchmarks up to N=10^6
├── results/                     # Canonical result logs and statistical stores
│   ├── passF/                   # Frozen Pass F empirical results (30 seeds)
│   ├── stability/               # Real-world partition perturbation audit logs
│   ├── stats.json               # Canonical omnibus test statistics & effect sizes
│   └── INVENTORY.md             # Complete experiment and result inventory
├── scripts/                     # Reproducibility and utility CLI scripts
│   ├── reproduce.py             # Central push-button reproduction CLI
│   ├── make_tables.py           # Programmatic LaTeX table generator
│   └── verify_bc.py             # Sarle's Bimodality Coefficient validation
├── src/                         # Core Python package source code
│   ├── cicc/                    # Conformal Inductive Consensus Clustering module
│   └── icc/                     # ICC estimator, BGSS gating, and bipartite engine
├── tests/                       # Unit and integration test suite (84 passing tests)
├── tools/                       # Repository and data consistency verifiers
│   └── check_consistency.py     # Automated scientific consistency checker
├── CITATION.cff                 # Machine-readable citation metadata
├── CONTRIBUTING.md              # Contributor guidelines and workflow
├── LICENSE                      # MIT Open Source License
├── pyproject.toml               # Project build metadata and dependencies
├── SECURITY.md                  # Security and vulnerability reporting policy
└── SUPPORT.md                   # Academic contact and support channels
```

---

## 6. Installation

```bash
# Clone the repository
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering

# Install core package in editable mode
pip install -e .

# Optional development and testing dependencies
pip install -e ".[dev]"
```

Verify the installation:
```bash
python -m pytest tests/ -q
python scripts/reproduce.py --scope smoke
```

---

## 7. Documentation

- [Reviewer & Reproducibility Guide](docs/REPRODUCIBILITY.md): Push-button reproduction commands, table/figure mappings, and verification checklists.
- [Dataset Guide & Verified Licenses](docs/DATA.md): Comprehensive metadata, open-access licenses, and cryptographic checksums for all 13 benchmark datasets.
- [API Reference](docs/api.md): Complete Python API documentation for `ICC`, `BGSS`, `BipartiteConsensus`, and conformal uncertainty modules.
- [Theoretical Foundations](docs/THEORETICAL_FOUNDATIONS.md): Mathematical formulations, Transfer-Cut spectral derivations, and finite-sample Sarle's BC bounds.
- [Computational Environment](docs/ENV.md): Hardware specifications, operating system details, and determinism configurations.

---

## 8. Citation

If you use this software, benchmark suite, or theoretical derivations in your research, please cite:

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

## 9. Authors & Contact

- **Prof. Kalyan Kumar Das** (Corresponding Author, Research Supervisor: `kalyan.biltu@gmail.com`)  
  Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India  
  ORCID: [0009-0004-8333-8900](https://orcid.org/0009-0004-8333-8900)
- **Akash Kundu** (Lead Developer, Code & Reproduction Materials Contact: `akashkundu1152@gmail.com`)  
  Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India  
  ORCID: [0009-0003-8246-7316](https://orcid.org/0009-0003-8246-7316)
- **Prof. Anirban Mukhopadhyay** (Senior Collaborator: `anirban@klyuniv.ac.in`)  
  Department of Computer Science and Engineering, University of Kalyani, Nadia, West Bengal, India  
  ORCID: [0000-0001-8128-3521](https://orcid.org/0000-0001-8128-3521)
