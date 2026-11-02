# ICC-Clustering Technical Debt & Maintainability Audit

## 1. Executive Summary

This audit assesses maintainability, typing coverage, error handling, interface consistency, and architectural technical debt across the `icc-clustering` codebase.

---

## 2. Technical Debt Findings

### Finding AUD-DEBT-001: Baseline Return Tuple vs Estimator Object Asymmetry
- **Severity:** **Medium**
- **Status:** **Open / Documented**
- **Affected Packages:** `src/icc/baselines/` vs `src/icc/consensus/`
- **Fact vs. Inference:** [Verified Fact].
- **Analysis:**
  - `InvariantCoreConsensusV2` follows the standard Scikit-Learn Estimator API pattern (`fit(X)`, `predict(X)`, attributes `labels_`, `stability_`, `aspp_summary_`).
  - Comparative baseline runners in `src/icc/baselines/` (`run_kmeans`, `run_spectral`, `run_fcag`, `run_hdbscan`, etc.) use a procedural functional interface returning a 3-element tuple: `(labels: np.ndarray, runtime_sec: float, metadata: ModelMetadata)`.
  - While this functional pattern facilitates rapid benchmark execution in `BenchmarkRunner`, it requires adapter wrappers (`BaseClusterer` in `algorithms/base.py`) when treating baselines as standard estimator objects.
- **Remediation:**
  Maintain functional wrappers for benchmark execution speed; introduce a unified `EstimatorAdapter(callable_fn)` in `src/icc/algorithms/base.py` to bridge functional runners to the Scikit-Learn API seamlessly.

---

### Finding AUD-DEBT-002: Incomplete Static Type Annotations in Subspace Sampling
- **Severity:** **Low**
- **Status:** **Open**
- **Affected Files:** `src/icc/consensus/icc.py:180-240`, `src/icc/core.py:110-145`
- **Fact vs. Inference:** [Verified Fact].
- **Analysis:**
  Although `src/icc/py.typed` is present (advertising PEP 561 compliance), several internal helper methods in `icc.py` use untyped internal variables or `Optional[Any]` parameters (e.g., `self.aspp_profiler_: Optional[Any] = None`).
- **Remediation:**
  Annotate all internal attributes with exact dataclass or protocol types to achieve 100% strict `mypy` compliance.

---

### Finding AUD-DEBT-003: Broad Exception Catching in Baseline Adapters
- **Severity:** **Low**
- **Status:** **Open**
- **Affected Files:** `src/icc/baselines/density.py:142`, `src/icc/baselines/anchor.py:45`
- **Fact vs. Inference:** [Verified Fact].
- **Analysis:**
  In `run_hdbscan()`:
  ```python
  try:
      from sklearn.cluster import HDBSCAN
      hdb = HDBSCAN(...)
      labels = hdb.fit_predict(X_clust)
  except Exception:
      from sklearn.cluster import DBSCAN
      ...
  ```
  Catching bare `Exception` can mask unexpected errors (e.g. `MemoryError`, invalid array shapes, or NaN values) rather than catching specifically `(ImportError, AttributeError, ValueError)`.
- **Remediation:**
  Narrow the exception specification to `except (ImportError, AttributeError):`.

---

### Finding AUD-DEBT-004: Global ConvergenceWarning Suppression in Pytest Configuration
- **Severity:** **Low**
- **Status:** **Accepted / Documented**
- **Affected File:** `pyproject.toml:126-130`
- **Fact vs. Inference:** [Verified Fact].
- **Analysis:**
  `pyproject.toml` filters out `ConvergenceWarning` globally:
  ```toml
  filterwarnings = [
      "ignore::sklearn.exceptions.ConvergenceWarning",
      "ignore:Graph is not fully connected:UserWarning",
  ]
  ```
  In random subspace clustering ensembles ($M=25$ models, $25\%$ features sampled per model in $D \gg N$ noisy space), individual subspace draws may occasionally draw collinear or uninformative dimensions where K-Means encounters duplicate centroids. Suppressing this warning globally avoids cluttering test logs, but risks hiding unintended convergence failures in user-facing scripts.
- **Remediation:**
  Retain warning filter in tests; ensure library code catches and logs convergence anomalies at `DEBUG` level.
