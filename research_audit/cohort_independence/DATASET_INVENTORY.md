# Research Audit: Master Dataset Inventory & Provenance Catalog

**Document Reference:** `research_audit/cohort_independence/DATASET_INVENTORY.md`  
**Related File:** `results/cohort_independence/dataset_inventory.csv`  
**Audit Date:** 2026-11-01  
**Auditor:** Senior Computational Biologist & Biomedical Data Curator  

---

## 1. Executive Overview of the Benchmark Suite

A thorough inspection of the repository identified a total of **29 datasets** across all active and legacy benchmarks: 
- **13 Core Paper Benchmarks** (`data/registry.yaml`, `configs/datasets.yaml`): 6 bulk oncology microarrays, 1 single-cell transcriptomics dataset, and 6 diverse non-genomic/control benchmarks.
- **9 Additional Audit Benchmarks** (`experiments/audit_controls/src/e1_extended_benchmarks.py`): The legacy 21-dataset audit suite.
- **6 Expanded Biological Oncology Cohorts** (`experiments/exp6_cohort_expansion/`): DLBCL, Breast (van 't Veer), Su2001, Novartis, GCM, and Endometrium.

---

## 2. Master Dataset Inventory Table

| Internal Key | Intended Dataset Name | Primary Citation | Accession / Source | Tissue / Modality | $N$ | $D$ | $K$ | Benchmark Role | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| `cns` | Central Nervous System Embryonal Tumors | Pomeroy et al. Nature 415, 436-442 (2002) | OpenML 45086 / tumors_C (OpenML 1107) | Central nervous system embryon | 60 | 7129 | Binary: 39 surv | Core Benchmark (Paper 1 & Audit) | Yes (Reference CNS Cohort |
| `colon` | Colon Cancer Gene Expression | Alon et al. PNAS 96(12), 6745-6750 (1999) | OpenML 45087 | Colon tissue (tumor biopsies v | 62 | 2000 | Binary: 40 tumo | Core Benchmark (Paper 1 & Audit) | Yes (Reference Colon Coho |
| `leukemia` | Golub Acute Leukemia (ALL vs AML) | Golub et al. Science 286(5439), 531-537 (1999) | OpenML 1104 | Bone marrow / peripheral blood | 72 | 7129 | Binary: 47 ALL  | Core Benchmark (Paper 1 & Audit) | Yes (Reference Leukemia C |
| `ovarian` | Ovarian Cancer Proteomics (SELDI-TOF) | Petricoin et al. Lancet 359(9306), 572-577 (2002) | OpenML 45098 / NCI-FDA Clinical Proteomics | Serum mass spectrometry spectr | 253 | 15154 | Binary: 91 norm | Core Benchmark (Paper 1 & Audit) | Yes (Serum Proteomics; In |
| `prostate` | Prostate Cancer Microarray | Singh et al. Cancer Cell 1(2), 203-209 (2002) | OpenML 45099 | Prostate tissue (radical prost | 102 | 12600 | Binary: 50 norm | Core Benchmark (Paper 1 & Audit) | Yes (Reference Prostate C |
| `srbct` | Small Round Blue Cell Tumors of Childhood | Khan et al. Nat Med 7(6), 673-679 (2001) | OpenML 45101 | Pediatric small round cell tum | 83 | 2308 | 4 Classes: 29 E | Core Benchmark (Paper 1 & Audit) | Yes (Reference SRBCT Coho |
| `zheng68k` | 10x PBMC 68k (Reduced 700 cells) | Zheng et al. Nat Commun 8, 14049 (2017) | 10x Genomics Fresh 68k PBMCs (Donor A) | Peripheral blood mononuclear c | 700 | 765 | 10 immune cell  | Core Benchmark (Paper 1 & Audit) | Yes (Single-Cell RNA-seq; |
| `sonar` | Sonar Signals (Mines vs Rocks) | Gorman RP, Sejnowski TJ. Neural Networks 1(1), 75-89 (1988) | OpenML 40 / UCI 151 | None (Acoustic sonar chirp ret | 208 | 60 | Binary: 111 Min | Core Benchmark Control (Non-Genomic) | NON-BIOLOGICAL CONTROL (N |
| `madelon` | Madelon Synthetic Feature Selection Benchmark | Guyon et al. NIPS 2003 Workshop on Feature Extraction (2003) | OpenML 1485 | None (Synthetic XOR clusters + | 500 | 500 | Binary: 250 vs  | Core Benchmark Control (Synthetic) | SYNTHETIC CONTROL (Not an |
| `isolet` | Isolet Spoken Letter Recognition | Fanty M, Cole R. NIPS 1990 (1991) | OpenML 300 / UCI 54 | None (Acoustic audio features  | 7797 | 617 | 26 Classes (Let | Core Benchmark Control (Audio) | NON-BIOLOGICAL CONTROL (N |
| `newsgroups20` | 20 Newsgroups Usenet Postings | Lang K. ICML 1995, 331-339 (1995) | CMU 20 Newsgroups corpus | None (Usenet newsgroup text po | 18846 | 10000 | 20 Classes (20  | Core Benchmark Control (Text) | NON-BIOLOGICAL CONTROL (N |
| `indian_pines` | Indian Pines AVIRIS Hyperspectral Flightline | Purcell et al. NASA Technical Memorandum (1992) | Purdue LARS / UPV/EHU AVIRIS repository | None (Hyperspectral optical ra | 10249 | 200 | 16 Classes (Cro | Core Benchmark Control (Hyperspectral) | NON-BIOLOGICAL CONTROL (N |
| `yale_b` | Extended Yale Face Database B | Georghiades AS, Belhumeur PN, Kriegman DJ. IEEE TPAMI 23(6), 643-660 (2001) | UCSD Center for Visual Computing | None (Facial photographic pixe | 2414 | 1024 | 38 Classes (38  | Core Benchmark Control (Vision) | NON-BIOLOGICAL CONTROL (N |
| `glioma` | Glioma (Mislabeled in script: OpenML 1107) | Pomeroy et al. Nature 2002 (Actually CNS tumors_C!) | OpenML 1107 (tumors_C) | CNS embryonal tissue | 60 | 7129 | Binary: 39 vs 2 | Audit Controls (e1_extended_benchmarks) | NO: 100% BIT-FOR-BIT DUPL |
| `lung_cancer` | Lung Cancer (Mislabeled in script: OpenML 1106) | Ramaswamy et al. PNAS 98(26), 15149-15154 (2001) | OpenML 1106 (GCM) | 14 human carcinoma types (mult | 190 | 16063 | 14 Classes: Bre | Audit Controls (e1_extended_benchmarks) | Yes (Independent Study, b |
| `breast_cancer_genomic` | Breast Cancer Genomic (Mislabeled in script: OpenML 1120) | Bock RK et al. (Major Atmospheric Gamma Imaging Cherenkov Telescope) | OpenML 1120 (MagicTelescope) | None (Gamma-ray Cherenkov atmo | 19020 | 10 | Binary: 12332 G | Audit Controls (e1_extended_benchmarks) | NO: MISLABELED ASTROPHYSI |
| `lymphoma` | Lymphoma (Mislabeled in script: OpenML 1157) | Risinger et al. / Armstrong et al. (Actually AP_Endometrium_Kidney!) | OpenML 1157 (AP_Endometrium_Kidney) | Endometrium vs Kidney adenocar | 321 | 10935 | Binary: Endomet | Audit Controls (e1_extended_benchmarks) | Yes (Independent Study, b |
| `usps` | USPS Digits (Mislabeled in script: OpenML 554) | LeCun et al. (Actually MNIST 784!) | OpenML 554 (mnist_784) | None (Handwritten digit graysc | 2000 | 784 | 10 Classes (Dig | Audit Controls (e1_extended_benchmarks) | NON-BIOLOGICAL CONTROL (M |
| `waveform` | Waveform Database Generator (version 1) | Breiman et al. Classification and Regression Trees (1984) | OpenML 60 (waveform-5000) | None (Synthetic triangular wav | 2000 | 40 | 3 Classes (Wave | Audit Controls (e1_extended_benchmarks) | SYNTHETIC CONTROL (Not an |
| `arrhythmia` | Arrhythmia Database (Cardiac ECG) | Guvenir et al. Computers in Cardiology 1997, 433-436 (1997) | OpenML 5 / UCI 5 | Cardiac electrophysiology (12- | 452 | 279 | 16 Classes (Nor | Audit Controls (e1_extended_benchmarks) | Yes (Clinical Cardiac Ele |
| `har` | Human Activity Recognition Using Smartphones | Anguita et al. ESANN 2013 (2013) | OpenML 1478 / UCI 240 | None (Smartphone inertial sens | 2000 | 561 | 6 Classes: Walk | Audit Controls (e1_extended_benchmarks) | NON-BIOLOGICAL CONTROL (I |
| `gisette` | Gisette (Mislabeled in script: OpenML 41027) | Guyon et al. NIPS 2003 (Mislabeled: actually Jungle Chess!) | OpenML 41027 (jungle_chess_2pcs_raw_endgame_complete) | None (Board game piece positio | 1000 | 6 | 3 Classes: Win, | Audit Controls (e1_extended_benchmarks) | NO: MISLABELED GAME DATAS |
| `dlbcl` | Diffuse Large B-Cell Lymphoma vs Follicular | Shipp et al. Nature Medicine 8(1), 68-74 (2002) | OpenML 45088 / DLBCL.arff.gz | Lymphoid tissue biopsies | 77 | 5469 | Binary: 58 DLBC | Expanded Oncology Benchmark (EXP6) | Yes (Independent Lymphoma |
| `breast` | Breast Cancer 5-Year Metastasis Prognosis | van 't Veer et al. Nature 415, 530-536 (2002) | OpenML 45085 / Breast.arff.gz | Primary breast carcinoma tumor | 97 | 24481 | Binary: 51 dise | Expanded Oncology Benchmark (EXP6) | Yes (Primary Dutch Breast |
| `su2001` | 11 Human Solid Tumor Types | Su et al. Cancer Res 61(19), 7388-7393 (2001) | OpenML 45084 / 11_Tumors.arff.gz | 11 human solid tumor tissues ( | 174 | 12533 | 11 Classes: Bla | Expanded Oncology Benchmark (EXP6) | Yes (Independent Multicen |
| `novartis` | 9 Human Carcinoma Subtypes | Su et al. PNAS 99(7), 4465-4470 (2002) | OpenML 45083 / 9_Tumors.arff.gz | 9 human tumor tissue categorie | 60 | 5726 | 9 Classes | Expanded Oncology Benchmark (EXP6) | Yes (Independent Study, p |
| `gcm` | Global Cancer Map (GCM 14 Tumors) | Ramaswamy et al. PNAS 98(26), 15149-15154 (2001) | OpenML 1106 / GCM.arff.gz | 14 human carcinoma subtypes | 190 | 16063 | 14 Classes: Bla | Expanded Oncology Benchmark (EXP6) | CAUTION: Assembled from m |
| `endometrium` | Endometrium vs Kidney Adenocarcinoma | Risinger et al. Cancer Res 63(1), 6-11 (2003) / Armstrong et al. | OpenML 1157 / AP_Endometrium_Kidney.arff.gz | Endometrial and Renal tissue | 321 | 10936 | Binary: Endomet | Expanded Oncology Benchmark (EXP6) | Yes (Independent Clinical |
| `gli` | Glioma High-Grade vs Low-Grade | Nutt et al. Cancer Res 63(7), 1602-1607 (2003) | OpenML 45089 / GLI.arff.gz | Human brain glioma tumor tissu | 85 | 22283 | Binary (High-gr | Expanded Oncology Benchmark | Yes (True Nutt 2003 Gliom |

---

## 3. Immediate Critical Findings from the Inventory Audit

### 3.1 Non-Biological Benchmark Inflation
Of the 21 datasets in the extended audit (`e1_extended_benchmarks.csv`):
- **Only 10 datasets are biological** (CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT, Zheng68k, Lung Cancer/GCM, Lymphoma/Endometrium, and Arrhythmia).
- **11 datasets are non-biological controls** (Sonar [acoustic], Madelon [synthetic], Isolet [audio speech], USPS/MNIST [handwritten digits], Waveform [synthetic], HAR [smartphone sensors], Gisette/Jungle Chess [board game], Newsgroups20 [Usenet text], Indian Pines [hyperspectral agriculture], and Yale B [facial photographs]).

> [!IMPORTANT]
> Claiming that ICC-Clustering was evaluated across '21 real-world biological cohorts' is scientifically invalid. Exactly 11 of the 21 datasets measure non-biological, synthetic, or physical sensor processes.

### 3.2 Severe OpenML Identifier Misattributions in Legacy Code
Forensic inspection of `experiments/audit_controls/src/e1_extended_benchmarks.py` revealed severe OpenML dataset misallocations:
1. **`glioma` vs. `cns` (100% Duplicate):** The script specified OpenML ID 1107 (`tumors_C`) for `glioma`. OpenML ID 1107 is actually the Pomeroy et al. 2002 CNS embryonal tumors dataset ($N=60, D=7129$). Both `cns.npz` and `glioma.npz` share the **exact same SHA-256 checksum** (`0e449bf...`). The real Glioma dataset (Nutt et al. 2003, $N=85, D=22283$) is OpenML ID 45089.
2. **`breast_cancer_genomic` (Astrophysics Cherenkov Telescope!):** The script mapped OpenML ID 1120 as `breast_cancer_genomic`. OpenML ID 1120 is actually **`MagicTelescope`** ($N=19020, D=10$), an astrophysics simulation of Cherenkov gamma-ray showers. It has zero biological origin.
3. **`lung_cancer` (Actually Multi-Tissue GCM):** OpenML ID 1106 is named `GCM` ($N=190, D=16063, K=14$), which is the Ramaswamy 14-tumor Global Cancer Map, not an isolated lung cancer cohort.
4. **`lymphoma` (Actually Endometrium vs Kidney):** OpenML ID 1157 is named `AP_Endometrium_Kidney` ($N=321, D=10935, K=2$), which is an endometrial and renal adenocarcinoma benchmark, not lymphoma.
5. **`gisette` (Actually Jungle Chess Game):** OpenML ID 41027 is `jungle_chess_2pcs_raw_endgame_complete` ($N=1000, D=6, K=3$), not the NIPS 2003 Gisette handwriting benchmark ($D=5000$).
6. **`usps` (Actually MNIST):** OpenML ID 554 is `mnist_784` ($N=2000, D=784$), not USPS digits ($16 \times 16 = 256$).

These misattributions explain why previous audits observed identical CNS and Glioma scores, and why the reported feature dimensionality fluctuated wildly across documentation versions.