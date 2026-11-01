# Forensic Audit Report: Curated Literature Leads, ArrayExpress, and Multi-Source Oncology Cohorts

**Document Reference:** `research_audit/cohort_discovery/literature_leads_audit_report.md`  
**JSON Catalog:** `research_audit/cohort_discovery/literature_leads_catalog.json`  
**Date:** 2026-11-01  
**Auditor:** Agent 2 & Agent 4 (Curated Literature, ArrayExpress, and Multi-Source Discovery Specialist)  
**Protocol:** `research_audit/cohort_discovery/COHORT_DISCOVERY_ELIGIBILITY_SPEC.md`  
**Branch:** `research/cohort-discovery`  

---

## 1. Executive Summary

In accordance with the ICC biological cohort expansion protocol and `COHORT_DISCOVERY_ELIGIBILITY_SPEC.md`, a systematic forensic examination was performed across **24 candidate oncology cohorts** from three major sources:
1. **Curated Literature Leads (GEO):** 17 landmark published bulk oncology cohorts spanning 8 organ sites (gastric, colorectal, lung, liver, breast, neuroblastoma, leukemia, lymphoma, bladder).
2. **ArrayExpress / BioStudies:** 3 candidate accessions (E-MTAB-669 compendia, E-MTAB-3732 reference atlas, and E-MTAB-1980 ccRCC primary cohort).
3. **NCI Genomic Data Commons (TCGA Harmonized RNA-seq):** 4 major TCGA cohorts (TCGA-BRCA, TCGA-LUAD, TCGA-COAD, TCGA-GBM).

Every cohort was audited against **Mandatory Gates A–I**, classified under the **B1–B6 label ontology**, and assigned to quantitative tiers.

### Key Classification Results:
- **Tier A (Confirmatory Bulk High-$D$ Benchmark):** **13 cohorts** ($N \ge 30, D \ge 500, D/N \ge 5$, verified B1 biological subtype/histology/lineage ground truth, clear provenance, open access terms).
- **Tier B (Confirmatory General / Contrast Stratum):** **4 cohorts** (Pass all gates, but labels are receptor status B3, tumor vs normal B2, or multi-platform split).
- **Separate Stratum (Bulk RNA-seq & Multi-Omics):** **5 cohorts** (GSE49710 SEQC RNA-seq, TCGA-BRCA, TCGA-LUAD, TCGA-COAD, TCGA-GBM).
- **Rejected from Primary Stratum (Derivative / Severe Overlap / Cross-Study Batch Corrected):** **2 cohorts** (E-MTAB-669 series and E-MTAB-3732).

---

## 2. Master Summary Table

| Cohort ID | Disease / Tissue | Platform | $N$ | $D$ | $D/N$ | Valid Label & Ontology | Gate A–I Status | Tier / Stratum | Eligibility Decision |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: |
| **GSE62254** | Gastric Adenocarcinoma | Affymetrix U133 Plus 2.0 (GPL570) | 300 | 54,675 | 182.3 | ACRG Subtypes (**B1**, $K=4$) | All PASS | **Tier A** | `ELIGIBLE_FOR_REVIEW` |
| **GSE39582** | Colon Adenocarcinoma | Affymetrix U133 Plus 2.0 (GPL570) | 566 | 54,675 | 96.6 | CIT Subtypes C1-C6 (**B1**, $K=6$) | All PASS | **Tier A** | `ELIGIBLE_FOR_REVIEW` |
| **GSE31210** | Lung Adenocarcinoma | Affymetrix U133 Plus 2.0 (GPL570) | 226 | 54,675 | 241.9 | Driver Mutants (**B1**, $K=4$) | All PASS | **Tier A** | `ELIGIBLE_FOR_REVIEW` |
| **GSE72094** | Lung Adenocarcinoma | Custom Affymetrix 2.0 (GPL15048) | 442 | 23,720 | 53.7 | KRAS/TP53/STK11 Subtypes (**B1**, $K=4$) | All PASS | **Tier A** | `ELIGIBLE_FOR_REVIEW` |
| **GSE14520** | Hepatocellular Carcinoma | Dual U133A (GPL3921 / GPL571) | 488 | 22,277 | 90.2 | Cirrhosis (**B1**) / Tumor vs Norm (**B2**) | All PASS | **Tier B** | `ELIGIBLE_FOR_REVIEW` |
| **GSE25066** | Breast Carcinoma | Affymetrix U133A (GPL96) | 508 | 22,283 | 43.9 | ER Status (**B3**) / PAM50 (**B6**) | All PASS | **Tier B** | `ELIGIBLE_FOR_REVIEW` |
| **GSE49710** | Neuroblastoma | Illumina HiSeq 2000 (GPL16876) | 498 | 43,827 | 88.0 | INSS Stage 1-4, 4S (**B1**, $K=5$) | All PASS | **Separate Stratum (RNA-seq)** | `ELIGIBLE_FOR_REVIEW` |
| **GSE13159** | Leukemia (MILE Cohort) | Affymetrix U133 Plus 2.0 (GPL570) | 2,096 | 54,675 | 26.1 | WHO Leukemia Lineages (**B1**, $K=18$) | All PASS | **Tier A** | `ELIGIBLE_FOR_REVIEW` |
| **GSE42568** | Breast Carcinoma | Affymetrix U133 Plus 2.0 (GPL570) | 104 | 54,675 | 525.7 | ER Status (**B3**) / Tumor vs Norm (**B2**) | All PASS | **Tier B** | `ELIGIBLE_FOR_REVIEW` |
| **GSE2034** | Breast Carcinoma | Affymetrix U133A (GPL96) | 286 | 22,283 | 77.9 | ER Status (**B3**) | All PASS | **Tier B** | `ELIGIBLE_FOR_REVIEW` |
| **GSE19188** | NSCLC (ADC vs SCC) | Affymetrix U133 Plus 2.0 (GPL570) | 128 | 54,675 | 427.1 | Histology ADC vs SCC (**B1**, $K=2$) | All PASS | **Tier A** | `ELIGIBLE_FOR_REVIEW` |
| **GSE21653** | Breast Carcinoma | Affymetrix U133 Plus 2.0 (GPL570) | 266 | 54,675 | 205.5 | Histologic Grade SBR (**B1**, $K=3$) | All PASS | **Tier A** | `ELIGIBLE_FOR_REVIEW` |
| **GSE10846** | DLBCL Lymphoma | Affymetrix U133 Plus 2.0 (GPL570) | 420 | 54,675 | 130.2 | Cell-of-Origin ABC/GCB (**B1**, $K=3$) | All PASS | **Tier A** | `ELIGIBLE_FOR_REVIEW` |
| **GSE14333** | Colorectal Cancer | Affymetrix U133 Plus 2.0 (GPL570) | 290 | 54,675 | 188.5 | Colon Subsite Location (**B1**, $K=3$) | All PASS | **Tier A** | `ELIGIBLE_FOR_REVIEW` |
| **GSE32894** | Bladder Urothelial Ca | Illumina HumanHT-12 (GPL6947) | 308 | 48,803 | 158.5 | Lund Taxonomy Subtypes (**B1**, $K=5$) | All PASS | **Tier A** | `ELIGIBLE_FOR_REVIEW` |
| **GSE41271** | Lung Adenocarcinoma | Illumina HumanWG-6 (GPL6884) | 275 | 48,803 | 177.5 | Histologic Differentiation (**B1**, $K=3$) | All PASS | **Tier A** | `ELIGIBLE_FOR_REVIEW` |
| **GSE88770** | Invasive Lobular Breast | Affymetrix U133 Plus 2.0 (GPL570) | 117 | 54,675 | 467.3 | ILC Histologic Variants (**B1**, $K=3$) | All PASS | **Tier A** | `ELIGIBLE_FOR_REVIEW` |
| **E-MTAB-669** | Multi-Cancer Compendia | Pooled Multi-GEO ComBat Arrays | 634 | 19,574 | 30.9 | Tumor vs Normal (**B2**) | **FAIL Gate I** (Derivative) | **Separate Stratum** | `REJECT_FROM_PRIMARY` |
| **E-MTAB-3732** | Human Tissue Atlas | Curated U133 Plus 2 Compendium | 27,870 | 54,675 | 1.96 | Tissue Lineage (**B1**) | **FAIL Gate I** (Derivative) | **Separate Stratum** | `REJECT_FROM_PRIMARY` |
| **E-MTAB-1980** | ccRCC Kidney Cancer | Affymetrix U133 Plus 2.0 (A-AFFY-44) | 101 | 54,675 | 541.3 | ccRCC Subtypes (**B1**, $K=2$) | All PASS | **Tier A** | `ELIGIBLE_FOR_REVIEW` |
| **TCGA-BRCA** | Breast Invasive Carcinoma | Illumina HiSeq STAR-Counts | 1,098 | 60,660 | 55.2 | PAM50 Subtypes (**B1**, $K=5$) | All PASS | **Separate Stratum (TCGA)** | `ELIGIBLE_FOR_REVIEW` |
| **TCGA-LUAD** | Lung Adenocarcinoma | Illumina HiSeq STAR-Counts | 515 | 60,660 | 117.8 | Expression Subtypes (**B1**, $K=3$) | All PASS | **Separate Stratum (TCGA)** | `ELIGIBLE_FOR_REVIEW` |
| **TCGA-COAD** | Colon Adenocarcinoma | Illumina HiSeq STAR-Counts | 458 | 60,660 | 132.5 | CMS Subtypes 1-4 (**B1**, $K=4$) | All PASS | **Separate Stratum (TCGA)** | `ELIGIBLE_FOR_REVIEW` |
| **TCGA-GBM** | Glioblastoma Multiforme | Illumina HiSeq STAR-Counts | 169 | 60,660 | 358.9 | Verhaak Subtypes (**B1**, $K=4$) | All PASS | **Separate Stratum (TCGA)** | `ELIGIBLE_FOR_REVIEW` |

---

## 3. Label Classification & Circularity Audit (B1–B6)

In strict accordance with Section 4.2 of the Eligibility Specification:
- **B1 Labels (Biological Subtype / Histology / Lineage):**
  - `GSE62254`: ACRG molecular subtypes (MSI, MSS/TP53+, MSS/TP53-, MSS/EMT; $K=4$).
  - `GSE39582`: CIT molecular subtypes (C1–C6; $K=6$).
  - `GSE31210`: Mutually exclusive oncogenic drivers (EGFR, KRAS, ALK, Triple-Neg; $K=4$).
  - `GSE72094`: KRAS/TP53/STK11 co-mutational groups (KL, KP, K-only, WT; $K=4$).
  - `GSE13159`: International WHO leukemia diagnostic lineages (AML, ALL, CLL, CML, MDS; $K=18$).
  - `GSE19188`: Histopathologic lung lineages (Adenocarcinoma vs Squamous Cell Carcinoma; $K=2$).
  - `GSE21653`: Elston-Ellis Scarff-Bloom-Richardson histologic grade ($K=3$).
  - `GSE10846`: Diffuse Large B-cell Lymphoma Cell-of-Origin (GCB vs ABC vs Unclassified; $K=3$).
  - `GSE14333`: Colorectal anatomical subsite location (Proximal vs Distal vs Rectum; $K=3$).
  - `GSE32894`: Lund Urothelial Carcinoma molecular taxonomy (UroA, UroB, GU, Infiltrated, SCCL; $K=5$).
  - `GSE41271`: Histopathologic differentiation grade (Well, Moderately, Poorly differentiated; $K=3$).
  - `GSE88770`: Invasive Lobular Carcinoma histological variants (Classic, Pleomorphic, Mixed; $K=3$).
  - `E-MTAB-1980`: Clear cell renal cell carcinoma molecular subtypes (ccA vs ccB; $K=2$).
  - `TCGA Cohorts`: PAM50 ($K=5$ for BRCA), Consensus transcriptional ($K=3$ for LUAD), CMS1-4 ($K=4$ for COAD), Verhaak ($K=4$ for GBM).

- **B2 Labels (Tumor vs Normal Diagnostic Contrasts):**
  - Identified in GSE39582 (566 vs 19), GSE31210 (226 vs 20), GSE14520 (247 vs 241), GSE42568 (104 vs 17), GSE19188 (128 vs 28), and TCGA normal controls. Normal controls are segregated to prevent inflating clustering scores on obvious tissue boundaries.

- **B3 Labels (Receptor / Somatic Mutations):**
  - `GSE25066`: ER Status (ER+ vs ER-).
  - `GSE2034`: ER Status (ER+ vs ER-).
  - `GSE42568`: ER Status (ER+ vs ER-).
  - Assigned to **Tier B (Molecular Receptor Stratum)**.

- **B4 Labels (Clinical Outcome / Survival):**
  - Overall survival (OS), relapse-free survival (RFS), metastasis-free survival (MFS), and therapy response (pCR/RD) were extracted and cataloged, but **strictly barred from clustering evaluation or $K$ tuning**.

- **B5 Labels (Technical Batches):**
  - Collection centers (MILE GSE13159), trial protocols (MDACC GSE25066), and array batches were documented to audit technical confounders.

- **B6 Labels (Inferred Signatures with Circularity Check):**
  - PAM50 in GSE42568 and Genomic Grade Index (GGI) in GSE88770 were flagged for circularity risk if the same expression features are clustered. True histopathological or central pathology review labels were prioritized instead.

---

## 4. Cohort Independence & Cross-Benchmark Overlap Audit

A forensic overlap audit was conducted against the 12 certified legacy benchmarks:
1. **Alon et al. 1999 (Colon, $N=62$):** Collected in the mid-1990s at Princeton University on Affymetrix Hu6800.
   - *Verification:* **Zero overlap** with GSE39582 (French CIT, 2013), GSE14333 (Melbourne, Australia, 2009), or TCGA-COAD (GDC, 2012).
2. **Golub et al. 1999 (Leukemia, $N=72$):** Collected in the 1990s at Dana-Farber Cancer Institute on Hu6800.
   - *Verification:* **Zero overlap** with GSE13159 MILE cohort (international 11-center study collected 2005–2008 on Affymetrix U133 Plus 2.0).
3. **Pomeroy et al. 2002 (CNS Embryonal Tumors, $N=60$):** Pediatric medulloblastoma/ATRT/PNET collected at Boston Children's Hospital.
   - *Verification:* **Zero overlap** with TCGA-GBM (adult glioblastoma multiforme).
4. **Khan et al. 2001 (SRBCT, $N=83$):** Pediatric round cell tumors (Ewing, rhabdomyosarcoma, Burkitt, neuroblastoma).
   - *Verification:* **Zero overlap** with GSE49710 (German Pediatric Oncology Society SEQC neuroblastoma cohort).
5. **van 't Veer et al. 2002 (Breast, $N=97$):** Primary Dutch breast tumors from the Netherlands Cancer Institute (NKI).
   - *Verification:* **Zero overlap** with Wang GSE2034 (Erasmus MC, Rotterdam), Hatzis GSE25066 (MD Anderson, Houston), Sabatier GSE21653 (Marseille, France), Clarke GSE42568 (Dublin, Ireland), or TCGA-BRCA (US multi-center).
6. **Bhattacharjee et al. 2001 (Lung, $N=203$):** Harvard/Whitehead Institute.
   - *Verification:* **Zero overlap** with Okayama GSE31210 (Tokyo, Japan), Schabath GSE72094 (Moffitt, Florida), Hou GSE19188 (Singapore/Rotterdam), or Sato GSE41271 (UTSW, Texas).
7. **Severe Overlap Identified:**
   - **`E-MTAB-669` series (E-MTAB-6690 to 6699):** Directly incorporates and batch-corrects samples from GSE39582, GSE14333, GSE14520, and others. **REJECTED from primary benchmark** to prevent pseudoreplication.
   - **`E-MTAB-3732`:** Multi-study compendium of 27,870 arrays that includes samples from primary GEO series. **REJECTED from primary benchmark**.

---

## 5. Deliverables & Data Integrity

1. **Structured Catalog:** Saved to `research_audit/cohort_discovery/literature_leads_catalog.json`.
2. **Audit Script:** Saved to `scripts/audit_literature_leads.py`.
3. **Download Manifest Links:** Official direct URLs for series matrix and processed zip archives are registered with no guessed FTP paths.
4. **License & Terms:** All candidate cohorts carry open public access and academic research permissions (NCBI GEO public domain, ArrayExpress CC0/CC-BY, NCI GDC open access).
