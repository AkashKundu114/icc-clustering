# 07 — Verification Log & Independent Command Audit

**Auditor:** Reproducibility & Data Engineer  
**Date:** October 13, 2026  
**Environment:** Python 3.14.6, Windows 11, PowerShell, Tectonic 0.17.0  

---

## 1. Executed Verification Commands & Outputs

### Test Suite Execution
- **Command:** `python -m pytest tests/ -v`
- **Output:**
  ```
  78 passed, 14 warnings in 62.96s (0:01:02)
  Coverage: 74% across 2,014 statements
  ```
- **Status:** **PASSED**

### Asset Consistency Audit
- **Command:** `python tools/check_consistency.py`
- **Output:**
  ```
  [*] Running ICC Consistency & Traceability Audit...
  [+] Verified 22 macros against raw results. Errors: 0
  [+] Pre-registered datasets in registry: 21
  [+] SUCCESS: All consistency and traceability gates PASSED.
  ```
- **Status:** **PASSED**

### Springer Manuscript Compilation
- **Command:** `manuscript/scripts/bin/tectonic.exe -Z search-path=springer_manuscript/bst springer_manuscript/main.tex`
- **Output:**
  ```
  Writing `springer_manuscript\main.pdf` (7.50 MiB)
  BibTeX author-year citations resolved cleanly via sn-mathphys-ay.bst
  ```
- **Status:** **PASSED**

### Overleaf Zip Packaging
- **Command:** `python -c "import zipfile; ..."`
- **Output:**
  ```
  Successfully regenerated springer_overleaf.zip (21.65 MB)
  Contains clean editable source, bst styles, cls, bib, and figures.
  Excludes compiled PDFs and temporary build artifacts.
  ```
- **Status:** **PASSED**
