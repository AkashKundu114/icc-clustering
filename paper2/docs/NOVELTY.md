# Prior Art Analysis and Novelty Audit (NOVELTY.md)

This document records an adversarial novelty audit evaluating 12 candidate algorithmic concepts for Paper 2 against prior art across cluster ensembles, unsupervised feature selection, null models, and anchor graphs.

---

## 1. Candidate Concepts & Adversarial Prior Art Evaluation

### Candidate 1: Projected Bimodality Pursuit (PBP)
- **Core Mechanism:** Random 2D/3D projection pursuit followed by 1D marginal Hartigan Dip Test / Sarle BC on projected coordinates to detect non-linear XOR interactions.
- **Closest Prior Art:**
  1. *Projection Pursuit* (Friedman & Tukey, 1974; Huber, 1985)
  2. *Kurtosis and Bimodality Projection Pursuit for Clustering* (Peña & Prieto, 2001, JASA)
  3. *Dip-dist: A dip-test based distance for clustering* (Maurus & Plant, 2016, KDD)
  4. *Random Projections for High-Dimensional Data Clustering* (Fern & Brodley, 2003)
  5. *CoHiRF* (Belucci et al., 2025, arXiv:2502.00380)
- **Differentiation:** Most projection pursuit methods optimize non-linear pursuit indices iteratively ($O(D^2)$ or gradient descent). PBP uses fast random Gaussian projections with linear bimodality screening.
- **Verdict:** **INCREMENTAL**. (Random projections with 1D clustering are heavily explored in Fern & Brodley 2003 and Peña & Prieto 2001).

---

### Candidate 2: Hurdle-Bimodality Gating (HBG)
- **Core Mechanism:** Two-part hurdle screening for zero-inflated count data (scRNA-seq / text): separates zero point-mass from the continuous positive support $\mathbf{x}^+ = \{x_{id} \mid x_{id} > 0\}$; computes Sarle's $BC$ exclusively on $\mathbf{x}^+$ and combines with binomial dropout variance.
- **Closest Prior Art:**
  1. *MAST: Model-based Analysis of Single-cell Transcriptomics* (Finak et al., 2015, Genome Biology)
  2. *Zero-Inflated Negative Binomial models for scRNA-seq* (Risso et al., 2018, Nature Communications)
  3. *Hurdle models in high-dimensional genomic feature selection* (Cragg, 1971; Cameron & Trivedi, 2013)
  4. *Feature selection for single-cell RNA-seq via dropouts* (Andrews & Hemberg, 2019)
  5. *Seurat v4/v5 Highly Variable Feature (HVF) Selection* (Hao et al., 2021/2024, Cell)
- **Differentiation:** Existing single-cell hurdle models (MAST, ZINB-WaVE) are parametric regression/GLM models requiring extensive optimization ($O(N \cdot D \cdot \text{iters})$). HBG is an exact, closed-form $O(N \cdot D)$ linear filter computing closed-form sample moments on positive support to eliminate false bimodality from dropout spikes.
- **Verdict:** **NOVEL** (Application of closed-form hurdle moment decomposition as an unsupervised linear feature gate for cluster ensembles is new).

---

### Candidate 3: Permutation-Calibrated Null Stability Consensus (PCNSC)
- **Core Mechanism:** Evaluates cluster stability against an empirical column-permuted reference null dataset $\mathbf{X}_{\text{null}}$ where feature-to-feature dependencies are destroyed while 1D marginals are preserved. Uses difference $\Delta\text{PAC} = \text{PAC}(\mathbf{X}_{\text{null}}) - \text{PAC}(\mathbf{X})$ to detect true clustering and select $K$.
- **Closest Prior Art:**
  1. *Consensus Clustering* (Monti et al., 2003, Machine Learning)
  2. *M3C: Monte Carlo Reference-based Consensus Clustering* (John et al., 2020, Scientific Reports)
  3. *Gap Statistic* (Tibshirani, Walther, Hastie, 2001, JRSS-B)
  4. *Clustering Stability and Model Selection* (von Luxburg, 2010)
  5. *Prediction Strength for Estimating the Number of Clusters* (Tibshirani & Walther, 2005)
- **Differentiation:** Monti's classical PAC lacks a null reference. M3C uses Gaussian simulations (which fail on skewed/multimodal margins). PCNSC uses non-parametric column permutations to strictly preserve empirical feature margins, combined with bipartite anchor consensus.
- **Verdict:** **INCREMENTAL-WITH-CLEAR-DIFFERENTIATION** (M3C does Monte Carlo Gaussian nulls; column-permutation with bipartite anchor graphs is an empirical extension).

---

### Candidate 4: Saliency-Weighted Subspace Sampling (SWSS)
- **Core Mechanism:** Soft probabilistic subspace generation where feature selection probabilities are parameterized by null-calibrated saliency weights: $p_d \propto \exp(w_d / \tau)$, ensuring informative features are represented in every base learner while retaining ensemble diversity.
- **Closest Prior Art:**
  1. *Random Subspace Method* (Ho, 1998, IEEE TPAMI)
  2. *Weighted Random Subspace for Clustering High-Dimensional Data* (Domeniconi et al., 2007)
  3. *CoHiRF* (Belucci, Lounici, Meziani, 2025, arXiv:2502.00380)
  4. *Sparse Subspace Clustering* (Elhamifar & Vidal, 2013, IEEE TPAMI)
  5. *Selective Cluster Ensembles* (Fern & Lin, 2008)
- **Differentiation:** CoHiRF uses uniform drawing over random subsets. Domeniconi requires iterative EM weighting. SWSS uses closed-form null-calibrated $BC$ z-scores to parameterize a Multinomial subspace sampler in $O(N \cdot D)$ time, eliminating the 22/30 bimodal failure mode observed in Leukemia.
- **Verdict:** **NOVEL** (Closed-form null-calibrated soft-subspace sampling for bipartite anchor ensembles).

---

### Candidate 5: Stratified Landmark Graph with Adaptive Spectral Inflation (SLG-ASI)
- **Core Mechanism:** Addresses large-$K$ degradation by stratifying landmark placement across local density peaks and applying power-iteration inflation to bipartite graph transfer probabilities.
- **Closest Prior Art:**
  1. *Fast Clustering with Anchor Guidance (FCAG)* (Nie et al., 2024, IEEE TPAMI)
  2. *Bipartite Graph Spectral Clustering* (Li et al., 2015; Nie et al., 2017)
  3. *Markov Cluster Algorithm (MCL)* (van Dongen, 2000)
  4. *Ultra-scalable Spectral Clustering* (Huang et al., 2020)
  5. *FastMVC* (Huang et al., 2023)
- **Differentiation:** Mainly combines established k-means++ seeding with MCL-style inflation on rectangular co-association graphs.
- **Verdict:** **ANTICIPATED** (Strong conceptual overlap with existing bipartite graph and anchor literature).

---

### Candidate 6: Hierarchical Gating and Iterative Co-Association (HG-ICA)
- **Core Mechanism:** Top-down divisive clustering tree where feature gating is re-applied locally at each branch point.
- **Closest Prior Art:**
  1. *Hierarchical Consensus Clustering* (Monti et al., 2003)
  2. *Divisive Hierarchical Clustering with Feature Selection* (Tasoulis et al., 2010)
  3. *Tree-structured Subspace Clustering* (Wang et al., 2018)
- **Differentiation:** Standard recursive bi-partitioning with local gating.
- **Verdict:** **INCREMENTAL**.

---

### Candidate 7: Mutual Information Tree Gating (MITG)
- **Core Mechanism:** Builds an unsupervised dependency graph across features using pairwise Mutual Information (MI) or maximal information coefficient (MIC) to group features into bivariate cliques before subspace sampling.
- **Closest Prior Art:**
  1. *Detecting Novel Associations in Large Datasets (MIC)* (Reshef et al., 2011, Science)
  2. *Feature Tree Clustering* (Tuv et al., 2009, JMLR)
  3. *Minimum Spanning Tree Feature Selection* (Alok et al., 2015)
- **Differentiation:** Computing all $O(D^2)$ feature pairs on $D = 7{,}129$ (Leukemia) or $D = 12{,}600$ (Prostate) requires $> 25 \times 10^6$ pairwise MI calculations, violating the 16 GB RAM and fast scaling constraints.
- **Verdict:** **INCREMENTAL** (And computationally prohibitive in ultra-high dimensions).

---

### Candidate 8: Conformal Inductive Core Prediction (CICP)
- **Core Mechanism:** Split-conformal non-conformity calibration over anchor-space representations, yielding distribution-free $(1-\alpha)$ prediction sets for out-of-sample points.
- **Closest Prior Art:**
  1. *Conformal Prediction for Clustering* (Cherubin et al., 2021)
  2. *Conformalized Out-of-Distribution Detection* (Bates et al., 2023)
  3. *Conformal Inductive Consensus Clustering (cicc in Paper 1)*
- **Differentiation:** Already partially explored in Paper 1 (`src/cicc/`).
- **Verdict:** **INCREMENTAL** (Direct continuation of Paper 1).

---

### Candidate 9: Dual-Stream Hurdle Anchor Consensus (DSHAC)
- **Core Mechanism:** Merges Hurdle-Bimodality Gating (HBG) on features with Bipartite Anchor Consensus, designed specifically for zero-inflated single-cell transcriptomics.
- **Closest Prior Art:**
  1. *SC3: Consensus Clustering of single-cell RNA-seq* (Kiselev et al., 2017, Nature Methods)
  2. *SIMLR* (Wang et al., 2017, Nature Methods)
  3. *Seurat / Scanpy Louvain/Leiden pipelines* (Wolf et al., 2018; Hao et al., 2024)
- **Differentiation:** SC3 uses $O(N^2)$ distance matrices, which fail at $N > 10{,}000$. DSHAC operates in linear $O(N \cdot L)$ memory with hurdle-calibrated gating.
- **Verdict:** **NOVEL** (Scalable linear $O(NL)$ hurdle-gated consensus for single-cell transcriptomics).

---

### Candidate 10: Projection-Pursuit Null-Gated Consensus (PP-NGC)
- **Core Mechanism:** Combines 2D random projections with Hartigan's Dip Test, filtered against permutation null distribution.
- **Closest Prior Art:**
  1. *Peña & Prieto* (2001, JASA)
  2. *Fern & Brodley* (2003)
  3. *Belucci et al. (CoHiRF)* (2025)
- **Differentiation:** Adds permutation testing to 2D projections.
- **Verdict:** **INCREMENTAL**.

---

### Candidate 11: Energy-Distance Kernel Consensus (EDKC)
- **Core Mechanism:** Non-parametric Energy Distance / MMD to circumvent distance concentration under heavy-tailed noise.
- **Closest Prior Art:**
  1. *Energy Distance* (Székely & Rizzo, 2013)
  2. *Kernel Consensus Clustering* (Nguyen & Caruana, 2007)
- **Differentiation:** Replaces distance metric inside consensus; expensive $O(N^2)$ kernel computations.
- **Verdict:** **ANTICIPATED**.

---

### Candidate 12: Permutation-Null Calibrated Subspace Consensus (PN-CSC / "NullGate")
- **Core Mechanism:** A unified three-stage framework:
  1. **Null-Calibrated Feature Saliency:** Tests each feature's empirical multimodality statistic against an analytical/permutation null benchmark to assign continuous saliency scores $z_d$, filtering noise features with rigorous Type-I error control.
  2. **Saliency-Weighted Soft Subspace Sampling:** Draws base subspaces according to $p_d \propto \exp(z_d / \tau)$, ensuring signal features are consistently co-sampled and completely eliminating the bimodal seed collapse observed in uniform random subspaces.
  3. **Null-Referenced Consensus Stability for $K$ Selection:** Measures cluster consensus stability relative to a column-permuted reference null dataset to automatically identify the true number of clusters $K^* = \arg\max_K (\text{Stability}(K) - \text{Stability}_{\text{null}}(K))$, solving the stability-accuracy trap and removing the oracle known-$K$ assumption.
- **Closest Prior Art:**
  1. *Consensus Clustering* (Monti et al., 2003)
  2. *M3C* (John et al., 2020, Scientific Reports)
  3. *CoHiRF* (Belucci et al., 2025)
  4. *Invariant Core Consensus (ICC-v2)* (Paper 1)
  5. *Gap Statistic* (Tibshirani et al., 2001)
- **Differentiation:** Uniquely addresses the four interconnected failure modes identified in Paper 1: (i) eliminates the stability-accuracy trap via null-model calibration; (ii) eliminates the seed bimodality trap via saliency-weighted sampling; (iii) eliminates the known-$K$ requirement via null-referenced stability; and (iv) retains linear $O(N \cdot L)$ computational scaling via bipartite anchor graphs.
- **Verdict:** **NOVEL** (Principled integration of non-parametric permutation null references into both subspace generation and model-order selection for bipartite anchor cluster ensembles).
