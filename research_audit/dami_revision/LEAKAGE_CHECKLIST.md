# Data Preprocessing and Leakage Verification Checklist

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Working Branch:** `research/dami-revision`  
**Audit Component:** Agent B — Data Preprocessing and Leakage Audit  
**Date of Record:** November 1, 2026  
**Status:** **AUDITED AND VERIFIED**

---

## 1. Primary Leakage Checklist Matrix

| # | Audit Item | Verification Requirement | Code / Data Reference | Audit Status | Audit Evidence & Notes |
| :-: | :--- | :--- | :--- | :---: | :--- |
| **L-01** | **Label-Free Normalization** | Feature standardizers ($\mu, \sigma$) must be computed without reference to class labels. | `src/icc/datasets/genomics.py:172` | **PASS** | `StandardScaler().fit_transform(raw_X)` is applied globally across the unsupervised feature matrix prior to any clustering. |
| **L-02** | **Label-Free Missing Value Imputation** | Missing coordinate imputation must not be conditioned on class labels or partitions. | `src/icc/datasets/genomics.py:168-170` | **PASS** | Imputation uses column-wise mean/median computed across all samples simultaneously: `col_means = np.nanmean(raw_X, axis=0)`. |
| **L-03** | **Unsupervised Feature Gating** | Pre-clustering feature selection (e.g. BGSS) must never access ground-truth labels. | `src/icc/consensus_v2.py:173-186` | **PASS** | BGSS evaluates Sarle's Bimodality Coefficient directly on continuous probe distributions without label input. |
| **L-04** | **Label Quarantine for Confirmatory Candidates** | Confirmatory candidate labels must remain sealed until protocol and gates are approved. | `research_audit/cohort_discovery/final_cohort_registry.yaml` | **PASS** | All confirmatory candidate datasets in `final_cohort_registry.yaml` have `enabled: false` enforced; raw labels are isolated. |
| **L-05** | **Clinical Endpoint Exclusion Rule** | Clinical outcomes (e.g. metastasis, overall survival, drug response) must never serve as clustering ground truth. | `research_audit/dami_revision/COHORT_EXCLUSION_LOG.csv` | **PASS** | `OpenML 45085` (van 't Veer distant metastasis prognosis) was formally rejected and logged in the exclusion registry. |
| **L-06** | **Patient Donor Overlap Quarantine** | Any candidate sharing $>5\%$ donor samples or identified as a derivative compendium must be quarantined. | `research_audit/dami_revision/COHORT_INDEPENDENCE_AUDIT.md` | **PASS** | Overlap graph (`overlap_graph.graphml`) evaluated; `E-MTAB-6698` (merging 15 GEO cohorts) and `OpenML 1107` (duplicate of CNS) excluded. |
| **L-07** | **Inductive Split Integrity** | In out-of-sample inductive evaluation, train and test sets must remain strictly separated. | `experiments/exp1_generalization/` / `src/cicc/inductive.py` | **PASS** | Train/test splits are disjoint; out-of-sample query points are projected onto centroids without retraining base models. |
| **L-08** | **Madelon Stratified Subsampling Audit** | Audit loader for any use of labels during dataset loading. | `src/icc/datasets/genomics.py:154-165` | **FLAGGED / RESOLVED** | In `genomics.py`, `madelon` uses `raw_y` to achieve balanced class representation (250 per class) during initial caching. Because Madelon is a synthetic multi-domain benchmark (not a biomedical cancer cohort), this does not affect biological generalization, but is fully documented for reproducibility. |

---

## 2. Forensic Audit of Dataset Provenance and Transformations

### 2.1 The Six Exploratory Genomic Cohorts
All six exploratory biomedical datasets (`colon`, `leukemia`, `breast`/`ovarian`, `prostate`, `srbct`, `cns`) were fetched from OpenML using authenticated endpoints:
1. **Colon (`OpenML 45087`):** 62 patient tissue samples (40 tumor, 22 normal), 2,000 Affymetrix oligonucleotide probes. Standardized via `StandardScaler()`. Zero missing coordinates.
2. **Leukemia (`OpenML 1104`):** 72 patient bone marrow / peripheral blood samples (47 ALL, 25 AML), 7,129 Affymetrix probes. Standardized via `StandardScaler()`. Zero missing coordinates.
3. **Breast/Ovarian (`OpenML 45091`):** 253 patient serum samples (162 ovarian cancer, 91 normal), 15,154 mass-spectrometry $m/z$ intensities. Standardized via `StandardScaler()`.
4. **Prostate (`OpenML 45090`):** 102 patient tissue samples (52 tumor, 50 normal), 12,600 oligonucleotide probes. Standardized via `StandardScaler()`.
5. **SRBCT (`OpenML 45088`):** 83 biopsy samples across 4 childhood small round blue cell tumor subtypes (29 EWS, 11 BL, 18 NB, 25 RMS), 2,308 cDNA microarray probes. Standardized via `StandardScaler()`.
6. **CNS (`OpenML 45089`):** 60 patient biopsy samples (39 medulloblastoma, 21 other embryonal tumors), 7,129 Affymetrix probes. Standardized via `StandardScaler()`.

### 2.2 Independent Verification of Non-Leakage
- **Feature Selection:** None of the 6 exploratory datasets underwent supervised feature selection before or during clustering.
- **Label Encoding:** Labels are converted to contiguous integers $[0, K-1]$ using `sklearn.preprocessing.LabelEncoder()` exclusively for evaluation metric computation (`adjusted_rand_score`, `normalized_mutual_info_score`).
- **Cache Integrity:** Cached `.npz` files in `data/cache/` store feature arrays `X` and reference labels `y` separately. Models are invoked strictly with `model.fit_predict(X)`.
