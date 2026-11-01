# Research Audit 13: Genuinely Unsupervised Model Order Selection Protocol (EXP8 / EXP6)

**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Document Reference:** `AUDIT-13-UNKNOWN-K-PROTOCOL`  
**Date:** 2026-10-31  

---

## 1. Scientific Motivation & Problem Statement

Consensus clustering was originally formulated by Monti et al. (Machine Learning 2003) as an unsupervised tool for discovering the latent number of clusters $K$. Yet, earlier drafts of the ICC/GAC manuscript evaluated clustering only under oracle conditions where true $K = K^*$ is known a priori.

This created a major scientific vulnerability:
- Şenbabaoğlu et al. (Sci Rep 2014) demonstrated that consensus clustering on pure Gaussian noise frequently generates an illusory peak in consensus stability at $K = 2$.
- In high dimensions ($D \gg N$), distance concentration flattens geometric contrast, potentially tricking model order criteria (PAC, Silhouette, BIC) into deceptive high-stability / low-accuracy attractors.
- **The Core Scientific Question:** Does feature gating (BGSS) protect against the unknown-$K$ discordance trap by preserving multi-modal coordinate structure, or does it introduce false modes?

---

## 2. Mathematical Formulation of ICC-AutoK

ICC-AutoK discovers the optimal cluster count $\hat{K}$ purely unsupervised using the **Proportion of Ambiguous Clustering (PAC)** evaluated on the consensus graph:

### 2.1 Consensus Cumulative Distribution Function (CDF)
For candidate cluster count $k \in \{2, 3, \dots, K_{\max}\}$, let $S^{(k)} \in [0, 1]^{N \times N}$ denote the consensus co-association matrix over $M$ base iterations:
$$F^{(k)}(c) = \frac{2}{N(N-1)} \sum_{1 \le i < j \le N} \mathbb{I}(S_{ij}^{(k)} \le c), \quad c \in [0, 1]$$
Under an ideal clustering, all pairs have co-association $S_{ij} \in \{0, 1\}$, resulting in a flat CDF curve between 0 and 1.

### 2.2 Proportion of Ambiguous Clustering (PAC)
PAC quantifies the fraction of sample pairs with unstable, intermediate co-assignment:
$$\text{PAC}(k) = F^{(k)}(u_2) - F^{(k)}(u_1), \quad \text{where } u_1 = 0.10, \; u_2 = 0.90$$
The optimal model order minimizes ambiguity:
$$\hat{K}_{\text{PAC}} = \arg\min_{k \in \{2, \dots, K_{\max}\}} \text{PAC}(k)$$

### 2.3 Linear-Memory Anchor PAC Acceleration
Evaluating $S_{ij}$ over all $\binom{N}{2}$ pairs requires $O(N^2)$ operations. In ICC-AutoK, we exploit the bipartite anchor representation $\tilde{B} \in \mathbb{R}^{N \times L}$:
- Uniformly sample $M_{\text{pairs}} = 10{,}000$ instance pairs $\mathcal{P} \subset \binom{[N]}{2}$.
- Approximate co-association in $O(L)$ time: $\hat{S}_{ij} = \sum_{l=1}^L \tilde{B}_{il} \tilde{B}_{jl}$.
- Compute $\widehat{\text{PAC}}(k)$ in $O(|\mathcal{P}| \cdot L)$ time and $O(1)$ auxiliary storage.

---

## 3. Synthetic Experimental Design (560-Run Phase Grid)

To isolate how noise, cluster count, and geometric imbalance affect model selection:

| Factor | Grid Levels | Physical / Geometric Rationale |
| :--- | :--- | :--- |
| **True Cluster Count ($K^*$)** | $K^* \in \{2, 3, 4, 5, 8, 10, 15\}$ | Spans small binary targets to large multi-class regimes. |
| **Cluster Balance** | Equal ($N_k = N/K$) vs. Unequal ($\boldsymbol{\pi} \sim \text{Dirichlet}(0.5)$) | Tests sensitivity to minority cluster collapse. |
| **Covariance Structure** | Isotropic ($\Sigma_k = I$) vs. Anisotropic ($\sigma_k^2 \in [0.5, 3.0]$, random rotation) | Tests non-spherical and heterogeneous cluster densities. |
| **Distractor Noise ($D_{\text{noise}}$)** | $D_{\text{noise}} \in \{0, 100, 1000, 5000\}$ continuous Gaussian/Laplacian noise | Simulates the transition from clean geometry to extreme distance concentration ($D/N = 16.7$). |
| **Sample Size ($N$)** | $N = 300$ instances per dataset | Fixed baseline scale across 5 independent seeds. |

Total Synthetic Configurations: $7 \times 2 \times 2 \times 4 \times 5 = \mathbf{560 \text{ independent runs}}$.

---

## 4. Evaluated Comparative Model Selectors

Every method searches over candidate grid $K \in \{2, 3, \dots, K_{\max}\}$ ($K_{\max} = \min(16, \lfloor N/10 \rfloor)$):
1. **ICC-AutoK (Proposed):** Anchor-accelerated PAC minimization on GAC consensus graph.
2. **HDBSCAN\*:** Flat cluster extraction without pre-specified $K$; count $\hat{K} = |\{c \in \mathcal{C} : c \neq -1\}|$.
3. **GMM with BIC:** $\hat{K}_{\text{BIC}} = \arg\min_k \text{BIC}(k)$ over diagonal and full covariance models.
4. **GMM with ICL:** $\hat{K}_{\text{ICL}} = \arg\min_k \text{ICL}(k)$ with assignment entropy penalty.
5. **Spectral Eigengap Heuristic:** $\hat{K}_{\text{Eigen}} = \arg\max_{k} (\lambda_{k+1} - \lambda_k)$ on normalized graph Laplacian.
6. **Hierarchical Dynamic Cut:** Dynamic tree cut on Ward dendrogram (Langfelder et al. 2008).
7. **X-Means:** Pelleg & Moore (2000) recursive KD-tree splitting based on local BIC tests.

---

## 5. Primary Evaluation Metrics

1. **Exact $K$ Recovery Accuracy:** $\text{Acc}_K = \mathbb{I}(\hat{K} = K^*)$.
2. **Absolute $K$ Estimation Error:** $\Delta K = |\hat{K} - K^*|$.
3. **Relative Error Ratio:** $\epsilon_K = \frac{|\hat{K} - K^*|}{K^*}$.
4. **External Clustering Accuracy at $\hat{K}$:** $\text{ARI}(\mathbf{y}_{\text{true}}, \hat{\mathbf{y}}_{\hat{K}})$ evaluated *after* selection is frozen.
5. **Discordance at Estimated $\hat{K}$:** $\mathcal{D}_{\hat{K}} = \text{Stab}(\hat{K}) - \text{ARI}(\hat{K})$, directly evaluating whether model order selection is tricked by artificial stability peaks.
