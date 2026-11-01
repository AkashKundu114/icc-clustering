# Scripts Catalog

This directory contains command-line interface (CLI) utilities for running experiments, data preparation, evaluation, and benchmark fetching with the **Invariant Core Consensus (ICC)** framework.

---

## Available Scripts

### 1. Experiment Runner (`scripts/run.py`)
Executes an end-to-end clustering benchmark experiment using YAML configuration files.

```bash
python scripts/run.py --config configs/default.yaml
python scripts/run.py --config configs/examples/synthetic.yaml --output-dir results/experiments
```

### 2. Data Preparation CLI (`scripts/prepare_data.py`)
Downloads, verifies, and analyzes high-dimensional datasets. Computes Bimodality Coefficients (BGSS) and feature statistics.

```bash
python scripts/prepare_data.py --dataset colon --visualize
```

### 3. Results Evaluator (`scripts/evaluate.py`)
Loads experimental result JSON files produced by `run.py` and prints summary tables, rank matrices, and statistical metrics.

```bash
python scripts/evaluate.py --results results/experiments/<run_name>.json --export-csv summary.csv
```

### 4. Benchmark Dataset Fetcher (`scripts/fetch_data.py`)
Validates local dataset caches and downloads benchmark datasets from public repositories.

```bash
python scripts/fetch_data.py
```
