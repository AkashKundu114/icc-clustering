# Reproducibility Guide: GAC Pipeline & Benchmark Suite

This guide provides step-by-step instructions for reproducing all empirical benchmarks, statistical tests, scaling evaluations, and figure assets reported in the manuscript:  
***Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes***

---

## 1. Environment & Dependencies

### Prerequisites
- Python 3.10+ (Tested on Python 3.14.6)
- OS: Linux, macOS, or Windows 11 (64-bit)
- Dedicated RAM: $\ge 16\text{ GB}$ recommended for billion-element synthetic scaling runs.

### Installation
Clone the repository and install core numerical packages:
```bash
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Core numerical libraries:
- `numpy>=1.26.0` (evaluated on 2.4.6)
- `scipy>=1.12.0` (evaluated on 1.18.0)
- `scikit-learn>=1.4.0` (evaluated on 1.9.1)
- `torch>=2.2.0` (evaluated on 2.16.0)

---

## 2. Automated Test Suite & Static Verification

Run the full automated test suite (94 unit, regression, and allowlist tests):
```bash
python -m pytest tests/ -v
```
*Expected Result:* `94 passed in ~45 seconds`.

Run code quality and static typing checks:
```bash
python -m ruff check src/
python -m mypy -p icc
python -m mypy -p cicc
```
*Expected Result:* Zero errors across all modules.

---

## 3. Data Acquisition

Download and cache all 13 multi-domain benchmark datasets from open-access repositories:
```bash
python scripts/fetch_data.py
```
This script downloads datasets from OpenML, Scanpy (PBMC68k), and UCI into `data/cache/`. Raw benchmark datasets are immutable.

---

## 4. Reproducing Core Empirical Benchmarks

### 4.1 Subsample Stability Protocol & Null Controls (Table 3)
To reproduce the 30-seed stratified subsample stability evaluations and column-permuted null controls across the six high-dimensional cohorts:
```bash
python scripts/stability_subsample.py
```
*Output Artifact:* `results/stability/subsample_stability_summary.csv`.

### 4.2 Benchmark Evaluation on 13 Cohorts (Table 9)
To run all 12 clustering algorithms across all 13 benchmarks under canonical seeds:
```bash
python scripts/run_fair_baselines.py
python scripts/run_phase3_experiments.py --exp 8a
```
*Output Artifacts:* `results/passF/benchmark_matrix_passF.csv` and `results/exp3_cohirf_benchmark.csv`.

### 4.3 Feature Gating & Anchor Selection Ablations (Tables 16, 17, 18)
To reproduce the matched random-gating ablation (Exp 8c) and anchor selection ablation (Exp 8b):
```bash
python scripts/run_phase3_experiments.py --exp 8b
python scripts/run_phase3_experiments.py --exp 8c
```
*Output Artifacts:* `results/exp8b_anchor_selection.csv` and `results/exp8c_feature_gating.csv`.

### 4.4 Untraced Computational Scalability (Table 6)
To reproduce pure untraced wall-clock execution times and tracemalloc memory profiles ($N \in [500, 10{,}000]$):
```bash
python scripts/run_untraced_scalability.py
```
*Output Artifact:* `results/scalability_untraced_raw.csv`.

---

## 5. Statistical Calculations & Macro Validation

To recompute all non-parametric Friedman tests, Nemenyi critical differences, and bootstrap confidence intervals, and verify them against manuscript macros:
```bash
python tools/check_consistency.py
python -m pytest tests/test_macro_consistency.py
python -m pytest tests/test_pdf_allowlist.py
```
*Expected Result:* All consistency checks pass cleanly with zero discrepancies.

---

## 6. Compiling the Manuscript PDF

To compile the LaTeX source into the final camera-ready PDF using the bundled Tectonic engine:
```bash
tools/bin/tectonic.exe paper/main.tex
```
*Output:* `paper/main.pdf` (43 pages, Springer Nature `sn-jnl.cls` style).

To regenerate all submission bundles:
```bash
python scripts/build_all_submission_packages.py
```
This refreshes all `.zip` and `.tar.gz` packages under `submission/`.
