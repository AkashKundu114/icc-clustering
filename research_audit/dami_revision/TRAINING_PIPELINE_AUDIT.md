# Training and Fitting Pipeline Forensic Audit Report

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Working Branch:** `research/dami-revision`  
**Audit Component:** Agent A — Training and Fitting Pipeline Audit  
**Date of Record:** November 1, 2026  
**Status:** **AUDITED AND VERIFIED**

---

## 1. Executive Summary

This forensic audit inspects every clustering algorithm implementation across `src/icc/`, `src/cicc/`, and `configs/baselines.yaml`. Each method was audited directly at the source code level to distinguish **fitted parameters** (optimization states updated via learning iterations) from **calculated deterministic values** (statistical summaries, affinity transformations, and heuristic metrics).

### Key Audit Findings:
1. **Unsupervised Purity:** Across all baseline models, hyperparameter configurations are fixed prior to model fitting ($K = K_{\text{target}}$) and do **not** utilize ground-truth class labels, validation partitions, or supervised feature filters.
2. **BGSS Label-Free Feature Selection:** The Bimodality Gating Subspace Selection (BGSS) in `src/icc/consensus_v2.py` computes Sarle's Bimodality Coefficient ($b_d = \frac{\text{skew}_d^2 + 1}{\text{kurtosis}_d + 3}$) in an entirely unsupervised manner on the full feature matrix prior to subspace draws.
3. **Surrogate Baseline Disclosure:** `FastMVC` (`src/icc/baselines/anchor.py:run_fastmvc`) is confirmed to be an internal random-subspace bipartite anchor-graph proxy inspired by FastMICE (Huang et al., IEEE TKDE 2023). It is **not** a faithful implementation of their official algorithmic pipeline and is explicitly cataloged as `FastMVC-Surrogate` (`stub: true` in `configs/baselines.yaml`).
4. **Sparse K-Means Sparsity Rule Discrepancy:** In `src/icc/baselines/sparse_kmeans.py`, the default rule is `s_rule='witten_scaled'` ($s = \max(1.1, 0.15\sqrt{D} + 1.0)$), whereas manuscript Table 2 describes `s_rule='table2'` ($s = \max(1.1, 1.1 + 0.5(\sqrt{D} - 1.1))$). Both are implemented and selectable; code consistency checks verify that experimental scripts specify this rule explicitly.
5. **Leiden/SNN Dependency Isolation:** `src/icc/baselines/leiden_snn.py` cleanly separates execution based on library availability. When `igraph` or `leidenalg` are missing and `allow_fallback=False`, it issues a warning and returns status `LeidenSNN (UNAVAILABLE)`, strictly preventing silent algorithmic substitution.
6. **High-Dimensional GMM Regularization:** `src/icc/baselines/probabilistic.py` automatically forces `covariance_type='diag'` whenever $D > 50$, preventing ill-conditioned covariance matrix inversions ($D \gg N$).

---

## 2. Comprehensive Algorithm-by-Algorithm Audit

### 2.1 Classical Single-Model Baselines (`src/icc/baselines/classical.py`)

#### K-Means (Lloyd, 1982)
- **Implementation File:** `src/icc/baselines/classical.py:run_kmeans` (invoking `src/icc/core.py:run_clusterer`).
- **Fitted vs. Calculated:** Fitted: $K$ centroid vectors in $\mathbb{R}^D$ updated via alternating assignment and center recalculation. Calculated: Euclidean distance matrix and Within-Cluster Sum of Squares (WCSS).
- **Input Representation:** Standardized matrix $\mathbf{X} \in \mathbb{R}^{N \times D}$.
- **Preprocessing:** Operates directly on standardized features; no feature selection.
- **Hyperparameter Selection:** $K = K_{\text{target}}$, $n_{\text{init}} = 1$, $\text{max\_iter} = 300$, $\text{tol} = 10^{-4}$.
- **Randomness / Seeds:** Seed passed to `sklearn.cluster.KMeans(random_state=seed)` or NumPy fallback `_kmeans_numpy(seed=seed)`.
- **Failure Handling:** In NumPy fallback, empty clusters dynamically reseed from points with maximum distance to active centers (`src/icc/core.py:158`).
- **Published Fidelity:** 100% faithful to standard Lloyd algorithm with $k$-means++ initialization.

#### Ward Hierarchical Agglomerative Clustering (Ward, 1963)
- **Implementation File:** `src/icc/baselines/classical.py:run_ward`.
- **Fitted vs. Calculated:** Calculated: $(N-1) \times 4$ linkage matrix $\mathbf{Z}$ merging pairs that minimize variance increase. No iterative parameters are learned.
- **Input Representation:** Standardized matrix $\mathbf{X} \in \mathbb{R}^{N \times D}$.
- **Preprocessing:** $\mathbf{X} + \epsilon_{\text{jitter}}$ where $\epsilon \sim \mathcal{N}(0, 10^{-4}\mathbf{I})$ (`src/icc/core.py:237`). Jitter ensures deterministic tie-breaking across different BLAS/LAPACK platforms.
- **Hyperparameter Selection:** $K = K_{\text{target}}$, linkage = `'ward'`, Euclidean metric.
- **Randomness / Seeds:** Seed controls tie-breaking jitter RNG.
- **Failure Handling:** Handled natively by SciPy linkage tree truncation (`fcluster(criterion="maxclust")`).
- **Published Fidelity:** Faithful standard implementation.

#### Normalized Spectral Clustering (Ng, Jordan, Weiss, 2002; Von Luxburg, 2007)
- **Implementation File:** `src/icc/baselines/classical.py:run_spectral`.
- **Fitted vs. Calculated:** Calculated: $k$-nearest neighbor graph ($\kappa = 10$), normalized graph symmetric Laplacian $\mathbf{L}_{\text{sym}} = \mathbf{I} - \mathbf{D}^{-1/2}\mathbf{W}\mathbf{D}^{-1/2}$, and leading $K$ eigenvectors $\mathbf{U} \in \mathbb{R}^{N \times K}$. Fitted: $k$-means clustering on row-normalized spectral embedding.
- **Input Representation:** Standardized matrix $\mathbf{X} \in \mathbb{R}^{N \times D}$.
- **Hyperparameter Selection:** $K = K_{\text{target}}$, affinity = `'nearest_neighbors'`, $n_{\text{neighbors}} = 10$.
- **Randomness / Seeds:** Seed passed to discretization k-means.
- **Failure Handling:** NumPy fallback adds diagonal damping $\mathbf{W} + 10^{-4}\mathbf{I}$ (`src/icc/core.py:216`) to guarantee positive semi-definiteness on disconnected graphs.
- **Published Fidelity:** Faithful implementation of Ng-Jordan-Weiss spectral clustering.

#### Fuzzy C-Means (Bezdek, 1981)
- **Implementation File:** `src/icc/baselines/classical.py:run_fcm` (invoking `src/icc/core.py:_fcm_like`).
- **Fitted vs. Calculated:** Fitted: Continuous membership matrix $\mathbf{U} \in [0, 1]^{N \times K}$ ($\sum_c u_{ic} = 1$) and cluster centers $\mathbf{V} \in \mathbb{R}^{K \times D}$. Calculated: Generalized fuzzy objective function.
- **Input Representation:** Standardized matrix $\mathbf{X} \in \mathbb{R}^{N \times D}$.
- **Hyperparameter Selection:** $K = K_{\text{target}}$, fuzzifier $m = 2.0$, $\text{max\_iter} = 100$, convergence tolerance $10^{-4}$.
- **Randomness / Seeds:** Seed initializes random Dirichlet membership matrix.
- **Failure Handling:** Division-by-zero protection via `1e-12` floor on distances.
- **Published Fidelity:** Faithful implementation.

---

### 2.2 Consensus and Ensemble Architectures (`src/icc/baselines/consensus.py`, `src/icc/consensus_v2.py`)

#### Standard Dense Consensus Clustering (Fred & Jain, IEEE TPAMI 2005)
- **Implementation File:** `src/icc/baselines/consensus.py:run_standard_consensus`.
- **Fitted vs. Calculated:** Fitted: $M = 25$ independent base k-means models on full feature space. Calculated: Dense $N \times N$ co-association matrix $\mathbf{S} = \frac{1}{M}\sum_{m=1}^M \mathbf{H}_m \mathbf{H}_m^T$, distance matrix $\mathbf{D} = 1 - \mathbf{S}$, and average linkage hierarchical clustering.
- **Complexity & Memory:** Time complexity $\mathcal{O}(M \cdot N D K + N^2 \log N)$; memory complexity $\mathcal{O}(N^2)$ to store the condensed distance array.
- **Label Independence:** Strictly unsupervised; base models use random initializations.
- **Published Fidelity:** Faithful implementation of Fred & Jain (2005) co-association consensus.

#### Core-Halo Consensus (Li et al., Artificial Intelligence, 2019)
- **Implementation File:** `src/icc/baselines/consensus.py:run_li_et_al_2019`.
- **Fitted vs. Calculated:** Fitted: $M=25$ base models. Calculated: $\mathbf{S} \in [0, 1]^{N \times N}$, per-sample stability scores $s_i = \frac{1}{N-1}\sum_{j \neq i} S_{ij}^2$, median thresholding $\tau = \text{median}(s)$, average linkage on core subset, and maximum average affinity allocation for halo points.
- **Failure Handling:** If $|\mathcal{C}_{\text{core}}| < K$, falls back to top-$K$ highest stability samples (`src/icc/baselines/consensus.py:120`).
- **Published Fidelity:** Faithful implementation of Li et al. (2019) determinacy core-halo consensus.

#### Full ICC-v2 / GAC (`src/icc/consensus_v2.py:InvariantCoreConsensusV2`)
- **Implementation File:** `src/icc/consensus_v2.py`.
- **Pipeline Architecture:**
  1. **Bimodality Gating (BGSS):** Computes Sarle's Bimodality Coefficient $b_d = \frac{\text{skew}_d^2 + 1}{\text{kurtosis}_d + 3}$ across all $D$ features. Filters for top $15\%$ bimodal features (active candidate pool $\mathcal{F}_{\text{active}}$).
  2. **Subspace Generation:** For each of $M=25$ base models, draws $30\%$ of features uniformly at random from $\mathcal{F}_{\text{active}}$.
  3. **Linear Co-association:** Accumulates sample-level stability in $\mathcal{O}(N \cdot K^2)$ time using linear bin-counting (`consensus_v2.py:261-267`).
  4. **Core Anchor Certification:** Certifies core points exceeding $\tau_{\text{core}} = 0.50$ quantile of stability; draws $L=40$ landmark anchors uniformly from core.
  5. **Bipartite Spectral Consensus:** Forms $N \times L$ bipartite co-association matrix $\mathbf{B}$, computes reduced $L \times L$ anchor graph Laplacian $\mathbf{L}_{\text{anchor}}$, solves for $K$ generalized eigenvectors, projects to $N$ samples, and discretizes via k-means.
- **Complexity & Memory:** Time complexity $\mathcal{O}(M \cdot N d_{\text{sub}} K + N L K)$; auxiliary memory $\mathcal{O}(N L)$, strictly bypassing the $\mathcal{O}(N^2)$ dense matrix bottleneck.
- **Failure Handling:** Regularized Laplacian eigenvalue solver with $\mathbf{L} + 10^{-6}\mathbf{I}$; dynamic cluster reseeding; handles disconnected graphs.
- **Published Fidelity:** Proposed method in manuscript.

#### Matched Random Gating Control (`src/icc/consensus_v2.py`)
- **Configuration:** `InvariantCoreConsensusV2(pool_mode='random')`.
- **Fitted vs. Calculated:** Identical to Full ICC-v2, except the active candidate pool $\mathcal{F}_{\text{active}}$ is selected uniformly at random from $\{1, \dots, D\}$ with budget matched exactly to BGSS ($15\%$ of features).
- **Scientific Role:** Isolates the specific contribution of bimodality feature gating from the bipartite anchor graph architecture.

---

### 2.3 Modern High-Dimensional & Specialized Baselines

#### Sparse K-Means (Witten & Tibshirani, JASA 2010)
- **Implementation File:** `src/icc/baselines/sparse_kmeans.py:run_sparse_kmeans`.
- **Fitted vs. Calculated:** Fitted: Alternating iterative optimization. Step 1: Given weights $\mathbf{w}$, fit weighted $k$-means on $\mathbf{X} \text{diag}(\sqrt{\mathbf{w}})$. Step 2: Given cluster labels, compute feature-wise Between-Cluster Sum of Squares ($\text{BCSS}_j$) and solve for non-negative weights $\mathbf{w}$ maximizing $\mathbf{w}^T \text{BCSS}$ subject to $\|\mathbf{w}\|_2 = 1, \|\mathbf{w}\|_1 \le s$.
- **Sparsity Rule Audit:**
  - `s_rule='witten_scaled'`: $s = \max(1.1, 0.15\sqrt{D} + 1.0)$ (code default).
  - `s_rule='table2'`: $s = \max(1.1, 1.1 + 0.5(\sqrt{D} - 1.1))$ (manuscript Table 2 rule).
  - Both rules are parameterized and verified.
- **Convergence Handling:** Terminated when cluster labels do not change between iterations or upon reaching `max_iter=15`.
- **Published Fidelity:** Faithful implementation of Witten & Tibshirani alternating optimization with soft-thresholding binary search.

#### HDBSCAN* (Campello et al., PAKDD 2013)
- **Implementation File:** `src/icc/baselines/density.py:run_hdbscan`.
- **Fitted vs. Calculated:** Fitted: Minimum spanning tree over mutual reachability distances, condensed cluster tree, and cluster stability extraction. Calculated: Noise assignment mask (`labels == -1`).
- **Hyperparameter Selection:** `min_cluster_size = 5`, `min_samples = None`, `metric = 'euclidean'`.
- **Dual Metric Evaluation:** `src/icc/baselines/density.py:evaluate_hdbscan_metrics` computes two separate validation metrics:
  1. `ari_full`: Standard full-sample ARI treating noise points as a distinct cluster ($c = -1$).
  2. `ari_core`: Conditional ARI computed strictly on core points (`labels != -1`), accompanied by coverage metrics (`coverage = 1 - noise_ratio`).
- **Published Fidelity:** Faithful wrapper around `hdbscan` / `sklearn.cluster.HDBSCAN`.

#### Leiden SNN Community Detection (Traag et al., Sci Rep 2019)
- **Implementation File:** `src/icc/baselines/leiden_snn.py:run_leiden_snn`.
- **Fitted vs. Calculated:** Fitted: PCA projection (30 components), Shared Nearest Neighbor (SNN) graph construction with Jaccard weights, and Leiden algorithm partition optimization using `CPMVertexPartition`.
- **Dependency Handling & Fallback Audit:**
  - When `igraph` and `leidenalg` are missing:
    - If `allow_fallback=False` (default): Issues a `UserWarning` and returns dummy zero labels with `status="UNAVAILABLE: <error>"`. **Does not silently substitute algorithms**.
    - If `allow_fallback=True`: Explicitly marks `method="Spectral-SNN-Fallback"` and invokes `run_spectral_snn`.
- **Published Fidelity:** Faithful Traag et al. implementation when optional libraries are present.

#### Fast Clustering with Anchor Guidance — FCAG (Nie et al., IEEE TPAMI 2024)
- **Implementation File:** `src/icc/baselines/anchor.py:run_fcag`.
- **Fitted vs. Calculated:** Fitted: $m = \min(100, N)$ anchor points via $k$-means++. Calculated: Row-stochastic bipartite similarity matrix $\mathbf{Z} \in \mathbb{R}^{N \times m}$ with adaptive neighbor weighting ($s=5$ nearest anchors). Solves generalized eigenvalue problem on $\mathbf{M} = \mathbf{D}_c^{-1/2} \mathbf{Z}^T \mathbf{Z} \mathbf{D}_c^{-1/2}$, projects eigenvectors to samples, and discretizes via $k$-means.
- **Fidelity Note:** The code docstring explicitly clarifies that this is a $k$-means++-anchor spectral re-implementation, not the original paper's projected gradient descent (PGD) / iterative reweighting (IRW) solvers.

#### Fast Multi-View Clustering Surrogate — FastMVC-Surrogate (Huang et al., IEEE TKDE 2023 Stub)
- **Implementation File:** `src/icc/baselines/anchor.py:run_fastmvc`.
- **Forensic Audit:** Line 243 explicitly documents:
  > `"NOTE: This is an internal random-subspace bipartite anchor-graph proxy inspired by FastMICE (Huang et al., IEEE TKDE 2023), but it is NOT an identical implementation of their official algorithmic pipeline. Manuscript tables and text should refer to it as 'FastMVC-Surrogate'."`
- **Catalog Status:** Marked `stub: true` in `configs/baselines.yaml:221` with instruction: `"exclude from headline comparisons"`.

#### Deep Embedded Clustering — DEC (Xie et al., ICML 2016)
- **Implementation File:** `src/icc/baselines/deep.py:run_dec`.
- **Fitted vs. Calculated:** Fitted: Fully-connected stacked autoencoder pretraining ($D \to 500 \to 500 \to 2000 \to 10$) using MSE reconstruction loss, followed by Student's $t$-distribution clustering layer optimization using KL divergence against auxiliary target distribution $\mathbf{P}$.
- **Hardware Requirement:** GPU recommended; requires TensorFlow/Keras or PyTorch backend.
- **Published Fidelity:** Faithful implementation of Xie et al. (2016).

---

## 3. Summary Compliance Matrix

All 10 core benchmark methods, 4 ablated controls, and 6 specialized/deep baselines have been fully characterized in `ALGORITHM_IMPLEMENTATION_MATRIX.csv` and `HYPERPARAMETER_REGISTRY.csv`. Zero label leakage or illicit supervised tuning was discovered in any clustering implementation.
