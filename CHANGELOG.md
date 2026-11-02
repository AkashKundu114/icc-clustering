# Changelog

All notable changes to ICC Clustering (`icc` import package; `icc-clustering` distribution) are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.2.1] - 2026-11-02

### Added
- **XERJ Corpus Hub contributor badge:** Retained the project contributor badge and profile link in the public README.
- **Public project documentation:** Updated researcher-facing project and installation guidance.
- **Research scope and naming documentation:** Clarified the stability versus external alignment distinction, the separate benchmark scopes, and that `ICC`/`ICCv2` are aliases for one estimator.
- **Python 3.10–3.14 CI/CD Matrix:** Configured full GitHub Actions matrix workflow testing across Python 3.10, 3.11, 3.12, 3.13, and 3.14 on both Ubuntu and Windows (`.github/workflows/ci.yml`).
- **Python 3.13 & 3.14 Compatibility Test Suite:** Added dedicated regression tests (`tests/regression/test_python_compatibility.py`) validating PEP 706 safe tarfile extraction, PEP 649/749 deferred annotation evaluation, dataclass typing resolution, and end-to-end estimator execution under modern runtimes.
- **Statistical Testing Extensions:** Implemented `wilcoxon_signed_rank_test` and `bonferroni_correction` in `src/icc/stats/testing.py` with PEP 484 type annotations.

### Changed
- **Distribution metadata:** The installable distribution is named `icc-clustering`; Python imports remain `icc`. This avoids directing users to an unrelated project registered under the shorter package name.
- **Reproduction CLI:** Removed unsupported `tables`, `figures`, and `full` scopes that returned success without generating research results.
- **Public data-rights metadata:** Replaced blanket license claims with source-variant evidence and explicit un-cleared redistribution status.
- **Version identity:** Aligned package, runtime, citation, and archival draft metadata at version 2.2.1.
- **Test Suite Expansion:** Expanded the automated test suite; run the current test suite to verify this source snapshot.
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
- **Benchmark utilities:** Added utilities for external-ARI benchmark evaluation. This changelog entry does not represent a 13-dataset stability experiment; the repository documentation distinguishes the 13-dataset external benchmark from the six-cohort stability study.

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
