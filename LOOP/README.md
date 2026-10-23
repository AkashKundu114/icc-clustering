# Research Integrity & Preregistration Archive

**Location:** `LOOP/`  
**Purpose:** Comprehensive archive of preregistered experiment protocols, iterative manuscript development cycles (Passes A through F), bibliographic CrossRef audits, and submission governance.  
**Target Venue:** Springer Nature (*Data Mining and Knowledge Discovery* / DAMI)

---

## 1. Executive Summary for Mentors & Reviewers

The files in this directory document the **iterative refinement and empirical preregistration** of the research manuscript and benchmark suite. To adhere strictly to Springer Nature research integrity standards, every major experimental update was governed by preregistration to prevent post-hoc hypothesis cherry-picking ($p$-hacking) and to enforce automated, single-source reproducibility.

---

## 2. Directory Contents & Navigation

### 2.1 Preregistration Protocols
Preregistering experiments before running full computational batches ensures that evaluation metrics, baseline solvers, and acceptance thresholds are frozen in advance:

| Protocol | Scope & Key Objectives |
| :--- | :--- |
| **[`PREREG_v1.md`](PREREG_v1.md)** | **Foundational Protocol:** Initial falsification of the consensus averaging hypothesis in high-dimensional noise regimes ($D \gg N$). |
| **[`PREREG_B.md`](PREREG_B.md)** | **Pass B Preregistration:** Multi-domain benchmark matrix expansion across 13 datasets $\times$ 11 algorithms (2,750 model fits). |
| **[`PREREG_C.md`](PREREG_C.md)** | **Pass C Preregistration:** 2x2 ablation design (Feature Gating $\times$ Anchor Consensus) and $N=10^6$ computational scaling protocol. |
| **[`PREREG_F.md`](PREREG_F.md)** | **Pass F Preregistration (Final Gate):** Strict single-source macro alignment (`numbers.tex`), automated PDF decimal allowlist scanning, and mirror synchronization. |

---

### 2.2 Bibliographic & Reference Audits
To guarantee zero citation fabrication or inaccurate bibliographic metadata:

| Document | Purpose & Outcomes |
| :--- | :--- |
| **[`REFS_AUDIT.md`](REFS_AUDIT.md)** | **Bibliographic Audit Summary:** Automated audit protocol querying the CrossRef REST API for all references in `springer_manuscript/references.bib`. |
| **[`REFS_AUDIT.csv`](REFS_AUDIT.csv)** | **CrossRef Verification Table:** Complete tabular database matching BibTeX citation keys to verified DOIs, official titles, publication years, and author rosters (100% verified; zero phantom citations). |
| **[`LITERATURE_MATRIX.csv`](LITERATURE_MATRIX.csv)** | **Taxonomy & Novelty Matrix:** Comprehensive feature-level comparison of ICC-v2 against 30+ related clustering methods (ensemble, subspace, spectral, deep, and anchor graph formulations). |
| **[`NOVELTY_VERDICTS.md`](NOVELTY_VERDICTS.md)** | **Novelty Positioning:** Analytical differentiation of ICC-v2's inductive centroid projection vs. Nyström sampling and landmark spectral clustering. |

---

### 2.3 Author & Submission Governance
Formal correspondence and compliance checklists for journal submission:

| Document | Description |
| :--- | :--- |
| **[`COVER_LETTER_DRAFT.md`](COVER_LETTER_DRAFT.md)** | Formal submission cover letter addressed to the Editors-in-Chief of Springer Nature *Data Mining and Knowledge Discovery* (DAMI). |
| **[`RESPONSE_TO_REVIEWERS_OUTLINE.md`](RESPONSE_TO_REVIEWERS_OUTLINE.md)** | Structured rebuttal framework and point-by-point response template addressing common reviewer queries on high-D consensus clustering. |
| **[`AUTHOR_CHECKLIST.md`](AUTHOR_CHECKLIST.md)** | Springer Nature author compliance checklist covering data availability, ethics, funding, and reproduction assets. |
| **[`AUTHOR_CONFIRMATION.md`](AUTHOR_CONFIRMATION.md)** | Author sign-off protocol affirming manuscript verification and code reproducibility. |
| **[`DISCLOSURE_OPTIONS.md`](DISCLOSURE_OPTIONS.md)** | Detailed analysis and rationale for the assistive AI disclosure statement compliant with Springer Nature generative AI editorial policies. |
| **[`DECISIONS.md`](DECISIONS.md)** | Architectural and methodological decision record detailing the evolution of ICC from v1.0 to v2.1. |
