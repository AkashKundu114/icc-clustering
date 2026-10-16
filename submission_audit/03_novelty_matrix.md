# 03 — Novelty Matrix & Prior-Art Decomposition

**Auditor:** Novelty & Prior-Art Investigator  
**Target:** Literature Positioning for *Data Mining and Knowledge Discovery*  
**Date:** October 13, 2026  

---

## 1. Prior-Art Landscape & Deconstructed Ingredients

To survive adversarial review, we explicitly delineate established literature components from the genuine contribution of ICC-v2:

| Component | Closest Literature & Prior Art | Established Fact / Prior Knowledge | ICC-v2 Relationship & True Delta | Novelty Classification |
|---|---|---|---|---|
| **Cluster Ensemble Formulation** | Strehl & Ghosh (JMLR 2002); Fred & Jain (TPAMI 2005) | Co-association matrix aggregation and hypergraph partitioning of base clusterings. | ICC-v2 uses evidence accumulation as base generator, but replaces the dense $N \times N$ matrix with anchor graph. | Established Prior Art |
| **Sarle's Bimodality Coefficient (BC)** | Sarle (SAS Institute 1983); Knapp (1990) | $BC = \frac{\gamma^2 + 1}{\kappa + 3}$ used in SAS clustering criterion for multimodal detection. | ICC-v2 applies finite-sample adjusted BC as an unsupervised linear feature screening filter prior to consensus ensembling. | Known Component in New Pipeline |
| **Bipartite Transfer-Cut Spectral Clustering** | Li, Yang, Xu (TKDE 2015); Nie et al. (TPAMI 2024, FCAG) | Bipartite graph $B \in \mathbb{R}^{N \times L}$ avoids $N \times N$ affinity matrix; decomposes on $L \times L$ space. | ICC-v2 uses Transfer-Cut formulation for consensus co-association graphs rather than raw Euclidean data graphs. | Known Component in New Pipeline |
| **Determinacy-Guided Core Selection** | Li, Zhang, Zhang (TKDE 2019) | Determinacy $\sigma_i = \sum_{j \neq i} S_{ij}^2$ measures consensus confidence; used to regularize matrix factorization. | Li et al. explicitly construct the full $N \times N$ matrix $S$. ICC-v2 computes exact $\sigma_i$ via cross-partition contingency tables without constructing $S$. | **Potentially Novel Algorithmic Contribution** |
| **Linear Determinacy Contingency Identity** | Unacknowledged in consensus clustering literature | Proposition 2 expresses row sum of squared co-associations as sum of joint contingency counts across partition pairs. | First closed-form contingency identity computing exact $\sigma_i$ in $O(M^2 N + M^2 K^2)$ time and $O(N + K^2)$ memory. | **Potentially Novel Theoretical Contribution** |
| **Closed-Form Centroid Induction** | Out-of-sample Nyström extensions (Fowlkes et al. 2004) | Classical consensus is strictly transductive; out-of-sample mapping requires re-clustering. | ICC-v2 weights centroids by sample determinacy in the active subspace to assign unseen points in $O(K \cdot |\mathcal{F}_{\text{active}}|)$ time. | **Potentially Novel Algorithmic Contribution** |
| **Anchor-Space Perturbation Profiling (ASPP)** | Monti et al. (Mach Learn 2003); Ben-Hur et al. (Pac Symp Biocomput 2002) | Cluster stability evaluated by resampling data and comparing all-pairs co-association tensors $O(P \cdot N^2)$. | ASPP evaluates 5 physical perturbation families strictly over $L$ certified anchor coordinates in $O(P \cdot NL)$ memory. | **Potentially Novel Algorithmic Contribution** |
| **Finite-Sample Stability Breakdown (Exp 0)** | Beyer et al. (ICDT 1999) on distance concentration | Theoretical concentration is known, but consensus ensemble behavior under isotropic noise was uncharacterized. | Empirical demonstration that consensus ensembles fall into a deceptive "stability trap" ($>0.8$ stability on pure noise boundaries). | **Potentially Novel Empirical Finding** |

---

## 2. Novelty Summary Matrix

| Claimed Contribution | Status After Literature Deconstruction | Recommendation for Manuscript |
|---|---|---|
| "Universal Superiority Across Multi-Domain Datasets" | **UNSUPPORTED / FALSE** | REMOVE. Friedman test $p=0.33$. Method loses to Ward and DEC on large-$N$, large-$K$ datasets. |
| "Rank #1 on Ultra-High-Dimensional Biomedical Regimes ($D/N > 20$)" | **SUPPORTED & DEFENSIBLE** | RETAIN as headline empirical contribution. |
| "Proposition 2 Contingency Identity Eliminates $O(N^2)$ Storage" | **SUPPORTED & NOVEL** | RETAIN as central theoretical contribution. |
| "Linear-Time Bimodality Subspace Gating (BGSS)" | **SUPPORTED** (as pipeline component) | RETAIN with proper attribution to Sarle (1983). Avoid claiming discovery of bimodality coefficient. |
| "Anchor-Space Perturbation Profiling" | **SUPPORTED & NOVEL** | RETAIN as practical stability diagnostic tool without quadratic overhead. |

---

## 3. The Defensible Central Hypothesis

> **Central Hypothesis:** In high-dimensional data regimes subject to isotropic distractor noise ($D \gg N$), unsupervised consensus clustering degrades due to distance concentration. By gating features via finite-sample bimodality coefficients and constructing a bipartite consensus graph over determinacy-certified anchors via cross-partition contingency tables, ICC-v2 recovers genuine cluster geometry in $O(N)$ auxiliary memory and enables closed-form inductive inference without materializing the $O(N^2)$ co-association matrix.
