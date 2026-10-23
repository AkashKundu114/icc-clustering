# ICC Software Release Verification Report (v2.1.0 Active Release & v2.0.0 Historical Baseline)

**Document Reference:** Release Verification Dossier for ICC-v2 and CICC  
**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Current Active Release Version:** `v2.1.0`  
**Prior Historical Release Baseline:** `v2.0.0` (Tag Date: 2026-10-17)  
**Lead Auditor:** Senior Research Governance & Reproducibility Auditor

---

## 1. Executive Summary & Release Verdict

The software repository `github.com/AkashKundu114/icc-clustering` has completed full formal verification for active release `v2.1.0` while maintaining complete historical audit continuity with foundational baseline `v2.0.0`.

- **Release Verdict:** **APPROVED FOR ACTIVE PRODUCTION & SUBMISSION ARCHIVAL (`v2.1.0`)**.
- **Test Suite Verification:** 84/84 unit and integration tests passing (100% pass rate).
- **Static Analysis & Linting:** Clean pass on `ruff check src/ tests/` (0 warnings) and `mypy -p icc` (0 errors, full `py.typed` compliance across all modules).
- **Comment Policy Compliance:** Strict comment-free policy across core algorithms in `src/` (0 `#` tokens in algorithmic implementations); verified by AST equivalence and static scanning.
- **Packaging Standard:** Fully compliant PEP 517/621 `pyproject.toml`, standard editable install `pip install -e .` and `pip install -e ".[dev]"`.

---

## 2. Release Scope & Evolution (v2.0.0 Baseline to v2.1.0 Active)

### 2.1 Active Release `v2.1.0` Additions
1. **Conformal Inductive Consensus Clustering (`src/cicc/`):**
   - Finite-sample distribution-free $(1 - \alpha)$ coverage guarantees with split-conformal p-values.
   - Target-decoy / knockoff False Discovery Rate (FDR) feature selection.
   - Point-of-care patient safety triage identifying ambiguous or out-of-distribution queries.
2. **Clinical Cancer Subtyping Pipelines (`examples/`):**
   - `examples/clinical_cancer_subtyping.py`: Full diagnostic workflow evaluating real-world clinical cancer microarrays (Golub Leukemia and Khan SRBCT).
   - `examples/realtime_patient_projection.py`: Real-time point-of-care biopsy projection with conformal prediction sets, achieving 22.6 us per-query latency.
3. **Publication Figure Tracking (`paper/figures/`):**
   - Tracked 58 publication benchmark figures, critical difference diagrams, runtime profiles, and ablation plots.
4. **Pre-Publication Embargo Boundary:**
   - Public algorithm source code, benchmarks, and figures clearly delineated from unpublished draft manuscript text.

### 2.2 Historical Baseline `v2.0.0` Foundations
- Top-level estimator `ICC` (alias for `InvariantCoreConsensusV2`) with standard scikit-learn API (`fit`, `predict`, `predict_proba`, `transform`, `fit_predict`).
- Bimodality-Gated Subspace Selection (BGSS / VSSG) with finite-sample null calibration.
- Rectangular bipartite anchor consensus graph $B \in \mathbb{R}^{N \times L}$ with Transfer-Cut spectral projection.
- Closed-form inductive projection in $O(K \cdot |\mathcal{F}_{\text{active}}|)$ operations.
- Anchor-Space Perturbation Profiling (ASPP) for cluster reliability certification.

---

## 3. Single Source of Truth Metrics (`paper/numbers.tex`)

All reported metrics are verified against the frozen Pass F execution store:
- **Benchmark Coverage:** 13 multi-domain benchmark datasets, 2,750 individual model fits, 11 baseline solvers (30 random seeds on 6 high-D datasets, 10 seeds on 7 general datasets).
- **Omnibus Friedman Test:** $\chi_F^2 = 9.59, p = 0.48$, Nemenyi Critical Difference $CD = 4.19$ (confirming absence of global dominance across diverse domains).
- **Target High-Dimensional Subgroup ($D/N > 20$):** ICC-v2 commands **Rank #1** with Mean ARI = 0.217 (vs Standard Consensus 0.037, DEC 0.045, K-Means 0.056).
- **Grand Mean ARI:** 0.152 across all 13 benchmarks (Rank 5.23).
- **Biomedical Microarrays:** Golub Leukemia: ARI = 0.600, Khan SRBCT: ARI = 0.546.
- **Asymptotic Complexity Scaling:** $N = 10^6$ instances in 55.6 s (3.05 GB peak RSS, 240 MB graph memory, 99.6% reduction over dense 8 TB co-association matrix).

---

## 4. Cryptographic Smoke Hash Comparison

Deterministic smoke evaluation is verified using `OMP_NUM_THREADS=1`:

| Trial | Frozen Baseline SHA256 | Release Candidate SHA256 | Verification Status |
| :--- | :--- | :--- | :---: |
| **Toy Dataset (N=100, D=20)** | `813664b8a3fb86a5f6a32287f371bf569907b20ee94c449f83457f10fd14c29b` | `813664b8a3fb86a5f6a32287f371bf569907b20ee94c449f83457f10fd14c29b` | **EXACT MATCH** |
| **Leukemia Seed 0** | `018085f09652f00685625c24e10e0a105a5bf74ee5671ff939918d7240d52383` | `018085f09652f00685625c24e10e0a105a5bf74ee5671ff939918d7240d52383` | **EXACT MATCH** |
| **Leukemia Seed 1** | `ea87bd61348e7d86e55767c1a33ac99ca0f5469c5220337058ae4e554688793d` | `ea87bd61348e7d86e55767c1a33ac99ca0f5469c5220337058ae4e554688793d` | **EXACT MATCH** |
| **Leukemia Seed 2** | `315034f7f22eaaa0416fb15dae06c75e983b172da0a2d5318d546d2dcc6a8c47` | `315034f7f22eaaa0416fb15dae06c75e983b172da0a2d5318d546d2dcc6a8c47` | **EXACT MATCH** |

---

## 5. Gate Verification Checklist

| Gate | Scope | Status | Evidence / Verification Path |
| :--- | :--- | :---: | :--- |
| **Gate A** | Reconnaissance Audit & Baseline Capture | **PASS** | `governance/release/AUDIT.md`, `governance/release/baseline/` |
| **Gate B** | Packaging & Scikit-Learn API Exposure | **PASS** | `pyproject.toml`, `requirements.txt`, `src/icc/__init__.py` |
| **Gate C** | Code Quality, Static Typing & Formatting | **PASS** | `ruff` (0 errors), `mypy` (0 errors), zero inline `#` in core logic |
| **Gate D** | Documentation, Guides & API Specifications | **PASS** | `README.md`, `docs/api.md`, `docs/DATA.md`, `CHANGELOG.md` |
| **Gate E** | CI Workflows, Security & License Decision | **PASS** | `.github/workflows/ci.yml`, `governance/release/LICENSE_DECISION.md` |
| **Gate F** | Conformal Inductive Projection & Oncology Examples | **PASS** | `src/cicc/`, `examples/`, `paper/figures/`, 84/84 tests passing |
