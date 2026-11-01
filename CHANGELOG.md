# Changelog

All notable changes to the Invariant Core Consensus (`icc`) package are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.2.0] - 2026-10-29

### Added
- **Automated Verification Suite:** Comprehensive test battery covering mathematical bounds, algorithm parity, and numerical determinacy.
- **Real-Data Stability Analysis:** Empirical measurement of the stability-accuracy trade-off across 13 benchmarks x 12 methods.

### Changed
- **Modern Literature Overhaul:** Upgraded comparative baselines and references across leading machine learning and data mining literature.
- **Empirical Harmonization:** Reconciled model fit count across 12 clustering pipelines (30 seeds on 6 high-D datasets, 10 seeds on 7 general datasets); Friedman stat = 11.56, p = 0.40, Nemenyi CD = 4.62; GAC pipeline commands Rank #1 on high-D biological cohorts (D/N > 20, mean ARI = 0.217, mean rank 2.17).
- **Test Suite Expansion:** Expanded automated test suite to 118 passing tests with 100% pass rate.

---

## [2.1.0] - 2026-10-23

### Added
- **Conformal Inductive Consensus Clustering (src/cicc/):** Unified framework combining bipartite anchor consensus, target-decoy feature gating with False Discovery Rate (FDR) control, and finite-sample split-conformal cluster assignment with guaranteed error coverage 1 - α.
- **Comprehensive Ablation Suite:** Component knockout benchmarks across 6 high-D datasets evaluating feature gating, bipartite anchor graph projection, base ensembling, and certified vs. random anchor selection.

### Changed
- **Modular Package Structure:** Separated public algorithm source code, benchmarks, and modular test hierarchy into canonical subpackages (`algorithms/`, `consensus/`, `data/`, `evaluation/`, `experiments/`, `stats/`, `utils/`).
- **Package Version Alignment:** Unified version declaration (2.2.0) across `pyproject.toml` and `src/icc/__init__.py`.

---

## [2.0.0] - 2026-10-17

### Added
- **`ICC` Top-Level Estimator:** Exposes scikit-learn standard interface (`fit`, `predict`, `predict_proba`, `transform`, `fit_predict`) as alias for `InvariantCoreConsensusV2`.
- **Variance-Stabilized Subspace Gating (VSSG):** Multimodality screening based on Sarle's Bimodality Coefficient with configurable gating modes (`"legacy"`, `"null_calibrated"`, `"robust"`, `"gauss"`).
- **Linear-Time Bipartite Anchor Consensus:** Reduces auxiliary memory from $\mathcal{O}(N^2)$ to $\mathcal{O}(NL)$ through rectangular bipartite co-association graph $B \in \mathbb{R}^{N \times L}$.
- **Transfer-Cut Subspace Projection:** Correct degree and eigenvalue scaling for bipartite graph Laplacian spectral embedding.
- **Closed-Form Inductive Projection:** Stability-weighted active subspace centroid assignment requiring $\mathcal{O}(K \cdot |\mathcal{F}_{\text{active}}|)$ operations per query point.
- **Anchor-Space Perturbation Profiling (ASPP):** Multi-family cluster reliability certification yielding Perturbation Sensitivity Index (PSI) and query confidence bounds in $\mathcal{O}(NL)$ auxiliary memory.
- **Standard Tooling & CI Configuration:** Complete `pyproject.toml` (PEP 621), GitHub Actions workflows (`.github/workflows/ci.yml`), pre-commit hooks, `.editorconfig`, and automated dataset downloader (`scripts/fetch_data.py`).

### Changed
- **Cleaned Internal Imports:** Transitioned all internal imports to package-relative or clean `icc.*` layout.

### Fixed
- **Proposition 1 Analytic Boundary:** Fixed minimum theoretical cluster separation bound to $\Delta/\sigma_0 \approx 1.854$, verified via numerical quadrature across $\nu \in [5, 100]$.
- **Madelon XOR Boundary Limitation:** Documented theoretical limitation of 1D marginal unimodality screening on non-linear multi-feature XOR interactions.
- **Type Annotations & Diagnostics Import:** Fixed dual-backend dynamic imports in `metrics.py` and canonical export typing across `icc.__init__`.
