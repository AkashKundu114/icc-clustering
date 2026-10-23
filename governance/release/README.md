# Software Release Governance & Quality Assurance

**Location:** `governance/release/`  
**Purpose:** Release verification records, regression test baselines, licensing decisions, and GitHub lifecycle management for the `icc` Python package.  
**Current Release Version:** `v2.0.0` / `v2.1.0`

---

## 1. Executive Summary for Mentors & Reviewers

This directory contains the quality assurance and release engineering records for the Inductive Consensus Clustering package (`icc`). It documents the pre-release audit, regression test baselines, licensing structure, and GitHub repository configuration required for publishing professional open-source research software.

---

## 2. Directory Contents & Navigation

| Document / Asset | Purpose & Scope |
| :--- | :--- |
| **[`RELEASE_REPORT.md`](RELEASE_REPORT.md)** | **Executive Release Sign-Off:** Documents the release verification battery for `v2.0.0`, including test pass rates (100%), code coverage (75%), static type checks (0 errors), and cross-platform installation smoke tests. |
| **[`AUDIT.md`](AUDIT.md)** | **Repository Sanitization Audit:** File-by-file audit ensuring that no unverified binaries, temporary caches, confidential credentials, or internal agent workflows are committed into the release artifact. |
| **[`LICENSE_DECISION.md`](LICENSE_DECISION.md)** | **Open-Source License Analysis:** Legal and practical justification for selecting the permissive MIT License for academic and commercial interoperability. |
| **[`GITHUB_SETTINGS.md`](GITHUB_SETTINGS.md)** | **Repository Configuration & Discoverability:** Settings roadmap for GitHub topics (`clustering`, `consensus-clustering`, `high-dimensional-data`, `spectral-clustering`), branch protection on `main`, and citation metadata. |
| **[`DEFERRED.md`](DEFERRED.md)** | **Post-Release Enhancement Backlog:** Documented roadmap items deferred to future releases (e.g., GPU-accelerated sparse matrix kernels, streaming consensus updates). |
| **[`baseline/`](baseline/)** | **Frozen Regression Test Logs:** Baseline stdout logs from initial test runs (`pytest_baseline.txt`, `mypy_baseline.txt`, `ruff_baseline.txt`) establishing the reference standard for regression prevention. |

---

## 3. Automated Release & CI Gates

All changes to the repository must satisfy the automated validation pipeline in `.github/workflows/ci.yml`:
1. **Linting & Formatting:** `ruff check src/ tests/` (zero warnings).
2. **Static Type Checking:** `mypy -p icc` (`py.typed` compliant across all 21 source modules).
3. **Unit & Integration Suite:** `pytest tests/` (all 84 unit tests passing).
4. **Reproducibility Smoke Run:** `python scripts/reproduce.py --scope smoke` (deterministic synthetic clustering verified).
5. **Manuscript Macro Consistency:** `python tests/test_macro_consistency.py` (zero hardcoded numbers).
6. **PDF Numerical Allowlist:** `python tests/test_pdf_allowlist.py` (strict regex scan of compiled PDF decimals).
