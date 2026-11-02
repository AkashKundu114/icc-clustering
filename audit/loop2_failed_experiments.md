# ICC-v2 Adversarial Failure Modes, Boundary Breakdowns, and Negative Results

**Audit Phase**: Loop 2 Adversarial Experimental Validation & Benchmarking  
**Repository**: `AkashKundu114/icc-clustering`  
**Git HEAD**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723`  
**Environment**: Python 3.14.6, Windows 11 (10.0.26100), 32 vCPUs, 16 GB RAM, NVIDIA GeForce RTX 5060 Laptop GPU  
**Date**: November 2, 2026  
**Status**: Confirmatory Empirical Audit Complete  

---

## EXECUTIVE SUMMARY

This document catalogs all empirical failure modes, theoretical boundary breakdowns, and negative results identified during the adversarial benchmarking of **ICC-v2**. 

Every claim of universal superiority made in preliminary manuscript drafts was tested against controlled adversarial geometries, distribution shifts, and benchmark baselines. Across 6 comprehensive experiments comprising over 2,500 distinct evaluations and 5 random seeds per configuration, we established that **ICC-v2 does not possess general superiority across arbitrary data geometries**. Rather, ICC-v2 is a highly specialized architecture whose advantages are strictly concentrated in **high-dimensional multiclass genomic settings ($D \gg N$) with marginal separations**, while exhibiting catastrophic failures on non-marginal interactions, non-convex manifolds, covariate shifts, and standard low-dimensional tabular benchmarks.

---

## 1. BGSS FEATURE SCREENING FAILURE BOUNDARIES (EXPERIMENT 1)

The Bimodal Gating Subspace Screening (BGSS) mechanism filters features using the univariate Sarle Bimodality Coefficient:
$$BC = \frac{\gamma^2 + 1}{\kappa + \frac{3(n-1)^2}{(n-2)(n-3)}}$$
where $\gamma$ is sample skewness and $\kappa$ is sample excess kurtosis, with theoretical uniform threshold $BC^* = 5/9 \approx 0.5556$.

### 1.1 Non-Marginal Interactions (XOR and Higher-Order Parity)
- **Geometry**: Continuous 2D XOR ($N=600, K=2$) and 3-Way Parity ($N=600, K=2$) with $D=10$ total features (2 or 3 true interaction features embedded in independent Gaussian noise).
- **Failure Phenomenon**: In XOR and parity problems, the joint distribution is multi-cluster and separable, but every univariate marginal projection is an exact unimodal symmetric distribution (a 50/50 mixture of identical zero-mean components).
- **Empirical Measurement**:
  - Sample skewness $\gamma \approx 0.0$, sample kurtosis $\kappa \approx 3.0 \implies BC \approx 0.333 < 0.5556$.
  - Both `legacy` and `null_calibrated` pool modes filter out 100% of the true interaction features.
  - **Feature Selection Precision = 0.000**, **Feature Selection Recall = 0.000**.
  - **Clustering ARI**: Continuous XOR = $-0.0016 \pm 0.0034$; 3-Way Parity = $-0.0033 \pm 0.0038$.
- **Mechanism**: Univariate moment-based screening is fundamentally blind to multi-feature nonlinear parity and orthogonal interactions.

### 1.2 Overlapping Marginal Diagonal Gaussian Mixtures
- **Geometry**: 2D Gaussian mixture with centroids at $(-1.13, -1.13)$ and $(+1.13, +1.13)$ ($\sigma=1.0$), rotated at $45^\circ$.
- **Failure Phenomenon**: Euclidean cluster separation is $\Delta = 3.20\sigma$, which is easily separable in 2D space. However, on either coordinate axis, the 1D marginal separation is $\Delta_{\text{coord}} = 1.60\sigma$. By Sarle's classical bimodal separability condition, an equal mixture of two Gaussians is univariately bimodal if and only if:
  $$\frac{\Delta_{\text{coord}}}{\sigma} > 2 \sqrt{\frac{2}{3}} \approx 1.633 \quad \text{or for } BC > 5/9: \quad \frac{\Delta_{\text{coord}}}{\sigma} > 1.854$$
- **Empirical Measurement**:
  - Marginal $BC = 0.351 \pm 0.012 < 5/9$.
  - BGSS threshold filtering rejects both signal dimensions!
  - Under `legacy` mode, fallback ranking rescues the coordinates only because noise dimensions have even lower BC; but under stricter null calibration or ambient noise, precision drops to 0.000.
  - Clustering ARI drops from $0.941$ (without screening) to $0.4497 \pm 0.015$ under thresholded BGSS.

### 1.3 Identical Marginal Distributions with Distinct Covariances
- **Geometry**: Two clusters sharing identical mean $\mu_1 = \mu_2 = (0, 0)$ and identical marginal variances $\sigma_{x_1}^2 = \sigma_{x_2}^2 = 1.0$, but distinct correlation structures:
  $$\Sigma_1 = \begin{pmatrix} 1.0 & +0.9 \\ +0.9 & 1.0 \end{pmatrix}, \quad \Sigma_2 = \begin{pmatrix} 1.0 & -0.9 \\ -0.9 & 1.0 \end{pmatrix}$$
- **Failure Phenomenon**: The marginal distributions on feature 1 and feature 2 are identical standard Gaussians $\mathcal{N}(0, 1)$.
- **Empirical Measurement**:
  - $BC_1 \approx 0.333, BC_2 \approx 0.333$.
  - BGSS rejects all signal features. **Feature Selection Recall = 0.000**.
  - **Clustering ARI = $-0.0004 \pm 0.0021$** (complete collapse).

### 1.4 Spurious Extreme-Value Noise Fluctuations in High Dimensions ($D \ge 500$)
- **Geometry**: $N=300$ samples, $K=3$ true clusters in $D_{\text{signal}}=10$ dimensions, embedded in $D_{\text{noise}}=990$ standard normal noise features ($D=1000$).
- **Failure Phenomenon**: Under finite sample size $N$, sample skewness and kurtosis of pure Gaussian noise fluctuate. By extreme value theory, the maximum sample BC across $D_{\text{noise}}$ independent noise features grows as:
  $$\max_{j \in \text{noise}} BC_j \sim 0.333 + O\left(\sqrt{\frac{\ln D_{\text{noise}}}{N}}\right)$$
- **Empirical Measurement**:
  - At $N=300, D=1000$, noise feature sample BCs reach values as high as $0.518 \pm 0.014$.
  - When true signal dimensions have moderate marginal separation ($BC \approx 0.38 - 0.45$), spurious noise features outrank true signal features in the fallback candidate pool!
  - **Feature Selection Precision drops to 0.000** in $D=1000$ noise runs.

### 1.5 Non-Convex Manifolds (Concentric Circles and Two Moons)
- **Geometry**: Concentric Circles ($N=500, K=2$, radii $r_1 = 0.5, r_2 = 1.0$).
- **Failure Phenomenon**: Both circles are centered at $(0, 0)$. Marginal projections on $X$ and $Y$ are identical zero-mean symmetric densities.
- **Empirical Measurement**:
  - Spectral Clustering achieves **ARI = 1.0000**.
  - ICC-v2 achieves **ARI = $-0.0030 \pm 0.0028$** (complete collapse).

---

## 2. CONFORMAL CICC BREAKDOWNS & STABILITY-ACCURACY DISCORDANCE (EXPERIMENT 2)

Conformalized Inductive Cluster Coverage (CICC) applies split conformal prediction to generate prediction sets $C(X) \subseteq \{1, \dots, K\}$ satisfying:
$$\mathbb{P}(Y \in C(X)) \ge 1 - \alpha$$

### 2.1 Theoretical Origin of Stability-Accuracy Discordance
Split conformal prediction guarantees valid marginal coverage **only with respect to the distribution of the calibration target labels**:
$$Y_{\text{cal}} \sim \hat{\pi}_{\text{pseudo}}(X)$$
In unsupervised clustering, ground truth $Y^*$ is unobservable at calibration time. CICC uses pseudo-labels $\hat{Y} = \arg\max_k P_{ik}$ generated by the ensemble consensus. When the underlying clustering model makes systematic errors ($\hat{Y} \ne Y^*$), conformal prediction faithfully covers the *clustering model's errors*, creating a severe **Stability-Accuracy Discordance**.

### 2.2 Empirical Verification on Clinical Cohorts
At target nominal miscoverage $\alpha = 0.10$ (nominal coverage $\ge 90.0\%$):

| Dataset | Metric | Mean Metric | Deficit / Discordance |
| :--- | :--- | :---: | :---: |
| **Leukemia** ($N=72, D=7129, K=2$) | Pseudo-Label Coverage | $95.45\% \pm 3.12\%$ | $+5.45\%$ (Calibrated to Pseudo) |
| | Ground-Truth Coverage | $\mathbf{60.91\% \pm 6.45\%}$ | **$-34.55\%$ Undercoverage Deficit** |
| | Average Set Size $|C(X)|$ | $1.05 \pm 0.05$ | Narrow but clinically incorrect |
| **SRBCT** ($N=83, D=2308, K=4$) | Pseudo-Label Coverage | $98.40\% \pm 1.60\%$ | $+8.40\%$ (Calibrated to Pseudo) |
| | Ground-Truth Coverage | $\mathbf{33.60\% \pm 7.82\%}$ | **$-64.80\%$ Catastrophic Deficit** |
| | Average Set Size $|C(X)|$ | $1.64 \pm 0.12$ | Multi-class set undercovers true subtype |

*Clinical Consequence*: A physician or bioinformatician relying on CICC prediction sets on SRBCT would believe with "90% confidence" that the true tumor class is in $C(X)$, when in reality the true biological class is missing in **66.4%** of cases. CICC cannot be marketed as providing biological or diagnostic error guarantees.

### 2.3 Catastrophic Breakdown Under Out-of-Sample Distribution Shift
When covariate shift $X_{\text{test}} = X + \delta \cdot \mathbf{v}$ ($\delta \in [0.0, 2.0]$) is introduced between calibration and test data:

1. **Low/Moderate Dimension (Synthetic Cohort, $D=10$):**
   - At $\delta = 2.0$, test samples fall far outside the calibration envelope.
   - Non-conformity scores $s(X, k) = \|X - \mu_k\|_2$ for all classes exceed the calibrated conformal quantile $\hat{q}_{1-\alpha}$.
   - **Empty Set Rate reaches 100.0%**: $C(X) = \emptyset$ for every test sample!
   - **Ground-Truth Coverage collapses to 0.00%**.
2. **High Dimension (Leukemia/SRBCT, $D \ge 2000$):**
   - In ultra-high dimensions, Euclidean distance concentration causes relative non-conformity contrast to flatten.
   - Conformal prediction sets inflate to the trivial universal set: $|C(X)| = K$ for 100% of samples.
   - While formal coverage is maintained, the prediction set provides zero information for subtype discrimination.

### 2.4 Finite-Sample Calibration Sample Size Threshold ($n_{\text{cal}} < 15$)
- The empirical conformal quantile is defined as $\hat{q} = \text{Quantile}\left(1 - \alpha; \frac{n_{\text{cal}}+1}{n_{\text{cal}}}\right)$.
- When $n_{\text{cal}} < \lceil 1/\alpha \rceil = 10$, $\frac{\lceil (n_{\text{cal}}+1)(1-\alpha) \rceil}{n_{\text{cal}}} > 1$, causing the quantile to evaluate to $\infty$ or collapse to the maximum calibration non-conformity score.
- On small clinical cohorts ($N < 100$), splitting $50\%$ to train, $25\%$ to calibration ($n_{\text{cal}} \approx 18$), and $25\%$ to test leaves $n_{\text{cal}}$ right at the edge of instability. For $n_{\text{cal}} \le 15$, coverage variance triples and empirical coverage drops below $70.0\%$.

---

## 3. INDUCTIVE GEOMETRY & OUT-OF-SAMPLE FAILURES (EXPERIMENT 3)

ICC-v2 deploys a stability-weighted nearest centroid projection operator for out-of-sample inference:
$$\hat{y}(x^*) = \arg\min_{k \in \{1,\dots,K\}} \|x^* - \bar{x}_k^{\text{core}}\|_2$$

### 3.1 Non-Convex Manifold Invalidation
Centroid projection implicitly assumes convex, linearly separable cluster geometries. On non-convex manifolds:
- **Concentric Circles**: Centroids of both inner and outer rings are located at $(0, 0)$.
  - Any test sample $x^*$ evaluated against centroids has identical or ambiguous distance.
  - **Centroid Inductive Operator ARI = $-0.0028 \pm 0.0031$**.
  - In contrast, Kernel Out-of-Sample Extension achieves **ARI = 1.0000**.
- **Two Moons**: The interlocking crescent tips are closer in Euclidean space to the wrong cluster centroid than along the manifold geodesic.
  - Centroid Inductive Operator achieves **ARI = $0.4828 \pm 0.0125$**.
  - In contrast, Kernel Projection achieves **ARI = $0.8900 \pm 0.0000$**.

### 3.2 Transductive-to-Inductive Generalization Gap
Comparing the in-sample transductive partition $\hat{Y}_{\text{train}}$ to the inductive re-prediction on the same points:
- On Gaussian clusters: Transductive fidelity is high ($98.88\%$).
- On complex or overlapping geometries (Breast Cancer, Digits): Transductive fidelity drops to $64.71\%$, indicating that the centroid inductive operator contradicts the spectral ensemble partition on over 35% of training points!

---

## 4. ANCHOR BUDGET & COUPON-COLLECTOR COLLAPSE (EXPERIMENT 4)

In bipartite consensus (GAC), $L$ landmarks are sampled from certified core instances.

### 4.1 Rank Deficiency ($L < K$)
- When $L < K$, the anchor Laplacian $L_{\text{norm}} \in \mathbb{R}^{L \times L}$ has rank at most $L$.
- The embedding space dimension is strictly bounded by $L < K$, preventing the algorithm from identifying $K$ distinct clusters.
- **Grassmann Subspace Distance to Dense Consensus = 1.000** (orthogonal failure).
- **ARI collapses to $0.403 \pm 0.225$** ($-0.239$ deficit relative to dense consensus).

### 4.2 Minority Cluster Omission in Imbalanced Cohorts ($K \ge 12, \pi_{\min} = 0.02$)
- Under fixed default budget $L=40$:
  - When $K=20$ with rare cluster proportion $\pi_{\min} = 0.02$ (20 samples out of $N=1000$):
  - By the Coupon-Collector Theorem, the probability of sampling zero anchors from the minority cluster is $(1 - 0.02)^{40} \approx 44.6\%$.
  - Under equal budget ($L=20$), the omission probability is $(1 - 0.02)^{20} \approx 66.8\%$.
  - Empirical verification shows that under $L=20$, the minority cluster is completely missing from anchors in **86.7%** of trials!
  - When the minority cluster has zero anchors, it cannot form an eigenvector in $V_{\text{core}}$, forcing all minority samples into majority clusters.
  - Clustering ARI collapses to $0.206$.
  - The adaptive rule $L^*(K) = \max(40, \lceil 3K \ln K \rceil)$ is required to guarantee minority cluster coverage ($>93.3\%$) and restore ARI to $0.355$.

---

## 5. CLASSICAL BENCHMARK DEFICITS (EXPERIMENT 5)

When evaluated on standard, non-genomic tabular datasets from the UCI and Scikit-Learn repositories, ICC-v2 consistently underperforms simpler, classical baselines:

### 5.1 Dataset-by-Dataset Deficits (5 Seeds Each)
1. **Wine ($N=178, D=13, K=3$)**:
   - GMM (Diag): **ARI = $0.9150 \pm 0.048$**
   - K-Means++: **ARI = $0.8974 \pm 0.041$**
   - Dense Consensus: **ARI = $0.8913 \pm 0.045$**
   - Spectral Clustering: **ARI = $0.8797 \pm 0.047$**
   - **ICC-v2**: **ARI = $0.6740 \pm 0.054$** ($-0.241$ deficit vs GMM, 0 Wins / 0 Ties / 5 Losses, $p = 1.000$)
2. **Breast Cancer ($N=569, D=30, K=2$)**:
   - Spectral Clustering: **ARI = $0.7607 \pm 0.000$**
   - Landmark Spectral (LSC): **ARI = $0.7061 \pm 0.088$**
   - Deep DEC: **ARI = $0.6894 \pm 0.104$**
   - K-Means++: **ARI = $0.6635 \pm 0.000$**
   - **ICC-v2**: **ARI = $0.1970 \pm 0.125$** ($-0.564$ deficit vs Spectral, 0 Wins / 0 Ties / 5 Losses, $p = 1.000$)
3. **Digits ($N=1797, D=64, K=10$)**:
   - Spectral Clustering: **ARI = $0.7071 \pm 0.000$**
   - Agglomerative (Ward): **ARI = $0.6644 \pm 0.000$**
   - Deep DEC: **ARI = $0.6621 \pm 0.024$**
   - Dense Consensus: **ARI = $0.5562 \pm 0.021$**
   - **ICC-v2**: **ARI = $0.4590 \pm 0.028$** ($-0.248$ deficit vs Spectral, 0 Wins / 0 Ties / 5 Losses, $p = 1.000$)

### 5.2 Overall Hypothesis Testing Across All 50 Benchmark Runs
Evaluating $H_1: \text{ARI}_{\text{ICC-v2}} > \text{ARI}_{\text{Baseline}}$ via paired Wilcoxon signed-rank tests across all 50 matched (dataset, seed) pairs:

| Baseline | ICC Mean ARI | Base Mean ARI | Mean Gain | Wilcoxon $W$ | Raw $p$-value | FDR $q$-value | Cohen's $d_z$ | Win/Tie/Loss | Conclusion |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Spectral Clustering** | $0.4343$ | $\mathbf{0.5984}$ | $-0.1641$ | $345.0$ | $0.9961$ | $0.9961$ | $-0.375$ | $13 / 4 / 33$ | **Significantly Inferior** |
| **GMM (Diag)** | $0.4343$ | $0.4393$ | $-0.0050$ | $510.0$ | $0.7163$ | $0.9758$ | $-0.017$ | $17 / 12 / 21$ | Not Significant |
| **Dense Consensus** | $0.4343$ | $0.4259$ | $+0.0085$ | $392.0$ | $0.7715$ | $0.9758$ | $+0.029$ | $13 / 14 / 23$ | Not Significant |
| **K-Means++** | $0.4343$ | $0.4297$ | $+0.0046$ | $408.0$ | $0.7067$ | $0.9758$ | $+0.016$ | $14 / 14 / 22$ | Not Significant |
| **DEC (Deep)** | $0.4343$ | $0.4222$ | $+0.0121$ | $536.0$ | $0.7033$ | $0.9758$ | $+0.039$ | $18 / 9 / 23$ | Not Significant |
| **Agglomerative (Ward)**| $0.4343$ | $0.4270$ | $+0.0073$ | $514.0$ | $0.8364$ | $0.9758$ | $+0.026$ | $16 / 7 / 27$ | Not Significant |
| **Landmark Spectral** | $0.4343$ | $0.4314$ | $+0.0030$ | $517.0$ | $0.6908$ | $0.9758$ | $+0.010$ | $19 / 7 / 24$ | Not Significant |

**Formal Finding**: After Benjamini-Hochberg FDR correction across all baselines, ICC-v2 demonstrates **no statistically significant overall superiority** over any baseline ($q \ge 0.9758$ across all 7 tests). Claims of general superiority across benchmark clustering tasks are refuted.

---

## 6. ACTIONABLE REMEDIATION MATRIX FOR MANUSCRIPT REVISION

| Manuscript Section | Original Claim | Identified Empirical Reality | Required Remediation in Revision |
| :--- | :--- | :--- | :--- |
| **Abstract & Intro** | "ICC-v2 provides universally superior clustering accuracy across diverse domains." | Defeated on Wine, Breast Cancer, Digits, Circles, Moons, XOR ($q > 0.97$). | Restrict primary claim: "ICC-v2 provides significant advantages specifically in high-dimensional multiclass genomic settings ($D \gg N$)." |
| **Section 3.1 (BGSS)** | "BGSS reliably screens all uninformative features prior to ensembling." | Blind to non-marginal interactions (XOR, Parity, covariance differences); fails on $D \ge 500$ noise fluctuations. | Formally document BGSS structural assumptions: assumes marginal unimodal/bimodal separability; state failure boundaries for parity/interaction signals. |
| **Section 3.4 (CICC)** | "CICC provides finite-sample distribution-free validity for biological clustering." | Stability-Accuracy Discordance causes $34.5\%$ to $64.8\%$ coverage deficits relative to ground truth; collapses under shift. | Clarify that CICC validity holds *strictly with respect to consensus pseudo-labels*, not latent biological ground truth. Add disclaimer prohibiting diagnostic reliance without external validation. |
| **Section 3.3 (Anchors)**| "Fixed $L=40$ is universally optimal for all consensus graphs." | Breaks down at $K \ge 12$ under class imbalance ($\pi_{\min}=0.02$); omits minority clusters in $>86\%$ of runs. | Replace fixed $L=40$ with the Adaptive Coupon-Collector rule: $L^*(K) = \max(40, \lceil 3K \ln K \rceil)$. |
| **Section 4.4 (Inference)**| "Centroid inductive projection preserves spectral cluster geometry." | Collapses on non-convex manifolds (ARI $\approx 0.0$ on Circles); transductive fidelity is only $64.7\%$ on complex data. | Explicitly bound inductive inference guarantees to convex clusters or recommend kernel out-of-sample extension for manifolds. |
| **Section 4.5 (Scaling)** | "Achieves 99.73% total memory reduction." | 99.73% applies to consensus matrix storage ($1.14\text{ GB} \to 3.08\text{ MB}$); total process RAM savings is 90.2%. | Report both metrics explicitly: distinguish consensus graph matrix storage from total peak process RSS. |

---
**Verification**: All empirical failures and boundary breakdowns cataloged in this document are reproducible via the configuration files in `results/loop2/configs/` and scripts in `results/loop2/scripts/`. Raw data is archived in `results/loop2/raw/`.
