# Research Audit: Duplicate & Near-Duplicate Profile Verification

**Document Reference:** `research_audit/cohort_independence/DUPLICATE_SAMPLE_AUDIT.md`  
**Related Files:** `results/cohort_independence/profile_similarity_pairs.csv`, `results/cohort_independence/duplicate_sample_candidates.csv`  
**Audit Date:** 2026-11-01  
**Auditor:** Senior Computational Biologist & Machine Learning Auditor  

---

## 1. Computational Profile Fingerprinting Overview

In biomedical transcriptomics, exact sample identifier strings can be obscured by pipeline renaming (e.g. `sample_0001` vs `GSM12345`). To detect shared biological patients and duplicate cohorts with absolute mathematical rigor, we performed **pairwise expression profile fingerprinting** across all shared feature spaces using:
- **Pearson correlation ($r$)** across zero-centered, unit-variance sample expression vectors.
- **Cosine similarity** on normalized feature vectors.
- **Exact floating-point array matching** across sample matrices.

---

## 2. Confirmed Duplicate Cohorts & Sample Lineage Overlaps

### 2.1 100% Bit-for-Bit Duplicate Cohorts

| Dataset A | Dataset B | Shared Features | Max $r$ | Exact Duplicate Count | Overlap Verdict |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `main_cns` | `exp3_glioma` | 7,129 | **1.00000** | **60 / 60** | **100% Bit-for-Bit Duplicate Matrix (SHA-256 match)** |
| `main_cns` | `exp3_cns` | 7,129 | **1.00000** | **60 / 60** | **100% Bit-for-Bit Duplicate Matrix** |
| `main_colon` | `exp3_colon` | 2,000 | **1.00000** | **62 / 62** | **100% Bit-for-Bit Duplicate Matrix** |
| `main_leukemia` | `exp3_leukemia` | 7,129 | **1.00000** | **72 / 72** | **100% Bit-for-Bit Duplicate Matrix** |
| `main_ovarian` | `exp3_ovarian` | 15,154 | **1.00000** | **253 / 253** | **100% Bit-for-Bit Duplicate Matrix** |
| `main_prostate` | `exp3_prostate` | 12,600 | **1.00000** | **102 / 102** | **100% Bit-for-Bit Duplicate Matrix** |
| `main_srbct` | `exp3_srbct` | 2,308 | **1.00000** | **83 / 83** | **100% Bit-for-Bit Duplicate Matrix** |

> [!CAUTION]
> `glioma` in `experiments/audit_controls/data/cache/glioma.npz` is **NOT an independent glioma dataset**. It is a direct copy of `cns.npz` derived from OpenML ID 1107 (`tumors_C`). Counting `cns` and `glioma` as two independent datasets in the 21-dataset benchmark represented a double-counting error.

### 2.2 Cross-Study Patient Sample Reuse (The GCM Composite Overlap)

When comparing Golub et al. (Leukemia, 1999) and Pomeroy et al. (CNS, 2002) against the Global Cancer Map (GCM, Ramaswamy et al. 2001) across the 7,129 shared Affymetrix Hu6800 probes:
- **61 of the 72 Leukemia samples** in Golub et al. match samples in GCM with Pearson $r \ge 0.990$ (max $r = 0.99917$). All 61 matching samples are labeled `'Leukemia'` in GCM.
- **8 of the 60 CNS embryonal tumor samples** in Pomeroy et al. match samples in GCM with Pearson $r > 0.90$ (max $r = 0.98538$). All matching samples are labeled `'CNS'` in GCM.

**Conclusion on GCM:** The Global Cancer Map is a **composite cross-study dataset** that ingested patient microarrays directly from Golub (1999) and Pomeroy (2002). Consequently, **GCM CANNOT be treated as an independent biological validation cohort relative to Leukemia and CNS** in benchmarking generalizability.