# Research Audit 10: Expanded Cohort Evaluation Protocol & Stratification Guidelines

**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Document Reference:** `AUDIT-10-COHORT-PROTOCOL`  
**Date:** 2026-10-31  

---

## 1. Ontological Stratification Framework

Clustering algorithms behave differently depending on the underlying data manifold. Pooling single-cell dropouts, continuous gene expression, and text document term vectors into a single aggregate obscures algorithm mechanics. 

The expanded benchmark enforces four strictly separated strata:

```
                                  BENCHMARK STRATA
 ┌─────────────────────────┬─────────────────────────┬─────────────────────────┬─────────────────────────┐
 │ Stratum 1: Bulk Oncology│ Stratum 2: Single-Cell  │ Stratum 3: Dense Control│ Stratum 4: Non-Genomic  │
 ├─────────────────────────┼─────────────────────────┼─────────────────────────┼─────────────────────────┤
 │ • 12 Microarray cohorts │ • 6 scRNA-seq cohorts   │ • Sonar, Madelon        │ • Isolet, Newsgroups20  │
 │ • D/N in [27, 301]      │ • N in [466, 8569]      │ • Dense continuous      │ • Indian Pines, Yale-B  │
 │ • Continuous manifold   │ • High dropout (>80%)   │ • Low/medium D          │ • Multiclass large-K    │
 │ • Additive noise        │ • Negative Binomial     │ • Positive/negative     │ • Benchmark bounds      │
 └─────────────────────────┴─────────────────────────┴─────────────────────────┴─────────────────────────┘
```

---

## 2. Standardized Preprocessing Protocols

### 2.1 Stratum 1: Bulk Oncology Microarrays ($D \gg N$)
1. **Missing Value Imputation:** If any coordinate contains NaN values, impute using the coordinate-wise mean $\bar{x}_j$:
   $$\hat{x}_{ij} = \frac{1}{|I_{\text{obs}, j}|} \sum_{i' \in I_{\text{obs}, j}} x_{i'j}$$
2. **Log Transformation:** Applied only if input expression represents raw non-negative fluorescence intensities with dynamic range $> 10^3$:
   $$x_{ij}' = \log_{10}(\max(x_{ij}, 1.0))$$
3. **Feature-Wise Standardization:** Each dimension is centered to zero mean and scaled to unit variance:
   $$\tilde{x}_{ij} = \frac{x_{ij}' - \hat{\mu}_j}{\hat{\sigma}_j + \epsilon}, \quad \epsilon = 10^{-12}$$
4. **Prohibition of Supervised Filtering:** Under no circumstances may class labels be used to select genes (e.g. via $t$-test or ANOVA). Feature selection must be purely unsupervised.

### 2.2 Stratum 2: Single-Cell RNA-seq (scRNA-seq)
1. **Quality Control & Cell Filtering:** Exclude low-quality cells with $<200$ detected genes or $>10\%$ mitochondrial expression.
2. **Total-Count Library Size Normalization:** Normalize read counts per cell to a target sum of $10{,}000$ (CP10K):
   $$x_{ij}' = \frac{x_{ij}}{\sum_{l=1}^D x_{il}} \times 10{,}000$$
3. **Variance-Stabilizing Log Transform:**
   $$\tilde{x}_{ij} = \ln(1 + x_{ij}')$$
4. **Highly Variable Gene (HVG) Selection:** To manage scRNA-seq feature spaces without violating the continuous manifold assumption, select the top $D_{\text{HVG}} = 2{,}000$ genes using the Seurat v3 dispersion method (Stuart et al., Cell 2019):
   - Fit a loess regression of $\log_{10}(\sigma_j^2 / \mu_j)$ against $\log_{10}(\mu_j)$.
   - Standardize feature variances using the loess model expectation.
   - Retain the top 2,000 features with highest normalized variance.

---

## 3. Evaluation Split & Seed Schedules

- **Replicate Schedule:**
  - High-$D$ bulk cohorts: 30 independent canonical random seeds ($\mathcal{S}_{\text{high}} = \{42, \dots, 71\}$).
  - Large $N$ single-cell cohorts ($N > 2{,}000$): 10 independent canonical random seeds ($\mathcal{S}_{\text{sc}} = \{42, \dots, 51\}$) to maintain compute feasibility.
- **Reporting Metrics:**
  - Adjusted Rand Index (ARI) relative to reference labels.
  - Normalized Mutual Information (NMI, arithmetic average formulation).
  - Adjusted Mutual Information (AMI).
  - Fowlkes-Mallows Index (FM).
  - Wall-clock runtime (seconds) and peak memory (RSS MB).
