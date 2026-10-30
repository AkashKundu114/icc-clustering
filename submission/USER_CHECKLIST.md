# User Action Checklist for Submission (USER_CHECKLIST.md)

Before initiating the final upload on the target portal or platform, the human investigator (Akash Kundu) must complete the following mandatory checks:

---

### Phase 1: Author Consents & Approvals
- [ ] Confirm and obtain written sign-off from all co-authors:
  - Prof. Kalyan Kumar Das (Corresponding Author & Research Supervisor)
  - Akash Kundu (Contributing Author & Lead Developer)
  - Prof. Anirban Mukhopadhyay (Contributing Author)
- [ ] Confirm corresponding author contact details: `kalyan.biltu@gmail.com`.
- [ ] Confirm code/data/materials request contact details: kashkundu1152@gmail.com.
- [x] Author ORCID iDs verified:
  - Prof. Kalyan Kumar Das: `0009-0004-8333-8900`
  - Akash Kundu: `0009-0003-8246-7316`
  - Prof. Anirban Mukhopadhyay: `0000-0001-8128-3521`

---

### Phase 2: Target Venue Selection
- [ ] Choose primary target journal from `submission/JOURNAL_SHORTLIST.md`:
  - [x] Primary Recommended: *Data Mining and Knowledge Discovery* (DAMI, Springer Nature)
  - [ ] Alternative 1: *IEEE Transactions on Knowledge and Data Engineering* (TKDE)
  - [ ] Alternative 2: *Information Fusion* (Elsevier)

---

### Phase 3: Declarations Verification
In `paper/main.tex` and all submission packages, all required declarations are active, verified, and compliant:
- [x] `Funding`: Declared.
- [x] `Conflict of interest`: Declared.
- [x] `Ethics approval and consent to participate`: Declared.
- [x] `Consent for publication`: Declared.
- [x] `Use of artificial intelligence tools`: Disclosed generically (no commercial model names).
- [x] `Authors' contributions`: Specified for all 3 authors.
- [x] `Data availability` and `Code availability`: Active with release tag `v2.2.0`.

---

### Phase 4: Platform-Specific Package Selection & Upload

Choose the appropriate package from `submission/` based on your destination platform:

#### 1. Overleaf Collaboration / Inspection
- **File**: `submission/overleaf_package.zip` (6.68 MB)
- **Instructions**:
  1. In Overleaf, click **New Project** $\to$ **Upload Project**.
  2. Select `overleaf_package.zip`.
  3. Overleaf auto-detects `main.tex` as the root document.
  4. Ensure Compiler is set to **pdfLaTeX** and TeX Live is **2024** or **2025**.
  5. Click **Recompile** — compiles cleanly with zero configuration.

#### 2. Springer Nature DAMI Official Submission (SNAPP / Editorial Manager)
- **File**: `submission/springer_nature_package.zip` (6.69 MB)
- **Accompanying Files**:
  - `submission/main.pdf`: Full compiled manuscript (46 pages) for reviewer reference.
  - `submission/COVER_LETTER.md`: Cover letter addressed to the Editor-in-Chief.
  - `submission/refs_report.csv`: 100% verified bibliographic resolution audit.
- **Instructions**:
  1. Log into Springer Nature SNAPP / Editorial Manager for *Data Mining and Knowledge Discovery*.
  2. Upload `springer_nature_package.zip` under Manuscript Source Files.
  3. Upload `submission/main.pdf` under Accompanying / Reviewer PDF.
  4. Copy the text from `submission/COVER_LETTER.md` into the submission cover letter field.

#### 3. arXiv Preprint Submission
- **Files**: `submission/arxiv_package.tar.gz` (6.41 MB) or `submission/arxiv_package.zip` (6.58 MB)
- **Instructions**:
  1. Log into [arXiv.org](https://arxiv.org/submit).
  2. Start new submission under `stat.ML` (primary) and `cs.LG` (secondary).
  3. In the Files step, upload `arxiv_package.tar.gz` (or `arxiv_package.zip`).
  4. arXiv auto-detects `main.tex` via `00README.XXX` and uses the pre-compiled `main.bbl` directly, bypassing BibTeX version mismatches.
  5. Verify arXiv auto-compiler output and proceed to review.
