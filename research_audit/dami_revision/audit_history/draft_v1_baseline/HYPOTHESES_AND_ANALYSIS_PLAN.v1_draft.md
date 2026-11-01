# Gate G1: Confirmatory Hypotheses and Statistical Analysis Plan

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Protocol Version:** `v1.0-DAMI-PLAN`  
**Branch:** `research/dami-revision`  
**Status:** **PROPOSED PROTOCOL — PENDING HUMAN APPROVAL BEFORE GATE G1 FREEZE**  

---

## 1. Study Overview and Analytical Demarcation

This protocol establishes the confirmatory hypothesis testing framework, cohort eligibility rules, multiplicity control procedures, and experiment grid for the DAMI revision of `icc-clustering`.

### Transparent Analytical Separation:
- **Exploratory Set (Pass F / Baseline):** The original 6 biomedical cohorts (`colon`, `leukemia`, `breast`, `prostate`, `srbct`, `cns`) have informed initial hypothesis formulation and post-hoc criteria (such as Rule i'). They are formally designated as **EXPLORATORY**.
- **Confirmatory Set (Expansion E4):** Only newly discovered, independently verified biological cohorts meeting all eligibility criteria and quarantined from initial development shall serve as the **CONFIRMATORY** testing cohort.
- **Sensitivity Set (Post-Hoc / Robustness):** Threshold grid scans, preprocessing ablations (E3), and leave-one-cohort-out checks shall be reported as **SENSITIVITY ANALYSES**.

---

## 2. Formal Hypotheses & Decision Rules

### Hypothesis 1 (H1: Stability–Accuracy Discordance in High Dimensions)
- **Null Hypothesis ($H_{0,1}$):** In high-dimensional cohorts ($D/N > 20$), subsampling clustering stability correlates positively with empirical clustering accuracy (ARI) across candidate algorithms:
  $$\rho(\text{Stability}, \text{ARI}) \ge 0.50$$
- **Alternative Hypothesis ($H_{1,1}$):** Subsample stability is decoupled from clustering accuracy ($\rho < 0.30$ or persistent discordance $\text{Stab} \ge 0.50, \text{ARI} \le 0.05$ across non-degenerate partitions).
- **Estimand:** Cohort-level paired stability-accuracy gap $\Delta_{\text{gap}} = \text{Stab} - \text{ARI}$.
- **Statistical Unit:** Biological cohort ($N$).
- **Test:** One-sample Wilcoxon signed-rank test on cohort-level gaps against zero, accompanied by leave-one-cohort-out sensitivity checks.

### Hypothesis 2 (H2: Conditional Advantage of Bimodality Gating)
- **Null Hypothesis ($H_{0,2}$):** In high-dimensional biomedical cohorts, Bimodality-Gated Subspace Selection (BGSS) under bipartite consensus yields no improvement over matched random feature gating:
  $$\Delta_{\text{BGSS}} = \text{ARI}_{\text{BGSS}} - \text{ARI}_{\text{Random}} \le 0$$
- **Alternative Hypothesis ($H_{1,2}$):** BGSS significantly improves ARI over matched random gating ($\Delta_{\text{BGSS}} > 0$).
- **Estimand:** Paired cohort difference in median ARI across 30 seeds.
- **Decision Rule:** One-sided paired Wilcoxon signed-rank test with family-wise error control at $\alpha = 0.05$.

### Hypothesis 3 (H3: Core Determinacy Certification Empirical Null)
- **Null Hypothesis ($H_{0,3}$):** Certified core anchors (Proposition 2) provide no empirical accuracy improvement over uniform random landmark anchors in bipartite consensus:
  $$|\text{ARI}_{\text{Core}} - \text{ARI}_{\text{RandomAnchors}}| \le 0.02$$
- **Alternative Hypothesis ($H_{1,3}$):** Certified core anchors confer a non-trivial accuracy gain ($|\Delta| > 0.02$).
- **Estimand:** Paired cohort difference between Full ICC-v2 and Knockout 4 (Random Landmarks).
- **Decision Rule:** Two-sided Wilcoxon signed-rank test; failure to reject at $\alpha = 0.05$ confirms the empirical null.

---

## 3. Statistical Analysis Plan & Multiplicity Control

### 3.1 Primary Inferential Units
- The **biological cohort** is the primary independent unit ($N$).
- Seeds ($S=30$) provide measurement precision within each cohort. Method performance on a given cohort is aggregated as the **median ARI** across the 30 seeds.
- Cross-cohort summaries report both **mean** and **median** paired differences, with non-parametric bootstrap uncertainty intervals (10,000 resamples).

### 3.2 Pre-Specified Comparison Family & Multiplicity Correction
To prevent selective reporting, the confirmatory evaluation defines a single, locked comparison family of 8 primary method comparisons against Full ICC-v2:
1. Full ICC-v2 vs. Ambient Standard Consensus (`StdCons_All`)
2. Full ICC-v2 vs. Ambient K-Means (`K-Means_All`)
3. Full ICC-v2 vs. Variance-Filtered K-Means (`K-Means_VarFilt`)
4. Full ICC-v2 vs. PCA K-Means (`K-Means_PCA`)
5. Full ICC-v2 vs. Laplacian Score K-Means (`K-Means_LapScore`)
6. Full ICC-v2 vs. Sparse K-Means (`SparseKMeans`)
7. Full ICC-v2 vs. Anchor Spectral Baseline (`FCAG`)
8. Full ICC-v2 vs. Multi-View Proxy (`FastMVC-Surrogate`)

**Multiplicity Procedure:**  
Holm-Bonferroni step-down procedure applied to the full 8-comparison family, controlling the Family-Wise Error Rate (FWER) at $\alpha = 0.05$. Both uncorrected $p$-values and adjusted $p_{\text{adj}}$-values will be explicitly reported in manuscript tables.

---

## 4. Cohort Expansion & Independence Criteria (E4)

### 4.1 Eligibility Criteria (per `COHORT_DISCOVERY_ELIGIBILITY_SPEC.md`):
1. **Human Origin:** Samples must be derived from human primary clinical specimens or biopsies.
2. **Assay Homogeneity:** Primary benchmark restricted to bulk transcriptomic assays (microarray or bulk RNA-seq). Single-cell, proteomics, and cell-line matrices shall not be mixed into the primary benchmark.
3. **Dimensionality:** Sample size $N \ge 40$, feature count $D \ge 1{,}000$, and ratio $D/N > 20$.
4. **Biological Ground Truth:** Discrete, curated molecular subtypes (e.g. PAM50 breast subtypes, ALL vs. AML leukemia lineages, histological tumor classes). **Clinical survival, relapse, or treatment response shall NEVER be used as cluster ground truth.**
5. **No Data Leakage:** Labels are sealed in a secure checksum vault and accessed ONLY after final cluster predictions are frozen and fingerprinted.

### 4.2 Cross-Study Independence Verification:
- An overlap graph (`overlap_graph.graphml`) will resolve patient-level overlap, duplicate aliquots, and cross-study re-accessions.
- Candidates with suspected or unresolved donor overlap will be quarantined and excluded from confirmatory tallies.

---

## 5. Experiment Grid (E1 through E8)

| Exp ID | Title | Objective | Primary Artifact Output |
| :--- | :--- | :--- | :--- |
| **E1** | All-Cell & Threshold Sensitivity | Evaluate stability-accuracy relationship unconditionally and across non-degeneracy thresholds. | `results/exp1_sensitivity/` |
| **E2** | Unconditional Estimands & Cohort Inference | Recompute all primary estimands using all cells, reporting median alongside mean. | `results/exp2_unconditional/` |
| **E3** | Preprocessing Ablations | Evaluate raw, log-transformed, standardized, and quantile-normalized variants without external labels. | `results/exp3_preprocessing/` |
| **E4** | Independent Cohort Expansion | Download, audit, and evaluate eligible independent confirmatory cohorts. | `results/exp4_expansion/` |
| **E5** | Positive Controls & Planted Signal | Isotropic noise simulations with known ground truth evaluating breakdown thresholds. | `results/exp5_simulations/` |
| **E6** | Consensus Configuration Analysis | Disentangle gating, anchor budget, and consensus weighting in matched settings. | `results/exp6_consensus/` |
| **E7** | Partition Confounding & Technical Drivers | Correlate discovered clusters with PC1–PC3, sequencing depth, and batch annotations. | `results/exp7_confounding/` |
| **E8** | BGSS vs. Matched Random Gating | Paired cohort comparison with budget-matched random feature gating. | `results/exp8_bgss_vs_random/` |

---

## 6. Stop Conditions for Confirmatory Execution

Confirmatory execution shall immediately halt and request human intervention if:
1. A candidate cohort's patient independence or label provenance cannot be verified.
2. A required preprocessing operation requires external class labels.
3. Running an experiment would overwrite frozen baseline results in `results/passF/` or `results/results.json`.
4. Any comparison requires altering a pre-specified hypothesis post hoc.
