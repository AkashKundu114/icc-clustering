# Comprehensive Mathematical, Algorithmic, and Theoretical Audit of ICC-v2

**Author:** Lead Mathematical Auditor & Senior Research Scientist (Antigravity)  
**Independent Review Streams:**
- **Agent A:** Spectral Consensus Theorist (`d83a606d-351c-4246-aa76-a8bca0210165`)
- **Agent B:** BGSS Screening Theorist (`ef63d285-cf3b-41ff-af45-63e8089e6ccd`)
- **Agent C:** Conformal Inference Theorist (`cec0cc0b-e9fc-4ee6-8e1b-247998ce70aa`)
- **Agent D:** Inductive Geometry Theorist (`18401a25-5b9c-435f-b43d-26def7f5f826`)
- **Agent E:** Spectral Graph & Complexity Theorist (`4ba1223f-7c1e-48d4-9d97-6de2a3abac69`)

**Target Repository:** `AkashKundu114/icc-clustering` (`D:\icc-clustering`)  
**Git HEAD:** `7ddbe8301b8d27c94f388c40acbc88b0dee82723` on branch `main`  
**Date of Audit:** 2026-11-02  
**Status:** Completed & Reconciled (Iterations 1, 2, and 3)  

---

## 1. Executive Summary & Lead Agent Reconciliation

This audit presents an independent, exhaustive mathematical and algorithmic verification of the theoretical foundations, implementation correctness, assumptions, and empirical claims of **Inductive Core Consensus v2 (ICC-v2)**, **Anchor-Space Perturbation Profiling (ASPP)**, and **Conformal Inductive Consensus Clustering (CICC)**.

Every theoretical proposition, lemma, theorem, and implementation module was audited from first principles by five independent specialist review agents, verified through analytical derivations and reproducible numerical experiments, and reconciled by the Lead Agent.

### 1.1 Master Claims Classification Summary

Of the 30 core mathematical, algorithmic, and empirical claims cataloged across the codebase and manuscript:
- **Valid (Mathematically Proven / Exact):** 6 claims (20.0%)
- **Conditional (Supported Under Explicit Assumptions):** 4 claims (13.3%)
- **Overstated (Plausible Concept, Overstated Guarantee):** 3 claims (10.0%)
- **Invalid (Incorrect or Unsupported):** 17 claims (56.7%)

### 1.2 Categorization by Publication Path
- **Issues Blocking Publication (Fatal P0 Defects):** 5 critical defects that would cause immediate retraction if published in their current form (Conformal coverage target mismatch, AutoK normalization collapse, Knockoff 100% FDR fallback, Inductive manifold disconnect, Transfer-Cut singular blow-up).
- **Issues Solvable by Manuscript Clarification (P1/P2 Framing):** 12 issues where mathematical bounds hold only under explicit assumptions (e.g., symmetry preconditions for Sarle's BC, interpreting conformal sets as in-distribution abstention bounds, documenting anchor clustering as an approximation of dense consensus, clarifying auxiliary memory scaling).
- **Issues Requiring Algorithmic Changes:** 13 code defects where implementation contradicts theoretical specifications (e.g., normalizing calibration inputs, removing dead decoy code, fixing small-$N_{\text{cal}}$ quantile clamping, removing the $N>2000$ dense subsampling fallback, dynamic $K$-aware anchor budgeting).

---

## 2. Audit Track A: BGSS Feature Screening & Interaction Blindspots

### 2.1 Theoretical Evaluation of Sarle's Bimodality Coefficient
In `src/icc/consensus/icc.py` (lines 173–186) and `docs/theory.md` Section 2, feature screening uses finite-sample Sarle's Bimodality Coefficient:
$$BC(\mathbf{f}_d) = \frac{g_{1, d}^2 + 1}{g_{2, d} + 3 c_N + \epsilon}$$
where $g_{1, d}$ is sample skewness, $g_{2, d}$ is unbiased sample excess kurtosis, and $c_N = \frac{(N-1)^2}{(N-2)(N-3)}$ for $N \ge 4$.

#### 1. Falsification of "Distribution-Free" Null Calibration [INCORRECT]
Proposition 1 in `docs/theory.md` asserts:
> *"For any continuous symmetric unimodal distribution with finite moments: $\lim_{N \to \infty} BC(\mathbf{f}_d) \le \frac{5}{9} \approx 0.5556$... Consequently, selecting candidate features with $BC(\mathbf{f}_d) \ge 5/9$ provides a distribution-free null-calibrated threshold that rejects unimodal noise."*

**Lead Agent Finding:** The claim of "distribution-free" noise rejection is **mathematically false**.
- By Khintchine’s representation theorem, the bound $BC \le 5/9$ holds **strictly for continuous symmetric unimodal densities**, where the continuous uniform distribution $U(a, b)$ achieves the infimum Pearson kurtosis ($\beta_2 = 1.8 \implies BC = 1/1.8 = 5/9$).
- For **asymmetric unimodal distributions**, skewness is non-zero, easily driving $BC > 5/9$ without multimodality:
  - Standard Exponential $\mathrm{Exp}(\lambda)$ (unimodal, mode at 0): $\gamma_1 = 2, \beta_2 = 9 \implies BC = (4 + 1)/9 = 5/9 \approx 0.5556$.
  - $\mathrm{Beta}(3, 1)$ (strictly increasing unimodal, mode at 1): $\gamma_1 = -0.8607, \beta_2 = 3.0952 \implies BC = 1.7408 / 3.0952 \approx \mathbf{0.5624} > 5/9$.
  - $\mathrm{Beta}(5, 1)$: $\gamma_1 = -1.1832, \beta_2 = 4.2000 \implies BC = \mathbf{0.5714} > 5/9$.
  - Continuous noise with modest zero-inflation ($p_0 > 0.15$) inflates skewness, pushing $BC > 0.60$.
- **Remediation:** Retract the claim of "distribution-free" noise rejection. State explicitly that $BC \le 5/9$ holds only under the assumption of continuous symmetric unimodal noise.

#### 2. The Finite-Sample Collapse Theorem [PROVEN]
Agent B proved that for an exact two-point symmetric sample with zero within-cluster variance ($\pm 1$ with $N/2$ instances each):
$$BC_{\text{two-point}}(N) = \frac{(N-2)(N-3)}{N^2 - 1}$$
Solving $BC_{\text{two-point}}(N) \ge 5/9$ requires:
$$4N^2 - 45N + 59 \ge 0 \implies N \ge 9.74$$
- For $N \le 9$, **even a 100% perfectly separated cluster feature fails the 5/9 threshold**:
  - $N = 4$: $BC = 0.1333$ (lower than standard normal Gaussian noise, $BC = 0.3333$).
  - $N = 6$: $BC = 0.3429 \approx BC_{\text{Gaussian}}$.
  - $N = 8$: $BC = 0.4762 < 5/9$.
- At small cohort sizes (e.g. rare biopsy pilot cohorts with $N \le 9$), BGSS deterministically discards perfectly discriminative features.

#### 3. Bimodality Gap in Gaussian Mixtures [PROVEN]
For a symmetric two-component Gaussian mixture $0.5\mathcal{N}(-\Delta, \sigma_0^2) + 0.5\mathcal{N}(\Delta, \sigma_0^2)$ with $\theta = (\Delta/\sigma_0)^2$, setting $BC(\theta) > 5/9$ yields:
$$2\theta^2 - 6\theta - 3 > 0 \implies \frac{\Delta}{\sigma_0} > \sqrt{\frac{3 + \sqrt{15}}{2}} \approx \mathbf{1.854} \implies 2\Delta > 3.708 \sigma_0$$
- In classical mixture theory (Behboodian 1970), a symmetric Gaussian mixture has a bimodal density if and only if $\Delta/\sigma_0 > 1.0$ (distance $> 2\sigma_0$).
- In the substantial regime $1.0 < \Delta/\sigma_0 < 1.854$, the underlying density is **strictly bimodal**, but Sarle's $BC < 5/9$. Consequently, `null_calibrated` mode discards genuine, moderately separated bimodal clusters.

### 2.2 Fundamental Blindness to Non-Marginal Structure
Because BGSS evaluates features strictly coordinate-by-coordinate in $\mathcal{O}(ND)$ time, integrating out all other dimensions destroys all joint copula information:

1. **Continuous XOR & Parity Interactions [PROVEN]:**  
   Clusters separated by sign quadrants ($Y = \mathrm{sign}(X_1 \cdot X_2)$) have marginal densities identically equal to $\mathcal{N}(0, 1)$ across all clusters. Population $BC(X_1) = BC(X_2) \equiv 1/3 \approx 0.3333$. In Madelon ($D=500$), BGSS scores on the 5 informative XOR features average $\hat{b}_d = 0.504 < 5/9$, collapsing ARI to $0.010 \pm 0.008$.
2. **Oblique Mixtures with Negative Covariance [PROVEN]:**  
   For two clusters with means $(-\mu, -\mu)$ and $(\mu, \mu)$ and within-cluster correlation $\rho = -0.9$ ($\mu = 0.8$), the 2D Mahalanobis distance is $D_M = 7.16\sigma$ (virtually zero Bayes error). However, coordinate projections have center separation of only $1.6\sigma_0 < 1.854\sigma_0$. Both features yield $BC \approx 0.35 < 5/9$ and are rejected as unimodal noise.
3. **Non-Linear Manifolds [PROVEN]:**  
   On concentric circles, coordinate projections form arcsine convolutions with $BC(X_1) = 0.4075$ and $BC(X_2) = 0.3969$ (both fail 5/9).
4. **Covariance-Differentiated Clusters [PROVEN]:**  
   Clusters with identical zero means but opposite covariance ($\rho_1 = 0.9, \rho_2 = -0.9$) have identical Gaussian marginals ($BC \equiv 1/3$).
5. **High-Dimensional Extreme Value Fluctuations [PROVEN]:**  
   With $N=100, D=1{,}000$ (2 XOR signal features and 998 noise features), maximum noise $BC$ reaches $0.4861$, while signal features have $BC \approx 0.35$ (ranking 595th and 870th). The top 15% candidate pool fails to retain Feature 0.

### 2.3 Implementation Realities: `legacy` vs. `null_calibrated`
- **Default Discrepancy:** In `src/icc/consensus/icc.py` line 105, default `pool_mode` is `"legacy"`. Lines 187–190 show that `legacy` mode **never checks $BC \ge 5/9$**; it unconditionally extracts the top 15% of features by sample $BC$.
- **Small-$D$ Bypass:** In `legacy` mode, `top_frac = min(1.0, max(0.15, 100.0 / D))`. For any dataset with $D \le 100$, `top_frac = 1.0`, meaning **zero feature gating occurs**.
- **Fallback Bug in `null_calibrated`:** In `null_calibrated` mode (line 238), if fewer than $\min(2, D)$ features pass $5/9$, the algorithm does not reject the dataset; it executes an uncalibrated fallback selecting the top $\min(D, \max(2, K))$ features by sample $BC$, which under the null ($D \gg N$) are simply extreme noise realizations.

---

## 3. Audit Track B: CICC & Conformal Calibration

### 3.1 Target of Guarantee Mismatch: Pseudo-Labels vs. Ground Truth
In `docs/theory.md` Section 9.1 and `examples/realtime_patient_projection.py`, CICC claims:
$$\Pr(y_{\text{query}} \in \mathcal{C}(\mathbf{x}_{\text{query}})) \ge 1 - \alpha$$
with guaranteed $(1 - \alpha = 90\%)$ conformal validity for point-of-care patient biopsies.

**Lead Agent Finding: [FATAL P0 DEFECT]**
1. **Calibration on Model Pseudo-Labels:** In `src/cicc/inductive.py` (lines 153–165), calibration labels $y_i^{\text{cal}}$ are generated by nearest-centroid argmax projection from discovery centroids:
   $$y_i^{\text{cal}} := \hat{Y}(X_i^{\text{cal}}) = \arg\max_{k \in \{0, \dots, K-1\}} \langle X_i^{\text{cal}}, \mathbf{c}_k \rangle$$
2. **True Biological Coverage Collapse:** Calibration scores $s_i = 1 - \max_k p_k(X_i) \le 1 - p_{Y_i^*}(X_i)$ stochastically dominate true nonconformity scores from below, making $\hat{q}$ systematically too conservative. In the repository's own benchmark demo (`examples/realtime_patient_projection.py`), evaluating $\mathcal{C}(X)$ against true clinical pathology (Leukemia ALL vs AML) yields:
   $$\text{Empirical Out-of-Sample Coverage} = \mathbf{46.7\%} \quad (\text{Nominal Claim: } 90.0\%)$$
   with 33.3% abstentions and 20% toxic misclassifications.
3. **Equivalence to an In-Distribution Abstention Bound [PROVEN]:**  
   Because calibration labels are argmax pseudo-labels, Agent C proved that for any query:
   $$\hat{Y}(x) \in \mathcal{C}(x) \iff |\mathcal{C}(x)| \ge 1 \iff \mathcal{C}(x) \neq \emptyset$$
   Therefore, the split-conformal guarantee with respect to pseudo-labels is **mathematically identical to an in-distribution abstention bound**:
   $$\Pr(\mathcal{C}(X) \neq \emptyset) \ge 1 - \alpha \iff \Pr(|\mathcal{C}(X)| = 0) \le \alpha + \frac{1}{N_{\text{cal}} + 1}$$
   It provides zero guarantee regarding biological ground truth, cluster stability, or disease etiology.

### 3.2 Nonconformity Score Metric Mismatch & Abstention Collapse
- **Metric Mismatch:** `docs/theory.md` §9.1 specifies Euclidean distance on a gated subspace: $s_i = \|\mathbf{x}_i[\mathcal{F}_{\text{gate}}] - \mathbf{c}_{y_i}[\mathcal{F}_{\text{gate}}\|_2$. `src/cicc/conformal.py` (lines 118–129) implements temperature-scaled softmax probabilities on cosine similarities across all $D$ features.
- **The Outlier Abstention Collapse Theorem [PROVEN]:**  
   Under cosine softmax nonconformity scores, an equidistant out-of-distribution outlier has $\langle \bar{x}, \mathbf{c}_k \rangle = 0 \implies p_k(x) = 1/K \implies s_k(x) = 1 - 1/K$.  
   If calibration scores yield $\hat{q} \ge 1 - 1/K$, then for **every** $x \in \mathbb{R}^D$:
   $$\max_k p_k(x) \ge \frac{1}{K} \implies 1 - \max_k p_k(x) \le 1 - \frac{1}{K} \le \hat{q} \implies |\mathcal{C}(x)| \ge 1$$
   Under this condition, the abstention rate is **identically 0% across the entire universe of possible inputs**. Outliers are never abstained upon; instead, equidistant outliers are assigned to all $K$ clusters simultaneously ($\mathcal{C}(x) = \{0, \dots, K-1\}$), directly breaking the dynamic memory novelty detection in `src/cicc/memory.py`.

### 3.3 Implementation Defects in `conformal.py`
1. **Normalization Asymmetry Bug:** In `fit_calibrate` (line 118), `X_cal` is unnormalized, whereas `predict` (line 159) unit-normalizes `X_test`. In standalone usage, this causes empirical coverage to drop from 90% to **67%** (-23% undercoverage).
2. **Small-$N_{\text{cal}}$ Undercoverage:** When $N_{\text{cal}} < 1/\alpha - 1$, the conformal target index $\lceil (N_{\text{cal}}+1)(1-\alpha) \rceil > N_{\text{cal}}$. Line 130 clamps this to 1.0, taking the sample maximum. The true coverage of the sample maximum is only $N_{\text{cal}}/(N_{\text{cal}}+1) < 1 - \alpha$ (e.g. at $N_{\text{cal}}=5, \alpha=0.10$, maximum coverage is $83.33\% < 90\%$).
3. **1-Based Label Crash (`IndexError`):** Line 127 indexes `probs_cal[i, int(labels_cal[i])]`. If labels are 1-based (standard in single-cell genomics), this raises an unhandled `IndexError: index 3 is out of bounds for axis 1 with size 3`.

### 3.4 Decoy Feature Gating Audit (`src/cicc/decoy.py`)
1. **Dead Code in `inductive.py`:** `self.selected_features_` is computed in `inductive.py` (lines 147–152) but **never passed** to centroids, calibration, or inference. All operations execute on the full $D$-dimensional ambient space.
2. **Knockoff Exchangeability Violations:** Synthetic decoys are sampled independently ($\mathrm{Cov}(X, \tilde{X}) = 0$), violating Model-X knockoff swap invariance. Post-clustering selection bias inflates null scores ($W_j > 0$ in 60.9% of pure noise features).
3. **100% FDR Fallback Bug:** Line 122 selects the top-ranked feature with `estimated_fdr = 1.0` when no feature meets `fdr_target`. Furthermore, if 0 features pass, line 140 returns the entire matrix $X$ unselected.

---

## 4. Audit Track C: Inductive Geometry & Out-of-Sample Projection

### 4.1 The Fundamental Geometric Disconnect
There is an absolute geometric contradiction between training and inference in ICC-v2:
- **Transductive Consensus Training:** Uses non-linear bipartite spectral graph theory (Transfer-Cut) to construct a normalized Laplacian $L_{\text{norm}}$, solve for eigenvectors $V_{\text{core}}$, and embed data into a spherical manifold $U \subset \mathbb{S}^{K-1}$, partitioning complex non-linear manifold geometry.
- **Inductive Inference (`predict`):** Discards the spectral embedding entirely and assigns unseen test points via **linear Euclidean nearest-centroid Voronoi projection in feature space $\mathbb{R}^D$** (`icc.py` lines 447–475):
  $$\hat{y}(\mathbf{x}_{\text{new}}) = \arg\min_{k \in \{0, \dots, K-1\}} \|\mathbf{x}_{\text{new}}[\mathcal{F}_{\text{active}}] - \mathbf{c}_k[\mathcal{F}_{\text{active}}\|_2$$
- **Root Cause:** In `src/icc/core.py` (line 225) and `src/icc/consensus/icc.py` (lines 250–259), `run_clusterer()` returns only the integer partition array `p` and **immediately discards the fitted base model estimators and parameters**. Because base models are not preserved, ICC-v2 cannot evaluate $\pi_m(\mathbf{x}_{\text{new}})$, cannot construct the bipartite anchor vector $B_{\text{new}, :}$, and cannot project into $U$. The feature-space centroid calculation was invented as an ad-hoc heuristic fallback.

### 4.2 Manifold Failure Modes & In-Sample Self-Inconsistency
1. **Concentric Circles:** Centroids coincide at the origin $\mathbf{c}_0 = \mathbf{c}_1 = \mathbf{0} \implies \Delta_{\min} = 0$. Transfer-Cut training achieves an ARI of **1.000**, but inductive `predict()` collapses to **-0.005** (random chance).
2. **Two Moons:** Training achieves ARI = **1.000**, but inductive `predict()` collapses to **0.333**.
3. **Anisotropic / Rotated Clusters:** Euclidean distance ignores cluster covariance, yielding an inductive error rate of **38.5%**.
4. **In-Sample Self-Inconsistency:** Because training boundaries are spectral while `predict()` boundaries are Euclidean Voronoi cells, `predict(X)` does not reproduce `labels_` on training points (e.g. 4% in-sample mismatch on high-dimensional benchmarks).
5. **Transformer API Violation (`icc.py:385-403`):** `transform()` returns unit-norm spherical spectral coordinates $U \in \mathbb{S}^{K-1}$, while `transform(X)` returns softmax posterior probabilities $\mathbf{p} \in \Delta^{K-1}$.

### 4.3 Scrutiny of Theorem 1
Theorem 1 in `docs/theory.md` bounds misclassification error by $(K-1)\exp(-\Delta_{\min}^2 / (8\sigma_{\max}^2))$.
**Lead Agent Finding: [OVERSTATED / CONDITIONAL]**
- The proof relies on a classical Chernoff bound for nearest-centroid projection with known population means and spherical isotropic noise.
- In the unsupervised high-dimensional regime claimed by ICC-v2, Theorem 1 is **invalidated by 6 unstated assumptions**:
  1. Assumes known population centroids ($\hat{\mathbf{c}}_k \equiv \mathbf{c}_k^*$), ignoring empirical centroid estimation error $\mathcal{O}_P(\sqrt{D_{\text{active}}/N_k})$ (error increased from 17.7% to 32.2% at $D_{\text{noise}}=500$).
  2. Assumes zero training label contamination (ARI = 1.0).
  3. Assumes spherical isotropic covariance ($\Sigma = \sigma^2 I$).
  4. Assumes convex, linearly separable clusters (collapses to $\Delta_{\min} = 0$ on manifolds).
  5. Assumes zero noise dimension leakage.
  6. Assumes zero distribution/batch shift.

### 4.4 The Architectural Solution: Native Transfer-Cut Spectral Projection
Agent D designed the exact mathematical solution that restores 100% geometric consistency without sacrificing microsecond latency:
1. Preserve fitted base models `self.base_models_ = [km_1, ..., km_M]` in `fit()`.
2. Store the projection operator $P_{\text{proj}} = D_A^{-1/2} V_K \Sigma^{-1/2} \in \mathbb{R}^{L \times K}$ and spherical spectral centroids $\boldsymbol{\mu}_k^{\text{spec}} \in \mathbb{S}^{K-1}$.
3. For query $\mathbf{x}_{\text{new}}$, evaluate base models to construct the bipartite anchor vector $\mathbf{b}(\mathbf{x}_{\text{new}})$, project into spectral embedding space $\mathbf{u}(\mathbf{x}_{\text{new}}) = \tilde{\mathbf{b}} P_{\text{proj}} / \|\tilde{\mathbf{b}} P_{\text{proj}}\|_2 \in \mathbb{S}^{K-1}$, and assign to nearest spectral centroid.
4. **Guarantees:** Zero in-sample self-inconsistency, full preservation of non-linear manifolds, and 50–100 $\mu$s query latency.

---

## 5. Audit Track D: Anchor Budget & Asymptotic Complexity

### 5.1 Feasibility Condition: What Happens When $L < K$?
1. **Strict Rank Deficiency [PROVEN]:** The reduced Laplacian $L_A \in \mathbb{R}^{L \times L}$ operates in $\mathbb{R}^L$. If $L < K$, $L_A$ has at most $L$ eigenvectors, making it mathematically impossible to span a $K$-dimensional simplex.
2. **The Origin Collapse Effect [PROVEN]:** By the pigeonhole principle, if $L < K$, at least $K - L$ clusters receive zero anchors. For unanchored instances, row sums in $B$ are zero, clamped to 1.0, yielding $\tilde{B}_{i, :} = \mathbf{0}^T$. Their spectral embeddings collapse to the **identical origin vector $\mathbf{0} \in \mathbb{R}^L$**. $K$-means cannot separate identical points, collapsing ARI and throwing convergence warnings.
3. **Coupon Collector Bound for Full Coverage [PROVEN]:** Even if $L \ge K$, random sampling requires:
   $$\mathbb{E}[L] = K H_K \approx K \ln K$$
   At $L = K$, the probability of missing at least one cluster is $1 - K!/K^K$ (96.2% at $K=5$, 99.96% at $K=10$).
4. **Minority Cluster Erasure [PROVEN]:** For an imbalanced cluster with proportion $\pi_{\min}$, covering it with probability $1 - \delta$ requires:
   $$L \ge \frac{\ln(1/\delta)}{\pi_{\min}}$$
   For $\pi_{\min} = 0.02, \delta = 0.05$, $L \ge 150$. The static default of $L = 40$ suffers a 44.6% failure rate of completely erasing rare clusters.
5. **Remediation:** Implement dynamic $K$-aware anchor budgeting: $L \ge \max(40, \lceil 3 K \ln K \rceil)$.

### 5.2 Asymptotic Complexity Verification (Theorem 2)
1. **Time Complexity [PROVEN]:** Total training runtime is $\mathcal{O}(N(D + M d_{\text{sub}} K + M^2 + M L) + L^3)$, which is strictly linear in $N$.
2. **Space Complexity [PROVEN WITH CLARIFICATION]:**
   - Bipartite graph storage replaces $N \times N$ matrix $S$ with $N \times L$ matrix $B$, requiring $\mathcal{O}(NL)$ RAM. For $N = 10^6, L = 30$, float64 requires exactly **240 MB**, bypassing the 8 TB dense barrier.
   - However, total auxiliary memory includes `P_stack` ($\mathcal{O}(MN)$) and `U_emb` ($\mathcal{O}(NK)$). Total auxiliary space is $\mathcal{O}(N(M + L + K) + L^2)$ ($\approx 345$ MB for $N=10^6$).

---

## 6. Audit Track E: Determinacy Theorem & Implementation Equivalence

### 6.1 Exactness of Proposition 2 (Linear Determinacy Identity)
Proposition 2 proves that sample determinacy $\sigma_i = \frac{1}{N-1}\sum_{j \neq i} S_{ij}^2$ can be computed in $\mathcal{O}(M^2 N + M^2 K^2)$ time and $\mathcal{O}(N + K^2)$ space without constructing $S$:
$$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i))$$
- **Algebraic Verification [PROVEN]:** Reconstructed from first principles; every step is algebraically exact with zero truncation error.
- **Numerical Verification [PROVEN]:** In `icc.py` lines 260–269, vectorized bincount uses integer arithmetic until final scalar division. Maximum error against dense matrix multiplication is $\|\Delta\|_\infty \le 2.78 \times 10^{-17}$. It is strictly more accurate and stable than dense summation.

### 6.2 The Large-$N$ Architectural Bug (`icc.py:289-320`)
- In `icc.py`, when $N > \text{dense\_threshold}$ (default 2000), lines 289–320 **completely bypass Proposition 2** and allocate a dense $1000 \times 1000$ matrix (25 MB) on a random subsample.
- **Mathematical Definition Switch:** In the $N \le 2000$ branch, `stability_` is second-order determinacy $\sigma_i = \frac{1}{N-1}\sum_{j\neq i} S_{ij}^2$. In the $N > 2000$ branch, line 318 sets `stability_ = np.mean(B, axis=1)` (first-order mean anchor similarity). These two statistics have a correlation of only $r = 0.6716$, causing inconsistent centroid weighting across sample sizes.
- **Performance Rationale Refuted:** Our benchmarks showed Proposition 2 executes in 0.07 s for $N=50,000$. The fallback is counterproductive and should be eliminated.

### 6.3 Transfer-Cut Operator Equivalence & Singularity
1. **Operator Divergence:** `icc.py` computes $W_A = \tilde{B}^T \tilde{B} = B^T D_X^{-2} B$, which differs from theoretical Transfer-Cut $W_r = B^T D_X^{-1} B$ by an extra factor of $D_X^{-1}$. This introduces a quadratic scale distortion, weighting instances in small clusters up to 81x higher than large clusters.
2. **Singular Value Blow-Up Bug (`icc.py:334-336`):** In `embedding="transfer_cut"`, columns are scaled by $1/\sqrt{\max(1 - \lambda_j, 10^{-9})}$. When eigenvalues $\lambda_j \ge 1.0$ (common in real graphs), $1 - \lambda \le 0$ is clipped to $10^{-9}$, causing a **$31,622\times$ noise amplification** that collapses the embedding into a 1D binary coordinate. `legacy` mode omits this scaling and achieves ARI 1.0 vs 0.828.
3. **Cross-Module Discrepancies:** `docs/theory.md` Section 4 documents the `legacy` formula as "Transfer-Cut"; `docs/api.md` lists default as `"transfer_cut"`, but code defaults to `"legacy"`; `aspp.py` line 305 hardcodes `legacy`, silently ignoring user settings.

---

## 7. AutoK Model Order Selection Degeneracy

### 7.1 Mathematical Root Cause of 100% Collapse
In `src/icc/consensus/autok.py` (lines 100–185), optimal cluster order $K^*$ is chosen by minimizing the Proportion of Ambiguous Clustering (PAC) on the anchor co-association matrix $\hat{S} = B B^T$:
$$\text{PAC}(k) = F_k(u_2) - F_k(u_1) = \frac{2}{N(N-1)} \sum_{i < j} \mathbb{I}(0.10 \le \hat{S}_{ij} \le 0.90)$$

**Lead Agent Proof of Degeneracy:**
1. In `icc.py`, rows of $B$ are degree-normalized across $L=40$ anchors: $\tilde{B}_{il} = B_{il} / \sum_{l=1}^L B_{il}$.
2. Under perfect cluster separation, instance $i \in \mathcal{C}_k$ connects only to anchors in $\mathcal{C}_k$ ($L_k \approx L/K$ anchors). Thus $\tilde{B}_{il} = 1/L_k$.
3. For two co-clustered instances $i, j \in \mathcal{C}_k$:
   $$\langle \tilde{\mathbf{b}}_i, \tilde{\mathbf{b}}_j \rangle = \sum_{l \in \mathcal{C}_k} \left(\frac{1}{L_k}\right)^2 = \frac{L_k}{L_k^2} = \frac{1}{L_k} = \frac{K}{L}$$
4. For $L = 40$ and $K \in \{2, 3, 4, 5\}$:
   - $K = 2 \implies \langle \tilde{\mathbf{b}}_i, \tilde{\mathbf{b}}_j \rangle = 1/20 = 0.0500 < 0.10$.
   - $K = 3 \implies \langle \tilde{\mathbf{b}}_i, \tilde{\mathbf{b}}_j \rangle = 3/40 = 0.0750 < 0.10$.
   - $K = 4 \implies \langle \tilde{\mathbf{b}}_i, \tilde{\mathbf{b}}_j \rangle = 4/40 = 0.1000$.
5. Even with 100% perfect cluster separation, the inner product cannot enter the ambiguity window $[0.10, 0.90]$.
6. For all pairs, $\hat{S}_{ij} < 0.10 \implies \mathbb{I}(0.10 \le \hat{S}_{ij} \le 0.90) \equiv 0 \implies \text{PAC}(k) \equiv 0.0000$.
7. In `autok.py`, ties at $\text{PAC} = 0$ are broken by selecting the minimum $k$, forcing **100% collapse to $K_{\min}$** across all 510/510 trials.
- **Remediation:** Rescale the PAC ambiguity window to the bipartite domain $[0.01, 0.08]$ or compute cosine similarities on $B$.

---

## 8. Prioritized Taxonomy of Findings & Remediation Plan

```
+----------------------------------------------------------------------------------------------------+
|                                    DEFECT TAXONOMY & SEVERITY                                      |
+----------------------------------------------------------------------------------------------------+
| Tier | Description                       | Count | Examples                                        |
+------+-----------------------------------+-------+-------------------------------------------------+
| P0   | Fatal / Retraction-Grade Defects  |   5   | CICC pseudo-label coverage collapse (46.7%)     |
|      |                                   |       | AutoK PAC bipartite normalization degeneracy    |
|      |                                   |       | Knockoff independent decoy 100% FDR fallback    |
|      |                                   |       | Inductive Euclidean vs Spectral disconnect      |
|      |                                   |       | Transfer-Cut 31,622x singular blow-up           |
+------+-----------------------------------+-------+-------------------------------------------------+
| P1   | Major Theoretical Overstatements  |   5   | Proposition 1 "distribution-free" claim         |
|      |                                   |       | Proposition 2 spectral equivalence conflation   |
|      |                                   |       | Theorem 1 unrealistic unstated assumptions      |
|      |                                   |       | Softmax conformal abstention impossibility      |
|      |                                   |       | Certified anchor null result (Knockout 4)       |
+------+-----------------------------------+-------+-------------------------------------------------+
| P2   | Algorithmic Inconsistencies       |   4   | Large-N dense subsampling fallback switch       |
|      |                                   |       | Normalization asymmetry in conformal.py         |
|      |                                   |       | Small-N_cal quantile clamping undercoverage     |
|      |                                   |       | Finite-sample BC collapse for N <= 9            |
+------+-----------------------------------+-------+-------------------------------------------------+
| P3   | Minor / Clerical Issues           |   3   | transform() API signature output mismatch       |
|      |                                   |       | 1-based label IndexError in conformal.py        |
|      |                                   |       | docs/api.md default embedding conflict          |
+----------------------------------------------------------------------------------------------------+
```

### Strategic Recommendations for Loop 2 (Manuscript Reframing)
1. **Section 4.1:** Restrict Proposition 1 to continuous symmetric unimodal distributions. Explicitly document that BGSS is an ultra-fast marginal filter blind to XOR and covariance interactions. Disclose default `legacy` behavior.
2. **Section 4.2:** Reframe Proposition 2 as an exact linear-memory determinacy identity for $\sigma_i$, explicitly documenting anchor consensus as an approximation of dense consensus.
3. **Section 4.3:** Restrict Theorem 1 to spherical isotropic clusters with known population centroids. Disclose the Euclidean Voronoi geometry of `predict()`.
4. **Section 5.2:** Report the Knockout 4 null result transparently: bipartite graph compression rather than core certification drives accuracy.
5. **Section 6.2 & 9.1:** Remove claims of 90% diagnostic coverage for patient biopsies. Reframe CICC split-conformal calibration as an in-distribution abstention bound, and disclose the 46.7% pathology coverage.

### Strategic Recommendations for Loop 3 (Algorithmic Remediation)
1. Eliminate the singular blow-up in `transfer_cut` by standardizing on SVD or regularizing singular values ($\max(1 - \lambda, 0.05)$).
2. Remove lines 289–320 in `icc.py` to run exact Proposition 2 for all $N$.
3. Implement Native Transfer-Cut Inductive Projection by preserving base models.
4. Rescale AutoK PAC thresholds to bipartite normalization densities $[0.01, 0.08]$.
5. Fix normalization asymmetry and small-$N_{\text{cal}}$ clamping in `conformal.py`.
6. Remove 100% FDR fallback and dead code in `decoy.py`.

---
*Comprehensive Audit Report concluded and saved to local audit registry.*
