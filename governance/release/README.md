# Software Release Governance & Quality Assurance

**Location:** `governance/release/`  
**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Purpose:** Release verification records, regression test baselines, licensing decisions, and GitHub lifecycle management for the `icc` and `cicc` packages.

---

## 1. Executive Summary for Mentors, Reviewers & Auditors

This directory contains quality assurance and release engineering records for the Inductive Consensus Clustering (`icc`) and Conformal Inductive Consensus Clustering (`cicc`) packages. It documents pre-release audits, regression test baselines, licensing structure, and GitHub repository configuration required for publishing professional open-source research software accompanying our Springer Nature manuscript.

### Verified Empirical Single Source of Truth (`paper/numbers.tex`)
All benchmarks and quantitative claims reflect the frozen Pass F execution store:
- **Benchmark Scale:** 13 multi-domain benchmark datasets, 2,750 individual model fits, 11 baseline solvers.
- **Omnibus Friedman Test:** $\chi_F^2 = 9.59, p = 0.48$, Nemenyi Critical Difference $CD = 4.19$ (confirming absence of global dominance across diverse datasets).
- **Target High-Dimensional Subgroup ($D/N > 20$):** ICC-v2 commands **Rank #1** with Mean ARI = 0.217 (vs Standard Consensus 0.037, DEC 0.045, K-Means 0.056).
- **Omnibus Ranks & Grand Mean:** ICC-v2 achieves Grand Mean ARI = 0.152 (Rank 5.23).
- **Key Biomedical Assays:** Golub Leukemia: ARI = 0.600, Khan SRBCT: ARI = 0.546.
- **Asymptotic Complexity Scaling:** $N = 10^6$ in 55.6 s (3.05 GB peak RSS, 240 MB graph memory, 99.6% reduction over dense 8 TB co-association matrix).

---

## 2. Directory Contents & Navigation

| Document / Asset | Purpose & Scope |
| :--- | :--- |
| **[`RELEASE_REPORT.md`](RELEASE_REPORT.md)** | **Executive Release Sign-Off:** Documents the release verification battery for active release `v2.1.0` (and historical baseline `v2.0.0`), covering `icc` core estimator, `cicc` conformal prediction, test pass rates (100%), code coverage, static typing, and reproducible installation smoke tests. |
| **[`AUDIT.md`](AUDIT.md)** | **Repository Sanitization Audit:** Comprehensive audit verifying that zero unverified binaries, temporary caches, confidential credentials, or internal agent workflows are committed into the release artifact. |
| **[`LICENSE_DECISION.md`](LICENSE_DECISION.md)** | **Open-Source License Analysis:** Legal and practical justification for selecting the permissive MIT License for academic and commercial interoperability. |
| **[`GITHUB_SETTINGS.md`](GITHUB_SETTINGS.md)** | **Repository Configuration & Discoverability:** Settings roadmap for GitHub topics (`clustering`, `consensus-clustering`, `high-dimensional-data`, `spectral-clustering`), branch protection on `main`, and citation metadata. |
| **[`DEFERRED.md`](DEFERRED.md)** | **Post-Release Enhancement Backlog:** Documented roadmap items deferred to future releases (e.g., GPU-accelerated sparse matrix kernels, streaming consensus updates). |
| **[`baseline/`](baseline/)** | **Frozen Regression Test Logs:** Baseline stdout logs from test runs (`pytest_baseline.txt`, `mypy_baseline.txt`, `ruff_baseline.txt`) establishing the reference standard for regression prevention. |

---

## 3. Active Release Features (`v2.1.0`)

The active release `v2.1.0` builds directly upon the historical `v2.0.0` foundational architecture:
1. **Conformal Inductive Consensus Clustering (`src/cicc/`):**
   - Finite-sample distribution-free $(1 - \alpha)$ coverage guarantees for cluster membership.
   - Target-decoy / knockoff False Discovery Rate (FDR) feature selection.
   - Point-of-care patient safety triage identifying ambiguous or out-of-distribution queries.
2. **Clinical Oncology Diagnostic Pipelines (`examples/`):**
   - `examples/clinical_cancer_subtyping.py`: Reproducible diagnostic stratification evaluating Golub Leukemia and Khan SRBCT datasets.
   - `examples/realtime_patient_projection.py`: Ultra-low latency out-of-sample patient projection (22.6 us per query) with conformal prediction sets.
3. **Publication Figure Tracking (`paper/figures/`):**
   - Comprehensive tracking of 58 publication benchmark figures, critical difference diagrams, and scaling profiles.

---

## 4. Automated Release & CI Gates

All changes to the repository must satisfy the automated validation pipeline:
1. **Linting & Formatting:** `ruff check src/ tests/` (zero warnings).
2. **Static Type Checking:** `mypy -p icc` (`py.typed` compliant across all source modules).
3. **Unit & Integration Suite:** `pytest tests/` (all unit and integration tests passing).
4. **Reproducibility Smoke Run:** `python scripts/reproduce.py --scope smoke` (deterministic synthetic clustering verified).
5. **Manuscript Macro Consistency:** `python tests/test_macro_consistency.py` (zero hardcoded numbers).
6. **PDF Numerical Allowlist:** `python tests/test_pdf_allowlist.py` (strict regex scan of compiled PDF decimals).
