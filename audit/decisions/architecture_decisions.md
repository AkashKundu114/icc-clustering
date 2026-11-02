# ICC-Clustering Architecture Decision Records (ADRs)

## Index of Architectural Decisions

- [ADR-001: Canonical Benchmark Package and Shims](#adr-001-canonical-benchmark-package-and-shims)
- [ADR-002: Deduplication of Consensus Clustering Engines](#adr-002-deduplication-of-consensus-clustering-engines)
- [ADR-003: Canonical Metrics Engine and Dual-Backend Verification](#adr-003-canonical-metrics-engine-and-dual-backend-verification)
- [ADR-004: Domain Dataset Loaders vs Functional Preprocessing](#adr-004-domain-dataset-loaders-vs-functional-preprocessing)
- [ADR-005: Baseline Clustering Registry and Algorithm Protocols](#adr-005-baseline-clustering-registry-and-algorithm-protocols)
- [ADR-006: Flat Documentation and Research Confidentiality Boundary](#adr-006-flat-documentation-and-research-confidentiality-boundary)

---

### ADR-001: Canonical Benchmark Package and Shims

- **Status:** **Accepted and Implemented**
- **Date:** 2026-11-01
- **Context:** Previous versions created an ambiguous division between experiment scripts, root-level output folders, and `src/icc/experiments/`. Furthermore, user requirements prohibit root-level `experiments/` folders while demanding that benchmark execution remains inside the Python library.
- **Decision:** 
  1. Create `src/icc/benchmarks/` as the single canonical execution package containing `runner.py` (`BenchmarkRunner`, `BenchmarkResult`), `fidelity.py`, `scaling.py`, and `benchmark_models.py`.
  2. Maintain `src/icc/experiments/` as a zero-overhead backward-compatibility package re-exporting symbols from `icc.benchmarks`.
  3. Exclude `results/` from Git and ensure `BenchmarkRunner` creates output directories dynamically upon execution.
- **Consequences:** Eliminates code duplication, prevents repository pollution, and allows existing client code (`from icc.experiments import ExperimentRunner`) to run without modification.

---

### ADR-002: Deduplication of Consensus Clustering Engines

- **Status:** **Accepted and Implemented**
- **Date:** 2026-11-01
- **Context:** The repository contained three overlapping consensus sources: `src/icc/consensus.py` (183 lines), `src/icc/consensus_v2.py` (572 lines), and `src/icc/consensus/` package (`icc.py`, `aspp.py`, `autok.py`, `conformal.py`). Because Python's import system resolves package directories before `.py` files of the same name, `src/icc/consensus.py` was shadowed dead code.
- **Decision:**
  1. Delete `src/icc/consensus.py` from disk.
  2. Establish `src/icc/consensus/icc.py` as the canonical implementation of both `InvariantCoreConsensusV2` (ICCv2 / GAC) and `InvariantCoreConsensus` (ICCv1).
  3. Convert `src/icc/consensus_v2.py` into a clean compatibility shim that re-exports canonical classes from `icc.consensus.icc`.
- **Consequences:** Resolves potential shadowing bugs, removes 750+ redundant lines, and maintains 100% compatibility for `from icc.consensus_v2 import InvariantCoreConsensusV2`.

---

### ADR-003: Canonical Metrics Engine and Dual-Backend Verification

- **Status:** **Accepted and Implemented**
- **Date:** 2026-11-01
- **Context:** `src/icc/metrics.py` (12 KB) was an exact line-for-line duplicate of `src/icc/evaluation/metrics.py`. Both implemented contingency-table-based clustering metrics (ARI, NMI, AMI, V-Measure, Fowlkes-Mallows) with dual-backend fallback (scikit-learn with pure-NumPy/SciPy fallback).
- **Decision:**
  1. Establish `src/icc/evaluation/metrics.py` as the single canonical source of clustering evaluation metrics.
  2. Convert `src/icc/metrics.py` into a compatibility shim re-exporting all public functions and internal fallback verification flags (`_SKLEARN_AVAILABLE`, `_sk_ari`, etc.).
- **Consequences:** Ensures single source of truth for all metric calculations, eliminates dual maintenance risk, and guarantees zero broken imports across examples and tests.

---

### ADR-004: Domain Dataset Loaders vs Functional Preprocessing

- **Status:** **Accepted and Implemented**
- **Date:** 2026-11-01
- **Context:** Confusion existed between `src/icc/data/` and `src/icc/datasets/`. Both contained a `registry.py` with identical contents.
- **Decision:**
  1. Separate responsibilities cleanly:
     - `src/icc/datasets/` is the canonical multi-domain benchmark loading system (covering 13 benchmark datasets across 7 domains: audio, genomics, image, scrnaseq, spectral, text).
     - `src/icc/data/` is retained for generic data preprocessing (`preprocessing.py` containing bimodality coefficient, synthetic signal/noise generators) and dynamic cohort discovery (`cohorts.py`).
  2. Convert `src/icc/data/registry.py` into a compatibility shim re-exporting from `src/icc/datasets.registry`.
- **Consequences:** Clarifies domain boundary, eliminates registry duplication, and protects generic preprocessing tools.

---

### ADR-005: Baseline Clustering Registry and Algorithm Protocols

- **Status:** **Accepted and Implemented**
- **Date:** 2026-11-01
- **Context:** `src/icc/algorithms/` and `src/icc/baselines/` contained duplicate files for anchor clustering, deep clustering, density clustering, and probabilistic models.
- **Decision:**
  1. Designate `src/icc/baselines/` as the canonical implementation package for all external and comparative baseline methods (K-Means, Ward, Spectral, FCM, GMM, HDBSCAN, DBSCAN, Sparse K-Means, Leiden-SNN, FCAG, FastMVC, DEC, CoHiRF).
  2. Consolidate `run_dbscan` into `src/icc/baselines/density.py`.
  3. Maintain `src/icc/algorithms/base.py` as the interface definition package defining `BaseClusterer`, `AlgorithmMetadata`, and `validate_clustering_input`.
  4. Convert `src/icc/algorithms/*.py` modules into thin shims re-exporting from `icc.baselines.*`.
- **Consequences:** Eliminates over 2,500 lines of duplicated baseline clustering code while preserving both algorithm access patterns (`get_model` and `get_algorithm`).

---

### ADR-006: Flat Documentation and Research Confidentiality Boundary

- **Status:** **Accepted and Implemented**
- **Date:** 2026-11-01
- **Context:** Documentation files had inconsistent UPPERCASE names, obsolete nested folders (`docs/figures/`), and references to internal audit codes or unpublished manuscript drafts.
- **Decision:**
  1. Flatten `docs/` hierarchy; remove `docs/figures/`.
  2. Standardize documentation names to lowercase concise filenames: `theory.md`, `reproducibility.md`, `data.md`, `setup.md`.
  3. Relocate all private audit findings, internal issue tags, and execution logs exclusively into local-only `/audit/` and `/results/` workspaces.
- **Consequences:** Public GitHub repository remains professional, clean, and free of unpublished research material, while private local engineering notes are preserved in verified local working directories.
