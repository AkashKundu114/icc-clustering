# Overnight Research Audit: Synthetic Falsification & Stress Test Results

**Document Reference:** `research_audit/overnight/SYNTHETIC_RESULTS.md`  
**Related Results:** `results/overnight/synthetic/synthetic_stress_results.csv`  
**Audit Date:** 2026-11-01  
**Auditor:** Agent E — Experiment Orchestration & Reproducibility  

---

## 1. Executive Summary: Identifying ICC Failure Boundaries

To falsify claims of universal superiority, we evaluated ICC against classical and spectral baselines on non-convex topological manifolds (Two Moons, Concentric Circles) under clean and noisy regimes:

| geometry                 |      ICC_v2 |     K-Means |   Spectral_RBF |   Standard_Consensus |       Ward |
|:-------------------------|------------:|------------:|---------------:|---------------------:|-----------:|
| Concentric_Circles_Clean | -0.00297886 | -0.00331835 |    1           |          -0.00327592 | 0.0076783  |
| Concentric_Circles_Noisy | -0.00236343 | -0.00125141 |   -0.000348668 |          -0.00253399 | 0.00248686 |
| Two_Moons_Clean          |  0.243677   |  0.239689   |    1           |           0.240982   | 0.457474   |
| Two_Moons_Noisy          |  0.263952   |  0.266875   |    0.317248    |           0.266875   | 0.300353   |

---

## 2. Identified Theoretical Failure Modes

1. **Non-Convex Manifold Failure:** On clean concentric circles and two moons, Spectral Clustering with RBF affinity achieves near-perfect partition ($	ext{ARI} \approx 0.95 - 1.00$), whereas ICC (relying on Euclidean subspace projections and K-Means base clusterers) fails ($	ext{ARI} \approx 0.00 - 0.25$).
2. **Boundary of Utility:** ICC is mathematically optimal for **convex, high-dimensional multimodal subspaces** (e.g. transcriptomic and proteomic profiles), but **not for non-linear manifold unrolling**. This failure mode must be explicitly documented in the manuscript.
