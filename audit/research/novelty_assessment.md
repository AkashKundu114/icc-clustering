# ICC-Clustering Novelty Assessment & Technical Claims Audit

## 1. Executive Summary

This report evaluates the claimed technical contributions of `icc-clustering` against established literature in consensus clustering, high-dimensional unsupervised learning, spectral graph theory, and conformal prediction.

---

## 2. Evaluation of Core Technical Claims

### Claim 1: Bimodality-Gated Subspace Selection (BGSS)
- **Claim:** Linear-time unsupervised feature screening using Sarle's Bimodality Coefficient ($BC$) prunes uninformative passenger/noise dimensions in $D \gg N$ regimes prior to cluster ensemble generation.
- **Implemented In:** `src/icc/core.py:25-55`, `src/icc/consensus/icc.py:175-230`
- **Comparison to Prior Art:**
  - *Sparse K-Means (Witten & Tibshirani 2010):* Employs an $L_1$ penalty on feature weights within an iterative K-Means expectation-maximization loop. Highly effective, but non-convex, sensitive to centroid initialization, and computationally expensive for large ensembles.
  - *Standard Consensus (Monti et al. 2003):* Performs random subspace draws uniformly without feature pre-filtering; in $D \gg N$ regimes where $>95\%$ of features are noise, random draws consistently select majority-noise subsets, inducing hallucinated stability.
  - *BGSS Advantage:* Operates as an independent pre-filter in strictly $O(N \cdot D)$ time. Bimodality coefficient $BC > 5/9$ identifies features exhibiting multi-modal distribution without requiring class labels.
- **Assessment:** **[Established Contribution]** Technically sound, computationally efficient, and mathematically grounded in Sarle (1983).

---

### Claim 2: Linear-Time Anchor-Bipartite Consensus Clustering
- **Claim:** Constructing an $N \times L$ bipartite anchor graph ($L \ll N$) and solving consensus via truncated SVD reduces time complexity from $O(N^3)$ to $O(N \cdot L \cdot K)$ and memory from $O(N^2)$ to $O(N \cdot L)$.
- **Implemented In:** `src/icc/consensus/icc.py:280-380`
- **Comparison to Prior Art:**
  - *Fast Certified Anchor Graph (FCAG, Li et al. 2020):* Demonstrates bipartite graph factorization for large-scale single-model spectral clustering.
  - *Fast Multi-View Consensus (FastMVC / FastMICE, Huang et al. 2023):* Applies anchor bipartite graphs to multi-view ensemble clustering.
  - *ICC-v2 Differentiation:* Combines bipartite anchor projection with random subspace ensembles and stability-weighted anchor affinity matrices.
- **Assessment:** **[Established Contribution]** Solves the primary scalability bottleneck of classical consensus clustering. Linearity verified empirically in `tests/regression/test_scaling_timing.py`.

---

### Claim 3: Anchor-Space Perturbation Profiling (ASPP)
- **Claim:** Evaluating multi-family cluster stability directly on the low-dimensional anchor graph representations ($O(N \cdot L)$) yields a diagnostic stability fingerprint without re-running base ensembles.
- **Implemented In:** `src/icc/consensus/aspp.py:1-408`
- **Comparison to Prior Art:**
  - *Monti et al. (2003) PAC & Consensus CDF:* Assesses stability across subsampling runs, but requires re-clustering the entire dataset for every bootstrap round ($O(B \cdot M \cdot N \cdot D)$).
  - *Model-Agnostic ASPP:* Decouples stability evaluation into 5 orthogonal perturbation operators (sampling, feature, measurement, technical batch shift, algorithmic).
- **Assessment:** **[Novel Diagnostic Contribution]** Provides multi-dimensional interpretability (identifying whether a cluster is sensitive to feature noise, batch effects, or subsampling) in under 1 second.

---

### Claim 4: Conformal Inductive Consensus Clustering (CICC)
- **Claim:** Extends transductive consensus clustering to online/streaming out-of-sample patient projection with finite-sample coverage guarantees ($P(Y \in \Gamma_{1-\alpha}) \ge 1 - \alpha$) and decoy feature gating.
- **Implemented In:** `src/cicc/conformal.py`, `src/cicc/decoy.py`, `src/cicc/inductive.py`
- **Comparison to Prior Art:**
  - Classical consensus clustering is strictly transductive; assigning an unseen patient requires re-clustering the entire historical cohort.
  - Inductive consensus projects query instances via anchor centroids $\mu_k^B$ in $O(N_{\text{query}} \cdot L)$ time ($\sim 5.5\ \mu\text{s}$ per sample).
  - Conformal prediction sets provide valid uncertainty quantification without parametric distributional assumptions.
- **Assessment:** **[Established Theoretical Extension]** Coverage guarantees are statistically valid under the exchangeability assumption between calibration instances and test queries.

---

## 3. Methodological Caveats & Boundary Conditions

1. **Exchangeability Assumption in Clinical Cohorts:** Conformal coverage guarantees assume calibration and test patients are independently and identically distributed. If a new query originates from an uncalibrated sequencing platform or different clinical center with strong technical batch shifts, coverage guarantees can degrade.
2. **Anchor Count Selection ($L$):** If $L < K$, the bipartite anchor graph cannot span the rank-$K$ subspace. Default $L = \min(40, N/2)$ satisfies rank requirements for typical biological subtyping ($K \in [2, 10]$).
3. **Severe Class Imbalance:** If a rare subtype represents $< 2\%$ of samples, random anchor sampling may fail to capture anchors within that cluster. Stratified or density-weighted anchor sampling is recommended for highly imbalanced cohorts.
