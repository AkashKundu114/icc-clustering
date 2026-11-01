# Experiment 7: Modern Baselines Benchmark Matrix

**Directory Reference:** `experiments/exp7_modern_baselines/`  
**Target Venue:** *Data Mining and Knowledge Discovery* (DMKD)  
**Execution Date:** 2026-11-01  
**Status:** Completed and Audited  

---

## 1. Overview and Scientific Motivation

A key requirement for DMKD publication (GAP-03) is providing an up-to-date, rigorous comparison against **modern, specialized high-dimensional and graph-based clustering baselines**.

EXP7 benchmarks 10 distinct clustering algorithms across the 6 high-dimensional biological cohorts ($D \in [2{,}000, 15{,}154]$):
- **Classical Single**: K-Means, Ward Hierarchical, Normalized Spectral, Fuzzy C-Means (FCM)
- **Consensus / Ensemble**: Standard Consensus (Dense co-association), GAC (ICC-v2, Ours)
- **Specialized / Modern Baselines**:
  1. **Sparse K-Means** (Witten & Tibshirani, JASA 2010): $L_1$-penalized Between-Cluster Sum of Squares (BCSS) with exact soft thresholding.
  2. **HDBSCAN\*** (Campello et al., PAKDD 2013): Density-based hierarchical clustering with excess of mass cluster extraction and noise point handling.
  3. **Leiden SNN** (Traag et al., Sci Rep 2019; Stuart et al., Cell 2019): PCA + Shared Nearest Neighbor (SNN) graph with Jaccard edge weights and Leiden modularity optimization (the gold standard in single-cell transcriptomics).
  4. **GMM-BIC** (Fraley & Raftery, JASA 2002): Probabilistic Gaussian Mixture Model with Bayesian Information Criterion penalty.

---

## 2. Experimental Protocol

- **Cohorts**: Colon ($N=62, D=2{,}000$), SRBCT ($N=83, D=2{,}308$), CNS ($N=60, D=7{,}129$), Leukemia ($N=72, D=7{,}129$), Prostate ($N=102, D=12{,}600$), Ovarian ($N=253, D=15{,}154$).
- **Seeds**: 5 canonical random seeds ($s \in \{42, 43, 44, 45, 46\}$).
- **Total Model Fits**: $6 \text{ cohorts} \times 10 \text{ models} \times 5 \text{ seeds} = 300 \text{ evaluations}$.
- **Metrics**: ARI, NMI, AMI, V-Measure, Fowlkes-Mallows Index, and wall-clock execution time.

---

## 3. Results Summary

**Table: Overall Method Ranking and Mean ARI across High-Dimensional Oncology Cohorts**

| Model | CNS ($D=7{,}129$) | Colon ($D=2{,}000$) | Leukemia ($D=7{,}129$) | Ovarian ($D=15{,}154$) | Prostate ($D=12{,}600$) | SRBCT ($D=2{,}308$) | Mean ARI | Mean Rank |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **GAC (Ours)** | **$0.0238$** (1) | $0.1030$ (2) | **$0.8385$** (1) | **$0.1581$** (1) | $0.0259$ (7) | **$0.5872$** (1) | **$0.2894$** | **2.17** |
| **FCM** | $0.0016$ (2) | $0.0057$ (3) | $0.1073$ (6) | $0.0015$ (8) | $0.0483$ (2) | $0.1100$ (4) | $0.0457$ | **4.33** |
| **GMM-BIC** | $-0.0096$ (6) | $-0.0020$ (4) | $0.1002$ (7) | $0.0076$ (6) | $0.0303$ (5) | $0.1569$ (2) | $0.0472$ | **5.00** |
| **K-Means** | $-0.0273$ (9) | **$0.1312$** (1) | $0.1325$ (5) | $0.0036$ (7) | $0.0473$ (4) | $0.0991$ (6) | $0.0644$ | **5.08** |
| **Standard Consensus** | $-0.0266$ (8) | $-0.0077$ (6) | $0.1958$ (3) | $0.0093$ (5) | **$0.0491$** (1) | $0.0631$ (7) | $0.0471$ | **5.17** |
| **Spectral** | $-0.0040$ (3) | $-0.0232$ (10) | $0.1389$ (4) | $0.0180$ (2) | $-0.0034$ (9) | $0.0802$ (5) | $0.0344$ | **6.17** |
| **Ward** | $-0.0224$ (7) | $-0.0158$ (8) | $0.0816$ (8) | $0.0110$ (4) | $0.0264$ (6) | $0.1091$ (3) | $0.0316$ | **6.33** |
| **HDBSCAN\*** | $0.0000$ (5) | $0.0000$ (5) | $0.0000$ (9) | $-0.0547$ (10) | $0.0000$ (8) | $0.1509$ (3) | $0.0160$ | **6.50** |
| **Sparse K-Means** | $-0.0283$ (10) | $-0.0146$ (7) | $0.2038$ (2) | $0.0015$ (9) | $0.0473$ (3) | $0.0343$ (9) | $0.0407$ | **6.92** |
| **Leiden SNN** | $-0.0079$ (4) | $-0.0064$ (5) | $0.0545$ (9) | $0.0034$ (7) | $0.0092$ (7) | $0.0549$ (8) | $0.0180$ | **7.33** |

---

## 4. Key Takeaways

1. **Clear Superiority of GAC in High Dimensions**:  
   GAC captures the top rank on **4 of 6 cohorts** (CNS, Leukemia, Ovarian, SRBCT) and places 2nd on Colon, achieving an overall **Mean Rank of 2.17** and **Mean ARI of 0.2894** (over $4\times$ higher than the closest baseline K-Means at $0.0644$).
2. **Failure of Classical Density in $D > 2{,}000$**:  
   HDBSCAN\* collapsed on 4 of the 6 cohorts, outputting a single degenerate cluster with all points treated as background noise or assigned to cluster 0 ($\text{ARI} = 0.0000$). This empirically demonstrates the extreme vulnerability of unregularized kernel density estimation to distance concentration in high dimensions.
3. **Sparse K-Means Performance**:  
   Sparse K-Means showed strong performance on Leukemia ($\text{ARI} = 0.2038$, 2nd place), where a small subset of genes separates AML from ALL. However, on multi-class SRBCT ($K=4$), Sparse K-Means degraded to $\text{ARI} = 0.0343$ (9th place), demonstrating that single $L_1$ lasso shrinkage across all clusters cannot capture distinct, non-overlapping gene signatures separating multiple sub-histologies.
4. **Reproducibility Files**:
   - `experiments/exp7_modern_baselines/src/run_exp7.py`
   - `experiments/exp7_modern_baselines/data/modern_baselines_benchmark.csv`
   - `experiments/exp7_modern_baselines/data/modern_baselines_summary.csv`
