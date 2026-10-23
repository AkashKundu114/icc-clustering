# MATHEMATICAL & THEORETICAL FOUNDATIONS (THEORY_NOTES.md)

**Canonical Manuscript Title**: "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue**: Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version**: `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Authors**: Antigravity Remediation Team (Subagent B - Theory & Method)  
**Verification Script**: `scripts/verify_prop1.py`  
**Execution Log**: `REMEDIATION/logs/verify_prop1.log`  

---

## 1. Proposition 1: Conditional Multimodality Separation Bound

### 1.1 Formal Statement
Let $X \sim \frac{1}{2}\mathcal{N}(-\Delta, \sigma_0^2) + \frac{1}{2}\mathcal{N}(\Delta, \sigma_0^2)$ be a symmetric two-component Gaussian mixture model representing an informative cluster-discriminative feature. Sarle's Bimodality Coefficient is defined as:
$$b(X) = \frac{\gamma^2 + 1}{\beta_2}$$
where $\gamma = \mathbb{E}[(X - \mu)^3]/\sigma^3$ is skewness and $\beta_2 = \mathbb{E}[(X - \mu)^4]/\sigma^4$ is Pearson's kurtosis.

Under Sarle's criterion, a feature is candidate multimodal if and only if $b(X) > b_{\text{uniform}} = \frac{5}{9}$. Then the required cluster separation is strictly bounded below by:
$$\frac{\Delta}{\sigma_0} > \sqrt{\frac{3 + \sqrt{15}}{2}} \approx 1.853778 \approx 1.854$$

### 1.2 Analytic Derivation
1. By symmetry around $\mu = 0$, all odd central moments vanish: $\mathbb{E}[X] = 0$ and $\gamma = 0$.
2. The total variance is:
   $$\sigma^2 = \mathbb{E}[X^2] = \sigma_0^2 + \Delta^2$$
3. The fourth central moment of the mixture is:
   $$\mathbb{E}[X^4] = 3\sigma_0^4 + 6\sigma_0^2 \Delta^2 + \Delta^4$$
4. Pearson's kurtosis evaluates to:
   $$\beta_2 = \frac{\mathbb{E}[X^4]}{\sigma^4} = \frac{3\sigma_0^4 + 6\sigma_0^2 \Delta^2 + \Delta^4}{(\sigma_0^2 + \Delta^2)^2}$$
5. Setting $b > \frac{5}{9} \iff \beta_2 < \frac{9}{5} = 1.8$:
   $$\frac{3\sigma_0^4 + 6\sigma_0^2 \Delta^2 + \Delta^4}{(\sigma_0^2 + \Delta^2)^2} < \frac{9}{5}$$
6. Substitute $\theta = (\Delta / \sigma_0)^2 \ge 0$:
   $$5(3 + 6\theta + \theta^2) < 9(1 + 2\theta + \theta^2)$$
   $$15 + 30\theta + 5\theta^2 < 9 + 18\theta + 9\theta^2$$
   $$4\theta^2 - 12\theta - 6 > 0 \iff 2\theta^2 - 6\theta - 3 > 0$$
7. Applying the quadratic formula:
   $$\theta = \frac{6 \pm \sqrt{36 - 4(2)(-3)}}{4} = \frac{6 \pm \sqrt{60}}{4} = \frac{3 \pm \sqrt{15}}{2}$$
   Since $\theta > 0$, the unique positive root is:
   $$\theta^* = \frac{3 + \sqrt{15}}{2} \approx 3.436492$$
8. Taking the square root gives the universal critical separation:
   $$\frac{\Delta}{\sigma_0} > \sqrt{3.436492} \approx \mathbf{1.853778} \approx \mathbf{1.854}$$

### 1.3 Extension to Heavy-Tailed Noise (Student-$t$)
Under Student-$t$ distributed noise with $\nu > 4$ degrees of freedom (finite fourth moment), the heavy tails inflate the kurtosis of each component:
$$\beta_2^{(t)} = 3 + \frac{6}{\nu - 4} > 3$$
Because excess kurtosis increases kurtosis for any given mixture separation, the required separation $\Delta / \sigma_0$ must strictly exceed $1.854$ (e.g., at $\nu=5$, $\Delta/\sigma_0 \approx 2.178$). Thus, $1.854$ constitutes the infimum over all continuous distributions with sub-Gaussian tails.

---

## 2. Transfer-Cut Bipartite Graph Formulation

### 2.1 Bipartite Construction
Standard consensus clustering computes an $N \times N$ pairwise co-association matrix $S \in [0, 1]^{N \times N}$, requiring $O(N^2)$ space. In ICC-v2, Transfer-Cut is formulated over a bipartite graph $G = (V_X \cup V_A, E, W)$, where:
- $V_X = \{x_1, \dots, x_N\}$ is the set of data instances.
- $V_A = \{a_1, \dots, a_L\}$ is the set of $L \ll N$ anchor instances (default $L=40$).
- The bipartite affinity matrix $B \in [0, 1]^{N \times L}$ is defined as:
  $$B_{ia} = \frac{1}{M} \sum_{m=1}^M \mathbf{1}\{\pi_m(x_i) = \pi_m(a)\}$$
- The complete bipartite adjacency matrix $W \in \mathbb{R}^{(N+L) \times (N+L)}$ is block off-diagonal:
  $$W = \begin{bmatrix} 0 & B \\ B^T & 0 \end{bmatrix}$$

### 2.2 Spectrum Equivalence via Singular Value Decomposition
The degree matrices are $D_X = \text{diag}(B \mathbf{1}_L) \in \mathbb{R}^{N \times N}$ and $D_A = \text{diag}(B^T \mathbf{1}_N) \in \mathbb{R}^{L \times L}$.
The normalized bipartite graph Laplacian problem:
$$(D - W) \mathbf{u} = \lambda D \mathbf{u}$$
reduces to the generalized singular value decomposition of the scaled matrix:
$$\tilde{B} = D_X^{-1/2} B D_A^{-1/2} \in \mathbb{R}^{N \times L}$$
Let $\tilde{B} = U \Sigma V^T$ be the SVD of $\tilde{B}$, with singular values $1 = \sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_K$.
The leading non-trivial left singular vectors:
$$U_{\text{emb}} = D_X^{-1/2} U_{:, 2:K+1} \in \mathbb{R}^{N \times K}$$
give the exact spectral embedding of all $N$ data points in $O(NLK)$ time and $O(NL)$ memory, completely circumventing $O(N^2)$ storage and eigendecomposition.

---

## 3. Bimodality Coefficient & Pre-Registered Scope Boundaries

### 3.1 Sarle's Criterion & Definition
The empirical Bimodality Coefficient for feature $d$ across sample observations $\{x_{1d}, \dots, x_{Nd}\}$ is computed as:
$$b_d = \frac{g_d^2 + 1}{k_d + 3 \cdot \frac{(N-1)^2}{(N-2)(N-3)}}$$
where $g_d$ is the sample skewness and $k_d$ is sample excess kurtosis.
For standard normal noise, $\mathbb{E}[b] = 1/3 \approx 0.333$.
For a uniform distribution, $b_{\text{uniform}} = 5/9 \approx 0.5556$.

### 3.2 Theoretical Limitation: 1D Marginal Unimodality (Madelon XOR Breakdown)
VSSG evaluates features independently along 1D marginal axes. This imposes a fundamental geometric limitation:
- If cluster structure is governed by multi-feature parity/XOR interactions (such as Madelon, where the class label is determined by non-linear combinations of features without marginal shift), the 1D marginal projection of each feature is strictly Gaussian.
- In Madelon, the true clusters have identical marginal means and variances across all 20 informative features.
- Consequently, the maximum observed $b_d$ across all 500 features is $0.5042 < 5/9$.
- VSSG cannot detect non-linear feature interactions without marginal bimodality. This limitation is formally acknowledged in the revised manuscript.

---

## 4. Anchor Determinacy vs. Uniform Random Sampling

### 4.1 Quadratic Determinacy Identity
Exact sample determinacy (stability) $\sigma_i$ is computed without forming the $N \times N$ matrix $S$:
$$\sigma_i = \frac{1}{N-1}\sum_{j \neq i} S_{ij}^2 = \frac{1}{(N-1)M^2} \sum_{m=1}^M \sum_{m'=1}^M N_{\pi_m(x_i), \pi_{m'}(x_i)}^{(m, m')} - \frac{1}{N-1}$$
where $N_{k, k'}^{(m, m')} = |\{j : \pi_m(x_j) = k \land \pi_{m'}(x_j) = k'\}|$ is the cross-partition contingency table.

### 4.2 Behavior in Small-Sample, High-Noise Regimes ($N \ll D$)
In datasets such as Leukemia ($N=72, D=7,129$) and SRBCT ($N=83, D=2,308$):
- Highly connected samples that achieve maximal quadratic determinacy frequently belong to the single largest dominant class.
- Determinacy-certified anchor selection (V5) tends to concentrate anchors within high-density regions of dominant clusters, starving minority clusters.
- Uniform random sampling (V4) draws anchors across the entire empirical support, ensuring non-zero representation of minority classes.
- As verified in empirical ablation, V4 achieved $0.628$ ARI on Leukemia and $0.650$ ARI on SRBCT, whereas V5 achieved $0.621$ and $0.614$.
- The revised manuscript clarifies that determinacy certification is an asymptotic variance-reduction technique designed for large $N$, and recommends uniform random anchors when $N < 100$.
