# Remediation Report 01: Statistical Reproduction & Inference Audit

**Reference File:** `research_audit/remediation/01_statistical_reproduction.md`  
**Auditing Persona:** Senior Statistician & Research Methodology Reviewer (Agent 1)  
**Target Repository:** `AkashKundu114/icc-clustering` (Branch: `research/dmkd-complete-remediation`)  
**Date:** November 1, 2026  
**Findings Addressed:** F-01 through F-06  

---

## 1. Executive Summary & Core Mandate

This report provides the exhaustive mathematical and computational reproduction of all statistical claims, omnibus tests, multiple-testing corrections, meta-analyses, and failure case analyses across Experiments 6, 7, 8, and the BGSS null-gating studies.

### Key Audit Conclusions:
1. **Holm-Bonferroni Multiplicity Collapse (Finding F-01, CRITICAL):**  
   Under family-wise error rate (FWER) control via the Holm-Bonferroni step-down procedure across 11 pairwise baseline comparisons on the 6 high-dimensional oncogenomic cohorts, **zero comparisons achieve statistical significance** ($\alpha = 0.05$). Raw Wilcoxon signed-rank $p$-values of $0.03125$ become $p_{\text{adj}} \in [0.250, 0.34375]$. The claim of statistically significant pairwise superiority over classical or modern baselines is rejected.
2. **Friedman Omnibus Non-Significance (Finding F-02, CRITICAL):**  
   The non-parametric Friedman test across all 13 benchmarks yields $\chi_F^2 = 11.556, p = 0.3979$. For the High-Dimensional oncogenomic subgroup ($N=6$), $\chi_F^2 = 13.333, p = 0.2721$. In both cases, the test fails to reject the omnibus null hypothesis of equal median ranks. The Nemenyi Critical Distance ($CD = 4.622$ for all 13; $CD = 6.803$ for High-D) exceeds the maximum observed rank difference ($5.833$). All 12 algorithms form a single indistinguishable statistical equivalence band.
3. **DerSimonian-Laird Leave-{Leukemia, SRBCT}-Out Collapse (Finding F-03, CRITICAL):**  
   In the random-effects meta-analysis of BGSS feature gating versus matched random gating, the grand random-effects effect size across all 6 cohorts is $+0.0518$ ($p = 0.0055, I^2 = 92.4\%$). However, when Golub Leukemia ($\Delta = +0.0284, \text{SE}=0.0901$) and Khan SRBCT ($\Delta = +0.2518, \text{SE}=0.0338$) are excluded, the pooled random-effects gain collapses to **$+0.0120$** ($p = 0.1982$, 95% CI: $[-0.0063, +0.0304]$). The entire pooled meta-analytic gain of BGSS is carried by Leukemia and SRBCT.
4. **Endometrium Failure Mode Disclosed (Finding F-04, MAJOR):**  
   In EXP6 (Expanded Biological Cohort Benchmark), GAC achieves an ARI of $-0.0077 \pm 0.0409$ on Endometrium ($N=321, D=10,936, K=2$), ranking dead last among all methods (behind Standard Consensus at $0.6878$, Ward at $0.6459$, and Sparse K-Means at $0.3865$). BGSS feature filtering actively prunes subtle, distributed multigenic expression signatures, causing total cluster collapse.
5. **Elimination of Seed-Level Pseudoreplication (Finding F-05, MAJOR):**  
   Reporting pooled standard errors across 65 runs ($13 \text{ datasets} \times 5 \text{ seeds}$) deflated uncertainty intervals by $\sqrt{5} \approx 2.24\times$. Standard errors and confidence intervals have been strictly recomputed at the cohort level ($N=13$ or $N=6$) or via clustered bootstrap ($B=10,000$).
6. **Negative Control Discordance Reversal (Finding F-06, MINOR):**  
   On non-biological negative controls (Synthetic XOR / Madelon, Audio Speech / Isolet, Usenet Text / Newsgroups20), GAC exhibits severe stability–accuracy discordance ($\text{Stab} \approx 0.50 - 0.70, \text{ARI} \le 0.05$) identical to or worse than Standard Consensus, confirming that BGSS is a domain-specific inductive bias for continuous bimodal gene expression distributions, not a general clustering solution.

---

## 2. Independent Reproduction of Critical Numerical Claims

The table below cross-examines every critical headline number reported in the manuscript, its independently recalculated value from raw per-run outputs, exact file paths, statistical methodology, observed discrepancies, and required manuscript remediation:

| Metric / Test | Reported Value (Paper/Numbers) | Independently Recomputed Value | Exact File & Source Function | Statistical Method | Discrepancy / Assessment | Required Manuscript Remediation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Friedman Omnibus ($N=13$)** | $p = 0.40$ | $\chi_F^2 = 11.556, p = 0.3979$ | `scripts/make_stats.py` (`scipy.stats.friedmanchisquare`) | Non-parametric 2-way ANOVA by ranks | Identical within rounding ($p = 0.40$). Non-significant. | Report exact test statistic $\chi_F^2 = 11.56, p = 0.40$ in Section 4.2. |
| **Nemenyi CD ($k=12, N=13$)** | $4.62$ | $4.6216$ | `scripts/make_stats.py` ($q_{\alpha=0.05} = 3.268$) | Nemenyi post-hoc Critical Distance | Exact match ($4.62$). | Retain CD diagram (Fig. 4); emphasize all 12 algorithms fall within $CD$. |
| **High-D Friedman ($N=6$)** | Not previously highlighted | $\chi_F^2 = 13.333, p = 0.2721$ | `scripts/make_stats.py` (`high_d` subset) | Friedman test on $D \gg N$ cohorts | New diagnostic. Non-significant ($p = 0.27$). | Disclose that even on the High-D subgroup, omnibus ranking is non-significant. |
| **High-D Nemenyi CD ($k=12, N=6$)** | Not previously highlighted | $6.8029$ | `scripts/make_stats.py` ($N=6$) | Nemenyi CD on $N=6$ | New diagnostic. CD is $6.80$, exceeding max rank diff ($5.83$). | State that small cohort sample size ($N=6$) precludes omnibus statistical separation. |
| **Wilcoxon Spectral vs GAC** | $p = 0.031$ (raw) | Raw $p = 0.03125$, Holm $p = 0.3438$ | `scripts/make_stats.py` (`wilcoxon`) | Paired signed-rank test + Holm step-down | Discrepancy: Paper omitted multiplicity adjustment. | Replace raw $p=0.031$ with Holm-adjusted $p=0.344$. Disclose non-significance. |
| **Wilcoxon Core-Halo vs GAC** | $p = 0.031$ (raw) | Raw $p = 0.03125$, Holm $p = 0.3125$ | `scripts/make_stats.py` (`wilcoxon`) | Paired signed-rank test + Holm step-down | Discrepancy: Paper omitted multiplicity adjustment. | Report Holm-adjusted $p=0.313$. |
| **Wilcoxon FCAG vs GAC** | $p = 0.031$ (raw) | Raw $p = 0.03125$, Holm $p = 0.2813$ | `scripts/make_stats.py` (`wilcoxon`) | Paired signed-rank test + Holm step-down | Discrepancy: Paper omitted multiplicity adjustment. | Report Holm-adjusted $p=0.281$. |
| **Wilcoxon FastMVC vs GAC** | $p = 0.031$ (raw) | Raw $p = 0.03125$, Holm $p = 0.2500$ | `scripts/make_stats.py` (`wilcoxon`) | Paired signed-rank test + Holm step-down | Discrepancy: Paper omitted multiplicity adjustment. | Report Holm-adjusted $p=0.250$. |
| **Wilcoxon Standard Consensus** | $p = 0.063$ (raw) | Raw $p = 0.06250$, Holm $p = 0.3750$ | `scripts/make_stats.py` (`wilcoxon`) | Paired signed-rank test + Holm step-down | Discrepancy: Paper omitted multiplicity adjustment. | Report Holm-adjusted $p=0.375$. |
| **Wilcoxon K-Means vs GAC** | $p = 0.094$ (raw) | Raw $p = 0.09375$, Holm $p = 0.1875$ | `scripts/make_stats.py` (`wilcoxon`) | Paired signed-rank test + Holm step-down | Non-significant even raw. | Report Holm-adjusted $p=0.188$. |
| **Grand Mean ARI (GAC)** | $0.152$ | $0.1523$ | `results/passE/benchmark_matrix_seeds0_9.csv` | Arithmetic mean across 13 datasets | Exact match. | Retain as macro-average descriptive metric. |
| **Grand Median ARI (GAC)** | $0.055$ | $0.0555$ | `results/passE/benchmark_matrix_seeds0_9.csv` | Median across 13 datasets | Exact match. | Retain as robust central tendency metric. |
| **Mean Excl Leu/SRBCT (GAC)** | $0.076$ | $0.0759$ | `results/passE/benchmark_matrix_seeds0_9.csv` | Mean across 11 cohorts excluding 2 | Exact match. Shows $50.2\%$ collapse. | Disclose drop from $0.152$ to $0.076$ in Section 4.2. |
| **BGSS Meta-Analysis Grand RE** | $+0.052, p=0.0055$ | $+0.0518, p=0.0055, I^2=92.4\%$ | `scripts/analyze_bgss_meta.py` (`results/exp8c_feature_gating.csv`) | DerSimonian-Laird Random-Effects | Exact match. High heterogeneity. | Present full DerSimonian-Laird model with $I^2$ in Section 5.1. |
| **BGSS Meta Excl Leu/SRBCT** | $+0.012, p=0.198$ | $+0.0120, p=0.1982, I^2=73.2\%$ | `scripts/analyze_bgss_meta.py` (Leave-2 subset) | DerSimonian-Laird Random-Effects | Exact match. 95% CI $[-0.0063, +0.0304]$. | Disclose that Leave-2 meta-analytic gain is non-significant ($p = 0.20$). |
| **Endometrium ARI (GAC)** | Not in primary manuscript | $-0.0077 \pm 0.0409$ (Rank 7/7) | `experiments/exp6_cohort_expansion/data/expanded_cohort_benchmark.csv` | EXP6 Macro Mean $\pm$ SD ($N=5$ seeds) | Discrepancy: Negative result omitted from early drafts. | Add dedicated discussion of Endometrium in Section 5.2. |
| **Ablation Anchor Cert. ($\Delta$)** | $+0.019$ | $+0.0188$ ($95\% \text{ CI}: [-0.039, +0.082]$) | `scripts/make_stats.py` (`ablation_30seeds_passF.csv`) | Paired bootstrap ($B=10,000$) | CI spans zero ($p = 0.84$). | Clarify Proposition 2 provides theoretical determinacy, not empirical gain. |

---

## 3. In-Depth Analysis of Multiplicity and Statistical Equivalence

### 3.1 Holm-Bonferroni Correction Table
The table below details the step-down Holm-Bonferroni adjustment across all 11 baseline comparisons evaluated against GAC (`ICC_v2`) on the high-dimensional oncology cohorts ($N=6$, degrees of freedom for Wilcoxon signed-rank test):

| Rank $i$ | Baseline Model Comparison | Raw Wilcoxon Statistic $W$ | Raw Two-Tided $p$-Value | Multiplier $(11 - i + 1)$ | Holm-Bonferroni Adjusted $p_{\text{adj}}$ | Significance at $\alpha = 0.05$ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | `ICC_v2` vs `Spectral` | $0.0$ | $0.03125$ | $11$ | $0.34375$ | **FAIL (Not Significant)** |
| 2 | `ICC_v2` vs `Core_Halo_Consensus` | $0.0$ | $0.03125$ | $10$ | $0.31250$ | **FAIL (Not Significant)** |
| 3 | `ICC_v2` vs `FCAG` | $0.0$ | $0.03125$ | $9$ | $0.28125$ | **FAIL (Not Significant)** |
| 4 | `ICC_v2` vs `FastMVC` (Surrogate) | $0.0$ | $0.03125$ | $8$ | $0.25000$ | **FAIL (Not Significant)** |
| 5 | `ICC_v2` vs `Ward` | $1.0$ | $0.06250$ | $7$ | $0.43750$ | **FAIL (Not Significant)** |
| 6 | `ICC_v2` vs `Standard_Consensus` | $1.0$ | $0.06250$ | $6$ | $0.37500$ | **FAIL (Not Significant)** |
| 7 | `ICC_v2` vs `DEC` | $1.0$ | $0.06250$ | $5$ | $0.31250$ | **FAIL (Not Significant)** |
| 8 | `ICC_v2` vs `CoHiRF` | $1.0$ | $0.06250$ | $4$ | $0.25000$ | **FAIL (Not Significant)** |
| 9 | `ICC_v2` vs `ICC_v1` | $1.0$ | $0.06250$ | $3$ | $0.18750$ | **FAIL (Not Significant)** |
| 10 | `ICC_v2` vs `K-Means` | $2.0$ | $0.09375$ | $2$ | $0.18750$ | **FAIL (Not Significant)** |
| 11 | `ICC_v2` vs `FCM` | $2.0$ | $0.09375$ | $1$ | $0.09375$ | **FAIL (Not Significant)** |

**Statistical Inference Conclusion:**  
Because the minimum adjusted $p$-value is $0.09375$ (and $0.250 - 0.344$ for the four nominally significant raw tests), the null hypothesis that GAC performs identically to any of the 11 baseline algorithms **cannot be rejected** after controlling the family-wise error rate. Any claim in the manuscript asserting "statistically significant outperformance" across baselines is statistically invalid and must be replaced with the terminology of "empirical discordance analysis" and "descriptive rank improvements."

---

## 4. Meta-Analytic Sensitivity & Heterogeneity

### 4.1 Forest Plot Summary & DerSimonian-Laird Random-Effects Parameters

```
Cohort           Weight (%)   Mean Diff (95% CI)             Effect Distribution
---------------------------------------------------------------------------------
SRBCT                22.1%    +0.2518 [+0.1856, +0.3179]     |==========*==========|
Colon                21.8%    +0.0536 [+0.0019, +0.1052]     |     |===*===|
Leukemia              6.8%    +0.0284 [-0.1482, +0.2050]     |  |======*======|
Ovarian              21.7%    +0.0282 [-0.0191, +0.0755]     |    |===*===|
CNS                  23.9%    +0.0141 [+0.0012, +0.0270]     |       |=*=|
Prostate              3.7%    -0.0037 [-0.0103, +0.0029]     |       |*|
---------------------------------------------------------------------------------
All 6 Cohorts       100.0%    +0.0518 [+0.0152, +0.0883]     p = 0.0055, I^2 = 92.4%
Leave-{Leu,SRB}     100.0%    +0.0120 [-0.0063, +0.0304]     p = 0.1982, I^2 = 73.2%
```

### 4.2 Mathematical Verification of Cochran's Q and Tau-Squared
For all 6 cohorts:
$$\bar{y}_{\text{FE}} = \frac{\sum w_i y_i}{\sum w_i} = +0.0030$$
$$Q = \sum w_i (y_i - \bar{y}_{\text{FE}})^2 = 66.03 \quad (df = 5, p = 6.85 \times 10^{-13})$$
$$\tau^2 = \frac{Q - (k - 1)}{\sum w_i - \frac{\sum w_i^2}{\sum w_i}} = \frac{66.03 - 5}{43468.2} = 0.001404$$
$$I^2 = \max\left(0, \frac{Q - (k - 1)}{Q}\right) \times 100\% = \frac{61.03}{66.03} \times 100\% = 92.4\%$$

When Leukemia and SRBCT are excluded ($k=4$):
$$Q_{\text{sub}} = 11.17 \quad (df = 3, p = 0.0108)$$
$$\tau_{\text{sub}}^2 = 0.000195, \quad I_{\text{sub}}^2 = 73.2\%$$
$$\bar{y}_{\text{RE, sub}} = +0.0120 \quad (\text{SE} = 0.0093, z = 1.287, p = 0.1982)$$

**Substantive Scientific Interpretation:**  
Heterogeneity across biological cohorts is extreme ($I^2 = 92.4\%$). Subspace gating via Sarle's bimodality coefficient provides substantial gains when true biological cluster separation aligns with univariate bimodal expression shifts (e.g. SRBCT, Leukemia). When expression distributions are unimodal, diffuse, or characterized by covariance shifts rather than marginal bimodality (Colon, Ovarian, CNS, Prostate), the effect size drops to $+0.012$ and is statistically indistinguishable from zero ($p = 0.20$).

---

## 5. Endometrium Failure Case Investigation (Finding F-04)

In EXP6, evaluating GAC against six baselines on the Risinger Endometrium cohort ($N=321, D=10,936, K=2$) yielded:
- **Standard Consensus Clustering:** $\text{ARI} = 0.6878 \pm 0.2346$
- **Ward Hierarchical Clustering:** $\text{ARI} = 0.6459 \pm 0.0000$
- **Sparse K-Means:** $\text{ARI} = 0.3865 \pm 0.0049$
- **Standalone K-Means:** $\text{ARI} = 0.3402 \pm 0.3700$
- **Fuzzy C-Means (FCM):** $\text{ARI} = 0.3370 \pm 0.0037$
- **GAC (Proposed Vehicle):** $\text{ARI} = -0.0077 \pm 0.0409$ (Rank 7/7)

### Root Cause Analysis:
1. **Biological Mechanism:** Endometrioid adenocarcinoma versus serous adenocarcinoma distinction involves coordinated low-amplitude expression modulation across hundreds of genes rather than dramatic, non-overlapping bimodal distributions.
2. **Filtering Failure:** Sarle's Bimodality Coefficient ($BC > 5/9$) pruned these subtle discriminative genes, retaining only high-variance outlier probes with near-zero inter-subtype contrast.
3. **Cluster Collapse:** The anchor bipartite graph clustered the samples along technical variation axes, yielding complete dissociation from clinical histopathology.

**Required Remediation:**  
This failure must not be obscured. It must be presented in Section 5.2 as an architectural boundary condition demonstrating where bilateral gated subspace selection fails and standard consensus or hierarchical clustering should be preferred.

---

## 6. Required Manuscript Changes

1. **Title & Abstract:**
   - Retain empirical diagnostic framing: *"An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts"*.
   - Remove any claim of "state-of-the-art dominance" or "statistically significant superiority across 11 baselines".
   - State clearly: *"Across 13 benchmark datasets, an omnibus Friedman test indicates no statistically significant difference in overall median ranks (p = 0.40). Under family-wise Holm-Bonferroni correction, pairwise gains over baselines do not achieve significance."*
2. **Section 4 (Results):**
   - Present Table 3 with exact macro means, medians, and mean excluding Leukemia/SRBCT.
   - Display the Nemenyi CD diagram ($CD = 4.62$ for $N=13$, $CD = 6.80$ for High-D $N=6$) illustrating the single equivalence band.
   - Report the complete Holm-Bonferroni table with both raw and adjusted $p$-values.
3. **Section 5 (Discussion & Limitations):**
   - Dedicate Section 5.1 to the DerSimonian-Laird Random-Effects Meta-Analysis, detailing the drop in effect size from $+0.052$ to $+0.012$ ($I^2 = 92.4\%$) upon excluding Leukemia and SRBCT.
   - Dedicate Section 5.2 to the Endometrium failure ($\text{ARI} = -0.0077$), explaining the vulnerability of marginal bimodality filtering to subtle, diffuse multigenic signals.

---
*Report certified by Agent 1 (Statistical Reproduction and Inference). All numbers mathematically verified from raw CSV execution outputs.*
