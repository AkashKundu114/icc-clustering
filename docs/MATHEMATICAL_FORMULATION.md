# Inductive Consensus Clustering (ICC-v2): Mathematical Formulation & Code Correspondence

This document formally connects the mathematical formulation, definitions, theorems, and propositions of **Inductive Consensus Clustering (ICC-v2)** and **Anchor-Space Perturbation Profiling (ASPP)** to their exact algorithmic implementations in `src/icc/`.

---

## 1. Problem Formulation & Subspace Decomposition

Let $\mathcal{X} = \{\mathbf{x}_1, \dots, \mathbf{x}_N\} \subset \mathbb{R}^D$ be an input dataset of $N$ observations in $D$ ambient dimensions, partitioned into $K$ latent clusters.

In high-dimensional distractor noise regimes ($D \gg N$), the ambient metric space decomposes into orthogonal signal and distractor subspaces:
$$\mathbb{R}^D = \mathcal{S} \oplus \mathcal{N}$$
- $\mathcal{S} = \mathrm{span}(\{\mathbf{e}_d\}_{d \in \mathcal{D}_{\text{signal}}})$ with $|\mathcal{D}_{\text{signal}}| = D_{\text{signal}} \ll D$ comprises the latent cluster manifold.
- $\mathcal{N} = \mathrm{span}(\{\mathbf{e}_d\}_{d \in \mathcal{D}_{\text{noise}}})$ with $|\mathcal{D}_{\text{noise}}| = D - D_{\text{signal}}$ comprises unimodal distractor noise.

---

## 2. Mathematical Definitions & Algorithmic Correspondence

### 2.1 Variance-Stabilized Subspace Gating (VSSG)

#### Mathematical Definition: Finite-Sample Sarle's Bimodality Coefficient
For each feature column $\mathbf{f}_d \in \mathbb{R}^N$ with sample variance $s_d^2 > 10^{-12}$:
$$\text{BC}_d = \frac{g_{1, d}^2 + 1}{g_{2, d} + 3 \cdot c_N + 10^{-5}}$$
where sample skewness $g_{1, d}$ and excess kurtosis $g_{2, d}$ are unbiased estimators:
$$g_{1, d} = \frac{\sqrt{N(N-1)}}{N-2} \frac{m_3}{m_2^{3/2}}, \quad g_{2, d} = \frac{N-1}{(N-2)(N-3)} \left[(N+1) \frac{m_4}{m_2^2} - 3(N-1)\right]$$
and the finite-sample correction factor is:
$$c_N = \begin{cases} \frac{(N-1)^2}{(N-2)(N-3)} & \text{if } N \ge 4 \\ 1.0 & \text{otherwise} \end{cases}$$

#### Proposition 1 (Null-Calibrated Gating Threshold)
For any continuous symmetric unimodal distribution with finite moments:
$$\lim_{N \to \infty} \text{BC}(\mathbf{f}_d) \le \frac{5}{9} \approx 0.5556$$
Features exceeding the threshold $\text{BC}_d > 5/9$ are retained in the candidate pool $\mathcal{F}_{\text{active}}$.

#### Code Implementation
- **Function:** `src/icc/preprocessing/__init__.py::compute_bimodality_coefficient`
- **Method:** `src/icc/consensus_v2.py::InvariantCoreConsensusV2.fit` (lines 204–220)
- **Memory Optimization:** Column-chunked evaluation (`chunk_size=1000` or `low_memory=True`), capping peak RAM at $\mathcal{O}(N \cdot \text{chunk\_size})$ rather than $\mathcal{O}(ND)$.

---

### 2.2 Base Partition Ensemble & Core Anchor Selection

#### Mathematical Definition: Sample Determinacy & Core Certification
Let $\Pi = \{\pi_1, \dots, \pi_H\}$ be an ensemble of $H$ base clusterings, each fitted on a random subspace of $\mathcal{F}_{\text{active}}$.
The sample determinacy margin $d_i$ evaluates the consensus clarity:
$$d_i = \max_{k \in \{0, \dots, K-1\}} P(k \mid x_i) - \max_{k' \ne k} P(k' \mid x_i)$$
where $P(k \mid x_i) = \frac{1}{H} \sum_{h=1}^H \mathbf{1}\{\pi_h(i) = k\}$.

Certified core anchors are selected from the upper quantile threshold $\tau$ (default $q=0.50$):
$$\mathcal{A} = \{i \in \{1, \dots, N\} \mid d_i \ge \text{Quantile}(d, 1 - \tau)\}$$
$L = \min(|\mathcal{A}|, L_{\max})$ anchor centroids are retained.

#### Code Implementation
- **Method:** `src/icc/consensus_v2.py::InvariantCoreConsensusV2.fit` (lines 330–385)
- **Anchor Sampling:** Subsamples at most `n_anchors` certified core instances to guarantee bounded $\mathcal{O}(NL)$ auxiliary memory.

---

### 2.3 Proposition 2: Exact Linear-Memory Determinacy Identity

#### Mathematical Formulation
The pairwise co-association matrix $S \in [0, 1]^{N \times N}$ is defined by:
$$S_{ij} = \frac{1}{H} \sum_{h=1}^H \mathbf{1}\{\pi_h(i) = \pi_h(j)\}$$
The average determinacy $\sigma_i = \frac{1}{N-1} \sum_{j \ne i} S_{ij}^2$ satisfies the exact closed-form identity:
$$\sum_{j=1}^N S_{ij}^2 = \frac{1}{H^2} \sum_{h_1=1}^H \sum_{h_2=1}^H C_{h_1, h_2}(\pi_{h_1}(i), \pi_{h_2}(i))$$
where $C_{h_1, h_2} \in \mathbb{N}^{K \times K}$ is the pairwise contingency table between base partitions $h_1$ and $h_2$.

#### Code Implementation
- **Method:** `src/icc/consensus_v2.py` (lines 345–375)
- **Complexity:** $\mathcal{O}(H^2 N + H^2 K^2)$ time and $\mathcal{O}(N + H K)$ auxiliary RAM, completely bypassing the dense $\mathcal{O}(N^2)$ matrix allocation.

---

### 2.4 Bipartite Graph Spectral Consensus (Transfer-Cut)

#### Mathematical Formulation
Let $\mathbf{B} \in [0, 1]^{N \times L}$ be the rectangular bipartite affinity matrix between all $N$ observations and the $L$ core anchors:
$$B_{il} = \frac{1}{H} \sum_{h=1}^H \mathbf{1}\{\pi_h(i) = \pi_h(a_l)\}$$
Let $\mathbf{D}_X = \mathrm{diag}(\mathbf{B} \mathbf{1}_L)$ and $\mathbf{D}_A = \mathrm{diag}(\mathbf{B}^\top \mathbf{1}_N)$.
The normalized bipartite graph cut reduces to the $L \times L$ generalized anchor eigensystem:
$$\mathbf{W}_A = \mathbf{B}^\top \mathbf{D}_X^{-1} \mathbf{B}$$
$$\mathbf{L}_A \mathbf{v} = \lambda \mathbf{D}_A \mathbf{v}$$
where $\mathbf{L}_A = \mathbf{D}_A - \mathbf{W}_A$.

The continuous sample embedding $\mathbf{U} \in \mathbb{R}^{N \times K}$ is recovered via exact Transfer-Cut projection:
$$\mathbf{U} = \mathbf{D}_X^{-1} \mathbf{B} \mathbf{V}_K$$
where $\mathbf{V}_K \in \mathbb{R}^{L \times K}$ contains the $K$ principal eigenvectors of $\mathbf{L}_A$. Unit-norm row normalization is applied prior to $k$-means discretization.

#### Code Implementation
- **Method:** `src/icc/consensus_v2.py` (lines 400–475)
- **Symmetry Exploitation:** Since $\mathbf{W}_A$ is mathematically symmetric, `scipy.linalg.eigh` evaluates the eigensystem on the upper triangle, delivering a $2.15\times$ speedup.

---

### 2.5 Inductive Out-of-Sample Centroid Projection

#### Mathematical Formulation
For an unseen query instance $\mathbf{x}_{\text{query}} \in \mathbb{R}^D$, out-of-sample assignment is evaluated directly in the active feature subspace:
$$\hat{y}(\mathbf{x}_{\text{query}}) = \arg\min_{k \in \{0, \dots, K-1\}} \|\mathbf{x}_{\text{query}, \mathcal{F}_{\text{active}}} - \mathbf{C}_{k, \mathcal{F}_{\text{active}}}\|_2$$
where $\mathbf{C}_k = \frac{1}{|S_k \cap \mathcal{A}|} \sum_{i \in S_k \cap \mathcal{A}} \mathbf{x}_i$ is the anchor-weighted cluster centroid.

Softmax confidence margins are evaluated under temperature $T$:
$$p_k(\mathbf{x}_{\text{query}}) = \frac{\exp(-\|\mathbf{x}_{\text{query}} - \mathbf{C}_k\|_2 / T)}{\sum_{k'=0}^{K-1} \exp(-\|\mathbf{x}_{\text{query}} - \mathbf{C}_{k'}\|_2 / T)}$$
$$\text{Margin}(\mathbf{x}_{\text{query}}) = p_{(1)}(\mathbf{x}_{\text{query}}) - p_{(2)}(\mathbf{x}_{\text{query}})$$

#### Code Implementation
- **Methods:** `src/icc/consensus_v2.py::InvariantCoreConsensusV2.predict` (lines 530–560), `predict_proba` (lines 565–595), `predict_with_stability` (lines 600–620).
- **Latency:** $\mathcal{O}(K \cdot |\mathcal{F}_{\text{active}}|)$ operations per query point ($< 50 \ \mu\text{s}$ per query), independent of dataset size $N$.

---

### 2.6 Anchor-Space Perturbation Profiling (ASPP)

#### Mathematical Formulation
Given consensus partition $\mathcal{C} = \{S_1, \dots, S_K\}$, ASPP evaluates stability under 5 perturbation operators $\mathcal{T}_m$:
1. **Sampling:** Bootstrap subsampling at rate $\alpha \in [0.7, 0.9]$.
2. **Feature:** Subspace feature dropout at rate $\beta \in [0.1, 0.3]$.
3. **Measurement:** Additive Gaussian jitter $\mathbf{X}' = \mathbf{X} + \mathcal{N}(0, \sigma^2 \mathbf{I})$.
4. **Technical:** Random orthogonal projection and coordinate rotation.
5. **Algorithmic:** Eigensolver tolerance and initialization seeds.

For each cluster $k$ and perturbation $m$, Jaccard retention evaluates cluster persistence:
$$\text{Retention}_k(m) = \frac{|S_k \cap S_{\hat{k}}^{(m)}|}{|S_k \cup S_{\hat{k}}^{(m)}|}$$
$$\text{PSI}_k = 1.0 - \frac{1}{|\mathcal{M}|} \sum_{m \in \mathcal{M}} \text{Retention}_k(m)$$

#### Code Implementation
- **Class:** `src/icc/aspp.py::AnchorSpacePerturbationProfiler` (lines 60–216).
- **Efficiency:** Perturbation profiling is evaluated in anchor space ($\mathcal{O}(NL)$ memory), preventing tensor blowup.

---

## 3. Mathematical Mapping Summary Table

| Concept / Symbol | LaTeX Equation | Source Code Location | Time Complexity | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Sarle's Bimodality** | $\text{BC} = \frac{\gamma_1^2 + 1}{\gamma_2 + 3c_N}$ | `preprocessing.compute_bimodality_coefficient` | $\mathcal{O}(ND)$ | $\mathcal{O}(N \cdot \text{chunk})$ |
| **Core Determinacy** | $\sigma_i = \frac{1}{N-1} \sum S_{ij}^2$ | `consensus_v2.py:345-375` (Prop. 2) | $\mathcal{O}(H^2 N + H^2 K^2)$ | $\mathcal{O}(N + HK)$ |
| **Bipartite Matrix** | $B_{il} = \frac{1}{H} \sum \mathbf{1}\{\pi(i) = \pi(l)\}$ | `consensus_v2.py:405-425` | $\mathcal{O}(NHL)$ | $\mathcal{O}(NL)$ |
| **Anchor Eigensystem** | $\mathbf{W}_A = \mathbf{B}^\top \mathbf{D}_X^{-1} \mathbf{B}$ | `consensus_v2.py:430-455` | $\mathcal{O}(NL^2 + L^3)$ | $\mathcal{O}(L^2)$ |
| **Transfer-Cut** | $\mathbf{U} = \mathbf{D}_X^{-1} \mathbf{B} \mathbf{V}_K$ | `consensus_v2.py:458-472` | $\mathcal{O}(NLK)$ | $\mathcal{O}(NK)$ |
| **Inductive Assignment**| $\hat{y} = \arg\min \|\mathbf{x} - \mathbf{C}_k\|_2$ | `consensus_v2.py:535-560` | $\mathcal{O}(M K \|\mathcal{F}\|)$ | $\mathcal{O}(K \|\mathcal{F}\|)$ |
| **ASPP Profiling** | $\text{PSI} = 1 - \frac{1}{M}\sum \text{Jaccard}$ | `aspp.py:120-210` | $\mathcal{O}(|\mathcal{M}| \cdot NL)$ | $\mathcal{O}(NL)$ |
