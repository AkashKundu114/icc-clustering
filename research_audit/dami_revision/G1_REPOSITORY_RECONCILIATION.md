# Phase A: Repository and Provenance Reconciliation Report

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Working Branch:** `research/dami-revision`  
**Current HEAD Commit:** `b12be26be02ab0ee3ef524455d9b13e29101a6af`  
**Starting Scientific Baseline:** `ab6be28ea5ded77ef5deb5f8cfab0a462c12c88f`  
**Date of Record:** November 1, 2026  
**Status:** **PHASE A RECONCILIATION COMPLETE — REPOSITORY PROVENANCE VERIFIED**  

---

## 1. Git Provenance, Branch Synchronization, and Safety Controls

A comprehensive forensic inspection of the repository's git infrastructure confirms the following operational baseline:

### 1.1 Branch and Remote Synchronization
- **Active Working Branch:** `research/dami-revision`.
- **Remote Configuration:** Remote `icc-remote` mapped to `https://github.com/AkashKundu114/icc-clustering.git`.
- **Synchronization State:** The local branch is ahead of `icc-remote/research/dami-revision` by exactly 1 commit (`b12be26`). It is ready to push upon human authorization.
- **Branch Isolation:** No changes have been merged into `main`, nor has any other research branch (`research/holdout-801010`, `research/cohort-discovery`, `research/overnight-experiments`) been overwritten.

### 1.2 Status of Pre-Registration Tag `prereg-dami-v1`
- **Audit Verification:** Execution of `git tag -l "prereg-dami-v1"` returns **null**.
- **Finding:** Neither a local nor a remote git tag named `prereg-dami-v1` exists.
- **Safety Attestation:** The tag is strictly quarantined and shall not be generated, signed, or pushed until the human investigator provides explicit authorization following Gate G1 review.

### 1.3 Confirmatory Experiment Execution Status
- **Audit Verification:** Inspection of `results/`, `experiments/`, and process tables confirms that **zero confirmatory experiments (E1 through E8) have been launched**.
- **Finding:** The confirmatory testing grid remains completely unexecuted and sealed.

---

## 2. Immutable Result Store Inventory & Forensic Integrity

The repository maintains frozen result stores from earlier exploratory benchmark passes. These files serve as the immutable single source of truth for all historical descriptive claims:

### 2.1 Frozen Store Directory Matrix

| Store Path | Role & Scientific Scope | Number of Model Fits | Status | Cryptographic Integrity |
| :--- | :--- | :---: | :---: | :--- |
| `results/passF/benchmark_matrix_passF.csv` | 13 multi-domain benchmarks (Pass F, 30 seeds high-D, 10 seeds general) | 3,000 | **IMMUTABLE** | Frozen; SHA verified |
| `results/passF/fair_baselines_30seeds_passF.csv` | 8 fair comparative baselines across 6 high-D cohorts (30 seeds) | 1,440 | **IMMUTABLE** | Frozen; SHA verified |
| `results/passF/ablation_30seeds_passF.csv` | Factorial architectural ablations (V0 through V6, 30 seeds) | 1,260 | **IMMUTABLE** | Frozen; SHA verified |
| `results/passF/ablation_stats_passF.json` | Recomputed bootstrap effect sizes and Wilcoxon statistics | N/A | **IMMUTABLE** | Matches `passF/` |
| `results/results.json` | Historical baseline registry | N/A | **IMMUTABLE** | Archived |
| `results/stats.json` | Canonical macro source for `paper/numbers.tex` | N/A | **ACTIVE / FROZEN** | Verified by `tools/check_consistency.py` |
| `results/study_null_gating/` | Exploratory feature gating breakdown experiments | 18,000 | **IMMUTABLE** | Archived exploratory store |

**Integrity Rule:** These result stores represent exploratory development history. No script, pipeline, or commit during this mission has modified or overwritten these files.

---

## 3. Discovered Candidates vs. Evaluated Benchmark Cohorts

A critical deficiency in earlier documentation was the ambiguous usage of the term "10 Category A cohorts", conflating candidate accessions discovered in search catalogs with actively evaluated benchmark datasets.

### 3.1 Transparent Epistemic Classification

```
+---------------------------------------------------------------------------------------+
| COHORT UNIVERSE LIFECYCLE DEMARCATION                                                 |
+---------------------------------------------------------------------------------------+
|  Level 1: Discovered Candidate Accessions (N = 339 GEO Series Records)                 |
|  - Raw repository query hits in candidate_catalog.csv                                 |
+---------------------------------------------------------------------------------------+
|  Level 2: Audited Forensic Candidate Pool (N = 27 Cohorts)                            |
|  - Evaluated against Mandatory Gates A-I in eligibility_decisions.csv                 |
+---------------------------------------------------------------------------------------+
|  Level 3: Approved Confirmatory Candidates (J = 15 Planned)                           |
|  - Tier A Intrinsic Subtypes (J = 10 Candidates): GSE62254, GSE39582, GSE31210, etc.  |
|  - Tier B General Phenotypes (J = 5 Candidates): GSE25066, GSE14520, GSE2034, etc.   |
|  Status: PROVENANCE_VERIFIED / CONFIRMATORY_ELIGIBLE (Zero runs executed)             |
+---------------------------------------------------------------------------------------+
|  Level 4: Active Evaluated Benchmark Suite (N = 13 Datasets, 3,000 Model Fits)        |
|  - 6 Exploratory High-D Biomedical Cohorts: colon, leukemia, ovarian, prostate, srbct, cns |
|  - 7 General Non-Genomic Datasets: madelon, waveform, sonar, isolet, etc.              |
|  Status: FROZEN EXPLORATORY BASELINE (Pass F results store)                           |
+---------------------------------------------------------------------------------------+
```

### 3.2 Reconciliation of the "10 Category A Cohorts" Claim
- **Audit Truth:** The claim that the study has "10 Category A cohorts" refers strictly to **10 validated independent candidate accessions** identified during cohort discovery (`research_audit/cohort_discovery/execution_report.md` and `eligibility_decisions.csv`) that meet all Tier A inclusion gates (human cancer tissue, bulk transcriptomic assay, $N \ge 30, D \ge 500, D/N \ge 5$, Category B1 biological ground truth, open license).
- **Physical Download Status:** Of these 10 candidates, only one series matrix (`GSE42568`) has been physically downloaded to `data/raw/cohort_discovery/` as a discovery proof-of-concept. The remaining 9 candidates are cataloged in `download_manifest_reviewed.csv` with verified FTP endpoints and SHA-256 target fingerprints, awaiting post-G1 execution in Experiment E4.
- **Evaluated Cohorts:** The **only cohorts currently evaluated in the benchmark** are the six historical exploratory cohorts (`colon`, `leukemia`, `ovarian`, `prostate`, `srbct`, `cns`).
- **Protocol Harmonization:** All revised protocol documents explicitly label the 10 Tier A datasets as **confirmatory candidate cohorts**, eliminating any implication that they have already been evaluated.

---

## 4. Reconciled Commit Provenance on `research/dami-revision`

The revision history on `research/dami-revision` reflects a clean, auditable trajectory:
1. `ab6be28` (Starting Baseline): Finalized Phase 0 baseline reports and disposition matrix.
2. `4624b6c` (Phase 0 Audit Completion): Forensic claims audit, baseline verification, and initial protocol drafting.
3. `b12be26` (Current HEAD): Formal protocol remediation, bifurcating H1, implementing TOST equivalence for H3, establishing multiplicity families, conducting dual-subagent independent reviews, and locking operational parameter contracts.

**Working Tree Status:** Clean. All modifications are committed and tracked.