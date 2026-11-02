# ICC-Clustering Code Duplication Audit

## 1. Executive Summary

This audit catalogs code duplication, legacy redundancy, and the architectural distinction between canonical engines and backward-compatibility shims across the `icc-clustering` codebase.

---

## 2. Duplication Findings & Resolution Status

### Finding AUD-DUP-001: Duplicate ASPP Implementation
- **Severity:** **High**
- **Status:** **RESOLVED** (Refactored in REF-001)
- **Files Affected:**
  - `src/icc/aspp.py` (originally 408 lines, 13,873 bytes)
  - `src/icc/consensus/aspp.py` (canonical 408 lines, 13,877 bytes)
- **Resolution Applied:**
  `src/icc/aspp.py` has been converted into an 18-line backward-compatibility shim that re-exports `ASPP_FAMILIES`, `AnchorSpacePerturbationProfiler`, and `ASPPConfig` from `icc.consensus.aspp`. `src/icc/__init__.py:9` now imports directly from `icc.consensus.aspp`.
- **Verification:**
  `python -m pytest tests/unit/test_aspp.py` passed 7/7 tests.

### Finding AUD-DUP-002: Semantic Collision on Data Functions
- **Severity:** **Medium**
- **Status:** **Identified & Tracked in Backlog (PEN-003)**
- **Files Affected:**
  - `src/icc/core.py` (lines 109-118, 269-279, 282-293)
  - `src/icc/data/preprocessing.py` (lines 176-184, 199-212, 215-220)
- **Impact:**
  - `pairwise_coassoc` in `core.py`: computes ensemble co-association $[0, 1]^{N \times N}$ from partition list.
  - `pairwise_coassoc` in `preprocessing.py`: computes binary adjacency $\{0, 1\}^{N \times N}$ from a single partition array.
  - `canonical` in `core.py`: returns a tuple; in `preprocessing.py`: returns an `np.ndarray`.
- **Planned Resolution:**
  Rename `core.pairwise_coassoc` to `ensemble_coassociation_matrix` and `core.canonical` to `canonical_partition_tuple` to eliminate collision.

---

## 3. Verified Canonical vs. Compatibility Shim Inventory

The following table documents all modules that function as intentional backward-compatibility layers versus their canonical single-source-of-truth implementations:

| Legacy / Shim Path | Canonical Implementation | Lines in Shim | Status | Verification Reference |
|---|---|---|---|---|
| `src/icc/aspp.py` | `src/icc/consensus/aspp.py` | 18 lines | **Verified Shim** | `tests/unit/test_aspp.py` |
| `src/icc/consensus_v2.py` | `src/icc/consensus/icc.py` | 25 lines | **Verified Shim** | `tests/regression/test_architecture_compatibility.py` |
| `src/icc/metrics.py` | `src/icc/evaluation/metrics.py` | 39 lines | **Verified Shim** | `tests/unit/test_metrics.py` |
| `src/icc/data/registry.py` | `src/icc/datasets/registry.py` | 22 lines | **Verified Shim** | `tests/integration/test_datasets.py` |
| `src/icc/data/loaders.py` | `src/icc/datasets/registry.py` | 11 lines | **Verified Shim** | `scripts/prepare_data.py` |
| `src/icc/autok.py` | `src/icc/consensus/autok.py` | 11 lines | **Verified Shim** | `tests/unit/test_autok.py` |
| `src/icc/experiments/runner.py` | `src/icc/benchmarks/runner.py` | 16 lines | **Verified Shim** | `tests/integration/test_runner.py` |
| `src/icc/experiments/benchmark_models.py` | `src/icc/benchmarks/benchmark_models.py` | 14 lines | **Verified Shim** | `tests/unit/test_consensus.py` |
| `src/icc/experiments/fidelity.py` | `src/icc/benchmarks/fidelity.py` | 16 lines | **Verified Shim** | `tests/regression/test_anchor_fidelity.py` |
| `src/icc/experiments/scaling.py` | `src/icc/benchmarks/scaling.py` | 16 lines | **Verified Shim** | `tests/regression/test_scaling_timing.py` |
| `src/icc/algorithms/anchor.py` | `src/icc/baselines/anchor.py` | 18 lines | **Verified Shim** | `tests/unit/test_algorithms.py` |
| `src/icc/algorithms/classical.py` | `src/icc/baselines/classical.py` | 27 lines | **Verified Shim** | `tests/unit/test_algorithms.py` |
| `src/icc/algorithms/cohirf.py` | `src/icc/baselines/cohirf.py` | 17 lines | **Verified Shim** | `tests/unit/test_algorithms.py` |
| `src/icc/algorithms/deep.py` | `src/icc/baselines/deep.py` | 24 lines | **Verified Shim** | `tests/unit/test_algorithms.py` |
| `src/icc/algorithms/density.py` | `src/icc/baselines/density.py` | 18 lines | **Verified Shim** | `tests/regression/test_algorithm_fidelity.py` |
| `src/icc/algorithms/leiden.py` | `src/icc/baselines/leiden_snn.py` | 19 lines | **Verified Shim** | `tests/regression/test_algorithm_fidelity.py` |
| `src/icc/algorithms/monti.py` | `src/icc/baselines/consensus.py` | 19 lines | **Verified Shim** | `tests/unit/test_algorithms.py` |
| `src/icc/algorithms/probabilistic.py` | `src/icc/baselines/probabilistic.py` | 19 lines | **Verified Shim** | `tests/unit/test_algorithms.py` |
| `src/icc/algorithms/sparse_kmeans.py` | `src/icc/baselines/sparse_kmeans.py` | 18 lines | **Verified Shim** | `tests/unit/test_algorithms.py` |
