# Biological Cohort Expansion and Lifecycle Management Report

**Author:** Agent E — Biological Cohort Provenance and Expansion Auditor  
**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Repository Branch:** `research/dami-revision`  
**Governing Documents:**
- [`COHORT_DISCOVERY_ELIGIBILITY_SPEC.md`](file:///d:/Final%20Year%20Project/research_audit/cohort_discovery/COHORT_DISCOVERY_ELIGIBILITY_SPEC.md)
- [`COHORT_CANDIDATE_REGISTRY.csv`](file:///d:/Final%20Year%20Project/research_audit/dami_revision/COHORT_CANDIDATE_REGISTRY.csv)
- [`COHORT_PROVENANCE_REPORT.md`](file:///d:/Final%20Year%20Project/research_audit/dami_revision/COHORT_PROVENANCE_REPORT.md)
- [`COHORT_OVERLAP_MATRIX.csv`](file:///d:/Final%20Year%20Project/research_audit/dami_revision/COHORT_OVERLAP_MATRIX.csv)

---

## 1. Lifecycle Framework for Cohort Expansion

To maintain strict scientific integrity, this audit introduces a 5-stage lifecycle classification for all datasets considered for the ICC-clustering project:

```
[Discovered Candidates] (339 Records)
        │
        ▼
[Forensic Audit Pool] (28 Cohorts)
        │
   ┌────┴───────────────────────────┬───────────────────────────┐
   ▼                                ▼                           ▼
[Eligible Confirmatory]       [Stratum / Tier C]         [Excluded / Quarantined]
- Tier A: 10 Cohorts          - RNA-seq: 1 Cohort        - Quarantined: 1 Cohort
- Tier B: 5 Cohorts           - Tier C: 2 Cohorts        - Excluded: 9 Cohorts
        │
        ▼ (Awaiting Gate G1 Human Approval)
[Downloaded & Preprocessed]
        │
        ▼ (Awaiting Protocol Freeze & Preregistration)
[Confirmatory Benchmark Evaluated] (E1–E8 Execution)
```

### Stage Definitions:
1. **Discovered Candidate:** Any public accession identified during systematic keyword queries in NCBI GEO, ArrayExpress, or OpenML.
2. **Forensic Audit Pool:** Datasets undergoing deep forensic inspection for patient provenance, sample overlap, assay platform, and ground-truth label validity.
3. **Eligible Confirmatory Cohort:** A dataset that has satisfied all 9 gates of `COHORT_DISCOVERY_ELIGIBILITY_SPEC.md` without exception.
4. **Downloaded & Preprocessed:** Raw matrix or series matrix acquired, checksum-verified, missing values handled, and log-transformed/standardized label-blind.
5. **Confirmatory Evaluated:** Evaluated under frozen preregistration protocols. **Zero confirmatory evaluations have been launched to date**, honoring the non-negotiable boundaries of Gate G1.

---

## 2. Reconciliation: Evaluated Benchmark vs. Confirmatory Expansion

### 2.1 The 6 Exploratory Baselines (Frozen)
The current benchmark matrix (`experiments/exp3_real_world_benchmarks/data/exp3_1_benchmark_matrix.csv` and `experiments/exp7_modern_baselines/data/modern_baselines_benchmark.csv`) contains evaluations on six historical datasets:
- `colon` ($N=62, D=2{,}000, K=2$)
- `srbct` ($N=83, D=2{,}308, K=4$)
- `cns` ($N=60, D=7{,}129, K=2$)
- `leukemia` ($N=72, D=7{,}129, K=2$)
- `prostate` ($N=102, D=12{,}600, K=2$)
- `ovarian` ($N=253, D=15{,}154, K=2$)

**Audit Finding:** These 6 cohorts are exploratory. They have directly influenced algorithm parameter tuning, density-grid selection, and threshold calibration throughout project development. They cannot be retroactively repurposed as confirmatory evidence.

### 2.2 Reconciling Expansion Numbers in Historical Manuscripts
Historical manuscript drafts referenced variable numbers of candidate cohorts:
- Draft texts intermittently claimed "15 independent biological cohorts" or "20 multi-center validation cohorts".
- **Forensic Truth:** The systematic discovery pipeline identified 339 GEO candidate records, filtered down to 28 candidate entries in the detailed forensic audit pool.
- Of these 28 candidate entries:
  - **10 cohorts** qualify for the primary **Tier A Confirmatory Bulk Microarray Benchmark** ($N \ge 30, D \ge 500, D/N \ge 5$, biological subtype ground truth, single-donor independence).
  - **5 cohorts** qualify for the secondary **Tier B Confirmatory Generalization Benchmark** (binary receptor/oncogene driver contrasts).
  - **1 cohort** (`TCGA-BRCA`) qualifies for the exploratory **Bulk RNA-Seq Separate Stratum**.
  - **2 cohorts** (`GSE352573`, `GSE352548`) are relegated to **Tier C (Exploratory Appendix Only)** due to small sample sizes ($N < 30$).
  - **1 cohort** (`GSE352244`) is **Quarantined** due to repeated longitudinal sampling of the same donors.
  - **9 cohorts** are **Permanently Excluded** due to fatal duplicate identities, meta-dataset dependencies, non-human tissue, controlled access barriers, or clinical outcome label contamination.

---

## 3. Tier A Confirmatory Cohort Inventory ($n=10$)

The table below defines the definitive Tier A confirmatory cohort expansion pool to be evaluated upon human authorization of Gate G1:

| ID | GEO Accession | Disease / Tissue Condition | Platform | Sample $N$ | Total Genes $D$ | True $K$ | Gold Standard Partition Type |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **C01** | `GSE62254` | Gastric Adenocarcinoma | Affymetrix HG-U133 Plus 2.0 | 300 | 54,675 | 4 | ACRG Molecular Subtypes (MSI, MSS/EMT, MSS/TP53+, MSS/TP53-) |
| **C02** | `GSE39582` | Colorectal Carcinoma | Affymetrix HG-U133 Plus 2.0 | 566 | 54,675 | 6 | CIT Molecular Subtypes (C1–C6) |
| **C03** | `GSE13159` | Acute Leukemia Consortium | Affymetrix HG-U133 Plus 2.0 | 2,096 | 54,675 | 3 | WHO Lineages (AML, ALL, CLL) |
| **C04** | `GSE31210` | Lung Adenocarcinoma | Affymetrix HG-U133 Plus 2.0 | 226 | 54,675 | 3 | Oncogenic Drivers (*EGFR*, *KRAS*, *ALK*/Triple Neg) |
| **C05** | `GSE10846` | Diffuse Large B-Cell Lymphoma | Affymetrix HG-U133 Plus 2.0 | 414 | 54,675 | 3 | Cell-of-Origin (GCB, ABC, PMBL) |
| **C06** | `GSE42568` | Breast Molecular Cohort | Affymetrix HG-U133 Plus 2.0 | 104 | 54,675 | 5 | Intrinsic Subtypes (PAM50) |
| **C07** | `GSE19188` | Non-Small Cell Lung Cancer | Affymetrix HG-U133 Plus 2.0 | 91 | 54,675 | 3 | Histological Types (Adeno, Squamous, Large Cell) |
| **C08** | `GSE21653` | Breast Carcinoma Series | Affymetrix HG-U133 Plus 2.0 | 266 | 54,675 | 4 | Subtypes (Basal, HER2, LumA, LumB) |
| **C09** | `GSE32894` | Urothelial Bladder Cancer | Illumina HumanHT-12 V3.0 | 308 | 28,869 | 5 | Lund Bladder Molecular Taxonomy |
| **C10** | `GSE49710` | Neuroblastoma Transcriptome | Agilent Human Custom Array | 498 | 44,495 | 2 | High-Risk Genetic Driver (*MYCN* Amp vs WT) |

**Total Tier A Confirmatory Cohort Size:** $N_{total} = 4{,}869$ independent patient tumor specimens.

---

## 4. Formal Quarantine Rules and Protocols

A cohort is placed in **Quarantine** when forensic analysis reveals an ambiguity, dependency, or structural defect that cannot be immediately resolved, preventing either clean acceptance or categorical exclusion.

### 4.1 Quarantined Cohort Specification
- **Cohort ID:** `GSE352244` (Longitudinal Multiple Myeloma Progression).
- **Reason for Quarantine:** The GEO series contains 105 samples, but these are derived from only 35 unique human patients sampled longitudinally at three clinical timepoints:
  1. Baseline newly diagnosed.
  2. First relapse.
  3. Second relapse.
- **Risk Assessment:** Evaluating standard clustering algorithms on repeated measures from the same patient induces severe intra-patient correlation, violating the Independent and Identically Distributed (i.i.d.) assumption underlying clustering validation.

### 4.2 Quarantine Release Protocol
A quarantined cohort can be released into the benchmark **only if** one of the following remediation protocols is executed and verified:
1. **Baseline-Only Pruning:** A verified algorithmic filter extracts exclusively the Timepoint 1 (baseline newly diagnosed) profile for each unique patient identifier, reducing $N$ to 35 strictly independent biological samples.
2. **Patient Identifier Reconciliation:** An unambiguous patient-to-sample mapping table is published and frozen in `research_audit/dami_revision/` demonstrating zero sample duplication.
3. **If unresolved:** The cohort remains quarantined and excluded from all primary and secondary statistical hypothesis tests (H1–H3).

---

## 5. Non-Contamination Boundaries

To prevent leakage between exploratory research and confirmatory validation:
1. **Code Execution Isolation:** No script in `experiments/` may load any Tier A or Tier B candidate cohort until human approval for Gate G1 is formally granted.
2. **Directory Sandboxing:** All confirmatory experiment runners must write to dedicated directories (`experiments/confirmatory_validation/outputs/`) rather than overwriting existing directories in `experiments/exp3_...` or `results/`.
3. **Immutability of Baseline Stores:** Results in `results/stats.json` and `experiments/exp3_real_world_benchmarks/data/` remain permanently frozen and archived.
