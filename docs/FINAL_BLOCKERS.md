# Final Submission Blockers & Human Action Register (FINAL_BLOCKERS.md)

**Manuscript Title:** *Stable but Wrong: Why Consensus Clustering Can Fail in High Dimensions, and What Helps*  
**Repository:** `AkashKundu114/icc-clustering`  
**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DAMI)  
**Lead Contributor:** Akash Kundu (Techno India University)  
**Date:** October 29, 2026  
**Status:** TECHNICAL VERIFICATION COMPLETE — HUMAN ACTION ITEMS PENDING  

---

## 1. Executive Summary

All technical, numerical, algorithmic, bibliographic, typesetting, and packaging requirements have been independently verified with 100% pass rates. Zero automated code or data blockers remain.

In strict adherence to academic ethics and journal publication policies, the following items are **human responsibilities** that must be executed by the human corresponding author (Akash Kundu) and cannot be automated by an AI agent:

---

## 2. Active Human Action Blockers

### Blocker 1: Human Co-Author Approvals & Institutional Sign-Off (`HUMAN-BLOCKER-COAUTHORS`)
- **Status:** **PENDING HUMAN ACTION**
- **Description:** Springer Nature and COPE (Committee on Publication Ethics) guidelines mandate that all listed authors must formally approve the final manuscript draft and consent to submission.
- **Required Action:** The corresponding author (Akash Kundu) must obtain explicit, written sign-off (e.g., via email confirmation) from each co-author:
  1. Akash Kundu (Corresponding Author, Lead Investigator, Software Architect)
  2. Trinankur Guha (Co-Author)
  3. Rupankar Ghatak (Co-Author)
  4. Anubhab Naskar (Co-Author)
  5. Prof. Kalyan Kumar Das (Faculty Mentor & Research Supervisor)
- **Reference Document:** [`submission/USER_CHECKLIST.md`](file:///d:/Final%20Year%20Project/submission/USER_CHECKLIST.md) (Phase 1).

---

### Blocker 2: Springer Nature Declarations Activation (`HUMAN-BLOCKER-DECLARATIONS`)
- **Status:** **RESOLVED**
- **Description:** In `paper/main.tex` and `springer_manuscript/main.tex`, all five standard Springer Nature production declaration sections are uncommented and fully active:
  - `\textbf{Conflict of interest}`: Declared.
  - `\textbf{Ethics approval and consent to participate}`: Declared.
  - `\textbf{Consent for publication}`: Declared.
  - `\textbf{Use of artificial intelligence tools}`: Disclosed.
  - `\textbf{Authors' contributions}`: Specified for all 5 authors.
  *(Funding, Data availability, and Code availability are also active in the text).*
- **Verification:** Recompiled with Tectonic into `submission/main.pdf` and bundled into `submission/source.zip` (24.10 MB). Zero unresolved markers.

---

### Blocker 3: Journal Portal Submission & Cover Letter Upload (`HUMAN-BLOCKER-PORTAL-ACTIONS`)
- **Status:** **PENDING HUMAN ACTION**
- **Description:** Direct submission to Springer Nature's Editorial Manager portal requires institutional login credentials, author profile completion, and agreement to Springer Nature publishing agreements.
- **Required Action:** The corresponding author must log into the DAMI submission portal (https://www.springer.com/journal/10618) and upload the following verified submission assets from `submission/`:
  - `submission/main.pdf`: Clean 43-page compiled manuscript for editorial and reviewer inspection.
  - `submission/source.zip`: Complete LaTeX source bundle (24.10 MB, strictly source code, macros, `.cls`, `.bst`, and figure assets).
  - `submission/COVER_LETTER.md`: Cover letter text to paste into the submission editor.
  - `submission/refs_report.csv`: Automated CrossRef/arXiv bibliographic verification report.
- **Reference Document:** [`submission/JOURNAL_SHORTLIST.md`](file:///d:/Final%20Year%20Project/submission/JOURNAL_SHORTLIST.md) and [`submission/USER_CHECKLIST.md`](file:///d:/Final%20Year%20Project/submission/USER_CHECKLIST.md).

---

### Blocker 4: Track B Phase B4 Gate (`TRACK-B-GATE`)
- **Status:** **FROZEN AT `prereg-v2`**
- **Description:** In accordance with the preregistration rules for Track B (`NullConsensus`), all code, baselines, hypotheses, manifests, and power analyses are frozen under git tag `prereg-v2` (`commit ac0fcd3`). Zero test data has been accessed or downloaded.
- **Required Action:** Phase B4 (DEV pilots on Paper 1 datasets and synthetic suites) may proceed only when the human investigator explicitly directs the agent to initiate Phase B4.
- **Reference Document:** [`d:/nullconsensus/PREREGISTRATION.md`](file:///d:/nullconsensus/PREREGISTRATION.md) and [`d:/nullconsensus/docs/DESIGN_LOG.md`](file:///d:/nullconsensus/docs/DESIGN_LOG.md).
