# ICC-Clustering Dead Code & Unused Artifacts Audit

## 1. Executive Summary

This audit evaluates unused functions, dead code branches, deprecated parameters, and legacy structural artifacts across the `icc-clustering` codebase.

---

## 2. Dead Code & Unused Artifact Findings

### Finding AUD-DEAD-001: Deprecated `beta` Parameter in ICC-v2
- **Severity:** **Low**
- **Status:** **Open / Documented**
- **Affected File:** `src/icc/consensus/icc.py:91-96`
- **Fact vs. Inference:** [Verified Fact].
- **Code Reference:**
  ```python
  if beta != 2.0:
      warnings.warn("beta is not used by ICC-v2 and is deprecated", DeprecationWarning)
  ```
- **Analysis:**
  In ICC-v1 (`InvariantCoreConsensus`), `beta` parameter was an active exponential decay coefficient ($w_i = \exp(-\beta \cdot \sigma_i)$) penalizing noise features. In ICC-v2 (`InvariantCoreConsensusV2`), noise filtering is handled completely by Bimodality-Gated Subspace Selection (BGSS). The parameter is retained solely for API compatibility with legacy scripts, but performs no mathematical function.
- **Remediation:**
  Maintain deprecation warning in v2.2.x; remove parameter in next major version (v3.0.0).

---

### Finding AUD-DEAD-002: Empty `src/icc/figures/` Directory
- **Severity:** **Informational**
- **Status:** **Open**
- **Affected Path:** `src/icc/figures/`
- **Fact vs. Inference:** [Verified Fact].
- **Analysis:**
  The directory `src/icc/figures/` contains no tracked files, code, or assets. Publication figures and visual documentation were cleaned up in prior phases.
- **Remediation:**
  Remove directory to keep package namespace clean: `rmdir src/icc/figures`.

---

### Finding AUD-DEAD-003: Redundant `src/icc/data/loaders.py` Wrapper
- **Severity:** **Low**
- **Status:** **Open / Documented**
- **Affected File:** `src/icc/data/loaders.py:1-13`
- **Fact vs. Inference:** [Verified Fact].
- **Code Reference:**
  ```python
  from .registry import load_dataset, list_datasets

  __all__ = ["load_dataset", "list_datasets"]
  ```
- **Analysis:**
  `loaders.py` is a 13-line file that merely imports and re-exports `load_dataset` and `list_datasets` from `src/icc/data/registry.py` (which itself delegates to `src/icc/datasets/registry.py`).
- **Remediation:**
  Maintain as legacy compatibility shim; deprecate direct imports from `icc.data.loaders` in favor of `icc.datasets.load_dataset`.

---

### Finding AUD-DEAD-004: Unused Internal Fallback Flags in Unreferenced Modules
- **Severity:** **Low**
- **Status:** **Open**
- **Affected Files:** `src/icc/baselines/deep.py:31`, `src/icc/baselines/anchor.py:21`
- **Fact vs. Inference:** [Verified Fact].
- **Analysis:**
  `_SKLEARN_AVAILABLE` boolean flags are defined at the module level in several baseline modules where scikit-learn is already a mandatory project requirement in `pyproject.toml`. These try/except import blocks are defensive legacy code from when scikit-learn was optional.
- **Remediation:**
  Rely on top-level `scikit-learn>=1.3.0` dependency declaration and remove redundant try/except guards for core libraries.
