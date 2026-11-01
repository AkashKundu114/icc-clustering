# Pre-Registration Record: DAMI Scientific Revision Protocol (v1.0)

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Working Branch:** `research/dami-revision`  
**Base Commit SHA:** `ab6be28ea5ded77ef5deb5f8cfab0a462c12c88f`  
**Date of Record:** November 1, 2026  
**Proposed Git Tag:** `prereg-dami-v1` (Pending Human Authorization)  

---

## 1. Administrative Information

- **Study Title:** Empirical Analysis of Stability-Accuracy Discordance and Bimodality-Gated Consensus Clustering in High-Dimensional Biomedical Cohorts
- **Lead Investigator:** Akash Kundu
- **Affiliation:** Indian Institute of Engineering Science and Technology (IIEST), Shibpur
- **Pre-Registration Status:** **DRAFT SPECIFICATION — PRE-REGISTERED PENDING USER APPROVAL (GATE G1)**

---

## 2. Study Objectives and Research Questions

1. **Question 1 (Discordance):** Does subsample clustering stability reliably indicate clustering accuracy (ARI) in high-dimensional biomedical cohorts ($D/N > 20$), or does distance concentration decouple stability from ground truth?
2. **Question 2 (Confounding):** Under what conditions do unsupervised consensus clustering algorithms converge stably to technical artifacts (e.g. sequencing depth, library size) rather than true biological subtypes?
3. **Question 3 (Component Attribution):** Which architectural components of Gated Anchor Consensus (BGSS feature gating, bipartite anchor graph compression, transfer-cut spectral optimization) provide measurable empirical improvements, and which are empirical nulls?
4. **Question 4 (Generalizability):** Do the empirical findings replicate across independent confirmatory biological cohorts and reasonable perturbations?

---

## 3. Pre-Specified Confirmatory Hypotheses

### Hypothesis H1 (Stability–Accuracy Discordance)
- In high-dimensional cohorts ($D/N > 20$), clustering stability and accuracy are decoupled. The cohort-level paired stability-accuracy gap $\Delta_{\text{gap}} = \text{Stab} - \text{ARI}$ is significantly greater than zero across non-degenerate partitions ($p < 0.05$).

### Hypothesis H2 (Conditional Utility of BGSS)
- Bimodality-Gated Subspace Selection (BGSS) provides a statistically significant improvement in median ARI over matched random feature gating under bipartite consensus ($\Delta > 0, p_{\text{adj}} < 0.05$ under Holm-Bonferroni correction). Under dense consensus, the effect size is significantly attenuated.

### Hypothesis H3 (Core Determinacy Certification Null)
- Proposition 2 sample determinacy core anchor certification yields an empirical accuracy difference indistinguishable from uniform random landmark anchors ($|\Delta_{\text{ARI}}| \le 0.02, p > 0.10$).

---

## 4. Confirmatory Dataset Eligibility & Quarantining Rules

### Inclusion Criteria:
1. Human primary clinical specimens (cancer tissue or biopsy).
2. Bulk transcriptomic expression profiling (microarray or bulk RNA-seq).
3. Sample count $N \ge 40$, feature count $D \ge 1{,}000$, and ratio $D/N > 20$.
4. Validated, non-circular biological ground truth (molecular subtype, histological class, or lineage).
5. Clean, publicly accessible repository accession (GEO, ArrayExpress, or TCGA).

### Explicit Exclusions:
1. Clinical outcomes (overall survival, disease-free survival, therapy response) are strictly excluded from serving as ground-truth cluster labels.
2. Cell-line, single-cell RNA-seq, and non-human datasets are excluded from the primary benchmark.
3. Candidate datasets with patient overlap or duplicate aliquot derivation from existing cohorts are quarantined.

### Label Vaulting:
Ground-truth label vectors are fingerprinted with SHA-256 digests and sealed during preprocessing, feature selection, anchor sampling, and clustering. Labels are unsealed strictly for final performance scoring.

---

## 5. Statistical Analysis & Multiplicity Control Plan

1. **Statistical Unit:** The biological cohort ($N$) is the independent unit of inference.
2. **Within-Cohort Summary:** Median ARI across 30 prespecified pseudo-random seeds ($S=30$).
3. **Cross-Cohort Aggregation:** Both mean and median cross-cohort effects reported with $95\%$ non-parametric bootstrap confidence intervals (10,000 resamples).
4. **Comparison Family:** A pre-specified family of 8 primary method comparisons against Full ICC-v2.
5. **Multiplicity Control:** Holm-Bonferroni step-down procedure applied across the full 8-method family, controlling family-wise error rate at $\alpha = 0.05$. Both uncorrected $p$ and adjusted $p_{\text{adj}}$ values must be disclosed.

---

## 6. Pre-Registration Freeze Protocol

- This specification is committed to `research_audit/dami_revision/PREREGISTRATION.md`.
- No confirmatory experiments shall be launched until the user explicitly reviews and approves Gate G1.
- Upon user approval, Git tag `prereg-dami-v1` will be generated and signed on `research/dami-revision`.
