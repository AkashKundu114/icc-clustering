# Biological Label Ontology & Ground-Truth Validity Audit

**Protocol:** `research_audit/cohort_discovery/COHORT_DISCOVERY_ELIGIBILITY_SPEC.md` Section 4.2  
**Audit Scope:** 27 candidate oncology cohorts across GEO, ArrayExpress, TCGA/GDC, and OpenML  
**Status:** Frozen Pre-Experimental Label Classification  

---

## 1. Ground-Truth Classification Framework (B1–B6 Ontology)

In strict adherence to the cohort discovery specification, every external target label is classified prior to any unsupervised clustering evaluation:

| Category | Definition | Scientific Role | Admissibility in Confirmatory Clustering |
| :--- | :--- | :--- | :--- |
| **B1** | Biological subtype, histological lineage, or discrete tumor subclassification | Primary unsupervised cluster ground truth | **Admissible for Primary Benchmark (Tier A)** |
| **B2** | Disease vs non-disease, or primary tumor vs adjacent normal tissue | Diagnostic contrast; macroscopic tissue separation | **Segregated to Tier B Diagnostic Stratum** |
| **B3** | Single molecular alteration, mutation, or hormone receptor status (ER/PR/HER2) | Molecular phenotype; binary or oligogenic markers | **Segregated to Tier B Receptor Stratum** |
| **B4** | Clinical outcome endpoints (overall survival, relapse-free survival, therapy response) | Downstream clinical association only | **STRICTLY FORBIDDEN as Clustering Ground Truth** |
| **B5** | Technical batch, processing center, sequencing plate, or longitudinal timepoint | Experimental design covariates | **REJECTED as Ground Truth** |
| **B6** | Inferred algorithmic signatures (e.g. centroid PAM50 calls, CMS classifier outputs) | Secondary derivative classes; circularity check required | **Admissible only with Circularity Disclosure** |

---

## 2. Detailed Label Classification Across Audited Cohorts

### 2.1 Category B1: Confirmatory Biological Subtypes & Histological Lineages (Tier A)

1. **GSE62254 (ACRG Gastric Cancer)**:
   - **Label Name:** `acrg_subtype`
   - **Semantics:** 4 Asian Cancer Research Group consensus genomic subtypes: Microsatellite Instability (`MSI`, $n=68$), Epithelial-to-Mesenchymal Transition (`MSS/EMT`, $n=46$), TP53 active (`MSS/TP53+`, $n=79$), TP53 inactive (`MSS/TP53-`, $n=107$).
   - **Circularity Assessment:** None. Subtypes represent distinct molecular pathways independently validated across clinical cohorts.
   - **Verdict:** Certified B1 Ground Truth.

2. **GSE39582 (CIT Colorectal Cancer)**:
   - **Label Name:** `cit_subtype`
   - **Semantics:** 6 Cartes d'Identité des Tumeurs molecular subtypes: C1 (CIN normal-like, $n=101$), C2 (dMMR, $n=109$), C3 (KRAS mutant, $n=70$), C4 (stem-like, $n=98$), C5 (CIN Wnt up, $n=116$), C6 (CIN normal-like, $n=72$).
   - **Verdict:** Certified B1 Ground Truth.

3. **GSE31210 (Okayama Lung Adenocarcinoma)**:
   - **Label Name:** `oncogenic_driver_status`
   - **Semantics:** 4 Mutational driver lineages: `EGFR_mut` ($n=127$), `KRAS_mut` ($n=20$), `ALK_fusion` ($n=11$), `Triple_Neg` ($n=68$).
   - **Verdict:** Certified B1 Ground Truth (mutually exclusive oncogenic driver pathways).

4. **GSE13159 (MILE Leukemia Consortium)**:
   - **Label Name:** `leukemia_lineage_class`
   - **Semantics:** WHO-defined diagnostic leukemia lineages: AML ($n=542$), ALL ($n=750$), CLL ($n=448$), CML ($n=122$), MDS ($n=160$).
   - **Verdict:** Certified B1 Ground Truth.

5. **GSE10846 (Lenz DLBCL Lymphoma)**:
   - **Label Name:** `dlbcl_cell_of_origin`
   - **Semantics:** Cell-of-Origin subtypes: Germinal Center B-cell (`GCB`, $n=180$), Activated B-cell (`ABC`, $n=167$), Unclassified ($n=67$).
   - **Verdict:** Certified B1 Ground Truth.

6. **GSE19188 (Hou NSCLC Histology)**:
   - **Label Name:** `histological_lineage`
   - **Semantics:** 3 Major histological lineages: Adenocarcinoma ($n=45$), Squamous Cell Carcinoma ($n=27$), Large Cell Carcinoma ($n=19$).
   - **Verdict:** Certified B1 Ground Truth (Pathologically verified tumor lineage).

7. **GSE21653 (Sabatier Breast Cancer)**:
   - **Label Name:** `molecular_subtype`
   - **Semantics:** Intrinsic molecular subtypes: Luminal A ($n=90$), Luminal B ($n=58$), Basal ($n=55$), HER2 ($n=43$), Normal-like ($n=20$).
   - **Verdict:** Certified B1 Ground Truth.

8. **GSE32894 (Sjodahl Lund Bladder Taxonomy)**:
   - **Label Name:** `lund_molecular_subtype`
   - **Semantics:** 6 Lund University urothelial carcinoma subtypes: Urobasal A ($n=95$), Urobasal B ($n=41$), Genomically Unstable ($n=94$), Infiltrated ($n=49$), SCC-like ($n=12$), Keratinized ($n=17$).
   - **Verdict:** Certified B1 Ground Truth.

9. **GSE42568 (Clarke Breast Cancer)**:
   - **Label Name:** `breast_intrinsic_subtype`
   - **Semantics:** 5 Intrinsic molecular classes: Luminal A ($n=34$), Luminal B ($n=19$), Basal-like ($n=17$), HER2-enriched ($n=11$), Claudin-low ($n=23$).
   - **Verdict:** Certified B1 Ground Truth.

10. **GSE49710 (SEQC Neuroblastoma)**:
    - **Label Name:** `mycn_status_inss_stage`
    - **Semantics:** Biological cytogenetic / risk lineages: MYCN amplified ($n=92$) vs MYCN non-amplified high-risk ($n=84$) vs low-risk ($n=322$).
    - **Verdict:** Certified B1 Ground Truth.

11. **GSE14333 (Jorissen Colorectal Dukes Stages)**:
    - **Label Name:** `dukes_stage`
    - **Semantics:** Pathological tumor invasion staging: Dukes A ($n=34$), Dukes B ($n=102$), Dukes C ($n=94$), Dukes D ($n=60$).
    - **Verdict:** Certified B1 Ground Truth (Histopathological tumor depth).

12. **GSE41271 (Sato Lung Adenocarcinoma)**:
    - **Label Name:** `histologic_differentiation`
    - **Semantics:** Tumor differentiation grade: Well-differentiated ($n=82$), Moderately-differentiated ($n=124$), Poorly-differentiated ($n=69$).
    - **Verdict:** Certified B1 Ground Truth.

13. **GSE88770 (Michaut Invasive Lobular Carcinoma)**:
    - **Label Name:** `ilc_molecular_subtype`
    - **Semantics:** Immune-related vs Hormone-related vs Reactive ILC subtypes.
    - **Verdict:** Certified B1 Ground Truth.

14. **E-MTAB-1980 (Sato Renal ccRCC)**:
    - **Label Name:** `ccrcc_subtype`
    - **Semantics:** Clear cell renal cell carcinoma subtypes ccrcc1 ($n=54$) vs ccrcc2 ($n=47$).
    - **Verdict:** Certified B1 Ground Truth.

---

### 2.2 Category B2: Diagnostic Contrast (Tier B Stratum)

- **GSE14520 (Roessler HCC)**: Tumor ($n=225$) vs Non-tumorous liver tissue ($n=220$). Classified as **B2**. Must be evaluated in a separate diagnostic contrast stratum, not as evidence of unsupervised cancer subtyping.

---

### 2.3 Category B3: Molecular Alteration & Receptor Phenotypes (Tier B Stratum)

- **GSE25066 (Hatzis MDACC Breast)**: ER-positive ($n=323$) vs ER-negative ($n=185$). Classified as **B3**.
- **GSE2034 (Wang Erasmus Breast)**: ER-positive ($n=209$) vs ER-negative ($n=77$). Classified as **B3**.
- **GSE72094 (Schabath Lung)**: KRAS mutant ($n=128$) vs KRAS wild-type ($n=314$). Classified as **B3**.

---

### 2.4 Category B4: Clinical Outcomes (STRICTLY FORBIDDEN)

- **van 't Veer 2002 Breast Cancer (OpenML 45085)**: Target label is 5-year distant metastasis prognosis (51 disease-free vs 46 early metastasis). **Rejected for primary clustering ground truth.** Clinical survival and recurrence are multigenic, non-deterministic physiological outcomes influenced by therapy, surgery, and host immunity; they do not form compact cluster distributions in baseline expression space.
- **Pomeroy CNS (OpenML 1107 / 45086)**: The 39 survivor vs 21 treatment failure label is an outcome endpoint. In the primary paper, this is acknowledged as a legacy benchmark artifact.

---

### 2.5 Category B5 & B6: Design Covariates and Inferred Labels

- **GSE352244**: Baseline vs Relapse 1 vs Relapse 2. Classified as **B5** (longitudinal sampling, dependent repeated measures).
- **E-TABM-669**: In vitro differentiation timepoint. Classified as **B5**.
- **TCGA Pan-Cancer PAM50 / CMS Calls**: Classified as **B6**. Eligible for secondary analysis only with explicit disclosure of classifier provenance and circularity boundaries.
