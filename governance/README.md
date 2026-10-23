# Research Governance, Provenance & Quality Assurance Dossiers

**Location:** `governance/`  
**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as the prior historical release baseline)*  
**Packages:** `icc` (Inductive Consensus Clustering), `cicc` (Conformal Inductive Consensus Clustering)

---

## 1. Executive Summary for Mentors, Reviewers & Auditors

To maintain the highest level of research integrity, mathematical reproducibility, and software engineering standards, all audit trails, preregistrations, theoretical proofs, empirical registries, and release governance records are consolidated within this directory:

```
governance/
├── remediation/       # Scientific audit trail, issue ledger, theory proofs, and claim verifications
├── preregistration/   # Preregistration protocols (Passes A-F), CrossRef reference audits, literature matrix
└── release/           # Software release reports (v2.1.0 / v2.0.0), MIT license analysis, and test baseline logs
```

### Verified Empirical Single Source of Truth (`paper/numbers.tex`)
All quantitative claims and manuscript tables strictly adhere to the frozen Pass F execution store:
- **Benchmark Breadth:** 13 multi-domain benchmark datasets, 2,750 individual model fits, 11 baseline solvers.
- **Omnibus Statistical Test:** Friedman test yields $\chi_F^2 = 9.59, p = 0.48$, Nemenyi Critical Difference $CD = 4.19$ (confirming no global dominance across heterogeneous benchmarks).
- **Target High-Dimensional Subgroup ($D/N > 20$):** ICC-v2 commands **Rank #1** with Mean ARI = 0.217 (vs Standard Consensus 0.037, DEC 0.045, K-Means 0.056).
- **Omnibus Ranks & Grand Mean:** ICC-v2 attains Grand Mean ARI = 0.152 (Rank 5.23).
- **Key Biomedical Microarrays:** Golub Leukemia: ARI = 0.600, Khan SRBCT: ARI = 0.546.
- **Asymptotic Complexity Scaling:** $N = 10^6$ instances in 55.6 s (3.05 GB peak RSS, 240 MB graph memory, 99.6% reduction over dense 8 TB co-association matrix).

---

## 2. Directory Map & Core Documents

### 2.1 [`remediation/`](remediation/README.md): Scientific Remediation & Verification Dossier
*Systematic tracking and verification of all 27 technical, numerical, and theoretical issues:*
- **[`remediation/LEDGER.md`](remediation/LEDGER.md):** Master issue matrix (`N1`-`N12`, `M1`-`M9`, `S1`-`S6`, `L1`-`L3`, `F1`, `P1-*`) with root causes, commit hashes, and verification commands.
- **[`remediation/THEORY_NOTES.md`](remediation/THEORY_NOTES.md):** Mathematical proofs for Proposition 1 (relative distance concentration under isotropic noise), Sarle's Bimodality Coefficient cutoff ($b_d \ge 5/9$), and Transfer-Cut Laplacian embeddings.
- **[`remediation/CLAIMS_AUDIT.md`](remediation/CLAIMS_AUDIT.md):** Line-by-line verification separating supported mathematical theorems from empirical observations.
- **[`remediation/ENV.md`](remediation/ENV.md):** Locked execution environments, hardware specifications, and random seed rosters (`seeds 0-29`).
- **[`remediation/ZENODO.md`](remediation/ZENODO.md):** Permanent DOI archival specification for `v2.1.0` (with historical `v2.0.0` records).

---

### 2.2 [`preregistration/`](preregistration/README.md): Research Integrity & Preregistration Archive
*Pre-experimental protocols and independent bibliographic validation:*
- **Preregistrations:** [`PREREG_v1.md`](preregistration/PREREG_v1.md), [`PREREG_B.md`](preregistration/PREREG_B.md), [`PREREG_C.md`](preregistration/PREREG_C.md), [`PREREG_F.md`](preregistration/PREREG_F.md) (frozen evaluation metrics and acceptance criteria prior to model fitting).
- **[`preregistration/REFS_AUDIT.csv`](preregistration/REFS_AUDIT.csv):** 100% automated bibliographic verification against the CrossRef REST API (zero phantom/unverifiable citations).
- **[`preregistration/LITERATURE_MATRIX.csv`](preregistration/LITERATURE_MATRIX.csv):** Feature-level taxonomy positioning ICC-v2 against 30+ baseline algorithms.
- **Submission Correspondence:** [`COVER_LETTER_DRAFT.md`](preregistration/COVER_LETTER_DRAFT.md) and [`RESPONSE_TO_REVIEWERS_OUTLINE.md`](preregistration/RESPONSE_TO_REVIEWERS_OUTLINE.md).

---

### 2.3 [`release/`](release/README.md): Software Release Governance & Quality Assurance
*Production release engineering for the `icc` and `cicc` Python packages:*
- **[`release/RELEASE_REPORT.md`](release/RELEASE_REPORT.md):** Formal release verification for `v2.1.0` (active release) and `v2.0.0` (historical baseline).
- **[`release/LICENSE_DECISION.md`](release/LICENSE_DECISION.md):** Legal and interoperability rationale for the permissive MIT License.
- **[`release/baseline/`](release/baseline/):** Frozen stdout regression baselines (`pytest_baseline.txt`, `mypy_baseline.txt`, `ruff_baseline.txt`).
