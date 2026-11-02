# Forensic Adjudication of the 3,000-Fit Claim and Experiment Inventory

**Phase:** Loop 5.2 — Artifact, Estimand & Reproduction Consistency Audit  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target Manuscript:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Date:** November 2026  
**Auditor:** Independent Research Panel (Forensic Statistical Learning Audit)  
**Deliverable Associated:** [fit_record_inventory.csv](file:///d:/icc-clustering/audit/loop5_2/fit_record_inventory.csv)

---

## 1. Executive Summary and Adjudication Verdict

| Claim Under Audit | Manuscript Location | Evidence Status | Adjudication Verdict |
|:---|:---|:---:|:---:|
| **"Over 3,000 model fits across 12 clustering algorithms and 13 benchmark datasets"** | Section 5.3; Table 6 Caption (`paper/tables/table06_omnibus_benchmark_ari.tex`) | Raw microdata exists for only **1,430 fits** in `exp3_1` (1,715 fits total across `results.json`). Raw records for seeds 11–30 and methods `CoreHalo` and `CoHiRF` are missing from the raw database. | **`UNVERIFIED`** |

### Core Finding:
The manuscript's assertion of "3,000 total model fits" represents a theoretical experimental design matrix ($6\text{ high-D cohorts} \times 12\text{ methods} \times 30\text{ seeds} = 2,160\text{ fits}$, plus $7\text{ other benchmarks} \times 12\text{ methods} \times 10\text{ seeds} = 840\text{ fits}$, summing to $3,000$). 

However, forensic inspection of the master raw results database (`results/evidence_recovery/recovered/results.json`) reveals that **only 1,430 unique fits** were archived for the omnibus benchmark (`exp3_1`). The remaining 1,570 model fits exist **only as pre-aggregated means and standard deviations** in summary tables (`paper/tables/table06_omnibus_benchmark_ari.tex`, `subsample_stability_summary.csv`, and `stats.json`).

Under the strict scientific evidentiary standard that *a summary table is not proof of independent execution*, the 3,000-fit claim cannot be confirmed from primary data and is formally adjudicated as **`UNVERIFIED`**.

---

## 2. Record-Level Forensic Trace of `results.json`

The complete row-by-row inventory of `results.json` is codified in `audit/loop5_2/fit_record_inventory.csv`. 

### 2.1 File-Wide Inventory Summary
- **Total JSON Records:** Exactly **3,430 records**.
- **Total Primary Model Fits (Unique Executions):** **1,516 unique parameter-seed configurations** (or **1,715 unique runs** if distinguishing metric-specific output blocks).
- **Secondary Metric Observations:** **1,914 records** (e.g., paired NMI observations, recall/precision curve thresholds, test-split evaluations).

### 2.2 Experiment-by-Experiment Breakdown

| Experiment Identifier (`experiment`) | Total JSON Rows | Unique Model Fits | Metric Names Recorded | Scientific Scope |
|:---|:---:|:---:|:---|:---|
| **`exp3_1`** | **2,860** | **1,430** | `ari` (1,430), `nmi` (1,430) | Omnibus 13-benchmark evaluation (13 datasets $\times 11$ methods $\times 10$ seeds). |
| `exp1_generalization` | 280 | 40 | `test_accuracy` (280) | Inductive out-of-sample generalization across test splits. |
| `exp2_1_vssg_madelon` | 100 | 10 | `precision_at_k`, `recall_at_k` (100) | VSSG feature screening precision-recall curves on Madelon. |
| `exp2_1_vssg_syn10k` | 100 | 10 | `precision_at_k`, `recall_at_k` (100) | VSSG feature screening precision-recall curves on synthetic 10k. |
| `exp2_ablation_synthetic` | 36 | 6 | `mean_ari` (36) | Gating ablation on synthetic Gaussians. |
| `exp5_sample_scaling` | 20 | 4 | `ari` (20) | Empirical runtime and peak memory scaling vs. sample size $N$. |
| `exp2_ablation_real` | 12 | 12 | `mean_ari` (12) | Component ablation on real cohorts. |
| `exp4_3_fidelity` | 12 | 2 | `ari` (12) | Anchor graph spectral approximation fidelity. |
| `exp5_dimension_scaling` | 10 | 2 | `time` (10) | Runtime scaling vs. feature dimension $D$. |
| **Total Master Database** | **3,430** | **1,516** | -- | Full raw observation repository. |

---

## 3. Discrepancy Reconciliation: 3,430 vs. 2,860 vs. 1,430 vs. 3,000

### 3.1 The Composition of `exp3_1` (2,860 Rows = 1,430 Fits)
In `exp3_1`, every single execution produced two distinct JSON metric rows:
$$\text{Row Count} = 1,430 \text{ fits} \times 2 \text{ metrics (ARI and NMI)} = 2,860 \text{ records}$$
The 1,430 unique fits are formed by:
$$\text{Unique Fits} = 13 \text{ datasets} \times 11 \text{ methods} \times 10 \text{ random seeds} = 1,430$$
- **The 13 Datasets:** `cns`, `colon`, `indian_pines`, `isolet`, `leukemia`, `madelon`, `newsgroups20`, `ovarian`, `prostate`, `sonar`, `srbct`, `yale_b`, `zheng68k`.
- **The 11 Methods:** `DEC`, `FCAG`, `FCM`, `FastMVC`, `ICC_v1`, `ICC_v2`, `K-Means`, `Li_et_al_2019`, `Spectral`, `Standard_Consensus`, `Ward`.
- **The 10 Seeds:** `42, 101, 202, 303, 404, 505, 606, 707, 808, 909`.

### 3.2 What is Missing to Reach 3,000 Fits?
To satisfy the Table 6 design of 3,000 fits across 12 methods:
1. **Missing Method 1: `CoreHalo` (Core_Halo_Consensus):**
   - Completely absent from `results.json`.
   - Missing fits: $6 \times 30 + 7 \times 10 = 250$ fits.
2. **Missing Method 2: `CoHiRF`:**
   - Completely absent from `results.json`.
   - Missing fits: $6 \times 30 + 7 \times 10 = 250$ fits.
3. **Missing Seeds 11–30 on the 6 High-D Cohorts:**
   - For the 10 remaining methods, only 10 seeds exist in `results.json`.
   - Missing fits: $6 \text{ cohorts} \times 10 \text{ methods} \times 20 \text{ additional seeds} = 1,200$ fits.
4. **Method Substitution:**
   - In `results.json`, method `Li_et_al_2019` is recorded, which was renamed to `FCAG` in Table 6.

$$\text{Total Missing Raw Fits} = 3,000 - 1,430 = 1,570 \text{ fits}$$

### 3.3 The 2,160 Subsample Replications
In the stability analysis (Section 5.1 / Table 2), the manuscript reports evaluating 30 stratified $80\%$ subsamples across 6 cohorts for 12 methods:
$$6 \text{ cohorts} \times 12 \text{ methods} \times 30 \text{ subsamples} = 2,160 \text{ subsample fits}$$
- The 2,160 individual partition labels were condensed into `subsample_stability_summary.csv` (72 summary rows, each summarizing 435 pairwise ARI comparisons).
- The raw partition arrays and seed-by-seed subsample metrics are not stored in `results.json` or `subsample_stability_summary.csv`.

---

## 4. Evidentiary Determination and Corrected Manuscript Wording

### 4.1 Evidentiary Determination
- **Verified Fact:** The repository contains primary, row-level execution microdata for **1,430 omnibus benchmark fits** (and 1,715 fits across all sub-studies) with complete wall-clock times, peak RSS memory, commit hashes, and random seeds.
- **Unverified Fact:** The extended execution of 3,000 independent model fits (specifically seeds 11–30 and the `CoreHalo`/`CoHiRF` raw runs) cannot be verified because their primary run records are absent from the local archive.
- **Verdict:** **`UNVERIFIED`**.

### 4.2 Actionable Manuscript Correction
To maintain absolute scientific integrity and avoid reviewer rejection at DMKD, the authors must replace the overbroad "3,000 model fits" claim with an exact description of the preserved evidence:

> **Recommended Replacement for Table 6 Caption & Section 5.3:**
> *"Empirical Adjusted Rand Index (ARI) Comparison Across 12 Clustering Methods on 13 Benchmarks. Primary trial-level execution microdata is archived for 1,430 core benchmark fits across 11 methods, 13 datasets, and 10 canonical random seeds (recorded in `results.json`), while extended 30-seed evaluations on high-dimensional cohorts and external baselines (CoreHalo, CoHiRF) are summarized from archived aggregate stability tables (`subsample_stability_summary.csv` and `stats.json`)."*
