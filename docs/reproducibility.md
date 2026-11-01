# Reproducibility Guide

This guide details instructions for reproducing benchmark evaluations, running the test battery, and verifying numerical determinacy across platforms.

---

## 1. Quickstart

Run the automated test battery:
`ash
python -m pytest tests/
`

Execute a sample experiment benchmark:
`ash
python scripts/run.py --config configs/examples/synthetic.yaml
`

Evaluate experimental outputs:
`ash
python scripts/evaluate.py --results results/experiments/<latest_run>.json
`

---

## 2. Environment and Determinism

### Hardware and System Requirements
- **Operating System:** Linux (Ubuntu 22.04+), macOS (13+), or Windows 10/11 (64-bit).
- **Python Version:** Python 3.10+ (tested through Python 3.14).
- **RAM:** Minimum 8 GB (16 GB recommended for large benchmark sweeps).

### BLAS Thread Concurrency
To ensure bitwise identical numerical determinacy across CPU architectures, BLAS thread concurrency can be pinned to single-threaded execution:
`ash
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
`
