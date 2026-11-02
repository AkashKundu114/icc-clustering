# ICC-v2 Experimental Ablation and Empirical Validation Plan

**Audit Phase**: Loop 3 Empirical Validation Protocol  
**Repository**: `AkashKundu114/icc-clustering`  
**Git HEAD**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723` (Clean working tree; 0 tracked modifications)  
**Target Venue**: Springer Nature, *Data Mining and Knowledge Discovery* (DMKD)  
**Date**: November 2, 2026  
**Status**: Formal Experimental Ablation Protocol Ready for Execution Upon Human Approval  

---

## 1. PURPOSE AND SCIENTIFIC RATIONALE

This ablation protocol defines the rigorous experimental framework required to validate every architectural change proposed for **ICC-v2.1** prior to merging into production code. 

To prevent confirmation bias and p-hacking, every ablation:
1. **Pre-registers explicit null and alternative hypotheses**.
2. **Fixes random seed schedules** across 5 independent seeds: `[42, 137, 2024, 7, 999]`.
3. **Specifies decision thresholds** using paired Wilcoxon signed-rank tests with Benjamini-Hochberg False Discovery Rate (FDR) correction at $\alpha = 0.05$.
4. **Isolates single-component variations** while holding all other algorithmic parameters constant.

---

## 2. ABLATION TRACK 1: FEATURE SCREENING & BGSS MECHANISMS

### 2.1 Hypotheses
- $H_{1, 1}$: Calibrated Marginal BGSS (Candidate A1) matches or exceeds Legacy BGSS ARI on $D \gg N$ genomics while eliminating false feature rejection in small cohorts ($N \le 9$).
- $H_{1, 2}$: Univariate BGSS (both modes) fails to achieve $\text{ARI} > 0.05$ on continuous XOR, 3-way parity, and distinct covariance structures.
- $H_{1, 3}$: Hybrid Budgeted Screening (Candidate A6) recovers $\text{ARI} \ge 0.80$ on continuous XOR and diagonal mixtures with less than $200\text{ ms}$ runtime overhead.

### 2.2 Controlled Experimental Suite
| Benchmark Cohort | Sample Size $N$ | Total Features $D$ | Informative $D^*$ | Signal Geometry | Ground Truth $K$ |
| :--- | :---: | :---: | :---: | :--- | :---: |
| **Small-Sample Pilot** | $8$ | $500$ | $10$ | Bimodal Gaussian | $2$ |
| **Continuous XOR** | $600$ | $20$ | $2$ | Sign quadrant interaction | $2$ |
| **Diagonal GMM** | $600$ | $20$ | $2$ | $\Delta = 1.60\sigma$ ($45^\circ$ rotation) | $2$ |
| **Distinct Covariance** | $600$ | $20$ | $2$ | $\rho_1 = +0.9, \rho_2 = -0.9$ | $2$ |
| **High-D Noise** | $300$ | $1,000$ | $10$ | Marginally separated + 990 noise | $3$ |
| **SRBCT (Genomics)** | $83$ | $2,308$ | Unknown | Real multiclass biopsy microarrays | $4$ |
| **Leukemia (Genomics)** | $72$ | $7,129$ | Unknown | Real ALL/AML gene expression | $2$ |

### 2.3 Compared Screening Variants
1. `Variant 1A`: No Feature Screening (`subspace_rate=0.30` on full ambient space $D$).
2. `Variant 1B`: Legacy BGSS (`pool_mode="legacy"`, top 15% rank selection).
3. `Variant 1C`: Null-Calibrated BGSS (`pool_mode="null_calibrated"`, $BC \ge 5/9$ threshold).
4. `Variant 1D`: Calibrated Two-Tier BGSS (Candidate A1, sample-size-conditioned threshold).
5. `Variant 1E`: Hybrid Budgeted Screening (Candidate A6, 2D slice rotation tests).

### 2.4 Metrics & Success Criteria
- Primary Metric: Clustering ARI, NMI, and AMI.
- Feature Selection Metrics: Precision, Recall, and F1-score on synthetic benchmarks with known ground-truth $D^*$.
- Runtime & Peak Memory: Milliseconds per screening pass.
- Success Criterion: Candidate A1 must achieve statistically equivalent ARI to Legacy BGSS on SRBCT/Leukemia ($p > 0.10$) while improving recall on $N \le 9$ pilot data.

---

## 3. ABLATION TRACK 2: CICC CONFORMAL CALIBRATION & NON-CONFORMITY

### 3.1 Hypotheses
- $H_{2, 1}$: Replacing cosine softmax with margin-distance non-conformity eliminates the Outlier Abstention Collapse, restoring clean non-zero abstention rates for out-of-distribution outliers.
- $H_{2, 2}$: Unit-normalizing $X_{\text{cal}}$ to match $X_{\text{test}}$ eliminates the $23\%$ undercoverage gap in `conformal.py`.
- $H_{2, 3}$: The empirical coverage of CCAA prediction sets holds at $\ge 1 - \alpha$ relative to transductive consensus labels, while explicitly failing to guarantee biological ground truth.

### 3.2 Compared Calibration Variants
1. `Variant 2A`: Audited Baseline CICC (Unnormalized $X_{\text{cal}}$, cosine softmax non-conformity, pseudo-label target).
2. `Variant 2B`: Normalized Softmax (Unit-normalized $X_{\text{cal}}$, cosine softmax, pseudo-label target).
3. `Variant 2C`: Normalized Margin-Distance CCAA (Unit-normalized $X_{\text{cal}}$, Euclidean margin-ratio score, pseudo-label target).
4. `Variant 2D`: Supervised Ground-Truth Calibration (Calibrated directly on external biological ground-truth labels).
5. `Variant 2E`: Mondrian Class-Conditional CCAA (Cluster-specific quantiles $\hat{q}_{1-\alpha}^{(k)}$).

### 3.3 Evaluation Protocol
- **Datasets**: Synthetic Gaussian ($N=600, K=3$), Leukemia ($N=72, K=2$), SRBCT ($N=83, K=4$).
- **Distribution Shift Sweep**: Covariate shift $\delta \in [0.0, 0.5, 1.0, 1.5, 2.0]$.
- **Calibration Split Sizes**: $n_{\text{cal}} \in [5, 10, 20, 40, 80]$.
- **Measured Metrics**:
  - Pseudo-label coverage: $\mathbb{P}(\hat{Y}_{\text{test}} \in \mathcal{C}(X_{\text{test}}))$.
  - Ground-truth coverage: $\mathbb{P}(Y_{\text{test}}^* \in \mathcal{C}(X_{\text{test}}))$.
  - Average prediction set efficiency: $\mathbb{E}[|\mathcal{C}(X)|]$.
  - Empty-set abstention rate: $\mathbb{P}(\mathcal{C}(X) = \emptyset)$.
  - Universal trivial set rate: $\mathbb{P}(|\mathcal{C}(X)| = K)$.
- **Success Criterion**: Margin-distance CCAA must satisfy empirical pseudo-label coverage $\ge 90\%$ at $\alpha=0.10$ for all $n_{\text{cal}} \ge 15$, exhibit non-zero abstention on outliers, and clearly disclose the ground-truth coverage deficit.

---

## 4. ABLATION TRACK 3: INDUCTIVE INFERENCE OPERATORS

### 4.1 Hypotheses
- $H_{3, 1}$: Native Transfer-Cut Spectral Extension (Option 2) achieves $\text{ARI} \ge 0.95$ on Concentric Circles and Two Moons, resolving the manifold collapse of centroid projection ($\text{ARI} \le 0.00$).
- $H_{3, 2}$: Native Spectral Extension achieves $\ge 98\%$ transductive fidelity on training points across all 10 benchmarks.
- $H_{3, 3}$: Stability-weighted centroid projection maintains an order-of-magnitude faster inference latency ($\le 2.0\,\mu\text{s}$ vs $\ge 50\,\mu\text{s}$).

### 4.2 Compared Inductive Variants
1. `Variant 3A`: Current Euclidean Nearest Centroid Voronoi in $\mathbb{R}^D$ (`inference_mode="centroid"`).
2. `Variant 3B`: Native Transfer-Cut Spectral Extension (`inference_mode="spectral"`).
3. `Variant 3C`: Landmark RBF Kernel Out-of-Sample Projection.
4. `Variant 3D`: 5-Nearest Neighbor Assignment on Certified Anchor Points.

### 4.3 Evaluation Benchmarks
- Non-Convex Manifolds: Concentric Circles ($N=500$), Two Moons ($N=500$).
- Standard Benchmarks: Iris ($N=150$), Wine ($N=178$), Breast Cancer ($N=569$), Digits ($N=1797$).
- Genomics: Leukemia ($N=72$), SRBCT ($N=83$).
- Metrics: Out-of-sample ARI, Transductive Fidelity ($\%$ match with `labels_` on training instances), Query Latency ($\mu\text{s}$ per instance), Pickled Model Storage Size (KB).
- Success Criterion: Dual-mode architecture enables user to choose between $1.10\,\mu\text{s}$ streaming centroid inference and $100\%$ manifold-preserving spectral inference.

---

## 5. ABLATION TRACK 4: ADAPTIVE ANCHOR BUDGETING & SPECTRAL FIXES

### 5.1 Hypotheses
- $H_{4, 1}$: The Coupon-Collector Adaptive Rule $L^*(K) = \min(N, \max(40, \lceil 3K \ln K \rceil))$ achieves $>90\%$ minority cluster coverage on imbalanced cohorts ($K=20, \pi_{\min}=0.02$), outperforming fixed $L=40$.
- $H_{4, 2}$: Regularizing Transfer-Cut singular values with $\sigma_j = \sqrt{\max(1 - \lambda_j, 0.05)}$ eliminates embedding collapse without degrading ARI on clean data.
- $H_{4, 3}$: Eliminating lines 289–320 and running Proposition 2 universally for all $N$ reduces total runtime and memory for $N > 2000$.

### 5.2 Controlled Parameter Grids
- Cluster counts: $K \in [2, 3, 5, 8, 12, 16, 20]$.
- Cluster proportions: Balanced ($\pi_k = 1/K$) vs Imbalanced ($\pi_{\min} \in [0.01, 0.02, 0.05]$).
- Compared Budget Rules:
  1. Under-Budget: $L = \max(2, K - 2)$
  2. Equal-Budget: $L = K$
  3. Static Default: Fixed $L = 40$
  4. Adaptive Coupon Rule: $L^*(K) = \min(N, \max(40, \lceil 3K \ln K \rceil))$
  5. Substantial: $L = 10K$
- Measured Metrics: Minority cluster coverage rate ($\%$ of runs where $|\mathcal{A} \cap \mathcal{C}_{\min}| \ge 1$), Canonical correlation with dense consensus $\bar{\rho}$, Grassmann subspace distance, Consensus clustering ARI, Laplacian eigensolve runtime (ms).

---

## 6. ABLATION TRACK 5: AUTOK MODEL ORDER PAC NORMALIZATION REPAIR

### 6.1 Hypotheses
- $H_{5, 1}$: Rescaling PAC to cosine similarity on anchor vectors $S_{ij}^{\text{cosine}} = \frac{\langle \mathbf{b}_i, \mathbf{b}_j \rangle}{\|\mathbf{b}_i\|_2 \|\mathbf{b}_j\|_2}$ resolves the 100% $K_{\min}$ collapse, correctly identifying true $K^*$ on synthetic clusters with ground-truth $K \in \{3, 4, 5, 6\}$.

### 6.2 Compared AutoK Variants
1. `Variant 5A`: Current Audited AutoK (Degree-normalized inner product on $[0.10, 0.90]$).
2. `Variant 5B`: Rescaled Ambiguity Window on Degree-Normalized Vectors ($[u_1, u_2] = [0.2 K/L, 0.8 K/L]$).
3. `Variant 5C`: Cosine Similarity PAC (Unnormalized anchor vectors, standard $[0.10, 0.90]$ window).
4. `Variant 5D`: Classical Monti Dense Consensus PAC (Ground-truth reference on $N \times N$ matrix).

### 6.3 Evaluation Cohorts
- Synthetic Gaussian cohorts with ground truth $K^* \in \{2, 3, 4, 5, 6\}$ (10 independent runs per $K^*$).
- Real genomic datasets: SRBCT (True $K^* = 4$), Leukemia (True $K^* = 2$), Iris (True $K^* = 3$), Wine (True $K^* = 3$).
- Metrics: Discovered $\hat{K}$, Absolute error $|\hat{K} - K^*|$, Exact recovery rate $\mathbb{P}(\hat{K} = K^*)$, PAC ambiguity curve trajectory.
- Success Criterion: Variant 5C must recover true $K^*$ in $\ge 80\%$ of synthetic trials, ending the 100% $K_{\min}$ collapse.

---

## 7. STATISTICAL VALIDATION & REPRODUCIBILITY PROTOCOL

Every ablation experiment will be recorded in a dedicated CSV manifest in `results/loop3/raw/` accompanied by an automated verification script. 

### Statistical Criteria for Adoption:
1. **Paired Wilcoxon Signed-Rank Test**:
   - One-tailed test evaluating $H_1: \text{Metric}(\text{New}) > \text{Metric}(\text{Baseline})$.
   - Minimum sample size: $n = 50$ matched pairs (10 datasets $\times$ 5 seeds).
2. **False Discovery Rate (FDR) Control**:
   - Benjamini-Hochberg adjustment applied across all simultaneous comparisons:
     $$q_i \le 0.05$$
3. **Effect Size (Cohen's $d_z$)**:
   - Component improvements must demonstrate at least a moderate effect size ($|d_z| \ge 0.50$) or eliminate a proven structural defect (e.g. 100% AutoK collapse).

---
*Ablation Plan completed and preserved in local audit registry.*
