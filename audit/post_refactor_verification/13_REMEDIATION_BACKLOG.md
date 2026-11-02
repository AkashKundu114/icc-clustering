# 13 Prioritized Engineering and Scientific Remediation Backlog

**Audit Target:** ICC-Clustering (`D:\icc-clustering`)  
**Auditor:** Lead Verification Auditor & Subagent Council  
**Audit Timestamp:** 2026-11-01T22:48:00+05:30  
**Repository HEAD:** `83728a441f44c1ed56a35a5bdb07490ff559de81` / `7ddbe8301b8d27c94f388c40acbc88b0dee82723`  

---

## 1. Backlog Overview

This remediation backlog compiles all verified defects, mathematical failures, security vulnerabilities, packaging bugs, and documentation inconsistencies identified across the six audit workstreams. Every item includes exact code locations, reproduction procedures, scientific impact assessments, concrete code remediations, and required regression tests.

### Severity Definitions:
- **P0 (Critical / Blocker):** Confidentiality leaks, invalid clinical safety guarantees, or fundamental research invalidity.
- **P1 (High Priority):** Algorithmic collapse, mathematical theory violations, broken packaging, or benchmark falsification.
- **P2 (Medium Priority):** Data leakage, unhandled exceptions on edge cases, API contract mismatches, or test runner flaws.
- **P3 (Low Priority):** Documentation typos, library import hygiene, or non-breaking stylistic inconsistencies.

---

## 2. Priority P0: Critical Blocker Issues

### Item P0-01: Public Git History Remediation Failure
- **File / Location:** Entire Git History DAG (`e3f54cc` $\to$ `83728a4` $\to$ `7ddbe83`); 22 public PR refs (`refs/pull/*/head`).
- **Description:** Sensitive internal files (`src/icc/confirmatory/*`, `scripts/update_revision_log.py`, `results/overnight/EXECUTION_MANIFEST.csv`, `results/results.json`) were never purged from Git history. They were merely deleted in regular commit `0565abc`.
- **Reproduction:**
  ```powershell
  git checkout e3f54cc0951d173f0e13a4b524628328f318e746 -- src/icc/confirmatory
  ```
- **Expected:** Complete removal of sensitive objects across all commits, trees, tags, and PR refs on GitHub.
- **Actual:** All sensitive files, manifests, and commit logs are fully retrievable from any local clone or remote GitHub reference.
- **Impact:** Public confidentiality exposure of private validation results, historical manifests, and internal research methodology.
- **Recommended Fix:** Execute `git-filter-repo` across the remote repository, coordinate force-push to `main`, and purge GitHub pull request refs and server-side cache via GitHub Support.
- **Regression Test Needed:** Automated pre-push hook scanning all rev-list objects for sensitive file paths and keywords.

---

### Item P0-02: Invalid Clinical Diagnostic Certainty Claims for Conformal Clustering
- **File / Location:** `src/cicc/conformal.py#L123-L133`, `examples/realtime_patient_projection.py#L80-L115`, `docs/theory.md#Sec 9.1`.
- **Description:** Conformal calibration guarantees $(1 - \alpha)$ coverage *only* for the model's self-generated centroid argmax pseudo-labels. In real clinical cohorts, coverage against true biological diagnoses collapses to 62.2% on Leukemia, 37.0% on SRBCT, and 46.7% in the real-time patient demonstration, producing 20% confident toxic misclassifications (ALL classified as AML with $P > 0.99$).
- **Reproduction:**
  ```powershell
  python examples/realtime_patient_projection.py
  ```
- **Expected:** Transparent disclosure that conformal coverage applies to internal cluster assignments, or calibration on labeled ground-truth cohorts.
- **Actual:** Advertised as providing "guaranteed 90% diagnostic certainty sets" for clinical oncology.
- **Impact:** Catastrophic diagnostic patient safety risk if deployed in clinical decision support.
- **Recommended Fix:** Retract clinical certainty claims from documentation; formally document pseudo-label coverage boundaries; update `realtime_patient_projection.py` to evaluate against verified pathology.
- **Regression Test Needed:** Conformal evaluation suite reporting empirical coverage on both pseudo-labels and ground-truth pathology across benchmark cohorts.

---

## 3. Priority P1: High Priority Issues

### Item P1-01: AutoK Model Order Selection Total Collapse to $K_{min}$
- **File / Location:** `src/icc/consensus/autok.py#L86-L92`, `L165-L171`, `L209-L210`.
- **Description:** Inner products between $L_1$ row-normalized vectors $B_{\text{norm}}$ are bounded by $K/L \le 0.125$, falling strictly below the ambiguity threshold $u_1 = 0.10$. This causes $\text{PAC}(K) \equiv 0.0000$ identically for all candidate $K$, collapsing AutoK to $K_{min}$ in 100.0% of trials (510/510 runs).
- **Reproduction:**
  ```powershell
  python results/post_refactor_verification/auto_k/run_adversarial_autok_benchmarks.py
  ```
- **Expected:** Selection of optimal $K$ based on true data clustering structure.
- **Actual:** 100% collapse to $K_{min}$ regardless of true cluster count or SNR.
- **Impact:** Complete failure of automated model order selection.
- **Recommended Fix:** Compute pairwise pseudo-co-associations via cosine similarity of unnormalized bipartite rows ($B_i \cdot B_j / (\|B_i\|_2 \|B_j\|_2)$) and implement Occam's parsimony rule.
- **Regression Test Needed:** Adversarial test suite asserting $K_{\text{PAC}} = K_{\text{true}}$ on well-separated Gaussian clusters ($K=2, 3, 4, 5$).

---

### Item P1-02: Decoy Feature Gating Breakdown and 100% FDR Under Null
- **File / Location:** `src/cicc/decoy.py#L80-L89`, `L122-L128`.
- **Description:** Gaussian decoys are sampled independently ($\text{Cov}(X, \tilde{X}) = 0$), violating exchangeability. Post-clustering double-dipping biases null statistics ($\Pr(W_j > 0) \approx 61\%$). When target FDR fails, line 122 selects `positive_W[-1]`, forcing false positive selections and 100% empirical FDR under null regimes.
- **Reproduction:**
  ```powershell
  python results/post_refactor_verification/knockoff/test_knockoff_simulation.py
  ```
- **Expected:** Return empty set ($\emptyset$) when target FDR cannot be met; control empirical FDR $\le q$.
- **Actual:** 100% empirical FDR across all pure null regimes.
- **Impact:** False discovery claims in published scientific analysis.
- **Recommended Fix:** Replace fallback with `self.selected_indices_ = np.array([], dtype=int)`; implement conditional Model-X knockoff generator.
- **Regression Test Needed:** Monte Carlo simulation asserting $\text{FDR} \le 0.10$ and zero discoveries under pure Gaussian noise.

---

### Item P1-03: Decoupled Feature Gating Dead Code in Inductive Consensus
- **File / Location:** `src/cicc/inductive.py#L147-L179`.
- **Description:** Feature gating stores selected features in `self.selected_features_`, but centroids, calibration labels, conformal calibrator, and `predict()` execute across all $D$ ambient dimensions.
- **Reproduction:** Inspect `src/cicc/inductive.py` lines 153–195; observe that `self.selected_features_` is never used to index `X_disc`, `X_cal`, or prospective `X`.
- **Expected:** Downstream projection and calibration operate on the selected feature subspace.
- **Actual:** Decoy gating is dead code with zero downstream impact.
- **Impact:** Discrepancy between published claims and actual model execution.
- **Recommended Fix:** Slice `X_disc[:, self.selected_features_]` and `X_cal[:, self.selected_features_]` prior to centroid calculation and projection.
- **Regression Test Needed:** Test asserting that noise features excluded by gating do not influence out-of-sample prediction sets.

---

### Item P1-04: Broken Console Scripts in Wheel Package
- **File / Location:** `pyproject.toml#L47-L50`, `src/icc/__main__.py#L11`.
- **Description:** Built wheel excludes `scripts/` from distribution; `icc-run` fails with `ModuleNotFoundError: No module named 'scripts'`; `icc` and `icc-demo` fail with `ModuleNotFoundError: No module named 'demo'`.
- **Reproduction:**
  ```powershell
  pip install results/post_refactor_verification/packaging/icc-2.2.0-py3-none-any.whl
  icc-run --help
  ```
- **Expected:** CLI entry points run cleanly from any directory.
- **Actual:** Unhandled `ModuleNotFoundError` crashes.
- **Impact:** Broken package distribution for pip users.
- **Recommended Fix:** Move CLI entry points into `src/icc/cli/` and update `[project.scripts]`.
- **Regression Test Needed:** CI step installing built wheel into isolated clean virtual environment and running `--help` on all entry points.

---

### Item P1-05: Hardcoded RNG Seed in Dataset Generation
- **File / Location:** `src/icc/data/preprocessing.py#L186`, `src/icc/core.py#L113`.
- **Description:** `build_dataset(seed=...)` accepts a user seed, but line 186 explicitly passes `seed=RNG_DATA_SEED` (`42`) to `make_signal()`. True cluster coordinates and labels are 100% frozen across all seeds.
- **Reproduction:**
  ```powershell
  python results/post_refactor_verification/benchmark_logs/test_seed_propagation.py
  ```
- **Expected:** Distinct seeds generate distinct cluster centers and latent geometries.
- **Actual:** Bitwise identical signal coordinates across all user seeds.
- **Impact:** Invalid multi-seed benchmark evaluations (evaluating only noise variations on a single frozen signal geometry).
- **Recommended Fix:** Pass `seed=seed` to `make_signal()`.
- **Regression Test Needed:** Test asserting $\max |S(\text{seed}_1) - S(\text{seed}_2)| > 0$ for distinct seeds.

---

### Item P1-06: Historical Synthetic Benchmark Claim Falsified
- **File / Location:** `docs/theory.md#Sec 10`, `README.md`.
- **Description:** Historical claim asserted ICC-v2 achieved $\text{ARI}=1.0000$ in $0.1340\text{s}$ while Standard Consensus required $0.3662\text{s}$ on Seed 101. In measured reality, ICC-v2 achieved only $\text{ARI}=0.4396$ ($\Delta\text{ARI} = -0.5604$), while Standard Consensus achieved $\text{ARI}=1.0000$ in $0.1210\text{s}$ (~3x faster than claimed).
- **Reproduction:**
  ```powershell
  python results/post_refactor_verification/benchmark_logs/reproduce_historical_benchmark.py
  ```
- **Expected:** Empirical reproducibility of published benchmark claims.
- **Actual:** Claim refuted on both accuracy and execution speed.
- **Impact:** Misleading scientific claims in public repository documentation.
- **Recommended Fix:** Revise documentation to report verified empirical accuracy and timing.
- **Regression Test Needed:** Benchmark verification suite asserting reported metrics match automated execution logs.

---

## 4. Priority P2: Medium Priority Issues

| Item ID | Component / File | Description | Recommended Fix |
|:---:|---|---|---|
| **P2-01** | `src/icc/datasets/genomics.py#L167` | Pre-split `StandardScaler` leakage across pooled cohort ($N$) before partitioning. | Cache raw arrays; apply scaling strictly on `X_train`. |
| **P2-02** | `src/icc/consensus/icc.py#L243` | Subspace sampling crashes on 1D inputs ($D=1$) with `ValueError` in `rng.choice`. | Clamp `sub_size = max(1, min(len(pool), int(len(pool) * rate)))`. |
| **P2-03** | `src/cicc/conformal.py#L127` | Label non-contiguity crash: `int(labels_cal[i])` raises `IndexError` on non-contiguous labels. | Map labels through `label_to_index` mapping dictionary. |
| **P2-04** | `src/icc/baselines/anchor.py#L27` | Import-time `ConvergenceWarning` on all-zero matrix emitted across 63/68 modules. | Replace with dummy non-degenerate points or simple module import test. |
| **P2-05** | `src/icc/stats/__init__.py#L7` | Missing exports: `wilcoxon_signed_rank_test` and `bonferroni_correction` not in `__all__`. | Import and expose functions in `src/icc/stats/__init__.py`. |
| **P2-06** | `src/icc/benchmarks/runner.py#L187`| 1-second timestamp resolution (`%Y%m%d_%H%M%S`) causes file overwrites. | Use microsecond resolution (`%f`) or UUID run IDs. |
| **P2-07** | `src/icc/benchmarks/runner.py#L85` | YAML config parameters `synthetic_n_samples` and `synthetic_k` ignored; $N=150$ hardcoded. | Read parameters dynamically from active configuration dictionary. |
| **P2-08** | `src/icc/consensus/icc.py#L318` | Stability attribute discontinuity at $N > 2000$ (stores mean affinity instead of stability). | Maintain consistent stability metric across dense and sparse regimes. |

---

## 5. Priority P3: Low Priority / Documentation Issues

| Item ID | Component / File | Description | Recommended Fix |
|:---:|---|---|---|
| **P3-01** | `README.md` | Non-existent `--visualize` CLI parameter documented for `prepare_data.py`. | Remove `--visualize` from CLI documentation. |
| **P3-02** | `docs/usage.md` | Non-existent constructor argument `ASPPConfig(n_bootstrap=10)` documented. | Update documentation to `n_base_models=5`. |
| **P3-03** | `src/icc/datasets/registry.py#L20`| Import-time filesystem mutation (`_DEFAULT_CACHE.mkdir(...)`). | Move directory creation inside `load_dataset()`. |
| **P3-04** | `src/icc/experiments/*.py` | Missing explicit `__all__` in compatibility shims (`getattr` returns `None`). | Declare explicit `__all__` matching `icc.benchmarks.*`. |
| **P3-05** | `src/icc/algorithms/__init__.py` | Contract mismatch in `list_models()` (returns 41 keys vs 14 display names). | Document distinction or expose unified model query helper. |
