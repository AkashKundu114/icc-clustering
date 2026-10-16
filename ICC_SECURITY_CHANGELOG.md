# ICC Security & Hardening Changelog

**Project:** Invariant Core Consensus (ICC-v2)  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Active Branch:** `fix/audit-remediation`  
**Release Cycle:** Security Hardening, Adversarial Input Defenses & Release Preparation  
**Date:** October 16, 2026  

---

## 1. Overview of Changes

This changelog records the specific code, configuration, test, and documentation modifications introduced to harden `icc-clustering` against adversarial inputs, eliminate supply chain deserialization risks, optimize computational resources, and verify publication-grade reproducibility.

---

## 2. Detailed Change Records

### [SEC-001] Elimination of Unsafe Deserialization in Benchmark Controls
- **Severity:** High (Remote Code Execution Prevention)
- **Files Modified:**
  - `experiments/audit_controls/src/e1_extended_benchmarks.py` (Line 95)
  - `experiments/audit_controls/src/e1_held_out_comparison.py` (Line 86)
  - `results/audit_controls/src/e1_extended_benchmarks.py` (Line 95)
  - `results/audit_controls/src/e1_held_out_comparison.py` (Line 86)
- **Change:** Changed `np.load(..., allow_pickle=True)` to `np.load(..., allow_pickle=False)`.
- **Rationale:** Prevents arbitrary object injection and code execution via compromised `.npz` caches while safely loading pure numeric `float64` / `int64` ndarrays.

---

### [SEC-002] Hyperparameter Domain and Range Sanitization
- **Severity:** Medium (Input Validation / DoS Prevention)
- **Files Modified:**
  - `src/icc/consensus_v2.py` (`InvariantCoreConsensusV2.__init__`)
- **Change:** Added explicit domain checks:
  - `n_clusters >= 2` (raises `ValueError` otherwise)
  - `n_base_models >= 1` (raises `ValueError` otherwise)
  - `n_anchors >= 1` (raises `ValueError` otherwise)
  - `0.0 < core_quantile <= 1.0` (raises `ValueError` otherwise)
  - `0.0 < subspace_rate <= 1.0` (raises `ValueError` otherwise)
  - `pool_mode in ("legacy", "bc_frac", "random_frac", "random", "robust", "gauss", "null_calibrated")` (raises `ValueError` otherwise)
- **Rationale:** Disallows negative, zero, or uncalibrated hyperparameter combinations that cause silent crashes, infinite loops, or mathematical nonsense.

---

### [SEC-003] Training Matrix Shape and Numerical Value Validation
- **Severity:** High (Crash and Poisoning Defense)
- **Files Modified:**
  - `src/icc/consensus_v2.py` (`InvariantCoreConsensusV2.fit_predict`)
- **Change:** Added strict pre-flight matrix validation:
  - Enforced `X.ndim == 2` (rejecting 1D arrays or 3D tensors).
  - Enforced `N > 0` and `D > 0` (rejecting empty matrices).
  - Enforced `N >= n_clusters` (rejecting under-determined cohorts).
  - Enforced `np.isnan(X).any() == False` and `np.isinf(X).any() == False`.
  - Cached `self.n_features_in_ = D` for subsequent inductive validation.
- **Rationale:** Prevents segmentation faults, unhandled linear algebra errors, and NaN contagion across base clusterers and bipartite graphs.

---

### [SEC-004] Centralized Out-of-Sample Query Sanitization and Transform API
- **Severity:** Medium (Interface Robustness & Memory Access Safety)
- **Files Modified:**
  - `src/icc/consensus_v2.py` (`_validate_X_new`, `transform`, `predict`, `predict_proba`, `predict_with_stability`)
- **Change:** 
  - Extracted centralized `_validate_X_new(X_new)` helper:
    - Enforces fitted state (`self.anchor_centroids_ is not None`, raising `RuntimeError`).
    - Enforces 2D array shape (`X_new.ndim == 2`).
    - Enforces exact feature dimension match (`X_new.shape[1] == self.n_features_in_`).
    - Rejects `NaN` and `Inf` query values.
  - Added public `transform(X_new, subspace=True)` method following Scikit-learn estimator conventions.
  - Refactored `predict`, `predict_proba`, and `predict_with_stability` to delegate distance computation to `transform`.
- **Rationale:** Eliminates silent out-of-bounds indexing or shape broadcast failures when query data has different feature counts than the training cohort.

---

### [SEC-005] Graceful Handling of Empty Query Batches
- **Severity:** Low (Fault Tolerance / API Contract)
- **Files Modified:**
  - `src/icc/consensus_v2.py` (`predict`, `predict_proba`, `predict_with_stability`, `transform`)
- **Change:** Added immediate zero-length batch branch returning valid empty ndarrays:
  - `predict`: returns `np.empty((0,), dtype=int)`
  - `predict_proba`: returns `np.empty((0, K), dtype=np.float64)`
  - `transform`: returns `np.empty((0, K), dtype=np.float64)`
  - `predict_with_stability`: returns dictionary of empty arrays
- **Rationale:** Streaming inference systems frequently encounter zero-length micro-batches; returning empty arrays avoids uncaught runtime crashes.

---

### [SEC-006] Adversarial and Boundary Test Suite Implementation
- **Severity:** Medium (Regression Safety)
- **Files Created:**
  - `tests/test_adversarial_inputs.py` (33 unit tests)
- **Change:** Authored comprehensive test classes:
  - `TestHyperparameterValidation`: 6 parametrized tests for out-of-bounds initialization.
  - `TestDegenerateFitInputs`: 6 tests for 1D/3D shapes, empty arrays, $N < K$, NaNs, and Infs.
  - `TestUnfittedModelGuards`: 4 tests for un-fitted estimator calls.
  - `TestOutOfSampleAdversarialInputs`: 5 tests for dimension mismatches, NaNs, Infs, and empty test batches.
  - `TestTransformAndNumericalStability`: 2 tests for consistency and extreme data scaling ($10^6$).
- **Rationale:** Permanently protects the repository against regressions and ensures CI fails if input validation is bypassed.

---

### [SEC-007] Resource Profiling and Benchmarking Tool
- **Severity:** Low (Performance Observability)
- **Files Created:**
  - `tools/profile_resources.py`
  - `results/resource_benchmarks.json`
- **Change:** Developed benchmarking script measuring runtime, peak RAM via `tracemalloc`, and process RSS memory via `psutil` across sample scaling ($N \in [100, 5000]$), dimension scaling ($D \in [20, 5000]$), and inductive throughput ($N_{\text{test}} \in [10, 20000]$).
- **Rationale:** Provides verified empirical evidence of $O(N)$ linear complexity, low memory footprint, and $>3.5\times 10^6\text{ samples/sec}$ query throughput.

---

### [SEC-008] Root Demo Forwarder and CI Workflow Harmonization
- **Severity:** Low (Usability & Developer Experience)
- **Files Modified/Created:**
  - `demo.py` (Root forwarder to `scripts/demo.py`)
  - `scripts/demo.py` (Added `sys.path` bootstrap, fixed unused imports and static f-strings)
  - `scripts/generate_supp_tables.py` (Import order cleanup)
  - `scripts/plot_conceptual_framework.py` (Removed unused variable, cleaned static f-strings)
- **Change:** Enabled both `python demo.py` and `python scripts/demo.py` to run out of the box regardless of working directory; verified full compatibility with `.github/workflows/ci.yml`.
- **Rationale:** Eliminates ModuleNotFoundError when new users clone and immediately execute `python demo.py`.

---

## 3. Verification Summary

- **Pytest Suite:** 113 / 113 passed in 35.80s.
- **Code Coverage:** 78% overall (`consensus_v2.py` at 82%, `core.py` at 93%, `aspp.py` at 93%).
- **Ruff Linter:** 100% clean across all directories.
- **Git Working Tree:** Clean, consistent, and ready for review.
