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
└── MANIFEST.md                         # Checksum and execution manifest
```

## Traceability to Manuscript
Every metric reported in the manuscript originates from `results.json` and is injected into LaTeX via `paper/numbers.tex`:
```bash
# Update manuscript macros from results.json
python scripts/make_numbers.py
```
