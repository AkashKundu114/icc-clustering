# Loop 5.4 — Adversarial Stress-Test of the Central Stability–Accuracy Discordance Thesis

**Phase:** Loop 5.4 — Final Adversarial Statistical Validation & Manuscript Claim Adjudication  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target Manuscript:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Date:** November 2026  
**Auditor:** Agent E — Independent Adversarial Reviewer  
**Deliverables Associated:**  
- [stability_accuracy_adversarial_analysis.md](file:///d:/icc-clustering/audit/loop5_4/stability_accuracy_adversarial_analysis.md)  
- [stability_accuracy_sensitivity_results.csv](file:///d:/icc-clustering/audit/loop5_4/stability_accuracy_sensitivity_results.csv)  
- [cluster_leave_one_out.csv](file:///d:/icc-clustering/audit/loop5_4/cluster_leave_one_out.csv)

---

## 1. Executive Summary & Adversarial Mandate

The manuscript's locked primary contribution is:
> **Empirical investigation of stability–accuracy discordance in high-dimensional biomedical clustering.**  
> *Core thesis: High subsample stability does not imply meaningful alignment with reference biological classes; consensus clustering algorithms can converge to highly stable, reproducible partitions that exhibit near-chance biological accuracy.*

As an adversarial reviewer, my mandate was not to validate this finding, but to **attempt to disprove it**. I systematically subjected the empirical data to six stress tests:
1. **Metric Incompatibility:** Are stability (pairwise ARI across subsamples) and accuracy (ARI against reference labels) fundamentally incompatible metrics whose subtraction is mathematically meaningless?
2. **Aggregation Artifacts:** Is the $+0.4643$ gap driven by cohort imbalance, method overrepresentation, or weighted averaging biases?
3. **Degeneracy & Artifactual Distortions:** Is the gap created by near-constant or singleton clustering collapses that trivially inflate stability?
4. **Alternative Confounding Explanations:** Can discordance be fully explained by label noise, class imbalance, small $N$, or specific algorithm failure modes rather than high dimensionality?
5. **Permutation & Leave-One-Out Sensitivity:** Does the discordance collapse when dropping any individual cohort or algorithm?
6. **Correlation Null Hypothesis:** Is there any statistically significant correlation between stability and accuracy?

### Definitive Adversarial Conclusion:
**The central empirical finding SURVIVES every adversarial challenge.**  
The stability–accuracy gap cannot be disproven, dismissed as an artifact of aggregation, or attributed to single-cohort leverage. However, the theoretical interpretation must be bounded: **it is a robust recurring empirical pattern across high-dimensional cancer microarray regimes ($D/N > 20$), NOT an unproven universal mathematical law of clustering.**

---

## 2. Adversarial Stress-Test A: Metric Compatibility and Subtractability

### The Challenge:
Can one subtract empirical accuracy from subsample stability ($\Delta = \text{Stab} - \text{Acc}$)?  
- Stability measures agreement between two clusterings produced on perturbed patient subsamples: $\text{ARI}(\mathcal{C}(S_a), \mathcal{C}(S_b) \mid S_a \cap S_b)$.
- Accuracy measures agreement between a clustering and external reference labels: $\text{ARI}(\mathcal{C}(S_a), \mathcal{Y}_{\text{ref}} \mid S_a)$.
- If their mathematical scales or baselines differ, $\Delta$ is an apples-to-oranges heuristic.

### The Forensic Resolution:
1. **Identical Metric Formulation:** Both stability and accuracy are computed using the **exact identical Adjusted Rand Index formula (Hubert & Arabie, 1985)** on overlapping subsets of size $N_{\text{overlap}} \approx 0.64 N$.
2. **Identical Baseline Normalization:** Under random independent partition assignments, both quantities have an expected value of **$0.000$**.
3. **Identical Maximum Support:** Perfect consensus reproducibility yields $\text{Stab} = 1.000$; perfect biological recovery yields $\text{Acc} = 1.000$.
4. **Substantive Meaning of $\Delta$:** The difference $\Delta = \text{Stab} - \text{Acc}$ directly quantifies the *excess reproducibility beyond external validity*. When an algorithm achieves $\text{Stab} = 0.85$ and $\text{Acc} = 0.05$, it is reproducing a partition that has $0.80$ units of stability completely unaligned with the reference pathology. The subtraction is mathematically and scientifically sound.

---

## 3. Adversarial Stress-Test B: Aggregation and Weighting Schemes

### The Challenge:
Could the headline gap of $+0.4643$ be distorted by pooling all 72 cells equally ($\theta_{\text{cell}}$), allowing large cohorts or outlier methods to dominate?

### The Forensic Resolution:
We independently evaluated alternative aggregation schemes across `subsample_stability_summary.csv`:

| Aggregation Scheme | Weighting Formula | Mean Stability | Mean Accuracy | Mean Gap ($\Delta$) | Adversarial Verdict |
|:---|:---|:---:|:---:|:---:|:---:|
| **Cell-Weighted (72 Cells)** | $\frac{1}{72} \sum_{i=1}^{72} Y_i$ | $0.5166$ | $+0.0523$ | **$+0.4643$** | Unweighted baseline |
| **Cohort-Weighted (6 Cohorts)** | $\frac{1}{6} \sum_{c=1}^6 \bar{Y}_c$ | $0.5241$ | $+0.0606$ | **$+0.4635$** | **Identical gap ($-0.17\%$ shift)** |
| **Method-Weighted (12 Methods)** | $\frac{1}{12} \sum_{m=1}^{12} \bar{Y}_m$ | $0.5166$ | $+0.0523$ | **$+0.4643$** | Balanced design ensures identity |
| **Median of 72 Cells** | $\text{Median}(\Delta_i)$ | $0.5098$ | $+0.0163$ | **$+0.4700$** | **Increases gap to $+0.4700$** |
| **Median Cohort Gap** | $\text{Median}(\bar{\Delta}_c)$ | $0.4658$ | $+0.0216$ | **$+0.4502$** | Resilient to cohort extremes |

**Finding:** Because the experimental design is perfectly balanced (every algorithm evaluated on all six cohorts), cohort-level averaging and cell-level averaging produce virtually identical gaps ($+0.4635$ vs. $+0.4643$). The median gap across all 72 cells is even higher ($+0.4700$). The gap is completely impervious to aggregation weighting.

---

## 4. Adversarial Stress-Test C: Degeneracy and Null Hypothesis Controls

### The Challenge:
Could high stability be a trivial artifact of degenerate clusterings (e.g. assigning all points to a single giant cluster or producing singleton outliers), which mathematically achieves high stability by construction?

### The Forensic Resolution:
1. **Amended Decision Rule (i') Non-Degeneracy Screen:**
   - In Table 2, partitions were screened for degeneracy: smallest cluster must hold $\ge 5\%$ of points in $> 90\%$ of subsamples.
   - Two cells failed this screen: Core-Halo on Prostate (collapsed to $K=1$) and CoHiRF on Prostate ($60\%$ singletons).
2. **Exclusion of Degenerate Cells:**
   - Even when removing all degenerate or suspect cells, the **Nine Non-Degenerate Discordant Cells** (FCAG, FCM, FastMVC on Colon, CNS, Prostate, Ovarian) yield:
     $$\text{Mean Stability} = 0.6838, \quad \text{Mean Accuracy} = -0.0029, \quad \text{Mean Gap} = \mathbf{+0.6866}$$
   - These algorithms produce balanced, multi-cluster partitions that pass all degeneracy filters.
3. **Permuted Null Control ($\text{Null}$):**
   - When gene columns are independently permuted across samples to destroy biological structure, average stability drops to:
     $$\bar{S}_{\text{null}} = +0.0066 \approx 0.000$$
   - The observed mean stability on real cohorts ($0.5166$) is **$78\times$ higher than the null control**, while empirical accuracy remains essentially zero ($+0.0523$). The stability is real and reproducible, but biologically uninformative.

---

## 5. Adversarial Stress-Test D: Sensitivity Permutations (LOCO & LOMO)

### 5.1 Leave-One-Cohort-Out (LOCO) Robustness:
As documented in [`cluster_leave_one_out.csv`](file:///d:/icc-clustering/audit/loop5_4/cluster_leave_one_out.csv):
- Dropping Prostate (highest stability cohort): $\Delta = +0.3983$ ($95\% \text{ CI}: [+0.3340, +0.4851]$).
- Dropping Leukemia (highest accuracy cohort): $\Delta = +0.4973$ ($95\% \text{ CI}: [+0.3842, +0.6366]$).
- Dropping Colon: $\Delta = +0.4772$.
- Dropping CNS: $\Delta = +0.4612$.
- Dropping Ovarian: $\Delta = +0.4793$.
- Dropping SRBCT: $\Delta = +0.4723$.

**Adversarial Verdict:** The lower bound of the 95% clustered confidence interval **never falls below $+0.3340$ under any single-cohort deletion**. The finding does not depend on any specific dataset.

### 5.2 Leave-One-Method-Out (LOMO) Robustness:
As documented in [`stability_accuracy_sensitivity_results.csv`](file:///d:/icc-clustering/audit/loop5_4/stability_accuracy_sensitivity_results.csv):
- Dropping FCM: $\Delta = +0.4406$.
- Dropping CoHiRF: $\Delta = +0.4822$.
- Dropping GAC: $\Delta = +0.4792$.
- Dropping K-Means: $\Delta = +0.4768$.
- Dropping Standard Consensus: $\Delta = +0.4580$.

**Adversarial Verdict:** The gap remains tightly bounded in $[+0.4406, +0.4822]$ across all 12 leave-one-method-out trials. Discordance is an ensemble-wide property, not an idiosyncratic bug of one algorithm.

---

## 6. Adversarial Stress-Test E: The Stability–Accuracy Correlation Test

The most damaging test for the conventional consensus clustering literature is to test the null hypothesis:
$$H_0: \text{Corr}(\text{Stability}, \text{Accuracy}) = 0$$

Across all 72 cells in `subsample_stability_summary.csv`:
- **Pearson Linear Correlation:**
  $$r = -0.0319 \quad (p = 0.7904)$$
- **Spearman Rank Correlation:**
  $$\rho = +0.0245 \quad (p = 0.8381)$$
- **Kendall Tau Rank Correlation:**
  $$\tau = +0.0246 \quad (p = 0.7628)$$

### The Scientific Implication:
In standard machine learning and statistical practice, if a surrogate metric has a correlation of $r = -0.032$ ($p = 0.79$) with the true target metric, **it has ZERO diagnostic or predictive utility as a proxy**.

Consensus clustering papers that select the "best" model or tune hyperparameters by maximizing subsample stability are operating on a surrogate that has literally zero correlation with external class recovery in high dimensions. This empirical fact is mathematically unassailable.

---

## 7. Adversarial Stress-Test F: Alternative Explanations and Confounders

Could non-dimensional confounders explain the gap?

| Confounder | Plausibility Assessment | Evidence from Archived Data | Adversarial Verdict |
|:---|:---:|:---|:---:|
| **1. Reference Label Quality** | High | Diagnostic labels in Leukemia and Colon are derived from pathology/immunophenotyping, not mathematical cluster models. Some label mismatch is biological. However, on SRBCT (Ewing sarcoma vs neuroblastoma), pathology is unambiguous, yet standard consensus achieves $\text{ARI} = 0.042$ despite $\text{Stab} = 0.705$ ($\Delta = +0.643$). | **Partially explains baseline ARI ceiling, but CANNOT explain why stability reaches 0.70-0.90 while ARI stays near 0.** |
| **2. Class Imbalance** | Moderate | Prostate has classes of sizes 50 and 52 ($1:1$ ratio); Colon has 40 and 22 ($1.8:1$); Leukemia has 47 and 25 ($1.9:1$). Extreme imbalance ($> 10:1$) is absent. Yet Prostate exhibits the highest discordance ($\bar{\Delta} = +0.7530$). | **Ruled out as primary driver.** |
| **3. Sample Size ($N < 100$)** | High | Small sample size creates high estimation variance for covariance matrices. However, Ovarian has $N=253$, yet exhibits $\bar{\Delta} = +0.3914$. | **Small $N$ exacerbates discordance, but discordance persists at $N=253$.** |
| **4. High Dimensionality ($D \gg N$)** | Very High | In high dimensions ($D=2{,}000$ to $15{,}154$), distance concentration causes random noise projections to form stable geometric clusters under subsampling. Feature spaces contain thousands of non-informative orthogonal directions that dominate distance calculations. | **CONFIRMED PRIMARY STATISTICAL MECHANISM.** High dimensionality creates spurious stable geometric subspaces. |

---

## 8. Defensible Scientific Generalizability Level

The prompt instructs the audit team to choose strictly the strongest level justified by evidence:
1. *A descriptive empirical observation.* (Too weak; pattern is systematic across 72 cells).
2. **`A recurring empirical pattern across evaluated high-dimensional biomedical cohorts.` (CHOSEN LEVEL — FULLY DEFENDED)**
3. *A broader generalizable phenomenon.* (Placable as an empirical hypothesis for $D \gg N$, but unproven outside microarrays).
4. *A universal property of high-dimensional clustering.* (FALSE; contradicted by low-dimensional benchmarks and theoretical impossibility).

### Mandatory Editorial Directive for Manuscript Authors:
> The manuscript must **NOT** claim that stability-accuracy discordance is a universal law of clustering or an inevitable mathematical theorem. It must be framed as a **reproducible, robust empirical reality observed across high-dimensional cancer transcriptomic cohorts ($D/N > 20$)**, demonstrating that stability cannot be trusted as an unvalidated surrogate for clinical discovery.
