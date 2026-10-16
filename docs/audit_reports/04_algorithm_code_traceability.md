# Report 04: Algorithm-Code Traceability & Implementation Verification

**Target Manuscript:** `ieee_manuscript/main.tex` (Algorithms 1 & 2)  
**Implementation Source:** `src/icc/consensus_v2.py` & `src/icc/aspp.py`  
**Audit Dimension:** Line-by-Line Alignment Between Theory, Pseudocode, and Source Code  
**Date:** October 16, 2026  

---

## 1. Algorithm 1: Invariant Core Consensus (ICC-v2) Traceability

Below is the step-by-step mapping between the mathematical formulation in Algorithm 1 of `main.tex` and the hardened Python implementation in [`src/icc/consensus_v2.py`](file:///d:/Final%20Year%20Project/src/icc/consensus_v2.py):

| Alg 1 Step | Mathematical Operation / Concept | LaTeX Equation in `main.tex` | Source Code Location (`consensus_v2.py`) | Traceability Status & Verification |
|---|---|---|---|:---:|
| **Input Check** | Matrix validation & sanitization | $X \in \mathbb{R}^{N \times D}$, finite, $N \ge K$ | `fit_predict()` lines 181–193 | **VERIFIED:** Rejects 1D/3D shapes, empty arrays, NaNs, and Infs. |
| **Step 1** | Finite-Sample Sarle Bimodality Scoring | $\text{BC}_d = \frac{g_1(d)^2 + 1}{g_2(d) + \text{corr}_N + \epsilon}$ | `fit_predict()` lines 198–218 | **VERIFIED:** Memory-bounded column chunking calculates exact unbiased SBC. |
| **Step 2** | Variance-Stabilized Subspace Gating (VSSG) | $\mathcal{P}_{\text{active}} = \text{Top}(\text{BC}, \rho \cdot D)$ | `fit_predict()` lines 220–270 | **VERIFIED:** Supports `legacy`, `bc_frac`, `robust`, and `null_calibrated` modes. |
| **Step 3** | Base Ensemble on Guided Subspaces | $\mathcal{P} = \{\pi_1, \dots, \pi_M\}, \quad \pi_m \in [K]^N$ | `fit_predict()` lines 280–290 | **VERIFIED:** Draws diverse guided subspaces of size $d_{\text{sub}}$; runs `run_clusterer()`. |
| **Step 4a** | Co-Association Determinacy Stability Identity | $\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2} \sum_{m_1, m_2} C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i))$ | `fit_predict()` lines 295–315 | **VERIFIED:** Proposition 2 implemented; exact symmetry cuts evaluations by 2x. |
| **Step 4b** | Statistical Anchor Certification | $\mathcal{A}_{\text{core}} = \{i : \text{stab}_i \ge \tau_{\text{core}}\}, \quad L = \min(m, |\mathcal{A}|)$ | `fit_predict()` lines 316–330 | **VERIFIED:** Top core quantile certified; $L$ anchors sampled uniformly without replacement. |
| **Step 4c** | Bipartite Rectangular Co-Association | $B_{i, \ell} = \frac{1}{M} \sum_m \mathbf{1}\{\pi_m(i) = \pi_m(a_\ell)\}$ | `fit_predict()` lines 331–337 | **VERIFIED:** In-place accumulation in $O(NL)$ memory. |
| **Step 5** | Bipartite Spectral Consensus (Transfer-Cut) | $L_{\text{anchor}} = I - D_A^{-1/2} W_A D_A^{-1/2}, \quad U = B_{\text{norm}} V$ | `fit_predict()` lines 338–365 | **VERIFIED:** Solves $K$ smallest eigenvalues via `subset_by_index=[0, k-1]`; K-Means on $U$. |
| **Step 6** | Stability-Calibrated Centroid Construction | $\mu_c = \frac{\sum_{i \in \mathcal{C}_c} w_i X_i}{\sum_{i \in \mathcal{C}_c} w_i}$ | `fit_predict()` lines 366–395 | **VERIFIED:** Stability-weighted cluster centroids cached; pre-sliced subspace centroids stored. |
| **Step 7** | Inductive Out-of-Sample Assignment | $\hat{y}(x_{\text{new}}) = \arg\min_c \|(x_{\text{new}} - \mu_c)_{\mathcal{P}_{\text{active}}}\|_2$ | `predict()` & `transform()` lines 475–515 | **VERIFIED:** Subspace projection executed in $O(K \cdot d_{\text{sub}})$ without re-clustering. |

---

## 2. Algorithm 2: Anchor-Space Perturbation Profiling (ASPP) Traceability

Below is the traceability mapping for Algorithm 2 (ASPP) in [`src/icc/aspp.py`](file:///d:/Final%20Year%20Project/src/icc/aspp.py):

| Alg 2 Step | Theoretical Operation | Implementation Location (`aspp.py`) | Verification Status |
|---|---|---|:---:|
| **Perturbation Engine** | 5 physical perturbation families (Sampling, Feature, Measurement, Technical, Algorithmic) | `_apply_perturbation()` lines 87–170 | **VERIFIED:** Applies controlled row dropout, feature masking, noise injection, and batch offsets. |
| **Anchor Tracking** | Map original certified anchors into perturbed views $\mathcal{A}_{\text{obs}}$ | `profile()` lines 260–275 | **VERIFIED:** Tracks surviving anchor positions without quadratic expansion. |
| **Perturbed Bipartite** | Auxiliary rectangular co-association $B^{(p, r)} \in \mathbb{R}^{N_{\text{obs}} \times L_{\text{obs}}}$ | `profile()` lines 280–305 | **VERIFIED:** Memory strictly bounded at $O(N_{\text{obs}} \cdot L_{\text{obs}})$. |
| **Compact Eigensystem** | Spectral extraction on $L_{\text{obs}} \times L_{\text{obs}}$ anchor Laplacian | `profile()` lines 307–325 | **VERIFIED:** Solves $K$ eigenvalues via `subset_by_index`. |
| **Stability Fingerprint** | Cluster-level membership retention & PSI computation | `profile()` lines 330–415 | **VERIFIED:** Computes Jaccard retention, $\text{PSI}_k$, and categorical reliability. |

---

## 3. Discontinued / Deprecated Code Path Audit

1. **Elimination of Dense $N \times N$ Bifurcation:**  
   The legacy codebase previously branched at $N = 2000$ (`if N <= self.dense_threshold: build_dense_S()`). This caused algorithmic inconsistency and $O(N^2)$ memory bloat. In the hardened codebase, Proposition 2 is universally executed for all $N$, providing complete mathematical unification.
2. **Deprecation of `beta`:**  
   The v1 hyperparameter `beta` has no mathematical role in ICC-v2. It now emits an explicit `DeprecationWarning` and is thoroughly tested in `tests/test_consensus_v2.py`.
3. **Subspace Centroid Pre-Caching:**  
   `self.anchor_centroids_sub_` is stored at the conclusion of `fit_predict()`, eliminating redundant centroid slicing during inductive inference queries.
