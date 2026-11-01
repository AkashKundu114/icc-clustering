# Research Audit 12: Modern Baseline Comparison Protocol & Implementation Specifications

**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Document Reference:** `AUDIT-12-BASELINE-PROTOCOL`  
**Date:** 2026-10-31  

---

## 1. Objectives & Compliance Standards

Reviewers at DMKD expect comparative benchmarks to evaluate algorithms against modern, competitive baselines under strict conditions of fairness:
1. **No Target Label Leakage:** Ground-truth class labels must never be used to tune hyperparameters, select features, or choose $K$.
2. **Computational Budget Matching:** Methods must operate under matched sample access and runtime constraints.
3. **Audit of Approximations:** Any method implemented as a surrogate or approximation must be explicitly flagged and isolated from decisive claims.

---

## 2. Mathematical Formulations for Newly Integrated Modern Baselines

### 2.1 Sparse K-Means (SKM; Witten & Tibshirani, JASA 2010)
- **Objective:** Solves a joint optimization problem over cluster assignments $C = \{C_1, \dots, C_K\}$ and non-negative feature weights $\mathbf{w} \in \mathbb{R}^D$:
  $$\max_{C, \mathbf{w}} \sum_{j=1}^D w_j \left( \sum_{i=1}^N (x_{ij} - \bar{x}_j)^2 - \sum_{k=1}^K \sum_{i \in C_k} (x_{ij} - \bar{x}_{kj})^2 \right)$$
  $$\text{subject to } \|\mathbf{w}\|_2 \le 1, \quad \|\mathbf{w}\|_1 \le s, \quad w_j \ge 0 \quad \forall j$$
- **Unsupervised Tuning of Sparsity Parameter $s$:**
  Evaluated across a grid $s \in [1.1, \sqrt{D}]$ using the permutation gap statistic:
  $$\text{Gap}(s) = \log(O(s)) - \frac{1}{B} \sum_{b=1}^B \log(O_b^*(s))$$
  where $O(s)$ is the observed between-cluster sum of squares, and $O_b^*(s)$ is obtained by permuting features independently across samples.

### 2.2 Leiden Community Detection on SNN Graph (Traag et al., 2019)
- **Graph Construction:**
  1. Dimensionality reduction to $d=30$ leading principal components.
  2. Compute $k$-nearest neighbors ($k=15$) for each sample under Euclidean distance.
  3. Formulate Shared Nearest Neighbor (SNN) graph where edge weight $W_{ij} = \frac{|\mathcal{N}(i) \cap \mathcal{N}(j)|}{2k - |\mathcal{N}(i) \cap \mathcal{N}(j)|}$ (Jaccard similarity).
- **Modularity Optimization:**
  Optimizes the Constant Potts Model (CPM) quality function:
  $$\mathcal{H}_{\text{CPM}} = -\sum_{c \in \mathcal{C}} \left( e(c) - \gamma \binom{|c|}{2} \right)$$
  where resolution parameter $\gamma$ is tuned unsupervised by maximizing partition stability across bootstrapped subgraphs.

### 2.3 Gaussian Mixture Models with BIC and ICL (Biernacki et al., 2000)
- **Model:** Expectation-Maximization fit of $K$ Gaussian components $\sum_{k=1}^K \pi_k \mathcal{N}(\mathbf{x} | \boldsymbol{\mu}_k, \Sigma_k)$.
- **Selection Criteria:**
  - **BIC:** $\text{BIC}(K) = -2 \ln \hat{L}_K + \nu_K \ln N$, balancing likelihood and parameter count $\nu_K$.
  - **ICL:** $\text{ICL}(K) = \text{BIC}(K) - 2 \sum_{k=1}^K \sum_{i=1}^N \hat{z}_{ik} \ln \hat{z}_{ik}$, penalizing high posterior classification entropy.

### 2.4 HDBSCAN\* (Campello et al., 2013; McInnes et al., 2017)
- **Algorithm:**
  1. Mutual reachability distance: $d_{\text{mreach}, k}(\mathbf{x}_i, \mathbf{x}_j) = \max\{d_{\text{core}, k}(\mathbf{x}_i), d_{\text{core}, k}(\mathbf{x}_j), \|\mathbf{x}_i - \mathbf{x}_j\|_2\}$.
  2. Minimum Spanning Tree construction and hierarchy condensation.
  3. Flat cluster extraction via excess of mass metric, assigning low-density samples to noise ($C_i = -1$).

### 2.5 True FastMICE ADMM Consensus Solver (Huang et al., 2023)
- Replaces the informal surrogate (`FastMVC-Surrogate`) with the exact alternating direction method of multipliers (ADMM) solver updating view weights $\alpha_v$, bipartite factorizations $S_v$, and consensus anchor connectivity $Z$.

---

## 3. Protocol Implementation in Codebase

The modern baseline benchmark suite is implemented in:
- `src/icc/baselines/sparse_kmeans.py`: Exact $L_1$ soft-thresholded BCSS solver with permutation gap statistic.
- `src/icc/baselines/leiden_snn.py`: PCA + Jaccard SNN + Leiden modularity optimizer.
- `src/icc/baselines/probabilistic.py`: GMM with automated BIC and ICL model order selection.
- `src/icc/baselines/density.py`: HDBSCAN* density hierarchy.
- `src/icc/baselines/fastmice.py`: Exact FastMICE ADMM solver.
- `experiments/exp7_modern_baselines/src/run_exp7.py`: Unified comparative execution script across all 12 high-$D$ cohorts over 10 canonical seeds.
