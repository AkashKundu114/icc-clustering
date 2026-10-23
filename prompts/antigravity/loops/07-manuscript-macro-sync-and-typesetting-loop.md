# Loop: Camera-Ready Manuscript & Macro Synchronization Loop

Use this loop to ensure that all LaTeX manuscript documents, tables, figures, numbers, and bibliography entries are camera-ready, synchronized with experimental results, and free of compiler warnings.

---

## Operating Budget & Setup
- **Maximum Iterations:** 3 iterations per run.
- **Assigned Subagent Personas:**
  - `Macro Synchronization Specialist (roo_coder)`: Generates and binds numbers macros to experimental JSON registries.
  - `LaTeX Typography Specialist (roo_debugger)`: Inspects compiler logs, overfull boxes, and table widths.
  - `Publication Auditor (roo_reviewer)`: Audits rendered PDF against publisher and journal guidelines.

---

## Iteration Protocol

### 1. Macro Generation & Single-Source Audit
- Execute the macro extraction script:
  ```bash
  python scripts/make_numbers.py
  ```
- Verify that every empirical number in the manuscript traces to `paper/numbers.tex`.
- Search for any hardcoded floating-point numbers in manuscript `.tex` files:
  ```bash
  grep -E '[0-9]+\.[0-9]{2,}' paper/main.tex
  ```
- Replace any detected hardcoded figures with programmatic macro references.

### 2. Bibliography Resolution & Citation Check
- Run BibTeX compilation:
  ```bash
  bibtex paper/main
  ```
- Check `paper/main.blg` for missing entries or malformed syntax.
- Confirm zero undefined citation warnings (`LaTeX Warning: Citation ... undefined`).

### 3. Typography & Overfull Box Remediation
- Run pdfLaTeX / Tectonic build and parse `paper/main.log`:
  - Locate all `Overfull \hbox` and `Overfull \vbox` occurrences.
  - Adjust table column widths (`\setlength{\tabcolsep}{...}`, `\resizebox`, or `p{width}`).
  - Wrap wide mathematical equations across multiple lines using `align` or `split`.

### 4. High-Resolution Figure Embedding Verification
- Synchronize all latest figures from experiments:
  ```bash
  python scripts/sync_figures.py
  ```
- Verify that all figures embedded in `paper/main.tex` exist in `paper/figures/` at native 300+ DPI.

### 5. Final PDF Compilation & Inspection
- Compile clean PDF:
  ```bash
  cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
  ```
- Confirm:
  - Zero fatal errors.
  - Zero `??` markers in text.
  - Page count and formatting comply strictly with target journal constraints.
