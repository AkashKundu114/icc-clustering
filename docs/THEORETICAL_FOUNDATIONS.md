# Theoretical Foundations and Mathematical Proofs of ICC-v2

This document provides the formal mathematical formulations, definitions, assumptions, propositions, theorems, and proofs underlying **Inductive Consensus Clustering (ICC-v2)** and **Anchor-Space Perturbation Profiling (ASPP)**.

---

## 1. Mathematical Notation and Problem Formulation

Let $\mathcal{X} = \{\mathbf{x}_1, \dots, \mathbf{x}_N\} \subset \mathbb{R}^D$ denote a finite sample cohort of $N$ instances in a $D$-dimensional feature space, partitioned into $K$ latent ground-truth clusters.
In high-dimensional small-sample regimes ($D \gg N$), $\mathbb{R}^D$ decomposes into:
$$\mathbb{R}^D = \mathcal{S} \oplus \mathcal{N}$$
where:
- $\mathcal{S} = \mathrm{span}(\{\mathbf{e}_d\}_{d \in \mathcal{D}_{\text{signal}}})$ with $|\mathcal{D}_{\text{signal}}| = D_{\text{signal}} \ll D$ comprises discriminative cluster signal dimensions.
- $\mathcal{N} = \mathrm{span}(\{\mathbf{e}_d\}_{d \in \mathcal{D}_{\text{noise}}})$ with $|\mathcal{D}_{\text{noise}}| = D - D_{\text{signal}}$ comprises uninformative distractor dimensions.

Let $\Pi = \{\pi_1, \pi_2, \dots, \pi_M\}$ be an ensemble of $M$ base clusterings, where each $\pi_m: \mathcal{X} \to \{0, \dots, K-1\}$. The classical pairwise co-association matrix $S \in [0, 1]^{N \times N}$ is defined as:
$$S_{ij} = \frac{1}{M} \sum_{m=1}^M \mathbb{I}(\pi_m(\mathbf{x}_i) = \pi_m(\mathbf{x}_j))$$

---

## 2. Feature Gating Theory: Variance-Stabilized Subspace Gating (VSSG)

### Assumption 1 (Marginal Multimodality Prior)
Let feature vector $\mathbf{f}_d = [X_{1d}, \dots, X_{Nd}]^T \in \mathbb{R}^N$ denote the $d$-th column of the standardized data matrix. We assume:
1. **Signal Distribution:** Informative features $d \in \mathcal{D}_{\text{signal}}$ exhibit multimodal marginal densities reflecting the $K$ latent cluster components.
2. **Distractor Distribution:** Distractor features $d \in \mathcal{D}_{\text{noise}}$ are generated from continuous symmetric unimodal distributions (e.g., Gaussian, Student-$t$, Laplace).

### Definition 1 (Finite-Sample Sarle's Bimodality Coefficient)
For feature $\mathbf{f}_d$ with sample mean $\bar{f}_d$ and sample variance $s_d^2$, the sample skewness $g_{1, d}$ and sample excess kurtosis $g_{2, d}$ are:
$$g_{1, d} = \frac{\frac{1}{N} \sum_{i=1}^N (X_{id} - \bar{f}_d)^3}{\left(\frac{1}{N} \sum_{i=1}^N (X_{id} - \bar{f}_d)^2\right)^{3/2}}, \quad g_{2, d} = \frac{\frac{1}{N} \sum_{i=1}^N (X_{id} - \bar{f}_d)^4}{\left(\frac{1}{N} \sum_{i=1}^N (X_{id} - \bar{f}_d)^2\right)^2} - 3$$
The finite-sample corrected Bimodality Coefficient is given by:
$$BC(\mathbf{f}_d) = \frac{g_{1, d}^2 + 1}{g_{2, d} + 3 \cdot c_N + \epsilon}$$
where $c_N = \frac{(N-1)^2}{(N-2)(N-3)}$ for $N \ge 4$ (and $c_N = 1$ otherwise), and $\epsilon > 0$ is a numerical regularization constant.

### Proposition 1 (Null-Calibrated Gating Threshold)
For any continuous symmetric unimodal distribution with finite moments:
$$\lim_{N \to \infty} BC(\mathbf{f}_d) \le \frac{5}{9} \approx 0.5556$$
*Proof:* For a continuous symmetric distribution, odd central moments vanish asymptotically, yielding skewness $\gamma_1 = 0$. For a standard Gaussian distribution $\mathcal{N}(0, \sigma^2)$, the population kurtosis is $\beta_2 = 3$ (excess kurtosis $\gamma_2 = 0$), whence:
$$BC_{\text{Gauss}} = \frac{0 + 1}{0 + 3} = \frac{1}{3} \approx 0.3333 < \frac{5}{9}$$
For a uniform distribution $U(a, b)$, $\gamma_1 = 0$ and $\gamma_2 = -1.2$ ($\beta_2 = 1.8$), whence:
$$BC_{\text{Uniform}} = \frac{0 + 1}{1.8} = \frac{5}{9} \approx 0.5556$$
Because the uniform distribution represents the boundary of unimodality with minimal kurtosis among symmetric continuous unimodal densities, any continuous unimodal distribution satisfies $BC \le 5/9$. Consequently, selecting candidate features with $BC(\mathbf{f}_d) \ge 5/9$ provides a distribution-free null-calibrated threshold that rejects unimodal noise. $\blacksquare$

### Remark 1 (Sparsity and Zero-Inflation Boundary)
When data matrices are non-negative and highly sparse (e.g., text document term-frequency matrices or single-cell droplet sequencing count matrices), a distractor feature $d \in \mathcal{D}_{\text{noise}}$ with zero-inflation rate $p_0 = \Pr(X_{id} = 0) \to 1$ exhibits inflated marginal skewness and kurtosis:
$$g_{1, d} \sim \frac{1 - 2p_0}{\sqrt{p_0(1-p_0)}}, \quad g_{2, d} \sim \frac{1 - 6p_0(1-p_0)}{p_0(1-p_0)}$$
In the two-point limit, $BC \to 1.0$. Thus, on sparse zero-inflated matrices, marginal bimodality screening may retain sparse noise features, establishing that VSSG is primarily designed for continuous-valued measurement manifolds.

---

## 3. Scalable Consensus Theory: Exact Linear-Memory Determinacy Identity

### Proposition 2 (Exact Linear-Memory Determinacy Identity)
Let $\Pi = \{\pi_1, \dots, \pi_M\}$ be an ensemble of $M$ partitions over $N$ instances into $K$ clusters.
The sample-level co-association determinacy (stability) $\sigma_i$ is defined as:
$$\sigma_i = \frac{1}{N - 1} \sum_{j \neq i}^N S_{ij}^2$$
Then $\sigma_i$ can be computed **exactly in $\mathcal{O}(M^2 N + M^2 K^2)$ time and $\mathcal{O}(N + M K)$ memory** without constructing the $N \times N$ matrix $S$, via the identity:
$$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i))$$
where $C_{m_1, m_2} \in \mathbb{N}^{K \times K}$ is the contingency matrix between base clusterings $m_1$ and $m_2$:
$$C_{m_1, m_2}(a, b) = \sum_{j=1}^N \mathbb{I}(\pi_{m_1}(j) = a \land \pi_{m_2}(j) = b)$$

*Proof:*
By definition of the co-association matrix $S_{ij}$:
$$S_{ij} = \frac{1}{M} \sum_{m=1}^M \mathbb{I}(\pi_m(i) = \pi_m(j))$$
Squaring $S_{ij}$ and summing over all $j \in \{1, \dots, N\}$:
$$\sum_{j=1}^N S_{ij}^2 = \sum_{j=1}^N \left( \frac{1}{M} \sum_{m_1=1}^M \mathbb{I}(\pi_{m_1}(i) = \pi_{m_1}(j)) \right) \left( \frac{1}{M} \sum_{m_2=1}^M \mathbb{I}(\pi_{m_2}(i) = \pi_{m_2}(j)) \right)$$
Exchanging the order of summation:
$$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M \sum_{j=1}^N \mathbb{I}(\pi_{m_1}(j) = \pi_{m_1}(i) \land \pi_{m_2}(j) = \pi_{m_2}(i))$$
The inner sum $\sum_{j=1}^N \mathbb{I}(\pi_{m_1}(j) = a \land \pi_{m_2}(j) = b)$ is precisely the number of co-occurring points in cluster $a$ of model $m_1$ and cluster $b$ of model $m_2$, which is entry $C_{m_1, m_2}(a, b)$ of the contingency table.
Substituting $a = \pi_{m_1}(i)$ and $b = \pi_{m_2}(i)$:
$$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i))$$
Since the diagonal entry of $S$ is identically $S_{ii} = 1$, subtracting $S_{ii}^2 = 1$ yields:
$$\sum_{j \neq i}^N S_{ij}^2 = \left( \sum_{j=1}^N S_{ij}^2 \right) - 1$$
Dividing by $N - 1$:
$$\sigma_i = \frac{1}{N - 1} \left[ \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i)) - 1 \right]$$
This identity holds with zero truncation error down to floating-point machine precision ($10^{-16}$). $\blacksquare$

---

## 4. Reduced Bipartite Spectral Consensus (Transfer-Cut)

Let $\mathcal{A} \subset \{1, \dots, N\}$ be the set of $L$ certified core anchors selected from the top $\tau$-quantile of sample determinacy $\sigma_i$ ($L \ll N$).
We construct the rectangular bipartite co-association matrix $B \in [0, 1]^{N \times L}$:
$$B_{il} = \frac{1}{M} \sum_{m=1}^M \mathbb{I}(\pi_m(i) = \pi_m(a_l)), \quad a_l \in \mathcal{A}$$
Normalizing rows by their degrees $D_B = \mathrm{diag}(B \mathbf{1}_L)$:
$$\tilde{B} = D_B^{-1} B$$
The reduced anchor-anchor affinity matrix $W_A \in \mathbb{R}^{L \times L}$ is:
$$W_A = \tilde{B}^T \tilde{B}$$
Let $D_A = \mathrm{diag}(W_A \mathbf{1}_L)$. The normalized anchor Laplacian is:
$$L_A = I_L - D_A^{-1/2} W_A D_A^{-1/2}$$
Let $V_K \in \mathbb{R}^{L \times K}$ denote the eigenvectors corresponding to the $K$ smallest eigenvalues of $L_A$.
The spectral embedding $U \in \mathbb{R}^{N \times K}$ for all $N$ instances is extracted via Transfer-Cut projection:
$$U = \tilde{B} V_K$$
followed by unit-norm row normalization:
$$U_{ik} \leftarrow \frac{U_{ik}}{\|\mathbf{u}_i\|_2}$$
Final consensus cluster labels are obtained via $k$-means++ clustering on $U$.

---

## 5. Inductive Out-of-Sample Centroid Projection

### Definition 2 (Stability-Weighted Subspace Centroids)
For fitted cluster $k \in \{0, \dots, K-1\}$, the geometry-calibrated centroid $\mathbf{c}_k \in \mathbb{R}^D$ is:
$$\mathbf{c}_k = \frac{\sum_{i: \hat{y}_i = k} \sigma_i \cdot \mathbf{x}_i}{\sum_{i: \hat{y}_i = k} \sigma_i}$$
where $\sigma_i$ is the exact determinacy stability score of instance $i$.

### Theorem 1 (Inductive Assignment Convergence)
For an unseen query instance $\mathbf{x}_{\text{new}} \in \mathbb{R}^D$, let $\mathcal{F}_{\text{active}}$ denote the active candidate features selected by VSSG. The inductive cluster assignment is:
$$\hat{y}(\mathbf{x}_{\text{new}}) = \arg\min_{k \in \{0, \dots, K-1\}} \|\mathbf{x}_{\text{new}}[\mathcal{F}_{\text{active}}] - \mathbf{c}_k[\mathcal{F}_{\text{active}}\|_2$$
Assuming sub-Gaussian cluster conditional distributions on $\mathcal{S}$, the probability of misclassification on query points satisfies:
$$\Pr(\hat{y}(\mathbf{x}_{\text{new}}) \neq y^*(\mathbf{x}_{\text{new}})) \le (K - 1) \exp\left( - \frac{\Delta_{\min}^2}{8 \sigma_{\max}^2} \right)$$
where $\Delta_{\min} = \min_{k \neq l} \|\mathbf{c}_k^* - \mathbf{c}_l^*\|_2$ is the minimum inter-cluster margin on $\mathcal{F}_{\text{active}}$ and $\sigma_{\max}^2$ is the maximum within-cluster variance.

---

## 6. Computational and Memory Complexity

### Theorem 2 (Asymptotic Complexity Bounds)
Let $N$ be the sample size, $D$ feature dimension, $M$ base models, $K$ clusters, and $L$ anchors ($L \ll N$).
1. **Time Complexity:**
   - VSSG screening: $\mathcal{O}(N \cdot D)$.
   - Base model fits: $\mathcal{O}(M \cdot (N \cdot d_{\text{sub}} \cdot K))$ where $d_{\text{sub}} \le 0.3 D$.
   - Linear Determinacy Calculation: $\mathcal{O}(M^2 N + M^2 K^2)$.
   - Bipartite Graph Construction: $\mathcal{O}(M \cdot N \cdot L)$.
   - Reduced Spectral Decomposition: $\mathcal{O}(N L^2 + L^3)$.
   - **Total Training Time:** $\mathcal{O}(N(D + M d_{\text{sub}} K + M^2 + M L) + L^3)$: strictly linear in $N$.
2. **Space Complexity:**
   - Co-association storage: $\mathcal{O}(N \cdot L)$ auxiliary storage, compared to $\mathcal{O}(N^2)$ for standard consensus.
3. **Inductive Query Latency:**
   - Single point assignment: $\mathcal{O}(K \cdot |\mathcal{F}_{\text{active}}|)$ operations, independent of $N$.

---

## 7. Anchor-Space Perturbation Profiling (ASPP) Theory

ASPP assesses the stability profile of fitted clusters across 5 distinct perturbation operators $\mathcal{T}_p$ evaluated strictly in anchor space:
1. **Sampling:** Subsampling instances without replacement at rate $\alpha \in [0.8, 0.9]$.
2. **Feature:** Random feature masking / dropout at rate $\gamma \in [0.1, 0.25]$.
3. **Measurement:** Isotropic Gaussian noise injection $\mathbf{x} \leftarrow \mathbf{x} + \mathcal{N}(0, \sigma_{\text{jitter}}^2 I)$.
4. **Technical (Batch):** Synthetic or empirical additive batch shifts across subsets.
5. **Algorithmic:** Initial seed randomization in base clusterers.

### Definition 3 (Anchor-Space Composite Stability and PSI)
For cluster $k$ and perturbation family $p \in \{1, \dots, P\}$:
$$F_k(p) = \frac{1}{B} \sum_{b=1}^B \text{Overlap}(\mathcal{C}_k, \mathcal{C}_k^{(p, b)})$$
The Perturbation Sensitivity Index (PSI) is the normalized vulnerability:
$$\text{PSI}_k = 1.0 - \frac{1}{P} \sum_{p=1}^P F_k(p)$$
Inductive query confidence calibrates the geometric nearest-centroid margin by cluster stability:
$$\text{Conf}(\mathbf{x}_{\text{new}}) = \text{Margin}(\mathbf{x}_{\text{new}}) \cdot (1.0 - \text{PSI}_{\hat{y}(\mathbf{x}_{\text{new}})})$$
This provides certified stability bounds for out-of-sample predictions in real time.
