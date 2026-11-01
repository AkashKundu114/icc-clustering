# Research Audit: Detailed Dataset Provenance & Patient Lineage Audit

**Document Reference:** `research_audit/cohort_independence/PROVENANCE_AUDIT.md`  
**Audit Date:** 2026-11-01  
**Auditor:** Senior Computational Biologist & Biomedical Data Curator  

---

## 1. Forensic Provenance Methodology

To establish whether datasets represent genuinely independent biological evidence, every candidate dataset was traced back through its upstream primary publication, supplementary data archives, clinical recruitment protocols, and microarray accession records. Datasets were categorized as follows:
- **Category A:** Confirmed Independent Biological Cohort (distinct clinical recruitment, distinct patient cohort).
- **Category B:** Independent Study with Potential Shared Author Laboratory or Uncertain Patient Overlap.
- **Category C:** Confirmed Shared Cohort or Composite Compilation (contains overlapping samples from another evaluated dataset).
- **Category D:** Exact / Near-Exact Derived Duplicate (reprocessed copy of an existing dataset).
- **Category E:** Disqualified / Mislabeled File (non-biological, synthetic, or wrong modality).

---

## 2. Dataset-by-Dataset Provenance Dossiers

### `colon`: Colon Cancer Gene Expression
- **Primary Publication:** Alon et al. 'Broad patterns of gene expression revealed by clustering analysis of tumor and normal colon tissues probed by oligonucleotide arrays.' PNAS 96.12 (1999): 6745-6750.
- **Authors:** U. Alon, N. Barkai, D. A. Notterman, K. Gish, S. Ybarra, D. Mack, A. J. Levine
- **Accession / Upstream Repository:** `Princeton Array Archive / OpenML 45087`
- **Assay Platform & Technology:** Affymetrix Hum60K oligonucleotide arrays (40 tumor biopsies, 22 normal colon tissues)
- **Patient Recruitment Details:** Independent clinical recruitment of 40 colon cancer patients from Princeton University Medical Center.
- **Lineage & Independence Assessment:** Confirmed Independent Biological Cohort. Benchmark standard since 1999.
- **Audit Classification:** **Category A (Confirmed Independent Cohort)**

### `srbct`: Small Round Blue Cell Tumors (SRBCT)
- **Primary Publication:** Khan et al. 'Classification and diagnostic prediction of cancers using gene expression profiling and artificial neural networks.' Nature Medicine 7.6 (2001): 673-679.
- **Authors:** J. Khan, J. S. Wei, M. Ringnér, L. H. Saal, M. Ladanyi, F. Westermann, F. Berthold, M. Schwab, C. R. Antonescu, C. Peterson, P. S. Meltzer
- **Accession / Upstream Repository:** `NCBI / NIH / OpenML 45101`
- **Assay Platform & Technology:** Custom cDNA microarrays with 2,308 filtered clones
- **Patient Recruitment Details:** 83 pediatric patient biopsies: 29 Ewing sarcoma (EWS), 11 Burkitt lymphoma (BL), 18 neuroblastoma (NB), and 25 rhabdomyosarcoma (RMS).
- **Lineage & Independence Assessment:** Confirmed Independent Biological Cohort. Independent NIH/NCI pediatric clinical trial recruitment.
- **Audit Classification:** **Category A (Confirmed Independent Cohort)**

### `leukemia`: Golub Acute Leukemia (ALL vs AML)
- **Primary Publication:** Golub et al. 'Molecular classification of cancer: class discovery and class prediction by gene expression monitoring.' Science 286.5439 (1999): 531-537.
- **Authors:** T. R. Golub, D. K. Slonim, P. Tamayo, C. Huard, M. Gaasenbeek, J. P. Mesirov, H. Coller, M. L. Loh, J. R. Downing, M. A. Caligiuri, C. D. Bloomfield, E. S. Lander
- **Accession / Upstream Repository:** `Whitehead/MIT Genome Center / OpenML 1104`
- **Assay Platform & Technology:** Affymetrix Hu6800 oligonucleotide arrays (7,129 probe sets)
- **Patient Recruitment Details:** 72 leukemia patients: 47 acute lymphoblastic leukemia (ALL; 38 B-cell, 9 T-cell) and 25 acute myeloid leukemia (AML) from St. Jude Children's Research Hospital and Cancer and Leukemia Group B (CALGB).
- **Lineage & Independence Assessment:** Confirmed Independent Biological Cohort. Foundational leukemia benchmark.
- **Audit Classification:** **Category A (Confirmed Independent Cohort)**

### `cns`: Central Nervous System Embryonal Tumors (CNS)
- **Primary Publication:** Pomeroy et al. 'Prediction of central nervous system embryonal tumour outcome based on gene expression.' Nature 415.6870 (2002): 436-442.
- **Authors:** S. L. Pomeroy, P. Tamayo, M. Gaasenbeek, L. M. Sturla, M. Angelo, M. E. McLaughlin, J. Y. Kim, L. C. Goumnerova, P. M. Black, C. Lau, J. C. Allen, D. Zagzag, M. M. Olson, T. Curran, C. Wetmore, J. A. Biegel, T. Poggio, S. Mukherjee, R. Rifkin, A. Califano, G. Stolovitzky, D. N. Louis, J. P. Mesirov, E. S. Lander, T. R. Golub
- **Accession / Upstream Repository:** `Broad/Whitehead Institute / OpenML 45086 / tumors_C (OpenML 1107)`
- **Assay Platform & Technology:** Affymetrix Hu6800 oligonucleotide array (7,129 probe sets)
- **Patient Recruitment Details:** 60 medulloblastoma biopsy specimens (39 patient survivors, 21 treatment failures).
- **Lineage & Independence Assessment:** Confirmed Independent Biological Cohort.
- **Audit Classification:** **Category A (Confirmed Independent Cohort)**

### `prostate`: Prostate Cancer Microarray
- **Primary Publication:** Singh et al. 'Gene expression correlates of clinical prostate cancer behavior.' Cancer Cell 1.2 (2002): 203-209.
- **Authors:** D. Singh, P. G. Febbo, K. Ross, D. G. Jackson, J. Manola, C. Ladd, P. Tamayo, A. A. Renshaw, A. V. D'Amico, J. P. Richie, E. S. Lander, M. Litzkow, K. R. Kantoff, T. R. Golub, W. R. Sellers
- **Accession / Upstream Repository:** `Broad Institute / Harvard / OpenML 45099`
- **Assay Platform & Technology:** Affymetrix U95Av2 arrays (12,600 probe sets)
- **Patient Recruitment Details:** 102 tissue samples: 50 non-tumor normal prostate tissues and 52 prostate tumor tissues from radical prostatectomies at Brigham and Women's Hospital.
- **Lineage & Independence Assessment:** Confirmed Independent Biological Cohort.
- **Audit Classification:** **Category A (Confirmed Independent Cohort)**

### `ovarian`: Ovarian Cancer Proteomics (SELDI)
- **Primary Publication:** Petricoin et al. 'Use of proteomic patterns in serum to identify ovarian cancer.' The Lancet 359.9306 (2002): 572-577.
- **Authors:** E. F. Petricoin, A. M. Ardekani, B. A. Hitt, P. J. Levine, V. A. Fusaro, S. M. Steinberg, G. B. Mills, C. Simone, D. A. Fishman, E. C. Kohn, L. A. Liotta
- **Accession / Upstream Repository:** `NCI-FDA Clinical Proteomics Program / OpenML 45098`
- **Assay Platform & Technology:** SELDI-TOF mass spectrometry (15,154 m/z spectral intensities)
- **Patient Recruitment Details:** 253 serum samples: 91 unaffected controls and 162 ovarian cancer patients (including 42 early Stage I cases).
- **Lineage & Independence Assessment:** Confirmed Independent Cohort. Serum mass spectrometry proteomic profile (independent biological modality from tissue transcriptomics).
- **Audit Classification:** **Category A (Confirmed Independent Cohort)**

### `zheng68k`: 10x PBMC 68k Single Cells (zheng68k / PBMC68k-reduced)
- **Primary Publication:** Zheng et al. 'Massively parallel digital transcriptional profiling of single cells.' Nature Communications 8 (2017): 14049.
- **Authors:** G. X. Y. Zheng, J. M. Terry, P. Belgrader, et al.
- **Accession / Upstream Repository:** `10x Genomics Fresh 68k PBMCs from Healthy Donor A`
- **Assay Platform & Technology:** Single-Cell Droplet Microfluidics (10x Chromium v1 chemistry)
- **Patient Recruitment Details:** 68,579 blood mononuclear cells from a single healthy blood donor (Donor A). Repository uses a reduced 700-cell subsample.
- **Lineage & Independence Assessment:** Single healthy biological donor. Note: `zheng68k` and `PBMC68k-reduced` are identical subsamples.
- **Audit Classification:** **Category A (Confirmed Independent scRNA-seq Cohort)**

### `glioma`: Glioma Benchmark in Audit Controls
- **Primary Publication:** Mislabeled in e1_extended_benchmarks.py as OpenML ID 1107 (Pomeroy 2002).
- **Authors:** Pomeroy et al. (Mislabeled as Nutt et al. 2003)
- **Accession / Upstream Repository:** `OpenML 1107 (tumors_C)`
- **Assay Platform & Technology:** Affymetrix Hu6800
- **Patient Recruitment Details:** 60 medulloblastoma patients (100% duplicate of CNS).
- **Lineage & Independence Assessment:** CRITICAL FLAW: 100% Bit-for-Bit Duplicate of CNS. OpenML ID 1107 is 'tumors_C' (Pomeroy CNS), not Nutt Glioma.
- **Audit Classification:** **Category D (Derived / 100% Exact Duplicate of CNS)**

### `lung_cancer`: Lung Cancer Benchmark in Audit Controls
- **Primary Publication:** Ramaswamy et al. PNAS 98(26), 15149-15154 (2001).
- **Authors:** Ramaswamy S, Tamayo P, Rifkin R, et al.
- **Accession / Upstream Repository:** `OpenML 1106 (GCM)`
- **Assay Platform & Technology:** Affymetrix Hu6800 / Hu35K (16,063 probe sets)
- **Patient Recruitment Details:** 190 tumors spanning 14 human carcinoma types (Global Cancer Map).
- **Lineage & Independence Assessment:** MISLABELED: It is GCM, not isolated lung cancer. Ingests 61/72 Golub Leukemia samples and 8/60 Pomeroy CNS samples.
- **Audit Classification:** **Category C (Shared Cohort / Composite Overlapping Dataset)**

### `breast_cancer_genomic`: Breast Cancer Genomic in Audit Controls
- **Primary Publication:** Bock RK et al. 'Methods for multidimensional event classification: a case study using images from a Cherenkov gamma-ray telescope.' NIM A (2004).
- **Authors:** R. K. Bock et al. (MAGIC Telescope Collaboration)
- **Accession / Upstream Repository:** `OpenML 1120 (MagicTelescope)`
- **Assay Platform & Technology:** Cherenkov atmospheric imaging telescope (10 image parameters)
- **Patient Recruitment Details:** Zero human patients. 19,020 simulated atmospheric gamma-ray and hadron showers.
- **Lineage & Independence Assessment:** CRITICAL MISATTRIBUTION: Non-biological astrophysics simulation. It has zero biological relevance.
- **Audit Classification:** **Category E (Unresolved / Disqualified Non-Biological Mislabeled File)**

### `lymphoma`: Lymphoma in Audit Controls
- **Primary Publication:** Risinger et al. / Armstrong et al. (AP Endometrium vs Kidney).
- **Authors:** Risinger JI et al. / Armstrong SA et al.
- **Accession / Upstream Repository:** `OpenML 1157 (AP_Endometrium_Kidney)`
- **Assay Platform & Technology:** Affymetrix HG-U95Av2 (10,935 probe sets)
- **Patient Recruitment Details:** 321 endometrial and kidney adenocarcinoma surgical specimens.
- **Lineage & Independence Assessment:** MISLABELED: It is Endometrium vs Kidney, not lymphoma. Represents an independent clinical cohort under wrong label.
- **Audit Classification:** **Category B (Independent Clinical Cohort, Misidentified in Script)**

### `gisette`: Gisette in Audit Controls
- **Primary Publication:** Jungle Chess Game Simulation (OpenML 41027).
- **Authors:** OpenML Contributor (Mislabeled as Isabelle Guyon NIPS 2003)
- **Accession / Upstream Repository:** `OpenML 41027 (jungle_chess_2pcs_raw_endgame_complete)`
- **Assay Platform & Technology:** Board game piece positions (D=6)
- **Patient Recruitment Details:** None (Board game endgames).
- **Lineage & Independence Assessment:** DISQUALIFIED: Mislabeled 6-variable chess endgame, not the NIPS 2003 handwriting benchmark.
- **Audit Classification:** **Category E (Disqualified Non-Biological Mislabeled File)**

### `usps`: USPS in Audit Controls
- **Primary Publication:** LeCun et al. MNIST Handwritten Digit Database (1998).
- **Authors:** Y. LeCun, C. Cortes, C. J. C. Burges
- **Accession / Upstream Repository:** `OpenML 554 (mnist_784)`
- **Assay Platform & Technology:** Grayscale 28x28 pixel images
- **Patient Recruitment Details:** None (Census Bureau employees and high-school students).
- **Lineage & Independence Assessment:** Non-biological image dataset. Mislabeled: it is MNIST ($28 \times 28 = 784$), not USPS ($16 \times 16 = 256$).
- **Audit Classification:** **Category E (Non-Biological Control)**

### `dlbcl`: DLBCL (Shipp et al. 2002)
- **Primary Publication:** Shipp et al. 'Diffuse large B-cell lymphoma outcome prediction by gene-expression profiling and supervised machine learning.' Nature Medicine 8.1 (2002): 68-74.
- **Authors:** M. A. Shipp, K. N. Ross, P. Tamayo, et al.
- **Accession / Upstream Repository:** `OpenML 45088 / DLBCL.arff.gz`
- **Assay Platform & Technology:** Affymetrix Hu6800 (5,469 filtered probe sets)
- **Patient Recruitment Details:** 77 lymphoma patients: 58 DLBCL vs 19 Follicular Lymphoma from Dana-Farber Cancer Institute.
- **Lineage & Independence Assessment:** Confirmed Independent Biological Cohort.
- **Audit Classification:** **Category A (Confirmed Independent Cohort)**

### `breast`: Breast Cancer 5-Year Metastasis (van 't Veer 2002)
- **Primary Publication:** van 't Veer et al. 'Gene expression profiling predicts clinical outcome of breast cancer.' Nature 415.6871 (2002): 530-536.
- **Authors:** L. J. van 't Veer, H. Dai, M. J. van de Vijver, et al.
- **Accession / Upstream Repository:** `OpenML 45085 / Breast.arff.gz`
- **Assay Platform & Technology:** Agilent Hu25k dual-channel oligonucleotide microarrays (24,481 probe sets)
- **Patient Recruitment Details:** 97 primary breast cancer patients: 51 disease-free (>5yr) vs 46 early distant metastases (<5yr) from Netherlands Cancer Institute.
- **Lineage & Independence Assessment:** Confirmed Independent Biological Cohort.
- **Audit Classification:** **Category A (Confirmed Independent Cohort)**

### `su2001`: 11 Human Solid Tumors (Su et al. 2001)
- **Primary Publication:** Su et al. 'Molecular classification of human carcinomas by use of gene expression signatures.' Cancer Research 61.19 (2001): 7388-7393.
- **Authors:** A. I. Su, J. B. Welsh, L. M. Sapinoso, et al.
- **Accession / Upstream Repository:** `OpenML 45084 / 11_Tumors.arff.gz`
- **Assay Platform & Technology:** Affymetrix GeneChip U95A (12,533 probe sets)
- **Patient Recruitment Details:** 174 primary solid tumor specimens spanning 11 carcinoma categories from multiple clinical centers.
- **Lineage & Independence Assessment:** Confirmed Independent Biological Cohort.
- **Audit Classification:** **Category A (Confirmed Independent Cohort)**

### `novartis`: 9 Human Carcinomas (Novartis / Su et al. 2002)
- **Primary Publication:** Su et al. 'Large-scale analysis of the human and mouse transcriptomes.' PNAS 99.7 (2002): 4465-4470.
- **Authors:** A. I. Su, T. Wiltshire, S. Batalov, et al.
- **Accession / Upstream Repository:** `OpenML 45083 / 9_Tumors.arff.gz`
- **Assay Platform & Technology:** Affymetrix HuGeneFL / U95 (5,726 probe sets)
- **Patient Recruitment Details:** 60 human carcinoma samples across 9 organ subtypes.
- **Lineage & Independence Assessment:** Independent study, but shares senior author laboratory (Genomics Institute of Novartis Research Foundation) with Su 2001.
- **Audit Classification:** **Category B (Independent Study, Author Lab Overlap)**

### `gcm`: Global Cancer Map (GCM / Ramaswamy 2001)
- **Primary Publication:** Ramaswamy et al. 'Multiclass cancer diagnosis using tumor gene expression signatures.' PNAS 98.26 (2001): 15149-15154.
- **Authors:** S. Ramaswamy, P. Tamayo, R. Rifkin, et al.
- **Accession / Upstream Repository:** `OpenML 1106 / GCM.arff.gz`
- **Assay Platform & Technology:** Affymetrix Hu6800 / Hu35K (16,063 probe sets)
- **Patient Recruitment Details:** 190 human tumors across 14 tissue types.
- **Lineage & Independence Assessment:** COMPOSITE OVERLAP: Assembled directly from Golub 1999 (61 leukemia samples) and Pomeroy 2002 (8 CNS samples).
- **Audit Classification:** **Category C (Composite Multi-Study Compilation with Confirmed Patient Overlap)**

### `endometrium`: Endometrium vs Kidney (Risinger 2003 / Armstrong)
- **Primary Publication:** Risinger et al. 'Global expression analysis of molecular markers in endometrial cancer.' Cancer Res 63.1 (2003): 6-11.
- **Authors:** J. I. Risinger, G. L. Maxwell, G. V. R. Chandramouli, et al.
- **Accession / Upstream Repository:** `OpenML 1157 / AP_Endometrium_Kidney.arff.gz`
- **Assay Platform & Technology:** Affymetrix HG-U95Av2 (10,936 probe sets)
- **Patient Recruitment Details:** 321 surgical tumor specimens: Endometrial and renal clear cell carcinomas.
- **Lineage & Independence Assessment:** Confirmed Independent Clinical Cohort.
- **Audit Classification:** **Category A (Confirmed Independent Cohort)**

### `gli`: Gliomas (Nutt et al. 2003, Genuine Glioma)
- **Primary Publication:** Nutt et al. 'Gene expression-based classification of malignant gliomas correlates better with survival than histologic grade.' Cancer Res 63.7 (2003): 1602-1607.
- **Authors:** C. L. Nutt, D. R. Mani, R. A. Betensky, et al.
- **Accession / Upstream Repository:** `OpenML 45089 / GLI.arff.gz`
- **Assay Platform & Technology:** Affymetrix U95Av2 (22,283 probe sets)
- **Patient Recruitment Details:** 85 human brain glioma specimens: 50 glioblastomas and 35 anaplastic oligodendrogliomas.
- **Lineage & Independence Assessment:** Genuine independent glioma cohort. (Note: NOT the duplicate OpenML 1107 tumors_C used in legacy audit controls).
- **Audit Classification:** **Category A (Confirmed Independent Cohort)**
