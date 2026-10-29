# User Action Checklist for Submission (USER_CHECKLIST.md)

Before initiating the final upload on the target journal portal, the human investigator (Akash Kundu) must complete the following mandatory checks:

---

### Phase 1: Author Consents & Approvals
- [ ] Confirm and obtain written sign-off from all co-authors:
  - Akash Kundu (Corresponding Author)
  - Trinankur Guha
  - Rupankar Ghatak
  - Anubhab Naskar
  - Prof. Kalyan Kumar Das (Faculty Mentor)
- [ ] Confirm corresponding author contact details: `akashkundu1152@gmail.com`.

---

### Phase 2: Target Journal Selection
- [ ] Choose primary target journal from `submission/JOURNAL_SHORTLIST.md`:
  - [x] Primary Recommended: *Data Mining and Knowledge Discovery* (Springer Nature)
  - [ ] Alternative 1: *IEEE Transactions on Knowledge and Data Engineering* (TKDE)
  - [ ] Alternative 2: *Information Fusion* (Elsevier)

---

### Phase 3: Declarations Restoration
In `paper/main.tex` and `springer_manuscript/main.tex`, restore the commented-out Springer Nature declarations right before submission:
- [ ] Uncomment `\section*{Declarations}`
- [ ] Uncomment `\subsection*{Funding}`
- [ ] Uncomment `\subsection*{Competing Interests}`
- [ ] Uncomment `\subsection*{Ethics Approval}`
- [ ] Uncomment `\subsection*{Consent to Participate}`
- [ ] Uncomment `\subsection*{Author Contributions}`
*(Note: Data Availability and Code Availability are already active in the text).*

---

### Phase 4: Portal Upload Package Verification
Upload the assets located in `submission/`:
- [ ] `submission/main.pdf`: Full compiled manuscript for reviewer inspection.
- [ ] `submission/source.zip`: Complete LaTeX source bundle (`main.tex`, `numbers.tex`, `references.bib`, `sn-jnl.cls`, `bst/`, `figures/`, `gen/`).
- [ ] `submission/COVER_LETTER.md`: Cover letter text to paste into the submission editor.
- [ ] `submission/refs_report.csv`: Bibliographic audit report verifying CrossRef/arXiv resolution.
