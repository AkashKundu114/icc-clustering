# Peer Reviewer & Reproducibility Guide

**Manuscript Title:** Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes  
**Target Publication Venue:** Springer Nature (*Data Mining and Knowledge Discovery* / DAMI)  
**Reference Implementation:** `icc` (Release v2.2.0)  

This guide provides an exhaustive, push-button roadmap for peer reviewers, academic researchers, and senior engineers to reproduce and verify every empirical table (Table 1 through Table 16), figure (Figure 1 through Figure 9), theoretical proposition, and asymptotic complexity claim presented in the manuscript.

---

## 1. Executive Push-Button Verification (< 1 Minute)

To verify the core implementation and empirical determinism immediately on any standard x86_64 or ARM64 system:

```bash
# 1. Fast smoke test across synthetic and real benchmark cohorts (< 3 seconds)
python scripts/reproduce.py --scope smoke

# 2. Recompile all manuscript LaTeX tables directly from raw empirical stores (~2 seconds)
python scripts/reproduce.py --scope tables

# 3. Verify theoretical proofs and statistical invariants (~3 seconds)
python scripts/reproduce.py --scope verify

# 4. Automated scientific consistency and fit-count arithmetic audit (< 2 seconds)
python tools/check_consistency.py

# 5. Full test suite (84 passing unit and integration tests)
python -m pytest tests/ -q
```

---

## 2. Environment, Determinism, & Pre-Flight Checklist

### Hardware and System Requirements
- **Operating Systems:** Linux (Ubuntu 20.04+, RHEL 8+), macOS (12.0+), or Windows 10/11 (64-bit).
- **Python Runtime:** Python 3.10, 3.11, or 3.12 (fully tested on 3.10 through 3.14).
- **Memory (RAM):** 8 GB minimum; 16 GB recommended for extreme-scale synthetic evaluations ($N = 10^6$).
- **Compute Acceleration:** All benchmark pipelines execute natively on CPU. PyTorch GPU acceleration is optional for deep embedding baselines (DEC).

### Determinism Protocol
Consensus clustering and randomized subspace projections require strict single-thread linear algebra determinism across diverse BLAS implementations (OpenBLAS, Intel MKL, Apple Accelerate). Enforce single-threaded BLAS execution prior to reproduction:

```bash
# Linux / macOS
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

# Windows (PowerShell)
$env:OMP_NUM_THREADS="1"
$env:MKL_NUM_THREADS="1"
$env:OPENBLAS_NUM_THREADS="1"
```

All stochastic components (synthetic generation, feature subspace projections, base $K$-Means initializations) use fixed canonical random seeds documented in the evaluation scripts (`seed` $\in \{0, \dots, 29\}$ for the 6 high-dimensional cancer cohorts; `seed` $\in \{0, \dots, 9\}$ for the remaining 7 cohorts; `seed = 42` for synthetic baselines).

---

## 3. Paper Table Traceability Matrix (Tables 1 through 16)

Every quantitative entry across all manuscript tables is compiled programmatically from raw, per-seed empirical result logs stored in `results/passF/`, `results/passE/`, and `results/`. Zero numbers are hand-typed.

| Table | Manuscript Description | Source Empirical File(s) in `results/` | CLI Generating Command | Expected Runtime |
| :--- | :--- | :--- | :--- | :---: |
| **Table 1** | Distance Geometries and Concentration Bounds | `results/exp8d_geometry_metrics.csv` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 2** | Real-World Partition Stability Across Perturbations | `results/stability/` / `results/results.json` | `python scripts/run_real_data_stability.py` | ~15 s |
| **Table 3** | Held-Out Inductive Generalization (ARI on 20% test splits) | `results/passF/inductive_paired_splits.csv`<br>`results/passE/inductive_agreement.json`<br>`results/passF/inductive_bootstrap_stats.json` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 4** | Computational Scalability vs. Sample Size $N$ ($N \le 10^4$) | `results/scaling_runs.csv`<br>`experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_results.csv` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 5** | Extreme Scalability to $N = 10^6$ Samples (3 Seeds) | `results/passE/exp5_controlled_scaling.csv`<br>`results/passE/exp5_scaling_stats.json` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 6** | Omnibus Benchmark ARI Across 13 Datasets (12 Methods) | `results/passF/benchmark_matrix_passF.csv`<br>`results/passF/benchmark_matrix_summary_passF.csv`<br>`results/passF/friedman_nemenyi_passF.json`<br>`results/stats.json` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 7** | Large-$K$ Anchor Budget Sensitivity ($K \in [5, 30], L \in [20, 100]$) | `results/exp8e_large_k_anchor_budget.csv` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 8** | Matched-Budget Feature Selection Baselines ($\lfloor 0.15 D \rfloor$) | `results/passF/fair_baselines_30seeds_passF.csv`<br>`results/passF/fair_baselines_summary_passF.json` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 9** | Vargha-Delaney $\hat{A}_{12}$ Effect Sizes vs. 11 Baselines | `results/passF/vargha_delaney_a12_passF.csv` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 10** | Seed Stability Diagnostics (Shapiro-Wilk $W$, $p$, CV) | `results/passF/shapiro_wilk_cv_passF.csv` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 11** | Architectural Component Ablation ($V_0$ through $V_5$) | `results/passF/ablation_30seeds_passF.csv`<br>`results/passF/ablation_stats_passF.json` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 12** | $2 \times 2$ Factorial Decomposition (Representation $\times$ Ensemble) | `results/passF/ablation_stats_passF.json` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 13** | Component Contributions (Paired $\Delta$ & 10k Bootstrap CIs) | `results/passF/component_contributions_passF.csv` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 14** | Supplementary Foundations & Asymptotic Complexity | Theoretical derivations & `results/refs_report.csv` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 15** | Case Studies Synthesis (Leukemia, SRBCT, Ovarian) | `results/passF/benchmark_matrix_summary_passF.csv`<br>`results/stats.json` | `python scripts/reproduce.py --scope tables` | < 2 s |
| **Table 16** | Degeneracy and Smallest-Cluster Size Audit | `results/stability/` / `results/passF/` | `python scripts/run_real_data_stability.py` | ~15 s |

---

## 4. Paper Figure Traceability Matrix (Figures 1 through 9)

All publication figures are rendered at 300 DPI vector/raster format and correspond to dedicated rendering scripts in `scripts/` and `experiments/`.

| Figure | Description | Underlying Data Files | Generating Script / Command | Expected Runtime |
| :--- | :--- | :--- | :--- | :---: |
| **Figure 1** | Conceptual Framework: Geometric Concentration, Ridge Projection, and Bipartite Transfer-Cut Graph | Synthetic manifold simulation | `python scripts/plot_conceptual_framework.py` | ~3 s |
| **Figure 2a** | ARI Stability Under Additive Distractor Noise ($D_{\text{noise}} \in [0, 5000]$) | `experiments/exp0_falsification/data/exp0_runs.csv`<br>`.../exp0_agg.csv` | `python experiments/exp0_falsification/src/plot_all_figures.py` | ~5 s |
| **Figure 2b** | Stability-Accuracy Gap ($\Delta = \text{Stability} - \text{ARI}$) Phase Transition | `experiments/exp0_falsification/data/exp0_finegrid.csv` | `python experiments/exp0_falsification/src/plot_all_figures.py` | ~5 s |
| **Figure 2c** | Noise Distribution Sensitivity Matrix (Gaussian, Uniform, Lognormal, $t$) | `experiments/exp0_falsification/data/exp0_noisetypes.csv` | `python experiments/exp0_falsification/src/plot_all_figures.py` | ~5 s |
| **Figure 3** | Real-World Partition Stability Across Perturbation Cohorts | `results/stability/` / `results/results.json` | `python scripts/run_real_data_stability.py` | ~15 s |
| **Figure 4a** | Inductive Oracle Generalization Accuracy | `experiments/exp1_generalization/data/exp1_generalization_results.csv` | `python experiments/exp1_generalization/src/plot_exp1.py` | ~4 s |
| **Figure 4b** | Inductive Pseudolabel Generalization Accuracy in High Noise | `experiments/exp1_generalization/data/exp1_pseudolabel_results.csv` | `python experiments/exp1_generalization/src/plot_exp1.py` | ~4 s |
| **Figure 5a** | Sample Complexity Scaling ($N \in [500, 10{,}000]$) | `results/scaling_runs.csv` | `python scripts/rerun_table4_timing.py` | ~5 s |
| **Figure 5b** | Runtime Component Breakdown and Empirical Scaling Exponent | `results/passE/exp5_controlled_scaling.csv` | `python scripts/rerun_table4_timing.py` | ~5 s |
| **Figure 6** | Extreme-Scale Scaling ($N = 10^6$) Performance Quad | `results/passE/exp5_controlled_scaling.csv`<br>`results/passE/exp5_scaling_stats.json` | `python experiments/exp5_extreme_scale/src/plot_exp5.py` | ~4 s |
| **Figure 7** | Omnibus Benchmark Matrix (13 Datasets $\times$ 11 Solvers) | `results/passF/benchmark_matrix_passF.csv` | `python experiments/exp3_real_world_benchmarks/src/plot_exp3.py` | ~5 s |
| **Figure 8** | Critical Difference Diagram (Nemenyi Post-Hoc Test, $\alpha = 0.05$) | `results/passF/friedman_nemenyi_passF.json`<br>`results/stats.json` | `python scripts/compute_stats_summary.py` | < 2 s |
| **Figure 9a** | Component Ablation Trajectories Across High-D Genomic Cohorts | `results/passF/ablation_30seeds_passF.csv` | `python experiments/exp2_ablation/src/plot_exp2.py` | ~5 s |
| **Figure 9b** | Factorial Waterfall Gain Analysis: Feature Gating vs. Anchor Consensus | `results/passF/ablation_stats_passF.json` | `python experiments/exp2_ablation/src/plot_exp2.py` | ~5 s |

---

## 5. Verification Checklist for Peer Reviewers

To systematically confirm the validity of all findings in under five minutes, reviewers can follow this five-step audit protocol:

- [ ] **Step 1: Check Environment and Dependencies**
  ```bash
  python -V
  python -c "import icc; print(f'ICC version: {icc.__version__}')"
  ```
- [ ] **Step 2: Execute Automated Consistency Checker**
  ```bash
  python tools/check_consistency.py
  ```
  *Expected Output:* Confirms 13 datasets in `data/registry.yaml`, 6 high-D cohorts ($D/N > 20$), exact fit arithmetic ($(6 \times 12 \times 30) + (7 \times 12 \times 10) = 3{,}000$ model fits), and confirms canonical statistical invariants in `results/stats.json`.
- [ ] **Step 3: Run Push-Button Smoke Suite**
  ```bash
  python scripts/reproduce.py --scope smoke
  ```
  *Expected Output:* Executes synthetic verification and runs Leukemia (Seed 0, ARI = 0.7376) and SRBCT (Seed 0, ARI = 0.4719) benchmarks in < 3 seconds.
- [ ] **Step 4: Regenerate Paper Tables from Raw Data**
  ```bash
  python scripts/reproduce.py --scope tables
  ```
  *Expected Output:* Dynamically builds all LaTeX tables from frozen Pass F files in `results/passF/` and places them in `paper/gen/`.
- [ ] **Step 5: Run Full Test Harness**
  ```bash
  python -m pytest tests/ -q
  ```
  *Expected Output:* `84 passed` across core clustering, conformal uncertainty estimation, bipartite graphs, and inductive projection modules.
