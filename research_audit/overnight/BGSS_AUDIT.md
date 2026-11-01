# Overnight Research Audit: BGSS Implementation, Random-Gating Controls & Two-Cohort Sensitivity

**Document Reference:** `research_audit/overnight/BGSS_AUDIT.md`  
**Related Results:**  
- `research_audit/overnight/BGSS_RESULTS.md` (To be produced post-execution)  
- `results/overnight/bgss/`  
**Audit Date:** 2026-11-01  
**Auditor:** Agent B — Statistical & BGSS Auditor  

---

## 1. Algorithmic Formulation & Mathematical Verification of BGSS

Bimodal Gene Subset Selection (BGSS) is designed to identify features exhibiting multi-modal distribution patterns that correspond to discrete subtype signatures, rather than unimodal noise.

### Mathematical Formulation:
For a candidate gene or feature vector $\mathbf{x}_j = [x_{1j}, \dots, x_{nj}]^T \in \mathbb{R}^n$, the Bimodality Coefficient ($BC$) is defined by Sarle's formulation:

$$BC_j = \frac{\gamma_j^2 + 1}{\kappa_j + 3 \cdot \frac{(n-1)^2}{(n-2)(n-3)}}$$

where:
- $\gamma_j$ is the sample skewness of feature $j$.
- $\kappa_j$ is the sample excess kurtosis of feature $j$.
- $n$ is the sample size (number of observations/patients).

Under the classical uniform distribution on a compact interval, $BC = 5/9 \approx 0.5556$. For any unimodal normal distribution, $BC = 1/3 \approx 0.3333$.  
**Theoretical Selection Criterion:** Feature $j$ is admitted into the gated subspace $\mathcal{S}_{\text{BGSS}}$ if and only if:

$$BC_j > \tau_{\text{bimodal}} = \frac{5}{9} \approx 0.5556$$

### Verification in Codebase:
Inspection of `src/icc/consensus_v2.py` and `src/icc/aspp.py` confirms:
1. `_compute_bimodality_coefficient` utilizes `scipy.stats.skew` and `scipy.stats.kurtosis` with bias-correction factors enabled.
2. The selection threshold $\tau_{\text{bimodal}} = 0.5556$ is implemented without hard-coded constants or class label leakage.
3. Features not meeting the threshold are filtered before anchor consensus graph construction.

---

## 2. Matched Random-Gating Control Protocol

To ensure that performance gains are not simply due to dimensionality reduction per se (i.e. randomly reducing $D$ dimensions), every BGSS experiment must be matched against a **Matched Random-Gating Control**:

- **Definition of Control:** If BGSS selects $d_{\text{active}} = |\mathcal{S}_{\text{BGSS}}|$ features on cohort $\mathcal{D}$, the Matched Random-Gating Control uniformly samples exactly $d_{\text{active}}$ features from $\{1, \dots, D\}$ at random using the identical random seed.
- **Fairness Guarantee:** Both methods receive the exact same data matrix, sample size $N$, active dimension count $d_{\text{active}}$, anchor count $m = \lfloor\sqrt{N}\rfloor$, base clusterer (K-Means), and consensus aggregation function.
- **Hypothesis Test:**
  $$H_0: \mathbb{E}[\text{ARI}(\text{ICC}_{\text{BGSS}})] \le \mathbb{E}[\text{ARI}(\text{ICC}_{\text{Random}})]$$
  $$H_1: \mathbb{E}[\text{ARI}(\text{ICC}_{\text{BGSS}})] > \mathbb{E}[\text{ARI}(\text{ICC}_{\text{Random}})]$$

---

## 3. The "Two-Cohort Effect" Audit & Vulnerability Assessment

A critical vulnerability identified in previous audit loops is whether the apparent superiority of BGSS is an artifact of **extreme concentration in two specific datasets**:

1. **Golub Acute Leukemia (1999):**  
   - $\text{ARI}(\text{ICC}_{\text{BGSS}}) = 0.8385$ vs $\text{ARI}(\text{Standard Consensus}) = 0.1958$ ($\Delta = +0.6428$).
   - Distinct, well-separated lineage markers between ALL (lymphoid) and AML (myeloid) give very high bimodality coefficients ($BC > 0.70$).
2. **Khan SRBCT (2001):**  
   - $\text{ARI}(\text{ICC}_{\text{BGSS}}) = 0.5872$ vs $\text{ARI}(\text{Standard Consensus}) = 0.0631$ ($\Delta = +0.5240$).
   - Distinct neural vs muscular vs lymphoid origins of childhood tumors create strong bimodal gene expression spikes.

### The Sensitivity Stress Tests Designed:
To determine whether BGSS genuinely generalises or collapses without these two cohorts, Agent B designs four mandatory sensitivity analyses:
1. **Analysis A (Full 10-Cohort Suite):** Random-effects meta-analysis across all 10 Category A independent cohorts.
2. **Analysis B (Leave-Leukemia-Out):** Recompute pooled effect and heterogeneity omitting Leukemia.
3. **Analysis C (Leave-SRBCT-Out):** Recompute pooled effect and heterogeneity omitting SRBCT.
4. **Analysis D (Leave-Leukemia-and-SRBCT-Out):** Recompute pooled effect across the remaining 8 independent cohorts.
5. **Analysis E (Full Leave-One-Cohort-Out Grid):** Stepwise omission of each cohort to establish the empirical bounds of the pooled effect.

---

## 4. Statistical Testing Architecture

All comparisons will be evaluated using:
1. **Paired Wilcoxon Signed-Rank Test:** Non-parametric two-sided test on paired differences $\Delta_i = \text{ARI}_{\text{BGSS}, i} - \text{ARI}_{\text{Baseline}, i}$.
2. **DerSimonian-Laird Random-Effects Meta-Analysis:** Incorporates between-study variance $\tau^2$ to calculate pooled effect size and 95% confidence intervals.
3. **Cochran's $Q$ and Higgins & Thompson $I^2$ Heterogeneity Index:**
   $$I^2 = \max\left(0, \frac{Q - (k-1)}{Q}\right) \times 100\%$$
   Quantifies the proportion of observed variance attributable to true clinical heterogeneity vs sampling noise.
