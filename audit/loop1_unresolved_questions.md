# Loop 1: Open Mathematical Questions, Unproven Bounds, and Theoretical Roadmap

**Audit Phase:** Loop 1 Mathematical, Algorithmic, and Theoretical Audit  
**Repository:** `AkashKundu114/icc-clustering` (`D:\icc-clustering`)  
**Commit:** `7ddbe8301b8d27c94f388c40acbc88b0dee82723`  
**Date:** 2026-11-02  

---

## 1. Executive Overview

This document formalizes the open mathematical problems, unproven theoretical conjectures, and unresolved foundational questions identified during the Loop 1 theoretical audit of Inductive Core Consensus v2 (ICC-v2), Anchor-Space Perturbation Profiling (ASPP), and Conformal Inductive Consensus Clustering (CICC).

Each entry defines:
- The formal mathematical statement of the problem;
- Why the current repository proof or documentation is incomplete or invalid;
- Theoretical and practical consequences;
- The precise theorem or proof required for rigorous remediation.

---

## 2. Unresolved Theoretical Questions

### Question 1: Exact Spectral Perturbation Gap Between Reduced Anchor Graph and Dense Consensus
- **Current Claim / Status:** The repository treats the Transfer-Cut bipartite spectral graph $W_A = \tilde{B}^T \tilde{B} \in \mathbb{R}^{L \times L}$ as an "efficient equivalence" or high-fidelity surrogate of the dense consensus co-association matrix $S \in [0, 1]^{N \times N}$.
- **Unresolved Mathematical Issue:** Proposition 2 proves exact computation of the scalar determinacy score $\sigma_i = \frac{1}{N-1}\sum_{j \neq i} S_{ij}^2$, but does **not** bound the spectral perturbation between the eigenspace of the dense normalized Laplacian $L_S = I - D_S^{-1/2} S D_S^{-1/2}$ and the Transfer-Cut eigenspace $V_{\text{core}}$.
- **Formal Question:** Under what conditions on the ensemble agreement matrix $S$, anchor budget $L$, and cluster separation margin $\Delta_{\text{sep}}$ does the principal angle $\Theta(U_{\text{dense}}, U_{\text{reduced}})$ satisfy a Davis-Kahan type bound:
  $$\sin \Theta(U_{\text{dense}}, U_{\text{reduced}}) \le \frac{\| \hat{S} - S \|_{\text{op}}}{\delta_{\text{spectral}}}$$
  where $\hat{S} = B D_A^{-1} B^T$ is the Nyström-like anchor operator and $\delta_{\text{spectral}} = \lambda_{K+1}(L_S) - \lambda_K(L_S)$ is the eigengap?
- **Research Impact:** Required to establish whether anchor-based consensus clustering can provably recover clusters when the eigengap of $S$ is small.

---

### Question 2: Finite-Sample Distribution of Sarle's Bimodality Coefficient Under General Gaussian Mixtures
- **Current Claim / Status:** Proposition 1 proves that for continuous symmetric unimodal distributions, $\lim_{N \to \infty} BC \le 5/9$, and that for a 2-component symmetric Gaussian mixture, $BC > 5/9$ asymptotically if and only if $\Delta/\sigma_0 > 1.854$.
- **Unresolved Mathematical Issue:** In finite samples, the estimator $BC_N = \frac{g_1^2 + 1}{g_2 + 3 c_N}$ is a nonlinear ratio of biased sample moment estimators. As proven by Agent B (Theorem 2.1), for an exact two-point cluster, $BC_N = \frac{(N-2)(N-3)}{N^2 - 1}$, which collapses below $5/9$ whenever $N \le 9$.
- **Formal Question:** What is the exact finite-sample distribution and expectation $\mathbb{E}[BC_N]$ for a $K$-component mixture model $\sum_{k=1}^K \pi_k \mathcal{N}(\mu_k, \sigma_k^2)$ as a function of sample size $N$, component proportions $\boldsymbol{\pi}$, and separation $\boldsymbol{\Delta}$?
- **Research Impact:** Essential for deriving sample-size-dependent threshold functions $\tau(N, \alpha)$ rather than relying on the asymptotic $5/9$ heuristic that discards clusters at small sample sizes.

---

### Question 3: Formal Generalization Bounds for Native Transfer-Cut Inductive Projection
- **Current Claim / Status:** Theorem 1 in `docs/theory.md` bounds misclassification error for nearest-centroid projection in Euclidean feature space $\mathbb{R}^D$:
  $$\Pr(\hat{y}(\mathbf{x}_{\text{new}}) \neq y^*(\mathbf{x}_{\text{new}})) \le (K-1)\exp\left(-\frac{\Delta_{\min}^2}{8\sigma_{\max}^2}\right)$$
  However, this bound assumes known population means, spherical isotropic covariance, and linear separability, collapsing completely on non-linear manifolds (e.g. concentric circles where $\Delta_{\min} = 0$).
- **Proposed Architectural Solution:** Agent D proposed the **Native Transfer-Cut Inductive Projection**, which evaluates out-of-sample query points via base model estimators, constructs the out-of-sample bipartite vector $\mathbf{b}(\mathbf{x}_{\text{new}})$, and projects directly into the spherical spectral embedding space $U \subset \mathbb{S}^{K-1}$.
- **Formal Question:** Can we prove an out-of-sample generalization bound for the Native Transfer-Cut Projection:
  $$\Pr(\hat{y}_{\text{spec}}(\mathbf{x}_{\text{new}}) \neq y^*(\mathbf{x}_{\text{new}})) \le \epsilon(M, L, \mathcal{R}_{\text{base}})$$
  expressed in terms of the ensemble diversity, base model Rademacher complexity $\mathcal{R}_{\text{base}}$, and anchor coverage, without assuming linear separability in $\mathbb{R}^D$?
- **Research Impact:** Would provide the first mathematically rigorous inductive spectral consensus guarantee in the literature that unrolls non-linear manifolds.

---

### Question 4: Valid Conformal Calibration Under Post-Clustering Selection Bias
- **Current Claim / Status:** CICC claims distribution-free split-conformal coverage $\Pr(y_{\text{query}} \in \mathcal{C}(\mathbf{x})) \ge 1 - \alpha$. Audits B and C proved that because calibration labels are model-generated argmax pseudo-labels, this guarantee is mathematically an **in-distribution abstention bound**:
  $$\Pr(\mathcal{C}(\mathbf{x}) = \emptyset) \le \alpha + \frac{1}{N_{\text{cal}} + 1}$$
- **Unresolved Mathematical Issue:** In unsupervised and semi-supervised deployment, practitioners seek coverage over true biological phenotypes $Y^*$. However, conditioning on discovery centroids $\mathbf{c}_k$ and selecting features using discovery labels creates severe post-selection conditioning bias.
- **Formal Question:** Can a valid conditional or marginal conformal guarantee with respect to latent biological phenotypes $Y^*$ be constructed in an unsupervised consensus setting? Specifically, if a small reference subset $N_{\text{audit}} \ll N$ has validated ground truth, what is the minimax optimal transfer-conformal score function that bounds label shift:
  $$\Pr(Y^* \in \mathcal{C}(X)) \ge 1 - \alpha - d_{\text{TV}}(P_{\text{ref}}, P_{\text{target}})?$$
- **Research Impact:** Critical for clinical diagnostic applications where misinterpreting an algorithmic abstention bound as a disease diagnostic safety guarantee could lead to adverse patient outcomes.

---

### Question 5: Optimal Dynamic Anchor Budgeting Under Arbitrary Cluster Imbalance
- **Current Claim / Status:** ICC-v2 hardcodes anchor budget $L = 40$ (or $L = \min(40, |core\_idx|)$).
- **Unresolved Mathematical Issue:** Agent E proved that covering an imbalanced cluster with prior $\pi_{\min} \ll 1/K$ with probability $1 - \delta$ requires:
  $$L \ge \frac{\ln(1/\delta)}{\pi_{\min}}$$
  When $\pi_{\min} = 0.02$ and $\delta = 0.05$, $L \ge 150$, causing $L = 40$ to suffer a 44.6% failure rate where the minority cluster receives zero anchors and completely collapses to $\mathbf{0} \in \mathbb{R}^K$.
- **Formal Question:** What is the optimal adaptive anchor selection policy $\pi_{\text{anchor}}(P_{\text{stack}})$ (e.g. Determinantal Point Processes (DPP), $k$-Means++ on partition space, or minimum-volume enclosing ellipsoids) that minimizes expected anchor budget $\mathbb{E}[L]$ subject to the constraint:
  $$\min_{k \in \{1, \dots, K\}} \Pr(L_k \ge 1) \ge 1 - \delta \quad \forall \boldsymbol{\pi} \in \Delta^{K-1}?$$
- **Research Impact:** Eliminates the static $L=40$ bottleneck and guarantees minority subtype retention in single-cell genomics and rare oncology cohorts.

---

### Question 6: Asymptotic Concentration of the AutoK Bipartite Normalization Gap
- **Current Claim / Status:** AutoK applies the Senbabaoglu Proportion of Ambiguous Clustering (PAC) metric to anchor affinity matrices to select optimal $K$. Reconciliation and Audit Tracks proved that inner products of degree-normalized anchor vectors $\langle \mathbf{b}_i, \mathbf{b}_j \rangle$ concentrate below $0.091 < 0.10$, making the PAC ambiguity window $(0.10, 0.90)$ identically empty and forcing PAC $\equiv 0$, collapsing AutoK to $K_{\min}$ in 510/510 trials.
- **Formal Question:** What is the limiting distribution of the empirical cumulative distribution function (CDF) of the anchor co-association matrix $B B^T$:
  $$F_k(c) = \frac{2}{N(N-1)} \sum_{i < j} \mathbb{I}((B B^T)_{ij} \le c)$$
  under the null hypothesis of unclustered uniform noise versus the alternative hypothesis of $K^*$ well-separated clusters, and what dynamic threshold mapping $c(L, M, K)$ restores PAC discriminatory power?
- **Research Impact:** Required to resurrect automated model order selection without reverting to computationally prohibitive $O(N^2)$ dense matrix construction.

---

## 3. Recommended Theoretical Roadmap for Loop 2 and Loop 3

```
+----------------------------------------------------------------------------------------------------+
|                                    LOOP 2 & 3 THEORETICAL ROADMAP                                  |
+----------------------------------------------------------------------------------------------------+
| Phase         | Core Task                            | Deliverable / Artifact                       |
+---------------+--------------------------------------+----------------------------------------------+
| Loop 2        | Formalize Proposition 1 Boundary     | Add Khintchine symmetry precondition & Beta  |
|               | Conditions & Finite-Sample Correction| counterexamples to Section 4.1 in manuscript |
+---------------+--------------------------------------+----------------------------------------------+
| Loop 2        | Clarify Proposition 2 vs Spectral    | Decouple scalar determinacy identity from    |
|               | Approximation in Section 4.2         | spectral clustering equivalence              |
+---------------+--------------------------------------+----------------------------------------------+
| Loop 2        | Rewrite Theorem 1 Assumptions & Scope| Narrow Theorem 1 to spherical isotropic      |
|               | in Section 4.3                       | clusters with known centroids                |
+---------------+--------------------------------------+----------------------------------------------+
| Loop 2        | Redefine CICC Conformal Guarantee as | Align Section 9 with Theorem 1 abstention    |
|               | In-Distribution Abstention Bound     | bound; disclose 46.7% pathology coverage     |
+---------------+--------------------------------------+----------------------------------------------+
| Loop 3        | Native Transfer-Cut Inductive Engine | Store base models; evaluate out-of-sample    |
|               | Algorithmic Design                   | spectral projections without Euclidean drop  |
+---------------+--------------------------------------+----------------------------------------------+
| Loop 3        | Dynamic K-Aware Anchor Budgeting     | Implement L >= max(40, ceil(3 K ln K)) bound |
|               | Implementation                       | to eliminate coupon-collector dropouts       |
+---------------+--------------------------------------+----------------------------------------------+
| Loop 3        | Rescale AutoK PAC Ambiguity Window   | Calibrate PAC thresholds to bipartite norm   |
|               | to Bipartite Density Domain          | domain [0.01, 0.08] or cosine space          |
+----------------------------------------------------------------------------------------------------+
```

---
*Report completed and stored in local audit registry.*
