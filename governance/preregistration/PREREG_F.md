# Pre-Registration Document: Pass F Statistical & Empirical Protocol (PREREG_F.md)

**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Date:** 2026-10-23  
**Status:** Pre-Specified Prior to Pass F Benchmark Execution  

---

## 1. Scope & Objective

This document pre-specifies the exact experimental protocol, random seed schedule, statistical formulas, and reporting conventions for Pass F of the manuscript:
*"Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data"* (early project allotment title that evolved into the canonical Springer Nature manuscript *"When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"*).

All subsequent empirical claims, tables, macro values, and prose in Sections 5-6 and the abstract must strictly conform to the execution of this protocol.

---

## 2. Seed Schedule & Dataset Allocations

### 2.1 High-Dimensional Subgroup ($D/N > 20$, 6 Datasets)
To address seed-variance in bimodal or high-variance regimes, all 11 benchmark methods will be executed across **30 independent random seeds** ($\text{seed} \in \{0, 1, \dots, 29\}$):
1. **CNS** ($N=60, D=7,129, K=2$)
2. **Colon** ($N=62, D=2,000, K=2$)
3. **Leukemia** ($N=72, D=7,129, K=2$)
4. **Ovarian** ($N=253, D=15,154, K=2$)
5. **Prostate** ($N=102, D=12,600, K=2$)
6. **SRBCT** ($N=83, D=2,308, K=4$)

### 2.2 Standard Benchmark Datasets (7 Datasets)
Due to computational constraints on massive/multi-class benchmarks (e.g., 20 Newsgroups with $N=18,846$ and $D=10,000$; Isolet with $N=7,797, K=26$; Indian Pines with $N=10,249$), the remaining 7 datasets retain the canonical **10 random seeds** ($\text{seed} \in \{0, 1, \dots, 9\}$):
1. **Sonar** ($N=208, D=60, K=2$)
2. **Madelon** ($N=500, D=500, K=2$)
3. **Indian Pines** ($N=10,249, D=200, K=16$)
4. **Isolet** ($N=7,797, D=617, K=26$)
5. **20 Newsgroups** ($N=18,846, D=10,000, K=20$)
6. **Extended Yale B** ($N=2,414, D=1,024, K=38$)
7. **PBMC68k-reduced** ($N=700, D=765, K=10$)

Table 4 will explicitly document this dual-scale reporting: 30-seed statistics for the 6 high-D datasets and 10-seed statistics for the general benchmarks, with seed counts stated in the caption and headers.

---

## 3. Candidate Methods (11 Models)

1. **K-Means** (Arthur & Vassilvitskii, SODA 2007): $n_{\text{init}}=10$, Lloyd's algorithm.
2. **Ward Linkage** (Ward, JASA 1963): Euclidean distance, deterministic.
3. **Spectral Clustering** (von Luxburg, Stat. Comput. 2007): $k$-NN affinity graph ($k=10$), normalized Laplacian.
4. **Fuzzy C-Means (FCM)** (Bezdek, 1981): fuzzifier $m=2.0$, max iter 150.
5. **Standard Consensus** (Fred & Jain, TPAMI 2005): $M=25$ base K-Means, co-association matrix $\mathbf{S}$, average-linkage consensus.
6. **Core-Halo Consensus (inspired by Li et al., 2019)**: $M=25$ base K-Means, stability threshold $\tau=\text{median}(\sigma)$, core average-linkage clustering, halo assignment via max co-association.
7. **DEC** (Xie et al., ICML 2016): Autoencoder $D \to 500 \to 500 \to 2000 \to 10$, pretrain 200 epochs, fine-tune 100 epochs, Student-$t$ clustering loss.
8. **FCAG** (Nie et al., TPAMI 2024): 40 anchors, bipartite graph partition.
9. **FastMVC** (Huang et al., TKDE 2023): 40 anchors, multi-view anchor graph.
10. **ICC-v1**: $M=25$, $L=40$ anchors, co-association consensus.
11. **ICC-v2 (Proposed)**: $M=25$, $L=40$ anchors, adaptive subspace projections ($\alpha=0.3$), core quantile $\tau=0.5$.

---

## 4. Headline Reporting Conventions & Formulas

1. **Point Estimates:**
   - Primary: Mean $\pm$ Standard Deviation.
   - Secondary (skewed distributions): Median.
   - Bimodal success metric: Fraction of seeds where $\text{ARI} > 0.50$.
   - 95% Confidence Intervals: Non-parametric bootstrap with $B=1,000$ resamples.

2. **Friedman Test Statistic:**
   $$\chi_F^2 = \frac{12 N}{k(k+1)} \left[ \sum_{j=1}^k R_j^2 - \frac{k(k+1)^2}{4} \right]$$
   where $k=11$ models, $N=13$ datasets (or $N=12$ excluding PBMC68k-reduced, or $N=6$ high-D subgroup).

3. **Nemenyi Critical Difference:**
   $$CD = q_\alpha \sqrt{\frac{k(k+1)}{6 N}}$$
   For $\alpha = 0.05$ and $k=11$, studentized range critical value $q_{0.05} = 3.219$.
   - For $N=13$: $CD = 3.219 \sqrt{\frac{11 \times 12}{6 \times 13}} = 4.19$.
   - For $N=12$: $CD = 3.219 \sqrt{\frac{11 \times 12}{6 \times 12}} = 4.36$.

4. **Bimodality Assessment:**
   Sarle's Bimodality Coefficient:
   $$BC = \frac{\gamma^2 + 1}{\kappa + \frac{3(n-1)^2}{(n-2)(n-3)}}$$
   A dataset is designated bimodal if and only if $BC > 0.556$ (the uniform distribution threshold) and Hartigan's dip test rejects unimodality ($p < 0.05$). If $BC \le 0.556$, the label "bimodal" must not be used.

---

## 5. Frozen Output Targets
All Pass F results will be stored in `results/passF/`:
- `high_d_30seeds_all_models.csv`: 6 datasets $\times$ 11 models $\times$ 30 seeds = 1,980 evaluations.
- `benchmark_matrix_passF.csv`: Unified matrix combining 30 seeds for high-D with 10 seeds for general benchmarks.
- `ablation_30seeds_passF.csv`: 2x2 Factorial ablation across 30 seeds for the 6 high-D datasets.
- `inductive_30seeds_passF.csv`: Direct inductive projection with paired differences and bootstrap CIs.
- `friedman_nemenyi_passF.json`: Exact recomputed ranks, $\chi_F^2$, $p$-values, and $CD$.
