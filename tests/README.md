# Test Automation Suite

This directory contains the unit, integration, and regression test suites for **Invariant Core Consensus (ICC)**.

All 118 tests pass with a 100% pass rate.

---

## Directory Architecture

The test suite is organized into three distinct tiers:

```text
tests/
├── unit/                       # Fast unit tests (< 0.1s each)
│   ├── test_core.py            # Synthetic generators and core baseline mechanics
│   ├── test_consensus.py       # ICC-v2 and GAC ensemble solvers
│   ├── test_aspp.py            # Anchor-Space Perturbation Profiler and PSI
│   ├── test_metrics.py         # Evaluation metrics with dual-backend fallback
│   ├── test_autok.py           # Auto-K model order selection
│   ├── test_cicc.py            # Conformal clustering and target-decoy FDR
│   ├── test_algorithms.py      # Baseline clustering algorithms dispatch
│   ├── test_inductive.py       # Inductive out-of-sample projection
│   └── test_edge_cases.py      # Numerical edge cases, zero-variance, missing data
├── integration/                # Pipeline and system integration tests
│   ├── test_datasets.py        # Dataset registry and cache integrity
│   ├── test_cohort_discovery.py # GEO metadata parsing and validation
│   ├── test_cohort_provenance.py# Cohort independence and sample integrity
│   ├── test_pipeline.py        # End-to-end preprocessing, training, evaluation
│   └── test_runner.py          # CLI runner and YAML config loading
└── regression/                 # Regression and theoretical boundary tests
    ├── test_anchor_fidelity.py # Anchor approximation fidelity bounds
    ├── test_scaling_timing.py  # Wall-clock scaling and memory allocation
    ├── test_theory_boundaries.py # Analytical separation bounds and surrogate disclosure
    ├── test_algorithm_fidelity.py# Algorithm parity and fallback warnings
    └── test_leakage.py         # Train/test leakage prevention checks
```

---

## Running Tests

### Run Full Test Suite
```bash
python -m pytest tests/
```

### Run Specific Test Tiers
```bash
# Unit tests only
python -m pytest tests/unit/

# Integration tests only
python -m pytest tests/integration/

# Regression tests only
python -m pytest tests/regression/
```

### Run with Coverage
```bash
python -m pytest tests/ --cov=src --cov-report=term-missing
```
