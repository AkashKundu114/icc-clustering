# Changelog

All notable changes to the Inductive Consensus Clustering (`icc`) package are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.1.0] - 2026-10-23

### Added
- **Conformal Inductive Consensus Clustering (src/cicc/):** Unified framework combining bipartite anchor consensus, target-decoy / knockoff feature gating with False Discovery Rate (FDR) control, and finite-sample split-conformal cluster assignment with guaranteed error coverage 1 - α.
- **Real-World Application Scripts (examples/):** Standalone reproducible pipelines for clinical oncological diagnostic subtyping (clinical_cancer_subtyping.py evaluating Leukemia and SRBCT) and real-time held-out point-of-care patient projection (realtime_patient_projection.py achieving 22.6 μs per-query latency).
- **Comprehensive Ablation Suite:** Component knockout benchmarks across 6 high-D datasets evaluating feature gating, bipartite anchor graph projection, base ensembling, and certified vs. random anchor selection.
- **Publication Experimental Visualizations (paper/figures/):** Tracked 58 high-resolution publication benchmark figures and architecture schematics validating asymptotic scaling, noise robustness, critical difference rankings, and hyperparameter sensitivity.

### Changed
- **Pre-Publication Embargo Boundary:** Separated public algorithm source code, benchmarks, and figures from unpublished draft manuscript text and compilation binaries.
- **Package Version Alignment:** Unified version declaration (2.1.0) across pyproject.toml and src/icc/__init__.py.

### Removed
- **Legacy Audit Artifacts:** Cleaned obsolete submission_audit/ records from repository tracking.

---

## [2.0.0] - 2026-10-17

### Added
- **`ICC` Top-Level Estimator:** Exposes scikit-learn standard interface (`fit`, `predict`, `predict_proba`, `transform`, `fit_predict`) as alias for `InvariantCoreConsensusV2`.
- **Variance-Stabilized Subspace Gating (VSSG):** Multimodality screening based on Sarle's Bimodality Coefficient ($b_d = \frac{\text{skew}_d^2 + 1}{\text{kurt}_d + 3}$) with configurable gating modes (`"legacy"`, `"null_calibrated"`, `"robust"`, `"gauss"`).
- **Linear-Time Bipartite Anchor Consensus:** Reduces auxiliary memory from $\mathcal{O}(N^2)$ to $\mathcal{O}(NL)$ through rectangular bipartite co-association graph $B \in \mathbb{R}^{N \times L}$.
- **Transfer-Cut Subspace Projection:** Correct degree and eigenvalue scaling for bipartite graph Laplacian spectral embedding.
- **Closed-Form Inductive Projection:** Stability-weighted active subspace centroid assignment requiring $\mathcal{O}(K \cdot |\mathcal{F}_{\text{active}}|)$ operations per query point.
- **Anchor-Space Perturbation Profiling (ASPP):** Multi-family cluster reliability certification yielding Perturbation Sensitivity Index (PSI) and query confidence bounds in $\mathcal{O}(NL)$ auxiliary memory.
- **Automated Macro Synchronizer:** `scripts/make_numbers.py` extracting single-source-of-truth metrics from `results/` directly into LaTeX macros.
- **Standard Tooling & CI Configuration:** Complete `pyproject.toml` (PEP 621), GitHub Actions workflows (`.github/workflows/ci.yml`), pre-commit hooks, `.editorconfig`, and automated dataset downloader (`scripts/fetch_data.py`).

### Changed
- **Subgroup Ranking Aligned:** Updated empirical claims and documentation to report accurate subgroup rank ($R = 2.33$ on $D/N > 20$, #1 rank) and calibrated Nemenyi Critical Difference ($\text{CD} = 4.21$ for $k=11, N=13$).
- **Cleaned Internal Imports:** Transitioned all internal imports to package-relative or clean `icc.*` layout, resolving duplicate package base collisions in static type analysis.
- **Stripped Internal Comments:** Removed all inline `#` implementation comments across `src/` to ensure documentation prose lives exclusively in markdown specifications, retaining single-line docstrings on public APIs.

### Fixed
- **Proposition 1 Analytic Boundary:** Fixed minimum theoretical cluster separation bound to $\Delta/\sigma_0 \approx 1.854$, verified via numerical quadrature across $\nu \in [5, 100]$.
- **Madelon XOR Boundary Limitation:** Documented theoretical limitation of 1D marginal unimodality screening on non-linear multi-feature XOR interactions.
- **Type Annotations & Diagnostics Import:** Fixed dual-backend dynamic imports in `metrics.py` and canonical export typing across `icc.__init__`.
