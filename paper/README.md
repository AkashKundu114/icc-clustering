# Manuscript Figures and Generated Tables

This directory contains publication figures and programmatic table files generated for:

> **"Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes"**  
> Springer Nature *Data Mining and Knowledge Discovery* (DAMI).

## Directory Structure

- `figures/`: High-resolution (300 DPI) publication figures and diagrams.
- `gen/`: Programmatically generated LaTeX tables (`.tex`) output by `python scripts/reproduce_tables.py`.

## Reproduction Commands

To regenerate all tables and figures from raw empirical stores:
```bash
# Regenerate LaTeX tables
python scripts/reproduce_tables.py

# Regenerate figures
python scripts/reproduce_figures.py
```
