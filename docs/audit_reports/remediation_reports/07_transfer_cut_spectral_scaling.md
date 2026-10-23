# Research Audit Report 07: Transfer-Cut Spectral Scaling & Anchor Bipartite Formulation

**Audit Target:** Bipartite Graph Partitioning & SVD Scaling in `src/icc/consensus_v2.py` and Manuscript Section 5.3  
**Canonical Manuscript Title:** When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination  
**Academic Lineage:** Initial University Allotment Title: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data" (`CSE_PROJECT_68`, Mentor: Prof. Kalyan Kumar Das); Early Proposal Blueprint: "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes"  
**Target Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI), document class `sn-jnl.cls` (`sn-mathphys-num.bst`), manuscript `paper/main.tex`.  
**Canonical Active Release:** v2.1.0  
**Status:** Remediated, Mathematically Proven & Audited (Stage A3, Pass F, and Section 5.3)  
**Date:** October 2026  

---

## 1. Executive Summary

A core algorithmic claim of ICC-v2 is its near-linear $\mathcal{O}(N L)$ scalability in sample size $N$, contrasting sharply with traditional dense consensus clustering methods that require $\mathcal{O}(N^2)$ time and memory to construct and factorize the pairwise co-association matrix $S \in \mathbb{R}^{N \times N}$.

The auditor requested an equation-level audit of the Transfer-Cut solver to ensure:
1. Exact algebraic equivalence between the Transfer-Cut SVD reduction and the Normalized Cut on the bipartite graph.
2. Proper degree matrix normalization and unit-norm embedding projections.
3. Strict absence of any implicit $N \times N$ matrix allocations.
4. Validation of memory and runtime scaling up to extreme scales ($N = 10^6$).

---

## 2. Mathematical Formulation: Bipartite Transfer-Cut

Let $X = \{x_1, \dots, x_N\} \subset \mathbb{R}^D$ be the dataset of $N$ samples, and let $U = \{u_1, \dots, u_L\} \subset \mathbb{R}^D$ be a set of $L$ representative anchor centroids ($L \ll N$, typically $L = 50$).

### 2.1 Bipartite Affinity Matrix
The affinity matrix $B \in \mathbb{R}^{N \times L}$ defines the connectivity between samples and anchors:
$$B_{il} = \begin{cases} \exp\left( - \frac{\|x_i - u_l\|^2}{2 \sigma_a^2} \right), & \text{if } u_l \in \mathcal{N}_r(x_i) \\ 0, & \text{otherwise} \end{cases}$$
where $\mathcal{N}_r(x_i)$ denotes the $r$-nearest anchors of sample $x_i$ ($r \ll L$, e.g., $r = 5$).

The bipartite adjacency matrix on the composite vertex set $V = X \cup U$ is given by:
$$W = \begin{bmatrix} \mathbf{0}_{N \times N} & B \\ B^T & \mathbf{0}_{L \times L} \end{bmatrix} \in \mathbb{R}^{(N+L) \times (N+L)}$$

### 2.2 Degree Normalization
The sample and anchor degree matrices are diagonal:
$$D_x = \text{diag}(B \mathbf{1}_L) \in \mathbb{R}^{N \times N}, \quad D_u = \text{diag}(B^T \mathbf{1}_N) \in \mathbb{R}^{L \times L}$$

The normalized bipartite transition matrix is:
$$\tilde{B} = D_x^{-1/2} B D_u^{-1/2} \in \mathbb{R}^{N \times L}$$

### 2.3 Exact SVD Equivalence to Bipartite Normalized Cut
The normalized random-walk Laplacian of the bipartite graph satisfies:
$$P = D^{-1} W = \begin{bmatrix} \mathbf{0} & D_x^{-1} B \\ D_u^{-1} B^T & \mathbf{0} \end{bmatrix}$$
The two-step random walk on the sample set $X$ corresponds to the transition matrix:
$$P_{xx} = D_x^{-1} B D_u^{-1} B^T$$
Computing the top eigenvectors of the normalized symmetric matrix $S_{xx} = D_x^{-1/2} B D_u^{-1} B^T D_x^{-1/2} = \tilde{B} \tilde{B}^T$ would normally require an $N \times N$ matrix.

However, by the Singular Value Decomposition (SVD) of the compact $N \times L$ matrix $\tilde{B}$:
$$\tilde{B} = \Phi \Sigma \Psi^T$$
where $\Psi \in \mathbb{R}^{L \times K}$ are the right singular vectors of $\tilde{B}$ (computed from the $L \times L$ Gram matrix $\tilde{B}^T \tilde{B}$), the sample spectral embedding $\Phi \in \mathbb{R}^{N \times K}$ is recovered directly via:
$$\Phi = \tilde{B} \Psi \Sigma^{-1} = D_x^{-1/2} B D_u^{-1/2} \Psi \Sigma^{-1}$$

---

## 3. Algorithmic Implementation Verification

In `src/icc/consensus_v2.py`, the Transfer-Cut is implemented without allocating any dense $N \times N$ intermediate:

```python
# Compute degree vectors in O(N L)
dx = np.array(B.sum(axis=1)).flatten()
du = np.array(B.sum(axis=0)).flatten()

dx_inv_sqrt = 1.0 / np.sqrt(np.maximum(dx, 1e-12))
du_inv_sqrt = 1.0 / np.sqrt(np.maximum(du, 1e-12))

# Scale B into normalized B_tilde
# B_tilde = diag(dx_inv_sqrt) @ B @ diag(du_inv_sqrt)
B_tilde = (B * du_inv_sqrt[None, :]) * dx_inv_sqrt[:, None]

# Compact SVD via truncated SVD on N x L matrix
# Only requires O(N L K + L^3) operations
U_svd, s, Vt = svd_fn(B_tilde, n_components=K)

# Normalize sample embeddings to unit L2 norm
norms = np.linalg.norm(U_svd, axis=1, keepdims=True)
U_normalized = U_svd / np.maximum(norms, 1e-12)

# Final clustering on compact spectral embedding
labels = kmeans_plusplus(U_normalized, n_clusters=K)
```

---

## 4. Empirical Complexity & Extreme-Scale Validation

As verified in `experiments/exp5_extreme_scale/` and quantified by macros in `paper/numbers.tex`:

1. **Memory Reduction:**  
   - At $N = 8,000$: **96.4%** RAM reduction over dense consensus.
   - At $N = 10,000$: **97.4%** overall RAM reduction and **99.6%** graph memory reduction.
   - Dense consensus requires allocating an 800 MB matrix at $N = 10,000$ and quickly exceeds workstation RAM, whereas ICC-v2 graph memory remains under 3 MB.

2. **Runtime Speedup:**  
   - On Ovarian cancer ($N = 253, D = 15,154$): **5.1x** speedup over dense consensus.
   - At $N = 10,000$: **2.9x** wall-clock speedup.

3. **Extreme Scale ($N = 10^6$ Single Cells):**  
   - At $N = 1,000,000$ samples, standard consensus would require an **8 TB** dense matrix, causing catastrophic out-of-memory failure.
   - ICC-v2 solves consensus in **55.6 s** (total execution time 141.2 s) with **240 MB** graph memory and **3.05 GB** peak RSS on a single commodity workstation.

| Consensus Approach | Graph Storage | Spectral Decomposition | Memory Footprint ($N=10^6$) | Runtime ($N = 10^6$) |
| :--- | :--- | :--- | :---: | :---: |
| **Standard Consensus (Fred & Jain)** | Dense $N \times N$ | Full Eigendecomposition | $\mathcal{O}(N^2) \approx 8.0 \text{ TB}$ | Out of Memory (OOM) |
| **Spectral Consensus (SEC)** | Sparse $N \times N$ | Lanczos Iteration | $\mathcal{O}(k_n N) \approx 48 \text{ GB}$ | $> 3 \text{ hours}$ |
| **ICC-v2 Transfer-Cut** | Compact $N \times L$ | Truncated SVD ($L \ll N$) | $\mathcal{O}(N L) \approx 240 \text{ MB}$ | **55.6 s** |

**Audit Sign-Off:** PASS: Transfer-Cut formulation verified mathematically, audited in source code, and benchmarked to 1,000,000 samples.
