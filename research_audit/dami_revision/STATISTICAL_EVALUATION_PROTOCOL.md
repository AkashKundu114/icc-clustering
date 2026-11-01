# Statistical Evaluation Protocol and Inferential Architecture

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Working Branch:** `research/dami-revision`  
**Audit Component:** Agent D — Statistical Evaluation and Inference  
**Date of Record:** November 1, 2026  
**Status:** **AUDITED AND VERIFIED**

---

## 1. Foundational Principles of Inferential Validity

### 1.1 The Biological Cohort as the Principal Unit of Generalization
In high-dimensional biomedical clustering, the independent sampling unit is the **biological cohort** (an independent patient population or clinical trial series $j \in \{1, \dots, J\}$). 

**Pseudoreplication Safeguards:**
- Random initialization seeds ($S = 30$) and subsampling draws ($B = 30$) represent within-cohort measurement precision, **not** independent biological replicates.
- Treating multiple algorithms or repeated seeds on the same biological cohort as independent samples to manufacture thousands of degrees of freedom is strictly prohibited.
- All primary confirmatory inferences are conducted on cohort-level summary statistics.

### 1.2 Two-Stage Hierarchical Aggregation Pipeline
To eliminate pseudoreplication while retaining measurement precision:
1. **Stage 1 (Within-Cohort Aggregation):** For algorithm $m$ on cohort $j$, compute the median performance across the 30 canonical random seeds:
   $$\tilde{Y}_{m, j} = \text{Median}_{s=1}^{30}\left( Y_{m, j, s} \right)$$
   The median is chosen over the mean due to its robust resistance to single-seed k-means convergence failures.
2. **Stage 2 (Between-Cohort Inferences):** For comparative evaluations between candidate method $A$ and reference method $B$, compute paired cohort-level differences:
   $$D_j = \tilde{Y}_{A, j} - \tilde{Y}_{B, j}, \quad j = 1, \dots, J$$
   Hypothesis tests, effect sizes, and bootstrap confidence intervals are computed exclusively over the vector $\mathbf{D} = (D_1, \dots, D_J)^T$.

---

## 2. Multiplicity Architecture & Error Control

All inferential procedures are organized into locked families with pre-specified family-wise error rate (FWER) control at $\alpha = 0.05$:

### 2.1 Family 1: Primary Comparative Baselines ($M=8$ Comparisons)
- **Comparisons:** Full ICC-v2 contrasted against 8 locked baselines:
  1. `K-Means_VarFilt`
  2. `K-Means_PCA`
  3. `K-Means_LapScore`
  4. `SparseKMeans`
  5. `Spectral`
  6. `Standard_Consensus`
  7. `Li_et_al_2019`
  8. `FCAG`
- **Correction Procedure:** Holm–Bonferroni step-down procedure on sorted two-tailed / one-tailed $p$-values:
  $$p_{(i)} \le \frac{\alpha}{M - i + 1}$$
- **Binding Directional Superiority Rule:** A baseline comparison is declared statistically significant if and only if:
  $$p_{\text{adj}} < 0.05 \quad \text{AND} \quad \text{Median}(D) > 0$$

### 2.2 Family 2: Architectural Component Attribution ($M=3$ Hypotheses)
- **Hypotheses:**
  - **H2a (BGSS Gating Advantage):** BGSS vs. matched random gating under bipartite consensus. Tested via one-sided paired Wilcoxon signed-rank test.
  - **H2b (Dense Consensus Attenuation):** Difference-of-differences interaction contrast:
    $$\Delta\Delta_j = (\text{ARI}_{\text{BGSS, Bip}, j} - \text{ARI}_{\text{Rand, Bip}, j}) - (\text{ARI}_{\text{BGSS, Dense}, j} - \text{ARI}_{\text{Rand, Dense}, j})$$
    Tested via one-sided paired Wilcoxon signed-rank test ($H_0: \Delta\Delta \le 0$).
  - **H3 (Core Anchor Determinacy Equivalence):** Certified core anchors vs. uniform random landmark anchors under margin $\delta = \pm 0.02$. Evaluated via Two One-Sided Tests (TOST).
- **Correction Procedure:** Holm–Bonferroni step-down at FWER $\alpha = 0.05$.

### 2.3 Family 3: Foundational Methodological Claims ($M=2$ Hypotheses)
- **Hypotheses:**
  - **H1a (Stability–Accuracy Decoupling):** Evaluates whether subsampling stability fails to predict clustering accuracy ($\rho < 0.30$). Tested via one-sample Wilcoxon signed-rank test on cohort-averaged Fisher $z$-transformed Spearman rank correlations.
  - **H1b (Stability-Minus-Accuracy False Confidence Gap):** Evaluates whether stability systematically exceeds accuracy ($\Delta_{\text{gap}} > 0.20$ vs. $\Delta_0 = 0.05$). Tested via one-sample Wilcoxon signed-rank test on cohort-level mean gaps.
- **Correction Procedure:** Fixed-sequence hierarchical testing at $\alpha = 0.05$. H1b is formally tested if and only if H1a rejects its null hypothesis.

---

## 3. Formal Two One-Sided Tests (TOST) Equivalence Framework for H3

To completely eliminate the scientific fallacy of claiming equivalence based on a non-significant $p$-value ($p > 0.10$):
1. **Hypothesis Formulation:**
   $$H_{0,3\text{a}}: \Delta \le -0.02, \quad H_{0,3\text{b}}: \Delta \ge +0.02 \quad \text{vs.} \quad H_{1,3}: -0.02 < \Delta < +0.02$$
2. **Equivalence Margin Justification ($\delta = \pm 0.02$):** Across human cancer cohorts with sample sizes $N \in [40, 500]$, an ARI difference of $|\Delta| < 0.02$ corresponds to reassignment of only 1 to 2 patient samples, falling squarely within the stochastic noise floor of random k-means initializations ($\sigma_{\text{ARI}} \approx 0.015\text{--}0.045$).
3. **Decision Rule:**
   - Compute non-parametric $90\%$ bootstrap confidence interval for the Hodges–Lehmann median difference: $[\text{CI}_{0.05}, \text{CI}_{0.95}]$.
   - **Equivalent:** If $[\text{CI}_{0.05}, \text{CI}_{0.95}] \subset (-0.02, +0.02)$.
   - **Non-Equivalent:** If CI falls entirely outside $[-0.02, +0.02]$.
   - **Inconclusive / Underpowered:** If CI overlaps either bound ($-0.02$ or $+0.02$). The protocol strictly prohibits claiming equivalence when an inconclusive outcome is observed.

---

## 4. Power Realities and Sample Size Transparency

Analytical power calculations under non-central $t$-distributions establish:
1. **Adequate Power ($>95\%$):** Achieved for H1a and H1b on $J=15$ cohorts due to large expected effect sizes ($d_z \ge 1.0$).
2. **Contingent Power ($35\%\text{--}70\%$):** For H2a gating advantage, power is heavily contingent on the biological prevalence of clean bimodal drivers across cancer types.
3. **Severely Underpowered ($0.0\%$ Power):** For H3 TOST equivalence at $\pm 0.02$ margin. Given empirical standard deviation $\sigma_D \approx 0.084$, achieving $80\%$ power requires $J \approx 162$ independent cohorts.
4. **Transparency Mandate:** The manuscript must openly report this statistical reality, represent $J=15$ as an underpowered preliminary confirmatory panel for equivalence, and report confidence intervals rather than definitive claims of confirmation.
