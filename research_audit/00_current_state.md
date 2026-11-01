# Research Audit 00: Current State of ICC-Clustering Repository & Manuscript

**Audit Timestamp:** 2026-10-31T23:40:00+05:30  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Working Directory:** `d:\Final Year Project`  
**Dedicated Revision Branch:** `dmkd-revision/scientific-strengthening`  
**Base Commit SHA:** `ca04ccbbc37fbab855e3cb41172f5115c87e3704`  
**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD / DAMI)  
**Lead Auditor:** Scientific Integration and Audit Team  

---

## 1. System Environment & Execution Context

| Component | Verified Specification | Audit Status |
| :--- | :--- | :--- |
| **Operating System** | Windows 11 Enterprise (x64) | Active pair-programming shell: PowerShell |
| **Python Runtime** | Python 3.14.6 (`.venv`) | Verified |
| **Core Scientific Stack** | `numpy==2.4.6`, `scipy==1.18.0`, `scikit-learn==1.9.1`, `pandas==2.2.3` | Installed & Operational |
| **Deep Learning Stack** | `torch==2.16.0.dev20261017+cu134`, `torchvision==0.30.0.dev20261030+cu134`, `tensorflow==2.22.0rc0`, `keras==3.15.1` | Installed & Operational |
| **Single-Cell Stack** | `scanpy==1.12.4`, `anndata==0.13.4` | Installed & Operational |
| **Clustering Extras** | `hdbscan`, `leidenalg`, `igraph` | Available via Scikit-Learn/custom implementations |
| **Git Working Tree** | Branch `dmkd-revision/scientific-strengthening`, checked out from `main` | Clean branching; existing frozen data preserved |

---

## 2. Inventory of Existing Experiments in Repository

| Experiment ID | Directory Path | Core Objective & Protocol | Key Scripts | Frozen Data Status |
| :--- | :--- | :--- | :--- | :--- |
| **EXP0** | `experiments/exp0_falsification/` | Falsification of stability-accuracy correlation under isotropic distractor noise ($D_{\text{noise}} \in [0, 5000]$). | `run_exp0.py`, `plot_exp0.py` | `data/exp0_agg.csv`, `exp0_runs.csv` (Frozen) |
| **EXP1** | `experiments/exp1_generalization/` | Out-of-sample inductive query generalization: Centroid vs. pseudo-label vs. Nyström. | `run_exp1.py`, `plot_exp1.py` | `data/exp1_generalization_results.csv` (Frozen) |
| **EXP2** | `experiments/exp2_ablation/` | Architectural component ablation (V0 to V5) across noise sweeps and high-$D$ cohorts. | `run_exp2.py`, `plot_exp2.py` | `data/exp2_ablation_results.csv` (Frozen) |
| **EXP3** | `experiments/exp3_real_world_benchmarks/` | Multi-dataset empirical evaluation across 13 cohorts (6 high-$D$ oncology microarrays + 7 diverse controls). | `run_exp3.py`, `plot_exp3.py` | `data/exp3_1_benchmark_matrix_v2.csv` (Frozen) |
| **EXP4** | `experiments/exp4_scalability_and_sensitivity/` | Sensitivity to ensemble size $M$, anchor budget $L$, and supplied $K$ misspecification. | `run_exp4.py`, `k_misspecification_sweep.py` | `data/exp4_sample_scaling_summary.csv` (Frozen) |
| **EXP5** | `experiments/exp5_extreme_scale/` | Extreme scalability benchmark up to $N = 10^6$ synthetic Gaussian instances with bipartite graph. | `run_exp5.py`, `plot_exp5.py` | `data/exp5_sample_scaling_results.csv` (Frozen) |
| **Audit Controls** | `experiments/audit_controls/` | Extended 21-dataset benchmark, label-free selector evaluation, and filter controls. | `e1_extended_benchmarks.py`, `a2_controls.py` | `data/e1_extended_benchmarks.csv` (Frozen) |
| **Study Null Gating**| `experiments/study_null_gating/` | Confirmatory GPU null-calibrated gating grid (preregistered hypothesis test). | `run_confirmatory_grid.py`, `gpu_scb.py` | `tier_a_results.json`, `confirmatory_summary.json` (Frozen; Primary H1 failed) |

---

## 3. Inventory of Master Results Registries (`results/`)

1. **`results/passF/` (Canonical Benchmark Suite Pass F - Read-Only):**
   - `benchmark_matrix_summary_passF.csv`: Aggregated performance metrics across 13 datasets and 11 models (143 rows).
   - `fair_baselines_30seeds_passF.csv`: Matched-feature-budget ablation across 9 methods and 6 high-$D$ cohorts over 30 seeds (1,620 rows).
   - `ablation_30seeds_passF.csv`: V0–V5 architectural knockout runs across 6 high-$D$ cohorts over 30 seeds (1,080 rows).
   - `ablation_stats_passF.json`: Summary means for V0–V5 and paired bootstrap statistics ($V_5 - V_4: \Delta = +0.019$).
   - `inductive_paired_splits.csv`: 10-split paired held-out inductive metrics across 6 cohorts (60 rows).
   - `shapiro_wilk_cv_passF.csv`: Normality and per-seed stability statistics over 30 seeds for the 6 high-$D$ cohorts.
   - `vargha_delaney_a12_passF.csv`: Non-parametric $A_{12}$ effect sizes across 10 baselines on 6 high-$D$ cohorts.
   - `friedman_nemenyi_passF.json`: Omnibus Friedman test statistics ($p = 0.40, CD = 4.62$).
2. **`results/passE/` (Scaling & Inductive Agreement - Read-Only):**
   - `inductive_agreement.json`: Test-set cluster assignment agreement distributions.
   - `exp5_controlled_scaling.csv`: Extreme scalability runtime across $N \in [10^4, 10^6]$ over 3 independent seeds.
3. **`results/stability/` (Master Stability Registries):**
   - `subsample_stability_summary.csv`: 30 stratified 80% subsample runs across 6 high-$D$ cohorts and 12 algorithms.
   - `real_data_stability_summary.csv`: Concordance summary table.
4. **`results/stats.json`:** Consolidated single-source-of-truth macro numbers injected into `paper/numbers.tex`.

---

## 4. Current Benchmark Cohort Suite (13 Datasets in Registry)

### Strata 1: High-Dimensional Oncology Microarrays ($D/N > 20$)
- **`cns`**: $N=60, D=7{,}129, K=2, D/N=118.82$ (OpenML 45086; Pomeroy et al. 2002)
- **`colon`**: $N=62, D=2{,}000, K=2, D/N=32.26$ (OpenML 45087; Alon et al. 1999)
- **`leukemia`**: $N=72, D=7{,}129, K=2, D/N=99.01$ (OpenML 1104; Golub et al. 1999)
- **`ovarian`**: $N=253, D=15{,}154, K=2, D/N=59.90$ (OpenML 45098; Petricoin et al. 2002)
- **`prostate`**: $N=102, D=12{,}600, K=2, D/N=123.53$ (OpenML 45099; Singh et al. 2002)
- **`srbct`**: $N=83, D=2{,}308, K=4, D/N=27.81$ (OpenML 45101; Khan et al. 2001)

### Strata 2: Tabular, Single-Cell, Text, Hyperspectral, and Vision Controls
- **`sonar`**: $N=208, D=60, K=2, D/N=0.29$ (OpenML 40)
- **`madelon`**: $N=500, D=500, K=2, D/N=1.00$ (OpenML 1485; 20 XOR + 480 distractor noise)
- **`isolet`**: $N=7{,}797, D=617, K=26, D/N=0.08$ (OpenML 300)
- **`zheng68k`**: $N=700, D=765, K=10, D/N=1.09$ (Scanpy `pbmc68k_reduced`; 10 immune cell types)
- **`newsgroups20`**: $N=18{,}846, D=10{,}000, K=20, D/N=0.53$ (Scikit-Learn TF-IDF 20 Newsgroups)
- **`indian_pines`**: $N=10{,}249, D=200, K=16, D/N=0.02$ (UPV/EHU AVIRIS hyperspectral flight line)
- **`yale_b`**: $N=2{,}414, D=1{,}024, K=38, D/N=0.42$ (Extended Yale B face crops under 64 illuminations)

---

## 5. Current Baseline Implementations Status

1. **Genuinely Implemented & Benchmarked:**
   - Classical: K-Means (1967), Ward Hierarchical (1963), Spectral Clustering (2007), Fuzzy C-Means (1981).
   - Consensus: Standard Consensus (Monti 2003 / Fred & Jain 2005), Core-Halo Consensus (Li et al. 2019), CoHiRF (2024), Ungated Anchor Consensus (ICC_v1), Gated Anchor Consensus (ICC_v2 / GAC).
   - Deep: Deep Embedded Clustering (DEC; Xie et al. ICML 2016, with PyTorch GPU implementation and Keras fallback).
2. **Approximations / Re-implementations:**
   - **FCAG (2024):** Re-implemented Nie et al. anchor bipartite graph $Z$ and generalized eigensolver $M$, but using k-means++ anchors and k-means discretization rather than the published PGD/IRW/CD solvers.
   - **FastMVC (2024):** Marked `stub: true` in `configs/baselines.yaml`. Random-subspace multi-view surrogate, NOT a faithful implementation of FastMICE (Huang et al., IEEE TKDE 2023). Excluded from headline comparisons.
3. **Unimplemented Stubs (Disabled in YAML, raising `NotImplementedError`):**
   - `run_idec` (IDEC; Guo et al. 2017)
   - `run_contrastive_clustering` (CC; Li et al. 2021)
   - `run_scan` (SCAN; Van Gansbeke et al. 2020)

---

## 6. Manuscript Source Architecture

- **`paper/main.tex`:** Primary LaTeX source with figures, tables, and algorithms.
- **`springer_manuscript/main.tex`:** Springer Nature format manuscript synchronized with `paper/main.tex`.
- **`paper/gen/` & `springer_manuscript/gen/`:** Auto-generated LaTeX tables generated via `scripts/make_tables.py` and `scripts/make_stability_outputs.py`.
- **`paper/numbers.tex`:** Auto-generated LaTeX macro variables generated via `scripts/make_stats.py`.
