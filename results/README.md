# Experimental Results and Artifacts

This directory contains frozen experimental results, evaluation metrics, statistical audit summaries, and aggregate artifacts.

## Repository Policy
- Metric summaries, frozen benchmark registries (`stats.json`, `results.json`, `passF/`), and statistical logs are tracked in version control for complete reproducibility.
- Large raw simulation replicates (such as millions of Monte Carlo trials) are excluded via `.gitignore`.
- Reference verification records and provenance ledgers are tracked in `refs_report.csv` and `refs_map.csv`.

## Directory Structure
```text
results/
├── passF/                             # Frozen Pass F execution store (3,000 model fits across 13 datasets)
├── passE/                             # Pass E exploratory scaling runs and controlled scaling
├── phase2/                            # Statistical evaluations and fair baseline comparisons
├── exp2_ablation/                     # Factorial ablation evaluations on genomics cohorts
├── stability/                         # Multi-seed cluster stability measurements
├── stats.json                         # Canonical benchmark result registry (single source of truth)
├── results.json                       # Master benchmark result registry
├── MANIFEST.md                        # Checksum and execution manifest
├── INVENTORY.md                       # Master experiment and configuration inventory
├── refs_report.csv                    # Automated CrossRef/arXiv API reference verification report
├── refs_map.csv                       # Per-citation section, sentence, and scientific rationale mapping
├── query_latency.json                 # Microsecond out-of-sample query latency benchmarks
├── exp3_cohirf_benchmark.csv          # CoHiRF baseline evaluations across 13 cohorts
├── exp8b_anchor_selection.csv         # Certified core vs random anchor selection evaluation
├── exp8c_feature_gating.csv           # BGSS vs random subspace feature selection evaluation
├── exp8d_distance_metrics.csv         # Distance concentration metrics across noise dimensions
├── exp8d_geometry_metrics.csv         # Metric concentration and distance ratio evaluations
├── exp8e_large_k_anchor_budget.csv    # Large-K anchor budget scaling evaluation (refuting starvation)
└── exp8f_sensitivity_grid.csv         # Hyperparameter sensitivity grid (M x L)
```

## Traceability & Scientific Verification
Every metric reported in the manuscript traces directly to `results/stats.json` and the Pass F execution store in `results/passF/`.

To verify all machine-checkable assertions and statistical invariants:
```bash
python tools/check_consistency.py
```
This automated verification suite checks:
1. Dataset counts, identifiers, and dimensions against `data/registry.yaml`.
2. Total fit count arithmetic: `(6 × 12 × 30) + (7 × 12 × 10) = 3,000` model fits.
3. High-D subgroup mean ARI (`0.217`), median ARI (`0.061`), and Friedman rank statistics.
4. Grand mean ARI (`0.152`), Friedman p-value (`0.40`), and Nemenyi critical difference (`4.62`).
5. Presence and integrity of all required result artifacts.
