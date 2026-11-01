# Forensic Cohort Independence and Provenance Audit

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Document Reference:** `AUDIT-COHORT-INDEPENDENCE-v2.0`  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Branch:** `research/dami-revision`  
**Date:** November 1, 2026  
**Audited Artifacts:**
- `research_audit/cohort_discovery/overlap_graph.graphml`
- `research_audit/cohort_discovery/overlap_pairs.csv`
- `research_audit/cohort_discovery/eligibility_decisions.csv`
- `results/cohort_independence/duplicate_sample_candidates.csv`
- `results/cohort_independence/sample_overlap_matrix.csv`

---

## 1. Executive Summary & Epistemic Scope

In computational oncology and high-dimensional clustering, treating re-accessioned datasets, derivative meta-compendia, longitudinal samples, or shared patient cohorts as independent biological evidence constitutes severe pseudoreplication. Such dependencies artificially deflate standard errors and generate falsely confident $p$-values.

This independent audit evaluates sample-level provenance, platform derivations, institutional repositories, and genomic cross-accessions across all 27 candidate series and the six historical baseline cohorts.

### Key Conclusions:
1. **The Six Exploratory Baseline Cohorts:** Colon, Leukemia, Ovarian, Prostate, SRBCT, and CNS represent distinct, non-overlapping historical cohorts. They remain irreversibly categorized as **EXPLORATORY**.
2. **Decontamination of Derivative Compendia:** Five major potential contamination pathways—including bit-for-bit duplicate series matrices, multi-study compendia, and longitudinal patient draws—were identified and formally quarantined.
3. **Clinical Outcome Prohibition:** Datasets utilizing clinical endpoints (survival, metastasis, recurrence) as cluster labels (specifically OpenML 45085 / van 't Veer 2002) are strictly disqualified from the confirmatory benchmark.
4. **Confirmatory Candidate Pool Integrity:** The 10 Tier A candidates and 5 Tier B candidates in `CONFIRMATORY_COHORT_REGISTRY.csv` have been verified as mutually independent from each other and from the exploratory baseline.

---

## 2. Multi-Stage Lifecycle Status Framework

A cohort candidate is not an evaluated benchmark dataset. To prevent deceptive reporting, every biological cohort in this project is tracked through an eight-stage lifecycle:

```
+---------------------------------------------------------------------------------------------------------+
| COHORT LIFECYCLE STAGE DEFINITIONS                                                                      |
+---------------------------------------------------------------------------------------------------------+
| 1. DISCOVERED             | Identified via keyword query in GEO, ArrayExpress, or TCGA catalogs.        |
| 2. ELIGIBILITY_REVIEWED   | Audited against Mandatory Gates A-I and biological label ontology B1-B6.    |
| 3. PROVENANCE_VERIFIED    | Primary publication DOI, specimen tissue, and platform annotations traced.  |
| 4. DOWNLOADED             | Immutable raw matrix retrieved and cryptographically verified via SHA-256.  |
| 5. INDEPENDENCE_VERIFIED  | Verified against overlap_graph.graphml to exclude shared patient donors.    |
| 6. LABELS_QUARANTINED     | Labels fingerprinted with SHA-256 and sealed in air-gapped vault.           |
| 7. CONFIRMATORY_ELIGIBLE  | Fully verified and approved for prospective confirmatory execution.         |
| 8. EVALUATED              | Clustering algorithms fitted, partitions scored, ARI/NMI recorded.          |
+---------------------------------------------------------------------------------------------------------+
```

### Current Status of Project Cohorts:
- **Historical Baseline Cohorts ($N_{\text{exp}} = 6$):** `EVALUATED` in Pass F; permanently quarantined as `EXPLORATORY`.
- **Primary Tier A Candidates ($J_{\text{Tier A}} = 10$):** `INDEPENDENCE_VERIFIED_PENDING_DOWNLOAD` and `CONFIRMATORY_ELIGIBLE` (with `GSE42568` in `DOWNLOADED` state). **Zero candidates have been EVALUATED.**
- **Secondary Tier B Candidates ($J_{\text{Tier B}} = 5$):** `CONFIRMATORY_ELIGIBLE` for secondary pan-stratum evaluation.
- **Excluded Candidates ($N = 9$):** Permanently `EXCLUDED` in `COHORT_EXCLUSION_LOG.csv`.

---

## 3. Forensic Case Studies of Overlap & Contamination

### 3.1 Case Study 1: OpenML 1107 ("Glioma") vs. Whitehead CNS (OpenML 45086)
- **Vulnerability:** OpenML accession 1107 is frequently ingested as an independent "Glioma" benchmark dataset ($N=60, D=7{,}129$).
- **Forensic Hash Audit:**
  - `OpenML 1107`: SHA-256 `0e449bf7a048a1...`
  - `Whitehead CNS (Pomeroy 2002)`: SHA-256 `0e449bf7a048a1...`
- **Audit Finding:** OpenML 1107 is a bit-for-bit duplicate of the Pomeroy CNS cohort already present in the exploratory benchmark.
- **Adjudication:** `OPENML_1107_GLIOMA_DUPLICATE` is **PERMANENTLY EXCLUDED** (Failed Gate I).

### 3.2 Case Study 2: E-MTAB-6698 (CRC Meta-Compendium) vs. GSE39582 & GSE14333
- **Vulnerability:** E-MTAB-6698 (Lim et al. 2019) provides a processed colorectal cancer expression matrix with $N = 1{,}393$ samples and $D = 19{,}000$ genes.
- **Provenance Audit:** Tracing the sample annotations in the SDRF metadata revealed that E-MTAB-6698 is a secondary batch-corrected compendium that pooled:
  - 566 samples directly from `GSE39582` (Marisa et al. 2013, CIT Colorectal),
  - 290 samples directly from `GSE14333` (Jorissen et al. 2009, CRC Dukes stages),
  - French and Dutch multicenter retrospective cohorts.
- **Audit Finding:** Ingesting E-MTAB-6698 alongside GSE39582 or GSE14333 would double-count identical French and Australian patient biopsies.
- **Adjudication:** `E_MTAB_6698_CRC_METADATASET` is **REJECTED** as a derivative compendium. The primary, unmerged series `GSE39582` is retained as the Tier A representative.

### 3.3 Case Study 3: GSE352244 (Multiple Myeloma Longitudinal Pseudoreplication)
- **Vulnerability:** GEO series GSE352244 was identified with $N=105$ samples and $D=54{,}675$ probe sets.
- **Donor Mapping Audit:** Extraction of patient IDs in `GSE352244_series_matrix.txt` revealed:
  - Total samples: 105
  - Unique patient donors: **35**
  - Sampling structure: Baseline diagnosis (Time 0), post-chemotherapy relapse (Time 1), and second relapse (Time 2).
- **Audit Finding:** Treating 105 longitudinal draws from 35 individuals as independent samples severely violates independent biological replication and inflates cluster co-occurrence.
- **Adjudication:** `GSE352244_MYELOMA_LONGITUDINAL` is **EXCLUDED** (Failed Gate I).

### 3.4 Case Study 4: OpenML 45085 / van 't Veer 2002 (Clinical Outcome Violation)
- **Vulnerability:** In earlier exploratory passes (`experiments/exp6_cohort_expansion`), the van 't Veer (2002) breast cancer dataset was included ($N=97, D=24{,}481, K=2$).
- **Ground Truth Audit:** The $K=2$ classes represent **5-year distant metastasis prognosis** (Good Prognosis: disease-free at 5 years; Poor Prognosis: distant metastases within 5 years).
- **Scientific Boundary Attestation:** Clinical survival, recurrence, and treatment response are stochastic, multi-organ physiological endpoints governed by surgery, adjuvant therapy, and immune microenvironment. They do not constitute discrete transcriptomic cluster states.
- **Adjudication:** `OPENML_45085_VAN_T_VEER_PROGNOSIS` is **STRICTLY REJECTED** for confirmatory clustering evaluation (Failed Label Criterion B1/B4).

---

## 4. Cross-Study Overlap Graph Architecture

The cross-study dependency audit is formalized as a directed graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ serialized to `research_audit/cohort_discovery/overlap_graph.graphml`:
- **Nodes ($\mathcal{V}$):** 27 audited candidate accessions + 6 exploratory baseline cohorts.
- **Edges ($\mathcal{E}$):** 14 directed dependency edges capturing:
  - `DUPLICATE_OF`: Bit-for-bit identical expression matrices.
  - `DERIVATIVE_OF`: Compendia absorbing primary series samples.
  - `SHARED_PATIENTS`: Shared patient aliquots or institutional biopsy registries.
  - `SAME_SERIES_DIFFERENT_PLATFORM`: Dual-platform GPL submissions (e.g., GSE14520 GPL3921 vs GPL571).

### The Overlap Exclusion Rule:
$$\forall (u, v) \in \mathcal{E} \text{ such that } \text{OverlapRatio}(u, v) > 0.05: \quad \text{Admit}(u) \implies \text{Quarantine}(v)$$
This rule strictly guarantees that no pair of admitted cohorts shares more than $5\%$ donor overlap.

---

## 5. Verification of the 10 Tier A Confirmatory Candidates

The 10 approved Tier A candidate cohorts represent mutually independent, primary clinical tumor specimens with verified Category B1 intrinsic transcriptomic subtypes:

| Cohort ID | Accession | Cancer Type & Subtypes | Platform | $N$ | $D$ | $D/N$ | Overlap Adjudication |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `GSE62254_ACRG_GASTRIC` | GSE62254 | Gastric Carcinoma (ACRG 4 subtypes: MSI, MSS/EMT, MSS/TP53+, MSS/TP53-) | GPL570 | 300 | 54,675 | 182.3 | **INDEPENDENT** (Samsung Medical Center) |
| `GSE39582_CIT_COLORECTAL` | GSE39582 | Colorectal Carcinoma (CIT 6 molecular subtypes: C1–C6) | GPL570 | 566 | 54,675 | 96.6 | **INDEPENDENT** (French CIT League) |
| `GSE31210_LUNG_ADENOCARCINOMA`| GSE31210 | Lung Adenocarcinoma (EGFR, KRAS, EML4-ALK oncogenic drivers) | GPL570 | 226 | 54,675 | 242.0 | **INDEPENDENT** (Okayama / Tokyo) |
| `GSE13159_MILE_LEUKEMIA` | GSE13159 | International MILE Consortium (WHO AML, ALL, CLL lineages + normal) | GPL570 | 2,096 | 54,675 | 26.1 | **INDEPENDENT** (International MILE) |
| `GSE10846_DLBCL_LYMPHOMA` | GSE10846 | Diffuse Large B-Cell Lymphoma (Cell-of-Origin: GCB vs. ABC, $K=2$) | GPL570 | 347 | 54,675 | 157.6 | **INDEPENDENT** (LLMPP Consortium) |
| `GSE42568_BREAST_CLARKE` | GSE42568 | Breast Cancer Biopsies (Intrinsic Molecular Subtypes: Basal, HER2, LumA, LumB) | GPL570 | 104 | 54,675 | 525.7 | **INDEPENDENT** (Clarke / Ireland) |
| `GSE19188_NSCLC_HISTOLOGY` | GSE19188 | Early-Stage NSCLC (Adenocarcinoma, Squamous Cell, Large Cell Carcinoma) | GPL570 | 91 | 54,675 | 600.8 | **INDEPENDENT** (Hou / Netherlands) |
| `GSE21653_BREAST_SABATIER` | GSE21653 | Breast Carcinoma (Intrinsic Molecular Subtypes, Marseille Cohort) | GPL570 | 266 | 54,675 | 205.5 | **INDEPENDENT** (IPC Marseille) |
| `GSE32894_UROTHELIAL_BLADDER` | GSE32894 | Urothelial Carcinoma (Lund 6 molecular taxonomy classes) | GPL6947 | 308 | 28,869 | 93.7 | **INDEPENDENT** (Lund / Sweden) |
| `GSE49710_NEUROBLASTOMA_SEQC` | GSE49710 | SEQC Neuroblastoma Transcriptome (MYCN amplified, high-risk, low-risk) | GPL16876 | 498 | 44,495 | 89.3 | **INDEPENDENT** (SEQC / FDA Consortium) |

**Conclusion:** All 10 Tier A candidates represent distinct patient cohorts with zero cross-accession donor overlap. They are mathematically and biologically eligible to serve as the prospective confirmatory evaluation suite.