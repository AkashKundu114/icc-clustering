# Overnight Research Audit: Modern & Classical Baseline Audit

**Document Reference:** `research_audit/overnight/BASELINE_AUDIT.md`  
**Related Results:**  
- `research_audit/overnight/BASELINE_RESULTS.md` (To be produced post-execution)  
- `results/overnight/baselines/`  
**Audit Date:** 2026-11-01  
**Auditor:** Agent C — Modern Baseline Auditor  

---

## 1. Inventory & Faithfulness Audit of Available Baselines

A thorough code audit of `src/icc/baselines/` and `configs/baselines.yaml` was conducted to establish the genuine methodological standing of each baseline:

| Method | Source Module | Primary Reference | Algorithmic Category | Implementation Status | Faithfulness Rating |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **K-Means** | `classical.py` | Lloyd (1982) | Classical Partitional | scikit-learn `KMeans(init='k-means++')` | Faithful (Standard reference) |
| **Ward Hierarchical** | `classical.py` | Ward (1963) | Agglomerative Hierarchical | scikit-learn `AgglomerativeClustering(linkage='ward')` | Faithful (Exact minimum variance) |
| **Spectral Clustering** | `classical.py` | Ng, Jordan, Weiss (2001) | Graph / Eigenspace | scikit-learn `SpectralClustering(affinity='rbf')` | Faithful (Normalized Laplacian) |
| **Fuzzy C-Means (FCM)** | `classical.py` | Bezdek (1981) | Soft Partitional | Vectorized objective minimization | Faithful (Standard $m=2.0$) |
| **Standard Consensus** | `consensus.py` | Monti et al. (2003) | Ensemble Consensus | Subspace subsampling + average co-association | Faithful (Monti consensus matrix) |
| **Sparse K-Means** | `sparse_kmeans.py` | Witten & Tibshirani (2010) | Sparse Subspace Selection | Iterative BCSS optimization with L1/L2 weights | **Faithful** (Implements exact Algorithm 1 from JASA 2010) |
| **HDBSCAN\*** | `density.py` | Campello, Moulavi, Sander (2013) | Density Hierarchy | `hdbscan.HDBSCAN(min_cluster_size=5)` | Faithful (Mutual reachability graph) |
| **GMM with BIC** | `probabilistic.py` | Schwarz (1978) | Model-Based Gaussian Mixture | scikit-learn `GaussianMixture(covariance_type='diag')` | Faithful (Diagonal cov for high-D) |
| **Leiden SNN** | `leiden_snn.py` | Traag et al. (2019) | Shared Nearest Neighbor Graph | Jaccard SNN + modularity optimization | Faithful (SNN graph community detection) |
| **FastMVC** | `anchor.py` | Surrogate Implementation | Multi-view anchor graph | Synthetic anchor projection | **Surrogate Only** (Do NOT represent as exact FastMICE) |

---

## 2. Deep Dive: Sparse K-Means Implementation Faithfulness

Inspection of `src/icc/baselines/sparse_kmeans.py` verifies that the implementation faithfully reproduces Witten & Tibshirani (JASA 2010, *A Framework for Feature Selection in Clustering*):
1. **Between-Cluster Sum of Squares (BCSS):** Features are weighted by $w_j \ge 0$ maximizing $\sum_j w_j \text{BCSS}_j$ subject to $\|w\|_2 \le 1, \|w\|_1 \le s$, and $w_j \ge 0$.
2. **Soft-Thresholding Operator:** Implements $\mathcal{S}(a, \Delta) = \text{sign}(a)(|a| - \Delta)_+$ with binary search for the Lagrange multiplier $\Delta$ matching the L1 bound $s = \sqrt{D} \times 0.3$.
3. **Alternating Optimization:** Alternates between standard K-Means clustering in weighted space and closed-form weight vector updates until convergence.

---

## 3. Fair Comparison & Metric Protocol

To ensure unimpeachable scientific fairness across all baselines:
1. **Known-K Protocol:** All fixed-K algorithms (K-Means, Ward, Spectral, FCM, Standard Consensus, Sparse K-Means, ICC) receive the exact true $K$ ground truth.
2. **Unknown-K Distinction:** Methods that automatically estimate $K$ (HDBSCAN*, GMM-BIC, Leiden SNN, ICC-AutoK) are explicitly reported in an unknown-K evaluation table; their estimated cluster count is recorded alongside performance metrics.
3. **Identical Preprocessing:** All methods receive the identical Z-score standardized matrix ($X \in \mathbb{R}^{N \times D}$) with the same random seeds ($S \in \{42, 101, 202, 303, 404\}$).
4. **Comprehensive Metric Suite:** Metrics recorded include:
   - Supervised Agreement: Adjusted Rand Index (ARI), Normalized Mutual Information (NMI), Adjusted Mutual Information (AMI), Fowlkes-Mallows Index (FM).
   - Unsupervised Topology: Silhouette Coefficient, Davies-Bouldin Index (DB), Calinski-Harabasz Index (CH).
   - Computational Footprint: Execution runtime in seconds, memory utilization.
