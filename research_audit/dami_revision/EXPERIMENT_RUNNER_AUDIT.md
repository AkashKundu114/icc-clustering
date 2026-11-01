# Experiment Execution Runners and Orchestration Audit Report

**Author:** Agent F — Experiment Execution, Runners, and Reproducibility Auditor  
**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Repository Branch:** `research/dami-revision`  
**Governing Documents:**
- [`EXPERIMENT_MANIFEST_SCHEMA.json`](file:///d:/Final%20Year%20Project/research_audit/dami_revision/EXPERIMENT_MANIFEST_SCHEMA.json)
- [`REPRODUCIBILITY_AND_EXECUTION_REPORT.md`](file:///d:/Final%20Year%20Project/research_audit/dami_revision/REPRODUCIBILITY_AND_EXECUTION_REPORT.md)

---

## 1. Executive Summary & Audit Scope

This audit performs an exhaustive, code-level inspection of every execution runner, launcher script, and orchestration pipeline in the repository. The objective is to identify vulnerabilities in execution determinism, hardware contention, seed propagation, error handling, floating-point serialization, and metadata tracking prior to confirmatory execution.

### Key Audit Findings:
1. **Asymmetric Error Handling:** In `experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py`, failed algorithm runs silently impute zero labels (`np.zeros(N)`) and assign `ari: 0.0`, whereas `experiments/exp7_modern_baselines/src/run_exp7.py` assigns `ari: np.nan`. Setting failed runs to 0.0 artificially drags down algorithm averages, while `np.nan` excludes them, distorting comparative baselines.
2. **Missing Atomic Flushing in EXP7:** `run_exp7.py` buffers all 300 trial results in memory and writes to disk only upon final script completion. Any unhandled exception, SIGINT, or out-of-memory (OOM) event terminates the script with complete data loss.
3. **Absence of Hardware and Environment Manifests:** None of the existing runners capture hardware architectures (CPU instruction sets, AVX2/AVX-512), GPU driver/CUDA versions, BLAS/LAPACK backend implementations (OpenBLAS vs. Intel MKL), or git commit hashes in their output data records.
4. **Thread Contention in Multiprocessing:** Several baseline implementations (Spectral Clustering, K-Means via scikit-learn, FastMVC) spawn internal OpenMP/BLAS worker threads without setting `OMP_NUM_THREADS=1` or `MKL_NUM_THREADS=1`, inducing core over-subscription and CPU cache thrashing during concurrent batch executions.

---

## 2. Exhaustive Runner Inspection Matrix

| Runner Script | Primary Purpose | CLI Invocations & Arguments | Seed Schedule & Propagation | Input / Output File Paths | Failure & Crash Handling | Serialization Format |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`run_exp3_1_benchmark_matrix.py`** | 13-Dataset Multi-Domain Benchmark Matrix (11 Models x 10 Trials) | `python -m experiments.exp3_real_world_benchmarks.src.run_exp3_1_benchmark_matrix` (No CLI args parsed; defaults hardcoded) | `SEEDS = [42, 101, 202, 303, 404, 505, 606, 707, 808, 909]`. Seed passed explicitly to model function. | Input: `icc.datasets.registry.load_dataset(dname)`<br>Output: `exp3_1_benchmark_matrix_v2.csv` | Traps exception in inner loop; sets `pred = np.zeros(N)` and `ari = 0.0`. Incremental CSV write on each trial. | CSV (ASCII floats, standard `pandas.to_csv`). No git commit or host metadata. |
| **`run_exp3_2_noise_stress_test.py`** | Feature Noise & Perturbation Stress Testing | `python -m experiments.exp3_real_world_benchmarks.src.run_exp3_2_noise_stress_test` | Hardcoded trial seeds 0–9. Passed to synthetic generator and models. | Input: Dataset registry or Gaussian noise injector<br>Output: `exp3_2_noise_stress_test.csv` | Try/except records error message in log; continues to next trial. | CSV (Real-time append). |
| **`run_exp3_3_inductive_real_world.py`** | Inductive Out-of-Sample Core Projection Evaluation | `python -m experiments.exp3_real_world_benchmarks.src.run_exp3_3_inductive_real_world` | Explicit train/test random split seeds (5-fold stratified). | Input: Registry datasets<br>Output: `exp3_3_inductive_real_world.csv` | Traps fit failures; logs warning and returns NaN predictions. | CSV. |
| **`run_exp3_4_statistical_significance.py`** | Post-hoc Wilcoxon Signed-Rank & p-value Calculation | `python -m experiments.exp3_real_world_benchmarks.src.run_exp3_4_statistical_significance` | Deterministic paired statistical calculations; no random seeds. | Input: `exp3_1_benchmark_matrix_v2.csv`<br>Output: `exp3_4_significance_results.csv` | Crashes on missing datasets or NaN values unless cleaned. | CSV + Formatted LaTeX summary strings. |
| **`run_exp7.py`** | Modern Baselines Benchmark (HDBSCAN, Leiden, Sparse K-Means, GMM) | `python experiments/exp7_modern_baselines/src/run_exp7.py` | `SEEDS = [42, 43, 44, 45, 46]` (5 seeds across 6 biological cohorts). | Input: `icc.datasets.registry.load_dataset`<br>Output: `modern_baselines_benchmark.csv` | Traps exceptions per model run; records `status = f"ERROR: {e}"` and `np.nan`. **No incremental disk flush**; writes df at exit. | CSV (`pandas.to_csv(index=False)`). |
| **`run_unknown_k.py`** (EXP8) | Model Order Selection ($K$ Unknown Sweep $K \in [2, 10]$) | `python experiments/exp8_unknown_k/src/run_unknown_k.py` | Fixed seeds per dataset run. | Input: Synthetic & Real datasets<br>Output: `unknown_k_real_results.csv` | Partial progress buffered in memory; flushed per dataset. | CSV. |
| **`run_confirmatory_grid.py`** (Study Null Gating) | Confirmatory Gating Grid & Matched-Random Controls | `python experiments/study_null_gating/run_confirmatory_grid.py` | Seed schedule mapped from configuration dictionary. | Input: Pre-downloaded GEO cache arrays<br>Output: `results/confirmatory_grid.csv` | Structured exception logger; writes intermediate checkpoints to `.npy`. | CSV + NumPy `.npy` checkpoints. |

---

## 3. Forensic Code-Level Deficiencies in Existing Runners

### 3.1 Defect 1: Error Imputation Discrepancy (Zero vs. NaN)
- **Location:** `experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py:423-429`
  ```python
  except Exception as e:
      print(f"\n[!] Error running {mname} on {dname} (trial {t_idx}): {e}")
      # In case of algorithm failure, record null predictions
      pred = np.zeros(N, dtype=int)
      elapsed_sec = 0.0
      lc = 0
      scores = {"ari": 0.0, "nmi": 0.0, "ami": 0.0, "v_measure": 0.0, "fm_index": 0.0}
  ```
- **Methodological Problem:** When a method crashes (e.g., FastMVC singularity or DEC out-of-memory), recording $\text{ARI} = 0.0$ treats a non-convergent or failed run as equivalent to an empirical clustering result that performed at chance level. However, pure chance clustering can yield negative ARI values (down to $-0.5$). Furthermore, setting runtime to $0.0$ seconds artificially deflates computational cost metrics.
- **Mandatory Remediation:** Failed runs must record `status = "FAILED"`, `ari = np.nan`, and the exact exception traceback. In the statistical evaluation protocol, algorithm non-convergence must be analyzed as a distinct failure rate metric rather than silently folded into performance distributions.

### 3.2 Defect 2: In-Memory Accumulation Without Atomic Flushes
- **Location:** `experiments/exp7_modern_baselines/src/run_exp7.py:117-124`
  ```python
  df = pd.DataFrame(records)
  df.to_csv(output_csv, index=False)
  ```
- **Execution Problem:** 300 computationally intensive runs (particularly Sparse K-Means and GMM sweeps on $D=15{,}154$) execute over several hours. If a power outage, process kill, or memory spike occurs on run 299, zero records are saved.
- **Mandatory Remediation:** Adopt the atomic file-append pattern with file locking or SQLite journal logging, writing each trial to disk immediately upon completion.

### 3.3 Defect 3: Lack of Command-Line Argument Parameterization
- **Audit Observation:** Neither `run_exp3_1_benchmark_matrix.py` nor `run_exp7.py` parses CLI arguments via `argparse` or `click`.
- **Reproducibility Problem:** To modify seeds, restrict runs to a specific cohort, or alter output file destinations, researchers must manually edit source code. This introduces substantial risk of uncommitted local modifications contaminating frozen repositories.
- **Mandatory Remediation:** Standardize all runner entry points to accept `--cohort`, `--models`, `--seeds`, `--output-dir`, and `--manifest-path` via standard POSIX CLI interfaces.

---

## 4. Environment and Hardware Determinism Audits

### 4.1 BLAS/LAPACK Threading and CPU Contention
- Clustering algorithms relying on matrix decomposition (Spectral Clustering, PCA-based GAC initializations, SVD) utilize underlying BLAS implementations (OpenBLAS, Intel MKL, or Apple Accelerate).
- By default, libraries such as NumPy and SciPy bind to all available logical CPU cores. If an outer experiment loop launches multiple concurrent processes or if threads contend for L3 cache, execution timing fluctuates by up to $300\%$, invalidating runtime benchmark comparisons.
- **Remediation Specification:** Every runner entry point must enforce single-thread mathematical execution at process initialization:
  ```python
  import os
  os.environ["OMP_NUM_THREADS"] = "1"
  os.environ["MKL_NUM_THREADS"] = "1"
  os.environ["OPENBLAS_NUM_THREADS"] = "1"
  os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
  os.environ["NUMEXPR_NUM_THREADS"] = "1"
  ```

### 4.2 Cross-Platform Floating-Point Non-Determinism
- **Linux (glibc) vs. Windows (MSVCRT) vs. macOS (Accelerate):** Transcendental functions (`exp`, `log`, `sin`) and floating-point summation orders differ across standard C runtimes.
- In K-Means and Spectral Clustering, minute differences in machine epsilon ($10^{-16}$) can flip cluster assignment for boundary samples, leading to divergent paths across $T=100$ ensemble iterations.
- **Remediation Specification:**
  - All experiment runs must record platform architecture (`platform.platform()`, `platform.processor()`, Python version, NumPy/SciPy versions).
  - Floating-point seeds must be initialized using `np.random.default_rng(SeedSequence(seed))` rather than legacy `np.random.seed(seed)`.

---

## 5. Experiment Manifest Architecture

To guarantee complete post-hoc auditability, all future experiment runners must generate an immutable `experiment_manifest.json` companion file alongside every CSV output.

The formal JSON Schema governing these manifests is implemented in:
[`EXPERIMENT_MANIFEST_SCHEMA.json`](file:///d:/Final%20Year%20Project/research_audit/dami_revision/EXPERIMENT_MANIFEST_SCHEMA.json)
