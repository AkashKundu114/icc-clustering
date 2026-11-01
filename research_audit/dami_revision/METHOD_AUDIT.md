# Phase 0: Method and Implementation Audit Report

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Audit Persona:** Agent A3 — Method and Implementation Auditor  
**Date:** November 1, 2026  
**Dedicated Revision Branch:** `research/dami-revision`  

---

## 1. Executive Summary

This method audit provides a rigorous, line-by-line inspection of the mathematical definitions, algorithmic implementations, baseline faithful representations, data preprocessing, and complexity formulations in `icc-clustering` (`src/icc/`).

### Overall Audit Verdict:
- **Core Pipeline Implementation (GAC / BGSS):** Fully mathematically sound, verified, and completely label-free.
- **Leakage Risk:** **ZERO**. No supervised ground-truth labels ($y$) enter feature gating, anchor selection, bipartite graph formation, transfer-cut spectral embedding, or K-Means discretization.
- **Baseline Implementations:** Re-evaluated. The internal random-subspace bipartite proxy previously named `FastMVC` is officially re-attributed as `FastMVC-Surrogate` (Huang et al., 2023).
- **Theoretical Claims:** Proposition 2 (sample determinacy bounds for core anchors) is mathematically derived but empirically an **indistinguishable null** ($\Delta = +0.019, p = 0.84$), as confirmed by Knockout 4 in Table 13. Theoretical claims have been calibrated to reflect this null finding.

---

## 2. Component-by-Component Algorithmic Audit

### 2.1 Bimodality-Gated Subspace Selection (BGSS)
- **Source File:** `src/icc/consensus_v2.py` (lines 145–195)
- **Mathematical Specification:**  
  For each feature $j \in \{1, \dots, D\}$, Sarle's Bimodality Coefficient ($BC$) is calculated:
  $$BC_j = \frac{g_j^2 + 1}{k_j + 3 \cdot \frac{(N-1)^2}{(N-2)(N-3)}}$$
  where $g_j$ is the sample skewness and $k_j$ is the excess kurtosis with finite-sample bias corrections.
- **Implementation Fidelity:**
  - Evaluates variances to mask zero-variance constant features ($s_j^2 < 10^{-12}$).
  - Uses `scipy.stats.kurtosis(..., bias=False)` and `scipy.stats.skew(..., bias=False)`.
  - Finite-sample denominator correction factor $3 \frac{(N-1)^2}{(N-2)(N-3)}$ for $N \ge 4$ is properly applied with a guard floor $10^{-5}$ to avoid division by zero.
  - Candidate pool extraction modes:
    - `bc_frac`: Selects top $\alpha \cdot D$ features ranked by $BC$.
    - `null_calibrated`: Filters features against the uniform null threshold $BC \ge 5/9 \approx 0.556$.
    - `random_frac` / `random`: Uniform random feature selection matching feature count (matched control).
- **Audit Assessment:** **VERIFIED**. Implementation strictly adheres to published statistical formulas. Operates entirely without external labels.

### 2.2 Base Model Generation & Random Subspacing
- **Source File:** `src/icc/consensus_v2.py` (lines 240–260)
- **Specification:**  
  Generates $M$ diverse partitions ($M = 30$ default) on random feature subspaces of size $d_{sub} = \max(2, \lfloor |S| \cdot \text{subspace\_rate} \rfloor)$.
- **Implementation Fidelity:**
  - Uses independent pseudo-random generator instances `rng = np.random.default_rng(seed)`.
  - Subspace sampling is without replacement within each draw.
  - Base clusterer default: `spectral` if $N \le 100$, else `kmeans`.
- **Audit Assessment:** **VERIFIED**.

### 2.3 Sample Stability & Anchor Selection
- **Source File:** `src/icc/consensus_v2.py` (lines 262–315)
- **Specification:**  
  Computes sample consensus agreement $S_{ij} = \frac{1}{M} \sum_{m=1}^M \mathbb{I}(P_m(i) == P_m(j))$.
  Sample stability index:
  $$\text{Stab}(i) = \frac{1}{N-1} \sum_{j \neq i} S_{ij}^2$$
- **Complexity Optimization:**
  - For $N \le 1000$, vectorized co-occurrence counts using `np.bincount(joint)` avoid explicit $N \times N$ matrix instantiation, running in $O(M^2 N + N)$.
  - For $N > 1000$, a subsample of 1000 candidate points is used to compute stability, preserving scalability.
- **Audit Assessment:** **VERIFIED**.

### 2.4 Bipartite Anchor Graph & Transfer-Cut Spectral Embedding
- **Source File:** `src/icc/consensus_v2.py` (lines 316–380)
- **Specification:**  
  Constructs bipartite affinity matrix $B \in \mathbb{R}^{N \times L}$ where $B_{il} = \frac{1}{M} \sum_{m=1}^M \mathbb{I}(P_m(i) == P_m(\text{anchor}_l))$.
  Row normalizes $B_{norm} = D_N^{-1} B$.
  Computes anchor affinity $W_{anchor} = B_{norm}^T B_{norm} \in \mathbb{R}^{L \times L}$.
  Solves normalized Laplacian $L_{norm} = I - D_A^{-1/2} W_{anchor} D_A^{-1/2}$ for the top $k$ generalized eigenvectors $V_{core} \in \mathbb{R}^{L \times k}$.
  Projects to samples via Transfer Cut:
  $$U_{emb} = B_{norm} D_A^{-1/2} V_{core} \text{diag}(1 - \lambda_k)^{-1/2}$$
- **Implementation Fidelity:**
  - `sla.eigh` performs stable symmetric eigensolve on $L \times L$ (where $L \ll N$, e.g., $L=8$ to $100$).
  - Guard floor against small eigenvalues $\max(1 - \lambda, 10^{-9})$.
  - Row normalization $\|U_{emb}\|_2 = 1$ before final K-Means discretization.
- **Audit Assessment:** **VERIFIED**. Solves the bipartite spectral graph in $O(N L k + L^3)$, drastically reducing the standard $O(N^3)$ spectral bottleneck.

---

## 3. Audit of Baselines and Method Competitors

| Baseline Key | Code Location | Claimed Reference | Actual Implementation Status | Fidelity Verdict |
| :--- | :--- | :--- | :--- | :--- |
| `K-Means` | `src/icc/baselines/classical.py` | MacQueen (1967) | `sklearn.cluster.KMeans` (k-means++, n_init=10) | FAITHFUL |
| `Ward` | `src/icc/baselines/classical.py` | Ward (1963) | `sklearn.cluster.AgglomerativeClustering(linkage='ward')` | FAITHFUL |
| `Spectral` | `src/icc/baselines/classical.py` | Ng, Jordan, Weiss (2001) | `sklearn.cluster.SpectralClustering` (rbf affinity) | FAITHFUL |
| `FCM` | `src/icc/baselines/classical.py` | Bezdek (1981) | Vectorized Fuzzy C-Means ($m=2.0$, convergence threshold $10^{-5}$) | FAITHFUL |
| `StdCons` | `src/icc/baselines/consensus.py` | Monti et al. (2003) | Dense consensus matrix, average linkage agglomeration | FAITHFUL |
| `FCAG` | `src/icc/baselines/anchor.py` | Li et al. (IEEE TKDE 2019) | Fast Bipartite Anchor Graph, k-means++ landmarks, transfer cut | FAITHFUL |
| `FastMVC-Surrogate`| `src/icc/baselines/anchor.py` | Huang et al. (TKDE 2023) | **Internal random-subspace bipartite proxy** (surrogate, not official FastMICE) | **QUALIFIED / SURROGATE** |
| `CoHiRF` | `src/icc/baselines/cohirf.py` | CoHiRF (2024) | Hierarchical random forest consensus with adaptive core estimation | FAITHFUL |
| `SparseKM` | `src/icc/baselines/sparse_kmeans.py` | Witten & Tibshirani (2010) | L1-penalized sparse K-Means with coordinate descent weight updates | FAITHFUL |
| `DEC` | `src/icc/baselines/deep.py` | Xie, Girshick, Farhadi (2016)| Deep Embedding Clustering (autoencoder pretraining + Student-t refinement) | FAITHFUL |

---

## 4. Evaluation of Theoretical Claims

### 4.1 Proposition 1: Sarle's Critical Bimodality Bound
- **Claim:** For any unimodal symmetric distribution, $BC \le 5/9 \approx 0.556$. For uniform distribution, $BC = 5/9$. Mixtures of two separated Gaussians exceed this bound ($BC \to 1.0$).
- **Audit Verification:** Mathematically rigorous and supported by classical distribution theory (Sarle 1983; Knapp 2007). Verified in synthetic bimodal simulations.

### 4.2 Proposition 2: Sample Determinacy Bounds for Core Anchors
- **Claim:** Derives finite-sample bounds certifying sample determinacy to isolate core anchors.
- **Audit Reality:** While mathematically derived, empirical knockout experiments (Table 13, Knockout 4) demonstrate that certified core anchors yield an ARI difference of $\Delta = +0.019$ ($p = 0.84$) compared to uniform random landmarks.
- **Required Action:** Proposition 2 cannot be presented as the primary driver of empirical success. The text must frankly state that core determinacy certification is an empirical null and that uniform random landmark selection achieves equivalent performance in the bipartite graph.

---

## 5. Non-Degeneracy Criteria & Discordance Protocol

- **Rule (i):** A cell is defined as discordant if $\text{Stab} \ge 0.50$ and $\text{Accuracy} \le 0.05$.
- **Rule (i') (Post-Hoc Qualification):** Excludes trivial partitions where the dominant cluster contains $>90\%$ of samples ($N_{\max} / N > 0.90$).
- **Audit Finding:**
  - When Rule (i') is applied, degenerate 1-cluster collapse is excluded, isolating partitions that produce meaningful multi-cluster splits that are completely biologically wrong.
  - When Rule (i') is omitted (unconditional), trivial partitions achieve nominal stability $= 1.0$ (every sample pair always co-occurs in the sole giant cluster).
  - **Remediation:** The manuscript and summary tables must report both unconditional and conditional discordance distributions, preventing any impression of cherry-picking.
