# ICC-v2 Public Release Audit (Phase A)

**Date:** 2026-10-17  
**Branch:** `release/public-cleanup`  
**Commit:** `fd6ff53` (Baseline recorded)  
**Auditor:** Subagent R (Orchestrated Release Audit)

---

## 1. Directory Tree & File Size Inventory

### 1.1 Overview
- **Total tracked files:** 572
- **Tracked files over 1 MB:** 26 files
- **Tracked files over 5 MB:**
  1. `manuscript/scripts/bin/tectonic.exe` (49.15 MB) — Standalone TeX binary engine.
  2. `experiments/exp3_real_world_benchmarks/data/cache/ovarian.npz` (26.42 MB) — Preprocessed benchmark cache.
  3. `springer_manuscript/springer_overleaf.zip` (21.75 MB) — Packaged submission zip.
  4. `manuscript/tkde_overleaf.zip` (21.66 MB) — Packaged submission zip.
  5. `manuscript/tkde_package.zip` (20.82 MB) — Packaged submission zip.
  6. `manuscript/icde_package.zip` (20.82 MB) — Packaged submission zip.
  7. `springer_manuscript/springer_nature_submission_package.zip` (20.80 MB) — Packaged submission zip.
  8. `springer_manuscript/main.pdf` (7.50 MB) — Compiled manuscript PDF.
  9. `paper/main.pdf` (7.44 MB) — Compiled manuscript PDF.
  10. `manuscript/tkde.pdf` (7.44 MB) — Compiled manuscript PDF.
  11. `manuscript/main.pdf` (7.44 MB) — Compiled manuscript PDF.
  12. `experiments/exp3_real_world_benchmarks/data/cache/prostate.npz` (5.23 MB) — Preprocessed benchmark cache.

### 1.2 Untracked Large Files
- `experiments/exp3_real_world_benchmarks/data/cache/newsgroups20.npz` (61.48 MB)
- `experiments/exp3_real_world_benchmarks/data/cache/lymphoma.npz` (25.45 MB)
- `data/cache/ovarian.npz` (26.42 MB)
- `experiments/exp3_real_world_benchmarks/data/cache/lung_cancer.npz` (18.45 MB)
- `data/cache/isolet.npz` (11.78 MB)
- `data/cache/newsgroups20.npz` (9.69 MB)
- `experiments/exp3_real_world_benchmarks/data/cache/isolet.npz` (8.19 MB)
- `experiments/exp3_real_world_benchmarks/data/cache/har.npz` (7.79 MB)
- `data/cache/indian_pines.npz` (6.53 MB)
- `data/raw/indian_pines/Indian_pines_corrected.mat` (5.68 MB)

*Policy & Gate Note:* Under Approval Gate 4, untracked generated caches are ignored by `.gitignore`. Large tracked binaries (`.zip`, `tectonic.exe`) are preserved unless user explicitly approves git history purge.

---

## 2. Secrets and Privacy Scan

### 2.1 Git History & Working Tree Secret Scan
- **Gitleaks / Regex Patterns Scanned:**
  - GitHub Personal Access Tokens (`ghp_*`, `github_pat_*`)
  - AWS Access Key IDs (`AKIA*`)
  - OpenAI / Anthropic API Keys (`sk-*`)
  - Slack Tokens (`xox*`)
  - JWT Tokens (`ey*`)
- **Result:** **0 secret patterns detected** across full commit history and working tree.

### 2.2 Privacy & Local Path Audit
- **Corresponding Author Emails Found:**
  - `akash231001001449@technoindiaeducation.com` (Author institutional email, present in `CITATION.cff`, `pyproject.toml`, `README.md`)
  - `akashkundu11522@gmail.com` (Author contact email in `CODE_OF_CONDUCT.md`, `README.md`)
  - `iauthor@gmail.com` (Standard template placeholder in Springer LaTeX source `sn-article.tex`)
- **Absolute Local Paths:**
  - `C:\Users\Akash\...` identified in `REMEDIATION/ENV.md` and captured log files (`REMEDIATION/logs/test_suite.log`, `exp0.log`, etc.). These document the empirical runtime environment per protocol.
  - Academic reference path: `/home/dengcai` in `src/icc/datasets/image.py` (Zhejiang University official Extended Yale B download URL: `http://www.cad.zju.edu.cn/home/dengcai/Data/YaleB/YaleB_32x32.mat`).

---

## 3. Dependency Inventory

### 3.1 Declared Core Dependencies (`pyproject.toml` / `requirements.txt`)
- `numpy>=1.23.0` (Used across 17 modules) — BSD-3-Clause
- `scipy>=1.10.0` (Used across 9 modules: SVD, distance, sparse matrices) — BSD-3-Clause
- `scikit-learn>=1.3.0` (Used across 11 modules: K-Means, metrics, preprocessing) — BSD-3-Clause
- `pandas>=2.0.0` (Result aggregation and table formatting) — BSD-3-Clause
- `matplotlib>=3.7.0` (Figure plotting) — PSF / Matplotlib
- `seaborn>=0.12.0` (Visualization aesthetics) — BSD-3-Clause
- `pyyaml>=6.0` (Dataset and baseline configuration loading) — MIT
- `tqdm>=4.60.0` (CLI progress tracking) — MIT / MPL-2.0
- `tabulate>=0.9.0` (Console summary formatting) — MIT

### 3.2 Optional Dependencies
- `torch>=2.0.0`, `tensorflow>=2.12.0`, `keras>=3.0.0` (Deep clustering baselines: DEC, IDEC, SCAN)
- `scanpy>=1.9.0`, `anndata>=0.9.0` (Single-cell RNA-seq benchmarks: Zheng68k, Tabula Muris)
- `pytest>=7.0.0`, `pytest-cov>=4.0.0`, `ruff`, `mypy` (Dev & CI testing)

---

## 4. Code-Quality & Architecture Inventory

### 4.1 Modules and Layout
- `src/icc/`:
  - `consensus_v2.py`: Core algorithm (`InvariantCoreConsensusV2`), anchor graph construction, Transfer-Cut bipartite SVD, out-of-sample prediction.
  - `consensus.py`: Legacy ICC-v1 implementation.
  - `aspp.py`: Adaptive Spectral Projection Perturbation filter (retained for backward compatibility and ablation).
  - `core.py`: Ensemble generators, co-association accumulation, partition generation.
  - `metrics.py`: ARI, NMI, AMI, V-Measure, Fowlkes-Mallows, Friedman/Nemenyi statistical tests.
  - `datasets/`: Domain loaders (`genomics.py`, `image.py`, `spectral.py`, `text.py`, `audio.py`, `scrnaseq.py`, `registry.py`).
  - `baselines/`: Classical (`classical.py`), anchor-based (`anchor.py`), consensus (`consensus.py`), deep (`deep.py`).
- **Public API Surface:**
  - `src/icc/__init__.py` exposes `InvariantCoreConsensusV2` (as well as `ICC` alias).
- **Quality Findings to Address in Phase B/C:**
  - Several modules contain `from src.icc...` imports instead of relative or package-relative `from icc...` imports, causing module duplication errors in mypy.
  - Public class `ICC` needs full scikit-learn standard conformance (`fit`, `predict`, `predict_proba`, `transform`, parameter validation).
  - Source files still contain inline explanatory `#` comments, which must be stripped per Rule 4, retaining only single-line docstrings on public APIs.

---

## 5. Data Inventory & Redistribution Status

| Dataset | Source | Redistribution / Licence Status | Action |
| :--- | :--- | :--- | :--- |
| `sonar` | OpenML (ID 40) / UCI | Public Domain (CC-BY-4.0 / Open Data) | Download script via OpenML |
| `madelon` | OpenML (ID 1485) / UCI | Public Domain (NIPS 2003 Feature Selection) | Download script via OpenML |
| `colon` | OpenML (Alon et al. 1999) | Academic Research Open Access | OpenML auto-fetch |
| `srbct` | OpenML (Khan et al. 2001) | Academic Research Open Access | OpenML auto-fetch |
| `cns` | OpenML (Pomeroy et al. 2002)| Academic Research Open Access | OpenML auto-fetch |
| `leukemia` | OpenML (Golub et al. 1999) | Academic Research Open Access | OpenML auto-fetch |
| `prostate` | OpenML (Singh et al. 2002) | Academic Research Open Access | OpenML auto-fetch |
| `ovarian` | OpenML (Petricoin et al. 2002)| Academic Research Open Access | OpenML auto-fetch |
| `newsgroups20`| scikit-learn / Tom Mitchell| Open Research Data | `fetch_20newsgroups` |
| `isolet` | OpenML (ID 300) / UCI | Public Domain | OpenML auto-fetch |
| `indian_pines`| Purdue University AVIRIS | NASA / Academic Public Use | Automated URL fetch |
| `yale_b` | ZJU / Georghiades et al. | Academic Research Use | Automated URL fetch |
| `zheng68k` | 10x Genomics (Zheng et al.) | Open Access Single-cell Dataset | `scanpy.datasets` fetch |

All datasets can be fetched on demand via `scripts/fetch_data.py`. No proprietary or non-redistributable datasets are bundled.

---

## 6. Reproducibility & Determinism Inventory

- **Host Specs:** Windows 11, Intel Core i7 (16 physical cores, 32 GB RAM).
- **Python Version:** 3.14.6 (64-bit).
- **Determinism Protocols:**
  - Random seeds controlled explicitly (`random_state` parameter across ensemble and anchor generation).
  - Multi-threaded BLAS/OpenMP nondeterminism controlled via environment flags: `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`.
- **Benchmark Runtimes:**
  - Smoke run (Toy + Leukemia seeds 0-2): ~5.2 seconds.
  - Full test suite (76 tests): ~38.9 seconds.

---

## 7. Baseline Checkpoint Verification (Gate A)

- **Test Suite:** `RELEASE/baseline/pytest_baseline.txt` (76 passed, 74% coverage).
- **Linter Output:** `RELEASE/baseline/ruff_baseline.txt` (460 findings captured).
- **Mypy Output:** `RELEASE/baseline/mypy_baseline.txt` (Captured duplicate module error).
- **Smoke Run Hashes:** Recorded in `RELEASE/baseline/smoke_baseline.json`:
  - `toy` labels SHA256: `813664b8a3fb86a5f6a32287f371bf569907b20ee94c449f83457f10fd14c29b`
  - `leukemia` seed 0 SHA256: `018085f09652f00685625c24e10e0a105a5bf74ee5671ff939918d7240d52383`
  - `leukemia` seed 1 SHA256: `ea87bd61348e7d86e55767c1a33ac99ca0f5469c5220337058ae4e554688793d`
  - `leukemia` seed 2 SHA256: `315034f7f22eaaa0416fb15dae06c75e983b172da0a2d5318d546d2dcc6a8c47`

**Gate A Status:** PASS. Baseline recorded. Proceeding to Phase B.
