# Research Audit 07: Baseline Method Selection, Taxonomy & Protocol Parity

**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Document Reference:** `AUDIT-07-BASELINE-TAXONOMY`  
**Date:** 2026-10-31  

---

## 1. Algorithmic Taxonomy of Evaluated Methods

To ensure an unassailable empirical evaluation for DMKD, algorithms are organized into five distinct families, separating general continuous benchmarks from specialized single-cell manifolds.

```
                                  EVALUATED CLUSTERING TAXONOMY
      ┌──────────────────┬─────────────────┬─────────────────┬──────────────────┬─────────────────┐
      │ 1. Classical     │ 2. Density/Graph│ 3. Feature-Gated│ 4. Consensus/Ens │ 5. Deep Learning│
      ├──────────────────┼─────────────────┼─────────────────┼──────────────────┼─────────────────┤
      │ • K-Means++      │ • HDBSCAN*      │ • Sparse K-Means│ • Std Consensus  │ • DEC           │
      │ • Ward Linkage   │ • Leiden (SNN)  │ • Variance Filt │ • Core-Halo (Li) │ • IDEC          │
      │ • Spectral Graph │ • DBSCAN        │ • PCA-KMeans    │ • CoHiRF         │ • Contrastive Cl│
      │ • Fuzzy C-Means  │                 │ • Laplacian Scr │ • GAC (Proposed) │   (CC)          │
      │ • GMM (BIC/ICL)  │                 │                 │ • FCAG (TPAMI'24)│                 │
      │                  │                 │                 │ • FastMICE       │                 │
      └──────────────────┴─────────────────┴─────────────────┴──────────────────┴─────────────────┘
```

---

## 2. Baseline Inclusion and Exclusion Justifications

| Algorithmic Family | Candidate Method | Selection Status | Primary Rationale & Input Assumptions | Excluded Alternatives & Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Classical** | K-Means (Lloyd 1982 / Arthur 2007) | **Included** | Universal distance-based baseline; k-means++ seeded. | Random-seed Lloyd (obsolete). |
| **Classical** | Ward Agglomerative Linkage (1963) | **Included** | Deterministic minimum-variance hierarchical baseline. | Single/Complete linkage (known to produce chaining). |
| **Classical** | Spectral Clustering (von Luxburg 2007) | **Included** | Standard graph partition baseline on $k$-NN Euclidean graph ($k=10$). | Unnormalized spectral cut (theoretically inferior). |
| **Classical** | Fuzzy C-Means (Bezdek 1981) | **Included** | Continuous fuzzy membership baseline ($m=2.0$). | Hard partition c-means (redundant with K-Means). |
| **Probabilistic** | Gaussian Mixture Models (BIC/ICL) | **Included** | Standard model selection baseline; full and diagonal covariances. | Spherical-only GMM (overly restrictive). |
| **Density & Graph**| HDBSCAN* (Campello 2013, McInnes 2017) | **Included** | Non-parametric density hierarchy; automatically detects noise points. | DBSCAN with fixed $\epsilon$ (fails under varying density). |
| **Density & Graph**| Leiden Community Detection (Traag 2019)| **Included** | Universal bioinformatics standard on PCA-SNN graph ($k=15$, CPM/modularity). | Louvain (can produce disconnected communities). |
| **Feature Selection**| Sparse K-Means (Witten-Tibshirani 2010)| **Included** | Definitive $L_1$ lasso feature-weighting method for $D \gg N$. | Ad-hoc thresholding. |
| **Feature Selection**| Variance-Filtered K-Means | **Included** | Matched-budget $\lfloor \alpha D \rfloor$ filter on marginal sample variance. | Arbitrary variance cutoffs. |
| **Feature Selection**| PCA-Filtered K-Means | **Included** | Unsupervised linear dimensionality reduction to leading $k$ PCs. | Heuristic component selection. |
| **Feature Selection**| Laplacian Score (He et al. 2005) | **Included** | Graph-locality preserving unsupervised feature ranking. | Supervised Fisher criterion (prohibited). |
| **Consensus** | Standard Consensus (Monti 2003 / Fred 2005) | **Included** | Canonical dense co-association matrix with average linkage ($M=25$). | Single-linkage consensus (chaining artifacts). |
| **Consensus** | Core-Halo Consensus (Li et al. 2019) | **Included** | Direct benchmark comparator utilizing co-association stability. | Ad-hoc heuristic voting. |
| **Consensus** | CoHiRF (2024) | **Included** | Hierarchical Random Forest consensus for high-dimensional tabular data. | Unweighted RF consensus. |
| **Consensus** | FCAG (Nie et al. IEEE TPAMI 2024) | **Included** | Scalable anchor-guided bipartite graph clustering. | Dense spectral consensus. |
| **Consensus** | True FastMICE (Huang et al. TKDE 2023) | **Included** | Multi-view bipartite graph factorization solved via ADMM. | FastMVC surrogate (audited and purged from headline claims). |
| **Deep Learning** | DEC (Xie et al. ICML 2016) | **Included** | Autoencoder pretraining + Student's $t$ distribution soft assignments. | Vanilla Autoencoder + K-Means (lacks joint optimization). |
| **Deep Learning** | IDEC (Guo et al. IJCAI 2017) | **Included** | Joint autoencoder reconstruction loss + Student-$t$ clustering loss. | DKM (Deep K-Means, redundant). |
| **Deep Learning** | Contrastive Clustering (Li et al. AAAI 2021) | **Included** | Instance-level and cluster-level dual contrastive self-supervised learning. | SCAN (relies on image-specific $k$-NN augmentations). |

---

## 3. Protocol Parity & Computational Budget Enforcement

To prevent benchmark manipulation and ensure submission-grade fairness:

### 3.1 Protocol A: Standardized Documented Defaults
- Every comparative baseline is benchmarked under its standard, published default hyperparameter configuration.
- No per-dataset label-informed hyperparameter tuning is permitted for any method.
- Ground truth reference labels are quarantined and used strictly after inference to compute external evaluation metrics (ARI, NMI, AMI, FM).

### 3.2 Protocol B: Equal-Budget Unsupervised Tuning
Where hyperparameters require tuning (e.g., sparsity parameter $s$ in Sparse K-Means, resolution $\gamma$ in Leiden, covariance structure in GMM):
- All methods receive an identical tuning budget of **10 function evaluations**.
- Model selection is governed exclusively by **strictly unsupervised criteria**:
  - Sparse K-Means: Permutation Gap Statistic (10 permutations).
  - GMM: Bayesian Information Criterion (BIC).
  - Leiden: Modularity stability across bootstrapped subgraphs.
  - ICC-AutoK: Proportion of Ambiguous Clustering (PAC) on bipartite anchor graph.
- **Strict Prohibition:** Reference labels must never enter hyperparameter selection, feature weighting, or model order discovery.

### 3.3 Hardware Constraints & Resource Quotas
- Classical & Consensus algorithms: Pinned to 1 CPU core (`OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`) to measure pure algorithmic efficiency.
- Deep clustering algorithms: Pinned to 1 dedicated NVIDIA RTX GPU with fixed CUDA deterministic flags (`torch.manual_seed(seed)`, `torch.use_deterministic_algorithms(True)`).
- Execution ceiling: Wall-clock timeout $T_{\max} = 600\text{ s}$ (10 minutes) per dataset-seed pair.
- Peak resident memory ceiling: $M_{\max} = 16.0\text{ GB}$. Runs exceeding this quota are flagged as `OOM` and recorded as failures rather than discarded.
