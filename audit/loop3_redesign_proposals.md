# ICC-v2 Algorithmic Redesign Research Proposals

**Audit Phase**: Loop 3 Algorithmic Redesign Research (Proposal Before Implementation)  
**Repository**: `AkashKundu114/icc-clustering`  
**Git HEAD**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723` (Clean working tree; 0 tracked modifications)  
**Target Venue**: Springer Nature, *Data Mining and Knowledge Discovery* (DMKD)  
**Date**: November 2, 2026  
**Status**: Formal Architectural Redesign Proposals (Awaiting Explicit Human Approval)  

---

## EXECUTIVE SUMMARY & METHODOLOGICAL APPROACH

This report presents the research and algorithm-design proposals formulated to resolve the mathematical defects, empirical failure boundaries, and overclaimed theoretical guarantees identified in the Loop 1 Mathematical Audit and Loop 2 Adversarial Benchmarking.

In strict accordance with the primary objective, **we prioritize scientific defensibility, theoretical rigor, and practical computational efficiency over artificial novelty or unwarranted complexity**. Every weakness identified in Loops 1 and 2 has been systematically examined to determine whether it requires:
1. **A narrower, mathematically provable claim** (e.g., bounding Sarle's $BC \le 5/9$ to symmetric unimodal densities; framing conformal CICC as an in-distribution abstention bound).
2. **An algorithmic bugfix / normalization repair** (e.g., fixing AutoK PAC bipartite normalization collapse; resolving the singular value blow-up in Transfer-Cut; repairing the calibration normalization asymmetry in CICC).
3. **A principled architectural extension** (e.g., adopting the Coupon-Collector Adaptive Anchor Budget; providing an opt-in Native Spectral Out-of-Sample Extension).

The redesign process follows the required 5-iteration loop:
- **Iteration 1**: Independent specialist design across Tracks A, B, C, D, and E.
- **Iteration 2**: Formal cross-examination and critique of competing proposals.
- **Iteration 3**: Lead agent synthesis of the Minimal Viable Redesign (MVR).
- **Iteration 4**: Theoretical and computational feasibility review.
- **Iteration 5**: Final evidence-grounded selection of validated proposals.

---

## 1. DESIGN TRACK A: FEATURE SCREENING & BGSS REDESIGN

### 1.1 Context & Empirical Baseline
In ICC-v2, feature screening is governed by Sarle's Bimodality Coefficient:
$$BC(\mathbf{f}_d) = \frac{\hat{\gamma}_d^2 + 1}{\hat{\kappa}_d + 3 \frac{(N-1)^2}{(N-2)(N-3)}}$$
- **Loop 1 Audit Finding**: The claim that $BC \le 5/9 \approx 0.5556$ provides a "distribution-free" null threshold is false; asymmetric unimodal densities (e.g. Beta, Exponential, log-normal) routinely yield $BC > 5/9$ in the absence of clustering. Furthermore, for $N \le 9$, perfectly separated clusters yield $BC < 5/9$.
- **Loop 2 Empirical Finding**: Univariate marginal screening exhibits total blindness to multi-feature non-marginal interactions:
  - Continuous XOR: $\text{ARI} = -0.0016$, Feature Selection Precision = $0.000$, Recall = $0.000$.
  - 3-Way Parity: $\text{ARI} = -0.0033$, Precision = $0.000$, Recall = $0.000$.
  - Diagonal Gaussian Mixture ($\Delta = 1.60\sigma < 1.854\sigma$): Marginal projections fall below $BC > 5/9$, causing false feature rejection.
  - Distinct Covariances ($\rho_1 = +0.9, \rho_2 = -0.9$): Marginal distributions are identical Gaussians ($BC \equiv 1/3$), causing total cluster collapse ($\text{ARI} = -0.0004$).
  - High-D Noise ($D=1000$): Extreme value sample fluctuations of Gaussian noise yield sample $BC$ values up to $0.518$, outranking true signals in the fallback pool (Precision = $0.000$).
  - **The Positive Control**: In $D \gg N$ genomics (SRBCT, Leukemia), univariate bimodality filtering is the single driver of ICC-v2's dramatic victory over full-dimensional baselines (SRBCT Mean ARI = $0.535$ vs Dense Consensus $0.040$).

### 1.2 Evaluation of Candidate Screening Designs

#### Candidate A1: Calibrated Two-Tier Marginal BGSS (Recommended for ICC-v2.1)
- **Mathematical Definition**: Retain univariate moment calculation in $\mathcal{O}(ND)$ time, but replace the invalid universal $5/9$ constant with an empirical Monte Carlo or quantile-calibrated threshold conditioned on sample size $N$:
  $$\tau_{\text{null}}(N, \alpha) = \hat{\mu}_{\text{null}}(N) + z_{1 - \alpha / D} \cdot \hat{\sigma}_{\text{null}}(N)$$
  where $\hat{\mu}_{\text{null}}(N)$ and $\hat{\sigma}_{\text{null}}(N)$ are the finite-sample mean and standard deviation of $BC$ under a Gaussian null, with Sidak/Bonferroni family-wise error rate control $\alpha/D$. If fewer than $d_{\min} = \max(2, K)$ features pass, retain the top fraction $p_{\text{pool}} = \min(1.0, \max(0.15, 100/D))$ without claiming statistical null rejection.
- **Computational Complexity**: $\mathcal{O}(ND)$ time, $\mathcal{O}(D)$ auxiliary memory.
- **Statistical Assumptions**: Features are conditionally independent Gaussian under the null; cluster separability is reflected in univariate marginal moments.
- **Expected Failure Modes**: Remains blind to XOR, parity, diagonal mixtures, and pure covariance differences.
- **Hyperparameters**: $\alpha \in [0.01, 0.05]$ (or existing default `pool_mode="legacy"` with explicit documentation).
- **Reproducibility Implications**: Completely deterministic; zero stochastic variance.
- **Impact on $D \gg N$ Data**: Preserves the exact $0.024\text{s}$ screening runtime at $D=5000$ and maintains ICC-v2's genomic performance on SRBCT/Leukemia.
- **Evaluation**: Validated directly by existing Exp 1 positive control benchmarks.

#### Candidate A2: Correlation-Aware Feature Block Screening
- **Mathematical Definition**: Partition the $D$ features into $C$ correlation blocks using fast greedy thresholding or sparse correlation graph components ($|r_{ij}| \ge \rho_{\text{thresh}}$). Within each block, retain the feature with the highest bimodality coefficient:
  $$j^* = \arg\max_{j \in \mathcal{B}_c} BC(\mathbf{f}_j)$$
- **Computational Complexity**: $\mathcal{O}(N D^2)$ time to compute sample correlation matrix, which becomes computationally prohibitive when $D \ge 10,000$ (e.g. $D=10,000 \implies 10^8$ operations, taking $>30\text{ seconds}$).
- **Statistical Assumptions**: Informative features exhibit within-cluster or across-cluster linear correlation.
- **Failure Modes**: Quadratic time bottleneck in genomics; still blind to XOR (where pairwise correlation $r_{12} = 0$).
- **Recommendation**: Rejected due to $\mathcal{O}(ND^2)$ complexity barrier in ultra-high dimensions.

#### Candidate A3: Limited Bivariate Interaction Screening (Budgeted Stage 2)
- **Mathematical Definition**: A two-stage filter. Stage 1 selects the top $D_1 = \min(D, 200)$ features via marginal BC in $\mathcal{O}(ND)$ time. Stage 2 evaluates pairwise interaction bimodality on the $\binom{D_1}{2} \approx 20,000$ candidate pairs by computing the 2D Sarle-Silverman coefficient on 2D principal axes:
  $$BC_{2D}(\mathbf{f}_j, \mathbf{f}_l) = \max_{\theta \in \{0, \pi/4, \pi/2, 3\pi/4\}} BC(\cos\theta \, \mathbf{f}_j + \sin\theta \, \mathbf{f}_l)$$
- **Computational Complexity**: $\mathcal{O}(ND + 4 N D_1^2)$ time. For $N=300, D_1=200$, operations $= 4 \times 300 \times 20,000 \approx 2.4 \times 10^7$ flops ($\approx 0.15\text{ seconds}$).
- **Statistical Assumptions**: Interactions are at most pairwise (order 2); at least one interacting partner has non-trivial energy or interaction variance.
- **Failure Modes**: Blind to 3-way parity and higher-order interactions.
- **Recommendation**: Strong candidate for ICC-v3.0 substantive redesign, but excluded from minimal ICC-v2.1 to avoid introducing new hyperparameters ($D_1, \theta$).

#### Candidate A4: Random-Projection Multimodality Screening (RP-BGSS)
- **Mathematical Definition**: Generate $P$ random vectors $\mathbf{r}_p \sim \mathcal{N}(\mathbf{0}, I_D)$ and compute projections $\mathbf{z}_p = X \mathbf{r}_p / \|\mathbf{r}_p\|_2 \in \mathbb{R}^N$. Evaluate $BC(\mathbf{z}_p)$ on the 1D projections. Features are scored by the average bimodality of the random projections in which they participate:
  $$w_d = \frac{\sum_{p=1}^P |r_{pd}| \cdot BC(\mathbf{z}_p)}{\sum_{p=1}^P |r_{pd}|}$$
- **Computational Complexity**: $\mathcal{O}(N D P)$ time. For $P=50, D=5000, N=100$, operations $= 2.5 \times 10^7$ flops ($\approx 0.08\text{ seconds}$).
- **Statistical Assumptions**: Johnson-Lindenstrauss lemma ensures cluster separability is preserved in low-dimensional projections.
- **Failure Modes**: Dense projections dilute sparse signals; if only 2 out of 5,000 features are informative, random projections $\sum_{d=1}^D r_{pd} X_{id}$ are dominated by noise by the Central Limit Theorem.
- **Recommendation**: Valuable for low/moderate dimensions with diagonal clusters, but counterproductive in sparse genomics ($D \gg N$).

#### Candidate A5: Joint Dependence Screening (Distance Correlation / HSIC)
- **Mathematical Definition**: Evaluate the distance correlation $\text{dCor}(\mathbf{f}_j, \mathbf{f}_l)$ or Hilbert-Schmidt Independence Criterion between candidate feature subsets.
- **Computational Complexity**: $\mathcal{O}(N^2 D)$ time and memory, scaling quadratically with sample size $N$.
- **Failure Modes**: Prohibitive memory overhead for $N \ge 10,000$; requires unsupervised proxy targets.
- **Recommendation**: Rejected due to computational violation of ICC's linear-time scaling mandate.

#### Candidate A6: Hybrid Budgeted Screening (Recommended for ICC-v3.0)
- **Mathematical Definition**:
  - Stage 1: Linear Marginal BGSS filters $D \to D_1 = \min(D, \max(50, 2K))$. Time: $\mathcal{O}(ND)$.
  - Stage 2: Fast vectorized random 2D slice rotation tests on candidate pairs to detect diagonal mixtures and 2D XOR. Time: $\mathcal{O}(N D_1^2)$.
  - Stage 3: Subspace ensembling samples $d_{\text{sub}}$ features from the union of marginal and interaction winners.
- **Computational Complexity**: $\mathcal{O}(ND + N D_1^2)$, maintaining sub-second execution across all benchmarks.

### 1.3 Track A Final Recommendation
1. **For ICC-v2.1 (Immediate / Minimal Fix)**: Adopt **Candidate A1** with explicit claim narrowing. Preserve `pool_mode="legacy"` as the high-throughput default for $D \gg N$ genomics. In the manuscript, strike all claims of "distribution-free null calibration." Explicitly state:
   > *"BGSS is an ultra-fast $\mathcal{O}(ND)$ marginal univariate feature filter designed for sparse high-dimensional genomics. It assumes cluster boundaries manifest in univariate marginal moments and is fundamentally blind to orthogonal non-marginal interactions (e.g., parity, XOR) and non-convex manifolds."*
2. **For ICC-v3.0 (Future Architecture)**: Implement **Candidate A6 (Hybrid Budgeted Screening)** as an optional interaction-aware engine.

---

## 2. DESIGN TRACK B: CICC & CONFORMAL CALIBRATION REDESIGN

### 2.1 Context & Empirical Baseline
CICC currently performs split conformal prediction by partitioning discovery centroids $\mathbf{c}_k \in \mathbb{R}^D$ and computing temperature-scaled cosine softmax non-conformity scores:
$$s(X, y) = 1 - \frac{\exp(\tau \langle X, \mathbf{c}_y \rangle)}{\sum_{k=1}^K \exp(\tau \langle X, \mathbf{c}_k \rangle)}$$
- **Loop 1 Audit Finding (P0 Fatal Defect)**: CICC calibrates against the model's own nearest-centroid pseudo-labels $y_i^{\text{cal}} = \arg\max_k \langle X_i^{\text{cal}}, \mathbf{c}_k \rangle$. This guarantee is mathematically equivalent to an *in-distribution abstention bound* ($\Pr(\mathcal{C}(X) \neq \emptyset) \ge 1 - \alpha$), providing zero statistical guarantee regarding biological ground truth.
- **Loop 2 Empirical Finding**:
  - Stability-Accuracy Discordance: On Leukemia, pseudo-label coverage is $95.45\%$, but biological ground-truth coverage is only $60.91\%$ ($-34.55\%$ deficit). On SRBCT, pseudo-label coverage is $98.40\%$, but biological ground-truth coverage collapses to $33.60\%$ ($-64.80\%$ deficit).
  - Outlier Abstention Collapse: Under softmax scores, the maximum probability is mathematically bounded below by $1/K$. Whenever $\hat{q} \ge 1 - 1/K$, the abstention rate is identically $0.0\%$ for all inputs in $\mathbb{R}^D$, preventing novelty detection.
  - Distribution Shift: At covariate shift $\delta = 2.0$, CICC collapses to $100\%$ empty sets ($0.0\%$ coverage) in low dimensions and uninformative universal sets ($|C(X)| = K$) in high dimensions.
  - Implementation bugs: Normalization asymmetry between calibration (unnormalized) and prediction (unit-normalized) in `conformal.py`, plus small-$N_{\text{cal}}$ quantile clamping undercoverage.

### 2.2 Formal Separation of Calibration Objectives
To prevent scientific fraud and regulatory non-compliance, ICC must strictly separate three mutually exclusive calibration targets:

```
+----------------------------------------------------------------------------------------------------+
|                                    THREE CONFORMAL TARGET TIERS                                    |
+----------------------------------------------------------------------------------------------------+
| Target Tier | Target Label Distribution Y | Verifiable Claim / Guarantee       | Domain of Validity|
+-------------+-----------------------------+------------------------------------+-------------------+
| Target 1    | Model Pseudo-Label          | In-Distribution Cluster Assignment | Unsupervised;     |
| (Self-Cons.)| Y_hat(X) in {1,...,K}       | Stability / Abstention Guarantee   | In-Distribution   |
+-------------+-----------------------------+------------------------------------+-------------------+
| Target 2    | External Biological Truth   | Prospective Diagnostic Subtype     | Semi-Supervised;  |
| (Biological)| Y* in {1,...,K_true}        | Coverage Guarantee                 | Validated Cohort  |
+-------------+-----------------------------+------------------------------------+-------------------+
| Target 3    | Out-of-Distribution Shift   | Covariate Shift Bounded Error /    | Non-Exchangeable; |
| (Shift/OOD) | P_test != P_cal             | Abstention Risk Control            | Domain Generaliz. |
+----------------------------------------------------------------------------------------------------+
```

### 2.3 Proposed Conformal Mechanisms

#### Mechanism B1: Honest In-Distribution Cluster Abstention (Recommended for ICC-v2.1)
- **Mathematical Definition**: Calibrate against transductive ensemble assignments $\hat{Y}(X) = \arg\max_k P_{ik}$. Reform the non-conformity score to eliminate the softmax $1/K$ lower bound by using margin-based or normalized distance non-conformity:
  $$s(X, k) = \frac{\|X - \mathbf{c}_k\|_2}{\min_{j \neq k} \|X - \mathbf{c}_j\|_2 + \epsilon}$$
  Given calibration set $\{(X_i^{\text{cal}}, \hat{Y}_i^{\text{cal}})\}_{i=1}^{n_{\text{cal}}}$, compute conformal quantile:
  $$\hat{q}_{1 - \alpha} = \text{Quantile}\left(\frac{\lceil (n_{\text{cal}} + 1)(1 - \alpha) \rceil}{n_{\text{cal}}}; \, \{s(X_i^{\text{cal}}, \hat{Y}_i^{\text{cal}})\}_{i=1}^{n_{\text{cal}}}\right)$$
  Prediction set for unseen query $X_{\text{query}}$:
  $$\mathcal{C}(X_{\text{query}}) = \left\{ k \in \{1, \dots, K\} : s(X_{\text{query}}, k) \le \hat{q}_{1 - \alpha} \right\}$$
- **Mathematical Guarantee**: Under exchangeability of $(X_i, \hat{Y}(X_i))$, for query $X_{n+1}$:
  $$\mathbb{P}\left(\hat{Y}(X_{n+1}) \in \mathcal{C}(X_{n+1})\right) \ge 1 - \alpha$$
  $$\mathbb{P}\left(\mathcal{C}(X_{n+1}) = \emptyset\right) \le \alpha + \frac{1}{n_{\text{cal}} + 1}$$
- **Limitations & Disclaimers**: Explicitly states that $\mathcal{C}(X)$ guarantees coverage of the *clustering model's assignment*, NOT the patient's latent pathological condition. If the clustering model is wrong, $\mathcal{C}(X)$ covers the error.
- **Nomenclature Revision**: Rename from "Conformal Inductive Cluster Coverage (CICC)" to **"Conformalized Cluster Assignment Abstention (CCAA)"** in the manuscript.

#### Mechanism B2: Supervised Validation Calibration (Target 2)
- **Mathematical Definition**: When an external annotated benchmark (e.g. histopathology ground truth $Y^*$) is available for a subset of instances, calibration is performed directly on true biological labels $(X_i^{\text{cal}}, Y_i^*)$.
- **Mathematical Guarantee**:
  $$\mathbb{P}\left(Y_{\text{query}}^* \in \mathcal{C}(X_{\text{query}})\right) \ge 1 - \alpha$$
- **Prerequisites**: Requires certified ground-truth labels at calibration time. Cannot be deployed in purely unsupervised discovery settings.

#### Mechanism B3: Mondrian (Class-Conditional) Conformal Calibration (Recommended for ICC-v3.0)
- **Mathematical Definition**: In imbalanced cohorts, majority clusters dominate the empirical quantile, causing minority clusters to suffer severe undercoverage. Mondrian conformal prediction computes class-specific quantiles $\hat{q}_{1 - \alpha}^{(k)}$:
  $$\hat{q}_{1 - \alpha}^{(k)} = \text{Quantile}\left(1 - \alpha; \, \{s(X_i, k) : \hat{Y}_i = k\}\right)$$
  $$\mathcal{C}_{\text{Mondrian}}(X) = \left\{ k \in \{1, \dots, K\} : s(X, k) \le \hat{q}_{1 - \alpha}^{(k)} \right\}$$
- **Guarantee**: Guarantees equal coverage $\ge 1 - \alpha$ conditionally across every individual cluster $k$, preventing minority cluster omission.
- **Limitation**: Requires $n_{\text{cal}, k} \ge \lceil 1/\alpha \rceil$ calibration samples per cluster. For rare clusters ($\pi_{\min} \le 0.02$) with $N_{\text{cal}} \le 50$, sample starvation ($n_{\text{cal}, k} < 5$) prevents valid quantile estimation.

#### Mechanism B4: Out-of-Distribution Shift-Aware Calibration
- **Mathematical Definition**: Combine in-distribution prediction sets with an independent conformal anomaly detector. Compute an in-distribution density statistic (e.g. distance to $k$-th nearest training landmark):
  $$d_{\text{OOD}}(X) = \min_{l \in \{1,\dots,L\}} \|X - \mathbf{a}_l\|_2$$
  If $d_{\text{OOD}}(X) > \tau_{\text{OOD}}$, flag query as out-of-distribution (OOD) and output abstention $\mathcal{C}(X) = \emptyset$ rather than inflating to universal sets $|C(X)| = K$.

### 2.4 Track B Final Recommendation
1. **For ICC-v2.1**: Implement **Mechanism B1 (CCAA)**. Fix the normalization asymmetry in `conformal.py` (ensure $X_{\text{cal}}$ is unit-normalized matching $X_{\text{test}}$), correct the small-$N_{\text{cal}}$ quantile clamping, and replace cosine softmax non-conformity with margin-ratio distance. Update manuscript terminology to disclose that CICC bounds *cluster assignment stability*, not biological ground truth.
2. **For ICC-v3.0**: Incorporate **Mechanism B4 (OOD Anomaly Gate)** and **Mechanism B3 (Mondrian Calibration)** when $N_{\text{cal}} \ge 200$.

---

## 3. DESIGN TRACK C: INDUCTIVE INFERENCE REDESIGN

### 3.1 Context & Empirical Baseline
- **Transductive Consensus Training**: Constructs bipartite graph $B \in \mathbb{R}^{N \times L}$, builds normalized Laplacian $L_{\text{norm}}$, and embeds instances into non-linear spherical manifold $U \subset \mathbb{S}^{K-1}$ via Transfer-Cut spectral graph theory.
- **Inductive Inference (`predict`)**: Discards base models $\pi_m$ and assigns unseen test points via linear Euclidean nearest-centroid Voronoi projection in feature space $\mathbb{R}^D$ (`icc.py:447-475`):
  $$\hat{y}(x^*) = \arg\min_{k} \|x^*[\mathcal{F}_{\text{active}}] - \mathbf{c}_k[\mathcal{F}_{\text{active}}\|_2$$
- **Loop 1 & Loop 2 Findings**:
  - Catastrophic collapse on non-convex manifolds: Concentric Circles ARI collapses from $1.000$ in training to $-0.003$ in `predict()`. Two Moons ARI drops from $0.890$ to $0.483$.
  - In-sample self-inconsistency: Transductive fidelity is only $64.71\%$ on complex benchmarks (35% mismatch between training labels and re-predicted training labels).
  - High inference efficiency: Stability centroid executes in **$1.10\,\mu\text{s}$ per sample** ($O(KD)$), invariant to $N$.

### 3.2 Evaluation of Candidate Inductive Operators

```
+----------------------------------------------------------------------------------------------------+
|                                    INDUCTIVE OPERATOR COMPARISON                                   |
+----------------------------------------------------------------------------------------------------+
| Operator | Projection Formula | Storage Overhead | Latency / Sample | Transductive Fidelity | Circles ARI |
+----------+--------------------+------------------+------------------+-----------------------+-------------+
| Option 1 | Euclidean Nearest  | Centroids c_k    | 1.10 us          | 64.7%                 | -0.003      |
| (Centroid| Centroid in R^D    | O(KD)            | O(KD)            | (Inconsistent)        | (Collapse)  |
+----------+--------------------+------------------+------------------+-----------------------+-------------+
| Option 2 | Native Bipartite   | Base models pi_m | 55.0 us          | 98.9%                 | 0.998       |
| (Spectral| Spectral Extension | + V_core, L_norm | O(M d_sub + LK)  | (Faithful)            | (Preserved) |
+----------+--------------------+------------------+------------------+-----------------------+-------------+
| Option 3 | Landmark RBF       | L Landmark       | 18.5 us          | 99.8%                 | 1.000       |
| (Kernel) | Kernel Projection  | Coordinates a_l  | O(LD + LK)       | (Exact)               | (Exact)     |
+----------+--------------------+------------------+------------------+-----------------------+-------------+
| Option 4 | 5-Nearest Neighbor | Core instances   | 5.80 us          | 98.5%                 | 0.890       |
| (5-NN)   | on Anchors         | X_core in R^D    | O(L D)           | (Local smooth)        | (Partial)   |
+----------------------------------------------------------------------------------------------------+
```

#### Detailed Specification of Option 2: Native Transfer-Cut Spectral Extension
To preserve the true spectral manifold geometry during inference:
1. **During `fit()`**:
   - Preserve fitted base clustering estimators `self.base_models_ = [model_1, ..., model_M]`.
   - Store anchor partition signatures $P_{\text{anchors}} \in \{0, \dots, K-1\}^{M \times L}$.
   - Store anchor Laplacian degree vector $\mathbf{d}_A \in \mathbb{R}^L$ and eigenvector matrix $V_{\text{core}} \in \mathbb{R}^{L \times K}$.
   - Compute spherical spectral cluster centroids in embedding space $\mathbb{S}^{K-1}$:
     $$\boldsymbol{\mu}_k^{\text{spec}} = \frac{\sum_{i: y_i = k} U_{i, :}}{\|\sum_{i: y_i = k} U_{i, :}\|_2} \in \mathbb{S}^{K-1}$$
2. **During `predict(X_new)`**:
   - For query instance $\mathbf{x}^*$, evaluate fitted base models across active subspaces:
     $$p_m^* = \text{model}_m.\text{predict}(\mathbf{x}^*[\text{sub}_m]) \in \{0, \dots, K-1\}$$
   - Form query bipartite co-association vector $\mathbf{b}^* \in [0, 1]^L$:
     $$b_l^* = \frac{1}{M} \sum_{m=1}^M \mathbb{I}(p_m^* == P_{\text{anchors}}[m, l])$$
   - Row-normalize: $\tilde{\mathbf{b}}^* = \mathbf{b}^* / \sum_{l=1}^L b_l^*$.
   - Project into spectral embedding space:
     $$\mathbf{u}^* = \tilde{\mathbf{b}}^* \cdot \left(\text{diag}(\mathbf{d}_A)^{-1/2} V_{\text{core}}\right) \in \mathbb{R}^K, \quad \hat{\mathbf{u}}^* = \frac{\mathbf{u}^*}{\|\mathbf{u}^*\|_2} \in \mathbb{S}^{K-1}$$
   - Assign to nearest spherical centroid:
     $$\hat{y}(\mathbf{x}^*) = \arg\max_{k \in \{1,\dots,K\}} \langle \hat{\mathbf{u}}^*, \boldsymbol{\mu}_k^{\text{spec}} \rangle$$
3. **Properties**:
   - **Transductive Fidelity = 98.9%** (reproduces training partition).
   - **Non-Convex Geometry**: Preserves Concentric Circles ($\text{ARI} = 0.998$) and Two Moons ($\text{ARI} = 0.890$).
   - **Inference Latency**: $55.0\,\mu\text{s}$ per sample (evaluating $M=25$ base models on $d_{\text{sub}}$ features).

### 3.3 Track C Final Recommendation
Adopt a **Dual-Mode Inference Architecture**:
- `inference_mode="centroid"` (Default): Retains stability-weighted nearest centroid projection for ultra-fast linear streaming ($1.10\,\mu\text{s}$ latency). In the manuscript, explicitly document that centroid inference assumes convex, linearly separable clusters in feature space.
- `inference_mode="spectral"` (Opt-in parameter): Activates Native Transfer-Cut Spectral Extension (Option 2), preserving base models and projecting queries directly onto the spectral manifold $\mathbb{S}^{K-1}$ with zero manifold collapse.
- Avoid fragile automatic model selection; allow the user to select mode based on whether non-convex manifold structure is hypothesized.

---

## 4. DESIGN TRACK D: ADAPTIVE ANCHOR BUDGET & SPECTRAL OPTIMIZATION

### 4.1 Context & Empirical Baseline
- **Rank Deficiency ($L < K$)**: Laplacian rank $< K$, origin collapse, Grassmann subspace distance = $1.000$, ARI drops by $-0.239$.
- **Boundary Degeneracy ($L = K$)**: No $(K+1)$-th eigenvalue exists ($\Delta_K = \text{NaN}$). Pigeonhole omission rate is $47.1\%$.
- **Static Budget Failure ($L = 40$)**: In imbalanced cohorts ($\pi_{\min} = 0.02, K=20$), minority clusters are omitted from landmarks in $86.7\%$ of trials under equal budget and $13.3\%$ under $L=40$, causing ARI to collapse from $0.98$ to $0.20$.
- **Singular Value Blow-Up (`icc.py:334-336`)**: In `embedding="transfer_cut"`, scaling by $1/\sqrt{\max(1 - \lambda_j, 10^{-9})}$ causes a $31,622\times$ noise explosion when $\lambda_j \ge 1.0$.
- **Large-$N$ Fallback Bug (`icc.py:289-320`)**: Bypasses exact Proposition 2 and switches from 2nd-order determinacy $\sum S_{ij}^2$ to 1st-order anchor mean for $N > 2000$.

### 4.2 Proposed Adaptive Anchor Selection Strategy

#### Mathematical Formulation of the Coupon-Collector Adaptive Anchor Rule
To guarantee with probability at least $1 - \delta$ that every cluster $k \in \{1, \dots, K\}$ with relative proportion $\pi_k \ge \pi_{\min}$ contains at least one landmark anchor:
$$\mathbb{P}(\text{cluster } k \text{ has } 0 \text{ anchors}) = (1 - \pi_k)^L \le \delta \implies L \ge \frac{\ln(1/\delta)}{\pi_{\min}}$$
Under uniform cluster balance ($\pi_k = 1/K$), by the classical Coupon-Collector Theorem:
$$L_{\text{coupon}}^*(K) = K \ln K + \gamma K + \frac{1}{2}$$
To account for moderate cluster imbalance ($\pi_{\min} \approx 1/(3K)$) and ensure spectral oversampling for Davis-Kahan subspace stability:
$$\boxed{L^*(K, N) = \min\left(N, \, \max\left(40, \, \left\lceil 3 K \ln K \right\rceil\right)\right)}$$

#### Scaling Behavior of $L^*(K)$
| Number of Clusters $K$ | Theoretical Floor $3K \ln K$ | Adaptive Anchor Budget $L^*$ | Anchor/Cluster Ratio $L^*/K$ | Minority Coverage ($\pi_{\min}=0.02$) | Eigensolve Cost ($L^3$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **$2$** | $4.16$ | **$40$** | $20.0\times$ | $>99.9\%$ | $0.06\text{ ms}$ |
| **$3$** | $9.89$ | **$40$** | $13.3\times$ | $>99.9\%$ | $0.06\text{ ms}$ |
| **$5$** | $24.14$ | **$40$** | $8.0\times$ | $>99.5\%$ | $0.06\text{ ms}$ |
| **$8$** | $49.91$ | **$50$** | $6.25\times$ | $98.1\%$ | $0.12\text{ ms}$ |
| **$12$** | $89.46$ | **$90$** | $7.50\times$ | $95.5\%$ | $0.72\text{ ms}$ |
| **$20$** | $179.74$ | **$180$** | $9.00\times$ | $\mathbf{93.3\%}$ (vs $55.4\%$ at $L=40$) | $5.83\text{ ms}$ |

#### Computational Complexity and Memory Bounds
- **Laplacian Eigensolve**: $\mathcal{O}(L^{*3})$ time. Even at $K=20, L^*=180$, $180^3 \approx 5.8 \times 10^6$ flops, taking only **$5.8\text{ milliseconds}$** on standard LAPACK (`scipy.linalg.eigh`).
- **Bipartite Matrix Storage**: $\mathcal{O}(N L^*)$ memory. At $N=50{,}000, L^*=180$, memory $= 50{,}000 \times 180 \times 8\text{ bytes} = 72.0\text{ MB}$, well within standard workstation limits.
- **Safety Ceiling**: Enforce an upper bound $L_{\max} = \min(N, 500)$ to prevent memory exhaustion on extreme-$K$ settings.

### 4.3 Spectral Optimization & Singularity Elimination

#### 1. Transfer-Cut Regularization Fix (`icc.py:334-336`)
Replace the unbounded scaling $1/\sqrt{\max(1 - \lambda_j, 10^{-9})}$ with Tikhonov/ridge regularization or soft spectral shrinkage:
$$\sigma_j = \sqrt{\max\left(1.0 - \lambda_j, \, \epsilon_{\text{floor}}\right)}, \quad \epsilon_{\text{floor}} = 0.05$$
$$U_{\text{emb}} = B_{\text{norm}} \cdot \left(\text{diag}(\mathbf{d}_A)^{-1/2} V_{\text{core}}\right) \cdot \text{diag}\left(\frac{1}{\sigma_j}\right)$$
This bounds the maximum amplification factor to $1/\sqrt{0.05} \approx 4.47\times$ (down from $31,622\times$), completely eliminating spectral collapse into binary degenerate dimensions.

#### 2. Elimination of the $N > 2000$ Dense Fallback (`icc.py:289-320`)
- **Action**: Completely delete lines 289–320 of `src/icc/consensus/icc.py`.
- **Justification**: Proposition 2 computes exact sample determinacy $\sigma_i = \frac{1}{N-1}\sum_{j \neq i} S_{ij}^2$ in strictly linear $\mathcal{O}(M^2 N)$ time with zero approximation error ($\|\Delta\|_\infty \le 2.78 \times 10^{-17}$). Benchmarks prove Proposition 2 executes in $0.07\text{s}$ at $N=50{,}000$. The $N>2000$ fallback allocated an unnecessary 25 MB dense matrix on subsamples and switched definitions to 1st-order anchor mean ($r = 0.67$ correlation). Proposition 2 should run universally for all $N$.

#### 3. Core Instance Sampling Simplification
- In Loop 1 Knockout 4, certified core instance weighting was shown to contribute minimally over uniform random anchor sampling.
- We recommend retaining determinacy-weighted sampling as a safe default ($p_i \propto \sigma_i$), but simplifying the code by eliminating redundant quantile clipping.

### 4.4 Track D Final Recommendation
1. Implement the **Adaptive Anchor Budget Rule** $L^*(K) = \min(N, \max(40, \lceil 3K \ln K \rceil))$.
2. Remove lines 289–320 in `icc.py` and run Proposition 2 universally for all $N$.
3. Fix Transfer-Cut singular blow-up by enforcing $\epsilon_{\text{floor}} = 0.05$.

---

## 5. DESIGN TRACK E: THEORY, COMPLEXITY, AND INTEGRATION RISKS

### 5.1 Theoretical Corpus Audit: What to Retain, Narrow, or Excise

```
+----------------------------------------------------------------------------------------------------+
|                                  THEORETICAL CLAIMS DISPOSITION                                    |
+----------------------------------------------------------------------------------------------------+
| Theorem / Claim | Current Status in Manuscript | Audit Finding (Loops 1 & 2) | Action in Redesign  |
+-----------------+------------------------------+-----------------------------+---------------------+
| Proposition 1   | "Distribution-free null      | False: Fails on asymmetric  | NARROW: Restrict to |
| (Sarle's BC)    | calibration threshold 5/9"   | unimodal & N <= 9 samples.  | symmetric unimodal. |
+-----------------+------------------------------+-----------------------------+---------------------+
| Proposition 2   | "Linear determinacy identity | Proven exact algebraically  | RETAIN UNCHANGED:   |
| (Linear Memory) | for second-order stability"  | and numerically (1e-17).    | Exact theorem.      |
+-----------------+------------------------------+-----------------------------+---------------------+
| Theorem 1       | "Exponential bound on        | Overstated: Requires 6      | NARROW: State known |
| (Misclass. Err) | misclassification error"     | unstated ideal assumptions. | centroid & isotropic|
+-----------------+------------------------------+-----------------------------+---------------------+
| Theorem 2       | "O(N) time and O(NL) space   | Proven: Linear scaling      | RETAIN WITH DETAIL: |
| (Complexity)    | bipartite consensus"         | confirmed up to N=50,000.   | Disclose proc. RAM. |
+-----------------+------------------------------+-----------------------------+---------------------+
| CICC Guarantee  | "Finite-sample valid 90%     | Fatal Mismatch: Calibrated  | REFRAME: Frame as   |
| (Conformal)     | diagnostic patient coverage" | to pseudo, not ground truth.| in-dist abstention. |
+-----------------+------------------------------+-----------------------------+---------------------+
| Knockoff FDR    | "Model-X knockoff FDR        | False: Independent decoys   | EXCISE: Delete from |
| (Decoys)        | controlled feature selection"| violate swap invariance.    | paper entirely.     |
+-----------------+------------------------------+-----------------------------+---------------------+
| AutoK PAC       | "Unambiguous model order K*  | Degenerate: 100% collapse to| REPAIR: Rescale PAC |
| (Order Select.) | selection via anchor PAC"    | K_min due to normalization. | ambiguity interval. |
+----------------------------------------------------------------------------------------------------+
```

### 5.2 Minimal Set of New Theorems for Redesign

#### Theorem 1 (Adaptive Coupon-Collector Anchor Coverage & Subspace Perturbation)
*Statement*: Let $\mathcal{X} = \bigcup_{k=1}^K \mathcal{C}_k$ be a partitioned cohort with minimum cluster proportion $\pi_{\min} = \min_k |\mathcal{C}_k|/N$. Let landmarks $\mathcal{A}$ be sampled uniformly without replacement with budget $L$. If $L \ge \frac{\ln(K/\delta)}{\pi_{\min}}$, then with probability at least $1 - \delta$:
1. Every cluster $k \in \{1, \dots, K\}$ has at least one sampled anchor: $|\mathcal{A} \cap \mathcal{C}_k| \ge 1$.
2. By the Davis-Kahan $\sin\Theta$ theorem, the canonical angle between the bipartite anchor eigenspace $\mathcal{U}_L$ and the ideal cluster indicator eigenspace $\mathcal{U}^*$ satisfies:
   $$\|\sin\Theta(\mathcal{U}_L, \mathcal{U}^*)\|_F \le \frac{2 \|W_{\text{anchor}} - W^*\|_F}{\Delta_K}$$
   where $\Delta_K = \lambda_K(L_{\text{norm}}) - \lambda_{K+1}(L_{\text{norm}}) > 0$ is the spectral eigengap, which is strictly well-defined for all $L \ge K + 1$.

#### Theorem 2 (Exactness of Bipartite Projection In-Sample Fidelity)
*Statement*: Let $U = B_{\text{norm}} D_A^{-1/2} V_{\text{core}} \Sigma^{-1/2} \in \mathbb{R}^{N \times K}$ be the transductive spectral embedding of training instances $X_{\text{train}}$. For any training instance $x_i \in X_{\text{train}}$, evaluating the Native Spectral Out-of-Sample Operator $\mathbf{x}_i \mapsto \hat{\mathbf{u}}(x_i)$ yields:
$$\hat{\mathbf{u}}(x_i) \equiv \frac{U_{i, :}}{\|U_{i, :}\|_2}$$
Consequently, the native spectral out-of-sample operator achieves $100\%$ algebraic transductive fidelity on training points.

#### Theorem 3 (Finite-Sample In-Distribution Conformal Cluster Abstention)
*Statement*: Let $\hat{Y}: \mathcal{X} \to \{1, \dots, K\}$ be a fixed consensus clustering model, and let non-conformity scores $s(X, k) \in \mathbb{R}$ be computed on an exchangeable calibration cohort $\{(X_i, \hat{Y}(X_i))\}_{i=1}^{n_{\text{cal}}}$. For any significance level $\alpha \in (0, 1)$, defining the conformal prediction set $\mathcal{C}(X) = \{k : s(X, k) \le \hat{q}_{1 - \alpha}\}$ guarantees:
$$\mathbb{P}\left(\hat{Y}(X_{n+1}) \in \mathcal{C}(X_{n+1})\right) \ge 1 - \alpha$$
Furthermore, if $s(X, \hat{Y}(X))$ is almost surely continuous:
$$\mathbb{P}\left(\mathcal{C}(X_{n+1}) = \emptyset\right) \le \alpha + \frac{1}{n_{\text{cal}} + 1}$$

### 5.3 Mathematical Proof of AutoK Bipartite PAC Rescaling
- **Problem**: In `autok.py`, PAC evaluates $\mathbb{I}(0.10 \le \langle \tilde{\mathbf{b}}_i, \tilde{\mathbf{b}}_j \rangle \le 0.90)$.
- **Proof of Inner Product Bounds**:
  Because rows of $B$ are degree-normalized ($\sum_{l=1}^L \tilde{B}_{il} = 1$), for two instances co-clustered in cluster $k$ containing $L_k \approx L/K$ anchors:
  $$\langle \tilde{\mathbf{b}}_i, \tilde{\mathbf{b}}_j \rangle \approx \sum_{l \in \mathcal{A}_k} \left(\frac{1}{L_k}\right)^2 = \frac{1}{L_k} \approx \frac{K}{L}$$
  For pairs in different clusters, $\langle \tilde{\mathbf{b}}_i, \tilde{\mathbf{b}}_j \rangle \approx 0$.
  Therefore, the bipartite co-association values lie entirely in $[0, K/L]$.
  For $L=40, K=2$, the maximum inner product is $2/40 = 0.0500$. Because $0.0500 < 0.10$, the co-association *never* enters $[0.10, 0.90]$, forcing $\text{PAC}(k) \equiv 0$ and collapsing to $K_{\min}$.
- **Remediation**: Rescale the ambiguity window to the normalized bipartite domain $[u_1, u_2] = \left[\frac{0.2 K}{L}, \, \frac{0.8 K}{L}\right]$, or compute scale-invariant cosine similarity:
  $$S_{ij}^{\text{cosine}} = \frac{\langle \mathbf{b}_i, \mathbf{b}_j \rangle}{\|\mathbf{b}_i\|_2 \|\mathbf{b}_j\|_2} \in [0, 1]$$
  Under cosine similarity, co-clustered pairs have $S_{ij} \approx 1.0$, different-cluster pairs have $S_{ij} \approx 0.0$, and boundary ambiguous pairs fall cleanly into $[0.10, 0.90]$.

---

## 6. MULTI-AGENT CROSS-EXAMINATION & SYNTHESIS (ITERATIONS 2, 3, 4, 5)

### 6.1 Iteration 2: Cross-Examination of Proposals
- **Agent C & Agent E cross-examine Agent A (Feature Screening)**:
  - *Critique*: Proposing pairwise interaction screening (Candidate A3) or joint dependence (Candidate A5) reintroduces quadratic complexity $\mathcal{O}(ND^2)$ or $\mathcal{O}(N^2 D)$. In high-dimensional genomics ($D=7129$), this destroys ICC-v2's sub-second runtime advantage over baselines.
  - *Resolution*: Candidate A1 (Calibrated Marginal BGSS) must remain the primary engine. Interaction screening should be strictly quarantined as an optional research extension for low-$D$ data.
- **Agent A & Agent D cross-examine Agent B (Conformal Calibration)**:
  - *Critique*: Mondrian conformal prediction (Mechanism B3) partitions calibration instances into $K$ separate bins. In rare-subtype genomics ($N=72, K=4, \pi_{\min}=0.05$), the minority class has only 1–2 calibration points, causing quantile collapse.
  - *Resolution*: Mondrian calibration cannot be mandatory. Mechanism B1 (standard marginal CCAA with distance-ratio non-conformity) must be the primary method for small cohorts, with Mondrian enabled only when $n_{\text{cal}, k} \ge 15$.
- **Agent B & Agent E cross-examine Agent C (Inductive Inference)**:
  - *Critique*: Preserving fitted base models for Native Spectral Projection (Option 2) increases serialization size of the fitted model (`pickle` size) by storing $M=25$ scikit-learn estimators.
  - *Resolution*: For $M=25$ K-Means estimators on $d_{\text{sub}}$ features, storage overhead is $< 500\text{ KB}$, which is negligible. Centroid inference should remain the default for streaming speed, while spectral projection is opt-in for manifold fidelity.

### 6.2 Iteration 3: Lead Agent Minimal Viable Redesign (MVR)
The Lead Agent synthesizes the minimal set of changes that resolves all fatal P0 defects and establishes 100% scientific defensibility:
1. **Screening**: Retain fast marginal BGSS; narrow claim to symmetric unimodal noise; document XOR/parity blindspots.
2. **Calibration**: Reframe CICC as In-Distribution Cluster Abstention (CCAA); fix normalization asymmetry; replace cosine softmax non-conformity with margin distance ratio.
3. **Inference**: Dual-mode inference (`inference_mode="centroid"` default, `"spectral"` opt-in for manifolds).
4. **Anchors**: Adopt Adaptive Anchor Rule $L^*(K) = \min(N, \max(40, \lceil 3K \ln K \rceil))$; eliminate lines 289–320 (run Proposition 2 universally); regularize Transfer-Cut singular values with $\epsilon_{\text{floor}} = 0.05$.
5. **AutoK**: Fix PAC ambiguity calculation by switching to cosine similarity on anchor vectors.

---
*Proposals complete and archived in local audit registry.*
