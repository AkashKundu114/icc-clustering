# Project Blockers and Decisions Register (BLOCKERS.md)

This file tracks active and resolved blocking conditions, external human decision gates, and co-author approval requirements under Rule R11.

---

## Active Blockers

1. **BLOCKER-COAUTHORS:**
   - *Description:* Written approval from all co-authors (Akash Kundu, Trinankur Guha, Rupankar Ghatak, Anubhab Naskar, Prof. Kalyan Kumar Das) is required prior to formal journal submission.
   - *Status:* PENDING_USER_SIGN_OFF
   - *Action:* Autonomous agent will prepare complete `submission/` package locally and await user submission.

2. **BLOCKER-DECLARATIONS:**
   - *Description:* Springer Nature declarations (Competing Interests, Ethics Approval, Consent to Participate, Authors' Contributions) are currently commented out with `% RESTORE BEFORE SUBMISSION...` per Springer sn-jnl template directives to maintain clean local drafts.
   - *Status:* PREPARED_FOR_RESTORATION
   - *Action:* Restore these commented-out blocks before uploading `.tex` to the Springer submission portal.

3. **BLOCKER-JOURNAL-CHOICE:**
   - *Description:* Final selection among target journal shortlist (Springer DAMI, IEEE TKDE, Information Fusion, Pattern Recognition, JMLR).
   - *Status:* RECOMMENDATION_PREPARED (Springer Nature DAMI recommended as primary).

---

## Resolved Blockers

- [x] **BLOCKER-NETWORK:** CrossRef and arXiv REST API connectivity tested and verified (HTTP 200).
- [x] **BLOCKER-REFS:** 100% of bibliography verified via CrossRef/arXiv APIs or primary manual URLs (`results/refs_report.csv`); 80.85% vintage (2024–2026).
- [x] **BLOCKER-MACROS:** Build-time macro verification tests passing cleanly (`tests/test_macro_consistency.py`, `tests/test_pdf_allowlist.py`).
- [x] **BLOCKER-DISK:** 80.8 GB disk space available on D: (exceeds 5 GB minimum threshold).
