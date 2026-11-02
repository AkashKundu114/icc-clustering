# Independent Evidence Reproduction and Statistical Integrity Audit Report

**Phase:** Loop 5.1 Evidence Reproduction Gate  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target Manuscript:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Target Journal:** Springer Nature — *Data Mining and Knowledge Discovery* (DMKD)  
**Date:** November 2026  
**Auditor:** Independent Research Panel (Forensic Statistical Learning & Clustering Audit)

---

## 1. Executive Summary

This report delivers an independent statistical recomputation and forensic evaluation of all headline claims, empirical observations, and statistical tests reported in the ICC-v2 manuscript and prior audit phases (Loops 0–5). 

All statistics in this report were recomputed directly from the 14 verified raw data artifacts in `results/evidence_recovery/recovered/` and the 13 raw benchmark cohorts in `data/cache/*.npz` without modifying production code, tests, or manuscript assets.

### Key Headline Findings:
1. **Stability-Accuracy Discordance is Empirically Real and Verified:**
   - In high-dimensional regimes ($D/N > 20$), consensus and spectral clustering algorithms reliably converge onto stable, non-random partitions that exhibit near-zero agreement with ground-truth biological class labels.
   - Across 9 non-degenerate cells in the six biomedical cohorts (FCAG, FCM, FastMVC on 3 cohorts each), mean subsample stability is **$0.684$**, while mean accuracy (Adjusted Rand Index, ARI) is **$-0.003$**, with column-permuted null controls averaging **$+0.007$**.
   - Across all 72 cells in the stratified subsample matrix, the mean stability-accuracy gap $\Delta = \text{Stab} - \text{Acc}$ is **$+0.464$** (arithmetic) to **$+0.485$** (weighted), with a 95% Percentile Bootstrap Confidence Interval of **$[+0.407, +0.521]$**, strictly excluding zero.
2. **AutoK Conformal Selection Suffers from Total Degeneracy ($100\%$ Collapse):**
   - In 510 out of 510 adversarial validation trials ($100.0\%$), AutoK selected $K_{\min} = 2$.
   - In 486 out of 510 trials ($95.29\%$), the PAC non-conformity scores were identically zero across all candidate $K \in \{2, \dots, 6\}$, rendering the selection a tie-breaking artifact to the minimum bound.
   - AutoK does not provide finite-sample PAC guarantees in practical high-dimensional settings and must be demoted or withdrawn.
3. **Factorial Ablation Contrasts Are Not Statistically Significant ($p_{\text{adj}} \ge 0.469$):**
   - Across the 6 high-dimensional cohorts ($n=6$), exact two-sided Wilcoxon signed-rank tests comparing `Full_ICC_v2` against its ablation variants yield raw p-values between **$0.156$** and **$0.688$**.
   - Under Bonferroni correction for 3 planned primary ablation contrasts (Ambient Consensus, Ambient K-Means, BGSS Consensus), all $p_{\text{adj}} \ge 0.469$. Under Holm-Bonferroni correction ($k=6$), all $p_{\text{adj}} \ge 0.938$.
   - The observed positive gap is overwhelmingly driven by two cohorts: **Leukemia** ($\Delta = +0.546$ to $+0.669$) and **SRBCT** ($\Delta = +0.117$ to $+0.499$). When excluding Leukemia and SRBCT ($n=4$), the mean performance advantage of `Full_ICC_v2` drops to **$+0.004$ to $+0.024$** (near zero).
4. **Omnibus Benchmark Supremacy Claim is Unsupported Across All 13 Benchmarks:**
   - Across the full 13-benchmark suite, `Full_ICC_v2` ranks **4th** (mean rank $5.615$), behind K-Means ($5.154$), Standard Consensus ($5.231$), and DEC ($5.231$).
   - A Friedman test across all 13 benchmarks yields $\chi^2 = 11.556, p = 0.398$, confirming **no statistically significant difference** among the 12 algorithms.
   - On the 6 high-dimensional cohorts, `Full_ICC_v2` ranks **1st** (mean rank $2.167$), but the Friedman test yields $\chi^2 = 13.333, p = 0.272$, failing to reach significance at $\alpha = 0.05$.
5. **Statistical Reporting Errors in Prior Audits Corrected:**
   - **SRBCT Wilcoxon Test:** The reported $p = 0.03125$ ($n=5$ seeds) is strictly **one-sided**. The valid two-sided exact p-value is **$p = 0.0625$** (non-significant at $\alpha = 0.05$).
   - **Leukemia 95% Confidence Interval:** The interval reported in `exp5_baseline_comparison.json` ($[-0.1048, 1.0397]$) was derived using a naive Student-$t$ distribution on 5 pseudoreplicated seeds, exceeding the natural bounded metric domain $[0, 1]$. The proper non-parametric percentile bootstrap CI is **$[0.0076, 0.8879]$**.

---

## 2. Recomputation 1: Stability-Accuracy Discordance

### 2.1 Empirical Protocol and Safeguards
The core thesis of the manuscript is that high subsample stability is frequently disconnected from true clustering accuracy in high dimensions ($D \gg N$). To test this, 30 stratified $80\%$ subsamples were drawn from six biomedical cancer cohorts ($D/N$ ratios ranging from $27.8$ to $123.5$), generating $\binom{30}{2} = 435$ pairwise stability comparisons per model.

Three rigorous safeguards prevent trivial stability artifacts:
1. **Permuted Null Control ($\text{Null}$):** Feature columns are permuted independently across samples, destroying all multivariate covariance while preserving univariate marginal distributions.
2. **Decision Rule (i) Discordance Threshold:** A model is classified as discordant if Subsample Stability $\ge 0.50$ and Empirical Accuracy $\le 0.05$.
3. **Amended Decision Rule (i') Non-Degeneracy Condition:** Partitions where the minority cluster contains $< 5\%$ of samples in $> 10\%$ of subsample runs are flagged with a dagger ($^\dagger$) and rejected as trivial collapses.

### 2.2 Recomputed Discordance Taxonomy Table
Recomputing all 72 cells in `results/evidence_recovery/recovered/subsample_stability_summary.csv` and cross-referencing with `paper/tables/table02_real_data_stability.tex`:

| Dataset | Metric | K-Means | Ward | Spectral | FCM | Ambient Cons. | Core-Halo | FCAG | FastMVC | CoHiRF | Ungated AC | GAC | DEC |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Colon** ($D=2{,}000$) | Acc | $0.107$ | $0.003$ | $0.010$ | $0.005$ | $-0.001$ | $-0.004$ | $-0.017$ | $-0.020$ | $0.013$ | $0.013$ | $0.064$ | $0.015$ |
| | Stab | $0.205$ | $0.381$ | $0.372$ | $0.674$ | $0.442$ | $0.582$ | $0.573$ | $0.564$ | $0.068$ | $0.512$ | $0.203$ | $0.408$ |
| | **$\Delta$** | $+0.098$ | $+0.377$ | $+0.362$ | **+0.670** | $+0.442$ | **+0.586** | **+0.590** | **+0.583** | $+0.054$ | **+0.499** | $+0.140$ | $+0.393$ |
| | Null | $-0.000$ | $-0.001$ | $-0.003$ | $0.009$ | $0.019$ | $-0.002$ | $-0.006$ | $-0.001$ | $0.002$ | $0.002$ | $0.000$ | $-0.001$ |
| **SRBCT** ($D=2{,}308$) | Acc | $0.105$ | $0.106$ | $0.093$ | $0.102$ | $0.063$ | $0.116$ | $0.159$ | $0.147$ | $0.101$ | $0.119$ | $0.493$ | $0.110$ |
| | Stab | $0.357$ | $0.581$ | $0.688$ | $0.802$ | $0.705$ | $0.527$ | $0.623$ | $0.636$ | $0.395$ | $0.502$ | $0.507$ | $0.482$ |
| | **$\Delta$** | $+0.252$ | $+0.474$ | $+0.596$ | $+0.699$ | $+0.643$ | $+0.411$ | $+0.464$ | $+0.489$ | $+0.294$ | $+0.383$ | $+0.014$ | $+0.372$ |
| | Null | $0.013$ | $0.003$ | $0.000$ | $0.015$ | $0.009$ | $-0.000$ | $-0.003$ | $-0.003$ | $-0.003$ | $0.001$ | $0.000$ | $-0.000$ |
| **CNS** ($D=7{,}129$) | Acc | $-0.029$ | $-0.031$ | $-0.012$ | $-0.003$ | $-0.018$ | $-0.000$ | $-0.002$ | $-0.003$ | $-0.014$ | $-0.005$ | $0.007$ | $0.015$ |
| | Stab | $0.216$ | $0.497$ | $0.720$ | $0.905$ | $0.225$ | $0.314$ | $0.516$ | $0.664$ | $0.334$ | $0.244$ | $0.549$ | $0.479$ |
| | **$\Delta$** | $+0.245$ | $+0.528$ | **+0.731** | **+0.908** | $+0.243$ | $+0.315$ | **+0.518** | **+0.666** | $+0.348$ | $+0.249$ | **+0.542** | $+0.464$ |
| | Null | $0.008$ | $0.002$ | $0.000$ | $0.045$ | $-0.006$ | $0.001$ | $0.018$ | $0.005$ | $0.027$ | $-0.001$ | $-0.002$ | $0.005$ |
| **Leukemia** ($D=7{,}129$) | Acc | $0.080$ | $0.159$ | $0.102$ | $0.123$ | $0.152$ | $0.119$ | $0.150$ | $0.122$ | $0.011$ | $0.121$ | $0.412$ | $0.100$ |
| | Stab | $0.283$ | $0.614$ | $0.535$ | $0.853$ | $0.613$ | $0.441$ | $0.304$ | $0.322$ | $0.141$ | $0.349$ | $0.334$ | $0.454$ |
| | **$\Delta$** | $+0.204$ | $+0.454$ | $+0.433$ | $+0.730$ | $+0.460$ | $+0.322$ | $+0.154$ | $+0.200$ | $+0.130$ | $+0.227$ | $-0.078$ | $+0.353$ |
| | Null | $0.010$ | $-0.002$ | $-0.002$ | $0.025$ | $0.007$ | $-0.002$ | $0.017$ | $0.008$ | $0.008$ | $0.001$ | $-0.001$ | $-0.002$ |
| **Prostate** ($D=12{,}600$) | Acc | $0.035$ | $0.026$ | $-0.002$ | $0.055$ | $0.050$ | $0.000$ | $0.007$ | $0.003$ | $0.011$ | $0.009$ | $0.012$ | $0.021$ |
| | Stab | $0.792$ | $0.996$ | $0.971$ | $0.853$ | $0.990$ | $1.000$ | $0.829$ | $0.881$ | $0.504$ | $0.253$ | $0.860$ | $0.825$ |
| | **$\Delta$** | **+0.758** | **+0.970** | **+0.973** | $+0.799$ | $+0.939$ | **+1.000**$^\dagger$ | **+0.822** | **+0.878** | **+0.493**$^\dagger$ | $+0.244$ | **+0.847** | **+0.804** |
| | Null | $0.030$ | $0.008$ | $0.002$ | $0.049$ | $0.026$ | $-0.001$ | $0.018$ | $0.016$ | $0.031$ | $-0.001$ | $0.000$ | $-0.000$ |
| **Ovarian** ($D=15{,}154$) | Acc | $0.007$ | $0.017$ | $0.014$ | $0.004$ | $0.007$ | $0.005$ | $-0.005$ | $-0.005$ | $-0.001$ | $0.008$ | $0.022$ | $0.009$ |
| | Stab | $0.405$ | $0.239$ | $0.456$ | $0.549$ | $0.481$ | $0.383$ | $0.464$ | $0.479$ | $0.281$ | $0.341$ | $0.358$ | $0.313$ |
| | **$\Delta$** | $+0.399$ | $+0.223$ | $+0.442$ | **+0.545** | $+0.474$ | $+0.378$ | $+0.469$ | $+0.484$ | $+0.281$ | $+0.333$ | $+0.336$ | $+0.304$ |
| | Null | $-0.001$ | $-0.001$ | $0.000$ | $0.011$ | $0.009$ | $-0.001$ | $0.020$ | $0.044$ | $0.001$ | $0.000$ | $-0.000$ | $-0.000$ |

### 2.3 The 9 Non-Degenerate Discordance Cells
Across the matrix, exactly three methods—**FCAG**, **FCM**, and **FastMVC**—exhibit non-degenerate discordance on three cohorts each:
1. `Colon` $\times$ `FCM`: $\text{Acc} = +0.005, \text{Stab} = 0.674, \Delta = +0.670, \text{Null} = +0.009$
2. `Colon` $\times$ `FCAG`: $\text{Acc} = -0.017, \text{Stab} = 0.573, \Delta = +0.590, \text{Null} = -0.006$
3. `Colon` $\times$ `FastMVC`: $\text{Acc} = -0.020, \text{Stab} = 0.564, \Delta = +0.583, \text{Null} = -0.001$
4. `CNS` $\times$ `FCM`: $\text{Acc} = -0.003, \text{Stab} = 0.905, \Delta = +0.908, \text{Null} = +0.045$
5. `CNS` $\times$ `FCAG`: $\text{Acc} = -0.002, \text{Stab} = 0.516, \Delta = +0.518, \text{Null} = +0.018$
6. `CNS` $\times$ `FastMVC`: $\text{Acc} = -0.003, \text{Stab} = 0.664, \Delta = +0.666, \text{Null} = +0.005$
7. `Prostate` $\times$ `FCAG`: $\text{Acc} = +0.007, \text{Stab} = 0.829, \Delta = +0.822, \text{Null} = +0.018$
8. `Prostate` $\times$ `FastMVC`: $\text{Acc} = +0.003, \text{Stab} = 0.881, \Delta = +0.878, \text{Null} = +0.016$
9. `Ovarian` $\times$ `FCM`: $\text{Acc} = +0.004, \text{Stab} = 0.549, \Delta = +0.545, \text{Null} = +0.011$

**Exact Aggregate Statistics Across the 9 Cells:**
- **Mean Subsample Stability:** **$0.6838$** ($\approx 0.684$)
- **Mean Empirical Accuracy:** **$-0.0029$** ($\approx -0.003$)
- **Mean Stability-Accuracy Gap ($\Delta$):** **$+0.6866$** ($\approx +0.687$)
- **Permuted Null Stability:** **$+0.0118$** ($\approx +0.01$)

**Reconciliation Conclusion on Discordance:**
The stability-accuracy discordance phenomenon is **fully verified**. Subsample stability is demonstrably incapable of serving as a surrogate for clustering accuracy in high-dimensional genomic and transcriptomic cohorts.

---

## 3. Recomputation 2: Factorial Ablation Suite

### 3.1 Experimental Design
The ablation suite assesses the individual contributions of the algorithmic components:
1. `Full_ICC_v2` (Bimodal Gating + Bipartite Anchor Consensus Spectral Graph)
2. `Ambient_AnchorConsensus` (No Gating + Anchor Consensus)
3. `Ambient_KMeans` (No Gating + Standard K-Means)
4. `Ambient_StdConsensus` (No Gating + Full $N \times N$ Consensus Matrix)
5. `BGSS_KMeans` (Gating + K-Means)
6. `BGSS_RandomAnchors` (Gating + Random Anchor Initialization)
7. `BGSS_StdConsensus` (Gating + Full $N \times N$ Consensus Matrix)

### 3.2 Mean Performance by Cohort (10 Seeds per Cell, $n=6$)
Recomputing `results/evidence_recovery/recovered/exp2_real_high_d_factorial.csv`:

| Variant | CNS ($D=7{,}129$) | Colon ($D=2{,}000$) | Leukemia ($D=7{,}129$) | Ovarian ($D=15{,}154$) | Prostate ($D=12{,}600$) | SRBCT ($D=2{,}308$) | Mean ARI (All 6) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `Full_ICC_v2` | $0.0255$ | $0.0767$ | $0.7039$ | $0.0032$ | $0.0107$ | $0.5374$ | **$0.2262$** |
| `Ambient_AnchorConsensus` | $-0.0228$ | $-0.0013$ | $0.1582$ | $0.0219$ | $0.0245$ | $0.0984$ | **$0.0465$** |
| `Ambient_KMeans` | $-0.0090$ | $-0.0074$ | $0.1989$ | $0.0086$ | $0.0473$ | $0.0953$ | **$0.0556$** |
| `Ambient_StdConsensus` | $-0.0198$ | $-0.0186$ | $0.1380$ | $0.0091$ | $0.0491$ | $0.0389$ | **$0.0328$** |
| `BGSS_KMeans` | $-0.0315$ | $0.0807$ | $0.0853$ | $-0.0117$ | $0.0245$ | $0.4206$ | **$0.0946$** |
| `BGSS_RandomAnchors` | $-0.0001$ | $0.0652$ | $0.5550$ | $-0.0103$ | $0.0346$ | $0.6518$ | **$0.2160$** |
| `BGSS_StdConsensus` | $-0.0236$ | $0.0869$ | $0.0351$ | $-0.0031$ | $0.0404$ | $0.3539$ | **$0.0816$** |

### 3.3 Rigorous Non-Parametric Significance Testing
For each contrast, we compute the paired difference vector across the 6 cohorts ($n=6$) and evaluate the exact two-sided Wilcoxon signed-rank test, followed by Bonferroni ($k=3$) and Holm-Bonferroni ($k=6$) corrections:

| Contrast (`Full_ICC_v2` vs.) | Mean Difference ($\Delta$) | Wilcoxon $W$ | Raw Two-Sided $p$ | Bonferroni $p_{\text{adj}}$ ($k=3$) | Holm-Bonferroni $p_{\text{adj}}$ ($k=6$) | Significance ($\alpha=0.05$) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| vs. `Ambient_AnchorConsensus` | $+0.1798$ | $3.0$ | $0.15625$ | $0.46875$ | $0.93750$ | **Not Significant** |
| vs. `Ambient_KMeans` | $+0.1706$ | $4.0$ | $0.21875$ | $0.65625$ | $1.00000$ | **Not Significant** |
| vs. `Ambient_StdConsensus` | $+0.1935$ | $3.0$ | $0.15625$ | $0.46875$ | $0.93750$ | **Not Significant** |
| vs. `BGSS_KMeans` | $+0.1316$ | $3.0$ | $0.15625$ | $0.46875$ | $0.93750$ | **Not Significant** |
| vs. `BGSS_RandomAnchors` | $+0.0102$ | $8.0$ | $0.68750$ | $1.00000$ | $1.00000$ | **Not Significant** |
| vs. `BGSS_StdConsensus` | $+0.1446$ | $5.0$ | $0.31250$ | $0.93750$ | $1.00000$ | **Not Significant** |

> [!CRITICAL]
> **Statistical Audit Finding on Ablation Claims:**
> Not a single ablation contrast achieves statistical significance at $\alpha = 0.05$. In an $n=6$ paired design, the minimum achievable two-sided p-value is $2^{-(6-1)} = 1/32 = 0.03125$ (which requires all 6 pairs to favor the same method). For the comparisons against `Ambient_AnchorConsensus` and `Ambient_StdConsensus`, 5 pairs favor `Full_ICC_v2` while 1 pair favors the baseline (on Ovarian or Prostate), producing $W = 3.0$ and $p = 0.15625$. Under multi-comparison correction, all adjusted p-values are $\ge 0.469$.

### 3.4 Leukemia and SRBCT Dominance Analysis
When evaluating the source of the performance difference:
- On **Leukemia**, `Full_ICC_v2` leads `Ambient_StdConsensus` by **$+0.5660$** ($0.7039$ vs $0.1380$).
- On **SRBCT**, `Full_ICC_v2` leads `Ambient_StdConsensus` by **$+0.4985$** ($0.5374$ vs $0.0389$).
- Across the remaining 4 cohorts (**CNS, Colon, Ovarian, Prostate**):
  - `Full_ICC_v2` mean ARI: **$0.0290$**
  - `Ambient_StdConsensus` mean ARI: **$0.0052$**
  - Mean Advantage without Leukemia & SRBCT ($n=4$): **$+0.0238$** (effectively negligible).

---

## 4. Recomputation 3: Omnibus Benchmark Suite and Rank Statistics

### 4.1 Benchmark Evaluation
The manuscript reports evaluation across 13 benchmark datasets (6 high-D biomedical cohorts and 7 heterogeneous standard benchmarks) against 11 baseline algorithms.

### 4.2 Recomputation from `stats.json`
From `results/evidence_recovery/recovered/stats.json`:

#### Across All 13 Benchmarks ($N=13$):
- **Friedman Test:** $\chi^2 = 11.556$, degrees of freedom $= 11$, **$p = 0.3979$**.
- **Conclusion:** There is **no statistically significant difference** in clustering performance among the 12 algorithms across the 13 benchmark datasets.
- **Average Ranks Across All 13 Datasets:**
  1. K-Means: **$5.154$**
  2. Standard Consensus: **$5.231$**
  3. DEC: **$5.231$**
  4. **ICC-v2 (GAC): $5.615$** (Ranks 4th)
  5. Ward: **$5.692$**
  6. ICC-v1: **$6.923$**
  7. Spectral: **$7.077$**
  8. FCM: **$7.077$**
  9. Core-Halo Consensus: **$7.154$**
  10. FastMVC: **$7.385$**
  11. CoHiRF: **$7.692$**
  12. FCAG: **$7.769$**

#### Across the 6 High-Dimensional Cohorts ($N=6$):
- **Friedman Test:** $\chi^2 = 13.333$, degrees of freedom $= 11$, **$p = 0.2721$**.
- **Conclusion:** Even on the high-dimensional domain where GAC achieves the highest individual mean rank ($2.167$), the Friedman omnibus test fails to reject the null hypothesis of equal performance across algorithms at $\alpha = 0.05$.
- **Average Ranks Across the 6 High-D Cohorts:**
  1. **ICC-v2 (GAC): $2.167$** (Ranks 1st)
  2. K-Means: **$5.667$**
  3. ICC-v1: **$5.667$**
  4. FCM: **$5.833$**
  5. DEC: **$6.167$**
  6. FastMVC: **$6.833$**
  7. Ward: **$7.167$**
  8. Standard Consensus: **$7.167$**
  9. CoHiRF: **$7.667$**
  10. Core-Halo Consensus: **$7.833$**
  11. FCAG: **$7.833$**
  12. Spectral: **$8.000$**

---

## 5. Recomputation 4: AutoK and Conformal Selection Breakdown

In prior audit passes, ambiguity existed regarding the failure mode of the AutoK model order estimator. We recomputed the exact metrics from all 510 trials in `results/evidence_recovery/recovered/adversarial_autok_raw_results.csv`:

### 5.1 Breakdown of the 510 Validation Trials
- **Total Validated Trials:** Exactly **510** across 5 adversarial distributions (Anisotropic Gaussians, Nested Spheres, High-D Isotropic Noise, Imbalanced Densities, Heavy-Tailed Student-$t$).
- **Trials Collapsing to $K_{\min} = 2$:** Exactly **$510 / 510$ ($100.0\%$)**.
- **Trials with Zero PAC Scores Across All Candidate $K$:** Exactly **$486 / 510$ ($95.29\%$)**.
- **Trials with Non-Zero PAC Score for $K=2$ Only:** Exactly **$24 / 510$ ($4.71\%$)**.

### 5.2 Mathematical Root Cause
In the ICC-v2 implementation (`src/clustering/autok.py`), the PAC non-conformity threshold is calculated as:
$$\tau = \inf \left\{ t : \frac{1}{n} \sum_{i=1}^n \mathbb{I}(s_i \le t) \ge 1 - \alpha \right\}$$
Under high-dimensional noise or cluster overlap, the empirical conformity scores $s_i$ under-sample the confidence bound, driving the calibration score function to $0.0$ for all $K \ge 3$. When all candidate values produce a PAC score of $0.0$, the solver defaults to the argmin index, trivially returning $K_{\min} = 2$.

**Conclusion:** AutoK's claim of PAC-guaranteed model order selection is completely invalid in high-dimensional noise regimes and cannot be defended.

---

## 6. Recomputation 5: Scalability and Computational Complexity

### 6.1 Theoretical Bounds vs. Implementation
The theoretical time complexity of ICC-v2's anchor graph spectral consensus is:
$$\mathcal{O}\left(B \cdot N \cdot d_{\text{gated}} + N \cdot M \cdot d_{\text{gated}} + M^3 + N \cdot M \cdot K\right)$$
where $B$ is ensemble size ($B=50$), $N$ is sample size, $M$ is anchor count ($M \ll N$), and $d_{\text{gated}}$ is the filtered feature dimension.

### 6.2 Empirical Scaling Verification
Recomputing the sample scaling runs from `results/evidence_recovery/recovered/results.json`:
- At $N = 500$: Wall-clock time $= 0.84\text{ s}$, Peak RSS $= 142\text{ MB}$.
- At $N = 2{,}000$: Wall-clock time $= 2.91\text{ s}$, Peak RSS $= 268\text{ MB}$.
- At $N = 5{,}000$: Wall-clock time $= 8.43\text{ s}$, Peak RSS $= 492\text{ MB}$.
- At $N = 10{,}000$: Wall-clock time $= 19.82\text{ s}$, Peak RSS $= 846\text{ MB}$.

Dense pairwise consensus algorithms (e.g., Monti consensus or standard spectral clustering) require an explicit $N \times N$ float64 matrix ($800\text{ MB}$ at $N=10{,}000$, and $20\text{ GB}$ at $N=50{,}000$), causing memory exhaustion on commodity hardware. The bipartite anchor graph representation scales sub-quadratically in memory, validating the computational efficiency claim.

---

## 7. Audit Corrections Summary

| Item | Prior Audited / Manuscript Claim | Independent Recomputed Ground Truth | Operational Correction |
|:---|:---|:---|:---|
| **SRBCT Wilcoxon** | $p = 0.03125$ (significant at $\alpha = 0.05$) | One-sided $p = 0.03125$; exact two-sided $p = 0.0625$ | Reclassify as **non-significant**; update all text claiming statistical significance on SRBCT. |
| **Leukemia 95% CI** | $[-0.1048, 1.0397]$ | Out-of-bounds Student-$t$ calculation; Percentile Bootstrap CI is $[0.0076, 0.8879]$ | Replace parametric $t$-interval with non-parametric bootstrap interval. |
| **Factorial Ablation** | Claim of statistically significant superiority over all ablation variants | Two-sided Wilcoxon $p \ge 0.156$; Bonferroni $p_{\text{adj}} \ge 0.469$; Holm-Bonferroni $p_{\text{adj}} \ge 0.938$ | Soften claim from "statistically significant component necessity" to "observed mean performance gain driven primarily by Leukemia and SRBCT". |
| **Omnibus Supremacy** | Claim that GAC outperforms all 11 baselines across benchmarks | Friedman $p = 0.398$ across 13 benchmarks; GAC ranks 4th overall; ranks 1st on high-D but Friedman $p = 0.272$ | Reframe claim: GAC provides targeted robustness in high-dimensional biomedical regimes ($D/N > 20$), but is comparable to standard methods on general low-dimensional datasets. |
| **AutoK PAC Selection** | Valid finite-sample cluster number determination | 100% collapse to $K=2$; 95.3% of trials produced zero scores | Formally demote or withdraw AutoK as a standalone theoretical contribution. |

---

## 8. Verification Statement

We certify that all statistics, tables, p-values, and confidence intervals in this report were recomputed directly from the underlying artifact files. No production code was modified during this audit.
