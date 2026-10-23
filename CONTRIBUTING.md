# Contributing to Inductive Consensus Clustering (ICC-v2)

Thank you for your interest in contributing to **Inductive Consensus Clustering (ICC-v2)**! This repository hosts the official reference implementation, full reproducibility test harness, and experiment suite for our paper submitted to **Springer Nature (*Data Mining and Knowledge Discovery* / DAMI)**.

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
8. [Reproducibility & Manuscript Artifacts](#reproducibility--manuscript-artifacts)

---

## Code of Conduct

All contributors and participants are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any violations or concerns to `akashkundu11522@gmail.com` or `akash231001001449@technoindiaeducation.com`.

---

## Getting Started & Development Setup

### Prerequisites
* Python 3.10+ (tested on Python 3.10, 3.11, 3.12, and 3.14)
* Git

### Step-by-Step Environment Setup
1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/inductive-consensus-clustering.git
   cd inductive-consensus-clustering
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
   ```

---

## Development Workflow

1. **Branch Naming**:
   Create a dedicated branch for your feature or bugfix from `main`:
   * `feat/short-description` (for new features or methods)
   * `fix/bug-description` (for bug fixes)
   * `exp/experiment-name` (for empirical extensions or evaluations)
   * `docs/improvement-name` (for documentation updates)

   ```bash
   git checkout -b feat/support-sparse-matrices
   ```

2. **Commit Conventions**:
   Write clear, imperative commit messages (e.g., `Add sparse matrix support for VSSG feature gating`, `Fix off-by-one indexing in bipartite anchor graph`).

---

## Testing & Verification

Every contribution must pass the automated test harness.

* **Run all tests**:
  ```bash
  python -m pytest tests -q
  ```

* **Run tests with coverage tracking**:
  ```bash
  python -m pytest tests --cov=src/icc --cov-report=term-missing
  ```

* **Run the quick interactive demo**:
  ```bash
  python demo.py
  ```

* **Verify numerical macro consistency with results registry**:
  ```bash
  python tests/test_macro_consistency.py
  python tests/test_pdf_allowlist.py
  ```

---

## Adding New Baselines & Datasets

### 1. Adding a New Baseline Algorithm
1. Implement the baseline function inside the appropriate sub-module under `src/icc/baselines/`:
   * `classical.py`: Single-model classical clustering (e.g., agglomerative, density-based).
   * `consensus.py`: Ensemble consensus methods.
   * `anchor.py`: Scalable bipartite or anchor-based clustering.
   * `deep.py`: Unsupervised deep clustering models.
2. Standard function signature:
   ```python
   def run_my_baseline(X: np.ndarray, k: int, seed: int = 42) -> tuple[np.ndarray, float, dict]:
       """
       Parameters
       ----------
       X : np.ndarray of shape (N, D)
       k : int (number of clusters)
       seed : int

       Returns
       -------
       labels : np.ndarray of shape (N,)
       runtime_seconds : float
       metadata : dict
       """
       ...
   ```
3. Register the method in `src/icc/baselines/__init__.py` and `configs/baselines.yaml`.

### 2. Adding a New Benchmark Dataset
1. Register the dataset metadata in `configs/datasets.yaml`.
2. Add the loader function in `src/icc/datasets/` ensuring it returns `X: np.ndarray` (standardized float64) and `y: np.ndarray` (integer labels in `[0, K-1]`).

---

## Code Style & Quality Standards

We use [Ruff](https://github.com/astral-sh/ruff) for fast, unified linting and formatting.

* **Check linting and formatting**:
  ```bash
  ruff check .
  ```

* **Automatically apply safe fixes**:
  ```bash
  ruff check --fix .
  ruff format .
  ```

---

## Submitting a Pull Request

Before opening a pull request, ensure:
- [ ] All 84 unit and integration tests pass (`pytest tests -q`).
- [ ] Code formatting and lint checks pass without errors (`ruff check .`).
- [ ] Any newly introduced public functions or classes have descriptive NumPy-style docstrings.
- [ ] If modifying algorithmic logic, verify that benchmark reproducibility is maintained.

---

## Reproducibility & Manuscript Artifacts

* If changes affect figures or benchmark CSVs, regenerate and synchronize figure assets:
  ```bash
  python scripts/sync_figures.py
  ```
* Verify and synchronize single source of truth macros:
  ```bash
  python scripts/make_numbers.py
  ```

Thank you for helping push the frontiers of robust, scalable consensus clustering!
