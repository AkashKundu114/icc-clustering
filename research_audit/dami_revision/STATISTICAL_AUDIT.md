# Phase 0: Independent Statistical Audit Report

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Audit Persona:** Agent A4 — Independent Statistical Auditor  
**Date:** November 1, 2026  
**Dedicated Revision Branch:** `research/dami-revision`  

---

## 1. Executive Summary

This independent statistical audit reconstructs all descriptive summaries, hypothesis tests, confidence intervals, effect sizes, and ranking procedures directly from the raw baseline stores (`results/passF/`, `results/passE/`, `results/stability/`).

### Key Statistical Conclusions:
1. **Omnibus Equivalence on Multi-Domain Benchmarks:**  
   Across all 13 benchmark datasets (3,000 model fits across 10 methods), the Friedman omnibus test yields $\chi^2 = 9.59, p = 0.4768$ (reported in manuscript as $p = 0.40$). With critical difference $CD = 4.62$, differences among top methods (Standard Consensus rank 4.85, K-Means rank 5.00, DEC rank 5.08, ICC-v2 rank 5.23) are statistically indistinguishable.
2. **Two-Cohort Concentration of BGSS Effect:**  
   In the 6 high-dimensional biomedical cohorts, Full ICC-v2 achieves a mean ARI of $0.217 \pm 0.253$. However, the distribution is extremely skewed:
   - **Leukemia:** ARI = $0.5998 \pm 0.367$
   - **SRBCT:** ARI = $0.5456 \pm 0.102$
   - **Colon:** ARI = $0.0721 \pm 0.045$
   - **Ovarian:** ARI = $0.0499 \pm 0.035$
   - **CNS:** ARI = $0.0210 \pm 0.034$
   - **Prostate:** ARI = $0.0122 \pm 0.022$  
   The **cohort-level median ARI is only 0.061**. Excluding Leukemia and SRBCT, the 4-cohort mean ARI drops to **0.0388**, indistinguishable from ambient consensus ($0.037$).
3. **Paired Multiplicity Correction:**  
   The paired Wilcoxon signed-rank test comparing Full ICC-v2 against Ambient Bipartite consensus on $n=6$ cohorts yields $W = 20.0, p = 0.0312$ uncorrected. Under family-wise error rate control (Holm-Bonferroni across the 8 pre-specified baseline comparisons), the adjusted $p$-value exceeds $\alpha = 0.05$ ($p_{adj} = 0.249$). The manuscript must report both uncorrected and adjusted $p$-values.
4. **Knockout 4 Confirms Core Determinacy Null:**  
   Comparing certified core anchors against uniform random landmark anchors yields $\Delta = +0.0188$ ($p = 0.8438$, two-sided Wilcoxon signed-rank). Proposition 2 core determinacy certification has no measurable benefit over uniform random sampling.
5. **Pseudoreplication Audit:**  
   Treating repeated seeds ($S=30$) or multiple method cells on the same biological cohort as independent units constitutes pseudoreplication. The independent statistical unit is the **biological cohort** ($N=6$). All cross-cohort inferences must treat cohorts as clusters or paired units.

---

## 2. Re-computation of Primary Statistical Estimands

### 2.1 Multi-Domain Benchmark Omnibus Evaluation ($N=13$ Datasets)
- **Data Source:** `results/passF/benchmark_matrix_passF.csv`
- **Model Fits:** 3,000 fits (10 methods × 10 seeds × 30 draws)
- **Friedman Test Statistic:** $\chi^2 = 9.594, \text{df} = 10, p = 0.4768$
- **Nemenyi Critical Difference:**
  $$CD = q_{\alpha} \sqrt{\frac{K(K+1)}{6N}} = 3.164 \sqrt{\frac{10 \times 11}{6 \times 13}} = 3.75 \quad (\alpha=0.05)$$
- **Average Ranks Across 13 Datasets:**
  1. Standard Consensus: $4.85$
  2. K-Means: $5.00$
  3. DEC: $5.08$
  4. ICC-v2 (GAC): $5.23$ (overall rank $5.62$ in Pass E, $5.23$ in Pass F)
  5. Ward: $5.31$
  6. ICC-v1: $6.38$
  7. Spectral: $6.62$
  8. Core-Halo Consensus: $6.62$
  9. FCM: $6.77$
  10. FastMVC-Surrogate: $6.92$
  11. FCAG: $7.23$
- **Statistical Verdict:** Fully non-significant omnibus variation across all 13 multi-domain benchmarks.

---

### 2.2 Factorial Decomposition & Component Attribution ($N=6$ High-D Cohorts)
- **Data Source:** `results/passF/ablation_30seeds_passF.csv`
- **Reconstructed Subgroup Summaries (Mean $\pm$ SD, Median [IQR]):**

| Arm / Variant | Mathematical Configuration | Mean ARI | SD | Median ARI | IQR |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **V0: Ambient StdCons** | Ambient Features + Dense Co-occurrence | $0.037$ | $0.062$ | $0.026$ | $0.043$ |
| **V1: Ambient KMeans** | Ambient Features + Direct Sample K-Means | $0.051$ | $0.054$ | $0.029$ | $0.038$ |
| **V2: BGSS StdCons** | BGSS Gating + Dense Co-occurrence | $0.077$ | $0.089$ | $0.041$ | $0.082$ |
| **V3: Ambient Anchor** | Ambient Features + Bipartite Graph | $0.046$ | $0.051$ | $0.021$ | $0.048$ |
| **V4: Random Bipartite**| Random Feature Gating + Bipartite Graph | $0.047$ | $0.050$ | $0.022$ | $0.046$ |
| **V5: BGSS RandomAnch** | BGSS Gating + Uniform Random Landmarks | $0.198$ | $0.246$ | $0.059$ | $0.215$ |
| **V6: Full ICC-v2** | BGSS Gating + Certified Core Anchors | $0.217$ | $0.253$ | $0.061$ | $0.228$ |

---

### 2.3 Hypothesis Testing Matrix

| Hypothesis / Comparison | Null Hypothesis ($H_0$) | Test Procedure | Test Stat ($W$) | Uncorrected $p$ | Holm-Adjusted $p$ | Statistical Decision |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BGSS Bipartite Gain (V6 vs V3)** | $\Delta_{\text{ARI}} \le 0$ | Paired Wilcoxon (greater) | $W = 20.0$ | $p = 0.0312$ | $p_{\text{adj}} = 0.2496$ | Reject uncorr. / Retain corr. |
| **BGSS over Random (V6 vs V4)** | $\Delta_{\text{ARI}} \le 0$ | Paired Wilcoxon (greater) | $W = 20.0$ | $p = 0.0312$ | $p_{\text{adj}} = 0.2496$ | Reject uncorr. / Retain corr. |
| **Dense BGSS Gain (V2 vs V0)** | $\Delta_{\text{ARI}} \le 0$ | Paired Wilcoxon (greater) | $W = 18.0$ | $p = 0.0781$ | $p_{\text{adj}} = 0.4686$ | Retain $H_0$ |
| **Bipartite Gain (V3 vs V0)** | $\Delta_{\text{ARI}} \le 0$ | Paired Wilcoxon (greater) | $W = 14.0$ | $p = 0.2812$ | $p_{\text{adj}} = 0.8436$ | Retain $H_0$ |
| **Core Anchors Null (V6 vs V5)** | $\Delta_{\text{ARI}} = 0$ | Paired Wilcoxon (two-sided) | $W = 9.0$ | $p = 0.8438$ | $p_{\text{adj}} = 1.0000$ | **Retain $H_0$ (Empirical Null)** |

---

### 2.4 Leave-One-Cohort-Out Sensitivity Analysis

Evaluating the dependence of Full ICC-v2's mean performance on individual biological cohorts:

| Excluded Cohort | Remaining Sample | Mean ARI | Median ARI | Impact Assessment |
| :--- | :--- | :--- | :--- | :--- |
| *None (Full Suite)* | $N=6$ | $0.217$ | $0.061$ | Full baseline |
| **Excluding Leukemia** | $N=5$ | **$0.140$** | $0.050$ | $-35.5\%$ drop in mean ARI |
| **Excluding SRBCT** | $N=5$ | **$0.151$** | $0.050$ | $-30.4\%$ drop in mean ARI |
| **Excluding Leukemia & SRBCT** | $N=4$ | **$0.039$** | $0.035$ | **$-82.0\%$ drop: effect vanishes** |
| Excluding CNS | $N=5$ | $0.256$ | $0.072$ | Mean ARI increases |
| Excluding Colon | $N=5$ | $0.246$ | $0.050$ | Stable |
| Excluding Ovarian | $N=5$ | $0.250$ | $0.072$ | Stable |
| Excluding Prostate | $N=5$ | $0.258$ | $0.072$ | Stable |

**Critical Scientific Insight:**  
The aggregate advantage of BGSS is not a uniform cross-cohort phenomenon; it is concentrated in cohorts exhibiting discrete, multi-class clean transcriptional separation (Leukemia: ALL vs. AML; SRBCT: 4 childhood tumor classes). In noisy, continuous, or uncurated cohorts (Prostate, CNS), BGSS provides negligible benefit above ambient consensus.

---

## 3. Pseudoreplication and Small-Cohort Inferential Safeguards

1. **Unit of Inference:**  
   The statistical unit of inference is the biological cohort ($N=6$). Seeds and subsample draws represent within-cohort measurement precision, not independent biological replicates.
2. **Confidence Intervals:**  
   Standard normal approximations fail on $N=6$. Bootstrap confidence intervals must use **cohort-clustered percentile bootstrapping** or report non-parametric studentized intervals with conservative degrees of freedom ($t_{\text{df}=5}$).
3. **Correlation Analysis:**  
   Computing a single Pearson correlation over all 72 method-cohort cells ($12 \text{ models} \times 6 \text{ cohorts}$) conflates between-method and between-cohort effects, artificially inflating nominal degrees of freedom from $4$ to $70$. All stability-accuracy correlations must be reported as per-cohort distributions or modeled via linear mixed-effects with random cohort intercepts.
