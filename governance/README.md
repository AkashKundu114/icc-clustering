# Research Governance, Provenance & Quality Assurance Dossiers

**Location:** `governance/`  
**Target Venue:** Springer Nature (*Data Mining and Knowledge Discovery* / DAMI)  
**Package:** `icc` (Inductive Consensus Clustering)

---

## 1. Executive Summary for Mentors & Reviewers

To maintain the highest level of research integrity, reproducibility, and software engineering standards, all audit trails, preregistrations, theoretical proofs, and release governance records are consolidated within this directory:

```
governance/
├── remediation/       # Scientific audit trail, issue ledger, theory proofs, and claim verifications
├── preregistration/   # Preregistration protocols (Passes A-F), CrossRef reference audits, literature matrix
└── release/           # Software release reports, MIT license analysis, and test baseline logs
```

---

## 2. Directory Map & Core Documents

### 2.1 [`remediation/`](remediation/README.md) — Scientific Remediation & Verification Dossier
*Systematic tracking and verification of 27 technical, numerical, and theoretical issues:*
- **[`remediation/LEDGER.md`](remediation/LEDGER.md):** Master issue matrix (`N1`–`N12`, `M1`–`M9`, `S1`–`S6`, `L1`–`L3`, `F1`, `P1-*`) with root causes, commit hashes, and verification commands.
- **[`remediation/THEORY_NOTES.md`](remediation/THEORY_NOTES.md):** Mathematical proofs for Proposition 1 (relative distance concentration under isotropic noise), Sarle's Bimodality Coefficient cutoff ($b_d \ge 5/9$), and Transfer-Cut Laplacian embeddings.
- **[`remediation/CLAIMS_AUDIT.md`](remediation/CLAIMS_AUDIT.md):** Line-by-line verification separating supported mathematical theorems from empirical observations.
- **[`remediation/ENV.md`](remediation/ENV.md):** Locked execution environments, hardware specifications, and random seed rosters (`seeds 0–29`).

---

### 2.2 [`preregistration/`](preregistration/README.md) — Research Integrity & Preregistration Archive
*Pre-experimental protocols and independent bibliographic validation:*
- **Preregistrations:** [`PREREG_v1.md`](preregistration/PREREG_v1.md), [`PREREG_B.md`](preregistration/PREREG_B.md), [`PREREG_C.md`](preregistration/PREREG_C.md), [`PREREG_F.md`](preregistration/PREREG_F.md) (frozen evaluation metrics and acceptance criteria prior to model fitting).
- **[`preregistration/REFS_AUDIT.csv`](preregistration/REFS_AUDIT.csv):** 100% automated bibliographic verification against the CrossRef REST API (zero phantom/unverifiable citations).
- **[`preregistration/LITERATURE_MATRIX.csv`](preregistration/LITERATURE_MATRIX.csv):** Feature-level taxonomy positioning ICC-v2 against 30+ baseline algorithms.
- **Submission Correspondence:** [`COVER_LETTER_DRAFT.md`](preregistration/COVER_LETTER_DRAFT.md) and [`RESPONSE_TO_REVIEWERS_OUTLINE.md`](preregistration/RESPONSE_TO_REVIEWERS_OUTLINE.md).

---

### 2.3 [`release/`](release/README.md) — Software Release Governance & Quality Assurance
*Production release engineering for the `icc` Python package:*
- **[`release/RELEASE_REPORT.md`](release/RELEASE_REPORT.md):** Formal release sign-off for `v2.0.0` / `v2.1.0`.
- **[`release/LICENSE_DECISION.md`](release/LICENSE_DECISION.md):** Legal and interoperability rationale for the permissive MIT License.
- **[`release/baseline/`](release/baseline/):** Frozen stdout regression baselines (`pytest_baseline.txt`, `mypy_baseline.txt`, `ruff_baseline.txt`).
