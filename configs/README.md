# Configuration Files

This directory contains configuration definitions for experiments, baseline models, datasets, and local AI coding agents.

## Contents
- `experiment_defaults.yaml`: Global default hyperparameters, random seeds, and compute settings for experiment execution.
- `baselines.yaml`: Baseline solver configurations (e.g., standard consensus clustering, DEC, spectral clustering, fuzzy c-means).
- `datasets.yaml`: Dataset specifications, split ratios, preprocessing pipelines, and dimensions.
- `agent.project.yaml`: Version-controlled non-secret project goals, constraints, and research rules for AI agents.
- `agent.local.example.yaml`: Template for machine-local compute limits and resource budgets. Copy to `agent.local.yaml` (ignored by Git).
