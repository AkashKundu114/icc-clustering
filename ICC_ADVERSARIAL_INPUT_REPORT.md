# ICC Adversarial Input and Boundary Robustness Report

**Project:** Invariant Core Consensus (ICC-v2)  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Active Branch:** `fix/audit-remediation`  
**Test Suite:** `tests/test_adversarial_inputs.py` & `tests/test_edge_cases.py`  
**Date:** October 16, 2026  

---

## 1. Scope and Objective

Machine learning clustering algorithms, particularly ensemble methods operating on high-dimensional data, are susceptible to degenerate inputs, malicious numerical corner cases, and dimension mismatch faults. The objective of this audit was to:
1. Define a rigorous taxonomy of adversarial and boundary input conditions.
2. Formulate explicit defensive behaviors for each condition.
3. Validate that ICC-v2 fails safely and informatively when presented with hostile inputs, while processing valid edge cases gracefully without numerical corruption.

---

## 2. Taxonomy of Adversarial & Degenerate Inputs

```
                                Adversarial Inputs
                                        │
      ┌────────────────────────┬────────┴───────────────┬────────────────────────┐
      │                        │                        │                        │
      ▼                        ▼                        ▼                        ▼
[Structural / Shape]    [Numerical Hostility]     [Domain Violations]      [Inductive Query]
 • 1D/3D arrays          • NaNs / Nulls            • N < K                  • Feature Mismatch
 • Empty matrices        • +Inf / -Inf             • Hyperparameters OOB    • Empty Query Batch
 • Constant Columns      • Extreme Magnitudes      • Unfitted Model Calls   • High-D Imbalance
```

### 2.1 Category A: Structural and Dimensional Malformations
- **1D Vector Input:** User supplies array with shape `(N,)` instead of `(N, D)`.
- **3D Tensor Input:** User passes image tensor `(N, H, W)` without flattening.
- **Empty Matrices:** Passing arrays with shape `(0, D)` or `(N, 0)`.
- **Under-Constrained Cohorts:** Passing sample sizes smaller than cluster counts ($N < K$), where clustering is mathematically under-determined.

### 2.2 Category B: Hostile Numerical Values
- **Missing / NaN Values:** Passing matrices containing un-imputed `np.nan` values.
- **Infinite Values:** Passing values containing positive or negative infinity (`\pm\infty`).
- **Extreme Coordinate Scales:** Inputs scaled to $10^{6}$ or $10^{-6}$, testing float arithmetic stability in distance computations.
- **Constant / Zero-Variance Features:** High-dimensional matrices where subset of features have zero sample variance (e.g., all 0.0 or constant value).
- **Duplicate Data Points:** Multiple identical feature vectors causing identical row vectors in distance matrices.

### 2.3 Category C: Initialization Hyperparameter Bounds
- **Invalid Cluster Count:** `n_clusters < 2` (0, 1, negative).
- **Invalid Base Models:** `n_base_models < 1` (0, negative).
- **Invalid Anchor Counts:** `n_anchors < 1` (0, negative).
- **Out-of-Bounds Quantiles:** `core_quantile <= 0.0` or `core_quantile > 1.0`.
- **Out-of-Bounds Subspace Rates:** `subspace_rate <= 0.0` or `subspace_rate > 1.0`.
- **Unrecognized Pool Modes:** Arbitrary string values passed to `pool_mode`.

### 2.4 Category D: Inductive Query and Transform Exploits
- **Dimension Mismatch:** Inductive query $X_{\text{new}}$ with feature dimension $D_{\text{test}} \neq D_{\text{train}}$.
- **Unfitted Invocations:** Invoking `predict()`, `predict_proba()`, `predict_with_stability()`, or `transform()` before `fit_predict()` or `fit()`.
- **Empty Query Batches:** Passing $X_{\text{new}}$ with shape `(0, D)` during out-of-sample inference.

---

## 3. Defensive Implementation Architecture

The defenses are integrated into `src/icc/consensus_v2.py`:

### 3.1 Initializer Validation Layer
```python
if n_clusters < 2:
    raise ValueError(f"n_clusters must be >= 2, got {n_clusters}")
if n_base_models < 1:
    raise ValueError(f"n_base_models must be >= 1, got {n_base_models}")
if n_anchors is not None and n_anchors < 1:
    raise ValueError(f"n_anchors must be >= 1, got {n_anchors}")
if not (0.0 < core_quantile <= 1.0):
    raise ValueError(f"core_quantile must be in (0, 1], got {core_quantile}")
if not (0.0 < subspace_rate <= 1.0):
    raise ValueError(f"subspace_rate must be in (0, 1], got {subspace_rate}")
valid_pool_modes = ("legacy", "bc_frac", "random_frac", "random", "robust", "gauss", "null_calibrated")
if pool_mode not in valid_pool_modes:
    raise ValueError(f"Invalid pool_mode '{pool_mode}'. Must be one of {valid_pool_modes}")
```

### 3.2 Training Input Sanitization (`fit_predict`)
```python
X = np.asarray(X, dtype=np.float64)
if X.ndim != 2:
    raise ValueError(f"Expected 2D feature matrix (N, D), got array with {X.ndim} dimensions and shape {X.shape}.")
N, D = X.shape
if N == 0 or D == 0:
    raise ValueError(f"Input feature matrix cannot be empty, got shape ({N}, {D}).")
if N < self.n_clusters:
    raise ValueError(f"n_samples={N} must be >= n_clusters={self.n_clusters}.")
if np.isnan(X).any() or np.isinf(X).any():
    raise ValueError("Input feature matrix contains NaN or Inf values. Clean or impute missing data before clustering.")
self.n_features_in_ = D
```

### 3.3 Inductive Inference Guard (`_validate_X_new` & `transform`)
```python
def _validate_X_new(self, X_new: np.ndarray) -> np.ndarray:
    if self.anchor_centroids_ is None:
        raise RuntimeError("Model has not been fitted yet. Call fit() or fit_predict() first.")
    X_new = np.asarray(X_new, dtype=np.float64)
    if X_new.ndim != 2:
        raise ValueError(f"Expected 2D feature matrix for X_new, got array with {X_new.ndim} dimensions and shape {X_new.shape}.")
    if hasattr(self, "n_features_in_") and self.n_features_in_ is not None:
        if X_new.shape[1] != self.n_features_in_:
            raise ValueError(
                f"Feature dimension mismatch: X_new has {X_new.shape[1]} features, "
                f"but InvariantCoreConsensusV2 was fitted on {self.n_features_in_} features."
            )
    if np.isnan(X_new).any() or np.isinf(X_new).any():
        raise ValueError("X_new contains NaN or Inf values. Preprocess missing values before prediction.")
    return X_new
```

---

## 4. Empirical Test Verification

The defensive capabilities were verified across 43 automated tests (`tests/test_adversarial_inputs.py` and `tests/test_edge_cases.py`):

| Test ID | Test Target | Input Condition | Expected Behavior | Observed Result | Status |
|---|---|---|---|---|---|
| **ADV-01** | `test_invalid_n_clusters` | $K \in \{0, 1, -2\}$ | Raises `ValueError` | `ValueError: n_clusters must be >= 2` | **PASS** |
| **ADV-02** | `test_invalid_n_base_models` | $M \in \{0, -1, -10\}$ | Raises `ValueError` | `ValueError: n_base_models must be >= 1` | **PASS** |
| **ADV-03** | `test_invalid_n_anchors` | $m \in \{0, -5\}$ | Raises `ValueError` | `ValueError: n_anchors must be >= 1` | **PASS** |
| **ADV-04** | `test_invalid_core_quantile` | $q \in \{-0.1, 0.0, 1.05, 2.0\}$ | Raises `ValueError` | `ValueError: core_quantile must be in (0, 1]` | **PASS** |
| **ADV-05** | `test_invalid_subspace_rate` | rate $\in \{-0.5, 0.0, 1.1, 5.0\}$ | Raises `ValueError` | `ValueError: subspace_rate must be in (0, 1]` | **PASS** |
| **ADV-06** | `test_invalid_pool_mode` | Mode `"malicious_code"` | Raises `ValueError` | `ValueError: Invalid pool_mode 'malicious_code'` | **PASS** |
| **ADV-07** | `test_rejects_1d_input` | Shape `(5,)` | Raises `ValueError` | `ValueError: Expected 2D feature matrix` | **PASS** |
| **ADV-08** | `test_rejects_3d_input` | Shape `(10, 5, 2)` | Raises `ValueError` | `ValueError: Expected 2D feature matrix` | **PASS** |
| **ADV-09** | `test_rejects_empty_input` | Shape `(0, 5)` and `(10, 0)` | Raises `ValueError` | `ValueError: Input feature matrix cannot be empty` | **PASS** |
| **ADV-10** | `test_rejects_fewer_samples` | $N=4, K=5$ | Raises `ValueError` | `ValueError: n_samples=4 must be >= n_clusters=5` | **PASS** |
| **ADV-11** | `test_rejects_nan_values` | Matrix with `NaN` entry | Raises `ValueError` | `ValueError: Input feature matrix contains NaN or Inf` | **PASS** |
| **ADV-12** | `test_rejects_inf_values` | Matrix with $\pm\infty$ entry | Raises `ValueError` | `ValueError: Input feature matrix contains NaN or Inf` | **PASS** |
| **ADV-13** | `test_unfitted_calls` | Query unfitted model | Raises `RuntimeError` | `RuntimeError: Model has not been fitted yet` | **PASS** |
| **ADV-14** | `test_dimension_mismatch` | $D_{\text{train}}=8, D_{\text{test}}\in\{5, 10\}$ | Raises `ValueError` | `ValueError: Feature dimension mismatch` | **PASS** |
| **ADV-15** | `test_out_of_sample_nan_inf` | Query with `NaN`/`Inf` | Raises `ValueError` | `ValueError: X_new contains NaN or Inf` | **PASS** |
| **ADV-16** | `test_empty_test_set` | Query with shape `(0, 8)` | Returns empty ndarrays | Returns shape `(0,)` int, `(0, 3)` float | **PASS** |
| **ADV-17** | `test_transform_predict` | Transform distance space | $\arg\min(D) == \text{predict}(X)$ | Exact equality confirmed | **PASS** |
| **ADV-18** | `test_scaled_data_stability` | Scale factor $10^6$ | Fit without crash | Valid partition produced, 0 NaNs | **PASS** |
| **ADV-19** | `test_zero_variance_features` | Zero-variance noise columns | Gating eliminates columns | Constant columns discarded safely | **PASS** |
| **ADV-20** | `test_duplicate_samples` | 50% duplicate rows | Stable anchor assignment | Over 85% duplicate label agreement | **PASS** |

---

## 5. Summary & Hardening Conclusion

All 43 tests pass cleanly. ICC-v2 has transitioned from assuming cooperative research scripts to an **adversarially resilient** clustering pipeline capable of safely handling hostile user inputs, malformed streaming batches, and un-sanitized dataset matrices without segmentation faults, uncaught exceptions, or data poisoning.
