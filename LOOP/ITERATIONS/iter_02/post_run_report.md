# Post-Simulation Autonomous Verification Report: Iteration 02
**Date:** 2026-10-19 16:34:13  
**Total Replicates Analyzed:** 18000 across 60 experimental cells  
**Hardware:** NVIDIA GeForce RTX 5060 Laptop GPU (CUDA 13.4, PyTorch cu134 nightly, Blackwell sm_120)  

---

## 1. Confirmatory Hypothesis Testing (Study 3')
- **Hypothesis H1 (Error Calibration on Validated Families F1, F2, F5):**
  - **Criterion:** FDR controlled at $q = 0.10$ with 95% bootstrap confidence interval upper bound $\le 0.10$.
  - **Result:** **FAIL** (32 of 48 cells passed, 66.7% pass rate).
  - Scope limit on bounded families (F3 Uniform, F4 Beta) documented per Pivot Rule A7 (boundary smoothing bias).

- **Hypothesis H3 (Statistical Power in Separable Regimes):**
  - **Criterion:** Mean power $\ge 0.80$ at $\Delta \ge 3.0, N \ge 250$.
  - **Result:** **PASS** (11 of 12 cells passed, 91.7% pass rate).

---

## 2. Updated Artifacts
- Raw results: `results/study_null_gating/confirmatory_raw/primary_grid_results.json`
- Evaluated summary: `results/study_null_gating/confirmatory_summary.json`
- Numeric macros: `springer_manuscript/numbers.tex`
- Typeset manuscript: `springer_manuscript/main.pdf` (compiled cleanly via Tectonic)
