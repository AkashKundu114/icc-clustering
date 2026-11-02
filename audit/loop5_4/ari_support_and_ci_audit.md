# Loop 5.4 — Statistical Methodology Audit: ARI Support and Confidence-Interval Interpretation

**Phase:** Loop 5.4 — Final Adversarial Statistical Validation & Manuscript Claim Adjudication  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target Manuscript:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Date:** November 2026  
**Auditor:** Agent A — Statistical Methodology Specialist  
**Deliverable Associated:** [ari_support_and_ci_audit.md](file:///d:/icc-clustering/audit/loop5_4/ari_support_and_ci_audit.md)

---

## 1. Executive Summary & Foundational Mathematical Correction

A pervasive error throughout Loops 2, 5, 5.1, 5.2, and 5.3 was the assertion that the Adjusted Rand Index (ARI) is mathematically bounded on the unit interval $[0, 1]$, and that any confidence interval with a negative lower endpoint is prima facie mathematically invalid.

This audit establishes the following rigorous mathematical corrections:
1. **The Adjusted Rand Index is NOT bounded on $[0, 1]$.** Its theoretical range is $[\text{ARI}_{\min}, 1.0]$, where $\text{ARI}_{\min} < 0$. Negative values reflect cluster alignments that are worse than expected under random permutation with fixed marginals.
2. **A negative lower endpoint does NOT invalidate an inferential interval for ARI.** It simply indicates that the confidence region includes scenarios where agreement is worse than random chance.
3. **An upper endpoint exceeding $1.0$ DOES indicate model failure.** Because $\max(\text{ARI}) \equiv 1.0000$ strictly by construction, an upper limit $> 1.0$ demonstrates that the parametric probability model (e.g. unbounded Gaussianity) contradicts the physical support of the metric.
4. **The Student-$t$ interval $[-0.1048, 1.0397]$ is rejected not because it is negative, but because it assumes an unbounded Gaussian distribution on severely bimodal, skewed 5-seed data**, violating the upper bound and delivering meaningless nominal coverage.
5. **A 10-seed bootstrap interval characterizes algorithmic initialization stochasticity on a fixed cohort, NOT population-level biological uncertainty.**

---

## 2. Mathematical Definition and Theoretical Support of the Adjusted Rand Index

### 2.1 Formulation (Hubert & Arabie, 1985)
Let $U = \{u_1, \dots, u_R\}$ and $V = \{v_1, \dots, v_C\}$ be two partitions of $N$ objects. Let $n_{ij} = |u_i \cap v_j|$, $a_i = \sum_j n_{ij}$, and $b_j = \sum_i n_{ij}$.
The unadjusted Rand Index (RI) counts concordant and discordant pairs:
$$\text{RI} = \frac{\sum_{i,j} \binom{n_{ij}}{2} + \binom{N}{2} - \left[ \frac{1}{2} \sum_i a_i^2 + \frac{1}{2} \sum_j b_j^2 - \sum_{i,j} n_{ij}^2 \right]}{\binom{N}{2}} \in [0, 1]$$

Under the generalized hypergeometric model of random permutations with fixed cluster size marginals, the expectation is:
$$\mathbb{E}\left[ \sum_{i,j} \binom{n_{ij}}{2} \right] = \frac{\sum_i \binom{a_i}{2} \sum_j \binom{b_j}{2}}{\binom{N}{2}}$$

The Adjusted Rand Index is defined by chance-correction:
$$\text{ARI} = \frac{\sum_{i,j} \binom{n_{ij}}{2} - \mathbb{E}\left[ \sum_{i,j} \binom{n_{ij}}{2} \right]}{\frac{1}{2}\left[ \sum_i \binom{a_i}{2} + \sum_j \binom{b_j}{2} \right] - \mathbb{E}\left[ \sum_{i,j} \binom{n_{ij}}{2} \right]}$$

### 2.2 Exact Range and Metric Support
- **Upper Bound:** $\text{ARI} \le 1.0$, with equality if and only if partitions $U$ and $V$ are identical up to label permutation.
- **Expected Value:** $\mathbb{E}[\text{ARI}] = 0.0$ when partitions are drawn independently at random conditional on marginal cluster sizes.
- **Lower Bound:** When the observed pair overlap is zero ($\sum_{i,j} \binom{n_{ij}}{2} = 0$), the numerator becomes strictly negative:
  $$\text{ARI}_{\min} = \frac{-\mathbb{E}\left[ \sum_{i,j} \binom{n_{ij}}{2} \right]}{\frac{1}{2}\left[ \sum_i \binom{a_i}{2} + \sum_j \binom{b_j}{2} \right] - \mathbb{E}\left[ \sum_{i,j} \binom{n_{ij}}{2} \right]} < 0$$
  Depending on cluster size balance, $\text{ARI}_{\min}$ can reach $-0.5$ (in balanced two-class settings) or approach $-1.0$.

### 2.3 Verification in Codebase and Library Implementations
In scikit-learn (`sklearn.metrics.adjusted_rand_score`), ARI is implemented following Hubert & Arabie (1985).
In the repository's primary data:
- In `results/loop2/raw/exp5_baseline_comparison.csv`, Seed 999 on Leukemia yields $\text{ARI} = -0.044618$.
- In `results/evidence_recovery/recovered/subsample_stability_summary.csv`, FastMVC on Colon yields $\text{ARI} = -0.0195$, and FCAG on Colon yields $\text{ARI} = -0.0168$.
- These negative empirical values are mathematically valid and reflect partitions that misalign relative to the marginal baseline.

---

## 3. Inventory of Erroneous Statements in Prior Audits

The following audit statements asserted the false $[0, 1]$ restriction and are hereby formally disproven:

| Audit Document | Line / Citation | Erroneous Claim | Forensic Correction |
|:---|:---:|:---|:---|
| **Loop 5.1 Report** | `independent_reproduction_report.md` (Line 37) | *"exceeding the natural bounded metric domain [0, 1]"* | ARI is bounded on $[\text{ARI}_{\min}, 1.0]$, not $[0, 1]$. Negative values are mathematically valid. |
| **Loop 5.1 Claim Ledger** | `claim_ledger_adjudication.csv` (CLM-10) | *"The reported interval violates the bounded domain [0, 1] of ARI"* | False assumption. Only the upper bound ($> 1.0$) violates metric support. |
| **Loop 5.2 Ledger** | `reproduction_execution_ledger.csv` (Line 3) | *"violates bounded domain [0,1]"* | Replicated the false premise. |
| **Loop 5.2 Adjudication** | `final_loop5_2_adjudication.md` (Dim 4) | *"produce out-of-bounds intervals ([-0.1048, 1.0397] on Leukemia)"* | Fails to distinguish valid negative support from invalid upper-bound overflow. |
| **Loop 5.3 Review** | `reproduction_code_adversarial_review.md` (Item 2) | *"exceeds bounded domain [0,1]"* | Perpetuated the uncritical rejection of negative endpoints. |

---

## 4. Evaluative Decomposition of Confidence-Interval Procedures

### 4.1 Computable vs. Valid Coverage: The Student-$t$ Trap
A confidence interval formula can always be evaluated mechanically if $s > 0$ and $n \ge 2$:
$$\bar{x} \pm t_{1-\alpha/2, n-1} \frac{s}{\sqrt{n}}$$

However, **computability does not imply valid coverage**.
The derivation of the Student-$t$ distribution assumes:
1. $X_i \overset{\text{iid}}{\sim} \mathcal{N}(\mu, \sigma^2)$, with support on $(-\infty, +\infty)$.
2. The sample mean and sample variance are statistically independent (by Cochran's theorem).

On the Leukemia 5-seed sample:
$$\mathbf{x}_5 = [0.8376, \; 0.7868, \; 0.7868, \; -0.0290, \; -0.0446]$$
- The empirical data is **bimodally clustered**: three seeds succeed ($\approx 0.80$), two seeds fail ($\approx -0.03$).
- The data is heavily negatively skewed.
- The sample size is extremely small ($n=5$, $df=4$).
- The critical multiplier is large: $t_{0.975, 4} = 2.7764$.
- The resulting margin of error is $2.7764 \times 0.2061 = 0.5722$, producing:
  $$\text{Upper Limit} = 0.4675 + 0.5722 = 1.0397 > 1.0$$
- **Verdict on Student-$t$:** It is **UNSUITABLE**. The upper limit asserts a non-zero probability that the true mean exceeds perfect clustering, while the symmetric Gaussian model grossly misrepresents the bimodal initialization failure rate.

### 4.2 Bootstrap Resampling with Small Seed Counts ($n=10$)
When applying non-parametric bootstrap to $n=10$ observations:
$$\mathbf{x}_{10} = [-0.0290, \; 0.8376, \; 0.9442, \; 0.8376, \; 0.8376, \; 0.8376, \; 0.0192, \; 0.8376, \; 0.8900, \; 0.7868]$$

1. **Discrete Support Limitation:**
   Resampling $n=10$ observations with replacement yields $\binom{10 + 10 - 1}{10} = \binom{19}{10} = 92{,}378$ possible distinct bootstrap samples. While larger than $n=5$ ($\binom{9}{5} = 126$), the bootstrap distribution of the mean is dominated by how many times the two failure seeds ($-0.0290$ and $+0.0192$) are drawn.
2. **Percentile vs. BCa Intervals:**
   - **Percentile Bootstrap:** $95\% \text{ CI} = [0.4291, 0.8594]$.
     Simple and intuitive, strictly bounded within the convex hull of sample means, but assumes transformation-invariance.
   - **BCa (Bias-Corrected and Accelerated) Bootstrap:** $95\% \text{ CI} = [0.4086, 0.8535]$.
     Accounts for the negative skewness (the $20\%$ failure tail) and acceleration parameter.
3. **Severe Bimodality Precludes Smooth Inference:**
   Because 8 seeds succeed ($\bar{x}_{\text{succ}} \approx 0.85$) and 2 seeds fail ($\bar{x}_{\text{fail}} \approx -0.00$), the algorithm exhibits a **bimodal mixture distribution**.
   Resampling from a bimodal sample with $n=10$ produces an interval that characterizes the mixture uncertainty, but reporting a single mean ($0.680$) and symmetric-looking CI obscures the essential engineering reality: **the algorithm either solves the dataset with high accuracy ($0.84$) or fails completely ($0.00$) depending on initialization.**

---

## 5. The Core Inferential Question: What Does a 10-Seed Interval Actually Estimate?

In classical statistics, a $95\%$ confidence interval for an estimand $\theta$ asserts that under repeated sampling of cohorts from the population, $95\%$ of constructed intervals cover $\theta$.

For the 10-seed Leukemia benchmark:
- **Dataset is Fixed:** The cohort consists of the identical $N=72$ patients and $D=7{,}129$ microarray gene expressions in every single run.
- **Biological Variation is Zero:** No new patients, tissues, or sequencing batches are sampled.
- **Algorithmic Stochasticity is 100%:** The only quantity varying across seeds is the pseudorandom initialization of K-means anchors or projection matrices.

### Crucial Methodological Warning:
> A 10-seed bootstrap interval on a fixed dataset **estimates the mean performance of the randomized algorithm over its initialization distribution on that specific dataset**. It does NOT quantify generalization uncertainty to future biomedical cohorts.

Labeling this an "evaluation of model uncertainty" without qualification is a severe scientific error that misleads peer reviewers and clinical readers.

---

## 6. Definitive Scientific Presentation Recommendation for the Manuscript

For Springer Nature (DMKD) publication, we recommend:

1. **Primary Reporting: Descriptive Moments & Individual Seeds:**
   - Report the **Sample Median** ($0.838$) alongside the **Sample Mean** ($0.680$).
   - Report the **Sample Standard Deviation** ($0.363$).
   - Explicitly disclose the bimodal structure: 8 of 10 runs achieve ARI $\in [0.78, 0.94]$, while 2 runs fail near zero ($-0.03$ and $+0.02$).
2. **Confidence Interval (if reported):**
   - Use the **10-seed BCa bootstrap interval** ($[0.409, 0.853]$) or Percentile interval ($[0.429, 0.859]$).
   - Accompany the interval with this mandatory footnote:
     > *"Note: Confidence intervals across random seeds characterize algorithmic initialization stochasticity on the fixed cohort, not sampling uncertainty over new biomedical patient populations."*
3. **Expunge Erroneous Assertions:**
   - Remove all claims that negative ARI values are out-of-bounds.
   - Remove Student-$t$ intervals that violate the physical maximum upper bound of 1.0.
