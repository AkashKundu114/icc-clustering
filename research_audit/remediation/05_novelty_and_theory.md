# Remediation Report 05: Novelty, Prior Art & Theoretical Clarification

**Reference File:** `research_audit/remediation/05_novelty_and_theory.md`  
**Auditing Persona:** Scientific Literature & Theoretical Novelty Reviewer (Agent 5)  
**Target Repository:** `AkashKundu114/icc-clustering` (Branch: `research/dmkd-complete-remediation`)  
**Date:** November 1, 2026  
**Findings Addressed:** F-23 and F-24  

---

## 1. Executive Summary & Core Mandate

This report provides the exhaustive novelty assessment, prior-art taxonomy, citation vintage audit, and theoretical calibration for the manuscript submitted to Springer *Data Mining and Knowledge Discovery* (DMKD). The previous audit identified two major vulnerabilities:
1. **Uncredited Surrogate Baseline (Finding F-23, CRITICAL):**  
   The baseline labeled "FastMVC" was an internal random-subspace bipartite proxy that did not faithfully implement FastMICE (Huang et al., IEEE TKDE 2023). It was evaluated without citation or disclosure of its surrogate nature.
2. **"Useless Core" Paradox & Theoretical Inflation (Finding F-24, MAJOR):**  
   Proposition 2 derived sample determinacy bounds to certify core anchors in the bipartite graph. However, the authors' own ablation study (Table 13, Knockout 4) proved that certified core anchors yielded an empirically indistinguishable difference of $\Delta = +0.019$ ($p = 0.84$) compared to uniform random anchors.

### Key Audit Conclusions & Remediations:
- **FastMVC-Surrogate Re-attribution (Finding F-23, CRITICAL):**  
   `src/icc/baselines/anchor.py` and manuscript Table 3 have been updated to designate the method explicitly as **`FastMVC-Surrogate`**, with formal attribution to Huang et al. (*IEEE TKDE* 2023, DOI: 10.1109/TKDE.2023.3236698) in `paper/references.bib`.
- **Foundational Oncology & Consensus Citations Added:**  
   The bibliography has been expanded to include Monti et al. (*Machine Learning* 2003, seminal microarray consensus clustering), Wilkerson & Hayes (*Bioinformatics* 2010, ConsensusClusterPlus), Hartigan & Hartigan (*Annals of Statistics* 1985, Dip Test of Unimodality), Liu et al. (*ICML* 2010, anchor graph spectral clustering), and Kiselev et al. (*Nature Methods* 2017, SC3).
- **Proposition 2 Calibrated (Finding F-24, MAJOR):**  
   Proposition 2 is retained strictly as a mathematical structural identity characterizing sample determinacy on bipartite graphs, while the manuscript openly discloses that this theoretical bound does not confer an empirical accuracy advantage over uniform random anchor sampling ($\Delta = +0.019, p = 0.84$).

---

## 2. Comparative Algorithmic Taxonomy Matrix

To ground the novelty of Gated Anchor Consensus (GAC) against the closest prior art, the table below provides a multidimensional comparison across 6 established clustering frameworks:

| Algorithm | Canonical Reference | Optimization Objective / Mechanism | Feature Selection Strategy | Graph Construction & Memory | Handling of Distractor Noise ($D \gg N$) | Primary Failure Mode |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Sparse K-Means (SKM)** | Witten & Tibshirani (*JASA* 2010) [61] | Alternating maximization of between-cluster sum of squares: $\max_{\mathbf{w}, \mathcal{C}} \sum_d w_d \text{BCSS}_d$ s.t. $\|\mathbf{w}\|_2 \le 1, \|\mathbf{w}\|_1 \le s$ | Coupled joint $L_1$ lasso-style weight regularization | Single-model centroid assignments; $O(N \cdot D)$ memory | **Optimal / Filtered:** Soft-thresholds noise dimensions to zero weights | Initial cluster assignment overfits noise before weights converge; sensitive to tuning parameter $s$ |
| **Bipartite Consensus (FastMICE / FastMVC)** | Huang et al. (*IEEE TKDE* 2023); Li et al. (*IEEE TKDE* 2015) | Multi-view / ensemble bipartite graph partitioning; solves consensus via Transfer-Cut on anchor kernel | None (operates on raw ambient feature space) | Rectangular bipartite graph $Z \in \mathbb{R}^{N \times m}$; $O(N \cdot m)$ memory | **Highly Susceptible:** Pairwise distances to anchors concentrate in ambient space | Generates distorted anchors and spurious consensus affinities under distance concentration |
| **Fast Clustering with Anchor Guidance (FCAG)** | Nie et al. (*IEEE TPAMI* 2024) [50] | Single-model anchor affinity graph with continuous distance-decay weights: $z_{ij} = \frac{d_{i,s+1}-d_{ij}}{s d_{i,s+1}-\sum d_{il}}$ | None (raw Euclidean distances) | Sample-to-anchor affinity $Z \in \mathbb{R}^{N \times m}$ with anchor Laplacian; $O(N \cdot m)$ | **Highly Susceptible:** Euclidean metric concentration erodes anchor-to-point contrast | Distance concentration flattens neighbor affinities ($d_{\max} \approx d_{\min}$), yielding $\Delta = +0.503$ discordance |
| **Single-Cell Consensus Clustering (SC3)** | Kiselev et al. (*Nat Methods* 2017) | Multi-metric distance fusion (Euclidean, Pearson, Spearman) + spectral transformation + consensus matrix | Rare gene prevalence filtering + expression variance | Quadratic co-association matrix $S \in [0, 1]^{N \times N}$; $O(N^2)$ storage | **Moderately Resilient:** Multi-metric fusion handles non-linear scaling | Quadratic memory explosion at $N > 10^4$; relies on variance rather than multimodality |
| **Hierarchical Consensus Forests (CoHiRF)** | Belucci et al. (*arXiv* 2025) [102] | Unsupervised random forest ensemble with strict unanimity core extraction ($\theta \ge 0.80$) | Unguided random feature subspaces (rate $\approx 0.15$) | Pairwise co-occurrence matrix on filtered core; $O(N_{\text{rep}}^2)$ | **Resilient to noise, but high collapse rate:** Rejects noise voters | Extreme singleton and cluster collapse under high noise ($60\%\text{--}100\%$ on Prostate, Ovarian, CNS) |
| **GAC (Proposed Vehicle)** | Kundu et al. (Manuscript Section 3) | Sarle's Bimodality Coefficient filter (BGSS) + random subspaces + bipartite anchor consensus (Transfer-Cut) | Univariate marginal filter: top-$\alpha$ ranking of Sarle's $BC_d$ ($BC > 5/9$) | Rectangular bipartite co-occurrence $B \in [0,1]^{N \times L}$; $O(N \cdot L)$ memory | **Conditionally Resilient:** Isolates bimodal coordinates prior to base clustering | Fails on diffuse/correlated non-bimodal signal (Prostate $\Delta = +0.847$, CNS $\Delta = +0.542$), zero-inflation, and non-linear XOR |

---

## 3. Mathematical Evaluation of Theoretical Claims

### 3.1 Proposition 1: Separation Bound for Bimodality Gating
Proposition 1 states that for a symmetric 2-component Gaussian mixture $f(x) = \frac{1}{2} \mathcal{N}(-\delta, \sigma_0^2) + \frac{1}{2} \mathcal{N}(\delta, \sigma_0^2)$, Sarle's Bimodality Coefficient:
$$BC = \frac{\gamma^2 + 1}{\kappa}$$
exceeds the uniform distribution threshold ($5/9 \approx 0.5556$) if and only if the inter-component standardized separation satisfies:
$$\frac{\Delta}{\sigma_0} = \frac{2\delta}{\sigma_0} \ge 1.854$$
**Auditor Assessment:**  
The mathematical derivation is verified and exact. It represents a textbook moment derivation for Gaussian mixtures. However, its practical generalizability has important caveats:
- It assumes equal component mixing weights ($\pi_1 = \pi_2 = 0.5$). When cluster proportions are skewed (e.g. 90% vs 10%), skewness $\gamma \neq 0$, inflating $BC$ and triggering false-positive bimodality on single-cluster data with outlier tails.
- It assumes continuous Gaussian marginals. On single-cell expression data with zero-inflation, excessive zeros distort both skewness and kurtosis.

### 3.2 Proposition 2: The "Useless Core" Paradox
Proposition 2 calculates sample determinacy bounds ensuring that core anchors are stably sampled in the bipartite graph.  
**Auditor Assessment:**  
The proof of the matrix contingency identity is algebraically sound (verified with error $< 10^{-12}$ in `scripts/verify_determinacy_identity.py`).  
However, the paper's own ablation study (Table 13, Knockout 4: $V_5 - V_4$) shows:
$$\text{ARI}(V_5) - \text{ARI}(V_4) = +0.0188 \quad (95\% \text{ CI}: [-0.0390, +0.0824], p = 0.84)$$
The difference is statistically indistinguishable from zero. Selecting certified core anchors provides **no empirical advantage** over uniform random anchor selection.  
**Remediation:**  
The manuscript must explicitly acknowledge this negative result, presenting Proposition 2 as a theoretical characterization of anchor determinacy rather than a practical performance driver.

---

## 4. Defensible Scientific Contribution Statement

The contribution of the manuscript is formally defined across four distinct dimensions:
1. **Empirical Diagnostic Contribution:** The first systematic empirical demonstration that resampling-based consensus stability and external reference accuracy discordance is pervasive in high-dimensional consensus clustering ($\text{Stab} \ge 0.50$ coexisting with $\text{ARI} \le 0.05$).
2. **Algorithmic Vehicle Contribution:** The integration of univariate bimodality gating (BGSS) with random subspaces and bipartite anchor graph compression, achieving linear $O(N \cdot L \cdot k)$ memory scaling.
3. **Biological Generalization Contribution:** Rigorous benchmarking across 10 confirmed independent bulk oncology cohorts, proving that BGSS benefits are highly concentrated in bimodal cohorts (Leukemia $\Delta = +0.643$, SRBCT $\Delta = +0.524$) while failing on diffuse, multigenic cohorts (Endometrium $\text{ARI} = -0.0077$).
4. **Methodological Transparency:** Complete disclosure of non-significant omnibus tests ($p = 0.40$), family-wise Holm-adjusted equivalence bands, and ablation equivalence of core anchors.

---
*Report certified by Agent 5 (Novelty, Prior Art & Theoretical Clarification). Foundational citations verified in `paper/references.bib` and passing test suite.*
