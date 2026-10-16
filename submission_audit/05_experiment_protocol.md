# 05 — Frozen Confirmatory Protocol & Preregistration

**Protocol Version:** 2.0 (Post-Audit Frozen Standard)  
**Date:** October 13, 2026  
**Status:** FROZEN  

---

## 1. Frozen Experimental Benchmarking Specification

To prevent post-hoc tuning or selective reporting, all future confirmatory evaluations must adhere strictly to this protocol:

### A. Dataset Inclusion & Stratification
- **Primary 13 Multi-Domain Suite:** CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT, Sonar, Madelon, 20 Newsgroups, Isolet, Indian Pines, Extended Yale B, Zheng68k.
- **Extended 21 Supplementary Suite:** Lymphoma, Lung Cancer, Glioma, Breast Cancer Genomic, Gisette, Waveform, HAR, USPS.
- **Operating Subgroup Rule:** Regimes are classified strictly by ambient dimensionality ratio:
  - High-dimensional biomedical subgroup: $D/N > 20$.
  - Large-sample / multi-class subgroup: $N > 5{,}000$ or $K \ge 20$.

### B. Standardized Preprocessing
- Count and expression data: $\log_2(X + 1)$ transformed where appropriate (as cataloged in `data/registry.yaml`).
- All continuous features: Per-feature standard score (zero mean, unit variance) fitted strictly on the transductive training split.
- Sparse features: Standardized using `with_mean=False` to preserve sparse matrix structure.

### C. Confirmatory Baselines & Configuration
1. **K-Means:** `KMeans(n_clusters=K, init='k-means++', n_init=10, random_state=seed)`
2. **Ward Linkage:** `AgglomerativeClustering(n_clusters=K, linkage='ward')`
3. **Spectral Clustering:** `SpectralClustering(n_clusters=K, affinity='nearest_neighbors', random_state=seed)`
4. **Fuzzy C-Means (FCM):** Standard fuzzy partition matrix with fuzzifier $m=2.0$.
5. **Standard Consensus (Std Cons):** Dense $N \times N$ co-association matrix with average-linkage hierarchical agglomeration ($M=50$).
6. **Li et al. (TKDE 2019):** Determinacy core non-negative matrix factorization.
7. **DEC (ICML 2016):** Deep Embedded Clustering with autoencoder pre-training (100 epochs) and clustering refinement (50 epochs).
8. **FCAG (TPAMI 2024):** Fast Clustering with Anchor Guidance ($L=40$).
9. **FastMVC (TKDE 2023):** Fast multi-view ensemble clustering with bipartite graph partitioning.
10. **ICC-v2 (Proposed):** Gated subspace ensembling with Proposition 2 determinacy anchors ($L=\max(40, 10K)$) and Transfer-Cut bipartite spectral embedding.

### D. Primary & Secondary Outcomes
- **Primary Metric:** Adjusted Rand Index (ARI).
- **Secondary Metrics:** Normalized Mutual Information (NMI), Adjusted Mutual Information (AMI), Fowlkes-Mallows Index (FMI), Clustering Accuracy (ACC).
- **Efficiency Metrics:** Peak auxiliary RAM consumption (MB), Wall-clock execution time (seconds).

### E. Confirmatory Statistical Testing
- Omnibus Test: Non-parametric Friedman test across all evaluated algorithms on the 13 benchmarks.
- Post-hoc Pairwise: Two-tailed Demšar Critical Difference diagram with Nemenyi test at $\alpha = 0.05$.
- Subgroup Testing: Wilcoxon signed-rank test on paired differences across the $D/N > 20$ subgroup.
