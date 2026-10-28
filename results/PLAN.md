# Experimental Protocol and Pre-Registration Plan (ICC-v2 Revision)

**Title:** *When Does Feature Gating and Anchor Consensus Salvage High-Dimensional Clustering? An Empirical and Geometric Analysis*  
**Date:** October 2026  
**Status:** Pre-registered and Frozen Prior to Experimental Execution  

---

## 1. Objectives & Research Questions
This experimental campaign investigates the performance and boundary conditions of ICC-v2 in light of recent 2024–2026 literature:
1. **Benchmark Comparison with 2025 Meta-Consensus (Exp 8a):** How does ICC-v2 compare against modern meta-consensus algorithms, specifically CoHiRF (Belucci et al., 2025), which combines random feature subsets with hierarchical consensus?
2. **Anchor Selection Paradigm Comparison (Exp 8b):** Does prototype-based anchor selection (K-Means centers or Balanced K-Means anchors, as in Nie et al. 2024 and Huang et al. 2023) improve clustering accuracy over uniform random sampling within certified core sets ($V_5$) or full random selection ($V_4$), or does the anchor certification null result persist?
3. **Feature Gating vs. Random Subspace Selection (Exp 8c):** Does unsupervised Bimodality-Gated Subspace Selection (BGSS) provide an accuracy advantage over CoHiRF-style pure random feature selection under strictly matched active feature budgets ($|\mathcal{F}_{\text{active}}| = \lfloor \alpha \cdot D \rfloor$)?
4. **Distance Concentration Across Diverse Metric Geometries (Exp 8d):** How does the high-dimensional noise stability trap behave under alternative non-Euclidean distance geometries (Chebyshev $L_\infty$ and Cosine distance), as analyzed by Peng et al. (2025)?
5. **Anchor Starvation Test on Large-$K$ Benchmarks (Exp 8e):** Does increasing the anchor budget to $L = \max(40, 10K)$ alleviate the performance collapse of ICC-v2 observed on benchmarks with large cluster counts ($K \ge 16$: Isolet, 20 Newsgroups, Extended Yale B, Indian Pines), or is anchor starvation an inadequate explanation for large-$K$ degradation?
6. **Hyperparameter Sensitivity Surface (Exp 8f):** What is the empirical response surface of ICC-v2 across ensemble sizes $M \in \{5, 10, 15, 25, 50\}$ and anchor budgets $L \in \{20, 40, 60, 80\}$ on the high-dimensional $D/N > 20$ cohorts?

---

## 2. Benchmark Datasets and Split Protocol
All 13 multi-domain benchmark datasets are evaluated under fixed seeds:
- **High-Dimensional Cohorts ($D/N > 20$, 30 Canonical Seeds: 42 to 71):**
  1. CNS ($N=60, D=7{,}129, K=2$)
  2. Colon ($N=62, D=2{,}000, K=2$)
  3. Leukemia ($N=72, D=7{,}129, K=2$)
  4. Ovarian ($N=253, D=15{,}154, K=2$)
  5. Prostate ($N=102, D=12{,}600, K=2$)
  6. SRBCT ($N=83, D=2{,}308, K=4$)
- **Remaining Seven Cohorts (10 Canonical Seeds: 42 to 51):**
  7. Sonar ($N=208, D=60, K=2$)
  8. Madelon ($N=500, D=500, K=2$, deterministic subsample from OpenML 1485)
  9. 20 Newsgroups ($N=18{,}846, D=10{,}000, K=20$)
  10. Isolet ($N=7{,}797, D=617, K=26$)
  11. Indian Pines ($N=10{,}249, D=200, K=16$)
  12. Extended Yale B ($N=2{,}414, D=1{,}024, K=38$)
  13. PBMC68k-reduced ($N=700, D=765, K=10$)

---

## 3. Evaluated Methods and Hyperparameter Freezing
- **ICC-v2 Frozen Settings:**
  - Feature gating: $\alpha = 0.15$ (top 15% features by Sarle's Bimodality Coefficient)
  - Core determinacy threshold: $\tau_{\text{core}} = 0.50$
  - Anchor budget: $L = 40$ (sampled uniformly from certified core set $\mathcal{C}$)
  - Ensemble size: $M = 25$ base partitions
  - Subspace fraction: $0.50 \cdot |\mathcal{F}_{\text{active}}|$
  - Base clusterers: Random initializations of linear K-Means
- **CoHiRF Baseline Protocol:**
  - Evaluated using official Python implementation / faithful adapter
  - Repetitions: $M = 25$
  - Feature sampling: Random feature views ($n_{\text{features}} = \max(2, \lfloor 0.15 \cdot D \rfloor)$)
  - Base clusterer: K-Means ($k=K$)
  - Consensus strategy: Factorized / unanimous hierarchical consensus
  - Freezing: Default published hyperparameters; no tuning per dataset
- **Anchor Selection Variants (Exp 8b):**
  - $V_4$: Uniform random anchors from full dataset
  - $V_5$: Uniform random anchors from certified core set $\mathcal{C}$ ($\tau_{\text{core}} = 0.50$)
  - $V_{\text{kmeans}}$: K-Means cluster centroids as anchors in active feature space
  - $V_{\text{balanced}}$: Balanced K-Means / stratified anchor selection
- **Metric Geometry Variants (Exp 8d):**
  - Euclidean ($L_2$)
  - Chebyshev ($L_\infty$)
  - Cosine distance
- **Large-K Anchor Scaling (Exp 8e):**
  - $L_{\text{scaled}} = \max(40, 10K)$ evaluated across Isolet ($L=260$), 20 Newsgroups ($L=200$), Indian Pines ($L=160$), and Yale B ($L=380$).

---

## 4. Evaluation Metrics and Statistical Battery
- **Primary Accuracy Metric:** Adjusted Rand Index (ARI) against ground truth labels
- **Secondary Metrics:** Normalized Mutual Information (NMI), Wall-clock runtime (s), Consensus stability index
- **Statistical Tests:**
  - Omnibus comparison: Friedman test ($\chi_F^2, p$-value) with average ranks assigned to ties
  - Post-hoc testing: Nemenyi critical difference (CD) at $\alpha = 0.05$
  - Pairwise paired testing: Two-sided Wilcoxon signed-rank tests with Holm-Bonferroni correction
  - Effect size: Vargha-Delaney $A_{12}$
  - Bootstrap uncertainty: $B = 10{,}000$ dataset-clustered bootstrap intervals ($95\%$ CI)

---

## 5. Non-Fabrication and Governance Rules
1. Every numerical result is written by automated scripts from raw arrays.
2. If new baselines (e.g. CoHiRF) outperform ICC-v2 on specific cohorts, results are reported transparently.
3. If increasing anchor budgets $L$ fails to rescue large-$K$ performance, anchor starvation is refuted and reported as an insufficient explanation.
