# Reproducibility Guide

**Paper Title:** Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes  
**Target Venue:** Springer Nature (*Data Mining and Knowledge Discovery* / DAMI)  
**Package:** `icc` (v2.2.0)  

This guide provides instructions and complete traceability for peer reviewers and researchers to replicate all empirical results, theoretical proposition validations, tables, and figures reported in the manuscript.

---

## 1. Quickstart Reproduction

To verify the core implementation and reproducibility in under one minute:

```powershell
# 1. Fast smoke test across synthetic and real benchmark datasets (~2s)
python scripts/reproduce.py --scope smoke

# 2. Complete mathematical proofs and 19-point numerical integrity verification (~5s)
python scripts/reproduce.py --scope verify

# 3. Regenerate all LaTeX tables directly from empirical result registries (~5s)
python scripts/reproduce.py --scope tables

# 4. Synchronize and render all high-resolution figures (~10s)
python scripts/reproduce.py --scope figures

# 5. Run the complete reproduction pipeline end-to-end
python scripts/reproduce.py --scope full
```

To run the complete automated test suite (98 tests across unit, integration, and paper verification):
```powershell
python -m pytest tests/
```

---

## 2. Environment and Determinism

### Hardware and System Requirements
- **Operating System:** Linux (Ubuntu 22.04+), macOS (13+), or Windows 10/11 (64-bit).
- **Python Version:** Python 3.10+ (tested through Python 3.14).
- **RAM:** Minimum 8 GB (16 GB recommended for extreme-scale benchmarks).
- **Hardware Acceleration:** All primary algorithms and benchmarks execute on standard CPUs; optional PyTorch GPU acceleration is utilized for deep clustering baselines (DEC, IDEC).

### BLAS Thread Concurrency
To ensure bitwise identical numerical determinacy across CPU architectures, BLAS thread concurrency is pinned to single-threaded execution across all runners:
```bash
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
```

### Random Seed Protocol
All stochastic components (synthetic data generation, feature subspace projections, base $K$-Means initializations) use fixed random seeds documented in `pyproject.toml` and script entrypoints (canonical seeds: `0` through `9` for multi-seed evaluations; `42` for synthetic baselines).

---

## 3. Manuscript Table Traceability Matrix

Every quantitative value in the manuscript tables originates from frozen empirical registries in `results/` and is compiled programmatically via `scripts/make_tables.py`.

| Table | Manuscript Description | Generated LaTeX File | Source Data File | Generating Command |
| :--- | :--- | :--- | :--- | :--- |
| **Table 1** | Distance Geometries and Concentration Bounds | `paper/gen/table01_distance_geometries.tex` | `results/exp8d_geometry_metrics.csv` | `python scripts/make_tables.py` |
| **Table 2** | Real-World Partition Stability Across Perturbations | `paper/gen/table02_real_data_stability.tex` | `results/stability/runs/*.parquet` | `python scripts/make_tables.py` |
| **Table 3** | Inductive Out-of-Sample Cluster Generalization | `paper/gen/table03_inductive_generalization.tex` | `results/exp1_generalization/` | `python scripts/make_tables.py` |
| **Table 4** | Sample Scaling and Runtime Profiling ($N \le 10^5$) | `paper/gen/table04_sample_scaling.tex` | `results/scaling_runs.csv` | `python scripts/make_tables.py` |
| **Table 5** | Extreme-Scale Scaling ($N = 10^6$) | `paper/gen/table05_extreme_scaling.tex` | `results/exp5_extreme_scale/` | `python scripts/make_tables.py` |
| **Table 6** | Omnibus Benchmark ARI Across 13 Datasets | `paper/gen/table06_omnibus_benchmark_ari.tex` | `results/results.json` | `python scripts/make_tables.py` |
| **Table 7** | Large-$K$ Anchor Budget Sensitivity | `paper/gen/table07_large_k_anchor_budget.tex` | `results/exp8e_large_k_anchor_budget.csv` | `python scripts/make_tables.py` |
| **Table 8** | Matched Feature Budget Ablation | `paper/gen/table08_matched_feature_budget.tex` | `results/results.json` | `python scripts/make_tables.py` |
| **Table 9** | Vargha-Delaney $\hat{A}_{12}$ Effect Sizes | `paper/gen/table09_vargha_delaney_effect_sizes.tex` | `results/stats.json` | `python scripts/make_tables.py` |
| **Table 10** | Seed Stability Diagnostics | `paper/gen/table10_seed_stability_diagnostics.tex` | `results/results.json` | `python scripts/make_tables.py` |
| **Table 11** | Full Ablation Variants Breakdown | `paper/gen/table11_ablation_variants.tex` | `results/exp2_ablation/` | `python scripts/make_tables.py` |
| **Table 12** | Factorial Decomposition ($2 \times 2$) | `paper/gen/table12_factorial_decomposition.tex` | `results/exp2_ablation/` | `python scripts/make_tables.py` |
| **Table 13** | Component Contributions & Marginal Gains | `paper/gen/table13_component_contributions.tex` | `results/results.json` | `python scripts/make_tables.py` |
| **Table 14** | Supplementary Foundations & Complexity | `paper/gen/table14_supplementary_foundations.tex` | Theoretical Proofs | `python scripts/make_tables.py` |
| **Table 15** | Case Studies Synthesis (Leukemia, SRBCT, Ovarian) | `paper/gen/table15_case_studies_synthesis.tex` | `results/results.json` | `python scripts/make_tables.py` |
| **Table 16** | Clinical Genomic Subtyping Verification | `paper/gen/table16_case_studies.tex` | `results/results.json` | `python scripts/make_tables.py` |

---

## 4. Manuscript Figure Traceability Matrix

All manuscript figures are saved at 300 DPI vector/raster formats and synchronized across manuscript directories via `scripts/sync_figures.py`.

| Figure | Manuscript Description | Image File | Generating Script |
| :--- | :--- | :--- | :--- |
| **Figure 1** | Conceptual Overview: Geometric Ridge and Distance Distortion | `paper/figures/fig01_conceptual_overview.png` | `scripts/plot_conceptual_framework.py` |
| **Figure 2a** | ARI Stability Under Additive Distractor Noise | `paper/figures/fig02a_ari_stability.png` | `experiments/exp0_falsification/src/plot_all_figures.py` |
| **Figure 2b** | Stability-Accuracy Gap Phase Transition | `paper/figures/fig02b_stability_accuracy_gap.png` | `experiments/exp0_falsification/src/plot_all_figures.py` |
| **Figure 2c** | Noise Distribution Sensitivity (Gaussian, Uniform, Lognormal) | `paper/figures/fig02c_noise_distribution_sensitivity.png` | `experiments/exp0_falsification/src/plot_all_figures.py` |
| **Figure 3** | Real-World Partition Stability Across Perturbation Cohorts | `paper/figures/fig03_real_data_stability.png` | `scripts/make_stability_outputs.py` |
| **Figure 4a** | Inductive Oracle Generalization Accuracy | `paper/figures/fig04a_inductive_oracle_generalization.png` | `experiments/exp1_generalization/src/plot_exp1.py` |
| **Figure 4b** | Inductive Pseudolabel Generalization Accuracy | `paper/figures/fig04b_inductive_pseudolabel_generalization.png` | `experiments/exp1_generalization/src/plot_exp1.py` |
| **Figure 5a** | Sample Complexity Scaling ($N \in [10^3, 10^5]$) | `paper/figures/fig05a_sample_complexity_scaling.png` | `scripts/run_clean_scaling_benchmark.py` |
| **Figure 5b** | Runtime Component Breakdown and Empirical Scaling Exponent | `paper/figures/fig05b_scalability_breakdown.png` | `scripts/run_exp5_controlled_scaling.py` |
| **Figure 6** | Extreme-Scale Scaling ($N = 10^6$) Performance Quad | `paper/figures/fig06_extreme_scale_quad.png` | `experiments/exp5_extreme_scale/src/plot_exp5.py` |
| **Figure 7** | Omnibus Benchmark Matrix (13 Datasets $\times$ 11 Solvers) | `paper/figures/fig07_benchmark_matrix_13datasets.png` | `experiments/exp3_real_world_benchmarks/src/plot_exp3.py` |
| **Figure 8** | Critical Difference Diagram (Nemenyi Post-Hoc Test, $\alpha = 0.05$) | `paper/figures/fig08_critical_difference_diagram.png` | `scripts/make_stats.py` |
| **Figure 9a** | Component Ablation Trajectories Across High-D Datasets | `paper/figures/fig09a_ablation_curves.png` | `experiments/exp2_ablation/src/plot_exp2.py` |
| **Figure 9b** | Factorial Waterfall Gain Analysis | `paper/figures/fig09b_ablation_waterfall.png` | `experiments/exp2_ablation/src/plot_exp2.py` |
| **Figure 10** | Feature Gating Interpretability Audit (Madelon & Synthetic PR) | `paper/figures/fig10_bgss_interpretability_audit.png` | `experiments/exp2_ablation/src/plot_exp2.py` |

---

## 5. Single Source of Truth & Macro Verification

To prevent statistical discrepancies between prose and empirical data, the repository enforces a strict single source of truth:
1. All raw benchmark evaluations are logged in `results/results.json` and `results/stability/`.
2. Omnibus statistical tests (Friedman test, Nemenyi critical differences, Wilcoxon effect sizes) are computed by `scripts/make_stats.py` and exported to `results/stats.json`.
3. All quantitative manuscript numbers are compiled into LaTeX macros via `scripts/make_numbers.py` and saved to `paper/numbers.tex`.
4. Automated verification via `python scripts/check_numbers.py` verifies all 19 core manuscript metrics against the compiled PDF, ensuring zero ungrounded claims.
