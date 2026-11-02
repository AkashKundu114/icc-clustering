# ICC-v2 Architecture Options, Decision Matrix, and Versioning Roadmap

**Audit Phase**: Loop 3 Algorithmic Redesign Research  
**Repository**: `AkashKundu114/icc-clustering`  
**Git HEAD**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723` (Clean working tree; 0 tracked modifications)  
**Target Venue**: Springer Nature, *Data Mining and Knowledge Discovery* (DMKD)  
**Date**: November 2, 2026  
**Status**: Architecture Selection Complete (Awaiting Explicit Human Approval Before Code Edits)  

---

## 1. COMPREHENSIVE ARCHITECTURAL DECISION MATRIX

Every candidate component proposed across Tracks A through E is evaluated below against 9 objective criteria. Proposals are ranked by **scientific validity, mathematical correctness, and computational feasibility**, rather than artificial novelty.

```
+------------------------------------------------------------------------------------------------------------------------------------------+
|                                                   ARCHITECTURAL DECISION MATRIX                                                          |
+------------------------------------------------------------------------------------------------------------------------------------------+
| # | Component Proposal       | Scientific Motivation         | Expected Impact           | Complexity Cost | New Hyperparams | Overfit Risk | Decision / Recommendation |
+---+--------------------------+-------------------------------+---------------------------+-----------------+-----------------+--------------+---------------------------+
| 1 | Two-Tier Calibrated      | Sarle 5/9 fails for N<=9 and  | Restores feature gating   | O(ND) time      | None (uses      | Low          | ADOPT (P0 in ICC-v2.1)    |
|   | BGSS (Candidate A1)      | asymmetric unimodal noise     | in finite small samples   | O(D) space      | existing pool)  |              | Restrict claim in paper   |
+---+--------------------------+-------------------------------+---------------------------+-----------------+-----------------+--------------+---------------------------+
| 2 | Pairwise Interaction     | BGSS blind to XOR and         | Recovers 2D XOR and       | O(ND + ND_1^2)  | D_1 pool size   | Medium       | DEFER to ICC-v3.0 (P2)    |
|   | Screening (Candidate A3) | diagonal mixture signals      | rotated Gaussian clusters | +150 ms compute | slice angles    |              | Optional low-D mode       |
+---+--------------------------+-------------------------------+---------------------------+-----------------+-----------------+--------------+---------------------------+
| 3 | Joint Dependence dCor /  | Nonlinear copula feature      | Recovers complex joint    | O(N^2 D) time   | Kernel bandwidth| High         | REJECT                    |
|   | HSIC (Candidate A5)      | dependence capture            | non-marginal dependencies | Prohibitive OOM | distance metric |              | Violates linear scaling   |
+---+--------------------------+-------------------------------+---------------------------+-----------------+-----------------+--------------+---------------------------+
| 4 | Conformal In-Dist Cluster| Fatal Target Mismatch: CICC   | 100% mathematically honest| O(N_cal D) time | None            | Zero         | ADOPT (P0 in ICC-v2.1)    |
|   | Abstention CCAA (Mech B1)| calibrates to pseudo, not true| abstention guarantee      | O(N_cal) space  |                 |              | Rename CICC -> CCAA       |
+---+--------------------------+-------------------------------+---------------------------+-----------------+-----------------+--------------+---------------------------+
| 5 | Normalization Asymmetry  | Unnormalized X_cal vs unit-   | Eliminates 23% empirical  | O(N_cal D) time | None            | Zero         | ADOPT (P0 in ICC-v2.1)    |
|   | Bugfix in conformal.py   | normalized X_test drops cov.  | undercoverage in predict  | O(1) space      |                 |              | Immediate bugfix          |
+---+--------------------------+-------------------------------+---------------------------+-----------------+-----------------+--------------+---------------------------+
| 6 | Mondrian Class-Condition | Class imbalance causes rare   | Equalizes coverage across | O(N_cal D) time | Minimum cluster | Medium       | DEFER to ICC-v3.0 (P2)    |
|   | Conformal (Mech B3)      | cluster coverage starvation   | imbalanced subtypes       | O(K) quantiles  | calibration n   |              | Fails when n_cal_k < 5    |
+---+--------------------------+-------------------------------+---------------------------+-----------------+-----------------+--------------+---------------------------+
| 7 | Dual-Mode Inductive      | Centroid Voronoi projection   | Preserves manifold ARI    | O(M d_sub + LK) | inference_mode  | Low          | ADOPT (P1 in ICC-v2.1)    |
|   | Architecture (Track C)   | collapses on non-convex data  | (Circles: -0.003 -> 0.998)| per query sample| ("centroid" /   |              | Fast default + opt-in     |
|   |                          | but is ultra-fast (1.10 us)   | Transductive fid -> 98.9% | (+50 us latency)| "spectral")     |              | faithful spectral mode    |
+---+--------------------------+-------------------------------+---------------------------+-----------------+-----------------+--------------+---------------------------+
| 8 | Coupon-Collector Adaptive| Fixed L=40 omits minority     | Restores minority cluster | O(L^3) eigen    | None            | Zero         | ADOPT (P0 in ICC-v2.1)    |
|   | Budget L*(K) (Track D)   | clusters in 86.7% at K>=12    | coverage (>93%); rho>=0.82| (+5 ms compute) | (Analytical)    |              | Proven theorem            |
+---+--------------------------+-------------------------------+---------------------------+-----------------+-----------------+--------------+---------------------------+
| 9 | Universal Proposition 2  | N>2000 fallback switches      | Eliminates 25MB subsample | ZERO overhead   | None (deletes   | Zero         | ADOPT (P0 in ICC-v2.1)    |
|   | Execution (Track D)      | definition to 1st-order mean  | allocation; exact stab.   | (Faster 0.07s)  | lines 289-320)  |              | Proven exact 1e-17        |
+---+--------------------------+-------------------------------+---------------------------+-----------------+-----------------+--------------+---------------------------+
| 10| Transfer-Cut Regularized | 1/sqrt(max(1-lambda, 1e-9))   | Eliminates 31,622x noise  | O(LK) time      | Regularization  | Zero         | ADOPT (P0 in ICC-v2.1)    |
|   | Singular Floor (Track D) | causes singular blow-up       | amplification in embed    | O(1) space      | floor eps=0.05  |              | Numerically stable        |
+---+--------------------------+-------------------------------+---------------------------+-----------------+-----------------+--------------+---------------------------+
| 11| AutoK Cosine PAC Window  | Degree-normalized inner prod  | Resolves 100% K-min       | O(n_pairs L)    | None            | Zero         | ADOPT (P0 in ICC-v2.1)    |
|   | Rescaling (Track E)      | < 0.10 forces PAC(k) == 0     | collapse; accurate K*     | O(1) space      | (Standard cos)  |              | Proven normalization fix  |
+---+--------------------------+-------------------------------+---------------------------+-----------------+-----------------+--------------+---------------------------+
| 12| Delete Knockoff Decoy    | Independent noise violates    | Removes invalid 100% FDR  | Eliminates dead | None (deletes   | Zero         | ADOPT (P0 in ICC-v2.1)    |
|   | Dead Code (Track E)      | swap invariance; dead code    | fallback & unpassed code  | code in src/    | decoy module)   |              | Dead code removal         |
+------------------------------------------------------------------------------------------------------------------------------------------+
```

---

## 2. VERSIONED ARCHITECTURAL ROADMAP

We define three explicit, versioned architectural milestones. We reject premature major version bumps: changes that correct mathematical claims, repair numerical bugs, and establish reproducibility belong to **ICC-v2.1**, whereas substantive algorithmic restructuring belongs to **ICC-v3.0**.

```
                           +-----------------------------------------------+
                           |                   ICC-v2.0                    |
                           |          (Current Audited Baseline)           |
                           +-----------------------------------------------+
                                                  |
                                                  | Minimal Repairs & Honest Claims
                                                  | (Zero breaking changes to API)
                                                  v
                           +-----------------------------------------------+
                           |                   ICC-v2.1                    |
                           |      (Mathematically Sound DMKD Release)      |
                           +-----------------------------------------------+
                                                  |
                                                  | Substantive Architectural Redesign
                                                  | (Multi-stage screening, Mondrian)
                                                  v
                           +-----------------------------------------------+
                           |                   ICC-v3.0                    |
                           |        (Next-Generation Research Engine)      |
                           +-----------------------------------------------+
```

### 2.1 ICC-v2.0: Current Validated Architecture (Status Quo Baseline)
- **Role**: Serves as the historical baseline against which all improvements and ablations are benchmarked.
- **Components**:
  - Feature Screening: Univariate Sarle's Bimodality Coefficient with default `pool_mode="legacy"`.
  - Base Clustering: Subspace K-Means or Spectral clustering over random candidate subsets.
  - Stability Metric: Proposition 2 vectorized linear determinacy for $N \le 2000$; heuristic 1st-order anchor mean fallback for $N > 2000$.
  - Consensus Graph: Bipartite rectangular affinity $B \in \mathbb{R}^{N \times L}$ with fixed anchor budget $L=40$.
  - Spectral Embedding: Transfer-Cut Laplacian with unregularized $1/\sqrt{1 - \lambda}$ scaling.
  - Out-of-Sample Inference: Stability-weighted nearest-centroid Voronoi projection in feature space $\mathbb{R}^D$.
  - Calibration: Split conformal prediction with cosine softmax non-conformity against nearest-centroid pseudo-labels.
  - Model Order: AutoK PAC minimization over $[0.10, 0.90]$ ambiguity window.
- **Documented Limitations**:
  - Inapplicable to non-convex manifolds (Concentric Circles ARI $\approx 0.0$).
  - Inapplicable to non-marginal interactions (XOR, parity ARI $\approx 0.0$).
  - Conformal prediction bounds self-consistency, not biological truth.
  - AutoK PAC exhibits 100% $K_{\min}$ collapse.

---

### 2.2 ICC-v2.1: Minimal Corrective Redesign (Recommended for DMKD Submission)
- **Philosophy**: Fix all fatal P0 bugs, narrow all overclaimed theorems to their mathematically provable regimes, eliminate numerical singularities, and adopt evidence-proven improvements without breaking scikit-learn API compatibility.
- **Architectural Enhancements**:
  1. **Adaptive Anchor Budgeting**:
     $$L^*(K, N) = \min\left(N, \, \max\left(40, \, \left\lceil 3 K \ln K \right\rceil\right)\right)$$
     Replaces static $L=40$. Guarantees minority cluster coverage ($>93\%$) and well-conditioned eigengaps for all $K \ge 12$.
  2. **Universal Proposition 2 Execution**:
     Completely excise lines 289–320 of `icc.py`. Run exact second-order determinacy identity $\sigma_i = \frac{1}{N-1}\sum_{j \neq i} S_{ij}^2$ for all $N$, eliminating the inconsistent subsampling switch.
  3. **Transfer-Cut Numerical Regularization**:
     Enforce a regularized singular value floor $\sigma_j = \sqrt{\max(1 - \lambda_j, 0.05)}$, eliminating the $31,622\times$ noise explosion and embedding collapse.
  4. **Dual-Mode Out-of-Sample Inference**:
     Introduce `inference_mode="centroid"` (default, $1.10\,\mu\text{s}$ latency) and `inference_mode="spectral"` (opt-in, preserves base models, constructs query bipartite vector $\mathbf{b}^*$, projects to $\mathbb{S}^{K-1}$, eliminating manifold collapse).
  5. **AutoK PAC Rescaling**:
     Compute sample-pair co-association using cosine similarity on anchor vectors $S_{ij}^{\text{cosine}} = \frac{\langle \mathbf{b}_i, \mathbf{b}_j \rangle}{\|\mathbf{b}_i\|_2 \|\mathbf{b}_j\|_2}$, resolving the 100% $K_{\min}$ collapse and restoring authentic PAC order selection.
  6. **Conformal Renaming & Bugfixes**:
     Rename CICC to **Conformalized Cluster Assignment Abstention (CCAA)**. Fix calibration normalization asymmetry in `conformal.py` (ensure $X_{\text{cal}}$ is unit-normalized) and correct small-$N_{\text{cal}}$ clamping. Disclose that CCAA guarantees in-distribution cluster assignment stability, not patient diagnostic truth.
  7. **Decoy Module Deprecation**:
     Excise `src/cicc/decoy.py` and remove dead decoy calls from `inductive.py`.
  8. **Manuscript Claim Narrowing**:
     Restrict Proposition 1 to continuous symmetric unimodal noise; restrict Theorem 1 to spherical isotropic convex clusters with known centroids; report matrix vs process memory transparently.

---

### 2.3 ICC-v3.0: Substantive Research Redesign (Future Long-Term Architecture)
- **Philosophy**: Major architectural evolution introducing multi-stage interaction discovery, density-aware out-of-distribution detection, and class-conditional conformal guarantees.
- **Architectural Enhancements**:
  1. **Hybrid Budgeted Feature Screening**:
     Two-stage screening combining linear marginal BGSS with limited 2D slice rotation tests to detect pairwise XOR and diagonal cluster rotations within an $\mathcal{O}(ND + ND_1^2)$ computational budget.
  2. **Mondrian (Class-Conditional) Conformal Calibration**:
     Cluster-specific non-conformity quantiles $\hat{q}_{1-\alpha}^{(k)}$ guaranteeing equal marginal coverage across highly imbalanced subtypes when $n_{\text{cal}, k} \ge 15$.
  3. **Conformal Out-of-Distribution Anomaly Gate**:
     Landmark density-based distance scoring $d_{\text{OOD}}(X) = \min_l \|X - \mathbf{a}_l\|_2$ to trigger clean empty-set abstention under severe distribution shift, preventing set inflation to uninformative universal sets ($|C(X)| = K$).
  4. **Automated Structural Geometry Probe**:
     Lightweight sample graph Laplacian eigengap probe to automatically detect non-convex manifold topology and configure `inference_mode="spectral"` seamlessly.

---

## 3. COMPONENT MAPPING ACROSS VERSIONS

The exact differences between ICC-v2.0, ICC-v2.1, and ICC-v3.0 are mapped below across all sub-modules:

| Functional Module | ICC-v2.0 (Audited Baseline) | ICC-v2.1 (Proposed Corrective) | ICC-v3.0 (Future Redesign) |
| :--- | :--- | :--- | :--- |
| **Feature Screening** | Univariate Sarle's BC; static 5/9 threshold; default `"legacy"` | Calibrated marginal BC; documented symmetric assumptions | Two-stage Hybrid: Marginal BGSS + 2D interaction slice tests |
| **Anchor Budget $L$** | Static fixed $L=40$ | Adaptive Coupon Rule: $L^*(K) = \min(N, \max(40, \lceil 3K \ln K \rceil))$ | Dynamic entropy-minimizing landmark budget |
| **Stability Computation** | Proposition 2 ($N \le 2000$); subsample 1st-order mean ($N > 2000$) | Universal Proposition 2 for all $N$ (lines 289–320 deleted) | Parallel GPU-accelerated Proposition 2 |
| **Transfer-Cut Laplacian** | Unregularized $1/\sqrt{1 - \lambda}$ ($31,622\times$ blow-up) | Regularized floor $\max(1 - \lambda, 0.05)$ | SVD-based bipartite manifold embedding |
| **Out-of-Sample Inference** | Linear Euclidean nearest centroid Voronoi in $\mathbb{R}^D$ | Dual-mode: `"centroid"` (fast) and `"spectral"` (faithful manifold) | Unified dual-space geodesic projection |
| **Conformal Calibration** | CICC split-conformal on pseudo-labels; unnormalized $X_{\text{cal}}$ | CCAA In-Distribution Abstention; unit-normalized $X_{\text{cal}}$; margin ratio | Mondrian class-conditional + OOD density gate |
| **Model Order AutoK** | Degree-normalized PAC on $[0.10, 0.90]$ (100% $K_{\min}$ collapse) | Cosine-normalized PAC on $[0.10, 0.90]$ (authentic $K^*$) | Multi-scale spectral gap + cosine PAC consensus |
| **Decoy Feature Selection** | Independent noise decoys; 100% FDR fallback bug; dead code | Excised from codebase and manuscript | Valid Model-X knockoffs with conditional Gaussian cov. |

---

## 4. ARCHITECTURAL RECOMMENDATION FOR IMMEDIATE AUTHOR APPROVAL

The Lead Agent recommends **immediate adoption of ICC-v2.1** as the production target for the DMKD manuscript revision. 

**Justification**:
1. **Zero High-Risk Dependencies**: ICC-v2.1 requires no external heavy dependencies, no quadratic distance matrices, and no stochastic deep autoencoders.
2. **Preserves Core Genomic Strength**: By maintaining marginal BGSS and subspace ensembling as the primary path, ICC-v2.1 retains 100% of its validated superiority on high-dimensional transcriptomics (SRBCT ARI = $0.535$, Leukemia ARI = $0.467$).
3. **Eliminates All 5 Fatal P0 Defects**: Resolves CICC target conflation, AutoK normalization collapse, Transfer-Cut singular explosion, inductive manifold disconnect, and knockoff decoy flaws.
4. **Publication-Ready Rigor**: Provides complete mathematical consistency between manuscript theorems and actual Python source code.

*Upon receiving human approval, ICC-v2.1 can be cleanly implemented and validated against the Loop 2 test suite.*
