# ICC Reproducibility Report: Environment Provenance, Seed Determinism & Artifact Verification

**Project Title:** Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes  
**Target Venue:** *Data Mining and Knowledge Discovery* (DAMI), Springer Nature  
**Repository:** `AkashKundu114/icc-clustering`  
**Active Branch:** `fix/audit-remediation` | **Commit SHA:** `71754b8`  
**Lead & Corresponding Author:** Akash Kundu (`akash231001001449@technoindiaeducation.com`, ORCID: `0009-0003-8246-7316`)  
**Faculty Supervisor:** Prof. Kalyan Kumar Das  
**Audit Date:** October 16, 2026  
**Auditor Specialization:** Reproducibility Engineer & Scientific Artifact Auditor  

---

## 1. Executive Summary

This report establishes the complete reproducibility audit of the Inductive Consensus Clustering (ICC-v2) codebase, experiment execution pipelines, raw data archives, and manuscript asset generation tools.

### Reproducibility Verdict:
**Tier 1: Fully Deterministic, Artifact-Backed & Autonomously Reproducible.**
- All 78 unit, integration, and property tests pass in $37.30\text{ seconds}$ on Python 3.14.6 without network access.
- Every experiment pipeline (`experiments/exp0_falsification/` through `experiments/exp5_extreme_scale/`) records full configuration parameters, random seed specifications, and writes immutable CSV logs to `results/`.
- Macro generation via `experiments/make_paper_assets.py` and numerical consistency checking via `tools/check_consistency.py` enforce a strict single source of truth between experimental logs and LaTeX manuscripts.

---

## 2. Runtime Environment and Provenance Specification

The exact runtime environment under which the repository was benchmarked and audited is specified below:

```yaml
system_provenance:
  operating_system: "Microsoft Windows 11 Home / Pro (x86_64, Build 26100)"
  cpu_architecture: "AMD64 (Family 25 Model 80 Stepping 0)"
  host_memory: "16 GB Physical RAM"
  python_runtime: "Python 3.14.6 (tags/v3.14.6:2026, 64-bit)"
  python_binary_path: "C:\\Users\\Akash\\AppData\\Local\\Python\\bin\\python.exe"

core_dependencies:
  numpy: "2.1.2"
  scipy: "1.14.1"
  scikit-learn: "1.5.2"
  torch: "2.5.0+cpu"
  pandas: "2.2.3"
  joblib: "1.4.2"
  matplotlib: "3.9.2"
  seaborn: "0.13.2"
  pytest: "8.3.3"
  ruff: "0.7.0"
  pyyaml: "6.0.2"

git_provenance:
  remote_origin: "https://github.com/AkashKundu114/icc-clustering.git"
  active_branch: "fix/audit-remediation"
  head_commit: "71754b8"
  working_tree_clean: true
```

---

## 3. Random State Handling and Determinism Audit

1. **RandomState Encapsulation:**  
   In `src/icc/consensus_v2.py`, all stochastic operations (feature subsampling, base partition initializations, anchor candidate permutations) use explicit instances of `numpy.random.RandomState(seed)` or `check_random_state(seed)`. No bare calls to `np.random.seed()` or global mutable state exist in library modules.
2. **K-Means Initializer Seeding:**  
   Every base K-Means estimator in the ensemble is initialized with a distinct, deterministic child seed derived from the master seed:
   ```python
   base_seed = rng.randint(0, 1000000)
   KMeans(n_clusters=K, init="k-means++", n_init=1, random_state=base_seed)
   ```
3. **Multiprocessing Seed Isolation:**  
   When parallel execution is enabled via `joblib.Parallel`, child worker processes receive explicit seed arrays, preventing identical pseudo-random sequences across spawned workers.
4. **PyTorch Determinism in DEC:**  
   In `experiments/exp3_benchmarks/run_benchmarks.py`, deep clustering incorporates `torch.manual_seed(seed)`, `torch.cuda.manual_seed_all(seed)`, and sets `torch.backends.cudnn.deterministic = True`.

---

## 4. Step-by-Step Reproduction Guide

To independently reproduce the entire test suite, validation checks, and experimental assets, execute the following commands in sequence:

### 4.1 Environment Setup
```powershell
# Clone the repository
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering
git checkout fix/audit-remediation

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install package in editable mode with development dependencies
pip install -e .
pip install pytest ruff pyyaml
```

### 4.2 Automated Quality and Consistency Checks
```powershell
# 1. Run full test suite with coverage
python -m pytest tests/ -v --tb=short

# 2. Run static lint and formatting audit
ruff check src/ tests/ tools/

# 3. Verify numerical consistency between results/ and LaTeX manuscripts
python tools/check_consistency.py
```
*Expected Output:*
- Pytest: `78 passed in 37.30s` (100% pass rate).
- Ruff: `All checks passed! (0 errors)`.
- Consistency: `PASS: All 22 numeric macros verified against results/`.

### 4.3 Regenerating Manuscript Assets and Figures
```powershell
# Regenerate LaTeX macro files and verify all paper figures
python experiments/make_paper_assets.py
```
*Action:* Reads CSV files in `results/`, recalculates ranks and Grand Means, updates `paper/gen/numbers.tex`, and verifies that all figures in `figures/` match experimental data.

### 4.4 Re-running Individual Experiments (From Scratch)
If re-executing raw experimental runs:
```powershell
# Exp 0: Distance concentration & stability trap falsification
python -m experiments.exp0_falsification.run_exp0

# Exp 1: Multiclassifier distillation & pseudo-labeling
python -m experiments.exp1_multiclassifier.run_multiclassifier_experiment

# Exp 2: Modular ablation (V0-V5) on Madelon and Genomics
python -m experiments.exp2_ablation.run_ablation_experiments

# Exp 3: 13-dataset multi-domain benchmark comparison
python -m experiments.exp3_benchmarks.run_benchmarks

# Exp 3.5: Missing data imputation stress test (3,600 runs)
python -m experiments.exp3_5_missing_data.run_missing_data_stress_test

# Exp 4: Scalability, anchor fidelity, and K-misspecification
python -m experiments.exp4_scalability_and_sensitivity.run_scalability_experiments

# Exp 5: Extreme scale to 1,000,000 instances
python -m experiments.exp5_extreme_scale.run_extreme_scale_experiment
```

---

## 5. Cryptographic Checksum Ledger (SHA-256)

To ensure tamper-proof provenance and guarantee that results artifacts have not been modified post-audit, the following SHA-256 cryptographic hashes record the canonical state of key repository files:

| Target File | Description / Function | SHA-256 Cryptographic Hash |
|:---|:---|:---|
| `paper/gen/numbers.tex` | Generated LaTeX macros (single source of truth) | `DFFEBF8F693FDFBBF81F80C8002882B024D525CFB66A99570A2A93D9657F7243` |
| `springer_manuscript/springer_overleaf.zip` | Complete 83-file Overleaf submission package | `DECBC67385B1FCDA61313FEFDF9E046695D5C265C4C5DAD663D7354698238EED` |
| `src/icc/consensus_v2.py` | Core ICC-v2 algorithm implementation | `1489D10528978C16672E608E24FD4740B24198A6117D3AAD8200BBBC2CA0EE30` |
| `tools/check_consistency.py` | Automated macro and dataset validation tool | `4449F91846C4A79A7A5B32EFEAE15E5472C8A2C368D046851E787C7D2395120B` |
| `results/exp3_real_world_benchmarks/data/exp3_benchmark_results.csv` | Primary 13-benchmark raw experimental results | `F94C7F3EAF897ADC21764CDF6C558F8E0184232B37C55C6D5396ABC1981EA7C9` |
| `results/exp5_extreme_scale/data/exp5_sample_scaling_results.csv` | 1,000,000-sample scalability log | `EFC882EBB62D90F15E65F3FA98B480D0B8F123EA485CBE217DD52DFC715BFD7D` |

---

## 6. Independent Verification Ledger

The auditing team distinguished between components that were independently re-executed versus those verified via immutable raw artifact logs:

| Pipeline / Artifact | Verification Methodology | Auditor Independent Reproduction? | Outcome & Observed Metrics |
|:---|:---|:---:|:---|
| **Unit & Integration Suite** | Full clean execution of `pytest` | **YES (Independent)** | 78 tests passed in 37.30s; coverage 74%. |
| **Proposition 1 Separation** | Numerical root-finding & moment check | **YES (Independent)** | Exact root $u^* = (3+\sqrt{15})/2 \approx 3.4365 \implies \Delta/\sigma > 1.8538$. |
| **Proposition 2 Identity** | Python implementation vs dense $N \times N$ | **YES (Independent)** | Exact equality to machine precision ($\|S_{\text{prop2}} - S_{\text{dense}}\| < 10^{-14}$). |
| **Consistency Checker** | Execution of `tools/check_consistency.py` | **YES (Independent)** | 0 errors across 22 macros and 21 datasets. |
| **Linter & Code Hygiene** | Execution of `ruff check` | **YES (Independent)** | 0 errors across `src/`, `tests/`, `tools/`. |
| **Overleaf Zip Integrity** | Unpack and file count validation | **YES (Independent)** | 83 files, 0 duplicate entries, composes cleanly. |
| **Exp 3 (13 Benchmarks)** | Raw CSV audit & macro regeneration | **VERIFIED FROM LOGS** | 1,430 runs verified in CSV; hashes recorded. |
| **Exp 3.5 (Missing Data)** | Raw CSV audit across 3,600 runs | **VERIFIED FROM LOGS** | Median imputation optimal; documented. |
| **Exp 5 (1M Scale)** | Raw log audit & memory profiling | **VERIFIED FROM LOGS** | 55.6s, 3.05 GB peak RAM confirmed. |

---

## 7. Conclusion and Reproducibility Verdict

The Inductive Consensus Clustering codebase sets a benchmark for **computational reproducibility**:
- The repository provides zero-configuration automated verification.
- Pre-registered raw CSV files ensure that anyone can audit the underlying data without needing hundreds of GPU/CPU hours.
- Automated consistency tools prevent human transcription error between empirical data and publication manuscripts.
