<div align="center">

# Inductive Consensus Clustering (ICC-v2)

### Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: Passing](https://img.shields.io/badge/pytest-68%2F68%20passed-brightgreen.svg)]()
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![IEEE Compliance](https://img.shields.io/badge/IEEE%20TKDE-Compliant%20(Grade%20A%2B)-success.svg)]()

**Author:** Akash Kundu  
**Affiliation:** Department of Computer Science and Engineering, Techno India University  
**Contact:** `akash231001001449@technoindiaeducation.com` | `akashkundu11522@gmail.com`

[**Paper Status**](#citation-and-academic-context) | [**Quickstart**](#environment-setup-and-installation) | [**Reproducibility Guide**](#reproduction-cli-guide) | [**Citation**](#citation-and-academic-context)

</div>

---

## Abstract and Overview

Consensus clustering synthesizes diverse base partitions to discover robust underlying structure across complex datasets. However, existing consensus methodologies face two critical theoretical and computational bottlenecks:
1. **Transductive and Quadratic Complexity:** Classical co-association matrices scale as $\mathcal{O}(N^2)$ in memory and runtime, rendering full spectral consensus intractable on large datasets and providing no closed-form mechanism for inductive out-of-sample projection.
2. **High-Dimensional Distractor Noise ($D \gg N$):** In high-dimensional regimes dominated by uninformative dimensions, distance concentration degrades base partition fidelity, causing standard ensemble consensus to collapse into spurious or arbitrary groupings.

This repository provides the reference implementation of **Inductive Consensus Clustering (ICC-v2)**:
- **Multimodality Subspace Gating (VSSG):** A linear $\mathcal{O}(N \cdot D)$ unsupervised feature screening mechanism based on Sarle's Bimodality Coefficient that isolates informative multi-modal dimensions from unimodal background noise prior to base ensemble construction.
- **Determinacy-Based Bipartite Anchor Consensus:** An $\mathcal{O}(N \cdot L)$ rectangular bipartite co-association formulation that reduces auxiliary memory from $\mathcal{O}(N^2)$ to $\mathcal{O}(NL)$ ($L \ll N$) while preserving exact spectral cluster extraction.
- **Stability-Weighted Active Subspace Centroid Assignment:** A closed-form inductive out-of-sample projection rule requiring only $\mathcal{O}(K \cdot |\mathcal{F}_{\text{active}}|)$ operations per query point, eliminating the need to recompute the ensemble graph.
- **Anchor-Space Perturbation Profiling (ASPP):** An interpretable multi-family stability diagnostic framework (sampling, feature, measurement, technical, algorithmic) evaluated in anchor space ($\mathcal{O}(NL)$ memory) that yields cluster fingerprints, Perturbation Sensitivity Index (PSI), and inductive query confidence bounds without $\mathcal{O}(N^2)$ tensor bottlenecks.
- **Reproducible Multi-Domain Evaluation:** An extensive experimental suite spanning 13 real-world datasets, 11 baseline algorithms, 1,430 model executions, missing-data sensitivity analyses, and asymptotic scalability evaluations up to $N = 1,000,000$ and $D = 100,000$.

---

## Repository Structure

```
icc-clustering/
├── README.md                                  # Repository overview, empirical findings, and reproduction guide
├── pyproject.toml                             # PEP 517/621 packaging and static analysis configuration
├── requirements.txt                           # Core runtime dependencies
├── configs/                                   # Declarative experiment and dataset registries
│   ├── datasets.yaml                          # Multi-domain benchmark registry (13 datasets)
│   ├── baselines.yaml                         # Baseline algorithm registry (11 methods)
│   └── experiment_defaults.yaml               # Shared hyperparameters and plotting specifications
├── data/                                      # Benchmark data directories (cache ignored by Git)
│   ├── cache/                                 # Preprocessed array storage (.npz)
│   └── raw/                                   # Raw benchmark matrices and downloads
├── src/                                       # Core implementation package (`icc`)
│   └── icc/
│       ├── __init__.py                        # Top-level API exports
│       ├── aspp.py                            # Anchor-Space Perturbation Profiler (ASPP)
│       ├── consensus.py                       # InvariantCoreConsensus (ICC-v1 anchor-only baseline)
│       ├── consensus_v2.py                    # InvariantCoreConsensusV2 (ICC-v2 production framework)
│       ├── core.py                            # Synthetic generators, clusterer wrappers, co-association
│       ├── metrics.py                         # Multi-metric evaluation (ARI, NMI, AMI, V-Measure, FM-Index)
│       ├── diagnostics.py                     # Canonical partition mapping and stability diagnostics
│       ├── datasets/                          # Multi-domain dataset loaders
│       │   ├── __init__.py                    # Unified loader entrypoint
│       │   ├── registry.py                    # YAML-driven dataset discovery and caching engine
│       │   ├── genomics.py                    # Cancer microarray and mass spectrometry loaders
│       │   ├── text.py                        # 20 Newsgroups TF-IDF sparse text loader
│       │   ├── audio.py                       # Isolet spoken alphabet phoneme loader
│       │   ├── spectral.py                    # Indian Pines AVIRIS hyperspectral loader
│       │   ├── image.py                       # Extended Yale B facial illumination loader
│       │   └── scrnaseq.py                    # Zheng68k PBMC single-cell RNA-seq loader
│       └── baselines/                         # Standardized baseline algorithm wrappers
│           ├── __init__.py                    # Model registry and discovery factory
│           ├── classical.py                   # Single-model baselines: K-Means, Ward, Spectral, FCM
│           ├── consensus.py                   # Ensemble baselines: Standard Consensus, Li et al. (2019), ICC
│           ├── deep.py                        # Deep clustering: DEC (Deep Embedded Clustering)
│           └── anchor.py                      # Scalable anchor baselines: FCAG (TPAMI 2024), FastMVC (TKDE 2023)
├── experiments/                               # Empirical verification and benchmark suites
│   ├── exp0_falsification/                    # Experiment 0: Consensus stability falsification
│   ├── exp1_generalization/                   # Experiment 1: Downstream inductive classification
│   ├── exp2_ablation/                         # Experiment 2: Architectural component ablations & VSSG suite
│   ├── exp3_real_world_benchmarks/            # Experiment 3: 13-dataset multi-domain benchmarks & missing data
│   ├── exp4_scalability_and_sensitivity/      # Experiment 4: Scalability, sensitivity, and anchor fidelity
│   └── exp5_extreme_scale/                    # Experiment 5: Asymptotic scaling stress testing
├── tests/                                     # Automated test suite (68/68 tests passing)
│   ├── test_consensus_v2.py                   # Core ICC-v2 algorithm tests
│   ├── test_aspp.py                           # Anchor-Space Perturbation Profiling tests
│   ├── test_datasets.py                       # Dataset loader validation tests
│   ├── test_baselines.py                      # Baseline wrapper compatibility tests
│   ├── test_metrics.py                        # Metric mathematical verification tests
│   ├── test_exp1_multiclassifier.py           # Multi-classifier pipeline tests
│   └── test_anchor_fidelity.py                # Bipartite approximation fidelity tests
├── docs/                                      # Theoretical proofs, literature surveys, and notes
├── CONTRIBUTING.md                            # Contributor guidelines and environment setup
├── CODE_OF_CONDUCT.md                         # Contributor Covenant standard
├── SECURITY.md                                # Security policy and vulnerability disclosure protocol
├── LICENSE                                    # MIT License
└── CITATION.cff                               # Citation metadata format
```

---

## Benchmark Suite Coverage

### 1. Multi-Domain Benchmark Datasets (13 Datasets Across 7 Domains)

The evaluation spans 13 benchmark datasets representing distinct structural characteristics, dimensionality regimes ($D \in [60, 15,154]$), sample scales ($N \in [60, 68,579]$), and cluster counts ($K \in [2, 38]$):

| Dataset | Domain | Samples ($N$) | Features ($D$) | Clusters ($K$) | Ratio ($D/N$) | Structural Challenge | Evaluation Status |
|---|---|:---:|:---:|:---:|:---:|---|:---:|
| **Sonar** | Acoustic Sensors | $208$ | $60$ | $2$ | $0.29$ | Continuous sonar returns (mines vs. rocks) | Verified |
| **Madelon** | Synthetic Distractor | $500$ | $500$ | $2$ | $1.00$ | 20 non-linear XOR features + 480 distractor noise features | Verified |
| **Colon** | Cancer Genomics | $62$ | $2,000$ | $2$ | $32.26$ | Colon tumor vs. normal tissue biopsies | Verified |
| **SRBCT** | Cancer Genomics | $83$ | $2,308$ | $4$ | $27.81$ | Small Round Blue Cell Tumors (4 diagnostic subtypes) | Verified |
| **CNS** | Cancer Genomics | $60$ | $7,129$ | $2$ | $118.82$ | Embryonal central nervous system tumors | Verified |
| **Leukemia** | Cancer Genomics | $72$ | $7,129$ | $2$ | $99.01$ | Acute lymphoblastic vs. acute myeloid leukemia | Verified |
| **Prostate** | Cancer Genomics | $102$ | $12,600$ | $2$ | $123.53$ | Prostate tumor vs. benign prostate specimens | Verified |
| **Ovarian** | Mass Spectrometry | $253$ | $15,154$ | $2$ | $59.90$ | High-resolution SELDI-TOF proteomic mass spectra | Verified |
| **20 Newsgroups** | Text Classification | $18,846$ | $10,000$ | $20$ | $0.53$ | High-dimensional sparse TF-IDF document vectors | Verified |
| **Isolet** | Speech Recognition | $7,797$ | $617$ | $26$ | $0.08$ | Continuous spoken alphabet phoneme spectral features | Verified |
| **Indian Pines** | Hyperspectral Imaging | $10,249$ | $200$ | $16$ | $0.02$ | Airborne AVIRIS sensor continuous spectral reflectance | Verified |
| **Yale B** | Facial Biometrics | $2,414$ | $1,024$ | $38$ | $0.42$ | Cropped facial reflectance across extreme illumination | Verified |
| **Zheng68k** | scRNA-seq Transcriptomics | $68,579$ | $2,000$ | $11$ | $0.03$ | Ultra-sparse single-cell PBMC transcriptomics | Verified |

---

### 2. Baseline Clustering Frameworks (11 Methods Across 4 Paradigms)

ICC-v2 is evaluated against 10 representative baselines:

| Category | Method | Key Reference | Venue and Year | Algorithmic Complexity | Core Mechanism |
|---|---|---|---|:---:|---|
| **Classical Single-Model** | **K-Means** | Lloyd | IEEE TIT 1982 | $\mathcal{O}(N D K)$ | Distance-to-centroid iterative minimization |
| **Classical Single-Model** | **Ward Linkage** | Ward | JASA 1963 | $\mathcal{O}(N^2 D)$ | Hierarchical minimum-variance agglomeration |
| **Classical Single-Model** | **Spectral Clustering** | Von Luxburg | Stat. Comput. 2007 | $\mathcal{O}(N^3)$ | Graph Laplacian eigen-decomposition |
| **Classical Single-Model** | **Fuzzy C-Means (FCM)** | Bezdek | Plenum Press 1981 | $\mathcal{O}(N D K)$ | Soft membership objective optimization |
| **Consensus Ensemble** | **Standard Consensus** | Fred & Jain | IEEE TPAMI 2005 | $\mathcal{O}(N^2)$ | Dense all-pairs co-association matrix |
| **Consensus Ensemble** | **Core-Halo Consensus** | Li et al. | Artif. Intell. 2019 | $\mathcal{O}(N^2)$ | Determinacy-thresholded core extraction |
| **Deep Clustering** | **DEC** | Xie et al. | ICML 2016 | Neural GPU | Autoencoder latent Student-$t$ distribution divergence |
| **Anchor-Based Scalable** | **FCAG** | Nie et al. | IEEE TPAMI 2024 | $\mathcal{O}(N M K)$ | Anchor-guided bipartite graph spectral clustering |
| **Anchor-Based Scalable** | **FastMVC** | Huang et al. | IEEE TKDE 2023 | $\mathcal{O}(N M K)$ | Multi-view bipartite anchor graph consensus fusion |
| **Consensus (Ablation)** | **ICC-v1** (Anchor-Only) | Kundu (This Work) | TKDE 2026 | $\mathcal{O}(N L K)$ | Bipartite core anchors without subspace gating |
| **Consensus (Proposed)** | **ICC-v2** (Full Framework) | Kundu (This Work) | TKDE 2026 | $\mathcal{O}(N L K)$ | VSSG subspace gating + bipartite anchor consensus |

---

## Summary of Key Empirical Findings

### 1. Falsification of Consensus Stability under Distractor Noise (Experiment 0)
- **Universal Stability Trap Refuted:** Isotropic distractor noise does not produce identical failure modes across distinct clustering objectives. K-Means and Gaussian Mixture Models exhibit classical dispersion instability ($\text{Stability} \to 0$ as $D_{\text{noise}} \to \infty$).
- **Objective-Specific Vulnerability:** Graph-partitioning and density-based consensus methods (e.g., Ward and dense spectral consensus) converge toward spurious, highly confident partition artifacts under high dimensions, falsely reporting high stability despite zero true cluster recovery.

### 2. Downstream Inductive Generalization (Experiment 1)
- Under $D_{\text{noise}} \ge 1,000$, training downstream classifiers using determinacy-filtered core pseudo-labels yields an average $+4.5\%$ test accuracy improvement over training on all pseudo-labels across Linear SVM, RBF SVM, Random Forests, Multi-Layer Perceptrons, and K-Nearest Neighbors.

### 3. Component Architectural Ablations (Experiment 2)
- **Core Certification:** Determinacy-based core selection provides a $+34\%$ Adjusted Rand Index (ARI) improvement in clean data regimes ($D_{\text{noise}} = 0$).
- **VSSG Subspace Gating:** Isolating informative dimensions via Sarle's Bimodality Coefficient prevents noise dimension contamination, maintaining cluster recovery in extreme noise regimes ($D_{\text{noise}} \ge 5,000$) where unguided consensus collapses.

### 4. Multi-Domain Benchmarking and Missing-Data Resilience (Experiment 3)
- **High-Dimensional Domain Specialization:** Across 13 benchmark datasets and 1,430 model executions, ICC-v2 achieves a Grand Mean ARI of **0.1599** (mean rank 5.46 across diverse domains). It demonstrates commanding Rank #1 performance on ultra-high-dimensional continuous biomedical cancer assays ($D/N > 20$, e.g., Leukemia ARI = 0.680 vs. DEC 0.148, SRBCT ARI = 0.538 vs. Std Cons 0.040, Ovarian ARI = 0.052), maintaining cluster recovery where deep models collapse due to sample sparsity ($N \le 100$).
- **Operating Envelope & Trade-offs:** On large-sample sparse text and single-cell count matrices (20 Newsgroups, Zheng68k), hierarchical Ward and DEC outperform ICC-v2, as zero-inflation violates the continuous unimodal distractor noise assumption.
- **Missing-Data Stability:** Under Missing Completely At Random (MCAR) rates up to $40\%$, ICC-v2 combined with mean or median imputation maintains over $80\%$ of its nominal cluster recovery accuracy on continuous datasets.

### 5. Computational Scalability and Asymptotic Behavior (Experiments 4 and 5)
- **Linear Sample Scaling:** Empirical execution times scale strictly as $\mathcal{O}(N)$, completing clustering on $N = 1,000,000$ synthetic observations in under 3.5 minutes on standard workstation hardware.
- **Memory Reduction:** Auxiliary bipartite storage requires $O(NL + L^2)$ floats, yielding a $39.1\%$ memory reduction over dense $O(N^2)$ consensus at $N = 8,000$, and enabling execution at scales where dense methods trigger out-of-memory errors.

---

## Environment Setup and Installation

The package requires Python 3.10 or newer and follows PEP 517/621 packaging conventions:

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering

# Install the core package in editable mode
pip install -e .
```

### 2. Optional Dependency Groups

Install additional dependency sets depending on the desired experimental scope:

```bash
# Deep learning baselines (PyTorch, TensorFlow, Keras for DEC)
pip install -e ".[deep]"

# Single-cell transcriptomics tools (Scanpy, AnnData for Zheng68k)
pip install -e ".[bio]"

# Development, static analysis, and testing tools (Pytest, Ruff)
pip install -e ".[dev]"

# All optional dependencies
pip install -e ".[all]"
```

### 3. Test Suite Verification

Run the automated test suite to verify the installation:

```bash
python -m pytest tests/ -v
```

All 62 unit and integration tests should pass without errors.

---

## Reproduction CLI Guide

All experimental figures and tables can be reproduced directly from precomputed evaluation caches or re-executed from scratch:

```bash
# Experiment 0: Falsification Suite (Figures 1-8)
python experiments/exp0_falsification/run_all.py --reproduce-plots

# Experiment 1: Inductive Generalization Suite (Figures 9, 10, 10b, 10c)
python experiments/exp1_generalization/run_exp1.py --run-full

# Experiment 2: Ablation and VSSG Interpretability Audit (Figures 11-13, 22a-c)
python experiments/exp2_ablation/run_exp2.py --reproduce-plots

# Experiment 3: 13-Dataset Benchmarks and Missing Data Audit (Figures 14-17, 25a-b)
python experiments/exp3_real_world_benchmarks/run_exp3.py --reproduce-plots

# Experiment 4: Scalability, Sensitivity, and Anchor Fidelity (Figures 18-21, 23, 24)
python experiments/exp4_scalability_and_sensitivity/run_exp4.py --reproduce-plots

# Experiment 5: Extreme Asymptotic Scaling Stress Suite (Figure 26)
python experiments/exp5_extreme_scale/run_exp5.py --reproduce-plots
```

---

## Python API Usage

The package provides a scikit-learn-compatible estimator interface:

```python
from src.icc import InvariantCoreConsensusV2
from src.icc.datasets import load_dataset
from src.icc.metrics import evaluate_all

# 1. Load benchmark dataset
X, y_true, meta = load_dataset("leukemia")
print(f"Loaded {meta['display_name']}: N={X.shape[0]}, D={X.shape[1]}")

# 2. Initialize and fit the ICC-v2 estimator
model = InvariantCoreConsensusV2(
    n_clusters=2,
    n_base_models=25,
    n_anchors=40,
    subspace_rate=0.25,
    core_quantile=0.50,
    beta=2.0,
    random_seed=42,
)
labels = model.fit_predict(X)

# 3. Evaluate clustering quality across standardized metrics
metrics = evaluate_all(y_true, labels)
print("Evaluation Results:")
print(f"  Adjusted Rand Index (ARI):       {metrics['ari']:.4f}")
print(f"  Normalized Mutual Info (NMI):    {metrics['nmi']:.4f}")
print(f"  Adjusted Mutual Info (AMI):      {metrics['ami']:.4f}")
print(f"  V-Measure:                       {metrics['v_measure']:.4f}")
print(f"  Fowlkes-Mallows Index (FM):      {metrics['fm_index']:.4f}")

# 4. Inductive out-of-sample prediction
out_of_sample_points = X[:5]
predicted_clusters = model.predict(out_of_sample_points)
print("Inductive predictions for query instances:", predicted_clusters)
```

---

## Citation and Academic Context

If you use this codebase, benchmark results, or methodology in your research, please cite:

```bibtex
@article{kundu2026inductive,
  author       = {Akash Kundu},
  title        = {Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes},
  journal      = {Manuscript Submitted for Peer Review},
  year         = {2026},
  institution  = {Techno India University},
  url          = {https://github.com/AkashKundu114/icc-clustering}
}
```

---

## License

This project is licensed under the [MIT License](LICENSE).
