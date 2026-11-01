# Development Guide

## Architecture Overview

```text
src/icc/
├── algorithms/     # Comparative baseline algorithms (KMeans, Spectral, GMM, HDBSCAN, FCAG, etc.)
├── consensus/      # Core consensus engines (ICCv2, GAC, ICCv1, ASPP, Auto-K, CICC)
├── data/           # Dataset registry, preprocessing (BGSS), and synthetic generators
├── evaluation/     # Evaluation metrics (ARI, NMI, AMI, PAC, coverage)
├── experiments/    # Unified experiment runner
├── stats/          # Non-parametric hypothesis tests (Friedman, Nemenyi CD, TOST)
└── utils/          # Logging, seed control, and timers
```

## Running Tests

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
