# Contributing to Invariant Core Consensus (ICC)

Thank you for your interest in contributing to **Invariant Core Consensus (ICC)**! This repository hosts the open-source reference implementation, test harness, and benchmarking suite for Invariant Core Consensus (ICC) and Conformal Inductive Consensus Clustering (CICC).

We welcome contributions ranging from bug fixes and documentation improvements to new baseline comparisons, additional benchmark datasets, and performance optimizations.

---

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started & Development Setup](#getting-started--development-setup)
3. [Development Workflow](#development-workflow)
4. [Testing & Verification](#testing--verification)
5. [Adding New Baselines & Datasets](#adding-new-baselines--datasets)
6. [Code Style & Quality Standards](#code-style--quality-standards)
7. [Submitting a Pull Request](#submitting-a-pull-request)
8. [Reproducibility & Benchmark Artifacts](#reproducibility--benchmark-artifacts)
9. [AI Navigation & XERJ Indexing](#ai-navigation--xerj-indexing)

---

## Code of Conduct

All contributors and participants are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any violations or concerns to `akashkundu1152@gmail.com`.

---

## Getting Started & Development Setup

### Prerequisites
* Python 3.10 through 3.14 (fully verified on Python 3.10, 3.11, 3.12, 3.13, and 3.14 across Linux and Windows)
* Git

### Step-by-Step Environment Setup
1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/AkashKundu114/icc-clustering.git
   cd icc-clustering
   ```

2. **Create and activate a clean virtual environment**:
   ```bash
   # On Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

   # On Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies in editable mode**:
   ```bash
   # Core dependencies + development and testing toolchains
   pip install -e ".[dev]"
   ```

4. **Verify installation**:
   ```bash
   python -c "import icc; print(icc.__version__)"
   python demo.py
   python -m pytest tests/
   ```

---

## Testing & Verification

All contributions must pass the automated test battery:

```bash
# Run all unit, integration, and regression tests
python -m pytest tests/

# Run Python version compatibility test suite
python -m pytest tests/regression/test_python_compatibility.py -v

# Run linting and code formatting checks
python -m ruff check src/ tests/

# Run static type checking
python -m mypy src
```

---

## Code Style & Quality Standards

- Adhere to PEP 8 styling conventions enforced by Ruff.
- Maximum line length: 120 characters.
- Ensure strict type hints checked by Mypy.
- Preserve backward-compatibility for public APIs and shims.

---

## AI Navigation & XERJ Indexing

This repository is indexed in the [XERJ Corpus Hub](https://hub.xerj.org/contributors/AkashKundu114) for AST-aware symbol lookups, semantic code search, and token-efficient reference retrieval:

```bash
# Autoindex codebase with XERJ
xerj autoindex . --approve proceed --disable-feedback

# Look up symbol definitions
xerj def "<symbol_name>"
```
