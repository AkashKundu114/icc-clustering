# Development Guide

## Architecture Overview

```text
src/icc/
├── algorithms/     # Comparative baseline shims (re-exporting from baselines/)
├── baselines/      # Canonical comparative baseline algorithms (KMeans, Spectral, GMM, HDBSCAN, FCAG, etc.)
├── benchmarks/     # Canonical benchmark runner and scaling suites
├── consensus/      # ICC estimator and legacy consensus implementation, ASPP, Auto-K, CICC
├── data/           # Dataset shims, preprocessing (BGSS), and synthetic generators
├── datasets/       # Canonical 13-benchmark dataset loader and registry suite
├── evaluation/     # Dual-backend evaluation metrics (ARI, NMI, AMI, PAC, coverage)
├── experiments/    # Backward-compatibility shims for benchmarks/
├── stats/          # Non-parametric hypothesis tests (Friedman, Nemenyi CD, TOST, Wilcoxon, Bonferroni)
└── utils/          # Logging, seed control, and timers
```

## Running Tests

Supported and verified across Python 3.10, 3.11, 3.12, 3.13, and 3.14.

Run full test suite:
```bash
python -m pytest tests/
```

Run specific test categories:
```bash
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/regression/
```

Run Python version compatibility verification:
```bash
python -m pytest tests/regression/test_python_compatibility.py -v
```

## Code Quality & Formatting

Linting and formatting with Ruff:
```bash
ruff check src tests
ruff format src tests
```

Type checking with Mypy:
```bash
mypy src
```
