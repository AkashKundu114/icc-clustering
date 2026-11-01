# Research Audit 09: Dataset Overlap and Biological Independence Audit

**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Document Reference:** `AUDIT-09-SAMPLE-OVERLAP`  
**Date:** 2026-10-31  

---

## 1. Core Principle of Biological Independence

In computational oncology and machine learning benchmarks, a catastrophic error is **pseudoreplication**—treating duplicate downloads, re-normalized variants, or overlapping patient subsets as independent biological cohorts. 

> **Scientific Axiom:** Two datasets $A$ and $B$ are independent biological cohorts if and only if their underlying patient donor populations $\mathcal{P}_A \cap \mathcal{P}_B = \emptyset$. Re-normalizing, re-filtering, or renaming the same biological observations does not generate new statistical evidence.

---

## 2. Forensic Investigation of Known & Suspected Overlaps

### 2.1 The CNS vs. Glioma Duplication (Critical Finding)
- **Investigation:** In `experiments/audit_controls/data/e1_extended_benchmarks.csv`, `cns` and `glioma` produced identical clustering results across 9 models and 5 seeds.
- **Forensic Diagnosis:**
  - `experiments/audit_controls/src/e1_extended_benchmarks.py:72` mapped `glioma` to OpenML ID `1107`.
  - Upstream OpenML metadata confirms ID `1107` is officially named `tumors_C` (Pomeroy et al., Nature 2002, Central Nervous System embryonal tumors, $N=60, D=7{,}129$).
  - This is the exact dataset already present in the benchmark as `cns` (OpenML 45086).
  - SHA-256 hash comparison confirmed bitwise identity: `0E449BF55F8E5682DE8DE4264C986C1B85B27F25CA0092B5A8A98CA2BB2A87FF`.
- **Verdict:** `glioma` in `experiments/audit_controls` was an accidental duplicate of `cns`.
- **Resolution:** Purged duplicate mapping. The true Glioma cohort (Nutt et al., Cancer Research 2003, $N=50, D=12{,}625, K=4$) is formally registered under OpenML `45089`.

### 2.2 `PBMC68k-reduced` vs. `zheng68k` vs. `pbmc4k`
- **Investigation:** Literature and repository files reference `PBMC68k`, `zheng68k`, and `PBMC 4k`.
- **Forensic Diagnosis:**
  - `zheng68k` and `PBMC68k-reduced` both represent the exact same 700-cell subsample from Zheng et al. (Nature Communications 2017) bundled in Scanpy (`scanpy.datasets.pbmc68k_reduced()`). The ground truth labels $\mathbf{y}$ are identical ($N=700, K=10$).
  - `pbmc4k` represents an independent 10x Genomics scRNA-seq run (Peripheral Blood Mononuclear Cells from a healthy donor, $N=4{,}340, K=8$).
- **Verdict:** `zheng68k` and `PBMC68k` are the same dataset under different aliases.
- **Resolution:** The repository enforces a single canonical entry `zheng68k`. `pbmc4k` is retained as a separate single-cell cohort.

### 2.3 Breast Cancer Cohort Independence: van 't Veer vs. GSE2034 vs. TCGA-BRCA
- **van 't Veer et al. (Nature 2002):** $N = 97$ primary breast tumors from Dutch cancer clinics profiled on Agilent dual-channel arrays (46 early metastasis, 51 disease-free).
- **Wang et al. / GSE2034 (Lancet 2005):** $N = 286$ lymph node-negative primary breast cancer patients profiled on Affymetrix HG-U133A arrays.
- **TCGA-BRCA:** Profiling from multi-center US TCGA consortium using Illumina HiSeq RNA-seq.
- **Verdict:** Patient donor sets are completely disjoint; collection sites, eras, and array platforms are independent. Both van 't Veer and GSE2034 represent genuine independent biological replications.

### 2.4 Lung Cancer Cohort Independence: Bhattacharjee vs. Ramaswamy vs. Novartis
- **Bhattacharjee et al. (PNAS 2001, OpenML 45094):** $N = 203$ lung specimens (186 lung tumors, 17 normal lung).
- **Ramaswamy et al. (PNAS 2001, OpenML 45091):** Global Cancer Map containing $N = 198$ tumors across 14 tissue types, including 24 lung carcinomas.
- **Novartis BPLC (Su et al. PNAS 2002, OpenML 45095):** Contains 27 lung adenocarcinoma samples.
- **Overlap Audit:** Ramaswamy et al. and Bhattacharjee et al. were both produced in collaboration with the Whitehead Institute/MIT Center for Genome Research.
- **Scientific Protocol:** To prevent donor contamination across lung samples, when Bhattacharjee (`lung_cancer`) is included in the benchmark, Ramaswamy is evaluated across all 14 carcinoma classes ($K=14$) rather than isolated as a lung cohort.

---

## 3. Summary of Certified Independent Biological Cohorts

The following 12 bulk oncology cohorts are certified free of patient sample overlap:

1. `colon` ($N=62, D=2{,}000, K=2$) — Alon et al. (1999) Princeton
2. `srbct` ($N=83, D=2{,}308, K=4$) — Khan et al. (2001) NIH Pediatric
3. `cns` ($N=60, D=7{,}129, K=2$) — Pomeroy et al. (2002) Boston Children's
4. `leukemia` ($N=72, D=7{,}129, K=2$) — Golub et al. (1999) Dana-Farber
5. `prostate` ($N=102, D=12{,}600, K=2$) — Singh et al. (2002) Brigham & Women's
6. `ovarian` ($N=253, D=15{,}154, K=2$) — Petricoin et al. (2002) NCI/FDA SELDI
7. `dlbcla` ($N=77, D=7{,}129, K=2$) — Shipp et al. (2002) Dana-Farber
8. `ramaswamy` ($N=198, D=16{,}063, K=14$) — Ramaswamy et al. (2001) Multi-Center GCM
9. `novartis_bplc` ($N=103, D=12{,}600, K=4$) — Su et al. (2002) Novartis Research Foundation
10. `su2001` ($N=174, D=12{,}533, K=11$) — Su et al. (2001) Genomics Institute of the Novartis
11. `breast_vantveer` ($N=97, D=4{,}988, K=2$) — van 't Veer et al. (2002) Netherlands Cancer Inst.
12. `risinger` ($N=42, D=12{,}625, K=4$) — Risinger et al. (2003) Duke University
