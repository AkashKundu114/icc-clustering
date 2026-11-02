# 04 Backward-Compatibility and Public API Audit Report

**Audit Target:** ICC-Clustering (`D:\icc-clustering`)  
**Auditor:** Agent B (Architecture & Compatibility Specialist) & Lead Verification Auditor  
**Audit Timestamp:** 2026-11-01T22:30:00+05:30  
**Repository HEAD:** `83728a441f44c1ed56a35a5bdb07490ff559de81` / `7ddbe8301b8d27c94f388c40acbc88b0dee82723`  
**Baseline Commits Compared:** `781eba578b3ba154a8cf4ac7eb054b3050e6cb4f` (Refactor) and `781eba5~1` (`3bc8459`, Pre-Refactor)

---

## 1. Executive Summary

This independent backward-compatibility audit verified whether the architecture consolidation in commit `781eba5` preserved historical public import paths, function signatures, constructor defaults, metadata contracts, and CLI entry points.

### Compatibility Verdict: **PARTIALLY COMPATIBLE WITH SUBTLE REGRESSIONS**

1. **Object Identity & Core Shims (PASS):**
   - Core compatibility shims (`icc.consensus_v2`, `icc.aspp`, `icc.autok`, `icc.metrics`, `icc.data.registry`, `icc.data.loaders`, `icc.experiments.runner`) preserve 100% object identity with their canonical implementations (`assert icc.consensus_v2.InvariantCoreConsensusV2 is icc.consensus.InvariantCoreConsensusV2`).
   - Core class constructors (`InvariantCoreConsensusV2`, `ASPPConfig`, `BenchmarkRunner`) maintain 100% parameter name, default value, and positional order parity against pre-refactor commit `3bc8459`.
2. **Identified API Regressions & Contract Breaches (DEFECTS):**
   - **Missing Public Exports in `icc.stats`:** `src/icc/stats/testing.py` implements `wilcoxon_signed_rank_test` and `bonferroni_correction`, but `src/icc/stats/__init__.py` fails to import or re-export them in `__all__`, causing standard package imports to crash with `ImportError`.
   - **Contract Discrepancy in `list_models()`:** `icc.algorithms.list_models()` returns 41 internal string keys (`['cohirf', 'dbscan', ...]`), whereas `icc.baselines.list_models()` and top-level `icc.list_models()` return 14 canonical YAML display names (`['K-Means', 'Standard_Consensus', ...]`).
   - **Omission of Explicit `__all__` in `icc.experiments.*` Shims:** `benchmark_models.py`, `fidelity.py`, and `scaling.py` use wildcard imports (`from ... import *`) without declaring `__all__`, causing `getattr(mod, '__all__', None)` to return `None`.
   - **Top-Level Warning Pollution on Import:** `src/icc/baselines/anchor.py:27` and `deep.py:27` fit scikit-learn KMeans on zero matrices during module initialization, polluting `stderr` with `ConvergenceWarning` across 63 out of 68 modules.
   - **Import-Time Filesystem Mutation:** `src/icc/datasets/registry.py:20` executes `_DEFAULT_CACHE.mkdir(parents=True, exist_ok=True)` at top-level module load time.

---

## 2. Compatibility Shim Verification Matrix

Every legacy entry point was audited for module importability, symbol availability, and object identity:

| Legacy Import Path | Canonical Target Module | Exported Symbols Audited | Object Identity Verified? | Backward Compatibility Status |
|---|---|---|:---:|---|
| `icc.consensus_v2` | `icc.consensus.icc` | `InvariantCoreConsensusV2`, `InvariantCoreConsensus`, `GAC`, `build_bipartite_graph`, `spectral_bipartite_consensus`, `asymmetric_bipartite_transfer` | **YES** | **PASS** (100% identical symbols) |
| `icc.aspp` | `icc.consensus.aspp` | `AnchorSpacePerturbationProfiler`, `ASPPConfig`, `ASPPProfile` | **YES** | **PASS** (100% identical symbols) |
| `icc.autok` | `icc.consensus.autok` | `AutoKResult`, `compute_anchor_pac`, `run_icc_autok` | **YES** | **PASS** (100% identical symbols) |
| `icc.metrics` | `icc.evaluation.metrics` | `ari`, `nmi`, `ami`, `v_measure`, `fowlkes_mallows`, `evaluate_all`, `evaluate_all_with_ci` | **YES** | **PASS** (Dual-backend fallbacks preserved) |
| `icc.data.registry` | `icc.datasets.registry` | `DatasetInfo`, `load_dataset`, `list_datasets`, `preprocess_dataset` | **YES** | **PASS** |
| `icc.data.loaders` | `icc.datasets.registry` | `load_dataset`, `list_datasets` | **YES** | **PASS** |
| `icc.experiments.runner` | `icc.benchmarks.runner` | `BenchmarkRunner`, `BenchmarkResult`, `ExperimentRunner`, `ExperimentResult` | **YES** | **PASS** (`ExperimentRunner is BenchmarkRunner`) |
| `icc.experiments.benchmark_models` | `icc.benchmarks.benchmark_models` | `MODELS`, benchmark model wrappers | **YES** | **PARTIAL** (Missing explicit `__all__`) |
| `icc.experiments.fidelity` | `icc.benchmarks.fidelity` | `run_fidelity_experiment`, `evaluate_fidelity` | **YES** | **PARTIAL** (Missing explicit `__all__`) |
| `icc.experiments.scaling` | `icc.benchmarks.scaling` | `run_scaling_experiment`, `evaluate_scaling` | **YES** | **PARTIAL** (Missing explicit `__all__`) |
| `icc.algorithms.*` | `icc.baselines.*` | `run_kmeans`, `run_ward`, `run_spectral`, `run_fcag`, `run_fastmvc`, etc. | **YES** | **PASS** (All 14 baseline runners match) |
| `icc.consensus.conformal` | `cicc.conformal` | `ConformalClusterer`, `ConformalResult` | **YES** | **PASS** (Clean adapter) |

---

## 3. Class Constructor and Parameter Signature Comparison

We compared AST parameter lists and default values between the pre-refactor baseline (`3bc8459`) and canonical HEAD (`83728a4`):

### 3.1 `InvariantCoreConsensusV2` Constructor

```python
# Pre-Refactor Baseline (3bc8459 in src/icc/consensus_v2.py):
def __init__(self, n_clusters=3, n_base_models=25, n_anchors=40, core_quantile=0.5,
             subspace_rate=0.3, beta=None, base_clusterer='auto', enable_aspp=False,
             aspp_config=None, random_state=42, random_seed=None, pool_mode='legacy',
             pool_mad_c=3.5, pool_alpha=0.05, embedding='legacy', dense_threshold=2000,
             pool_frac=0.15)

# Canonical HEAD (83728a4 in src/icc/consensus/icc.py):
def __init__(self, n_clusters: int = 3, n_base_models: int = 25, n_anchors: int = 40,
             core_quantile: float = 0.5, subspace_rate: float = 0.3,
             beta: Optional[float] = None, base_clusterer: str = 'auto',
             enable_aspp: bool = False, aspp_config: Optional[ASPPConfig] = None,
             random_state: int = 42, random_seed: Optional[int] = None,
             pool_mode: str = 'legacy', pool_mad_c: float = 3.5,
             pool_alpha: float = 0.05, embedding: str = 'legacy',
             dense_threshold: int = 2000, pool_frac: float = 0.15)
```

- **Signature Differences:** Exactly 0 parameter name changes, 0 default value changes, 0 positional order re-orderings.
- **Enhancements:** Full PEP 484 type annotations added. Legacy parameter aliases (`random_seed` mapped to `random_state`, `beta` mapped to `core_quantile`) operate with identical backwards-compatible semantics.

### 3.2 `ASPPConfig` Configuration Dataclass

```python
@dataclass
class ASPPConfig:
    families: Tuple[str, ...] = ('sampling', 'feature', 'measurement', 'technical', 'algorithmic')
    levels: Dict[str, Tuple[float, ...]] = field(default_factory=...)
    repetitions: int = 2
    n_base_models: int = 5
    subspace_rate: float = 0.3
    hi_threshold: float = 0.7
    lo_threshold: float = 0.45
    max_response_sd: float = 0.15
    random_state: int = 42
```

- **Signature Differences:** Bitwise identical between `src/icc/aspp.py` and `src/icc/consensus/aspp.py`.

### 3.3 Return Container Parity: `ModelMetadata` vs `AlgorithmMetadata`

- All 14 registered baseline clustering runners (`run_kmeans`, `run_ward`, `run_fcag`, `run_icc_v2`, etc.) return a 3-tuple `(labels, runtime_seconds, ModelMetadata)`.
- In `src/icc/baselines/classical.py`:
  ```python
  class ModelMetadata(int):
      """
      Hybrid return container behaving as int (for legacy scripts expecting lc = N)
      while supporting full dict indexing (for scripts accessing metadata["method"]).
      """
  ```
- Because `ModelMetadata` inherits from `int`, legacy callers expecting `labels, time, lc = run_kmeans(...)` continue to evaluate `isinstance(lc, int) == True` and `int(lc) == n_core`.
- Modern callers accessing `metadata["method"]` or `metadata["converged"]` are fully supported via dict-like indexing.

---

## 4. Deep Inspection of API Regressions

### 4.1 Defect B-01: Missing Exports in `src/icc/stats/__init__.py`
- **Location:** `src/icc/stats/__init__.py#L7-L16`
- **Severity:** P2 (Moderate API Regression)
- **Problem:**
  Commit `1761c1a` introduced two critical statistical testing functions into `src/icc/stats/testing.py`:
  1. `wilcoxon_signed_rank_test(x, y=None)`
  2. `bonferroni_correction(p_values)`
  However, `src/icc/stats/__init__.py` was never updated to re-export them:
  ```python
  from .testing import (
      friedman_test,
      hodges_lehmann_estimator,
      nemenyi_critical_distance,
      tost_equivalence_test,
  )
  __all__ = [
      "hodges_lehmann_estimator",
      "tost_equivalence_test",
      "friedman_test",
      "nemenyi_critical_distance",
  ]
  ```
- **Reproduction:**
  ```python
  from icc.stats import wilcoxon_signed_rank_test
  # ImportError: cannot import name 'wilcoxon_signed_rank_test' from 'icc.stats'
  ```
- **Documentation Impact:** `docs/api.md` explicitly instructs users to run `from icc.stats import wilcoxon_signed_rank_test, bonferroni_correction`, which crashes in user code.

### 4.2 Defect B-02: Contract Discrepancy in `list_models()`
- **Location:** `src/icc/algorithms/__init__.py#L80` vs `src/icc/baselines/__init__.py#L90-L114`
- **Severity:** P2 (API Inconsistency)
- **Problem:**
  - `icc.algorithms.list_models()` aliases `list_algorithms()` and returns 41 internal string dispatch keys:
    ```python
    ['cohirf', 'dbscan', 'dec', 'fastmvc', 'fcag', 'fcm', 'gmm', 'hdbscan', 'icc_v1', 'icc_v2', 'k-means', 'kmeans', ...]
    ```
  - `icc.baselines.list_models()` and `icc.list_models()` parse `configs/baselines.yaml` and return 14 canonical display names:
    ```python
    ['K-Means', 'Ward', 'Spectral', 'FCM', 'Standard_Consensus', 'Li_et_al_2019', 'ICC_v1', 'ICC_v2', 'DEC', 'IDEC', 'CC', 'SCAN', 'FCAG', 'FastMVC']
    ```
- **Consequence:** Code that transitions from `from icc.algorithms import list_models` to `from icc.baselines import list_models` encounters an incompatible data contract (41 normalized keys vs 14 display titles).

### 4.3 Defect B-03: Top-Level `ConvergenceWarning` Pollution on Module Import
- **Location:** `src/icc/baselines/anchor.py#L27` and `src/icc/baselines/deep.py#L27`
- **Severity:** P2 (Library Hygiene / User Experience)
- **Problem:**
  Both files perform an import-time availability check for `scikit-learn`:
  ```python
  _test = _SkKMeans(n_clusters=2, n_init=1).fit_predict(np.zeros((4, 2)))
  ```
  Fitting 2 clusters on all-zeros produces identical points, triggering `sklearn.exceptions.ConvergenceWarning: Number of distinct clusters (1) found smaller than n_clusters (2)`.
- **Measurement:**
  In our isolated import tests (`results/post_refactor_verification/isolated_imports.json`), **63 out of 68 modules** in the package unconditionally emitted this warning to `stderr` upon import.
- **Proper Pattern:** `src/icc/core.py:28` cleanly tests availability with `_sk_ari([0, 1], [0, 1])`, emitting zero warnings.

### 4.4 Defect B-04: Import-Time Filesystem Mutation
- **Location:** `src/icc/datasets/registry.py#L20`
- **Severity:** P3 (Library Hygiene)
- **Problem:**
  ```python
  _PROJECT_ROOT = Path(__file__).resolve().parents[3]
  _DEFAULT_CACHE = _PROJECT_ROOT / "data" / "cache"
  _DEFAULT_CACHE.mkdir(parents=True, exist_ok=True)
  ```
  Executing `import icc` or `import icc.datasets` forcibly creates `data/cache` on the local disk. In read-only or containerized execution environments (e.g. AWS Lambda, read-only Docker containers), this raises an unhandled `OSError: [Errno 30] Read-only file system`.

---

## 5. Machine-Readable API Manifest Comparison

A complete AST inventory was extracted across HEAD (`83728a4`), post-refactor baseline (`781eba5`), and pre-refactor baseline (`3bc8459`). The raw JSON manifests are preserved in `results/post_refactor_verification/`:

| Metric | Pre-Refactor (`3bc8459`) | Post-Refactor Baseline (`781eba5`) | Audited HEAD (`83728a4`) | Net Refactor Change |
|---|:---:|:---:|:---:|:---:|
| Total Source Modules | 59 | 68 | 68 | +9 modular subpackages |
| Total Public Classes | 42 | 45 | 45 | +3 structured classes |
| Total Public Functions | 184 | 192 | 194 | +10 canonical functions |
| Total Exported Symbols | 312 | 348 | 350 | +38 symbols |
| Total Lines of Code (src/) | 14,820 | 10,380 | 10,412 | **-4,408 duplicate lines** |
| Broken Shim Exports | 0 | 2 | 2 | Missing `wilcoxon`, `bonferroni` |
| Circular Import Errors | 0 | 0 | 0 | **0 circular dependencies** |

---

## 6. Recommendations & Action Items

1. **Patch `src/icc/stats/__init__.py`:**
   Add `wilcoxon_signed_rank_test` and `bonferroni_correction` to exports and `__all__`.
2. **Harmonize `list_models()` Contract:**
   Update `icc.algorithms.__init__.py` to document the distinction between algorithm dispatch keys and registered baseline model names, or export `list_registered_models()`.
3. **Eliminate Import-Time Sklearn Fitting:**
   Replace `_SkKMeans(n_clusters=2).fit_predict(np.zeros((4, 2)))` with `np.array([[0.0, 0.0], [1.0, 1.0]])` or a simple `from sklearn.cluster import KMeans` test.
4. **Defer Filesystem Directory Creation:**
   Move `_DEFAULT_CACHE.mkdir(...)` inside `load_dataset()` to prevent side effects at import time.
5. **Declare Explicit `__all__` in `icc.experiments.*`:**
   Replace wildcard imports with explicit symbol lists matching `icc.benchmarks.*`.
