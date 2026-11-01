# Comprehensive Evaluation Design and Benchmark Architecture

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Working Branch:** `research/dami-revision`  
**Audit Component:** Agent C — Comprehensive Evaluation Design  
**Date of Record:** November 1, 2026  
**Status:** **AUDITED AND VERIFIED**

---

## 1. Executive Summary & Design Principles

An empirical benchmark must never evaluate algorithms using a single, isolated metric. Evaluating solely by Adjusted Rand Index (ARI) risks obscuring degenerate cluster solutions, ignoring severe runtime overheads, or rewarding algorithms that achieve apparent stability through pathological clustering behaviors.

This comprehensive evaluation framework structures performance assessment across **five distinct, non-interchangeable dimensions**:
1. **Clustering Quality:** Partition agreement with biological reality (ARI, AMI, NMI, V-Measure).
2. **Consensus Stability & Discordance:** Resampling consistency, cluster stability, and the empirical divergence between stability and accuracy.
3. **Consensus Matrix Topology:** Ambiguity concentration, PAC, and consensus CDF characteristics.
4. **Stress Robustness:** Sensitivity to feature noise, sample subsampling, missing coordinates, and hyperparameter perturbations.
5. **Computational Scalability:** Wall-clock runtime, peak RAM consumption, and failure attrition rates.

---

## 2. Scientific Claim to Metric Mapping Architecture

To prevent selective metric reporting (cherry-picking), every scientific claim is bound to an explicit primary metric and secondary confirmatory indicators prior to experimental execution:

| Scientific Dimension | Scientific Claim Under Evaluation | Primary Metric | Secondary / Diagnostic Metrics | Multiplicity Treatment |
| :--- | :--- | :--- | :--- | :--- |
| **Comparative Superiority** | Full ICC-v2 outperforms baseline clustering algorithms on high-dimensional biomedical cohorts. | Cohort-level paired difference in median ARI ($\Delta\text{ARI}$) | Paired $\Delta\text{AMI}$, $\Delta\text{NMI}$, $\Delta\text{V-Measure}$ | Family 1 (Holm-Bonferroni across 8 baselines) |
| **Bimodality Gating Gain** | BGSS feature selection confers performance advantages over matched random feature gating under bipartite consensus. | Cohort-level paired difference in median ARI ($\Delta_{\text{gating}} = \text{ARI}_{\text{BGSS}} - \text{ARI}_{\text{random}}$) | Proportion of true bimodal drivers selected, active feature count | Family 2 (Holm-Bonferroni across ablated arms) |
| **Dense Consensus Attenuation** | The BGSS performance gain is significantly reduced under dense co-occurrence consensus compared to bipartite consensus. | Interaction contrast: $\Delta\Delta = (\text{ARI}_{\text{BGSS, Bip}} - \text{ARI}_{\text{Rand, Bip}}) - (\text{ARI}_{\text{BGSS, Dense}} - \text{ARI}_{\text{Rand, Dense}})$ | Ratio of treatment effects, paired sign test | Family 2 (Holm-Bonferroni across ablated arms) |
| **Core Anchor Determinacy Equivalence** | Certified core anchors perform equivalently to uniform random landmark anchors within margin $\pm 0.02$. | Two One-Sided Tests (TOST) on paired difference $\Delta = \text{ARI}_{\text{certified}} - \text{ARI}_{\text{random\_anchors}}$ | $90\%$ and $95\%$ bootstrap confidence intervals, anchor stability variance | Family 2 (TOST equivalence procedure) |
| **Stability–Accuracy Decoupling** | Subsampling stability fails to predict clustering accuracy across model families ($\rho < 0.30$). | Cohort-averaged Fisher $z$-transformed Spearman rank correlation ($z(\hat{\rho})$) | Repeated-measures correlation $\rho_{\text{rm}}$, mixed-effects slope $\beta_1$ | Family 3 (Hierarchical testing step 1) |
| **False Confidence Gap** | Subsample stability systematically exceeds external clustering accuracy ($\Delta_{\text{gap}} > 0.20$). | Cohort-level mean gap: $\bar{\Delta}_j = \frac{1}{M}\sum_m (\text{Stab}_{m, j} - \text{ARI}_{m, j})$ | Proportion of model runs with $\text{Stab} > \text{ARI} + 0.20$ | Family 3 (Hierarchical testing step 2) |
| **Unsupervised Model Order Discovery** | Bipartite PAC minimization discovers the optimal cluster count $K^*$ without reference labels. | Absolute error in discovered model order: $|\hat{K}_{\text{PAC}} - K^*|$ | Discovered $\hat{K}_{\text{PAC}}$, candidate PAC curves in $[0.10, 0.90]$, Silhouette score | Family 4 (Descriptive / exploratory) |
| **Computational Scalability** | Bipartite consensus achieves linear memory $\mathcal{O}(N L)$ and execution time scaling compared to quadratic dense consensus $\mathcal{O}(N^2)$. | Wall-clock latency $t_{\text{sec}}$ and Peak RAM (MB) across scaling grids ($N \in [10^2, 10^5]$) | Theoretical flop counts, fitted scaling exponents | Family 4 (Descriptive / benchmark) |

---

## 3. Protocol for Multi-Metric Evaluation Execution

### 3.1 External Validation Pipeline
For every fitted clustering solution $\hat{\mathbf{y}} \in \{0, \dots, K-1\}^N$:
1. Check for degenerate collapse: if $|\text{unique}(\hat{\mathbf{y}})| < 2$, record run as degenerate (`ARI = 0.0, NMI = 0.0, AMI = 0.0`).
2. Compute full suite of external metrics using `src/icc/metrics.py:evaluate_all`:
   ```python
   scores = evaluate_all(y_true, y_pred)
   # returns {'ari': float, 'nmi': float, 'ami': float, 'v_measure': float, 'fm_index': float}
   ```
3. Generate $B=1{,}000$ bootstrap resamples to derive empirical $95\%$ confidence intervals per individual run.

### 3.2 Stability Assessment Protocol
1. **Subsample Agreement:** For each algorithm, draw 30 pairs of $80\%$ random subsamples $(\mathcal{X}_1, \mathcal{X}_2)$. Compute $\text{ARI}$ on the sample overlap $\mathcal{X}_1 \cap \mathcal{X}_2$.
2. **Seed Variance:** Evaluate algorithm across 30 canonical random seeds $\mathcal{S} = \{0, 1, \dots, 29\}$ on identical data. Compute standard deviation $\sigma_{\text{seed}}(\text{ARI})$.
3. **Partition Perturbation:** Evaluate sensitivity to Gaussian feature jitter ($\sigma \in \{0.01, 0.05, 0.10\}$) and coordinate dropout ($5\%, 10\%, 20\%$).

### 3.3 Consensus-Specific Matrix Diagnostics
1. **PAC Evaluation:** Evaluate empirical CDF of consensus matrix $\mathbf{S}$ at $u_1 = 0.10$ and $u_2 = 0.90$:
   $$\text{PAC} = F(0.90) - F(0.10)$$
2. **Cluster Imbalance Ratio:**
   $$\text{IR} = \frac{\max_c |C_c|}{\min_c |C_c|}$$
   Identifies fragmented singleton clusters or collapsed giant components.
