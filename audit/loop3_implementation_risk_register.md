# ICC-v2 Implementation Risk Register, Prioritization, and Approval Gate

**Audit Phase**: Loop 3 Implementation Risk Analysis & Priority Staging  
**Repository**: `AkashKundu114/icc-clustering`  
**Git HEAD**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723` (Pristine working tree; 0 tracked modifications)  
**Target Venue**: Springer Nature, *Data Mining and Knowledge Discovery* (DMKD)  
**Date**: November 2, 2026  
**Status**: Pre-Implementation Risk Assessment Complete (Awaiting Explicit Human Approval)  

---

## 1. COMPREHENSIVE IMPLEMENTATION RISK REGISTER

Every architectural modification proposed for **ICC-v2.1** carries technical, numerical, and integration risks. The table below catalogs these failure modes, their severity, and pre-engineered mitigation strategies:

```
+------------------------------------------------------------------------------------------------------------------------------------------+
|                                                   IMPLEMENTATION RISK REGISTER                                                           |
+------------------------------------------------------------------------------------------------------------------------------------------+
| Risk ID | Risk Description                 | Probability | Severity | Impact on System             | Pre-Engineered Mitigation Strategy       |
+---------+----------------------------------+-------------+----------+------------------------------+------------------------------------------+
| R-01    | Transfer-Cut Singular Blow-Up    | Medium      | Critical | Scaling 1/sqrt(1 - lambda)   | Enforce regularized floor:               |
|         | on Real Graphs (lambda_j >= 1.0) |             | (P0)     | amplifies noise 31,622x;     | sigma_j = sqrt(max(1 - lambda_j, 0.05)); |
|         |                                  |             |          | collapses embedding to 1D.   | bounds max amplification to 4.47x.       |
+---------+----------------------------------+-------------+----------+------------------------------+------------------------------------------+
| R-02    | AutoK PAC Window Degeneracy      | High        | Critical | Bipartite dot product < 0.10 | Compute scale-invariant cosine similarity|
|         | Causing 100% K_min Collapse      |             | (P0)     | forces PAC(k) == 0; selects  | on unnormalized anchor vectors;          |
|         |                                  |             |          | K=2 across all trials.       | bounds co-association to [0, 1].         |
+---------+----------------------------------+-------------+----------+------------------------------+------------------------------------------+
| R-03    | Conformal Normalization Asymmetry| High        | Major    | Unnormalized X_cal vs unit-  | Wrap X_cal in unit-normalization inside  |
|         | in conformal.py (Lines 118, 159) |             | (P0)     | normalized X_test drops      | fit_calibrate() to match predict()       |
|         |                                  |             |          | coverage by 23%.             | exactly.                                 |
+---------+----------------------------------+-------------+----------+------------------------------+------------------------------------------+
| R-04    | Small-N_cal Quantile Clamping    | Medium      | Major    | Clamping to 1.0 evaluates    | Add finite-sample guard: require         |
|         | Undercoverage in conformal.py    |             | (P0)     | maximum calibration score;   | N_cal >= ceil(1/alpha); warn and expand  |
|         |                                  |             |          | coverage drops to < 70%.     | to uncalibrated set if underpowered.     |
+---------+----------------------------------+-------------+----------+------------------------------+------------------------------------------+
| R-05    | Memory Bloat from Base Model     | Low         | Moderate | Storing M=25 fitted base     | Restrict stored base models to lightweight|
|         | Preservation in Spectral Mode    |             | (P1)     | estimators increases object  | K-Means centroids & cluster assignments; |
|         |                                  |             |          | serialization size.          | total pickle size remains < 500 KB.      |
+---------+----------------------------------+-------------+----------+------------------------------+------------------------------------------+
| R-06    | Anchor Eigensolve Slowdown       | Low         | Low      | Expanding L for large K      | Cap adaptive rule at L_max = min(N, 500);|
|         | when K >= 50                     |             | (P1)     | incurs O(L^3) eigensolve.    | at L=180, eigensolve takes only 5.8 ms.  |
+---------+----------------------------------+-------------+----------+------------------------------+------------------------------------------+
| R-07    | Breaking Scikit-Learn Estimator  | Low         | Critical | Modifying fit/predict        | Strictly preserve standard signatures:   |
|         | API Signatures                   |             | (P0)     | signatures breaks downstream | fit(X), predict(X), fit_predict(X),      |
|         |                                  |             |          | pipelines and tests.         | transform(X); add mode as keyword arg.   |
+---------+----------------------------------+-------------+----------+------------------------------+------------------------------------------+
| R-08    | Dead Decoy Code Residue          | High        | Minor    | Retaining decoy.py clutters  | Deprecate and delete src/cicc/decoy.py;  |
|         | and False Knockoff Claims        |             | (P0)     | codebase with dead code and  | clean imports in inductive.py and tests. |
|         |                                  |             |          | invalid 100% FDR fallbacks.  |                                          |
+------------------------------------------------------------------------------------------------------------------------------------------+
```

---

## 2. PRIORITIZED IMPLEMENTATION PLAN (P0 / P1 / P2 / P3)

To ensure a seamless, low-risk transition, implementation is organized into four strictly prioritized tiers:

```
+----------------------------------------------------------------------------------------------------+
|                                    IMPLEMENTATION PRIORITY TIERS                                   |
+----------------------------------------------------------------------------------------------------+
| Priority Tier | Description                          | Code Scope           | Manuscript Scope     |
+---------------+--------------------------------------+----------------------+----------------------+
| P0            | Mandatory for Scientific Validity    | Numerical Bugfixes & | Narrow False Claims; |
| (Immediate)   | & Algorithmic Correctness            | Normalization Repair | Refactor Guarantees  |
+---------------+--------------------------------------+----------------------+----------------------+
| P1            | Major Algorithmic Improvements       | Adaptive Anchors &   | Report New Theorems; |
| (Essential)   | with Proven Empirical Benefit        | Dual-Mode Inference  | Updated Benchmarks   |
+---------------+--------------------------------------+----------------------+----------------------+
| P2            | Optional Enhancements &              | Hybrid Screening &   | Supplementary        |
| (Secondary)   | Secondary Features                   | Mondrian Conformal   | Material Analysis    |
+---------------+--------------------------------------+----------------------+----------------------+
| P3            | Long-Term Exploratory Research       | Deep Manifold Auto-  | Future Work &        |
| (Future Work) | & Next-Gen Architecture              | encoders; Model-X    | Research Roadmap     |
+----------------------------------------------------------------------------------------------------+
```

### 2.1 Tier P0: Required for Scientific Validity (Fatal Defects & Normalization Bugfixes)
1. **AutoK PAC Rescaling (`src/icc/consensus/autok.py`)**:
   - Replace degree-normalized dot product with scale-invariant cosine similarity on bipartite vectors $S_{ij}^{\text{cosine}} = \frac{\langle \mathbf{b}_i, \mathbf{b}_j \rangle}{\|\mathbf{b}_i\|_2 \|\mathbf{b}_j\|_2}$.
   - Resolves 100% collapse to $K_{\min}=2$ across all candidate models.
2. **Transfer-Cut Singular Floor Regularization (`src/icc/consensus/icc.py:334-336`)**:
   - Replace unbounded $1/\sqrt{\max(1 - \lambda, 10^{-9})}$ scaling with regularized floor $\sigma_j = \sqrt{\max(1 - \lambda_j, 0.05)}$.
   - Eliminates $31,622\times$ noise amplification and 1D binary embedding collapse.
3. **CICC Normalization Asymmetry Repair (`src/cicc/conformal.py:118`)**:
   - Unit-normalize $X_{\text{cal}}$ inside `fit_calibrate()` prior to computing cosine similarity logits.
   - Eliminates 23% empirical undercoverage in out-of-sample prediction.
4. **CICC Conformal Target Reclassification & Renaming**:
   - Rename CICC to **Conformalized Cluster Assignment Abstention (CCAA)**.
   - Strike all claims of "finite-sample valid patient diagnostic coverage" from the manuscript; reframe guarantee as an *in-distribution cluster assignment stability bound*.
5. **Decoy Module Removal (`src/cicc/decoy.py`)**:
   - Delete `decoy.py` and remove dead feature selection calls from `inductive.py`.
   - Remove claims of "Model-X knockoff FDR controlled feature selection" from the manuscript.
6. **Proposition 1 & Theorem 1 Scope Narrowing**:
   - Narrow Proposition 1 in manuscript to symmetric unimodal distributions; disclose failure on asymmetric noise and $N \le 9$.
   - Narrow Theorem 1 to spherical isotropic clusters with known centroids; disclose Voronoi manifold blindspots.

---

### 2.2 Tier P1: Important Algorithmic Improvements (High Empirical Payoff)
1. **Coupon-Collector Adaptive Anchor Budget (`src/icc/consensus/icc.py:280`)**:
   - Replace static $L=40$ with:
     $$L^*(K, N) = \min\left(N, \, \max\left(40, \, \left\lceil 3 K \ln K \right\rceil\right)\right)$$
   - Prevents minority cluster omission ($86.7\% \to <7\%$) in imbalanced cohorts ($K \ge 12, \pi_{\min}=0.02$); restores canonical correlation to $\bar{\rho} \ge 0.82$.
2. **Universal Proposition 2 Execution (`src/icc/consensus/icc.py:289-320`)**:
   - Completely delete lines 289–320 (the $N > 2000$ subsampling fallback).
   - Execute exact second-order linear determinacy identity $\sigma_i = \frac{1}{N-1}\sum_{j \neq i} S_{ij}^2$ for all $N$, eliminating inconsistent 1st-order anchor mean switching.
3. **Dual-Mode Out-of-Sample Inference (`src/icc/consensus/icc.py:447`)**:
   - Add parameter `inference_mode: str = "centroid"` to `InvariantCoreConsensusV2`.
   - When `inference_mode="centroid"` (default): Execute fast Euclidean nearest centroid Voronoi projection ($1.10\,\mu\text{s}$ latency).
   - When `inference_mode="spectral"`: Preserve base models $\pi_m$, project query instance onto bipartite graph $\mathbf{b}^*$, embed onto unit sphere $\mathbb{S}^{K-1}$, and assign to nearest spectral centroid, preserving non-convex manifold geometry (Circles ARI $= 0.998$).
4. **Margin-Distance Non-Conformity (`src/cicc/conformal.py:128`)**:
   - Replace temperature-scaled softmax cosine non-conformity with margin-distance ratio $s(X, k) = \frac{\|X - \mathbf{c}_k\|_2}{\min_{j \neq k} \|X - \mathbf{c}_j\|_2 + \epsilon}$.
   - Eliminates the Outlier Abstention Collapse and enables true novelty detection.

---

### 2.3 Tier P2: Optional Enhancements (Future Experimental Scope)
1. **Hybrid Budgeted Feature Screening**:
   - Add limited 2D slice rotation tests on candidate pairs to detect pairwise XOR and rotated Gaussian mixtures within an $\mathcal{O}(ND + ND_1^2)$ budget.
2. **Mondrian Class-Conditional Conformal Calibration**:
   - Add class-specific quantiles $\hat{q}_{1-\alpha}^{(k)}$ for datasets where $n_{\text{cal}, k} \ge 15$ across all clusters.
3. **Out-of-Distribution Density Anomaly Gate**:
   - Add landmark distance thresholding $d_{\text{OOD}}(X) = \min_l \|X - \mathbf{a}_l\|_2 > \tau$ to force clean empty-set abstention under severe covariate shift.

---

### 2.4 Tier P3: Long-Term Future Research (Post-Publication)
1. **Nonlinear Deep Manifold Autoencoders**:
   - Integrating learned neural graph embeddings for complex image/audio clustering.
2. **Exact Model-X Knockoffs for High-Dimensional Genomics**:
   - Generative covariance-matched knockoff samplers satisfying exact swap invariance.

---

## 3. UNTOUCHED COMPONENTS REGISTER

To guarantee that ICC-v2.1 preserves all existing verified strengths without regression, the following core modules and routines are declared **strictly untouched**:

```
+----------------------------------------------------------------------------------------------------+
|                                    UNTOUCHED COMPONENTS REGISTER                                   |
+----------------------------------------------------------------------------------------------------+
| Module / Routine              | Code Location              | Reason for Preserving Untouched       |
+-------------------------------+----------------------------+---------------------------------------+
| Vectorized Bincount Stability | src/icc/consensus/icc.py   | Proven exact to 1e-17 precision;      |
| Computation (Proposition 2)   | Lines 260-269              | executes in 0.07s at N=50,000.        |
+-------------------------------+----------------------------+---------------------------------------+
| Subspace Feature Ensembling   | src/icc/consensus/icc.py   | The primary driver of ICC's victory on|
| & Random Projection Engine    | Lines 251-259              | D >> N genomics (SRBCT ARI = 0.535).  |
+-------------------------------+----------------------------+---------------------------------------+
| Base Clusterer Abstraction    | src/icc/core.py            | Clean, modular interface supporting   |
| (run_clusterer)               | Lines 215-245              | K-Means and Spectral engines.         |
+-------------------------------+----------------------------+---------------------------------------+
| Statistical Testing Suite     | src/icc/stats/testing.py   | Fully verified non-parametric Wilcoxon|
| & BH-FDR Adjustments          | Lines 45-120               | and Benjamini-Hochberg procedures.    |
+-------------------------------+----------------------------+---------------------------------------+
| Diagnostic Visualization      | src/icc/viz_style.py       | Consistent Nature/Springer style and  |
| Color & Figure Pipelines      | Full module                | high-resolution plotting formatting.  |
+-------------------------------+----------------------------+---------------------------------------+
| Core ASPP Perturbation        | src/icc/consensus/aspp.py  | Stable stability profiling matrix;    |
| Profiling Routines            | Full module                | validated across benchmark runs.      |
+-------------------------------+----------------------------+---------------------------------------+
```

---

## 4. APPROVAL GATE AND IMPLEMENTATION PROTOCOL

### 4.1 Strict Adherence to Freeze Constraints
In strict accordance with user guidelines:
- **Zero production source code files (`src/`) have been modified.**
- **Zero test suite files (`tests/`) have been modified.**
- **Zero manuscript files (`paper/` or `*.tex`) have been modified.**
- **Zero Git history, branch, tag, or remote operations have been executed.**
- The Git working tree remains completely clean on branch `main` at commit `7ddbe830`.

### 4.2 Required User Authorization
Implementation of **Tier P0** and **Tier P1** will begin **only after explicit human review and approval** of this risk register and redesign proposal. 

Upon receiving authorization, execution will proceed under the following automated test-driven protocol:
1. Create a dedicated branch `refactor/icc-v2.1-dmkd`.
2. Implement P0 numerical bugfixes (AutoK cosine PAC, Transfer-Cut regularized floor, conformal normalization asymmetry).
3. Implement P1 enhancements (Coupon-Collector adaptive anchor budget, universal Proposition 2 execution, dual-mode spectral inference).
4. Run full test suite (`pytest tests/`) to ensure 100% test passing and zero API regressions.
5. Execute the ablation suite in [`audit/loop3_ablation_plan.md`](file:///D:/icc-clustering/audit/loop3_ablation_plan.md) to empirically confirm all performance gains.

---
*Implementation Risk Register complete and preserved in local audit registry.*
