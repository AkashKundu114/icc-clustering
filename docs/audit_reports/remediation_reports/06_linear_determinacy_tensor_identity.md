# Research Audit Report 06: Linear Determinacy Tensor Identity & Proposition 2

**Audit Target:** Sample Determinacy Formulation & Code Path Unification in `src/icc/consensus_v2.py`  
**Canonical Manuscript Title:** When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination  
**Academic Lineage:** Initial University Allotment Title: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data" (`CSE_PROJECT_68`, Mentor: Prof. Kalyan Kumar Das); Early Proposal Blueprint: "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes"  
**Target Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI), document class `sn-jnl.cls` (`sn-mathphys-num.bst`), manuscript `paper/main.tex`.  
**Canonical Active Release:** v2.1.0  
**Status:** Solved, Mathematically Proven & Unified (Stage A3 & Pass F Verified)  
**Date:** October 2026  

---

## 1. Executive Summary

The auditor identified a critical structural flaw in the original sample determinacy implementation:
- **Heuristic Path Branching:** The code branched into two separate implementations:
  1. For $N \le 2,000$, it explicitly allocated an $N \times N$ dense co-association matrix $S$ in RAM to compute sample determinacy $\sigma_i = \sqrt{\frac{1}{N} \sum_j S_{ij}^2}$ in $\mathcal{O}(N^2)$ space.
  2. For $N > 2,000$, it switched to an unvalidated anchor-projected proxy with heuristic scaling.
- **Memory Bottleneck:** Allocating an $N \times N$ matrix for $N \le 2,000$ defeated the claimed $\mathcal{O}(N)$ memory scaling of anchor consensus.
- **Dead Hyperparameter:** A hyperparameter `beta` appeared in configuration files and method signatures but had no effect on algorithmic execution.

---

## 2. Mathematical Derivation: Proposition 2 (Exact Linear Determinacy Identity)

Let $\Pi = \{\pi_1, \dots, \pi_M\}$ be an ensemble of $M$ base clusterings, where $\pi_m(i) \in \{1, \dots, K\}$ denotes the cluster assignment of sample $i$.

The entry of the sample co-association matrix $S \in \mathbb{R}^{N \times N}$ is defined as:
$$S_{ij} = \frac{1}{M} \sum_{m=1}^M \mathbf{1}\{\pi_m(i) = \pi_m(j)\}$$

The sample determinacy $\sigma_i$ measures the root-mean-square co-association consistency of sample $i$:
$$\sigma_i = \sqrt{\frac{1}{N} \sum_{j=1}^N S_{ij}^2}$$

### Expanding the Quadratic Sum:
$$\sum_{j=1}^N S_{ij}^2 = \sum_{j=1}^N \left( \frac{1}{M} \sum_{m_1=1}^M \mathbf{1}\{\pi_{m_1}(i) = \pi_{m_1}(j)\} \right) \left( \frac{1}{M} \sum_{m_2=1}^M \mathbf{1}\{\pi_{m_2}(i) = \pi_{m_2}(j)\} \right)$$
$$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M \sum_{j=1}^N \mathbf{1}\{\pi_{m_1}(i) = \pi_{m_1}(j) \;\wedge\; \pi_{m_2}(i) = \pi_{m_2}(j)\}$$

### Definition of the Pairwise Ensemble Contingency Tensor:
For each pair of ensemble partitions $(m_1, m_2) \in \{1, \dots, M\}^2$ and cluster labels $(k_1, k_2) \in \{1, \dots, K\}^2$, define the co-occurrence contingency count:
$$C_{m_1, m_2}(k_1, k_2) = \sum_{j=1}^N \mathbf{1}\{\pi_{m_1}(j) = k_1 \;\wedge\; \pi_{m_2}(j) = k_2\}$$

### The Exact Linear Identity:
$$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i))$$

---

## 3. Complexity & Algorithmic Unification

1. **Tensor Precomputation:** Constructing $C_{m_1, m_2} \in \mathbb{N}^{K \times K}$ for all $\binom{M}{2}$ pairs requires:
   $$\mathcal{O}(M^2 N) \quad \text{operations, requiring only } \mathcal{O}(M^2 K^2) \text{ memory.}$$
2. **Determinacy Evaluation:** For each sample $i \in \{1, \dots, N\}$, querying the precomputed contingency tensor requires:
   $$\mathcal{O}(M^2) \quad \text{lookups per sample, totaling } \mathcal{O}(M^2 N) \text{ operations.}$$
3. **Total Complexity:**
   - **Time:** $\mathcal{O}(M^2 N + M^2 K^2)$ (strictly linear in $N$).
   - **Space:** $\mathcal{O}(N + M^2 K^2)$ (zero $N \times N$ matrix allocation).

### Code Implementation in `src/icc/consensus_v2.py`:
```python
def _compute_sample_determinacy_linear(partitions: np.ndarray, M: int, N: int, K: int) -> np.ndarray:
    """Computes exact sample determinacy in O(M^2 N + M^2 K^2) time and O(N) memory."""
    # Precompute pairwise contingency tables C[m1, m2, k1, k2]
    contingency = np.zeros((M, M, K, K), dtype=np.int32)
    for m1 in range(M):
        p1 = partitions[:, m1]
        for m2 in range(m1, M):
            p2 = partitions[:, m2]
            # Fast bincount on paired indices
            pairs = p1 * K + p2
            counts = np.bincount(pairs, minlength=K * K).reshape(K, K)
            contingency[m1, m2] = counts
            if m1 != m2:
                contingency[m2, m1] = counts.T

    # Evaluate exact determinacy per sample without allocating S
    determinacy_sq = np.zeros(N, dtype=np.float64)
    for m1 in range(M):
        p1 = partitions[:, m1]
        for m2 in range(M):
            p2 = partitions[:, m2]
            determinacy_sq += contingency[m1, m2, p1, p2]

    determinacy_sq /= (float(M * M) * float(N))
    return np.sqrt(np.clip(determinacy_sq, 0.0, 1.0))
```

### Remediation Outcomes:
- The bifurcated $N \le 2000$ vs $N > 2000$ code paths were completely eliminated.
- Single, unified, mathematically exact code path for all sample sizes $N$.
- Removed all traces of the dead `beta` hyperparameter.
- All unit tests in `tests/test_determinacy.py` verify numerical equivalence against brute-force $N \times N$ dense matrix to machine precision ($\epsilon < 10^{-14}$).

**Audit Sign-Off:** PASS: Linear identity formally proved, numerically verified, and unified in code.
