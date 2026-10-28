# Experimental Results and Artifacts

This directory contains frozen experimental results, evaluation metrics, statistical audit summaries, and aggregate artifacts.

## Repository Policy
- Metric summaries, frozen benchmark registries (`results.json`, `MANIFEST.md`), and statistical logs are tracked in version control for complete reproducibility.
- Large raw simulation replicates (such as millions of Monte Carlo trials) are excluded via `.gitignore`.
- Plotted figure binaries are excluded and automatically synced into `paper/figures/`.

## Directory Structure
```text
results/
├── exp0_falsification/                 # Exp 0 noise falsification metrics and runs
├── exp1_generalization/                # Exp 1 out-of-sample inductive generalization
├── exp2_ablation/                      # Exp 2 ablation study on ASPP and ensemble weighting
├── exp3_real_world_benchmarks/         # Exp 3 real-world multi-dataset benchmark tables
├── exp4_scalability_and_sensitivity/   # Exp 4 scaling with sample size and dimensionality
├── exp5_extreme_scale/                 # Exp 5 extreme-scale (100k samples, 50k dimensions)
├── phase2/                             # Statistical tests (Friedman, Nemenyi CD)
├── study_null_gating/                  # Confirmatory GPU null-gating replicates
├── figures/                            # Consolidated result visualizations
├── tables/                             # Auto-generated LaTeX tables
├── results.json                        # Master benchmark result registry (single source)
├── MANIFEST.md                         # Checksum and execution manifest
├── INVENTORY.md                        # Master experiment and configuration inventory
├── PLAN.md                             # Pre-registered experimental execution protocol
├── refs_report.csv                     # Automated CrossRef/arXiv API reference verification report
├── refs_map.csv                        # Per-citation section, sentence, and scientific rationale mapping
├── lit_candidates.csv                  # Candidate 2024–2026 literature survey records
├── exp3_cohirf_benchmark.csv           # CoHiRF baseline benchmark evaluations across 13 cohorts
├── exp8b_anchor_selection.csv          # Certified core vs random anchor selection evaluation
├── exp8c_feature_gating.csv            # BGSS vs random subspace feature selection evaluation
├── exp8d_distance_metrics.csv          # Distance concentration metrics across noise dimensions
├── exp8e_large_k_anchor_budget.csv     # Large-K anchor budget scaling evaluation (refuting starvation)
└── exp8f_sensitivity_grid.csv          # Hyperparameter sensitivity grid (M x L)
```

## Traceability to Manuscript
Every metric reported in the manuscript originates from `results.json` and is injected into LaTeX via `paper/numbers.tex`:
```bash
# Update manuscript macros from results.json
python scripts/make_numbers.py

# Verify reference audit against CrossRef and arXiv APIs
python scripts/verify_refs.py refs.bib --out results/refs_report.csv --manual refs_manual.csv
```
