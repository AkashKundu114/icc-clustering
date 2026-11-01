# Scripts Directory Catalog

**Repository:** Feature-Gated Bipartite Graph Ensembles (`icc`)  
**Paper Title:** Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes  
**Target Venue:** Springer Nature (*Data Mining and Knowledge Discovery* / DAMI)  
**Release Version:** v2.2.0  

This directory contains the production-grade research reproduction scripts for peer reviewers, reproducibility auditors, and researchers. All ad-hoc, temporary, or experimental prototyping scripts have been purged to present a clean, maintainable, and audit-ready research software repository.

---

## Quickstart Reproduction Guide

Reviewers can verify all empirical results, theoretical propositions, and manuscript artifacts using the central reproduction CLI:

```powershell
# 1. Fast smoke test across synthetic and real benchmark datasets (~2s)
python scripts/reproduce.py --scope smoke

# 2. Complete mathematical proofs and 19-point numerical integrity verification (~5s)
python scripts/reproduce.py --scope verify

# 3. Regenerate all 21 LaTeX tables directly from empirical result registries (~5s)
python scripts/reproduce.py --scope tables

# 4. Synchronize and render all high-resolution figures (~10s)
python scripts/reproduce.py --scope figures

# 5. Run the complete reproduction pipeline end-to-end
python scripts/reproduce.py --scope full
```

---

## Retained Script Catalog

The canonical scripts in this directory are organized into functional modules:

### 1. Central Reproduction & Data Ingestion
- [`reproduce.py`](reproduce.py): Unified reproduction CLI supporting `--scope smoke`, `verify`, `tables`, `figures`, and `full`.
- [`fetch_data.py`](fetch_data.py): Downloads, caches, and verifies the dimensional integrity ($N, D, K$) of all 13 benchmark datasets.
- [`sync_figures.py`](sync_figures.py): Synchronizes and standardizes figure artifacts across manuscript directories (`paper/`, `springer_manuscript/`).
- [`rename_figs_and_tables.py`](rename_figs_and_tables.py): Enforces consistent figure and table filenames matching paper numbering.

### 2. Manuscript Tables, Numbers & Statistics
- [`make_tables.py`](make_tables.py): Programmatically generates all LaTeX tables (Tables 1–21) from frozen result stores.
- [`make_stats.py`](make_stats.py): Computes omnibus statistical significance tests (Friedman $\chi^2$, Nemenyi critical differences, Wilcoxon signed-rank tests) and writes `results/stats.json`.
- [`make_numbers.py`](make_numbers.py): Compiles quantitative macros to `paper/numbers.tex`, guaranteeing zero hand-coded statistics in prose.
- [`make_stability_outputs.py`](make_stability_outputs.py): Aggregates cluster stability metrics and generates stability tables.
- [`export_stats_to_passf.py`](export_stats_to_passf.py): Exports frozen statistical registries across evaluation passes.

### 3. Mathematical & Theoretical Verifications
- [`verify_prop1.py`](verify_prop1.py): Numerical quadrature and root-finding validating the Proposition 1 separation boundary ($\Delta / \sigma_0 \ge 1.854$).
- [`verify_determinacy_identity.py`](verify_determinacy_identity.py): Validates Proposition 2 contingency tensor determinacy to machine precision ($< 10^{-14}$).
- [`verify_bc.py`](verify_bc.py): Analytical derivation and empirical validation of Sarle's Bimodality Coefficient unimodal and bimodal bounds ($BC = 5/9 \approx 0.556$).
- [`verify_bc_simulation.py`](verify_bc_simulation.py): Monte Carlo simulation auditing finite-sample statistical power and noise sensitivity of Sarle's BC.
- [`check_numbers.py`](check_numbers.py): 19-point automated numerical integrity audit verifying that compiled PDF statistics match frozen empirical registries.
- [`verify_refs.py`](verify_refs.py): Automated CrossRef and arXiv bibliographic API verification ensuring citation validity.

### 4. Empirical Benchmarks & Experiments
- [`run_fair_baselines.py`](run_fair_baselines.py): Evaluates feature selection baselines (Variance Filter, Truncated SVD, Laplacian Score, Sparse K-Means) against ICC-v2.
- [`run_high_d_ablation_2x2.py`](run_high_d_ablation_2x2.py): Executes the $2 \times 2$ factorial ablation cross across high-dimensional genomics cohorts over 10 random seeds.
- [`run_inductive_direct.py`](run_inductive_direct.py): Evaluates out-of-sample inductive cluster assignment across benchmark datasets and stratified splits.
- [`run_real_data_stability.py`](run_real_data_stability.py): Evaluates partition stability under bootstrap and subsample perturbations across real-world datasets.
- [`run_clean_scaling_benchmark.py`](run_clean_scaling_benchmark.py): Measures runtime and memory scaling across varying sample sizes $N$ and dimensions $D$.
- [`run_exp5_controlled_scaling.py`](run_exp5_controlled_scaling.py): Controlled scaling benchmark estimating the empirical scaling exponent $\beta \approx 1.05$.
- [`run_phase3_experiments.py`](run_phase3_experiments.py): Executes Phase 3 experiments including large-$K$ anchor budgets, distance geometries, and sensitivity sweeps.
- [`analyze_bgss_meta.py`](analyze_bgss_meta.py): DerSimonian-Laird random-effects meta-analysis, Cochran's $Q$, $I^2$ heterogeneity, and leave-out sensitivity tests.
- [`audit_degeneracy.py`](audit_degeneracy.py): Analyzes null feature gating and cluster degeneracy protection.

### 5. Visualization & Submission Packaging
- [`plot_conceptual_framework.py`](plot_conceptual_framework.py): Renders the multi-panel motivational conceptual diagram (Figure 1) at publication resolution (300 DPI).
- [`plot_fig08_cd_diagram.py`](plot_fig08_cd_diagram.py): Generates the Critical Difference diagram across benchmark algorithms.
- [`replot_fig2_subsample.py`](replot_fig2_subsample.py): Regenerates Figure 2 empirical subsampling stability curves.
- [`package_submission.py`](package_submission.py): Packages the complete LaTeX manuscript source, figures, tables, and bibliography for Springer Nature submission.

### 6. Extended Scientific Audit & Verification Pipelines
- [`cohort_audit/`](cohort_audit/): Modular pipeline for biological dataset provenance, sample identifier linkage, OpenML metadata auditing, and duplicate profile detection.
- [`overnight/`](overnight/): Comprehensive benchmark execution suite for EXP6 (cohort expansion), EXP7 (modern baselines), and EXP8 (unknown-$K$ discovery).

---

## Determinism and Environment

To guarantee bitwise identical outputs across CPU architectures, BLAS thread concurrency is pinned to 1 in all reproduction entrypoints:
```bash
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
```
All random seeds are explicitly documented and fixed in `pyproject.toml` and individual experiment runners.
