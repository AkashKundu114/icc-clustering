# Assay-Specific Preprocessing & Feature Isolation Audit

**Protocol:** `research_audit/cohort_discovery/COHORT_DISCOVERY_ELIGIBILITY_SPEC.md` Section 5  
**Audit Scope:** Feature normalization, missingness handling, and matrix orientation across all approved cohorts  
**Mandate:** Zero Label Leakage; Complete Isolation of Feature Selection from Ground-Truth Labels  

---

## 1. Matrix Orientation & Mathematical Contract

At the public loader boundary for Inductive Consensus Clustering (ICC):
$$\mathbf{X} \in \mathbb{R}^{N \times D}, \quad \mathbf{y} \in \mathcal{Y}^N$$
- **Axis 0 (Rows):** Biological samples ($N$). Original sample IDs (GSM, TCGA barcode, patient ID) are strictly preserved in metadata.
- **Axis 1 (Columns):** Measured biological features ($D$, probes or gene symbols).
- No transpose operations occur silently at runtime.

---

## 2. Microarray Assay Preprocessing Protocol

For all bulk microarray cohorts (`GSE62254`, `GSE39582`, `GSE31210`, `GSE13159`, `GSE10846`, `GSE42568`, `GSE19188`, `GSE21653`, `GSE32894`, `GSE14333`, `GSE41271`, `GSE88770`, `E-MTAB-1980`):

1. **Source Representation:**
   - Uniform extraction from official NCBI GEO / ArrayExpress Series Matrix files.
   - Intensity values are $\log_2$-transformed if raw MAS5/RMA values exceed 100.
2. **Missing Feature & Low Variance Filtering:**
   - Features with all NaN or zero variance across the cohort are purged.
   - Prespecified missingness threshold: any probe with $> 10\%$ missing values is excluded; remaining missing values are imputed using column-wise feature median fitted strictly on the feature matrix without label references.
3. **Probe-to-Gene Mapping (Optional Dimension Reduction):**
   - For genome-wide analyses, probes mapping to the same Entrez Gene are collapsed using the median expression per gene.
   - In the benchmark matrix, the full native high-dimensional feature space ($D > 20{,}000$) is preserved to test high-$D$ consensus stability.
4. **Standardization:**
   - Each feature is standardized independently:
     $$x_{ij}' = \frac{x_{ij} - \mu_j}{\sigma_j}$$
   - Zero label information enters $\mu_j$ or $\sigma_j$.

---

## 3. Bulk RNA-seq Stratum Preprocessing Protocol

For bulk RNA-seq cohorts (`TCGA-BRCA`, `TCGA-LUAD`, `TCGA-COAD`, `TCGA-GBM`, `GSE49710`):

1. **Quantification Level:** Gene-level unnormalized counts (STAR-Counts) or RSEM TPM.
2. **Transformation:**
   - Non-linear abundance stabilization via $\log_2(\text{TPM} + 1)$ or Variance Stabilizing Transformation (VST).
   - Raw sequencing counts are **never** directly standardized with z-scores to avoid extreme variance distortion from unexpressed genes.
3. **Low-Abundance Filtering:**
   - Genes with $< 10$ counts in $> 80\%$ of samples are filtered out prior to clustering.

---

## 4. Single-Cell & Pseudobulk Stratum Preprocessing Protocol

For single-cell transcriptomics (`Zheng68k`, `GSE352702`):
- Single-cell assays must not pool thousands of cells from 1–4 donors as independent biological cohorts.
- Where patient-level tasks are performed, single-cell profiles must be aggregated to pseudobulk profiles by donor before cross-cohort meta-analysis.
- High-variability gene selection (HVG) uses Seurat/Scanpy dispersion criteria calculated purely within the training fold.

---

## 5. Non-Negotiable Leakage Protections

1. **No Supervised Differential Expression (DE):** Features are never ranked, filtered, or selected using student's t-test, ANOVA, or limma against external labels $y$.
2. **No Outcome-Informed Filtering:** Survival times, hazard ratios, or therapy response never guide feature selection.
3. **No Cross-Cohort Merging:** Independent cohorts are preprocessed strictly in isolation. ComBat batch correction across disparate datasets is prohibited for the per-cohort benchmark.
