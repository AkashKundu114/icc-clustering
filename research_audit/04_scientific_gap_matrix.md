# Research Audit 04: Scientific Gap Matrix & Resolution Roadmap

**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD / DAMI)  
**Target Manuscript:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Date:** 2026-10-31  

---

## 1. Executive Matrix of Scientific Gaps

| Gap ID | Identified Scientific Vulnerability | Evidence in Existing Repository | Methodological / Statistical Consequence | Proposed Phase & Resolution Protocol | Target Deliverable |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GAP-01** | **Limited Cohort Coverage ($n=6$)** | Only 6 high-dimensional oncology cohorts ($D/N > 20$) in primary stability-accuracy analysis. | Statistical power severely restricted. Minimum attainable two-sided Wilcoxon $p = 2^{-5} = 0.03125$. Under Holm-Bonferroni correction across 3 gating tests, $p_{\text{adj}} \approx 0.094 > 0.05$. | **Phase 2 & Phase 3:** Expand suite to $n=12$ independent bulk oncology cohorts ($D/N > 20$) and 6 single-cell RNA-seq cohorts. | `research_audit/08_dataset_provenance.csv`, `experiments/exp6_cohort_expansion/` |
| **GAP-02** | **Concentration of BGSS Gains in 2 Cohorts** | The $+0.169$ gain of BGSS under bipartite consensus rests almost entirely on Leukemia ($+0.398$) and SRBCT ($+0.447$). Colon ($+0.078$), CNS ($+0.007$), Prostate ($+0.004$), and Ovarian ($-0.012$) show minimal response. | Risk of benchmark overfitting to two historic microarray datasets with extreme lineage binarization. Does BGSS generalize to subtle cancer staging or polygenic phenotypes? | **Phase 3:** Leave-One-Cohort-Out (LOCO) and Leave-(Leukemia+SRBCT)-Out validation; DerSimonian–Laird random-effects meta-analysis and forest plots. | `research_audit/15_statistical_analysis_plan.md`, `experiments/exp7_modern_baselines/` |
| **GAP-03** | **Absence of Contemporary Baselines** | Benchmarks compare primarily against pre-2010 classical methods (K-Means, Ward, FCM, Spectral), DEC (2016), and an informal FastMVC surrogate. No Sparse K-Means, no Leiden on SNN graphs, no modern self-supervised contrastive clustering. | Reviewers at DMKD will rightly object that GAC is only compared against obsolete algorithms and a non-faithful surrogate. | **Phase 4:** Implement and benchmark Sparse K-Means (Witten & Tibshirani 2010), Leiden SNN (Traag et al. 2019), GMM with BIC/ICL, HDBSCAN*, and true FastMICE ADMM solver. | `research_audit/11_baseline_fidelity.csv`, `research_audit/12_baseline_comparison_protocol.md` |
| **GAP-04** | **Complete Absence of Unknown-$K$ Experiments** | All 12 algorithms currently receive ground-truth $K = K^*$. Consensus clustering was originally formulated by Monti et al. (2003) specifically to discover unknown $K$. | The manuscript's central thesis—stability-accuracy discordance—remains untested under realistic model order discovery. Does noise trick consensus stability into picking false $\hat{K} = 2$? | **Phase 5:** Design and execute **EXP6/EXP8 (Unknown-$K$ Benchmark)** using ICC-AutoK (PAC and consensus area change) across a 560-cell synthetic grid and real cohorts. | `research_audit/13_unknown_k_protocol.md`, `research_audit/14_unknown_k_results.md` |

---

## 2. Deep Dive: Gap 1 & Gap 2 (Cohort Coverage & BGSS Fragility)

### 2.1 The Mathematical Mechanism Behind the Leukemia/SRBCT Concentration
Sarle's Bimodality Coefficient:
$$b_d = \frac{\gamma_d^2 + 1}{\kappa_d + 3}$$
evaluates marginal coordinate distributions. Under Gaussian or continuous unimodal noise, $\mathbb{E}[b_d] \approx 5/9 \approx 0.556$ (or $1/3 \approx 0.333$ under uniform distribution).
- **Why Leukemia ($+0.398$) & SRBCT ($+0.447$) succeed:**
  - In Leukemia (Golub et al., ALL vs. AML), master transcription factors (e.g. *MPO*, *CD19*, *HOXA9*) are completely silenced in one lineage and abundantly transcribed in the other. Their marginal distributions form two distinct well-separated modes, driving $b_d \gg 0.70$. BGSS easily separates them from unimodal background noise ($p = 1.38 \times 10^{-10}$).
  - In SRBCT (Khan et al., 4 pediatric lineages), lineage-specific markers (*EWS-FLI1*, *PAX3-FKHR*, *MYCN*) show discrete multi-modal bursts across the 4 cancer types.
- **Why Prostate ($+0.004$) & CNS ($+0.007$) fail:**
  - In Prostate (Singh et al., tumor vs. normal), single genes exhibit subtle shifts confounded by stromal contamination and sequencing depth. The marginals remain unimodal with heavy tails ($b_d \approx 0.333$), rendering univariate screening ineffective.
  - In CNS (Pomeroy et al., survivor vs. fatality), prognosis is polygenic and continuous without discrete lineage bifurcation.

### 2.2 The Scientific Solution
1. **Expand to 12 Independent Bulk Oncology Cohorts ($D/N > 20$):**
   Add DLBCLA ($N=77, D=7129$), Ramaswamy ($N=198, D=16063$), NovartisBPLC ($N=103, D=12600$), Su2001 ($N=174, D=12533$), Breast van 't Veer ($N=97, D=4988$), and Risinger ($N=42, D=12625$).
2. **Formal Subgroup Stratification:**
   Classify cohorts a priori into **Lineage-Driven (Expected High BC)** vs. **Polygenic / Staging (Expected Low BC)** to formally test the theoretical prediction that BGSS functions if and only if coordinates exhibit detectable marginal multimodality.
3. **Leave-(Leukemia+SRBCT)-Out Evaluation:**
   Directly report whether GAC retains statistical gains when both Leukemia and SRBCT are excluded.

---

## 3. Deep Dive: Gap 3 (Contemporary Baseline Comparison)

### 3.1 The Missing Modern Baselines
1. **Sparse K-Means (SKM, Witten & Tibshirani, JASA 2010):**
   - The definitive $L_1$-penalized feature-weighting clustering method for $D \gg N$.
   - Directly tests whether BGSS's $O(ND)$ marginal filter matches or beats joint regularized $L_1$ lasso weights.
2. **High-Dimensional Graph Community Detection (PCA + SNN + Leiden; Traag et al. 2019, Stuart et al. 2019):**
   - The universal standard in single-cell genomics and transcriptomics.
   - Evaluates how modularity optimization on shared nearest neighbor graphs behaves under stability-accuracy discordance.
3. **GMM with Model Selection (BIC and ICL; Biernacki et al. 2000):**
   - Rigorous probabilistic baseline testing whether soft density estimation and assignment entropy penalties prevent discordance.
4. **HDBSCAN\* (Campello et al. 2013, McInnes et al. 2017):**
   - Density-based hierarchical clustering that automatically rejects noise points ($C = -1$).
5. **Faithful FastMICE Solver (Huang et al., IEEE TKDE 2023):**
   - Replaces the informal surrogate with the true ADMM consensus bipartite solver.

---

## 4. Deep Dive: Gap 4 (Unknown-$K$ Model Order Discovery)

### 4.1 The Scientific Dilemma
In actual scientific discovery, ground-truth $K$ is unknown.
- Şenbabaoğlu et al. (2014) showed that consensus clustering on pure noise frequently indicates a false peak at $K=2$.
- Under $D \gg N$, distractor noise creates an "unknown-$K$ discordance trap": methods converge to deceptive, highly stable partitions at incorrect $K$ with zero external accuracy.

### 4.2 The Scientific Solution
1. **Implement ICC-AutoK:**
   - Unsupervised model order selection over $K \in \{2, \dots, K_{\max}\}$ using the Proportion of Ambiguous Clustering (PAC):
     $$\text{PAC}_K = F_K(0.90) - F_K(0.10)$$
   - Accelerated via $O(1)$ memory anchor pair sampling ($M_{\text{pairs}} = 10{,}000$).
2. **Benchmark Against 6 Automatic-K Estimators:**
   - HDBSCAN\*
   - GMM-BIC
   - GMM-ICL
   - Spectral Eigengap
   - Dynamic Tree Cut
   - X-Means
3. **Evaluate Across Both Synthetic Grids and Real Cohorts:**
   - Report $\hat{K}$ exact recovery rate, absolute error $|\hat{K} - K^*|$, ARI at $\hat{K}$, and discordance $\Delta = \text{Stab}(\hat{K}) - \text{Acc}(\hat{K})$.
