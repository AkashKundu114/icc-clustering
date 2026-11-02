# Loop 5: Mathematical and Theoretical Adjudication Report

**Author:** Agent B — Mathematical, Algorithmic, and Statistical Learning Theory Specialist  
**Adjudication Date:** November 2, 2026  
**Repository:** `AkashKundu114/icc-clustering` (`D:\icc-clustering`)  
**Target Manuscript:** `paper/manuscript/main.tex`  

---

## Executive Summary

This report delivers an independent, first-principles mathematical adjudication of all theoretical claims, propositions, theorems, and redesign proposals across Loops 1 through 4. Every mathematical assertion is evaluated for formal proof correctness, hidden assumptions, domain of validity, and theoretical guarantees.

---

## 1. Topic-by-Topic Mathematical Derivations & Adjudications

### Topic 1: Sarle's Bimodality Coefficient & the 5/9 Bound
**Definition:** Sarle's Bimodality Coefficient is defined as:
$$BC = \frac{\gamma^2 + 1}{\kappa + 3}$$
where $\gamma = \frac{\mu_3}{\sigma^3}$ is skewness and $\kappa = \frac{\mu_4}{\sigma^4} - 3$ is excess kurtosis ($\beta_2 = \kappa + 3$ is Pearson kurtosis).

**Adjudication of the $5/9$ Bound:**
- For any continuous distribution, Pearson's inequality states $\beta_2 \ge \gamma^2 + 1$, which implies $BC \le 1$.
- For the standard continuous uniform distribution $U(a, b)$: $\gamma = 0$ (by symmetry) and $\beta_2 = 9/5 = 1.8$ ($\kappa = -1.2$). Therefore:
  $$BC_{\text{uniform}} = \frac{0^2 + 1}{1.8} = \frac{5}{9} \approx 0.5556.$$
- For any **symmetric unimodal distribution** with finite fourth moment, the famous inequality of Teuscher and Guiard (1995) and Darlington (1970) establishes that Pearson kurtosis satisfies $\beta_2 \ge 9/5 = 1.8$, with equality attained in the limit by the continuous uniform distribution (or degenerate symmetric two-point mass). Since $\gamma = 0$ by symmetry:
  $$BC_{\text{symm-unimodal}} = \frac{1}{\beta_2} \le \frac{1}{1.8} = \frac{5}{9}.$$
- **Critical Vulnerability / Falsification of Universal Unimodality Bound:**
  The bound $BC \le 5/9$ holds **strictly for symmetric unimodal distributions**. For asymmetric unimodal distributions, $\gamma \neq 0$, and the numerator $\gamma^2 + 1$ can grow arbitrarily large without forcing a proportional increase in $\kappa + 3$.
  *Counterexample (Log-Normal Distribution):* Let $X \sim \text{Lognormal}(0, \sigma^2)$. $X$ is strictly unimodal for all $\sigma > 0$. As $\sigma$ increases (e.g., $\sigma = 1.5$), skewness $\gamma \approx 33.5$ and Pearson kurtosis $\beta_2 \approx 4,375$. Then:
  $$BC = \frac{33.5^2 + 1}{4375} \approx \frac{1123}{4375} \approx 0.256.$$
  For moderately skewed unimodal distributions (e.g. mixture of an exponential and narrow Gaussian, or Pareto with $\alpha > 4$), $BC$ regularly exceeds $5/9$.
- **Status:** **Proven Under Stated Assumptions (Requires Explicit Symmetric Density Restriction).**

---

### Topic 2: Finite-Sample Behavior of $BC$ for Small $N$
In `src/icc/features/bgss.py` and Equation (1) of `main.tex`, sample skewness $\hat{\gamma}$ and excess kurtosis $\hat{\kappa}$ are estimated via Fisher's finite-sample bias-corrected formulas:
$$\hat{\gamma} = \frac{\sqrt{N(N-1)}}{N-2} g_1, \quad \hat{\kappa} = \frac{N-1}{(N-2)(N-3)} \left[(N+1) g_2 + 6\right]$$
**Mathematical Finding:**
1. Under a Gaussian null with sample size $N$, the sample kurtosis estimator has standard error:
   $$\text{SE}(\hat{\kappa}) \approx \sqrt{\frac{24}{N}}.$$
   For the CNS cohort ($N = 60$) and Colon cohort ($N = 62$), $\text{SE}(\hat{\kappa}) \approx \sqrt{24/60} \approx 0.632$.
2. Because $\hat{\kappa}$ appears in the denominator ($\max(\hat{\kappa} + 3 \cdot \frac{(N-1)^2}{(N-2)(N-3)}, 10^{-5})$), random negative sample variations of $\hat{\kappa}$ cause the denominator to drop close to zero, producing extreme positive outliers in $\hat{b}_d$.
3. Across $D = 15,154$ dimensions (Ovarian), testing 15,154 independent noise features will inevitably produce hundreds of extreme finite-sample false positives that exceed $5/9$ purely by chance.
- **Status:** **Empirically Supported; Asymptotic Convergence Fails for $N \le 60$ Without Multiple-Testing FDR Correction.**

---

### Topic 3: Gaussian Mixture Separation Threshold ($\Delta/\sigma_0 \approx 1.854$)
Let $X \sim 0.5 \mathcal{N}(-\Delta, \sigma_0^2) + 0.5 \mathcal{N}(\Delta, \sigma_0^2)$.
- Mean $\mu = 0$, variance $\sigma^2 = \sigma_0^2 + \Delta^2 = \sigma_0^2(1 + \theta)$, where $\theta = (\Delta/\sigma_0)^2$.
- By symmetry, skewness $\gamma = 0$.
- Fourth central moment:
  $$\mu_4 = 3\sigma_0^4 + 6\sigma_0^2 \Delta^2 + \Delta^4 = \sigma_0^4(3 + 6\theta + \theta^2).$$
- Pearson kurtosis:
  $$\beta_2 = \frac{\mu_4}{\sigma^4} = \frac{3 + 6\theta + \theta^2}{(1 + \theta)^2}.$$
- Bimodality coefficient:
  $$BC = \frac{1}{\beta_2} = \frac{(1 + \theta)^2}{\theta^2 + 6\theta + 3} = \frac{\theta^2 + 2\theta + 1}{\theta^2 + 6\theta + 3}.$$
- Setting $BC > 5/9$:
  $$\frac{\theta^2 + 2\theta + 1}{\theta^2 + 6\theta + 3} > \frac{5}{9} \iff 9(\theta^2 + 2\theta + 1) > 5(\theta^2 + 6\theta + 3)$$
  $$4\theta^2 - 12\theta - 6 > 0 \iff 2\theta^2 - 6\theta - 3 > 0.$$
- Roots of quadratic:
  $$\theta = \frac{6 \pm \sqrt{36 - 4(2)(-3)}}{4} = \frac{6 \pm \sqrt{60}}{4} = \frac{3 \pm \sqrt{15}}{2}.$$
  Since $\theta = (\Delta/\sigma_0)^2 > 0$:
  $$\theta > \frac{3 + \sqrt{15}}{2} \approx \frac{3 + 3.87298}{2} = 3.43649.$$
- Taking the square root:
  $$\frac{\Delta}{\sigma_0} > \sqrt{3.43649} \approx 1.85377 \approx 1.854.$$
- **Status:** **Mathematically Proven and Exact.**

---

### Topic 4: BGSS Inability to Detect Nonlinear Manifolds and XOR Parity
BGSS evaluates features strictly coordinate-by-coordinate:
$$b_d = \text{BC}(\mathbf{f}_d).$$
- **XOR / Parity Failure:** In a balanced 2D XOR or parity distribution, the joint distribution contains 4 distinct clusters: $(+1, +1), (-1, -1)$ vs $(+1, -1), (-1, +1)$. However, the marginal distribution of each coordinate $X_1$ and $X_2$ is identical to a balanced mixture of $+1$ and $-1$ centered around zero with identical variance, or strictly unimodal if blurred by continuous noise. On the Madelon benchmark (which embodies an XOR parity hypercube embedded in 480 noise coordinates), the true informative coordinates have strictly unimodal marginals ($\gamma \approx 0, \kappa \approx 0 \implies b_d \approx 1/3$). BGSS discards all true signal coordinates.
- **Covariance-Only Clusters:** If two clusters share identical marginal distributions along coordinate axes but differ in covariance ($\Sigma_1 = \left[\begin{smallmatrix}1 & 0.8 \\ 0.8 & 1\end{smallmatrix}\right]$ vs $\Sigma_2 = \left[\begin{smallmatrix}1 & -0.8 \\ -0.8 & 1\end{smallmatrix}\right]$), marginal moments are identical across classes ($\gamma_d = 0, \kappa_d = 0$), so $b_d \approx 1/3$. BGSS is blind to covariance structure.
- **Status:** **Mathematically Proven Structural Limitation.**

---

### Topic 5: Proposition 2 (Exact Determinacy Identity)
**Theorem Statement:**
Let $S_{ij} = \frac{1}{M} \sum_{m=1}^M \mathbf{1}\{\pi_m(i) = \pi_m(j)\}$. Then:
$$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i))$$
where $C_{m_1, m_2}(c_1, c_2) = \sum_{j=1}^N \mathbf{1}\{\pi_{m_1}(j)=c_1 \wedge \pi_{m_2}(j)=c_2\}$.
- **Proof:**
  $$\sum_{j=1}^N S_{ij}^2 = \sum_{j=1}^N \left(\frac{1}{M} \sum_{m_1=1}^M \mathbf{1}\{\pi_{m_1}(i) = \pi_{m_1}(j)\}\right) \left(\frac{1}{M} \sum_{m_2=1}^M \mathbf{1}\{\pi_{m_2}(i) = \pi_{m_2}(j)\}\right)$$
  $$= \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M \sum_{j=1}^N \mathbf{1}\{\pi_{m_1}(j) = \pi_{m_1}(i) \wedge \pi_{m_2}(j) = \pi_{m_2}(i)\}.$$
  By definition of the contingency matrix $C_{m_1, m_2}$, the inner sum over $j$ is exactly $C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i))$. $\square$
- **What It Does NOT Prove:**
  Proposition 2 proves that sample determinacy $\sigma_i$ can be computed in $O(M^2 N + M^2 K^2)$ without materializing $S$. It **does NOT prove** that clustering the bipartite anchor graph $B$ is spectrally equivalent to clustering $S$.
- **Status:** **Mathematically Proven and Exact.**

---

### Topic 6: Transfer-Cut Normalization & Regularization
In `src/icc/consensus/bipartite_graph.py`, the bipartite normalized cut constructs:
$$B_{\text{norm}} = D_R^{-1} B, \quad W_{\text{anchor}} = B_{\text{norm}}^T B_{\text{norm}} \in \mathbb{R}^{L \times L}, \quad D_A = \operatorname{diag}(W_{\text{anchor}} \mathbf{1}_L).$$
The normalized anchor Laplacian is:
$$L_{\text{anchor}} = I - D_A^{-1/2} W_{\text{anchor}} D_A^{-1/2}.$$
The Transfer-Cut theorem (Li et al., 2015) proves that if $(\lambda, \mathbf{v})$ is an eigenpair of $L_{\text{anchor}}$, the sample embedding is given by:
$$\mathbf{u} = B_{\text{norm}} D_A^{-1/2} \mathbf{v} \cdot \frac{1}{\sqrt{1 - \lambda}}.$$
- **Vulnerability / Regularization Constant:**
  As $\lambda \to 1$ (which occurs when the bipartite graph has weakly connected components or isolated anchors), the factor $(1 - \lambda)^{-1/2} \to \infty$, causing numerical instability. In code, this is clamped: $\max(1 - \lambda, 10^{-4})^{-1/2}$.
  Clamping at $10^{-4}$ acts as a Tikhonov regularizer that bounds the maximum norm of sample coordinates, but perturbs the true harmonic extension of the graph Laplacian.
- **Status:** **Proven Under Regularization Bounds; Clamping Constant Must Be Disclosed.**

---

### Topic 7: Adaptive Anchor Budget $L^*(K)$ & Minority Cluster Coverage
In Loop 3, Agent D proposed the heuristic:
$$L^*(K) = \max(40, \lceil 3 K \ln K \rceil).$$
**Mathematical Derivation & Refutation of "General Minority Coverage Guarantee":**
- Let the dataset consist of $K$ clusters with mixture proportions $\pi_1 \ge \pi_2 \ge \dots \ge \pi_{\min} > 0$.
- Under uniform random sampling of $L$ anchors with replacement from $N$ instances:
  For any specific cluster $k$, the probability that zero anchors are drawn from cluster $k$ is:
  $$P(A_k = 0) = (1 - \pi_k)^L \le e^{-L \pi_k}.$$
- To ensure that the minority cluster receives at least one anchor with probability at least $1 - \delta$:
  $$(1 - \pi_{\min})^L \le \delta \implies L \ge \frac{\ln(1/\delta)}{\ln\left(\frac{1}{1 - \pi_{\min}}\right)} \approx \frac{\ln(1/\delta)}{\pi_{\min}}.$$
- **Simultaneous Coverage of All $K$ Clusters:**
  By the union bound:
  $$P\left(\bigcup_{k=1}^K \{A_k = 0\}\right) \le \sum_{k=1}^K (1 - \pi_k)^L \le K (1 - \pi_{\min})^L \le K e^{-L \pi_{\min}}.$$
  Setting $K e^{-L \pi_{\min}} \le \delta$:
  $$L \ge \frac{\ln(K/\delta)}{\pi_{\min}} = \frac{\ln K + \ln(1/\delta)}{\pi_{\min}}.$$
- **Coupon Collector Comparison:**
  If clusters are strictly balanced ($\pi_{\min} = 1/K$), then:
  $$L \ge K (\ln K + \ln(1/\delta)).$$
  For $\delta = 0.05$, $\ln(1/0.05) \approx 3.0$, yielding $L \approx K \ln K + 3K$.
- **Why $3 K \ln K$ Fails Under Imbalance:**
  If clusters are imbalanced (e.g., in cancer cohorts where a rare subtype represents $\pi_{\min} = 0.02$ and $K = 4$):
  $$3 K \ln K = 3(4)\ln 4 \approx 12(1.386) \approx 17.$$
  With $L = 17$ and $\pi_{\min} = 0.02$:
  $$P(\text{miss minority}) = (1 - 0.02)^{17} = (0.98)^{17} \approx 0.709.$$
  There is a **$70.9\%$ probability of completely missing the minority cluster**!
- **Status:** **Refuted as a General Guarantee; True Minority Coverage Requires $L = \Omega\left(\frac{\ln(K/\delta)}{\pi_{\min}}\right)$.**

---

### Topic 8: Inductive Out-of-Sample Centroid Projection vs. Manifold Extension
In Section 4.3 (Equations 9--10), GAC projects out-of-sample query points $\mathbf{x}^* \in \mathbb{R}^D$ via:
$$y^* = \arg\min_k \|\mathbf{x}^*_{[\mathcal{F}_{\text{active}}]} - \boldsymbol{\mu}_k\|_2, \quad \text{where } \boldsymbol{\mu}_k = \frac{\sum_{i: y_i = k} \sigma_i \mathbf{x}_{i, [\mathcal{F}_{\text{active}}]}}{\sum_{i: y_i = k} \sigma_i}.$$
- **Geometric Inconsistency:**
  Spectral bipartite clustering operates in the spectral embedding space $U \in \mathbb{R}^{N \times K}$, where non-linearly separable manifolds (e.g. concentric circles or spirals) become linearly separable.
  However, projecting back to $\mathbb{R}^{|\mathcal{F}_{\text{active}}|}$ and computing the Euclidean centroid $\boldsymbol{\mu}_k$ discards the spectral kernel trick.
  If cluster $k$ is an outer ring in concentric circles, the Euclidean centroid $\boldsymbol{\mu}_k$ falls into the center of the ring (inside the inner cluster!). Consequently, any query point on the outer ring is misassigned.
- **Empirical Confirmation:** In Loop 2 Exp 3 (`exp3_inductive_geometry.csv`), GAC inductive ARI on concentric circles is exactly $-0.003$ (total failure).
- **Correct Formulation (Transfer-Cut Native Projection):**
  For query instance $\mathbf{x}^*$, compute its affinity vector to the $L$ anchors: $\mathbf{b}^* \in \mathbb{R}^L$, where $b_a^* = \frac{1}{M}\sum_m \mathbf{1}\{\pi_m(\mathbf{x}^*) = \pi_m(\mathbf{x}_a)\}$. The out-of-sample spectral coordinate is:
  $$\mathbf{u}^* = \frac{\mathbf{b}^*}{\|\mathbf{b}^*\|_1} D_A^{-1/2} V \operatorname{diag}(1 - \boldsymbol{\lambda})^{-1/2}.$$
  Assigning $y^* = \arg\min_k \|\mathbf{u}^* - \mathbf{c}_k^{\text{spec}}\|_2$ preserves manifold topology.
- **Status:** **Euclidean Centroid Operator Fails on Manifolds; Must Be Bounded to Convex Geometries.**

---

### Topic 9: CCAA Conformal Calibration Target & Exchangeability
In Loop 3, Agent B proposed "CCAA" (Conformal Cluster Assignment with Calibration Split).
- **The Theoretical Flaw:**
  Standard split-conformal prediction requires exchangeable pairs $(Z_1, \dots, Z_n, Z_{n+1})$ drawn from distribution $P$.
  In unsupervised learning, true biological class labels $Y_i$ are latent and unobserved.
  CCAA uses transductive consensus labels $\hat{y}_i$ as pseudo-ground truth.
  Therefore, CCAA guarantees coverage **only of the algorithm's own transductive assignments**, NOT the true clinical or biological classes.
  If the transductive consensus is discordant with biology (e.g. on Prostate where $\text{ARI} = 0.012$), achieving $90\%$ coverage of the wrong cluster provides zero diagnostic value.
- **Status:** **Plausible for Internal Cluster Membership; Invalid as a Clinical or Biological Guarantee.**

---

### Topic 10: Complexity Bounds (Theorem 1)
Equation (5) in `main.tex` asserts:
$$T_{\text{GAC}} = O\bigl(N D + D \log D + M^2 N + M^2 K^2 + M I_{\text{km}} N |\mathcal{F}_{\text{sub}}| K + M N L + N L^2 + L^3 + N L K + I_{\text{km}} N K^2\bigr).$$
- **Term-by-term proof:**
  1. $ND$: Single-pass computation of sample mean, variance, skewness, and kurtosis across $D$ features.
  2. $D \log D$: Sorting $D$ bimodality coefficients.
  3. $M^2 N + M^2 K^2$: Exact sample determinacy calculation (Proposition 2).
  4. $M I_{\text{km}} N |\mathcal{F}_{\text{sub}}| K$: Fitting $M$ base K-Means models on subspaces.
  5. $M N L$: Constructing $N \times L$ bipartite co-assignment matrix $B$.
  6. $N L^2$: Matrix multiplication $B_{\text{norm}}^T B_{\text{norm}} \in \mathbb{R}^{L \times L}$.
  7. $L^3$: Eigendecomposition of $L \times L$ normalized anchor Laplacian.
  8. $N L K$: Matrix multiplication $U = B_{\text{norm}} V \in \mathbb{R}^{N \times K}$.
  9. $I_{\text{km}} N K^2$: Final K-Means clustering on $N$ points in $\mathbb{R}^K$.
- For fixed $M, K, L, |\mathcal{F}_{\text{sub}}|$, all terms are strictly linear in $N$ ($O(N)$). Auxiliary working memory is $O(NL + L^2)$ for $B$ and $W_{\text{anchor}}$, bypassing $O(N^2)$.
- **Status:** **Mathematically Proven and Sound.**

---

## 2. Master Mathematical Adjudication Table

| Component | Mathematical Claim | Formal Status | Required Manuscript Action |
|:---|:---|:---|:---|
| **Sarle's BC (Prop 1)** | $BC \le 5/9$ bounds unimodality. | **Proven Under Explicit Assumptions** | Restrict to *symmetric* unimodal distributions. Add Remark on skewed counterexamples. |
| **Separation (Prop 1)** | Separation $\Delta/\sigma_0 > 1.854 \iff BC > 5/9$. | **Proven and Exact** | Retain without alteration. |
| **Determinacy (Prop 2)** | Contingency formulation computes $\sigma_i$ in $O(M^2 N + M^2 K^2)$. | **Proven and Exact** | Retain without alteration. |
| **Complexity (Thm 1)** | Pipeline time is $O(N)$, auxiliary graph memory is $O(NL)$. | **Proven and Exact** | Retain; clarify empirical power-law is pre-asymptotic. |
| **Inductive Centroid** | $y^* = \arg\min_k \|x^* - \boldsymbol{\mu}_k\|_2$ provides general out-of-sample extension. | **Incorrect / Contradicted on Manifolds** | Explicitly restrict to convex/hyper-ellipsoidal geometry; disclose manifold failure. |
| **Adaptive Anchor Rule** | $L^*(K) = \max(40, \lceil 3 K \ln K \rceil)$ guarantees minority cluster coverage. | **Incorrect / Refuted Under Imbalance** | Discard claim of general minority coverage; replace with $L = \Omega(\ln(K/\delta)/\pi_{\min})$. |
| **CCAA Conformal** | Provides finite-sample valid cluster assignment sets. | **Plausible for Internal Cluster Model Only** | Retain strictly as Future Work; prohibit clinical validity claims. |
| **Transfer-Cut Clamp** | Clamping $\max(1-\lambda, 10^{-4})$ preserves eigensystem. | **Empirically Supported Approximation** | Disclose regularizing perturbation in Section 4.2. |
