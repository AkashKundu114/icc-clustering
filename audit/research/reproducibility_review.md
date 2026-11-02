# ICC-Clustering Reproducibility and Benchmark Infrastructure Audit

**Auditor:** QA & Reproducibility Specialist  
**Execution Environment:** Python 3.14.6, pytest-9.1.1, Windows Platform  
**Test Suite Status:** 126 passed, 0 failed, 0 skipped in 69.51s (100% pass rate)

---

## 1. Executive Summary

A comprehensive audit was conducted covering the entire testing framework (20 test files across unit, integration, and regression tiers), benchmark orchestration pipelines (`src/icc/benchmarks/`, `scripts/`), and experiment configuration schemas (`configs/`).

While the repository demonstrates strong unit test coverage and clean mathematical fallbacks, the audit identified **six critical reproducibility risks and profiling methodology flaws** that affect benchmark timing accuracy, hyperparameter propagation, and reproduction automation.

---

## 2. Findings Taxonomy and Reproducibility Risk Summary

| Finding ID | Domain | Severity | Affected File / Line | Fact vs. Inference | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AUD-REPRO-001** | Profiling Flaw: Memory Tracking Active During Wall-Clock Timing | **High** | `src/icc/benchmarks/scaling.py:43-57`<br>`src/icc/benchmarks/fidelity.py:113-127` | Verified Fact | Open |
| **AUD-REPRO-002** | Config Disconnect: `BenchmarkRunner` Ignores Model Hyperparameters | **High** | `src/icc/benchmarks/runner.py:121-127`<br>`configs/default.yaml` | Verified Fact | Open |
| **AUD-REPRO-003** | Incomplete Reproduction Script (`reproduce.py` Exits 0 on Tables/Figures/Full) | **High** | `scripts/reproduce.py:32-34` | Verified Fact | Open |
| **AUD-REPRO-004** | Tautological Test Assertions Providing Zero Defect Detection | **Medium** | `tests/integration/test_cohort_provenance.py:36,50`<br>`tests/regression/test_theory_boundaries.py:29-37` | Verified Fact | Open |
| **AUD-REPRO-005** | Deep Baseline Framework Divergence (PyTorch on GPU vs TensorFlow on CPU) | **Medium** | `src/icc/baselines/deep.py:433-445` | Verified Fact | Open |
| **AUD-REPRO-006** | Hardcoded Random Seed in Dataset Row Subsampling | **Low** | `src/icc/datasets/genomics.py:156` | Verified Fact | Open |

---

## 3. Detailed Technical Findings

### AUD-REPRO-001: Profiling Methodology Flaw — Memory Tracking Active During Timing Passes
- **Severity:** High
- **Affected Files:**
  - `src/icc/benchmarks/scaling.py:43-57`
  - `src/icc/benchmarks/fidelity.py:113-127`
- **Fact vs. Inference:** [Verified Fact].
- **Problem Analysis:**
  In `scaling.py`:
  ```python
  def benchmark_model_execution(model_name, model_fn, X, k, seed=42):
      tracemalloc.start()
      t0 = time.perf_counter()
      try:
          pred, elapsed, lc = model_fn(X, k, seed=seed)
          t_total = time.perf_counter() - t0
          current, peak = tracemalloc.get_traced_memory()
      finally:
          tracemalloc.stop()
      return t_total, peak_mb, lc, oom
  ```
  `tracemalloc.start()` intercepts all internal memory allocations (`PyMem_Malloc`). Running memory tracing concurrently with wall-clock timing introduces 20% to 100% CPU overhead depending on array allocation frequency.
  This directly contradicts `tests/regression/test_scaling_timing.py:101`, which asserts:
  > *"tracemalloc must remain inactive during pure timing pass... Traced memory in a dedicated separate pass."*
- **Actionable Remediation Guidance:**
  Separate memory profiling from runtime benchmarking into two distinct sequential passes:
  1. **Pass 1 (Timing):** Run `model_fn` with `tracemalloc` completely stopped; measure pure execution runtime.
  2. **Pass 2 (Memory):** In a separate invocation, start `tracemalloc`, execute `model_fn`, record peak RAM, and stop `tracemalloc`.

---

### AUD-REPRO-002: Hyperparameter Disconnect in `BenchmarkRunner`
- **Severity:** High
- **Affected Files:** `src/icc/benchmarks/runner.py:121-127`, `configs/default.yaml:26-36`
- **Fact vs. Inference:** [Verified Fact].
- **Problem Analysis:**
  `BenchmarkRunner.run_single` instantiates `InvariantCoreConsensusV2`:
  ```python
  if algorithm_name in ("icc_v2", "icc", "gac"):
      model = InvariantCoreConsensusV2(
          n_clusters=k,
          random_state=seed,
      )
      labels = model.fit_predict(X)
  ```
  It completely ignores model hyperparameter blocks specified in configuration files (`configs/default.yaml` defines `n_anchors: 50`, `subspace_rate: 0.25`, `core_quantile: 0.50`). The model is always instantiated with default constructor values (`n_anchors=40`, `subspace_rate=0.30`).
- **Actionable Remediation Guidance:**
  Pass configuration parameters into the model constructor:
  ```python
  icc_kwargs = self.config.get("icc_v2", {})
  model = InvariantCoreConsensusV2(
      n_clusters=k,
      random_state=seed,
      **icc_kwargs,
  )
  ```

---

### AUD-REPRO-003: Non-Functional Reproduction Scopes in `scripts/reproduce.py`
- **Severity:** High
- **Affected File:** `scripts/reproduce.py:32-35`
- **Fact vs. Inference:** [Verified Fact].
- **Problem Analysis:**
  Lines 32–34 handle `--scope tables`, `--scope figures`, and `--scope full`:
  ```python
  else:
      print(f"[*] Scope '{args.scope}' executed.")
      sys.exit(0)
  ```
  Executing `python scripts/reproduce.py --scope full` outputs a success message and exits `0` immediately without executing experiments, running benchmarks, or generating tables.
- **Actionable Remediation Guidance:**
  Implement functional CLI pipelines executing `scripts/run.py` and `scripts/evaluate.py --output-csv` to regenerate benchmark summary tables.

---

### AUD-REPRO-004: Tautological Test Assertions
- **Severity:** Medium
- **Affected Files:**
  - `tests/integration/test_cohort_provenance.py:36-47`
  - `tests/integration/test_cohort_provenance.py:50-57`
  - `tests/regression/test_theory_boundaries.py:29-37`
- **Fact vs. Inference:** [Verified Fact].
- **Problem Analysis:**
  1. `test_independent_benchmark_cohorts`:
     `assert cohort in registered or cohort in benchmark_cohorts` evaluates to `assert cohort in registered or True`, which is guaranteed to pass unconditionally.
  2. `test_rejection_of_low_dimensional_controls`: Asserts `assert 10 < 50` and `assert 6 < 50` on hardcoded integers.
  3. `test_proposition_one_analytical_bound`: Asserts `bound = 1.853778; assert np.isclose(bound, 1.854)` without executing any mathematical formula or distribution sampling.
- **Actionable Remediation Guidance:**
  Replace tautologies with meaningful assertions verifying that the dataset registry contains required cohorts, and simulating bimodal Gaussian transitions to confirm the analytical separation boundary.

---

### AUD-REPRO-005: Deep Baseline Framework Divergence
- **Severity:** Medium
- **Affected File:** `src/icc/baselines/deep.py:433-445`
- **Fact vs. Inference:** [Verified Fact].
- **Problem Analysis:**
  `run_dec` branches dynamically:
  - If CUDA GPU is available $\implies$ runs `_run_dec_torch_gpu` (PyTorch).
  - If CPU $\implies$ runs `_import_deep_backend` (TensorFlow/Keras).
  PyTorch and TensorFlow have different layer weight initializations, optimizer implementations, and float precision behaviors, introducing hardware-dependent numerical variance.
- **Actionable Remediation Guidance:**
  Standardize `run_dec` on PyTorch for both CPU and GPU execution.

---

### AUD-REPRO-006: Hardcoded Seed in Dataset Subsampling
- **Severity:** Low
- **Affected File:** `src/icc/datasets/genomics.py:156`
- **Fact vs. Inference:** [Verified Fact].
- **Problem Analysis:**
  When loading genomics datasets requiring row subsampling (e.g. Madelon, $N=500$), the row subsampler uses hardcoded `rng = np.random.default_rng(42)`. Multi-seed benchmarks evaluate identical sample rows rather than independent random subsamples.
- **Actionable Remediation Guidance:**
  Accept `seed: int = 42` in `load_dataset` and propagate it to `np.random.default_rng(seed)`.
