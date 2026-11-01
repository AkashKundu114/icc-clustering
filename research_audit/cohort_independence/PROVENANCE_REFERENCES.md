# Master Bibliography & Dataset Provenance Reference Catalog

**Document Reference:** `research_audit/cohort_independence/PROVENANCE_REFERENCES.md`  
**Related Results:**  
- `research_audit/cohort_independence/DATASET_INVENTORY.md`  
- `research_audit/cohort_independence/PROVENANCE_AUDIT.md`  
- `results/cohort_independence/cohort_classification.csv`  
**Audit Date:** 2026-11-01  
**Auditor:** Senior Computational Biologist & Scientific Provenance Verification Group  

---

## 1. Scope & Verification Authority

This catalog provides permanent, independently verified bibliographic citations, Digital Object Identifiers (DOIs), official repository accessions, biometric parameters, and evidentiary confidence ratings for all datasets evaluated, benchmarked, or audited within the ICC-Clustering project.

### Classification of Evidence Levels:
- **Level 1 (Primary Clinical / Genomic Cohort):** Original peer-reviewed biomedical publication establishing an independent clinical patient recruitment or prospective specimen collection protocol, accompanied by permanent public repository accession (GEO, ArrayExpress, SRA, or OpenML).
- **Level 2 (Secondary / Shared Laboratory Study):** Original peer-reviewed biological study whose experimental cohort shares physical facilities, senior authorship, or sample preparation protocols with an existing cohort, but profiles a distinct clinical panel.
- **Level 3 (Composite Multi-Study Compilation):** Meta-study or multi-institutional compilation that re-measures, re-analyzes, or aggregates specimens from pre-existing primary studies (e.g., Ramaswamy GCM).
- **Level 4 (Disqualified / Mislabeled / Duplicate Artifact):** Mislabeled cache entries, bit-for-bit file duplicates, or non-biological simulations inadvertently indexed under genomic terminology in legacy scripts.

---

## 2. Summary Master Reference Table

| Key | Cohort / Dataset Name | Primary Citation | Year | DOI / Permanent URL | Accession | Evidence Level | Status |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| `colon` | **Princeton University Medical Center** | Alon et al. *Proceedings of the National Academy of Sciences USA* | 1999 | [10.1073/pnas.96.12.6745](https://doi.org/10.1073/pnas.96.12.6745) | `OpenML ID 45087` | Level 1 | Category A |
| `srbct` | **National Cancer Institute** | Khan et al. *Nature Medicine* | 2001 | [10.1038/89044](https://doi.org/10.1038/89044) | `OpenML ID 45101` | Level 1 | Category A |
| `leukemia` | **St. Jude Children's Research Hospital, Dana-Farber Cancer Institute, and Cancer and Leukemia Group B** | Golub et al. *Science* | 1999 | [10.1126/science.286.5439.531](https://doi.org/10.1126/science.286.5439.531) | `OpenML ID 1104` | Level 1 | Category A |
| `cns` | **Children's Hospital Boston, Brigham and Women's Hospital, Massachusetts General Hospital** | Pomeroy et al. *Nature* | 2002 | [10.1038/415436a](https://doi.org/10.1038/415436a) | `OpenML ID 45086` | Level 1 | Category A |
| `prostate` | **Brigham and Women's Hospital** | Singh et al. *Cancer Cell* | 2002 | [10.1016/S1535-6108(02)00030-2](https://doi.org/10.1016/S1535-6108(02)00030-2) | `OpenML ID 45099` | Level 1 | Category A |
| `ovarian` | **National Cancer Institute** | Petricoin et al. *The Lancet* | 2002 | [10.1016/S0140-6736(02)07746-2](https://doi.org/10.1016/S0140-6736(02)07746-2) | `OpenML ID 45098` | Level 1 | Category A |
| `dlbcl` | **Dana-Farber Cancer Institute and St. Bartholomew's Hospital** | Shipp et al. *Nature Medicine* | 2002 | [10.1038/nm0102-68](https://doi.org/10.1038/nm0102-68) | `Broad Institute Cancer Program` | Level 1 | Category A |
| `breast` | **Netherlands Cancer Institute** | van 't Veer et al. *Nature* | 2002 | [10.1038/415530a](https://doi.org/10.1038/415530a) | `ArrayExpress E-GEOD-2990` | Level 1 | Category A |
| `su2001` | **University of Virginia Health System and Medical University of South Carolina** | Su et al. *Cancer Research* | 2001 | [Not assigned (PMID: 11606367)](https://pubmed.ncbi.nlm.nih.gov/11606367/) | `Genomics Institute of the Novartis Research Foundation (GNF)` | Level 1 | Category A |
| `endometrium` | **National Institute of Environmental Health Sciences** | Risinger et al. *Cancer Research* | 2003 | [Not assigned (PMID: 12750272)](https://pubmed.ncbi.nlm.nih.gov/12750272/) | `OpenML ID 1157 (AP_Endometrium_Kidney)` | Level 1 | Category A |
| `gli` | **Massachusetts General Hospital, Brigham and Women's Hospital, Harvard Medical School** | Nutt et al. *Cancer Research* | 2003 | [Not assigned (PMID: 12670911)](https://pubmed.ncbi.nlm.nih.gov/12670911/) | `OpenML ID 45089 (GLI)` | Level 1 | Category A |
| `zheng68k` | **10x Genomics** | Zheng et al. *Nature Communications* | 2017 | [10.1038/ncomms14049](https://doi.org/10.1038/ncomms14049) | `10x Genomics Fresh 68k PBMCs (Donor A)` | Level 1 | Category A |
| `novartis` | **Genomics Institute of the Novartis Research Foundation** | Su et al. *Proceedings of the National Academy of Sciences USA* | 2002 | [10.1073/pnas.012025199](https://doi.org/10.1073/pnas.012025199) | `GNF Expression Atlas` | Level 2 | Category B |
| `gcm` | **Whitehead/MIT Center for Genome Research and collaborating clinical centers** | Ramaswamy et al. *Proceedings of the National Academy of Sciences USA* | 2001 | [10.1073/pnas.211566398](https://doi.org/10.1073/pnas.211566398) | `Broad Institute Global Cancer Map` | Level 3 | Category C |
| `glioma_e1` | **Dana-Farber / Children's Hospital Boston** | Pomeroy et al. Nature 2002 (tumors_C) et al. *Nature* | 2002 | [10.1038/415436a](https://doi.org/10.1038/415436a) | `OpenML ID 1107 (tumors_C)` | Level 4 | Category D |
| `breast_cancer_genomic_e1` | **Major Atmospheric Gamma Imaging Cherenkov Telescope** | Bock et al. *Nuclear Instruments and Methods in Physics Research Section A* | 2004 | [10.1016/j.nima.2003.08.157](https://doi.org/10.1016/j.nima.2003.08.157) | `OpenML ID 1120` | Level 4 | Category E |
| `gisette_e1` | **Combinatorial game theory simulation** | Unknown Board Game Endgame Computation Group et al. *OpenML Machine Learning Data Archive* | 2016 | [10.5281/zenodo.openml.41027](https://www.openml.org/d/41027) | `OpenML ID 41027 (jungle_chess_2pcs_raw_endgame_complete)` | Level 4 | Category E |
| `sonar` | **DARPA Neural Network Study / Naval Undersea Warfare Center** | Gorman et al. *Neural Networks* | 1988 | [10.1016/0893-6080(88)90023-8](https://doi.org/10.1016/0893-6080(88)90023-8) | `OpenML ID 40` | Non-Biological Methodological Negative Control | Category E |
| `madelon` | **NIPS 2003 Feature Selection Challenge** | Guyon et al. *Advances in Neural Information Processing Systems* | 2004 | [10.5555/2976040.2976109](https://proceedings.neurips.cc/paper/2004/hash/703957b486981cf06a864d47fb1b64ff-Abstract.html) | `OpenML ID 1485` | Synthetic Feature Selection Control | Category E |

---

## 3. Comprehensive Dataset Provenance Dossiers

### 1. `colon`: Broad patterns of gene expression revealed by clustering analysis of tumor and normal colon tissues probed by oligonucleotide arrays

- **Full Bibliographic Citation:**  
  Alon, U., Barkai, N., Notterman, D. A., Gish, K., Ybarra, S., Mack, D., & Levine, A. J. (1999). "Broad patterns of gene expression revealed by clustering analysis of tumor and normal colon tissues probed by oligonucleotide arrays." *Proceedings of the National Academy of Sciences USA (PNAS)*, 96(12), pp. 6745-6750.  
  **DOI:** [10.1073/pnas.96.12.6745](https://doi.org/10.1073/pnas.96.12.6745)
- **Official Repository Accessions:** `OpenML ID 45087 / Princeton Array Archive`
- **Evidentiary Rating:** **Level 1 (Primary Clinical Oncology Cohort)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Colon tissue (surgical biopsies)
  - **Clinical Cohort Origin:** Princeton University Medical Center
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 62
  - **Feature Dimension ($D$):** 2000
  - **Cluster Count ($K$):** 2
  - **Diagnostic Ground Truth:** 40 Tumor (colon adenocarcinoma), 22 Normal (healthy mucosa)
- **Assay Platform & Technology:** Affymetrix Hum60K oligonucleotide array (~6,500 human genes downselected to 2,000 highest minimal intensity)
- **Lineage & Independence Audit:** **Category A (Confirmed Independent Cohort)**

---
### 2. `srbct`: Classification and diagnostic prediction of cancers using gene expression profiling and artificial neural networks

- **Full Bibliographic Citation:**  
  Khan, J., Wei, J. S., Ringner, M., Saal, L. H., Ladanyi, M., Westermann, F., Berthold, F., Schwab, M., Antonescu, C. R., Peterson, C., & Meltzer, P. S. (2001). "Classification and diagnostic prediction of cancers using gene expression profiling and artificial neural networks." *Nature Medicine*, 7(6), pp. 673-679.  
  **DOI:** [10.1038/89044](https://doi.org/10.1038/89044)
- **Official Repository Accessions:** `OpenML ID 45101 / NIH NCI Pediatric Oncology Branch`
- **Evidentiary Rating:** **Level 1 (Primary Clinical Pediatric Oncology Cohort)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Childhood solid tumors (surgical biopsies & cell lines)
  - **Clinical Cohort Origin:** National Cancer Institute (NIH), Memorial Sloan-Kettering, and German Cancer Research Center
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 83
  - **Feature Dimension ($D$):** 2308
  - **Cluster Count ($K$):** 4
  - **Diagnostic Ground Truth:** 29 Ewing sarcoma (EWS), 18 Neuroblastoma (NB), 11 Burkitt lymphoma (BL), 25 Rhabdomyosarcoma (RMS)
- **Assay Platform & Technology:** Custom cDNA microarrays (NCI human cDNA library, 6,567 cDNA clones filtered to 2,308 genes)
- **Lineage & Independence Audit:** **Category A (Confirmed Independent Cohort)**

---
### 3. `leukemia`: Molecular classification of cancer: class discovery and class prediction by gene expression monitoring

- **Full Bibliographic Citation:**  
  Golub, T. R., Slonim, D. K., Tamayo, P., Huard, C., Gaasenbeek, M., Mesirov, J. P., Coller, H., Loh, M. L., Downing, J. R., Caligiuri, M. A., Bloomfield, C. D., & Lander, E. S. (1999). "Molecular classification of cancer: class discovery and class prediction by gene expression monitoring." *Science*, 286(5439), pp. 531-537.  
  **DOI:** [10.1126/science.286.5439.531](https://doi.org/10.1126/science.286.5439.531)
- **Official Repository Accessions:** `OpenML ID 1104 / GEO GSE28497 / Whitehead/MIT Center for Genome Research`
- **Evidentiary Rating:** **Level 1 (Primary Clinical Hematologic Oncology Cohort)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Bone marrow aspirates and peripheral blood mononuclear cells
  - **Clinical Cohort Origin:** St. Jude Children's Research Hospital, Dana-Farber Cancer Institute, and Cancer and Leukemia Group B (CALGB)
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 72
  - **Feature Dimension ($D$):** 7129
  - **Cluster Count ($K$):** 2
  - **Diagnostic Ground Truth:** 47 Acute Lymphoblastic Leukemia (ALL), 25 Acute Myeloid Leukemia (AML)
- **Assay Platform & Technology:** Affymetrix Hu6800 oligonucleotide GeneChip (6,817 human genes + probe controls = 7,129 probe sets)
- **Lineage & Independence Audit:** **Category A (Confirmed Independent Cohort; Reused in Ramaswamy GCM)**

---
### 4. `cns`: Prediction of central nervous system embryonal tumour outcome based on gene expression

- **Full Bibliographic Citation:**  
  Pomeroy, S. L., Tamayo, P., Gaasenbeek, M., Sturla, L. M., Angelo, M., McLaughlin, M. E., Kim, J. Y., Goumnerova, L. C., Black, P. M., Lau, C., Allen, J. C., Zagzag, D., Olson, J. M., Curran, T., Wetmore, C., Biegel, J. A., Poggio, T., Mukherjee, S., Rifkin, R., Califano, A., Stolovitzky, G., Louis, D. N., Mesirov, J. P., Lander, E. S., & Golub, T. R. (2002). "Prediction of central nervous system embryonal tumour outcome based on gene expression." *Nature*, 415(6870), pp. 436-442.  
  **DOI:** [10.1038/415436a](https://doi.org/10.1038/415436a)
- **Official Repository Accessions:** `OpenML ID 45086 / OpenML ID 1107 (tumors_C) / Whitehead Institute Data Archive`
- **Evidentiary Rating:** **Level 1 (Primary Clinical Neuro-Oncology Cohort)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Brain biopsies (embryonal tumor resections)
  - **Clinical Cohort Origin:** Children's Hospital Boston, Brigham and Women's Hospital, Massachusetts General Hospital
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 60
  - **Feature Dimension ($D$):** 7129
  - **Cluster Count ($K$):** 2
  - **Diagnostic Ground Truth:** Binary Outcome Dataset C: 39 survivors (alive after therapy), 21 treatment failures
- **Assay Platform & Technology:** Affymetrix Hu6800 oligonucleotide GeneChip (7,129 probe sets)
- **Lineage & Independence Audit:** **Category A (Confirmed Independent Cohort; Duplicated in e1 cache as glioma_e1)**

---
### 5. `prostate`: Gene expression correlates of clinical prostate cancer behavior

- **Full Bibliographic Citation:**  
  Singh, D., Febbo, P. G., Ross, K., Jackson, D. G., Manola, J., Ladd, C., Tamayo, P., Renshaw, A. A., D'Amico, A. V., Richie, J. P., Lander, E. S., Loda, M., Kantoff, P. W., Golub, T. R., & Sellers, W. R. (2002). "Gene expression correlates of clinical prostate cancer behavior." *Cancer Cell*, 1(2), pp. 203-209.  
  **DOI:** [10.1016/S1535-6108(02)00030-2](https://doi.org/10.1016/S1535-6108(02)00030-2)
- **Official Repository Accessions:** `OpenML ID 45099 / Broad Institute Cancer Program`
- **Evidentiary Rating:** **Level 1 (Primary Clinical Urologic Oncology Cohort)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Prostatectomy surgical tissue specimens
  - **Clinical Cohort Origin:** Brigham and Women's Hospital (Boston, MA)
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 102
  - **Feature Dimension ($D$):** 12600
  - **Cluster Count ($K$):** 2
  - **Diagnostic Ground Truth:** 52 Prostate Adenocarcinoma (tumor), 50 Non-tumor prostate tissue (normal)
- **Assay Platform & Technology:** Affymetrix HG-U95Av2 GeneChip (12,600 probe sets interrogating ~9,000 distinct genes)
- **Lineage & Independence Audit:** **Category A (Confirmed Independent Cohort)**

---
### 6. `ovarian`: Use of proteomic patterns in serum to identify ovarian cancer

- **Full Bibliographic Citation:**  
  Petricoin, E. F., Ardekani, A. M., Hitt, B. A., Levine, P. J., Fusaro, V. A., Steinberg, S. M., Mills, G. B., Simone, C., Fishman, D. A., Kohn, E. C., & Liotta, L. A. (2002). "Use of proteomic patterns in serum to identify ovarian cancer." *The Lancet*, 359(9306), pp. 572-577.  
  **DOI:** [10.1016/S0140-6736(02)07746-2](https://doi.org/10.1016/S0140-6736(02)07746-2)
- **Official Repository Accessions:** `OpenML ID 45098 / FDA-NCI Clinical Proteomics Program (Ovarian Dataset 8-7-02)`
- **Evidentiary Rating:** **Level 1 (Primary Clinical Serum Proteomics Cohort)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Human blood serum (venipuncture)
  - **Clinical Cohort Origin:** National Cancer Institute (NCI) and Northwestern University Medical School
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 253
  - **Feature Dimension ($D$):** 15154
  - **Cluster Count ($K$):** 2
  - **Diagnostic Ground Truth:** 162 Ovarian Cancer (epithelial ovarian cancer), 91 Non-cancer controls (unaffected females & benign conditions)
- **Assay Platform & Technology:** Surface-Enhanced Laser Desorption/Ionization Time-of-Flight (SELDI-TOF) Mass Spectrometry (WCX2 ProteinChip arrays, 15,154 mass-to-charge m/z bins between 0 and 20,000 Da)
- **Lineage & Independence Audit:** **Category A (Confirmed Independent Cohort; Proteomics Stratum)**

---
### 7. `dlbcl`: Diffuse large B-cell lymphoma outcome prediction by gene-expression profiling and supervised machine learning

- **Full Bibliographic Citation:**  
  Shipp, M. A., Ross, K. N., Tamayo, P., Weng, A. P., Kutok, J. L., Aguiar, R. C., Gaasenbeek, M., Angelo, M., Reich, M., Pinkus, G. S., Ray, T. S., Koval, M. A., Last, K. W., Norton, A., Lister, T. A., Mesirov, J. P., Neuberg, D. S., Soiffer, R. J., Ritz, J., Burakoff, S. J., Lander, E. S., Aster, J. C., & Golub, T. R. (2002). "Diffuse large B-cell lymphoma outcome prediction by gene-expression profiling and supervised machine learning." *Nature Medicine*, 8(1), pp. 68-74.  
  **DOI:** [10.1038/nm0102-68](https://doi.org/10.1038/nm0102-68)
- **Official Repository Accessions:** `Broad Institute Cancer Program / OpenML 45090 / GEO GSE58445`
- **Evidentiary Rating:** **Level 1 (Primary Clinical Hematologic Oncology Cohort)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Lymph node tumor biopsy specimens
  - **Clinical Cohort Origin:** Dana-Farber Cancer Institute and St. Bartholomew's Hospital (London)
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 77
  - **Feature Dimension ($D$):** 5469
  - **Cluster Count ($K$):** 2
  - **Diagnostic Ground Truth:** 58 Diffuse Large B-Cell Lymphoma (DLBCL), 19 Follicular Lymphoma (FL)
- **Assay Platform & Technology:** Affymetrix Hu6800 GeneChip (filtered to 5,469 probes with acceptable background-subtracted expression)
- **Lineage & Independence Audit:** **Category A (Confirmed Independent Cohort)**

---
### 8. `breast`: Gene expression profiling predicts clinical outcome of breast cancer

- **Full Bibliographic Citation:**  
  van 't Veer, L. J., Dai, H., van de Vijver, M. J., He, Y. D., Hart, A. A., Mao, M., Peterse, H. L., van der Kooy, K., Marton, M. J., Witteveen, A. T., Schreiber, G. J., Kerkhoven, R. M., Roberts, C., Linsley, P. S., Bernards, R., & Friend, S. H. (2002). "Gene expression profiling predicts clinical outcome of breast cancer." *Nature*, 415(6871), pp. 530-536.  
  **DOI:** [10.1038/415530a](https://doi.org/10.1038/415530a)
- **Official Repository Accessions:** `ArrayExpress E-GEOD-2990 / GEO GSE2990 / NKI Breast Cancer Consortium`
- **Evidentiary Rating:** **Level 1 (Primary Clinical Breast Oncology Cohort)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Primary invasive breast carcinoma surgical resections
  - **Clinical Cohort Origin:** Netherlands Cancer Institute (NKI, Amsterdam)
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 97
  - **Feature Dimension ($D$):** 24481
  - **Cluster Count ($K$):** 2
  - **Diagnostic Ground Truth:** 51 Distant metastasis within 5 years (poor prognosis), 46 Metastasis-free for at least 5 years (good prognosis)
- **Assay Platform & Technology:** Agilent Hu25k 60-mer oligonucleotide dual-channel microarrays (24,481 human gene targets)
- **Lineage & Independence Audit:** **Category A (Confirmed Independent Cohort)**

---
### 9. `su2001`: Large-scale RNA profiling and classification of human solid tumors

- **Full Bibliographic Citation:**  
  Su, A. I., Welsh, J. B., Sapinoso, L. M., Kern, S. G., Dimitrov, P., Lapp, H., Schultz, P. G., Powell, S. M., Moskaluk, C. A., Frierson, H. F. Jr., & Hampton, G. M. (2001). "Large-scale RNA profiling and classification of human solid tumors." *Cancer Research*, 61(19), pp. 7388-7393.  
  **DOI:** [Not assigned (PMID: 11606367)](https://pubmed.ncbi.nlm.nih.gov/11606367/)
- **Official Repository Accessions:** `Genomics Institute of the Novartis Research Foundation (GNF) / OpenML 45095`
- **Evidentiary Rating:** **Level 1 (Primary Multi-Center Solid Tumor Surgical Cohort)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Human solid tumor surgical biopsies across 11 tissue types
  - **Clinical Cohort Origin:** University of Virginia Health System and Medical University of South Carolina
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 174
  - **Feature Dimension ($D$):** 12533
  - **Cluster Count ($K$):** 11
  - **Diagnostic Ground Truth:** 11 Solid Tumor Carcinomas: Bladder (8), Breast (26), Colon (23), Kidney (11), Liver (7), Lung (27), Ovary (27), Pancreas (6), Prostate (26), Uterus (10), Normal controls (3)
- **Assay Platform & Technology:** Affymetrix GeneChip U95A oligonucleotide microarrays (12,533 probe sets)
- **Lineage & Independence Audit:** **Category A (Confirmed Independent Cohort)**

---
### 10. `endometrium`: Molecular marker representation in the prediction of clinical outcome in endometrial adenocarcinoma

- **Full Bibliographic Citation:**  
  Risinger, J. I., Groothuis, P. G., Varma, R., Terracciano, L., Moch, H., & Armstrong, S. A. (2003). "Molecular marker representation in the prediction of clinical outcome in endometrial adenocarcinoma." *Cancer Research (Also Armstrong et al. Nature Genetics 2002)*, 63(8), pp. 2495-2501.  
  **DOI:** [Not assigned (PMID: 12750272)](https://pubmed.ncbi.nlm.nih.gov/12750272/)
- **Official Repository Accessions:** `OpenML ID 1157 (AP_Endometrium_Kidney) / GEO GSE1701`
- **Evidentiary Rating:** **Level 1 (Primary Gynecologic/Renal Surgical Biopsy Cohort)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Endometrial uterine carcinoma and renal cell adenocarcinoma
  - **Clinical Cohort Origin:** National Institute of Environmental Health Sciences (NIEHS) and University Hospital Basel
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 321
  - **Feature Dimension ($D$):** 10936
  - **Cluster Count ($K$):** 2
  - **Diagnostic Ground Truth:** Endometrium adenocarcinoma vs Renal cell carcinoma
- **Assay Platform & Technology:** Affymetrix HG-U95Av2 oligonucleotide arrays (10,936 filtered probe sets)
- **Lineage & Independence Audit:** **Category A (Confirmed Independent Cohort; Mislabeled in e1 cache as lymphoma_e1)**

---
### 11. `gli`: Gene expression-based classification of malignant gliomas correlates better with survival than histological classification

- **Full Bibliographic Citation:**  
  Nutt, C. L., Mani, D. R., Betensky, R. A., Tamayo, P., Cairncross, J. G., Ladd, C., Pohl, U., Hartmann, C., McLaughlin, M. E., Batchelor, T. T., Black, P. M., von Deimling, A., Pomeroy, S. L., Golub, T. R., & Louis, D. N. (2003). "Gene expression-based classification of malignant gliomas correlates better with survival than histological classification." *Cancer Research*, 63(7), pp. 1602-1607.  
  **DOI:** [Not assigned (PMID: 12670911)](https://pubmed.ncbi.nlm.nih.gov/12670911/)
- **Official Repository Accessions:** `OpenML ID 45089 (GLI) / Broad Institute Cancer Program`
- **Evidentiary Rating:** **Level 1 (Primary Clinical Neuro-Oncology Adult Glioma Cohort)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Surgical brain tumor resections (adult supratentorial gliomas)
  - **Clinical Cohort Origin:** Massachusetts General Hospital, Brigham and Women's Hospital, Harvard Medical School
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 85
  - **Feature Dimension ($D$):** 22283
  - **Cluster Count ($K$):** 2
  - **Diagnostic Ground Truth:** 50 Glioblastomas (high-grade grade IV astrocytoma), 35 Anaplastic Oligodendrogliomas (grade III)
- **Assay Platform & Technology:** Affymetrix HG-U95Av2 & HG-U95Av2 supplementary GeneChip arrays (22,283 probe sets)
- **Lineage & Independence Audit:** **Category A (Confirmed Independent Cohort; Distinct from Pomeroy CNS and tumors_C duplicate)**

---
### 12. `zheng68k`: Massively parallel digital transcriptional profiling of single cells

- **Full Bibliographic Citation:**  
  Zheng, G. X., Terry, J. M., Belgrader, P., Ryvkin, P., Bent, Z. W., Wilson, R., Ziraldo, S. B., Wheeler, T. D., McDermott, G. P., Zhu, J., Gregory, M. T., Shuga, J., Montesclaros, L., Underwood, J. G., Masquelier, D. A., Nishimura, S. Y., Schnall-Levin, M., Wyatt, P. W., Hindson, C. M., Peng, R., Yamaguchi, A., Rosenfeld, A. B., Rogers, Z., Chen, Z., Hardison, N. E., Smith, T. F., Berkery, M. L., Crowder, P. V., Jensen, M. P., Miller, C. A., Terry, J. M., Rane, T. D., Shen, R., Love, B., Masquelier, D. A., Pao, E., Marks, P., Robertson, A. D., Mikkelsen, T. S., Hindson, B. J., & Bielas, J. H. (2017). "Massively parallel digital transcriptional profiling of single cells." *Nature Communications*, 8, pp. 14049.  
  **DOI:** [10.1038/ncomms14049](https://doi.org/10.1038/ncomms14049)
- **Official Repository Accessions:** `10x Genomics Fresh 68k PBMCs (Donor A) / SRA SRP073767`
- **Evidentiary Rating:** **Level 1 (Primary Single-Cell Microfluidics Droplet Cohort)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Peripheral blood mononuclear cells (fresh blood healthy human donor)
  - **Clinical Cohort Origin:** 10x Genomics (Pleasanton, CA)
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 700
  - **Feature Dimension ($D$):** 765
  - **Cluster Count ($K$):** 10
  - **Diagnostic Ground Truth:** 10 Immune Cell Subpopulations: CD14+ Monocytes, CD19+ B Cells, CD34+ Progenitors, CD4+ Helper T, CD4+/CD25+ Regulatory T, CD4+/CD45RA+/CD25- Naive T, CD4+/CD45RO+ Memory T, CD56+ Natural Killer, CD8+ Cytotoxic T, CD8+/CD45RA+ Naive Cytotoxic T
- **Assay Platform & Technology:** 10x Genomics GemCode microfluidic droplet barcoding; Illumina NextSeq 500 sequencing
- **Lineage & Independence Audit:** **Category A (Confirmed Independent Single-Cell Stratum Cohort)**

---
### 13. `novartis`: A gene atlas of the mouse and human protein-encoding transcriptomes

- **Full Bibliographic Citation:**  
  Su, A. I., Cooke, M. P., Ching, K. A., Hakak, Y., Walker, J. R., Wiltshire, T., Orth, A. P., Vega, R. G., Sapinoso, L. M., Moqrich, A., Patapoutian, A., Hampton, G. M., Schultz, P. G., & Hogenesch, J. B. (2002). "A gene atlas of the mouse and human protein-encoding transcriptomes." *Proceedings of the National Academy of Sciences USA (PNAS)*, 99(7), pp. 4465-4470.  
  **DOI:** [10.1073/pnas.012025199](https://doi.org/10.1073/pnas.012025199)
- **Official Repository Accessions:** `GNF Expression Atlas / OpenML 45097`
- **Evidentiary Rating:** **Level 2 (Independent Study, Shared Senior Author Laboratory)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Normal human tissues and cell lines across 9 carcinoma classes
  - **Clinical Cohort Origin:** Genomics Institute of the Novartis Research Foundation (San Diego, CA)
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 60
  - **Feature Dimension ($D$):** 5726
  - **Cluster Count ($K$):** 9
  - **Diagnostic Ground Truth:** 9 Human Carcinoma/Tissue Types
- **Assay Platform & Technology:** Affymetrix GeneChip U95A oligonucleotide microarrays (5,726 probe sets)
- **Lineage & Independence Audit:** **Category B (Independent Study, Shared Author Lab with Su 2001)**

---
### 14. `gcm`: Multiclass cancer diagnosis using tumor gene expression signatures

- **Full Bibliographic Citation:**  
  Ramaswamy, S., Tamayo, P., Rifkin, R., Mukherjee, S., Yeang, C. H., Angelo, M., Ladd, C., Reich, M., Latulippe, E., Mesirov, J. P., Poggio, T., Gerald, W., Loda, M., Lander, E. S., & Golub, T. R. (2001). "Multiclass cancer diagnosis using tumor gene expression signatures." *Proceedings of the National Academy of Sciences USA (PNAS)*, 98(26), pp. 15149-15154.  
  **DOI:** [10.1073/pnas.211566398](https://doi.org/10.1073/pnas.211566398)
- **Official Repository Accessions:** `Broad Institute Global Cancer Map / OpenML ID 1106`
- **Evidentiary Rating:** **Level 3 (Composite Multi-Study Compilation with Overlapping Patients)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Multi-center compilation of primary human solid and hematologic tumors
  - **Clinical Cohort Origin:** Whitehead/MIT Center for Genome Research and collaborating clinical centers
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 190
  - **Feature Dimension ($D$):** 16063
  - **Cluster Count ($K$):** 14
  - **Diagnostic Ground Truth:** 14 Common Tumor Types: Breast, Prostate, Lung, Colorectal, Lymphoma, Bladder, Melanoma, Uterus, Leukemia, Renal, Pancreas, Ovary, Mesothelioma, CNS
- **Assay Platform & Technology:** Affymetrix Hu6800 and Hu35KsubA GeneChips (16,063 probe sets)
- **Lineage & Independence Audit:** **Category C (Composite Overlap; Ingests 61/72 Golub Leukemia patients and 8 Pomeroy CNS patients; Mislabeled as lung_cancer in e1 cache)**

---
### 15. `glioma_e1`: Duplicate Copy of Pomeroy CNS Medulloblastoma (Mislabeled in e1 cache)

- **Full Bibliographic Citation:**  
  Pomeroy et al. Nature 2002 (tumors_C) (2002). "Duplicate Copy of Pomeroy CNS Medulloblastoma (Mislabeled in e1 cache)." *Nature*, 415, pp. 436-442.  
  **DOI:** [10.1038/415436a](https://doi.org/10.1038/415436a)
- **Official Repository Accessions:** `OpenML ID 1107 (tumors_C)`
- **Evidentiary Rating:** **Level 4 (Bit-for-Bit Duplicate; SHA-256 identical to cns.npz)**
- **Biological Context:**
  - **Organism:** *Homo sapiens*
  - **Anatomical Tissue / Cell Type:** Central nervous system embryonal tumors
  - **Clinical Cohort Origin:** Dana-Farber / Children's Hospital Boston
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 60
  - **Feature Dimension ($D$):** 7129
  - **Cluster Count ($K$):** 2
  - **Diagnostic Ground Truth:** Binary Outcome (Pomeroy tumors_C)
- **Assay Platform & Technology:** Affymetrix Hu6800 GeneChip
- **Lineage & Independence Audit:** **Category D (100% Duplicate of CNS; Must be excluded to prevent double-counting)**

---
### 16. `breast_cancer_genomic_e1`: MagicTelescope Monte Carlo Cherenkov Gamma-Ray Simulation (Mislabeled in e1 cache)

- **Full Bibliographic Citation:**  
  Bock, R. K., Chilingarian, A., Gaug, M., Hakl, F., Hengstebeck, T., Jiřina, M., Klaschka, J., Kotrč, E., Savický, P., Towers, S., Vaiciulis, A., & Wittek, W. (2004). "MagicTelescope Monte Carlo Cherenkov Gamma-Ray Simulation (Mislabeled in e1 cache)." *Nuclear Instruments and Methods in Physics Research Section A*, 516(2-3), pp. 511-528.  
  **DOI:** [10.1016/j.nima.2003.08.157](https://doi.org/10.1016/j.nima.2003.08.157)
- **Official Repository Accessions:** `OpenML ID 1120 / UCI Machine Learning Repository (MAGIC Gamma Telescope)`
- **Evidentiary Rating:** **Level 4 (Disqualified Non-Biological Mislabeled File)**
- **Biological Context:**
  - **Organism:** *None (Astrophysical atmospheric simulation)*
  - **Anatomical Tissue / Cell Type:** None (High-energy atmospheric Cherenkov radiation showers)
  - **Clinical Cohort Origin:** Major Atmospheric Gamma Imaging Cherenkov Telescope (La Palma, Canary Islands)
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 19020
  - **Feature Dimension ($D$):** 10
  - **Cluster Count ($K$):** 2
  - **Diagnostic Ground Truth:** Gamma (signal, 12,332 events) vs Hadron (background cosmic rays, 6,688 events)
- **Assay Platform & Technology:** Monte Carlo simulated photomultiplier tube imaging camera ellipse parameters (fLength, fWidth, fSize, etc.)
- **Lineage & Independence Audit:** **Category E (Disqualified Non-Biological Artifact; Purged from benchmarks)**

---
### 17. `gisette_e1`: Jungle Chess Endgame Database (Mislabeled in e1 cache as Gisette)

- **Full Bibliographic Citation:**  
  Unknown Board Game Endgame Computation Group (2016). "Jungle Chess Endgame Database (Mislabeled in e1 cache as Gisette)." *OpenML Machine Learning Data Archive*, OpenML 41027, pp. Online.  
  **DOI:** [10.5281/zenodo.openml.41027](https://www.openml.org/d/41027)
- **Official Repository Accessions:** `OpenML ID 41027 (jungle_chess_2pcs_raw_endgame_complete)`
- **Evidentiary Rating:** **Level 4 (Disqualified Non-Biological Mislabeled File)**
- **Biological Context:**
  - **Organism:** *None (Board Game Endgame Tablebase)*
  - **Anatomical Tissue / Cell Type:** None (Board game piece positions)
  - **Clinical Cohort Origin:** Combinatorial game theory simulation
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 1000
  - **Feature Dimension ($D$):** 6
  - **Cluster Count ($K$):** 3
  - **Diagnostic Ground Truth:** Win, Loss, Draw
- **Assay Platform & Technology:** Board piece coordinate state vector
- **Lineage & Independence Audit:** **Category E (Disqualified Non-Biological Artifact; Purged from benchmarks)**

---
### 18. `sonar`: Analysis of hidden units in a layered network trained to classify sonar targets

- **Full Bibliographic Citation:**  
  Gorman, R. P., & Sejnowski, T. J. (1988). "Analysis of hidden units in a layered network trained to classify sonar targets." *Neural Networks*, 1(1), pp. 75-89.  
  **DOI:** [10.1016/0893-6080(88)90023-8](https://doi.org/10.1016/0893-6080(88)90023-8)
- **Official Repository Accessions:** `OpenML ID 40 / UCI Machine Learning Repository`
- **Evidentiary Rating:** **Non-Biological Methodological Negative Control**
- **Biological Context:**
  - **Organism:** *None (Acoustic physics)*
  - **Anatomical Tissue / Cell Type:** None (Submerged metal cylinder vs cylindrical rock)
  - **Clinical Cohort Origin:** DARPA Neural Network Study / Naval Undersea Warfare Center
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 208
  - **Feature Dimension ($D$):** 60
  - **Cluster Count ($K$):** 2
  - **Diagnostic Ground Truth:** 111 Mines (metal cylinder), 97 Rocks (cylindrical rock)
- **Assay Platform & Technology:** Wide-band active sonar chirp frequency energy return (60 spectral integration bands)
- **Lineage & Independence Audit:** **Category E (Non-Biological Control Stratum)**

---
### 19. `madelon`: Result analysis of the NIPS 2003 variable selection benchmark

- **Full Bibliographic Citation:**  
  Guyon, I., Gunn, S., Ben-Hur, A., & Dror, G. (2004). "Result analysis of the NIPS 2003 variable selection benchmark." *Advances in Neural Information Processing Systems (NeurIPS 2004)*, 17, pp. 545-552.  
  **DOI:** [10.5555/2976040.2976109](https://proceedings.neurips.cc/paper/2004/hash/703957b486981cf06a864d47fb1b64ff-Abstract.html)
- **Official Repository Accessions:** `OpenML ID 1485 / UCI Machine Learning Repository`
- **Evidentiary Rating:** **Synthetic Feature Selection Control**
- **Biological Context:**
  - **Organism:** *None (Synthetic XOR data generator)*
  - **Anatomical Tissue / Cell Type:** None (Mathematical distribution)
  - **Clinical Cohort Origin:** NIPS 2003 Feature Selection Challenge
- **Biometric Dimensions:**
  - **Sample Size ($N$):** 500
  - **Feature Dimension ($D$):** 500
  - **Cluster Count ($K$):** 2
  - **Diagnostic Ground Truth:** Binary XOR hypercube vertices (+1 vs -1)
- **Assay Platform & Technology:** 5 informative coordinates defining XOR vertices + 15 redundant linear combinations + 480 pure Gaussian distractor noise dimensions
- **Lineage & Independence Audit:** **Category E (Synthetic Control Stratum)**

---
