# Scripts Directory Catalog

**Repository:** Inductive Core Consensus Clustering (ICC-v2)  
**Paper Title:** When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination  
**Target Venue:** Springer Nature (*Data Mining and Knowledge Discovery* / DAMI)  
**Release Version:** v2.1.0  

This directory contains verified, production-grade scripts for peer reviewers, reproducibility auditors, and contributors. All legacy, redundant, or one-off patch scripts have been removed to ensure a clean, audit-ready codebase.

---

## Retained Scripts Overview

The 15 retained scripts are organized into five functional categories:

1. **Reproduction and Data Ingestion**
   - `reproduce.py`: Central reproduction CLI for smoke, standard, and full reproduction runs.
   - `fetch_data.py`: Downloads, caches, and verifies all 13 benchmark datasets.
   - `sync_figures.py`: Synchronizes all generated figure artifacts across manuscript directories.

2. **Manuscript Macro and Claims Governance**
   - `make_numbers.py`: Top-level wrapper ensuring single-source-of-truth macro compilation.
   - `make_numbers_passF.py`: Programmatic LaTeX macro generator compiling `numbers.tex` from frozen Pass F stores.
   - `claims_check.py`: Automated audit tool verifying manuscript claims against `results/results.json`.

3. **Theoretical and Methodological Verification**
   - `verify_prop1.py`: Numerical quadrature and root finding validating Proposition 1 separation boundary ($\Delta / \sigma_0 \ge 1.854$).
   - `verify_bc_simulation.py`: Monte Carlo simulation auditing Sarle's Bimodality Coefficient finite-sample power and unimodal bounds.
   - `compute_inductive_bootstrap.py`: Dataset-level clustered bootstrap computing 95% confidence intervals for Table 2.
   - `run_refs_audit.py`: Live CrossRef API auditor verifying metadata for all BibTeX entries in `references.bib`.

4. **Empirical Benchmarks and Scaling Experiments**
   - `run_fair_baselines.py`: Evaluates feature selection baselines (Variance Filter, Truncated SVD, Laplacian Score, Sparse K-Means) against ICC-v2.
   - `run_high_d_ablation_2x2.py`: Executes the $2 \times 2$ factorial ablation cross across 6 high-dimensional genomics datasets over 10 random seeds.
   - `run_inductive_direct.py`: Evaluates out-of-sample inductive cluster assignment across 9 datasets and 10 stratified splits.
   - `run_exp5_controlled_scaling.py`: Benchmarks scaling performance across sample sizes $N \in \{10^4, 10^5, 10^6\}$, estimating the empirical scaling exponent $\beta$.

5. **Visualization**
   - `plot_conceptual_framework.py`: Generates the four-panel motivational conceptual illustration (Figure 0) at 300 DPI.

---

## Detailed Script Catalog

### 1. `reproduce.py`
- **Purpose:** Primary reproduction command-line interface for reviewers. Runs smoke verification on synthetic and real benchmark datasets with fixed seeds to guarantee bitwise reproducibility.
- **Execution:**
  ```powershell
  python scripts/reproduce.py --scope smoke
  ```
- **Expected Output:**
  ```text
  ============================================================
  ICC-v2 Reproduction: Smoke Scope (Synthetic + Real Benchmarks)
  ============================================================
  [1/3] Synthetic: N=100, D=20, clusters=3, sum=108
  [2/3] Leukemia (Seed 0): N=72, D=7129, ARI=0.7376
  [3/3] SRBCT (Seed 0):    N=83, D=2308, ARI=0.4719
  ------------------------------------------------------------
  Smoke reproduction passed in ~2.2 seconds.
  ============================================================
  ```

---

### 2. `fetch_data.py`
- **Purpose:** Discovers, fetches, unpacks, and validates the dimensional integrity ($N, D, K$) of all 13 benchmark datasets used in the study.
- **Execution:**
  ```powershell
  python scripts/fetch_data.py
  ```
- **Expected Output:**
  Iterates over all 13 benchmark datasets (sonar, madelon, colon, srbct, cns, leukemia, prostate, ovarian, newsgroups20, isolet, indian_pines, yale_b, zheng68k), confirming `[OK] Loaded: shape=(N, D), labels=K` and concluding with `Dataset verification complete: 13/13 ready.`

---

### 3. `sync_figures.py`
- **Purpose:** Recursively scans `experiments/` and `figures/` for generated high-resolution figures (`*.png`) and synchronizes them across all manuscript target directories (`paper/figures/`, `springer_manuscript/figures/`, `manuscript/figures/`).
- **Execution:**
  ```powershell
  python scripts/sync_figures.py
  ```
- **Expected Output:**
  ```text
  Total figures synced across manuscript directories: 60
  ```

---

### 4. `make_numbers.py`
- **Purpose:** Forwarding wrapper script that calls `make_numbers_passF.py`. Guarantees zero hand-edited numerical values in LaTeX manuscript files by generating all quantitative macros programmatically.
- **Execution:**
  ```powershell
  python scripts/make_numbers.py
  ```
- **Expected Output:**
  Compiles and writes identical copies of `numbers.tex` to `springer_manuscript/numbers.tex`, `paper/numbers.tex`, and `manuscript/numbers.tex`.

---

### 5. `make_numbers_passF.py`
- **Purpose:** Core numerical macro compilation engine. Ingests frozen Pass F result stores (`results/passF/benchmark_matrix_summary_passF.csv`, `friedman_nemenyi_passF.json`, `ablation_stats_passF.json`, `fair_baselines_summary_passF.json`) and formats 49 distinct LaTeX macros for the manuscript.
- **Execution:**
  ```powershell
  python scripts/make_numbers_passF.py
  ```
- **Expected Output:**
  ```text
  Saved springer_manuscript/numbers.tex
  Saved paper/numbers.tex
  Saved manuscript/numbers.tex
  ```

---

### 6. `claims_check.py`
- **Purpose:** Research integrity auditor that systematically checks each empirical claim listed in `governance/remediation/CLAIMS.md` against `results/results.json` and records a verified scoreboard.
- **Execution:**
  ```powershell
  python scripts/claims_check.py
  ```
- **Expected Output:**
  Summary scoreboard reporting matching and documented negative controls:
  ```text
  Total claims evaluated: 201
  MATCH: 188
  MISMATCH: 13
  ```

---

### 7. `verify_prop1.py`
- **Purpose:** Rigorous mathematical verification of Proposition 1. Solves the fourth-moment kurtosis equation $b(\theta) = 5/9$ using Brent's method and numerical quadrature across Gaussian and Student-$t$ noise regimes ($\nu \in [5, 100]$).
- **Execution:**
  ```powershell
  python scripts/verify_prop1.py
  ```
- **Expected Output:**
  Confirms the exact analytic root $\Delta / \sigma_0 = \sqrt{(3 + \sqrt{15})/2} \approx 1.853778$ and prints quadrature convergence:
  ```text
  Proposition 1 Exact Separation Bound (Gaussian): 1.853778
  Proposition 1 Numerical Root:                  1.853778
  nu =   5.0 | delta = 2.8122 | sigma0 = 1.2910 | Delta/sigma0 = 2.1783
  ...
  nu = 100.0 | delta = 1.8781 | sigma0 = 1.0102 | Delta/sigma0 = 1.8592
  VERIFICATION_SUCCESSFUL: Proposition 1 separation bound Delta/sigma0 >= 1.854 confirmed.
  ```

---

### 8. `verify_bc_simulation.py`
- **Purpose:** Monte Carlo simulation auditing Sarle's Bimodality Coefficient (BC) finite-sample detection power $P(\text{BC} \ge 5/9)$ across sample sizes $N \in \{60, 100, 250, 1000\}$ and verifying maximum population BC across skew-normal distributions.
- **Execution:**
  ```powershell
  python scripts/verify_bc_simulation.py
  ```
- **Expected Output:**
  Prints finite-sample power table (e.g., $P=0.49$ at $N=60$ scaling to $P=0.97$ at $N=1{,}000$ for informative features) and confirms maximum skew-normal population $\text{BC} = 0.5135 < 5/9$.

---

### 9. `compute_inductive_bootstrap.py`
- **Purpose:** Computes Table 2 paired differences across held-out splits and executes a dataset-level clustered bootstrap ($B=2{,}000$) to derive non-parametric 95% confidence intervals for out-of-sample inductive projection.
- **Execution:**
  ```powershell
  python scripts/compute_inductive_bootstrap.py
  ```
- **Expected Output:**
  ```text
  ================================================================================
  DATASET-LEVEL BOOTSTRAP 95% CONFIDENCE INTERVALS (B=2,000)
  ================================================================================
  Centroid vs Ambient K-Means     : Mean Diff = +0.0458, 95% CI = [-0.0290, +0.1292]
  Centroid vs Nystrom Subspace    : Mean Diff = -0.0234, 95% CI = [-0.0809, +0.0329]
  Centroid vs Random Forest       : Mean Diff = -0.0061, 95% CI = [-0.0527, +0.0455]
  [OK] Saved results to results/passF/inductive_bootstrap_stats.json
  ```

---

### 10. `run_refs_audit.py`
- **Purpose:** Live reference metadata auditor. Queries the CrossRef REST API for all entries in `springer_manuscript/references.bib`, cross-checks volume, issue, and page numbers, and writes the audit report to `governance/preregistration/REFS_AUDIT.csv`.
- **Execution:**
  ```powershell
  python scripts/run_refs_audit.py
  ```
- **Expected Output:**
  Iterates through all 32 references and logs verification status, outputting `Wrote governance/preregistration/REFS_AUDIT.csv with complete metadata verification.`

---

### 11. `run_fair_baselines.py`
- **Purpose:** Benchmarks high-dimensional feature selection baselines against ICC-v2 across 13 benchmark datasets and 10 random seeds.
- **Execution:**
  ```powershell
  python scripts/run_fair_baselines.py
  ```
- **Expected Output:**
  Logs per-dataset ARI and NMI for Variance Filter, PCA/SVD, Laplacian Score, and Sparse K-Means, writing records to `results/phase2/fair_baselines.csv`.

---

### 12. `run_high_d_ablation_2x2.py`
- **Purpose:** Full $2 \times 2$ factorial ablation experiment analyzing the interaction between feature gating (Ambient vs. BGSS) and consensus reduction (Dense vs. Anchor) across 6 high-dimensional datasets.
- **Execution:**
  ```powershell
  python scripts/run_high_d_ablation_2x2.py
  ```
- **Expected Output:**
  Generates per-variant summary tables and exports all 420 experiment runs to `results/exp2_ablation/exp2_real_high_d_factorial.csv`.

---

### 13. `run_inductive_direct.py`
- **Purpose:** Evaluates direct inductive projection of out-of-sample test samples onto fitted cluster representations across 9 benchmark datasets and 10 seeds.
- **Execution:**
  ```powershell
  python scripts/run_inductive_direct.py
  ```
- **Expected Output:**
  Exports inductive accuracy metrics across methods (Nystrom Subspace, Full Centroid, Pseudo-Supervised NearestCentroid, Pseudo-Supervised RandomForest, Direct K-Means) to `results/phase2/inductive_direct.csv`.

---

### 14. `run_exp5_controlled_scaling.py`
- **Purpose:** Evaluates runtime and memory scalability across extreme sample sizes ($N \in \{10^4, 10^5, 10^6\}$) under controlled synthetic conditions, measuring the empirical scaling exponent $\beta$.
- **Execution:**
  ```powershell
  python scripts/run_exp5_controlled_scaling.py
  ```
- **Expected Output:**
  Outputs linear regression fits on log-log coordinates, saving metrics and scaling exponent estimates with 95% confidence intervals to `results/passE/exp5_scaling_stats.json`.

---

### 15. `plot_conceptual_framework.py`
- **Purpose:** Renders the four-panel motivational conceptual illustration for Section 1 of the manuscript:
  - Panel (a): True Signal Subspace ($d=2$) with certified anchor cores.
  - Panel (b): High-Dimensional Noise Drowning ($D=2{,}000$) with distance variance collapse inset.
  - Panel (c): Bimodality-Gated Subspace Selection (BGSS) separating signal from noise.
  - Panel (d): Geometry-Calibrated Inductive Projection assigning unseen query instances.
- **Execution:**
  ```powershell
  python scripts/plot_conceptual_framework.py
  ```
- **Expected Output:**
  ```text
  [SUCCESS] Saved figure to: springer_manuscript/figures/fig0_conceptual_framework.png
  [SUCCESS] Saved figure to: paper/figures/fig0_conceptual_framework.png
  [SUCCESS] Saved figure to: manuscript/figures/fig0_conceptual_framework.png
  [SUCCESS] Saved figure to: experiments/figures/fig0_conceptual_framework.png
  ```

---

## Quality and Verification Standards

All retained scripts in this directory conform to the repository's strict quality contract:
- **Zero Fabrication:** All metrics originate from deterministic benchmarks or frozen result stores.
- **PEP 8 / Ruff Compliance:** 100% clean check via `ruff check scripts/` with 0 warnings or errors.
- **Strict Formatting:** Zero em-dash characters (`\u2014`) are permitted anywhere in code, docstrings, or documentation.
