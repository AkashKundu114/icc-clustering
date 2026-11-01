# Overnight Research Audit: Unknown-K Model Order Selection Benchmark Design

**Document Reference:** `research_audit/overnight/UNKNOWN_K_DESIGN.md`  
**Related Results:**  
- `research_audit/overnight/UNKNOWN_K_RESULTS.md` (To be produced post-execution)  
- `results/overnight/unknown_k/`  
**Audit Date:** 2026-11-01  
**Auditor:** Agent D — Unknown-K Experiment Designer  

---

## 1. Scientific Motivation & Problem Statement

In classical clustering literature, algorithms are routinely provided the ground-truth number of clusters $K^*$, reducing the task to partition optimization. In actual biomedical discovery, **the true number of molecular subtypes $K^*$ is strictly unknown**.

A critical scientific gap identified in the ICC-Clustering manuscript was the **complete absence of an unknown-K evaluation**. This audit establishes a rigorous, leak-free benchmark evaluating how accurately algorithms estimate $K$ in unsupervised high-dimensional manifolds submerged in noise.

---

## 2. Unsupervised Model Order Selection Protocol

### Strict Safeguards:
1. **Zero Access to Ground-Truth Labels:** True class labels and the true $K^*$ are strictly isolated in a post-hoc evaluation harness; no model selection routine or hyperparameter search receives $K^*$.
2. **Search Range:** All candidate algorithms explore candidate cluster counts $K \in \{2, 3, 4, 5, 6, 7, 8, 9, 10\}$.
3. **Internal Selection Criteria:**
   - **ICC-AutoK:** Computes the Proportion of Ambiguous Clustering (PAC) on the anchor co-association matrix across candidate $K$:
     $$\text{PAC}(K) = F_K(u_2) - F_K(u_1)$$
     where $u_1 = 0.1, u_2 = 0.9$, selecting $K^* = \arg\min_K \text{PAC}(K)$.
   - **GMM-BIC:** Minimizes Bayesian Information Criterion $\text{BIC}(K) = -2\ln\hat{L} + k_p \ln N$.
   - **GMM-ICL:** Minimizes Integrated Completed Likelihood $\text{ICL}(K) = \text{BIC}(K) + 2 \text{Entropy}(Z)$.
   - **Spectral Eigengap:** Maximizes the Laplacian eigengap $\delta_K = \lambda_{K+1} - \lambda_K$.
   - **HDBSCAN\*:** Infers $K$ non-parametrically from persistent density hierarchies above noise floor.

---

## 3. Synthetic Benchmark Geometry Suite

Synthetic datasets are generated across 8 distinct topological difficulty levels:

| Configuration ID | True $K^*$ | Sample Size $N$ | Signal Dims $D_{\text{signal}}$ | Noise Dims $D_{\text{noise}}$ | Cluster Balance | Density Structure | Topology |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **SYN-K2-BAL** | 2 | 200 | 20 | 100 | Balanced (100:100) | Homogeneous | Isotropic Gaussian |
| **SYN-K3-BAL** | 3 | 300 | 20 | 100 | Balanced (100:100:100) | Homogeneous | Isotropic Gaussian |
| **SYN-K4-IMB** | 4 | 400 | 30 | 150 | Imbalanced (200:100:60:40) | Heterogeneous | Varying Covariance |
| **SYN-K5-HIGHNOISE**| 5 | 500 | 20 | 500 | Balanced (100 each) | Homogeneous | 96% Distractor Noise |
| **SYN-K8-COMPLEX** | 8 | 400 | 40 | 200 | Imbalanced Dirichlet | Heterogeneous | Dense Clusters |
| **SYN-K10-EXTREME** | 10 | 500 | 50 | 500 | Imbalanced Dirichlet | Heterogeneous | High-D Multi-Class |
| **SYN-MOONS-K2** | 2 | 300 | 2 | 50 | Balanced (150:150) | Equal | Non-Convex Intertwined |
| **SYN-CIRCLES-K2** | 2 | 300 | 2 | 50 | Balanced (150:150) | Equal | Concentric Manifolds |

---

## 4. Real Biological Cohorts with Hidden K

Representative real biological cancer cohorts evaluated under hidden-$K$:
1. `colon` ($N=62, D=2,000$, Hidden True $K=2$)
2. `srbct` ($N=83, D=2,308$, Hidden True $K=4$)
3. `leukemia` ($N=72, D=7,129$, Hidden True $K=2$)
4. `cns` ($N=60, D=7,129$, Hidden True $K=2$)
5. `su2001` ($N=174, D=12,533$, Hidden True $K=11$)
6. `dlbcl` ($N=77, D=5,469$, Hidden True $K=2$)
7. `breast` ($N=97, D=24,481$, Hidden True $K=2$)

---

## 5. Evaluation Metrics for Model Order Selection

For each algorithm and dataset run:
1. **$K$ Estimation Accuracy:** $\mathbb{I}\{\hat{K} = K^*\}$.
2. **Absolute Error in $K$:** $\Delta K = |\hat{K} - K^*|$.
3. **Signed Error in $K$:** $\hat{K} - K^*$ (Detects systematic over-clustering or under-clustering).
4. **Post-Hoc ARI:** Adjusted Rand Index against true biological labels using the autonomously chosen partition.
5. **Post-Hoc NMI / AMI:** Normalized and Adjusted Mutual Information.
6. **Execution Runtime:** Time in seconds to perform complete model order sweep.
