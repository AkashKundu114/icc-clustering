# Overnight Research Audit: Comprehensive Dataset & Cohort Provenance Audit

**Document Reference:** `research_audit/overnight/DATASET_AUDIT.md`  
**Related Deliverables:**  
- `results/overnight/dataset_manifest.csv`  
- `research_audit/overnight/DATASET_MANIFEST.md`  
**Audit Date:** 2026-11-01  
**Auditor:** Agent A — Dataset & Cohort Auditor  

---

## 1. Executive Summary: Resolving the 21-Dataset Benchmark Paradox

A complete examination of the repository manifests, loading routines, OpenML caches, and raw matrix checksums demonstrates:
- **The "21-Dataset Benchmark" Claim is 52.4% Non-Biological:** 11 of the 21 datasets in `e1_extended_benchmarks.csv` were physical sensor or synthetic controls.
- **Two Cache Files Were Catastrophically Mislabeled:** `MagicTelescope` (astrophysics gamma-ray simulation) was cached as `breast_cancer_genomic`; `Jungle Chess` endgame was cached as `gisette`.
- **One Dataset Was a Redundant Duplicate:** `glioma` was an identical copy of `cns` (Pomeroy 2002 medulloblastoma).
- **One Dataset Ingested Existing Patients:** `gcm` (OpenML 1106) swallowed 61 Golub Leukemia patients ($r \ge 0.990$) and 8 Pomeroy CNS patients ($r > 0.90$).
- **Maximum True Independent Bulk Oncology Cohorts Available:** **10 confirmed Category A cohorts** (`colon`, `srbct`, `cns`, `leukemia`, `prostate`, `ovarian`, `dlbcl`, `breast`, `su2001`, `endometrium`), plus `zheng68k` in the single-cell stratum.

---

## 2. Master Dataset Roster & Technical Parameters

# Overnight Research Audit: Master Dataset Manifest

**Document Reference:** `research_audit/overnight/DATASET_MANIFEST.md`  
**Related File:** `results/overnight/dataset_manifest.csv`  
**Audit Date:** 2026-11-01  
**Auditor:** Agent A — Dataset & Cohort Auditor  

---

## 1. Dataset Eligibility & Stratification Summary

| Dataset Key | Intended Name | Biological Domain | $N$ | $D$ | $K$ | Category | Primary ICC | BGSS Audit | Baselines | Unknown-K |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| `colon` | **Colon Adenocarcinoma Gene Expr** | Gastrointestinal Oncology | 62 | 2000 | 2 | Category A | Eligible | Eligible | Eligible | Eligible |
| `srbct` | **Small Round Blue Cell Tumors o** | Pediatric Oncology (EWS,  | 83 | 2308 | 4 | Category A | Eligible | Eligible | Eligible | Eligible |
| `cns` | **Central Nervous System Embryon** | Neuro-Oncology (Pediatric | 60 | 7129 | 2 | Category A | Eligible | Eligible | Eligible | Eligible |
| `leukemia` | **Acute Leukemia (ALL vs AML)** | Hematologic Oncology (Bon | 72 | 7129 | 2 | Category A | Eligible | Eligible | Eligible | Eligible |
| `prostate` | **Prostate Adenocarcinoma Gene E** | Urologic Oncology (Radica | 102 | 12600 | 2 | Category A | Eligible | Eligible | Eligible | Eligible |
| `ovarian` | **Ovarian Cancer Serum Proteomic** | Gynecologic Oncology (Ser | 253 | 15154 | 2 | Category A | Eligible | Eligible | Eligible | Eligible |
| `dlbcl` | **Diffuse Large B-Cell Lymphoma ** | Hematologic Oncology (Lym | 77 | 5469 | 2 | Category A | Eligible | Eligible | Eligible | Eligible |
| `breast` | **Breast Cancer 5-Year Distant M** | Breast Oncology (Primary  | 97 | 24481 | 2 | Category A | Eligible | Eligible | Eligible | Eligible |
| `su2001` | **11 Human Solid Tumor Carcinoma** | Multi-Organ Solid Tumors  | 174 | 12533 | 11 | Category A | Eligible | Eligible | Eligible | Eligible |
| `endometrium` | **Endometrium vs Kidney Adenocar** | Gynecologic and Renal Onc | 321 | 10936 | 2 | Category A | Eligible | Eligible | Eligible | Eligible |
| `zheng68k` | **10x PBMC Single-Cell Transcrip** | Single-Cell Immunology (1 | 700 | 765 | 10 | Category A | Eligible | Eligible | Eligible | Eligible |
| `novartis` | **9 Human Carcinomas (Novartis G** | Human Carcinoma Panel | 60 | 5726 | 9 | Category B | Eligible | Eligible | Eligible | Eligible |
| `gcm` | **Global Cancer Map (Ramaswamy 2** | 14 Common Tumor Types (Co | 190 | 16063 | 14 | Category C | EXCLUDED | EXCLUDED | EXCLUDED | EXCLUDED |
| `glioma_e1` | **Glioma in e1 cache (OpenML 110** | Neuro-Oncology | 60 | 7129 | 2 | Category D | EXCLUDED | EXCLUDED | EXCLUDED | EXCLUDED |
| `breast_cancer_genomic_e1` | **MagicTelescope (OpenML 1120 mi** | Astrophysical Radiation P | 19020 | 10 | 2 | Category E | EXCLUDED | EXCLUDED | EXCLUDED | EXCLUDED |
| `gisette_e1` | **Jungle Chess Endgame (OpenML 4** | Board Game Simulation | 1000 | 6 | 3 | Category E | EXCLUDED | EXCLUDED | EXCLUDED | EXCLUDED |
| `sonar` | **Sonar Signals (Mines vs Rocks)** | Acoustic Signal Processin | 208 | 60 | 2 | Category E | Eligible | EXCLUDED | Eligible | Eligible |
| `madelon` | **Madelon Synthetic XOR Benchmar** | Synthetic Non-Linear Benc | 500 | 500 | 2 | Category E | Eligible | EXCLUDED | Eligible | Eligible |

---

## 2. Definitive Exclusion Decisions

1. **`glioma_e1` EXCLUDED:** 100% Bit-for-Bit exact duplicate of `cns` (Pomeroy 2002 medulloblastoma, SHA-256 `0e449bf...`). Including both would double-count medulloblastoma.
2. **`gcm` EXCLUDED from Independent Biological Summaries:** Ramaswamy Global Cancer Map ingested 61 of 72 Golub Leukemia patients and 8 Pomeroy CNS patients. It cannot be treated as an independent cohort alongside Leukemia or CNS.
3. **`breast_cancer_genomic_e1` & `gisette_e1` PURGED:** OpenML cache mislabels representing astrophysics simulation (MagicTelescope, $D=10$) and board game endgame (Jungle Chess, $D=6$).
4. **Non-Biological Controls (`sonar`, `madelon`) STRATIFIED:** Retained in non-biological control stratum only; excluded from biological BGSS gene gating.


---

## 3. Preprocessing & Leakage Safeguards

1. **Unsupervised Transformation Verification:** All core microarrays are standardized via transductive Z-score standardization across features without using ground-truth class labels.
2. **Feature Dimension Audit:** Dimensions ($D = 2,000$ to $24,481$) reflect the full or intensity-filtered probe sets from the primary publications; no supervised label-informed gene downselection was applied prior to clustering.
3. **Automated Verification:** All matrices are stored as float32 NumPy arrays with samples as rows ($N$) and features as columns ($D$).
