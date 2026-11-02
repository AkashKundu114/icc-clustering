# 00 Research Workspace Initialization and Baseline Report

**Repository Target:** `D:\icc-clustering`  
**Remote Target:** `https://github.com/AkashKundu114/icc-clustering.git`  
**Phase:** LOOP 0 ?" Research Workspace Initialization and Evidence Integrity Gate  
**Execution Timestamp:** 2026-11-01T23:45:00+05:30  
**Operating System:** Windows 11 / PowerShell  
**Python Runtime:** Python 3.14.0rc2  

---

## 1. Executive Summary

This report establishes the baseline configuration, version control state, repository layout, and directory responsibilities for the local-only research workspace initialized under **LOOP 0**.

The primary objective of this phase is to construct an isolated, reproducible, local-only research workspace (`paper/`) and establish a rigid evidence-integrity gate before any mathematical proofs, statistical audits, or experimental remediations are undertaken. In strict adherence to the mandate:
- No tracked source files in `src/` have been altered.
- No automated tests in `tests/` have been modified.
- No Git history, tags, branches, or remote references have been rewritten or pushed.
- The `paper/` directory is strictly excluded locally via `.git/info/exclude`.
- Canonical manuscript sources, statistical macro registries, bibliography files, style classes, figures, and tables have been preserved and indexed.
- The complete raw artifact inventory has been independently cross-verified against the physical filesystem.

---

## 2. Baseline Git State & Remote Tracking Status

A forensic audit of the Git repository at `D:\icc-clustering` verified the following baseline parameters:

| Parameter | Recorded Baseline Value | Verification Command | Integrity State |
|---|---|---|---|
| **Local Active Branch** | `main` | `git branch --show-current` | Verified |
| **Local Active HEAD** | `7ddbe8301b8d27c94f388c40acbc88b0dee82723` | `git rev-parse HEAD` | Verified |
| **Remote Origin URL** | `https://github.com/AkashKundu114/icc-clustering.git` | `git remote get-url origin` | Verified |
| **Remote Tracking Branch** | `origin/main` | `git rev-parse --abbrev-ref --symbolic-full-name @{u}` | Up-to-date with remote |
| **Working Tree Status** | Clean (0 modified, 0 untracked files) | `git status --porcelain` | Clean |
| **Last Commit Subject** | `Expand Python compatibility CI and docs` | `git log -1 --pretty=%s` | Verified |
| **Last Commit Date** | `Sun Nov 1 22:19:09 2026 +0530` | `git log -1 --pretty=%cd` | Verified |
| **Direct Parent Commit** | `83728a441f44c1ed56a35a5bdb07490ff559de81` | `git rev-parse HEAD~1` | Linear child |

---

## 3. Existing Ignored Directories & Exclusion Architecture

### 3.1 Tracked `.gitignore` Analysis
The tracked `.gitignore` file enforces repository hygiene across development and production environments. It contains explicit rules for:
1. **Local Agent Workspace:** `/audit/`, `/results/`
2. **Data Caches and Large Downloads:** `data/cache/`, `data/raw/`, `data/paul15/`, `*.h5`, `*.h5ad`
3. **Experiment Caches:** `results/experiments/*.json`, `experiments/**/data/*.npz`, `results/study_null_gating/confirmatory_raw/`, `results/stability/`
4. **Python Build/Environment:** `__pycache__/`, `build/`, `dist/`, `.venv/`, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`
5. **Manuscript, LaTeX, and Submission Assets:** `submission/`, `manuscript/`, `paper/`, `*.tex`, `*.pdf`, `*.bib`, `*.bst`, `*.cls`, `*.sty`, `*.aux`, `*.bbl`, `*.blg`, `*.out`
6. **Visual Artifacts:** `**/figures/*` (excluding `.gitkeep` and `README.md`)

### 3.2 Local-Only Git Exclusion (`.git/info/exclude`)
To ensure that the newly created local-only paper workspace remains strictly local to this working copy without modifying the tracked `.gitignore` file, `.git/info/exclude` was updated:

```text
# git ls-files --others --exclude-from=.git/info/exclude
# Private local coding-agent workspace
/audit/
/results/

# Local-only research paper workspace
/paper/
paper/
```

Verification via `git status` confirmed that neither `paper/` nor its 226 sub-assets appear in Git status or untracked file listings.

---

## 4. Current Manuscript Locations & Provenance

Prior to workspace initialization, a full-disk search for manuscript assets was conducted. Manuscript files were located across three distinct environments:

| Environment / Path | Description | Files Present | Canonical Status |
|---|---|---|---|
| `D:\icc-clustering\results\evidence_recovery\recovered\` | Recovered audit vault in working copy | `numbers.tex` (4,087 bytes) | Verified recovered copy |
| `D:\icc-clustering-private-archive\springer_manuscript\` | Clean Springer Nature package in private archive | `main.tex`, `numbers.tex`, `references.bib`, 16 figures, 34 tables | Production candidate |
| `D:\icc-clustering-private-archive\paper\` | Complete publication suite with class file | `main.tex`, `numbers.tex`, `references.bib`, `sn-jnl.cls`, 76 figures, 31 tables, `convert_to_springer.py` | **Canonical Reference Source** |
| `D:\icc-clustering-private-archive\full_branches\dami-revision\paper\` | Historical pre-sanitization branch snapshot | `main.tex` (138,466 bytes), `numbers.tex`, `references.bib` | Historical reference (unredacted) |

### Canonical Source Selection:
`D:\icc-clustering-private-archive\paper\` was identified as the **canonical manuscript source** because:
1. It contains the official Springer Nature class file `sn-jnl.cls` (55,857 bytes).
2. Its `main.tex` (123,788 bytes) represents the sanitized, submission-targeted state formatted for *Data Mining and Knowledge Discovery* (DAMI / DMKD).
3. It contains the complete set of 76 high-resolution (300 DPI) publication figures and 31 LaTeX tables in `gen/`.
4. Its `numbers.tex` bitwise matches the recovered copy in `results\evidence_recovery\recovered\numbers.tex` (SHA-256: `10265f3d68da1985938382a9601c258193cc35a24579aa505133d480bb9493f7`).

---

## 5. Existing LaTeX Configuration & Toolchain Requirements

### 5.1 Manuscript Document Configuration
- **Document Class:** `\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}` (v3.1, Dec 2024)
- **Bibliography Style:** `sn-mathphys-num.bst` (Vancouver / numerical citation order)
- **Macro Engine:** Direct input of `numbers.tex` via `\input{numbers.tex}`
- **Compilation Toolchain Requirements:** `pdflatex`, `bibtex`, multi-pass compilation (`pdflatex -> bibtex -> pdflatex -> pdflatex`)

### 5.2 Host System LaTeX Availability Check
A comprehensive search for LaTeX compilers was conducted across the Windows host environment:

| Executable | Search Command | System Status | Path |
|---|---|---|---|
| `pdflatex` | `where.exe pdflatex` | **NOT FOUND** | None |
| `latexmk` | `where.exe latexmk` | **NOT FOUND** | None |
| `xelatex` | `where.exe xelatex` | **NOT FOUND** | None |
| `lualatex` | `where.exe lualatex` | **NOT FOUND** | None |
| `bibtex` | `where.exe bibtex` | **NOT FOUND** | None |
| `tectonic` | `where.exe tectonic` | **NOT FOUND** | None |

**Policy Compliance:** As mandated by the protocol, no global software packages or TeX distributions were installed. An automated static AST validation engine was implemented in `paper/build/build_manuscript.py` to audit document dependencies, citations, labels, and figures in the absence of a native compiler.

---

## 6. Existing Raw Experimental Artifacts

A physical inventory of raw experimental data confirmed the presence of the following artifact groups:

### 6.1 Core Audit Artifacts (`results/post_refactor_verification/`)
- `auto_k/adversarial_autok_raw_results.csv` (104,264 bytes): 510-trial raw AutoK evaluation matrix across 17 data regimes.
- `auto_k/adversarial_autok_summary.json` (9,763 bytes): Scenario-level aggregation of AutoK collapse rates.
- `benchmark_logs/reproduction_benchmarks.csv` (14,849 bytes): 5-repeat timing and memory profiles across 10 random seeds.
- `benchmark_logs/aggregate_seed_statistics.csv` (1,646 bytes): Aggregated 10-seed performance metrics.
- `conformal/conformal_audit_results.json` (3,796 bytes): Monte Carlo calibration observations on Leukemia and SRBCT.
- `knockoff/knockoff_audit_results.json` (8,125 bytes): Empirical false discovery rate (FDR) observations under pure null data.
- `leakage/leakage_audit_results.json` (2,684 bytes): 5-fold cross-validation comparisons of pre-split vs post-split standardization.
- `packaging/clean_env_results.json` (4,185 bytes): Clean virtualenv test traces diagnosing wheel packaging errors.

### 6.2 Recovered Vault Artifacts (`results/evidence_recovery/recovered/`)
All 14 recovered evidence files are physically present in `results\evidence_recovery\recovered\`:
- All 8 core audit files listed above (bitwise identical copies).
- `exp2_real_high_d_factorial.csv` (43,385 bytes): Factorial ablation matrix across 6 high-dimensional benchmarks.
- `subsample_stability_summary.csv` (10,622 bytes): Stratified subsample stability microdata evaluating the $+0.485$ discordance gap.
- `real_data_stability_summary.csv` (16,630 bytes): Cohort-level stability and accuracy metrics across 13 datasets.
- `stats.json` (11,858 bytes): Non-parametric statistical evaluations (Friedman test, Nemenyi CD, bootstrap intervals).
- `results.json` (1,627,258 bytes): Master benchmark evaluation database across 13 datasets and 12 clustering algorithms.
- `numbers.tex` (4,087 bytes): LaTeX macro registry defining 84 publication statistics.

---

## 7. Existing Experiment & Reproduction Scripts

The repository contains experiment orchestration and analysis scripts across two directories:

### 7.1 Production Script Directory (`scripts/`)
- `scripts/run.py` (5,142 bytes): CLI entrypoint for running benchmark suites.
- `scripts/evaluate.py` (3,892 bytes): Statistical evaluation and metric aggregation.
- `scripts/prepare_data.py` (4,210 bytes): Dataset ingestion and normalization pipeline.
- `scripts/fetch_data.py` (3,415 bytes): Automated downloader for public benchmark arrays.
- `scripts/reproduce.py` (6,120 bytes): Top-level reproduction harness for published tables.

### 7.2 Post-Refactor Verification Suites (`results/post_refactor_verification/`)
- `auto_k/run_adversarial_autok_benchmarks.py` (11,643 bytes): Generates adversarial AutoK evaluation matrix.
- `benchmark_logs/reproduce_benchmarks.py` (8,807 bytes): Profiles runtime, peak memory, and ARI stability across seeds.
- `conformal/audit_conformal.py` (13,135 bytes): Evaluates inductive conformal coverage on Leukemia and SRBCT.
- `knockoff/audit_knockoff.py` (12,364 bytes): Evaluates Model-X knockoff exchangeability and empirical FDR under null features.
- `leakage/audit_leakage.py` (4,844 bytes): Measures test-set contamination from pre-split standardization.
- `packaging/test_clean_install.py` (2,586 bytes): Installs built wheels into isolated virtual environments.

---

## 8. Directory Separation Architecture

Strict boundaries have been established across the repository to enforce scientific integrity:

```text
D:\icc-clustering\
├── paper/      [LOCAL EMBARGO] Manuscript source, tables, figures, bibliography, build logs.
│               NEVER committed. NEVER pushed. Excluded via .git/info/exclude.
├── audit/      [AUDIT WORKSPACE] Independent audits, forensic reports, remediation plans, logs.
│               Excluded via .gitignore and .git/info/exclude.
├── results/    [EXPERIMENTAL VAULT] Raw experimental outputs, execution logs, benchmark databases.
│               Excluded via .gitignore and .git/info/exclude.
├── src/        [PRODUCTION SOURCE] Pure algorithmic implementation (ICC, consensus, feature gating).
│               Strictly tracked in Git. Zero modifications permitted during Loop 0.
└── tests/      [AUTOMATED TESTING] Unit, regression, and property test suites.
                Strictly tracked in Git. Zero modifications permitted during Loop 0.
```

### Governing Partitioning Rules:
1. **No Raw Data in Manuscript Workspace:** `paper/` contains only presentation assets (LaTeX tables, compiled figures, bibliography). No raw matrices (`.npz`, `.h5`, `.csv` microdata) may be placed inside `paper/`.
2. **No Manuscript Drafts in Source Directories:** No `.tex`, `.bib`, `.cls`, or `.pdf` files may reside in `src/`, `tests/`, or `scripts/`.
3. **No Unaudited Numbers:** Every macro in `numbers.tex` must be generated by an audited script from a verified raw artifact in `results/`.
