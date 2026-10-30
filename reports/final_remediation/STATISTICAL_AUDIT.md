# Statistical Methodology & Estimand Audit Report

**Report Location:** `reports/final_remediation/STATISTICAL_AUDIT.md`  
**Manuscript Title:** *Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes*  
**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI)  
**Status:** INDEPENDENTLY RECALCULATED AND AUDITED  

---

## 1. Overview and Estimand Framework

To prevent statistical misinterpretations and ensure complete transparency, this audit documents every mathematical estimand, sampling design, statistical test, and confidence interval procedure used in the manuscript.

### 1.1 Non-Parametric Test Selection Justification
Parametric Student's $t$-tests and ANOVA assume normally distributed errors. In clustering benchmarking, ARI distributions frequently exhibit:
1. Hard boundaries at $\text{ARI} = 1.0$ (perfect recovery) and $\text{ARI} \approx 0.0$ (random chance).
2. Heavy discrete bimodality on small biomedical cohorts (e.g. on Leukemia, 22/30 seeds sample informative coordinates and reach $\text{ARI} > 0.50$, while 8/30 seeds collapse near $0.0$).
3. Shapiro-Wilk tests strongly reject normality on 4 of the 6 high-dimensional cohorts ($p < 10^{-4}$ on Colon, Leukemia, Ovarian, and Prostate).

Consequently, non-parametric tests (Friedman omnibus rank test, two-tailed Nemenyi post-hoc test, paired Wilcoxon signed-rank test with Holm-Bonferroni adjustment, and percentile bootstrap confidence intervals) were pre-specified as the standard statistical suite.

---

## 2. Stability Estimands and Alignment Protocol

The manuscript evaluates four distinct stability and accuracy quantities that must not be conflated:

### 2.1 Subsample Stability ($\text{Stab}$)
* **Definition:** Pairwise agreement across stochastic subsamples. Let $\mathcal{S}_1, \dots, \mathcal{S}_B$ denote $B=30$ independent stratified $80\%$ subsamples drawn from cohort $\mathcal{X}$. For any pair $(u, v)$ with $1 \le u < v \le B$, let $\mathcal{I}_{u,v} = \mathcal{S}_u \cap \mathcal{S}_v$ denote the intersecting subset of observations present in both draws.
* **Alignment Formulation:**
  $$\text{Stab} = \frac{1}{\binom{B}{2}} \sum_{1 \le u < v \le B} \text{ARI}\left(\pi^{(u)}|_{\mathcal{I}_{u,v}}, \pi^{(v)}|_{\mathcal{I}_{u,v}}\right).$$
* **Pair Count:** For $B=30$, the number of distinct pairwise evaluations is exactly:
  $$\binom{30}{2} = \frac{30 \times 29}{2} = 435 \text{ pairs}.$$
* **Sample Overlap:** On an $80\%$ draw, the expected intersection size is $0.80^2 N = 0.64 N$. Observations outside $\mathcal{I}_{u,v}$ are excluded before computing contingency overlaps $n_{ij}$, guaranteeing valid label alignment.

### 2.2 Subsample Accuracy ($\text{Acc}$)
* **Definition:** Mean clustering accuracy of each subsample model evaluated against true ground-truth diagnoses restricted to that subsample:
  $$\text{Acc} = \frac{1}{B} \sum_{u=1}^B \text{ARI}\left(\pi^{(u)}, \mathbf{y}^*|_{\mathcal{S}_u}\right).$$

### 2.3 Permuted Null Control Stability ($\text{Null}$)
* **Definition:** Subsample stability evaluated on matrix $\tilde{\mathbf{X}}$ where every column coordinate $d \in \{1, \dots, D\}$ is independently permuted across samples:
  $$\tilde{X}_{i, d} = X_{\sigma_d(i), d}, \quad \sigma_d \in \mathfrak{S}_N.$$
* **Theoretical Role:** Destroys all multi-feature correlation and cluster manifolds while strictly preserving marginal coordinate distributions. If real stability is elevated ($\text{Stab} \ge 0.50$) while null stability collapses ($\text{Null} \approx 0.0$), elevated stability is proven to stem from geometric attractors in the noise manifold rather than univariate marginal variance.

### 2.4 Seed Stability on Full Cohort ($\text{Seed}^*$)
* **Definition:** Mean pairwise ARI across $B=30$ stochastic initializations on the complete, unperturbed cohort:
  $$\text{Seed}^* = \frac{1}{\binom{B}{2}} \sum_{1 \le u < v \le B} \text{ARI}\left(\pi^{(u)}, \pi^{(v)}\right).$$
* **Methodological Caveat:** Deterministic algorithms (Ward agglomerative linkage, Spectral clustering with deterministic Lanczos eigensolver) trivially achieve $\text{Seed}^* = 1.000$ because they yield identical outputs across seeds on unperturbed data. Seed stability is therefore uninformative for deterministic solvers, which is why the subsample perturbation protocol ($\text{Stab}$) is necessary.

---

## 3. Stability–Accuracy Gap Calculations

### 3.1 Pairwise Gap Metric ($\Delta$)
The stability–accuracy gap measures the degree to which an algorithm converges stably onto incorrect partitions:
$$\Delta = \text{Stab} - \text{Acc}.$$
* **Decision Rule (i) ("Stable but Wrong"):** Satisfied when $\text{Stab} \ge 0.50$ and $\text{Acc} \le 0.05$.
* **Empirical Incidence:**
  - Three methods meet Rule (i) across $\ge 3$ distinct cohorts: FCAG (Colon, CNS, Prostate), FCM (Colon, CNS, Ovarian), and FastMVC (Colon, CNS, Prostate).
  - On Prostate ($D=12{,}600$), 10 of 12 methods satisfy Rule (i), led by Ward ($\Delta = +0.970$), Spectral ($\Delta = +0.973$), and Core-Halo ($\Delta = +1.000$).

### 3.2 Pooled Bootstrap Confidence Interval
* **Target Estimand:** Overall mean gap across all 12 clustering models and 6 high-dimensional cohorts ($12 \times 6 = 72$ cells).
* **Resampling Scheme:** Dataset-clustered non-parametric bootstrap ($B = 10{,}000$ iterations) resampling cohorts with replacement.
* **Result:**
  $$\bar{\Delta}_{\text{overall}} = +0.464, \quad 95\% \text{ CI}: [+0.363, +0.607].$$
* **Interpretation:** Zero is firmly excluded, confirming that consensus and graph clustering models systematically exhibit positive stability–accuracy gaps in extreme high-dimensional noise regimes.

### 3.3 GAC Specific Gap
* For the GAC pipeline specifically across the 6 cohorts:
  $$\text{Stab}_{\text{GAC}} = 0.468, \quad \text{Acc}_{\text{GAC}} = 0.168, \quad \Delta_{\text{GAC}} = +0.300, \quad 95\% \text{ CI}: [+0.058, +0.561].$$
* On Leukemia ($\Delta = -0.078$) and SRBCT ($\Delta = +0.014$), GAC eliminates the gap. On Prostate ($\Delta = +0.847$) and CNS ($\Delta = +0.542$), weak bimodality causes GAC to fall into the stability trap.

---

## 4. Hypothesis Testing and Inferential Coexistence

### 4.1 Omnibus Friedman Test
* **Null Hypothesis ($H_0$):** All 12 clustering algorithms exhibit equal performance across the 13 benchmark datasets.
* **Computation:**
  $$\chi_F^2 = 11.5562 \approx 11.56, \quad p = 0.3979 \approx 0.40 \gg 0.05.$$
* **Conclusion:** Fails to reject the null hypothesis. There is no statistically significant overall performance difference among the 12 algorithms across the 13 multi-domain datasets.

### 4.2 Nemenyi Post-Hoc Analysis
* **Critical Difference Threshold:**
  $$CD = 4.62 \quad (\alpha = 0.05).$$
* **Observed Rank Range:** Best rank is K-Means ($5.15$); lowest rank is FCAG ($7.77$). Maximum pairwise rank difference is $|5.15 - 7.77| = 2.62 < 4.62$.
* **Conclusion:** All 12 algorithms belong to a single equivalence clique.

### 4.3 Coexistence of CI Excluding Zero and Non-Significant Wilcoxon Test
In Section 7.3, the $V_5 - V_2$ factorial interaction reports:
$$\text{Mean Difference} = +0.139, \quad 95\% \text{ Bootstrap CI}: [+0.004, +0.321], \quad \text{Wilcoxon } p \approx 0.156.$$

**Methodological Explanation:**
1. **Different Questions:** The bootstrap confidence interval estimates the sampling distribution of the *mean difference*, which is dominated by large positive gains on Leukemia ($+0.557$) and SRBCT ($+0.213$).
2. **Discrete Rank Constraints:** The two-tailed Wilcoxon signed-rank test evaluates *rank order of absolute differences* on $n=6$ pairs. With $n=6$, the theoretical minimum $p$-value occurs when all 6 differences have the same sign ($W=0, p = 2 \times 0.5^6 = 0.03125$).
3. When even a single cohort has a negative difference (Prostate: $-0.028$), $W = 3.0$, and the exact discrete two-tailed $p$-value jumps to $0.15625$.
4. Stating both metrics transparently prevents cherry-picking and accurately conveys that while the average gain is positive, the non-parametric sign test on 6 datasets does not achieve formal significance.
