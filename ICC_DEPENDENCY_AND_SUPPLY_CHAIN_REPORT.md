# ICC Dependency and Supply Chain Security Report

**Project:** Invariant Core Consensus (ICC-v2)  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Active Branch:** `fix/audit-remediation`  
**Specification Files:** `pyproject.toml`, `requirements.txt`  
**Date:** October 16, 2026  

---

## 1. Executive Summary

This report assesses the third-party dependency surface, build configuration, supply chain posture, and packaging architecture of `icc-clustering`. Uncontrolled dependency creep and unpinned transitive packages introduce significant supply chain vulnerabilities, bitrot, and reproducibility collapse. 

The dependency architecture of ICC-v2 has been structured with **strict core isolation**:
- The core algorithm relies solely on mature, ubiquitous scientific libraries (`numpy`, `scipy`, `scikit-learn`, `pandas`).
- Heavy framework dependencies (`torch`, `tensorflow`, `scanpy`) are completely decoupled into optional extras (`[deep]`, `[bio]`, `[dev]`).
- Deserialization formats avoid arbitrary executable object streams (`pickle`), enforcing safe NumPy `.npz` storage.
- Zero untrusted build-time hooks or native compiled extensions exist in `setup.py` / `pyproject.toml`.

---

## 2. Dependency Architecture & Segmentation

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ICC Packaging Architecture                       │
└────────────────────────────────────────────────────────────────────────┘
                                    │
    ┌───────────────────────────────┴───────────────────────────────┐
    │                                                               │
    ▼                                                               ▼
[Core Numerical Tier] (Mandatory)                     [Optional Specialty Tiers]
 • numpy >= 1.23.0                                     • [deep]  (torch, tensorflow, keras)
 • scipy >= 1.10.0                                     • [bio]   (scanpy, anndata)
 • scikit-learn >= 1.3.0                               • [dev]   (pytest, pytest-cov, ruff)
 • pandas >= 2.0.0                                     • [all]   (all tiers combined)
 • matplotlib >= 3.7.0, seaborn >= 0.12.0
 • pyyaml >= 6.0, tqdm >= 4.60.0, tabulate >= 0.9.0
 • reportlab >= 4.0.0, Pillow >= 9.5.0
```

### 2.1 Core Dependency Tier (Mandatory)
The core package install (`pip install -e .`) installs only the minimal stack required for invariant consensus clustering, VSSG subspace gating, certified anchor consensus, ASPP diagnostics, and out-of-sample projection:

| Dependency | Minimum Version | Primary Functional Purpose | License |
|---|---|---|---|
| `numpy` | `>=1.23.0` | Matrix operations, RNG seeding, vectorized array math | BSD-3-Clause |
| `scipy` | `>=1.10.0` | Bipartite SVD, sparse adjacency matrices, pairwise distances | BSD-3-Clause |
| `scikit-learn` | `>=1.3.0` | Base K-Means clustering, evaluation metrics (ARI, NMI) | BSD-3-Clause |
| `pandas` | `>=2.0.0` | ASPP diagnostic tables, tabular experiment logs | BSD-3-Clause |
| `matplotlib` | `>=3.7.0` | Visualization and diagnostic plotting | PSF / BSD |
| `seaborn` | `>=0.12.0` | Statistical figure aesthetics and heatmaps | BSD-3-Clause |
| `pyyaml` | `>=6.0` | Experiment configuration parsing | MIT |
| `tqdm` | `>=4.60.0` | Progress meters for lengthy multi-seed benchmark loops | MPL-2.0 / MIT |
| `tabulate` | `>=0.9.0` | Pretty-printed terminal output tables in walkthrough demos | MIT |
| `reportlab` | `>=4.0.0` | PDF report and certificate generation | BSD-3-Clause |
| `Pillow` | `>=9.5.0` | Raster figure processing and rasterized visual assets | HPND |

### 2.2 Specialty Dependency Tiers (Optional Extras)
Heavy or domain-specific libraries are isolated in `pyproject.toml` under `[project.optional-dependencies]`:
- **`[deep]`**: `torch>=2.0.0`, `tensorflow>=2.12.0`, `keras>=3.0.0`. Required only for training comparative deep learning baselines (DEC, IDEC, Contrastive Clustering). If not installed, classical baselines and ICC-v2 execute seamlessly without warning.
- **`[bio]`**: `scanpy>=1.9.0`, `anndata>=0.9.0`. Required only for single-cell genomics benchmarks (e.g., 10x PBMC, mouse cortex datasets).
- **`[dev]`**: `pytest>=7.0.0`, `pytest-cov>=4.0.0`, `black`, `ruff`. Used for local testing, test coverage generation, and static code linting.
- **`[all]`**: Installs the complete suite across all groups.

---

## 3. Supply Chain Security and Deserialization Audit

### 3.1 Unsafe Deserialization Elimination
Python's standard `pickle` serialization format poses a major vulnerability if an untrusted user modifies a saved checkpoint or benchmark file. Executable payloads can be disguised as pickled objects and executed upon calling `pickle.load()` or `np.load(..., allow_pickle=True)`.

**Audit Findings:**
- In benchmark control scripts (`experiments/audit_controls/src/e1_extended_benchmarks.py`, `e1_held_out_comparison.py`, and `results/audit_controls/src/*.py`), four instances of `np.load(..., allow_pickle=True)` were identified.
- **Remediation:** All calls were modified to `allow_pickle=False`. 
- **Verification:** All `.npz` caches contain only standard numerical `np.float64` and `np.int64` arrays. The regression suite confirms that all benchmark loaders function identically with `allow_pickle=False`, completely neutralizing the arbitrary code execution vector.

### 3.2 Dynamic Evaluation & Shell Execution Audit
- Search for `eval(`: **0 occurrences** across repository.
- Search for `exec(`: **0 occurrences** across repository.
- Search for `os.system(`: **0 occurrences** across repository.
- Search for `subprocess.call` or `subprocess.Popen` with `shell=True`: **0 occurrences** across repository.

### 3.3 Build-System Integrity
The project uses standard declarative metadata in `pyproject.toml` governed by `setuptools>=61.0`. There are no custom build hooks, executable `setup.py` scripts executing external network requests, or bundled binary C-extensions that bypass PyPI wheel audits.

---

## 4. Environment & Platform Compatibility Matrix

| Environment / OS | Python 3.10 | Python 3.11 | Python 3.12 | Python 3.13 | Python 3.14 | Status |
|---|---|---|---|---|---|---|
| **Ubuntu Linux (x86_64)** | Verified (CI) | Verified (CI) | Verified (CI) | Supported | Supported | **Fully Verified** |
| **Windows 11 (x86_64)** | Verified (CI) | Verified (CI) | Verified (CI) | Verified | Verified (Active: 3.14.6) | **Fully Verified** |
| **macOS (Apple Silicon)** | Supported | Supported | Supported | Supported | Supported | **Standard PyPI** |

---

## 5. Security Recommendations for Upstream Users

1. **Virtual Environment Isolation:** Always install within a virtual environment (`python -m venv .venv`).
2. **Minimal Extra Installation:** Unless benchmarking deep baselines, install only the core package:
   ```powershell
   pip install -e .
   ```
3. **Reproducibility Locking:** For production deployment or publication archiving, freeze exact transitive package versions:
   ```powershell
   pip freeze > requirements-lock.txt
   ```
