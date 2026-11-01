# Research Audit 15: Statistical Analysis Plan & Multiple Testing Protocol

**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Document Reference:** `AUDIT-15-STATISTICAL-PLAN`  
**Date:** 2026-10-31  

---

## 1. Primary Principle of Experimental Units & Pseudoreplication

> **Statistical Axiom:** The experimental unit in cross-cohort benchmark comparisons is the **independent patient cohort** ($j \in \{1, \dots, J\}$). Random algorithmic seeds drawn on the same dataset are nested technical replicates, not independent biological evidence.

Treating 30 random seeds from 6 cohorts as $N = 180$ independent observations is a form of pseudoreplication that severely deflates standard errors and yields falsely small $p$-values. The DMKD submission must enforce cohort-level clustered inference.

---

## 2. Statistical Testing & Estimation Hierarchy

### 2.1 Paired Comparisons across Cohorts
For any two algorithms $A$ and $B$, let $Y_{Aj}$ and $Y_{Bj}$ denote the mean performance on cohort $j$ averaged across replicate seeds:
$$\Delta_j = Y_{Aj} - Y_{Bj}, \quad j = 1, \dots, J$$
- **Primary Test:** Two-sided Wilcoxon signed-rank test on $\Delta_1, \dots, \Delta_J$:
  $$W = \min(W^+, W^-), \quad W^+ = \sum_{j : \Delta_j > 0} R_j, \quad W^- = \sum_{j : \Delta_j < 0} R_j$$
  where $R_j$ is the rank of $|\Delta_j|$.
- **Minimum $p$-Value Constraint:** With $J = 6$ cohorts, the exact minimum possible two-sided $p$-value is $2^{-(6-1)} = 0.03125$. With $J = 12$ expanded cohorts, the minimum drops to $2^{-(12-1)} \approx 0.00049$, providing adequate statistical power.

### 2.2 Hierarchical / Dataset-Clustered Bootstrap ($B = 10{,}000$)
To compute distribution-free confidence intervals that account for both cohort-level variance and within-cohort seed variance:
1. For $b = 1, \dots, B$:
   - Resample $J$ cohorts with replacement from $\{1, \dots, J\}$.
   - For each selected cohort $j$, resample $S$ seeds with replacement from $\{0, \dots, S-1\}$.
   - Compute bootstrap statistic $\hat{\theta}^{(b)}$ (e.g. mean difference, discordance gap).
2. The $95\%$ bootstrap confidence interval is the $[\alpha/2, 1 - \alpha/2]$ percentile interval:
   $$\text{CI}_{0.95} = [\hat{\theta}_{(250)}, \hat{\theta}_{(9750)}]$$

### 2.3 Multiplicity Control: Holm–Bonferroni Correction
When evaluating a family of $M_{\text{tests}}$ pairwise hypotheses (e.g. comparing GAC against multiple comparative baselines, or testing gating across three consensus types):
1. Sort unadjusted $p$-values: $p_{(1)} \le p_{(2)} \le \dots \le p_{(M)}$.
2. Compare each $p_{(m)}$ against step-down threshold:
   $$\alpha_m = \frac{\alpha}{M - m + 1}$$
3. Reject $H_{(m)}$ if $p_{(k)} \le \alpha_k$ for all $k \le m$.
4. Adjusted $p$-value: $p_{\text{adj}, (m)} = \max_{k \le m} \min(1.0, (M - k + 1) p_{(k)})$.

### 2.4 Random-Effects Meta-Analysis (DerSimonian–Laird Model)
Synthesizes evidence across heterogeneous cohorts while explicitly quantifying between-cohort variance $\tau^2$:
- **Standardized Mean Difference (Hedges' $g$):**
  $$g_j = \left( 1 - \frac{3}{4(n_{Aj} + n_{Bj}) - 9} \right) \frac{\bar{Y}_{Aj} - \bar{Y}_{Bj}}{S_{\text{pooled}, j}}$$
- **Cochran's Heterogeneity Test:**
  $$Q = \sum_{j=1}^J w_j (g_j - \bar{g})^2, \quad w_j = \frac{1}{\mathrm{Var}(g_j)}$$
- **Between-Cohort Heterogeneity Variance ($\tau^2$):**
  $$\tau^2 = \max\left( 0, \frac{Q - (J - 1)}{\sum w_j - \frac{\sum w_j^2}{\sum w_j}} \right)$$
- **Inconsistency Index ($I^2$):**
  $$I^2 = \max\left(0, \frac{Q - (J - 1)}{Q}\right) \times 100\%$$
- **Summary Random-Effects Weight:** $w_j^* = \frac{1}{\mathrm{Var}(g_j) + \tau^2}$.

### 2.5 Vargha–Delaney Non-Parametric Effect Size ($A_{12}$)
Quantifies the probability that algorithm $A$ yields a higher score than algorithm $B$ on a random run:
$$A_{12} = \frac{\sum_{i=1}^m \sum_{k=1}^n \mathbb{I}(X_i > Y_k) + 0.5 \mathbb{I}(X_i = Y_k)}{m \cdot n}$$
- $A_{12} = 0.50$: Stochastic equivalence.
- $A_{12} > 0.56$: Small advantage.
- $A_{12} > 0.64$: Medium advantage.
- $A_{12} > 0.71$: Large advantage.
