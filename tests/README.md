# Test Automation Suite

This directory contains the unit, integration, and build-time consistency test suites for the reference implementation of:

> **When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination**  
> *Target Venue:* Springer Nature (*Data Mining and Knowledge Discovery* / DAMI)  
> *Release Version:* v2.1.0  
> *Total Tests:* 86 passing (100% pass rate)

---

## Architecture Overview

The test suite is structured into four functional tiers:

1. **Algorithm and Core Mechanics**: Tests for the Invariant Core Consensus v2 (ICC-v2) solver, bipartite graph construction, spectral embedding backends, synthetic data generators, and mathematical co-association invariants.
2. **Conformal and Inductive Generalization**: Tests for Conformal Inductive Consensus Clustering (CICC), target-decoy feature gating with FDR control, closed-form out-of-sample projection, and downstream multi-classifier generalization.
3. **Baselines, Metrics, and Datasets**: Tests covering 10+ baseline clustering algorithms, evaluation metrics with dual-backend parity (scikit-learn and pure NumPy/SciPy fallback), and dataset registry loading and caching.
4. **Reproducibility and Macro Traceability**: Strict build-time validation asserting that every macro in `springer_manuscript/numbers.tex`, every table in the manuscript, and every numerical value in compiled artifacts matches the frozen experimental results store.

---

## Test Catalog

The test suite contains 13 modular test files:

| Test File | Focus Area | Canonical Modules Covered |
| :--- | :--- | :--- |
| `test_consensus_v2.py` | Core ICC-v2 Algorithm | `icc.consensus_v2.InvariantCoreConsensusV2`, bipartite graph, candidate pool modes (`legacy`, `bc_frac`, `random_frac`, `robust`, `null_calibrated`), spectral embeddings (`legacy`, `transfer_cut`), and beta deprecation. |
| `test_cicc.py` | Conformal & Memory | `cicc.decoy.DecoyFeatureGating` (FDR control), `cicc.conformal.ConformalClusterer` (finite-sample coverage), `cicc.inductive.InductiveConsensusClusterer`, and `cicc.memory.InductiveConsensusMemory`. |
| `test_inductive_projection.py` | Inductive Projection | Geometry-calibrated out-of-sample projection (`.predict`, `.predict_proba`), subspace gating advantage under noise, and temperature scaling monotonicity. |
| `test_aspp.py` | Perturbation Profiling | `icc.aspp.AnchorSpacePerturbationProfiler`, `icc.aspp.ASPPConfig`, perturbation stability index (PSI), and reliability categorization. |
| `test_baselines.py` | Baseline Algorithms | Baseline registry dispatch (`list_models`, `get_model`), classical solvers (K-Means, Ward, Spectral, FCM), consensus baselines, anchor solvers (FCAG, FastMVC), and deep clustering interfaces. |
| `test_metrics.py` | Evaluation Metrics | `icc.metrics.evaluate_all`, `evaluate_all_with_ci`, dual-backend fallback parity (scikit-learn vs pure NumPy/SciPy), ARI, NMI, AMI, V-Measure, and Fowlkes-Mallows index. |
| `test_datasets.py` | Dataset Registry | Unified dataset registry (13 benchmark datasets across 6 domains), metadata validation against `configs/datasets.yaml`, cache loaders, and preprocessing pipeline. |
| `test_core_and_generators.py` | Generators & Core Math | Synthetic benchmark generator (`build_dataset` across 5 noise regimes), pairwise co-association properties, base clustering engines, and legacy ICC-v1 solver. |
| `test_edge_cases.py` | Numerical Robustness | Robustness against zero-variance features, duplicate instances, tiny sample size limits ($N=10$), extreme dimension ratio ($D/N=250$), metric boundaries, and MCAR missing data imputation. |
| `test_macro_consistency.py` | Macro & Manuscript Traceability | Single-source-of-truth verification ensuring all LaTeX macros in `numbers.tex`, Table 4, Table 5, and Fig. 8 scaling curves reconcile with frozen Pass F result stores. |
| `test_pdf_allowlist.py` | PDF Numerical Audit | Regex-level text audit of compiled `springer_manuscript/main.pdf` ensuring zero ungrounded decimals, purging stale tokens, and confirming Figure 7 critical difference ranks. |
| `test_anchor_fidelity.py` | Scalability & Fidelity | Scalability sweep verification, approximation fidelity bounds between bipartite anchor consensus and exact dense consensus graph. |
| `test_exp1_multiclassifier.py` | Downstream Generalization | Downstream inductive classifier generalization across SVM, Random Forest, Multi-Layer Perceptron (MLP), and K-Nearest Neighbors (KNN). |

---

## Execution Guide

### Running the Complete Suite

To run all 86 tests with coverage reporting:

```powershell
pytest tests/
```

### Running Fast Focused Suites

To run specific modules or functional groups:

```powershell
# 1. Core ICC-v2 solver and bipartite graph tests
pytest tests/test_consensus_v2.py

# 2. Conformal prediction and out-of-sample projection
pytest tests/test_cicc.py tests/test_inductive_projection.py

# 3. ASPP perturbation profiling
pytest tests/test_aspp.py

# 4. Baselines and evaluation metrics
pytest tests/test_baselines.py tests/test_metrics.py

# 5. Numerical robustness and edge cases
pytest tests/test_edge_cases.py

# 6. Build-time macro and manuscript consistency
pytest tests/test_macro_consistency.py tests/test_pdf_allowlist.py
```

### Verbose Output Without Coverage

```powershell
pytest tests/ -v --no-cov
```

---

## Test Environment Requirements

- **Python Version**: 3.10 or higher (tested on Python 3.10, 3.11, 3.12, 3.13, 3.14)
- **Core Dependencies**: `numpy`, `scipy`, `pandas`, `scikit-learn`, `pytest`, `pytest-cov`, `pyyaml`
- **Optional Dependencies**:
  - `pymupdf` (for `test_pdf_allowlist.py`)
  - `scanpy`, `anndata` (for un-cached scRNA-seq tests; skipped gracefully if absent)
  - `torch`, `tensorflow`, `keras` (for deep baselines; skipped gracefully if absent)
