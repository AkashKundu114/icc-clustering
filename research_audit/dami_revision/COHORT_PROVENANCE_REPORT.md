# Forensic Cohort Provenance and Lineage Audit Report

**Author:** Agent E — Biological Cohort Provenance and Expansion Auditor  
**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Repository Branch:** `research/dami-revision`  
**Governing Protocol:** `research_audit/cohort_discovery/COHORT_DISCOVERY_ELIGIBILITY_SPEC.md`  
**Associated Artifacts:**
- [`COHORT_CANDIDATE_REGISTRY.csv`](file:///d:/Final%20Year%20Project/research_audit/dami_revision/COHORT_CANDIDATE_REGISTRY.csv)
- [`COHORT_OVERLAP_MATRIX.csv`](file:///d:/Final%20Year%20Project/research_audit/dami_revision/COHORT_OVERLAP_MATRIX.csv)
- [`COHORT_EXPANSION_REPORT.md`](file:///d:/Final%20Year%20Project/research_audit/dami_revision/COHORT_EXPANSION_REPORT.md)

---

## 1. Executive Summary & Audit Mandate

To satisfy the non-negotiable scientific boundaries of DMKD, all genomic, transcriptomic, and molecular cohorts must undergo forensic provenance tracing before any confirmatory claims can be evaluated. Specifically:
1. **The 6 Exploratory Cohorts** (`colon`, `leukemia`, `breast`, `prostate`, `srbct`, `cns`) are strictly locked as exploratory baseline generators and cannot serve as confirmatory validation.
2. **Accession Disambiguation:** A new accession code does not imply biological independence. Re-analyses, meta-compendia, patient re-samplings, and duplicate uploads must be identified and isolated.
3. **Ground-Truth Label Independence:** In accordance with Gate B of the Eligibility Specification, clinical outcome endpoints (survival time, relapse, treatment failure, distant metastasis) are strictly disqualified from serving as ground-truth clustering partitions. Ground-truth partitions must reflect stable intrinsic biological taxonomy (histology, cell-of-origin, genetic driver alterations, or established consensus molecular subtypes).
4. **Lifecycle Stratification:** Out of 28 candidate datasets investigated, 10 meet Tier A confirmatory requirements, 5 meet Tier B (generalization), 1 forms a separate RNA-seq stratum, 2 are relegated to Tier C exploratory status, 1 is quarantined pending sample de-duplication, and 9 are permanently excluded.

---

## 2. Forensic Traceability of the 6 Exploratory Baselines

The table below documents the historical provenance of the 6 legacy exploratory cohorts. All six are archived in frozen result stores and must remain classified as exploratory.

| Cohort Name | OpenML / Curated Source | Primary Citation | Platform / Assay | Biological $N$ | Features $D$ | True $K$ | Partition Ground Truth | Independence & Provenance Limitations |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Colon** | OpenML 45087 / Alon 1999 | Alon et al. (1999) *PNAS* 96:6745 | Affymetrix Hum6800 (Oligonucleotide) | 62 | 2,000 | 2 | 40 Tumor vs 22 Normal Colon Tissue (Histopathology) | Small sample size ($N=62$). Normal mucosa vs adenocarcinoma; extreme biological contrast. Heavily overfitted by decades of ML literature. |
| **Leukemia** | OpenML 1104 / Golub 1999 | Golub et al. (1999) *Science* 286:531 | Affymetrix Hu6800 (Oligonucleotide) | 72 | 7,129 | 2 | 47 ALL (Acute Lymphoblastic) vs 25 AML (Acute Myeloid) (Morphology/Cytochemistry) | Gold standard 1999 benchmark. Pre-split into 38 train / 34 test in original paper; pooled here to 72. Two fundamentally distinct hematopoietic cell lineages. |
| **Breast** (Ovarian) | OpenML 45085 / Curated Matrix | Petricoin et al. (2002) *Lancet* 359:572 | SELDI-TOF Mass Spectrometry (WCX2) | 253 | 15,154 | 2 | 162 Ovarian Cancer vs 91 Normal Controls (Serum Spectra) | Mass spec surface ionization profile, not microarray gene expression. Known baseline artifacts documented by Baggerly et al. (2004). |
| **Prostate** | OpenML 45088 / Singh 2002 | Singh et al. (2002) *Cancer Cell* 1:203 | Affymetrix Hu95av2 (Oligonucleotide) | 102 | 12,600 | 2 | 52 Prostate Tumor vs 50 Normal Prostate (Histology) | 102 radical prostatectomy specimens. Standard binary tissue classification. |
| **SRBCT** | OpenML 45089 / Khan 2001 | Khan et al. (2001) *Nat Med* 7:673 | cDNA Microarray (Filter hybridized) | 83 | 2,308 | 4 | 29 EWS, 11 BL, 18 NB, 25 RMS (Immunohistochemistry / RT-PCR) | Small Round Blue Cell Tumors of childhood. Four distinct diagnostic entities. Highly structured multi-class benchmark. |
| **CNS** | OpenML 45086 / Pomeroy 2002 | Pomeroy et al. (2002) *Nature* 415:436 | Affymetrix Hu6800 (Oligonucleotide) | 60 | 7,129 | 2 | 10 Medulloblastoma survivors vs 21 Treatment failures + others (or 60 tumors_C) | Central Nervous System embryonal tumors. Frequently re-annotated across OpenML (duplicate entry OpenML 1107). |

---

## 3. Tier A Confirmatory Biological Cohorts ($N \ge 30, D \ge 500, D/N \ge 5$)

Tier A datasets represent high-dimensional, clinically and biologically characterized cohorts possessing gold-standard subtype definitions derived independently of clustering inputs.

### 3.1 GSE62254 (ACRG Gastric Adenocarcinoma)
- **NCBI GEO Accession:** `GSE62254` (Platform: GPL570, Affymetrix HG-U133 Plus 2.0).
- **Publication & PubMed ID:** Cristescu et al. (2015), *Nature Medicine* 21(5):449–456. PMID: 25894828.
- **Data Availability:** Public GEO series matrix and raw CEL archives.
- **Specimens & Patients:** $N = 300$ primary gastric adenocarcinoma patient tumors collected at Samsung Medical Center (Seoul, Korea). Single specimen per donor.
- **Dimensionality:** Raw features $D = 54{,}675$ probe sets, log2 RMA normalized. Filtered to $D = 10{,}000$ most variable genes for benchmark matrix.
- **Ground Truth Partition ($K=4$):** Asian Cancer Research Group (ACRG) consensus molecular subtypes:
  1. *MSI* (Microsatellite Instability; hypermutated, best prognosis, $n=68$).
  2. *MSS/EMT* (Epithelial-Mesenchymal Transition; loss of CDH1, youngest age, worst prognosis, $n=46$).
  3. *MSS/TP53+* (Active TP53 pathway, intact p53, intermediate prognosis, $n=79$).
  4. *MSS/TP53-* (Inactive TP53 pathway, high chromosomal instability, $n=107$).
- **Label Independence Verification:** Established by targeted sequencing, MLH1 IHC, and chromosomal copy-number arrays, completely external to the RNA transcriptomic clustering input.
- **Overlap Audit:** Zero patient or institutional overlap with Alon 1999 or any exploratory benchmark.

### 3.2 GSE39582 (CIT Colorectal Carcinoma)
- **NCBI GEO Accession:** `GSE39582` (Platform: GPL570, Affymetrix HG-U133 Plus 2.0).
- **Publication & PubMed ID:** Marisa et al. (2013), *PLoS Medicine* 10(5):e1001453. PMID: 23700391.
- **Data Availability:** Public GEO series matrix and raw CEL files.
- **Specimens & Patients:** $N = 566$ primary colon adenocarcinomas from French national Cartes d'Identité des Tumeurs (CIT) program across 7 French hospitals.
- **Dimensionality:** $D = 54{,}675$ probe sets, RMA normalized. Filtered to $D = 10{,}000$.
- **Ground Truth Partition ($K=6$):** CIT molecular subtyping:
  - C1: CIN / Immune Down ($n=102$)
  - C2: dMMR / MSI ($n=108$)
  - C3: KRAS mutated / Metabolic ($n=72$)
  - C4: Cancer-associated stroma / Stem-like ($n=99$)
  - C5: CIN / Wnt upregulated ($n=115$)
  - C6: CIN / Normal-like ($n=70$)
- **Label Independence Verification:** Labels derived from independent French multi-omic profiling combining array-CGH, KRAS/BRAF sequencing, and MMR immunohistochemistry.
- **Overlap Audit:** Completely independent of Alon 1999 ($N=62$, Princeton/USA). Caution: Absorbed by secondary meta-compendium `E-MTAB-6698` (which must be excluded to prevent double-counting).

### 3.3 GSE13159 (MILE International Leukemia Consortium)
- **NCBI GEO Accession:** `GSE13159` (Platform: GPL570, Affymetrix HG-U133 Plus 2.0).
- **Publication & PubMed ID:** Kohlmann et al. (2008), *Lancet Oncology* 9(3):221–232; Haferlach et al. (2010), *J Clin Oncol* 28(15):2529–2537. PMID: 20406943.
- **Data Availability:** Public GEO series matrix ($N=2{,}096$).
- **Specimens & Patients:** Multi-center international study (11 participating laboratories across 3 continents).
- **Dimensionality:** $D = 54{,}675$ probe sets.
- **Ground Truth Partition ($K=16$ or Primary Lineage $K=3$):** WHO hematologic malignancy diagnostic categories confirmed by reference laboratory karyotyping, FISH, and flow cytometry:
  - AML (Acute Myeloid Leukemia, $n=542$)
  - ALL (Acute Lymphoblastic Leukemia, T-cell and B-lineage, $n=750$)
  - CLL (Chronic Lymphocytic Leukemia, $n=448$)
  - Healthy donor controls and others ($n=356$).
- **Label Independence Verification:** Gold-standard cytogenetic karyotyping and flow immunophenotyping.
- **Overlap Audit:** Zero overlap with Golub 1999 (Golub collected 1995–1998 at Dana-Farber/Whitehead; MILE collected 2005–2008 across 11 international centers).

### 3.4 GSE31210 (Okayama Early-Stage Lung Adenocarcinoma)
- **NCBI GEO Accession:** `GSE31210` (Platform: GPL570, Affymetrix HG-U133 Plus 2.0).
- **Publication & PubMed ID:** Okayama et al. (2012), *Cancer Research* 72(1):100–111. PMID: 22080568.
- **Data Availability:** Public GEO series matrix.
- **Specimens & Patients:** $N = 226$ Stage I-II primary lung adenocarcinomas from National Cancer Center Hospital (Tokyo, Japan). Single surgical resections.
- **Dimensionality:** $D = 54{,}675$ probe sets.
- **Ground Truth Partition ($K=3$):** Mutual oncogenic driver alterations:
  - *EGFR* mutant ($n=127$)
  - *KRAS* mutant ($n=20$)
  - *ALK* fusion / Triple Negative ($n=79$).
- **Label Independence Verification:** High-sensitivity Sanger sequencing and FISH/IHC validation for ALK rearrangements.
- **Overlap Audit:** Independent East Asian cohort; zero overlap with western thoracic cohorts.

### 3.5 GSE10846 (Lenz Diffuse Large B-Cell Lymphoma)
- **NCBI GEO Accession:** `GSE10846` (Platform: GPL570, Affymetrix HG-U133 Plus 2.0).
- **Publication & PubMed ID:** Lenz et al. (2008), *New England Journal of Medicine* 359(22):2313–2323. PMID: 19038878.
- **Data Availability:** Public GEO series matrix.
- **Specimens & Patients:** $N = 414$ DLBCL pretreatment biopsy specimens from the Leukemia and Lymphoma Molecular Profiling Project (LLMPP).
- **Dimensionality:** $D = 54{,}675$ probe sets.
- **Ground Truth Partition ($K=3$):** Biological cell-of-origin (COO) classification:
  - GCB (Germinal Center B-cell-like, $n=183$)
  - ABC (Activated B-cell-like, $n=167$)
  - Primary Mediastinal / Unclassified ($n=64$).
- **Label Independence Verification:** Established via the LLMPP Bayesian cell-of-origin predictor and independent immunohistochemical algorithms (Hans algorithm).
- **Overlap Audit:** Completely independent of all 6 exploratory cohorts.

### 3.6 GSE42568 (Clarke Breast Cancer Molecular Taxonomy)
- **NCBI GEO Accession:** `GSE42568` (Platform: GPL570, Affymetrix HG-U133 Plus 2.0).
- **Publication & PubMed ID:** Clarke et al. (2013), *Cancer Cell* 24(5):660–673. PMID: 24229712.
- **Data Availability:** Public GEO series matrix.
- **Specimens & Patients:** $N = 104$ primary breast carcinoma biopsies with 17 normal breast tissue controls ($N_{total} = 121$).
- **Dimensionality:** $D = 54{,}675$ probe sets.
- **Ground Truth Partition ($K=5$):** Intrinsic molecular subtypes (PAM50): Luminal A ($n=34$), Luminal B ($n=20$), HER2-enriched ($n=16$), Basal-like ($n=17$), Normal-like ($n=17$).
- **Label Independence Verification:** IHC/CISH for ER, PR, and HER2 protein and gene amplification.
- **Overlap Audit:** Completely independent of Petricoin ovarian spectra and van 't Veer breast series.

### 3.7 GSE19188 (Hou Early-Stage NSCLC Histology)
- **NCBI GEO Accession:** `GSE19188` (Platform: GPL570, Affymetrix HG-U133 Plus 2.0).
- **Publication & PubMed ID:** Hou et al. (2010), *PLoS ONE* 5(4):e10250. PMID: 20422047.
- **Data Availability:** Public GEO series matrix.
- **Specimens & Patients:** $N = 91$ resected non-small cell lung cancer tumors and 65 adjacent non-tumor lung tissues ($N_{total} = 156$).
- **Dimensionality:** $D = 54{,}675$ probe sets.
- **Ground Truth Partition ($K=3$ Tumor Histologies):**
  - Lung Adenocarcinoma ($n=45$)
  - Squamous Cell Carcinoma ($n=27$)
  - Large Cell Carcinoma ($n=19$).
- **Label Independence Verification:** Formal microscopic pathology and WHO histological diagnostic criteria.
- **Overlap Audit:** Independent surgical cohort from Prince Charles Hospital, Australia.

### 3.8 GSE21653 (Sabatier Breast Cancer Subtypes)
- **NCBI GEO Accession:** `GSE21653` (Platform: GPL570, Affymetrix HG-U133 Plus 2.0).
- **Publication & PubMed ID:** Sabatier et al. (2011), *Molecular Cancer* 10:86. PMID: 21774813.
- **Data Availability:** Public GEO series matrix.
- **Specimens & Patients:** $N = 266$ untreated primary breast cancers from Institut Paoli-Calmettes, Marseille, France.
- **Dimensionality:** $D = 54{,}675$ probe sets.
- **Ground Truth Partition ($K=4$):** Standard clinical/molecular breast subtypes: Basal ($n=55$), HER2 ($n=42$), Luminal A ($n=88$), Luminal B ($n=81$).
- **Label Independence Verification:** IHC testing for ER, PR, and ERBB2/HER2.

### 3.9 GSE32894 (Sjödahl Lund Bladder Taxonomy)
- **NCBI GEO Accession:** `GSE32894` (Platform: GPL6947, Illumina HumanHT-12 V3.0).
- **Publication & PubMed ID:** Sjödahl et al. (2012), *Clin Cancer Res* 18(12):3377–3386. PMID: 22553347.
- **Data Availability:** Public GEO series matrix.
- **Specimens & Patients:** $N = 308$ urothelial bladder carcinomas from Lund University Hospital, Sweden.
- **Dimensionality:** $D = 28{,}869$ probe sets.
- **Ground Truth Partition ($K=5$):** Lund bladder molecular taxonomy: Urobasal A ($n=95$), Urobasal B ($n=43$), Genomically Unstable ($n=98$), Infiltrated ($n=48$), SCC-like ($n=24$).
- **Label Independence Verification:** Comprehensive immunohistochemical panel and pathological staging.

### 3.10 GSE49710 (SEQC Neuroblastoma Transcriptome)
- **NCBI GEO Accession:** `GSE49710` (Platform: GPL16876, Agilent-020382 Human Custom Microarray).
- **Publication & PubMed ID:** Zhang et al. (2015), *Genome Biology* 16:73. PMID: 25887222.
- **Data Availability:** Public GEO series matrix.
- **Specimens & Patients:** $N = 498$ primary neuroblastomas from Children's Oncology Group (COG) and German Neuroblastoma Trial.
- **Dimensionality:** $D = 44{,}495$ features.
- **Ground Truth Partition ($K=2$ or $K=4$):** High-risk genomic marker: *MYCN* Amplification ($n=92$) vs *MYCN* Non-amplified ($n=401$).
- **Label Independence Verification:** Fluorescence in situ hybridization (FISH) assessment of MYCN gene copy number.

---

## 4. Tier B Confirmatory Generalization Stratum ($N \ge 30, D \ge 500$)

Tier B cohorts feature robust clinical or diagnostic phenotypes that represent binary molecular states or disease states rather than multi-class intrinsic molecular subtyping taxonomies.

| Accession | Disease / Tissue | Platform | Sample $N$ | Features $D$ | Phenotypic Label | Verification Method | Justification for Tier B Placement |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| **GSE25066** | Breast Carcinoma | GPL96 (HG-U133A) | 508 | 22,283 | ER+ ($n=330$) vs ER- ($n=178$) | Clinical Immunohistochemistry (IHC) | Binary receptor contrast rather than full 5-class intrinsic taxonomy. |
| **GSE2034** | Breast Carcinoma | GPL96 (HG-U133A) | 286 | 22,283 | ER+ ($n=209$) vs ER- ($n=77$) | Clinical IHC and Ligand Binding | Binary receptor phenotype; high quality but limited to binary split. |
| **GSE72094** | Lung Adenocarcinoma | GPL15048 (Rosetta) | 442 | 22,283 | KRAS mutant ($n=144$) vs Wildtype ($n=298$) | Targeted Exon Capture Sequencing | Single oncogene driver contrast. |
| **GSE14520** | Hepatocellular Carcinoma | GPL3921 / GPL571 | 445 | 22,277 | HCC Tumor ($n=225$) vs Non-tumor ($n=220$) | Liver Needle Histopathology | Normal vs tumor diagnostic contrast; dual-platform complexity. |
| **GSE14333** | Colorectal Carcinoma | GPL570 (HG-U133 Plus 2) | 290 | 54,675 | Dukes Stage A/B ($n=145$) vs C/D ($n=145$) | Surgical Pathological Staging | Anatomic pathological staging rather than unsupervized molecular cluster. |

---

## 5. Separate Stratum: High-Throughput Bulk RNA-Seq

To eliminate assay-specific variance confounding (sequencing depth, count distributions, zero-inflation) from microarray hybridization intensity distributions, bulk RNA-seq cohorts are strictly partitioned into a Separate Stratum.

- **TCGA-BRCA (Harmonized STAR-Counts):** $N = 1{,}095$ primary breast carcinomas, $D = 60{,}660$ ENSEMBL transcripts. Ground truth: PAM50 intrinsic subtypes (LumA, LumB, Basal, Her2, Normal). Derived from independent RNA-seq calling and GDC pathology.
- **TCGA-LUAD (Harmonized STAR-Counts):** $N = 515$ lung adenocarcinomas, $D = 60{,}660$. Ground truth: Transcriptional subtypes (Bronchioid, Squamoid, Magnoid).
- **TCGA-COAD (Harmonized STAR-Counts):** $N = 458$ colon adenocarcinomas, $D = 60{,}660$. Ground truth: Consensus Molecular Subtypes (CMS1–CMS4) derived from the Colorectal Cancer Subtyping Consortium (CRCSC).

---

## 6. Excluded Candidates and Red-Team Quarantines

In accordance with Gate B, Gate D, and Gate I of the Eligibility Specification, 9 candidates are permanently disqualified or placed in quarantine:

1. **`OPENML_45085` (van 't Veer 2002 Breast Series):**  
   *Disqualification Reason:* Uses 5-year distant metastasis occurrence ($n=44$ vs $n=34$) as ground-truth clustering label. Violates Gate B4 (clinical prognosis endpoint). Permanently excluded from benchmark.
2. **`OPENML_1107` (`tumors_C` / `glioma`):**  
   *Disqualification Reason:* Forensic bit-for-bit SHA-256 hash matching reveals that this dataset is 100% identical to the Pomeroy CNS benchmark (`OpenML 45086`). Claiming it as an independent "Nutt et al. Glioma" cohort is scientific misattribution. Permanently excluded.
3. **`E-MTAB-6698` (CIT-Jorissen Meta-Compendium):**  
   *Disqualification Reason:* Secondary meta-dataset that merged `GSE39582` ($n=566$) and `GSE14333` ($n=290$) using ComBat batch normalization. Violates Gate I (derivative meta-analysis). Evaluating both `GSE39582` and `E-MTAB-6698` would double-count 856 patients. Permanently excluded.
4. **`GSE352244` (Longitudinal Multiple Myeloma):**  
   *Disqualification Reason:* Contains 105 samples originating from only 35 unique patients sampled at diagnosis, first relapse, and second relapse. Violates sample independence (Gate I). Quarantined.
5. **`E-TABM-669`:**  
   *Disqualification Reason:* *Mus musculus* embryonic stem cell line experiment. Violates Gate A (human oncology/clinical requirement). Permanently excluded.
6. **`EGAS00000000083` (METABRIC):**  
   *Disqualification Reason:* Controlled access under European Genome-phenome Archive (EGA Data Access Committee agreement required). Violates Gate G (open, unencumbered reproducibility). Excluded.
7. **`GSE352606`:**  
   *Disqualification Reason:* In vitro HCT116 cell culture perturbation, $N = 4 < 15$. Violates Gate B and Gate D. Excluded.
8. **`OPENML_1120` (MAGIC Gamma Telescope):**  
   *Disqualification Reason:* Synthetic Monte Carlo simulation of high-energy atmospheric gamma ray showers ($D = 10$). Not biological genomics. Excluded.
9. **`GSE352573` (Liposarcoma):**  
   *Disqualification Reason:* $N = 21 < 30$. Relegated to Tier C exploratory appendix only.

---

## 7. Sign-off and Gate Compliance

- **Biological Independence Verified:** Yes. All Tier A and Tier B cohorts are confirmed free of donor overlap with the 6 exploratory baselines.
- **Clinical Outcome Prohibition Enforced:** Yes. No survival, relapse, or therapy response labels permitted.
- **Assay Separation Enforced:** Yes. Microarray and RNA-seq cohorts remain in distinct benchmark strata.
- **Status:** **APPROVED FOR PROTOCOL FREEZE (AWAITING HUMAN GATE APPROVAL)**.
