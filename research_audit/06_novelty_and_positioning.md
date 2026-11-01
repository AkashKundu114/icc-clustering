# Research Audit 06: Novelty, Positioning, and Scientific Contribution for DMKD

**Target Journal:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Document Reference:** `AUDIT-06-DMKD-POSITIONING`  
**Date:** 2026-10-31  

---

## 1. Reframing the Central Scientific Contribution

### 1.1 Why the Previous "Universal Superiority" Framing Was Unsound
Earlier informal working drafts of the manuscript carried claims of broad algorithmic superiority. However, the repository's own rigorous empirical audits refute that framing:
1. Across the 13 multi-domain benchmark cohorts, the 12 evaluated methods are statistically indistinguishable (Omnibus Friedman test: $p = 0.40, \text{CD} = 4.62$).
2. The $+0.169$ gain of Bimodality-Gated Subspace Selection (BGSS) under bipartite consensus is concentrated in two cohorts (Leukemia $+0.398$, SRBCT $+0.447$), while the other four cohorts show minimal change ($+0.004$ to $+0.078$).
3. Under dense consensus, BGSS adds only $+0.031$, confounded by a degenerate cluster collapse on Leukemia.
4. Determinacy-based core anchor selection yields no measurable advantage over uniform random landmark sampling ($\Delta = +0.019, 95\%\text{ CI } [-0.040, +0.082], p = 0.84$).

### 1.2 The Defensible Central Contribution for DMKD
The strongest, most defensible, and high-impact contribution for DMKD is:

> **A systematic, statistically defensible framework for diagnosing stability–accuracy discordance in high-dimensional consensus clustering, identifying the conditions under which stable partitions fail to recover externally validated structure, and determining when feature gating and anchor-based consensus can or cannot mitigate that failure.**

Rather than marketing an algorithm as an infallible panacea, the manuscript provides a critical methodological and empirical service to the data mining community:
- **Exposing the Stability–Accuracy Discordance Trap:** Proving that high subsample stability (the standard metric used in bioinformatics and computational oncology to certify cluster reliability) routinely co-exists with near-zero agreement with diagnostic reference labels ($\text{ARI} \le 0.05$).
- **Characterizing the Failure Modes:** Showing that stable discordant partitions latch onto dominant technical nuisance axes (library size, total expression, PCA outliers) rather than target pathology.
- **Delineating Algorithmic Boundaries:** Providing an honest, controlled factorial decomposition showing that bipartite compression alone and random feature selection fail on their own, and that univariate marginal feature gating (BGSS) helps if and only if informative coordinates exhibit detectable marginal multimodality.

---

## 2. Formal Research Questions, Hypotheses & Falsification Protocols

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CORE RESEARCH QUESTIONS                         │
├───────────────┬────────────────────────────────────────────────────────┤
│ RQ1: Extent   │ Frequency of stability-accuracy discordance when D>>N  │
│ RQ2: Drivers  │ Technical/geometric mechanisms explaining discordance  │
│ RQ3: Gating   │ BGSS vs. matched-budget unsupervised feature filtering │
│ RQ4: Cohorts  │ Generalization across independent biological cohorts   │
│ RQ5: Unknown-K│ Behavior under genuinely unsupervised cluster discovery│
│ RQ6: Moderns  │ Susceptibility of modern baselines to the discordance  │
│ RQ7: Scaling  │ True computational complexity and memory boundaries    │
└───────────────┴────────────────────────────────────────────────────────┘
```

### RQ1: Extent of Stability–Accuracy Discordance
- **Hypothesis $H_{1}$:** In high-dimensional regimes ($D/N > 20$), standard clustering and consensus methods repeatedly converge onto stable partitions under resampling that fail to align with external reference classes ($\text{Stab} \ge 0.50$ and $\text{Acc} \le 0.05$), while column-permuted null stability remains near zero.
- **Primary Outcome:** Subsample stability ($\text{Stab}$), empirical accuracy ($\text{Acc}$), permuted null stability ($\text{Null}$), and discordance gap $\Delta = \text{Stab} - \text{Acc}$.
- **Experimental Unit:** An algorithm-cohort evaluation cell over 30 stratified 80% subsamples (435 pairs).
- **Confirmatory Experiment:** Multi-cohort subsample stability benchmark with non-degeneracy audit (Table 2 in manuscript; EXP3).
- **Appropriate Statistical Test:** Paired Wilcoxon signed-rank test on $\Delta$, and cohort-clustered bootstrap 95% confidence intervals ($B = 10{,}000$).
- **Falsification Criterion:** If the stability-accuracy gap $\Delta$ across non-degenerate cells is statistically indistinguishable from zero (95% CI includes zero) or if permuted null stability equals subsample stability, $H_1$ is falsified.
- **Manuscript Section:** Section 4 (*Empirical Stability–Accuracy Discordance on Biomedical Cohorts*).

### RQ2: Geometric and Technical Drivers of Discordance
- **Hypothesis $H_{2}$:** Stable discordant partitions reflect dominant sample-level continuous variance axes (such as leading principal components, sequencing depth, and extreme geometric outliers) rather than discrete biological cluster structure.
- **Primary Outcome:** Pearson correlation coefficient $r$ between partition indicator vector and (i) sample PC1 coordinate, (ii) total feature expression per sample, and (iii) sample distance to coordinate centroid.
- **Experimental Unit:** Individual sample partition assignments on the unperturbed cohort.
- **Confirmatory Experiment:** Geometric diagnostic audit on Prostate and CNS (Fig. 3 in manuscript).
- **Appropriate Statistical Test:** Correlation significance tests with Bonferroni correction across covariates.
- **Falsification Criterion:** If cluster assignments do not correlate with PC1 or total expression ($|r| < 0.20, p > 0.05$) while remaining discordant with reference labels, $H_2$ is falsified.
- **Manuscript Section:** Section 4.2 (*Geometric Diagnosis of Discordance: What Are Discordant Partitions Finding?*).

### RQ3: Efficacy of Marginal Multimodality Gating (BGSS)
- **Hypothesis $H_{3}$:** Bimodality-Gated Subspace Selection (BGSS) outperforms matched-budget random feature selection under bipartite consensus in high-dimensional noise regimes by prioritizing coordinates with bimodal marginal distributions.
- **Primary Outcome:** Subgroup mean ARI difference: $\Delta_{\text{gating}} = \text{ARI}_{\text{BGSS}} - \text{ARI}_{\text{Random}}$ under matched budget $\lfloor \alpha D \rfloor$.
- **Experimental Unit:** Paired difference across 30 seeds per cohort.
- **Confirmatory Experiment:** Factorial knockout and matched-budget feature selection benchmark (Table 8 & Table 12; EXP2).
- **Appropriate Statistical Test:** Paired Wilcoxon signed-rank test and cohort-clustered bootstrap 95% CI ($B = 10{,}000$).
- **Falsification Criterion:** If $\Delta_{\text{gating}} \le 0$ across the high-$D$ cohort average or if 95% CI includes zero, $H_3$ is falsified.
- **Manuscript Section:** Section 6 (*Ablation and Algorithmic Attribution*).

### RQ4: Biological Generalization Across Independent Cohorts
- **Hypothesis $H_{4}$:** The cluster recovery advantage of BGSS generalizes to independent high-dimensional oncology cohorts exhibiting strong lineage-defining oncogenes, but collapses on cohorts characterized by subtle polygenic variation.
- **Primary Outcome:** Per-cohort Hedges' $g$ effect size relative to ambient baselines, stratified by empirical bimodality score ($\bar{b}_d$).
- **Experimental Unit:** Independent biological patient cohort ($n = 12$ bulk cohorts).
- **Confirmatory Experiment:** Leave-One-Cohort-Out (LOCO) cross-validation and Leave-(Leukemia+SRBCT)-Out evaluation (EXP7).
- **Appropriate Statistical Test:** DerSimonian–Laird random-effects meta-analysis with Cochran's $Q$ and $I^2$ heterogeneity index.
- **Falsification Criterion:** If GAC fails to maintain positive effect size ($g^* \le 0$) when Leukemia and SRBCT are excluded, or if performance across all 10 remaining cohorts is negative, $H_4$ is falsified.
- **Manuscript Section:** Section 5 & Section 7.2 (*Cohort Generalization and Subgroup Boundary Analysis*).

### RQ5: Unknown-$K$ Estimation and Model Order Selection
- **Hypothesis $H_{5}$:** High-dimensional distractor noise creates an unknown-$K$ discordance trap where standard model order criteria (Silhouette, BIC, Eigengap) pick trivial $\hat{K} = 2$ partitions, whereas consensus PAC on gated anchor graphs recovers true $K^*$ when coordinate multimodality is preserved.
- **Primary Outcome:** Exact cluster count accuracy ($\Pr(\hat{K} = K^*)$), absolute count error $|\hat{K} - K^*|$, and ARI evaluated at estimated $\hat{K}$.
- **Experimental Unit:** Unsupervised execution across 560 synthetic configurations and 12 real biological cohorts without reference labels.
- **Confirmatory Experiment:** Unknown-$K$ Model Order Discovery Benchmark (EXP8).
- **Appropriate Statistical Test:** Multi-class classification accuracy tests and paired Wilcoxon tests on absolute $K$ error.
- **Falsification Criterion:** If ICC-AutoK achieves lower exact recovery than random guess or fails to outperform GMM-BIC and Eigengap under distractor noise, $H_5$ is falsified.
- **Manuscript Section:** Section 5.4 (*Unsupervised Cluster-Number Discovery in High Dimensions*).

### RQ6: Susceptibility of Modern Baselines
- **Hypothesis $H_{6}$:** Contemporary high-dimensional clustering methods (including Sparse K-Means and graph-based Leiden modularity) remain susceptible to stability-accuracy discordance unless explicit coordinate screening is applied.
- **Primary Outcome:** Subsample stability, accuracy, and discordance gap $\Delta$ for Sparse K-Means, Leiden, and HDBSCAN*.
- **Experimental Unit:** 30 stratified subsamples across the 12 high-$D$ cohorts.
- **Confirmatory Experiment:** Modern Baselines Benchmark Matrix (EXP7).
- **Appropriate Statistical Test:** Friedman rank sum test across modern methods and GAC.
- **Falsification Criterion:** If a modern baseline consistently achieves $\text{Stab} \ge 0.50$ and $\text{Acc} \ge 0.50$ across all high-$D$ cohorts, the discordance trap is falsified as a universal property.
- **Manuscript Section:** Section 5.3 (*Comparison with Modern and Specialized Baselines*).

### RQ7: Computational Complexity and Memory Scaling
- **Hypothesis $H_{7}$:** Bipartite graph compression reduces consensus graph memory from $O(N^2)$ to $O(N \cdot L)$ without sacrificing cluster partition recovery, maintaining empirical sub-linear runtime scaling up to $N = 10^5$.
- **Primary Outcome:** Empirical process RSS memory (MB) and wall-clock execution time (seconds) across $N \in [10^3, 10^6]$.
- **Experimental Unit:** Replicate runs on synthetic Gaussian manifolds.
- **Confirmatory Experiment:** Controlled scalability benchmark (EXP5).
- **Appropriate Statistical Test:** Power-law log-log linear regression slope $\beta$ with 95% bootstrap confidence intervals.
- **Falsification Criterion:** If empirical memory scaling exceeds $O(N)$ or if wall-clock runtime exhibits super-quadratic scaling ($\beta \ge 2.0$), $H_7$ is falsified.
- **Manuscript Section:** Section 5.5 (*Computational Scalability and Memory Efficiency*).
