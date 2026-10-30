---
name: Reproducibility Inquiry / Benchmark Question
about: Inquiries regarding paper experiments, baseline evaluations, or benchmark data reproduction
title: '[REPRODUCIBILITY] '
labels: reproducibility, question
assignees: ''
---

## Specific Paper Table / Figure in Question
Specify which table or figure from the paper you are seeking to replicate:

### Empirical Tables (Tables 1–16)
- [ ] Table 1: Distance Geometries & Concentration Bounds (`results/tables/table01_distance_geometries.csv`)
- [ ] Table 2: Real-World Partition Stability Across Perturbations (`results/tables/table02_real_data_stability.csv`)
- [ ] Table 3: Held-Out Inductive Generalization (`results/tables/table03_inductive_generalization.csv`)
- [ ] Table 4: Computational Scalability vs. $N$ (`results/tables/table04_sample_scaling.csv`)
- [ ] Table 5: Extreme Scalability to $N=10^6$ (`results/tables/table05_extreme_scaling.csv`)
- [ ] Table 6: Omnibus Benchmark ARI Across 13 Datasets (`results/tables/table06_omnibus_benchmark_ari.csv`)
- [ ] Table 7: Large-$K$ Anchor Budget Sensitivity (`results/tables/table07_large_k_anchor_budget.csv`)
- [ ] Table 8: Matched-Budget Feature Selection Baselines (`results/tables/table08_matched_feature_budget.csv`)
- [ ] Table 9: Vargha-Delaney Effect Sizes $\hat{A}_{12}$ (`results/tables/table09_vargha_delaney_effect_sizes.csv`)
- [ ] Table 10: Seed Stability Diagnostics (Shapiro-Wilk $W$, $p$, CV) (`results/tables/table10_seed_stability_diagnostics.csv`)
- [ ] Table 11: Architectural Component Ablation $V_0$–$V_5$ (`results/tables/table11_ablation_variants.csv`)
- [ ] Table 12: $2 \times 2$ Factorial Decomposition (`results/tables/table12_factorial_decomposition.csv`)
- [ ] Table 13: Component Contributions & Paired Bootstrap CIs (`results/tables/table13_component_contributions.csv`)
- [ ] Table 15: Clinical Case Studies Synthesis (Leukemia, SRBCT, Ovarian) (`results/tables/table15_case_studies_synthesis.csv`)
- [ ] Table 16: Cluster Degeneracy Audit (`results/stability_degeneracy_audit.csv`)

### Figures (Figures 1–10)
- [ ] Figure 1: Conceptual Framework & Architecture
- [ ] Figure 2a, 2b, 2c: Synthetic Noise Falsification Suite
- [ ] Figure 3: Real-World Partition Stability & Accuracy Trap
- [ ] Figure 4a, 4b: Inductive Generalization
- [ ] Figure 5a, 5b: Sample Complexity Scaling vs. $N$
- [ ] Figure 6: Extreme Scalability to $N=10^6$ Quad
- [ ] Figure 7: Omnibus Benchmark Matrix (13 Datasets $\times$ 11 Baselines)
- [ ] Figure 8: Critical Difference (CD) Diagram
- [ ] Figure 9a, 9b: Stepwise Component Ablation Curves & Waterfall
- [ ] Figure 10: BGSS Saliency & Interpretability Audit

## Execution Command & Observed Output
- **Command executed:**
  ```bash
  python scripts/reproduce.py --scope ...
  # or
  python scripts/reproduce_tables.py --table ...
  ```
- **Observed output or metrics:**
- **Expected values according to the paper / `docs/REPRODUCIBILITY.md`:**

## System Environment & Hardware
- OS: [e.g., Linux Ubuntu 22.04 LTS / Windows 11 / macOS Sonoma]
- Python Version: [e.g., 3.10.12, 3.11.8, 3.12.3]
- BLAS Thread Determinism: Did you set `export OMP_NUM_THREADS=1`? [Yes / No]
- CPU Architecture & Available Memory:

## Additional Context & Diagnostic Logs
Attach any terminal logs, CSV outputs, or tracebacks to assist in reproduction verification.
