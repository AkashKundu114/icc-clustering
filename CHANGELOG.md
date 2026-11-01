# Changelog

All notable changes to the Invariant Core Consensus (`icc`) package are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.2.1] - 2026-11-01

### Added
- **XERJ Corpus Hub Contributor Badge:** Integrated official XERJ Corpus Hub indexing and contributor badge into `README.md` and `CONTRIBUTING.md` for AI agent reference search.
- **Python 3.10–3.14 CI/CD Matrix:** Configured full GitHub Actions matrix workflow testing across Python 3.10, 3.11, 3.12, 3.13, and 3.14 on both Ubuntu and Windows (`.github/workflows/ci.yml`).
- **Python 3.13 & 3.14 Compatibility Test Suite:** Added dedicated regression tests (`tests/regression/test_python_compatibility.py`) validating PEP 706 safe tarfile extraction, PEP 649/749 deferred annotation evaluation, dataclass typing resolution, and end-to-end estimator execution under modern runtimes.
- **Statistical Testing Extensions:** Implemented `wilcoxon_signed_rank_test` and `bonferroni_correction` in `src/icc/stats/testing.py` with PEP 484 type annotations.

### Changed
- **Test Suite Expansion:** Expanded automated test battery from 118 to 133 passing tests with 100% pass rate and 67% statement coverage.
- **Architecture Deduplication:** Converted duplicate `src/icc/aspp.py` into an 18-line backward-compatibility shim re-exporting from canonical `src/icc/consensus/aspp.py`.
- **Public Documentation Overhaul:** Synchronized and modernized all repository guides (`README.md`, `setup.md`, `usage.md`, `development.md`, `reproducibility.md`, `CONTRIBUTING.md`), fixing code fence formatting and standardizing references.

### Security
- **Archive Extraction Hardening:** Integrated PEP 706 `data_filter` checks in `src/icc/datasets/scrnaseq.py` to prevent directory traversal (TarSlip).
- **Web Demo CORS & Validation:** Restricted CORS wildcard origins and enforced boundary validation on API endpoints in `examples/web_demo/app/main.py`.
- **NumPy File Descriptors:** Enforced context-manager handling for `np.load` calls across dataset loaders.

---

## [2.2.0] - 2026-10-29

### Added
- **Automated Verification Suite:** Comprehensive test battery covering mathematical bounds, algorithm parity, and numerical determinacy.
- **Real-Data Stability Analysis:** Empirical measurement of the stability-accuracy trade-off across 13 benchmarks x 12 methods.

### Changed
- **Modern Literature Overhaul:** Upgraded comparative baselines and references across leading machine learning and data mining literature.
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
