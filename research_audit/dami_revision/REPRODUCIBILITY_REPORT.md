# Phase 0: Reproducibility and Verification Audit Report

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Audit Persona:** Agent A7 — Independent Reproducibility Engineer  
**Date:** November 1, 2026  
**Revision Branch:** `research/dami-revision`  

---

## 1. Executive Summary

This reproducibility audit evaluates the end-to-end execution, test coverage, code quality, and numerical consistency of `icc-clustering` on the dedicated revision branch `research/dami-revision`.

### Verification Scorecard:
- **Test Suite Execution:** **PASSED** (Exit Code: 0, 100% of non-slow tests passing).
- **Static Analysis & Linting:** **PASSED** (Exit Code: 0, `ruff check` cleanly passed on `src/` and `tests/`).
- **Smoke Scope Reproduction:** **PASSED** (Exit Code: 0, 1.77 seconds).
- **Mathematical & Numerical Verifier:** **PASSED** (Exit Code: 0, all 19 numerical macros and propositions verified).
- **PDF Consistency:** **PASSED** (Zero unresolved `??` or missing citation keys in `paper/main.pdf`).

---

## 2. Test Execution & Coverage Audit

### Command Executed:
```powershell
python -m pytest tests/ -k "not slow" -q
```
- **Exit Status:** `0` (Success)
- **Total Tests Collected & Passed:** 126 test cases across 20 test files.
- **Failures / Errors:** `0`
- **Execution Time:** ~35.2 seconds

### Code Coverage Breakdown:
| Package / Module | Total Statements | Missed Statements | Coverage % |
| :--- | :--- | :--- | :--- |
| `src/cicc/` (Conformal Inductive Suite) | 324 | 33 | 90% |
| `src/icc/aspp.py` (ASPP Profiling) | 216 | 15 | 93% |
| `src/icc/consensus_v2.py` (GAC Core) | 275 | 61 | 78% |
| `src/icc/metrics.py` (Validation Metrics) | 187 | 22 | 88% |
| `src/icc/baselines/classical.py` | 52 | 4 | 92% |
| `src/icc/baselines/consensus.py` | 113 | 4 | 96% |
| `src/icc/baselines/sparse_kmeans.py` | 77 | 6 | 92% |
| `src/icc/baselines/anchor.py` | 153 | 36 | 76% |
| `src/icc/datasets/registry.py` | 100 | 13 | 87% |
| **Entire Repository Aggregate** | **2,954** | **871** | **71%** |

---

## 3. Scope Reproduction Smoke Checks

### Command Executed:
```powershell
python scripts/reproduce.py --scope smoke
```
- **Exit Status:** `0` (Success in 1.77 seconds)
- **Output Validation:**
  - `[1/3] Synthetic:` $N=100, D=20$, recovered clusters = 3.
  - `[2/3] Leukemia (Seed 0):` $N=72, D=7{,}129$, $\text{ARI} = 0.7376$.
  - `[3/3] SRBCT (Seed 0):` $N=83, D=2{,}308$, $\text{ARI} = 0.4719$.

---

## 4. Multi-Point Numerical & Theoretical Verifier

### Command Executed:
```powershell
python scripts/reproduce.py --scope verify
```
- **Exit Status:** `0` (Success)
- **Verifications Confirmed:**
  1. **19-Point Numerical Claim Verifier (`scripts/check_numbers.py`):**  
     Matches all generated values in `paper/numbers.tex`:
     - Friedman $p$-value: $0.40$
     - Nemenyi CD: $4.62$
     - ICC-v2 Overall Rank: $5.62$
     - DEC Overall Rank: $5.23$
     - High-D ICC-v2 Rank: $2.17$
     - Grand Mean ARI: $0.152$
     - Omnibus Median ARI: $0.055$
     - Mean Excluding Leukemia/SRBCT: $0.076$
     - Graph Memory Reduction: $99.6\%$
     - Peak RAM Reduction: $97.4\%$
     - Leukemia ARI: $0.600 \pm 0.367$
     - SRBCT ARI: $0.546 \pm 0.102$
  2. **Proposition 1 Analytical Root Verifier (`scripts/verify_prop1.py`):**  
     Confirmed exact critical separation bound:
     $$\frac{\Delta}{\sigma_0} \ge 1.853778 \approx 1.854$$
  3. **Proposition 2 Contingency Identity Verifier (`scripts/verify_determinacy_identity.py`):**  
     Tested across 9 parameter regimes ($N=10\text{--}200, M=1\text{--}50, K=2\text{--}15$); maximum algebraic discrepancy $< 7.11 \times 10^{-15}$ ($< 10^{-12}$ tolerance).
  4. **Sarle's Bimodality Coefficient Thresholds (`scripts/verify_bc.py`):**  
     Verified uniform threshold $BC = 5/9 \approx 0.5556$, exponential $BC = 0.5556$, lognormal $BC = 0.3445$, beta $BC = 0.5624$.

---

## 5. Artifact Checksum Ledger

| File Path | SHA-256 Digest | Verification Role |
| :--- | :--- | :--- |
| `results/results.json` | `0e5d2c10343ba077ff109e5f6554ecc191d89a590dfaf28bec2ef3e950e3ba27` | Frozen Phase 1 results store |
| `results/MANIFEST.md` | `951238021aa74d611a6e95dbaa8b67fb4d97a9d92dc65dc700d77534fcdbdaf2` | Frozen result manifest |
| `results/stats.json` | `83858600000b0d02fbad9742c333d634621f2fc1c64fdcd848c689ea952c4761` | Single source of truth for LaTeX macros |
| `paper/main.tex` | Checked in branch `research/dami-revision` | Submission manuscript source |
| `paper/numbers.tex` | Generated via `scripts/make_stats.py` | Synchronized quantitative macros |
