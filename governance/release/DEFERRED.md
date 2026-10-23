# Deferred Code-Quality Findings (Phase C)

**Date:** 2026-10-17  
**Branch:** `release/public-cleanup`  
**Auditor:** Subagent Q  

Per project instructions:
> "Fix all findings that do not change behaviour; for any finding that would change behaviour, log it in RELEASE/DEFERRED.md instead of changing it."

---

## 1. Deprecation Warning on `beta` Parameter
- **Location:** `src/icc/consensus_v2.py:122`
- **Issue:** `beta` is a legacy hyperparameter from ICC-v1 (soft-threshold kernel exponent) that is not used in ICC-v2 anchor consensus.
- **Why Deferred:** Removing `beta` from `InvariantCoreConsensusV2.__init__` would break backward compatibility for experiment scripts and configurations (`configs/experiment_defaults.yaml`) that pass `beta=2.0`. A `DeprecationWarning` is emitted while retaining the argument.

## 2. Low Coverage in Single-Cell and Spectral Loaders
- **Location:** `src/icc/datasets/scrnaseq.py` (34%), `src/icc/datasets/spectral.py` (33%), `src/icc/datasets/image.py` (39%)
- **Issue:** These loaders fetch remote multi-gigabyte or external matrices (e.g. 10x Genomics 68k PBMC tarball, Indian Pines AVIRIS hyperspectral `.mat`).
- **Why Deferred:** Unit tests in standard CI run offline or mocked to keep execution under 1 minute; full dataset downloads are tested via `scripts/fetch_data.py`.

## 3. Deep Clustering Baseline Stubs
- **Location:** `src/icc/baselines/deep.py` (`IDEC`, `CC`, `SCAN`)
- **Issue:** Stubs raise `NotImplementedError` when instantiated without optional external neural libraries.
- **Why Deferred:** Preserves API contract and documented reproduction boundaries without introducing non-standard heavyweight deep learning runtime requirements into core package installation.
