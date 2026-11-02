# Executive Remediation Plan: ICC-Clustering Repository & DMKD Submission Readiness

**Target Repository**: `AkashKundu114/icc-clustering`  
**Current HEAD**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723` (`origin/main`)  
**Audit Status**: Post-Refactor Forensic Audit & Evidence Recovery Complete  
**Final Submission Verdict**: **NO-GO** (Until P0/P1 Remediation is Fully Validated)  

---

## 1. Context and Strategic Objective

An exhaustive, forensic evidence-recovery audit of `AkashKundu114/icc-clustering` was conducted to evaluate its readiness for peer-reviewed submission to *Data Mining and Knowledge Discovery* (DMKD). The investigation established that while core components of the underlying Gated Anchor Consensus (GAC) method are mathematically sound and reproducible (notably Bimodality-Gated Subspace Selection, the Linear Determinacy Identity, and Bipartite Scalability), the repository contains critical **P0 and P1 defects**:

1. **Active Exposure of Historical Confidential Artifacts** on GitHub `origin/main` (commit `e3f54cc` is an active ancestor; 22 public PR refs expose historical vaults).
2. **Clinical and Statistical Misattribution of Conformal Predictions** (coverage collapses to 37.0%–62.2% on real patient pathology; 20% toxic misclassifications).
3. **100% Collapse of AutoK Model Order Selection** ($L_1$ normalization forces $\text{PAC} \equiv 0.0$ and collapse to $K_{min}$ on 510/510 trials).
4. **Methodological Invalidation of Knockoff Feature Gating** (independent Gaussian decoys violate exchangeability; 100% false discovery rate under null; selected features are dead code).
5. **Frozen Synthetic Seed Leakage** (`make_signal` hardcodes `seed=42`, preventing genuine seed variation across synthetic benchmarks).
6. **Falsified Historical Benchmark Comparisons** against Standard Consensus.
7. **Fatal Wheel Packaging Breakdown** (all console scripts crash with `ModuleNotFoundError` in clean environments).

This Executive Remediation Plan establishes a strict, phased roadmap to resolve every identified defect before any manuscript resubmission.

---

## 2. Phased Remediation Strategy

Remediation must proceed in four sequential phases with strict decision gates:

```
[Phase 1: Confidentiality & Safety Isolation]
       │
       ▼
[Phase 2: Algorithmic & Statistical Repair]
       │
       ▼
[Phase 3: Unbiased Re-Benchmarking & Packaging]
       │
       ▼
[Phase 4: Manuscript Alignment & Submission Gate]
```

### Phase 1: Git History Remediation & Confidentiality Isolation (Priority: P0)
- **Objective**: Permanently purge unreleased confirmatory scripts, execution manifests, and sensitive author logs from all public branches, tags, and pull request references on GitHub.
- **Actions**:
  1. Coordinate with repository administrators to perform an official, coordinated Git history rewrite using `git-filter-repo` or BFG Repo-Cleaner across all remote references.
  2. Explicitly remove historical sensitive directories: `src/icc/confirmatory/`, `experiments/vault/`, `EXECUTION_MANIFEST.csv`, and unreleased results archives.
  3. Close and delete or purge GitHub pull requests `refs/pull/1/head` through `refs/pull/22/head`.
  4. Force-push the sanitized history to `origin/main` and recreate release tags (`v1.0.0`, `v2.2.0`).
  5. Instruct all collaborators to re-clone from the sanitized upstream.

### Phase 2: Core Algorithmic & Statistical Repair (Priority: P0 / P1)
- **Objective**: Fix broken mathematical logic and align code with defensible scientific guarantees.
- **Actions**:
  1. **Conformal Framing & Verification (P0)**:
     - Remove all claims in documentation and docstrings claiming CICC provides "guaranteed coverage for clinical diagnosis" or "error-controlled biological phenotyping".
     - Formally document that CICC conformal sets provide finite-sample marginal coverage *strictly with respect to the clustering algorithm's own internal inductive assignments* (pseudo-labels), NOT external unobserved ground-truth pathology.
     - Add an explicit user warning and clinical diagnostic disclaimer in `src/cicc/conformal.py`.
  2. **AutoK Algorithm Repair (P1)**:
     - Replace the flawed PAC calculation in `src/icc/consensus/autok.py`. Instead of computing PAC on the row-normalized bipartite matrix $B_{norm} B_{norm}^T$ (whose inner products collapse below 0.10), compute the co-association matrix directly in cluster assignment space or calibrate the ambiguity threshold $\epsilon$ dynamically based on empirical quantiles of $B B^T$.
     - Re-run the full 510-trial parameter sweep across noise regimes to verify AutoK selects true $K^*$ reliably.
  3. **Knockoff / Decoy Gating Correction (P1)**:
     - If Model-X knockoffs are retained: Implement true second-order Gaussian knockoffs with equi-correlated or SDP-optimized feature covariance matching $\Sigma_{XX}$, rather than independent standard normal noise.
     - Eliminate the fallback bug at `src/cicc/decoy.py:122` that forces feature selection under pure null data.
     - Wire the selected features directly into `src/cicc/inductive.py` so feature gating is actually executed rather than acting as dead code.
     - Alternatively: Deprecate `cicc.decoy` and rely exclusively on the verified, mathematically sound BGSS module.
  4. **Synthetic Seed Independence Fix (P1)**:
     - In `src/icc/core.py:build_dataset()`, remove the hardcoded `seed=RNG_DATA_SEED` (42) passed to `make_signal()`. Propagate the caller's seed dynamically to both signal and noise generators so that synthetic benchmarks test across genuinely independent cluster realizations.

### Phase 3: Unbiased Re-Benchmarking & Packaging Repair (Priority: P1)
- **Objective**: Produce unassailable, independently reproducible benchmark tables and deliver an installable package.
- **Actions**:
  1. **Benchmark Re-execution**:
     - Re-run full benchmarks across all 13 real biomedical cohorts and synthetic grids with unbiased baseline implementations.
     - Retract fraudulent speedup claims; accurately report that Standard Consensus runs in $0.12\text{s}$ and record true ICC-v2 runtimes without artificial inflation.
     - Accurately report that anchor certification yields $\Delta = +0.019$ ($p=0.844$) over random anchors, reframing anchor selection as a computational compression mechanism rather than an accuracy booster.
  2. **Packaging & Console Script Fix**:
     - Fix `pyproject.toml` console script entrypoints. Move CLI commands into proper importable submodules within `src/icc/cli/`.
     - Update `pyproject.toml` package discovery so all necessary subpackages are bundled into wheels.
     - Add a dedicated CI workflow job that builds a wheel (`python -m build`), creates an isolated clean virtual environment, installs `dist/*.whl`, and verifies `icc`, `icc-demo`, and `icc-run` outside the source tree.

### Phase 4: Manuscript & Technical Documentation Alignment (Priority: P1)
- **Objective**: Align every table, figure, and claim in `main.tex` and `numbers.tex` with verified microdata.
- **Actions**:
  1. Update `numbers.tex` macros to reflect verified statistical values.
  2. Rewrite Section 4.2 to present core anchors honestly as an $\mathcal{O}(N L)$ memory compression technique rather than a statistical accuracy enhancer.
  3. Ensure CICC conformal prediction is presented with precise theoretical boundaries and clinical disclaimers.
  4. Archive all recovered raw CSV and JSON artifacts into a public, immutable DOI repository (e.g., Zenodo) linked in the manuscript Data Availability statement.

---

## 3. Decision Gate Criteria for DMKD Submission

The manuscript may ONLY be transitioned from **NO-GO** to **GO** when all of the following verifiable conditions are met:

| Gate | Requirement | Verification Method | Sign-off Status |
| :---: | :--- | :--- | :---: |
| **Gate 1** | Remote Git history is sanitized; commit `e3f54cc` is unreachble; all 22 PR refs purged. | `git log origin/main` and `git ls-remote` show zero trace of historical vaults. | **PENDING** |
| **Gate 2** | Conformal documentation and code contain explicit pseudo-label framing and clinical disclaimer. | Code inspection of `src/cicc/conformal.py` and unit tests in `tests/unit/test_cicc.py`. | **PENDING** |
| **Gate 3** | AutoK correctly identifies $K^*$ on $\ge 90\%$ of benchmark trials across $K \in [2, 10]$. | Re-execution of 510-trial adversarial sweep recorded in `results/`. | **PENDING** |
| **Gate 4** | Synthetic data generation produces distinct cluster centroids and labels across different seeds. | Unit test verifying centroid variance across seeds in `test_core.py`. | **PENDING** |
| **Gate 5** | Wheel installs and console scripts (`icc`, `icc-demo`, `icc-run`) execute successfully in clean virtual environment. | CI matrix job passes on clean environment without `-e .`. | **PENDING** |
| **Gate 6** | Every number in `main.tex` and `numbers.tex` traces directly to an archived raw data file. | Automated regex check against `results/` microdata. | **PENDING** |
