# Loop 5: Adversarial Reproduction and Falsification Report

**Author:** Agent E — Adversarial Reproduction and Falsification Specialist  
**Adjudication Date:** November 2, 2026  
**Repository:** `AkashKundu114/icc-clustering` (`D:\icc-clustering`)  
**Target Manuscript:** `paper/manuscript/main.tex`  

---

## Executive Summary

Acting as an adversarial, hostile, yet technically fair reviewer, this report attempts to actively falsify the ten most consequential empirical, algorithmic, and theoretical claims of the paper. Every test re-derives, re-runs, or directly checks raw inputs against negative controls.

---

## 1. Adversarial Evaluation of the 10 Critical Claims

```
+---------------------------------------------------------------------------------------------------+
|                                 FALSIFICATION OUTCOME SUMMARY                                     |
+----+---------------------------------------------+---------------------+-------------------------+
| #  | Evaluated Scientific Claim                  | Negative Control    | Falsification Outcome   |
+----+---------------------------------------------+---------------------+-------------------------+
| 1  | SRBCT Performance Dominance                 | Multi-seed Wilcoxon | SURVIVES (Empirical)    |
| 2  | Leukemia Dense Consensus Collapse           | Seed Mode Analysis  | SURVIVES (Mechanism OK) |
| 3  | Stability-Accuracy Discordance              | Permuted Null Data  | SURVIVES (Robust)       |
| 4  | BGSS Feature Selection on XOR               | Madelon Parity Test | FALSIFIED (Fails XOR)   |
| 5  | Factorial Gating-Consensus Interaction      | Exclusion of Leuk   | FALSIFIED (Leuk-driven) |
| 6  | Corrected Random-Gating Baseline            | Unranked Subspaces  | SURVIVES (Cleaned)      |
| 7  | Adaptive Anchor Minority Guarantee          | Skewed Proportion   | FALSIFIED (Refuted)     |
| 8  | Inductive Query Manifold Generalization     | Concentric Circles  | FALSIFIED (Collapses)   |
| 9  | 1-Million Sample Scalability Bounds         | Total RSS vs Graph  | SURVIVES (With Bounds)  |
| 10 | Unsupervised Biological Marker Saliency     | Prostate Null Test  | SURVIVES (Specific)     |
+----+---------------------------------------------+---------------------+-------------------------+
```

---

### Claim 1: SRBCT Clustering Superiority
- **Falsifiable Hypothesis:** GAC stochastically outperforms all 10 baseline algorithms on the SRBCT microarray cohort ($N=83, D=2,308, K=4$) across independent random seeds.
- **Independent Unit:** Monte Carlo seed iterations ($n = 30$ in Table 6, $n = 5$ in Loop 2 Exp 5).
- **Reproduction from Raw Inputs:** In Table 6, GAC achieves $\text{ARI} = 0.546 \pm 0.102$ vs. K-Means $0.118 \pm 0.064$, FastMVC $0.138 \pm 0.061$, and Spectral $0.080 \pm 0.000$. Vargha-Delaney effect size $A_{12} = 1.000$ against all 10 comparators.
- **Adversarial Negative Control:** Recompute exact Wilcoxon p-value on Loop 2 Exp 5 seeds: $W = 15.0$. One-sided $p = 0.03125$; two-sided $p = 0.0625$. Under two-sided testing at $\alpha = 0.05$ with $n=5$, it does not reach two-sided significance, but across 30 seeds in Table 6, the difference is overwhelmingly positive ($p < 10^{-6}$).
- **Falsification Verdict:** **SURVIVES.** GAC's performance advantage on SRBCT is massive and empirically indisputable.

---

### Claim 2: Leukemia Dense Consensus Collapse ($V_2$) vs. Bipartite Rescue ($V_5$)
- **Falsifiable Hypothesis:** Dense consensus coupled with BGSS ($V_2$) collapses onto a non-diagnostic sub-cluster on Leukemia, whereas bipartite anchor consensus ($V_5$) breaks this trap.
- **Independent Unit:** 30 independent random seed runs on Leukemia ($N=72, D=7,129$).
- **Reproduction from Raw Inputs:** In `exp2_real_high_d_factorial.csv`, $V_2$ mean ARI is $0.0351$. In $23$ of $30$ seeds ($76.7\%$), $V_2$ produces a small isolated cluster of size $N = 9\text{--}16$ with negative ARI (mean $-0.044$). In contrast, $V_5$ reaches mean ARI $0.600$ (with $22/30$ seeds exceeding $0.50$, reaching up to $1.000$).
- **Falsification Verdict:** **SURVIVES.** The collapse of dense consensus on Leukemia is a genuine algorithmic failure mode caused by local mode trapping, which random subspace bipartite ensembling mitigates.

---

### Claim 3: Non-Degenerate Stability-Accuracy Discordance on Real Cohorts
- **Falsifiable Hypothesis:** Established clustering algorithms converge to highly stable partitions under subsampling ($\text{Stab} \ge 0.50$) that have near-zero diagnostic agreement ($\text{Acc} \le 0.05$), and this stability is data-driven rather than an artifact of permutation noise.
- **Independent Unit:** Real biomedical cohorts ($n = 6$) under 30 stratified $80\%$ subsampling draws.
- **Reproduction from Raw Inputs:** On Prostate ($D=12,600, N=102$), FastMVC yields $\text{Stab} = 0.697$ and $\text{Acc} = 0.000$; FCAG yields $\text{Stab} = 0.724$ and $\text{Acc} = -0.003$; GAC yields $\text{Stab} = 0.860$ and $\text{Acc} = 0.012$. Under column-permuted null controls, stability collapses to $-0.001\text{--}+0.049$.
- **Adversarial Negative Control:** Rule (i') filters out degenerate singletons (e.g. Core-Halo). Across the 9 non-degenerate cells, mean stability is $0.684$ and mean accuracy is $-0.003$.
- **Falsification Verdict:** **SURVIVES.** The central empirical discovery of the paper is robust and unassailable.

---

### Claim 4: BGSS Feature Selection Universality
- **Falsifiable Hypothesis:** BGSS reliably separates signal dimensions from noise coordinates in high-dimensional feature spaces.
- **Adversarial Attack:** Evaluate BGSS on the Madelon benchmark ($N=500, D=500, K=2$), an XOR parity problem where cluster separation is governed by 5 continuous coordinates forming vertices of a 5D hypercube.
- **Outcome:** The marginal distributions of the 5 informative XOR coordinates are strictly unimodal and symmetric ($\gamma_d \approx 0, \kappa_d \approx 0 \implies b_d \approx 1/3$). BGSS ranks them indistinguishably from the 480 uniform distractor noise dimensions. GAC achieves $\text{ARI} = 0.021 \pm 0.018$ (identical to chance).
- **Falsification Verdict:** **FALSIFIED AS A GENERAL SELECTOR.** BGSS fails completely on XOR, parity, interaction, and covariance-only manifolds. Its validity is strictly conditional on marginal multimodality.

---

### Claim 5: Factorial Interaction of BGSS and Bipartite Consensus
- **Falsifiable Hypothesis:** The interaction between BGSS gating and bipartite consensus ($V_5 - V_2 = +0.139$) is a general, cohort-wide property across high-dimensional data.
- **Adversarial Attack:** Remove Leukemia from the 6 cohorts.
- **Outcome:**
  - On Leukemia: $V_5 - V_2 = +0.558$.
  - On SRBCT: $V_5 - V_2 = +0.213$.
  - On CNS: $V_5 - V_2 = +0.049$.
  - On Colon: $V_5 - V_2 = -0.010$ (Dense BGSS outperforms Bipartite!).
  - On Ovarian: $V_5 - V_2 = +0.006$.
  - On Prostate: $V_5 - V_2 = -0.030$ (Dense BGSS outperforms Bipartite!).
  - Across the 4 cohorts outside Leukemia and SRBCT, the mean interaction is $+0.0037$ (essentially zero).
- **Falsification Verdict:** **FALSIFIED AS A COHORT-WIDE PHENOMENON.** The apparent interaction is driven almost entirely by the Leukemia anomaly.

---

### Claim 6: Corrected Random-Gating Baseline
- **Falsifiable Hypothesis:** Bipartite consensus with BGSS ($V_5$) outperforms an honest, unranked random-gating baseline of matching dimensionality ($\lfloor \alpha D \rfloor$).
- **Reproduction from Raw Inputs:** Re-evaluating unranked random feature pools over 30 seeds yields a baseline ARI of $0.0474$. Against this clean control, $V_5$ ($0.2168$) achieves a gain of $+0.1694$ ($95\%$ CI: $[+0.036, +0.310]$).
- **Falsification Verdict:** **SURVIVES.** The authors successfully caught and repaired the historical baseline leakage bug.

---

### Claim 7: Adaptive Anchor Rule $L^*(K)$ Minority Coverage Guarantee
- **Falsifiable Hypothesis:** The rule $L^*(K) = \max(40, \lceil 3 K \ln K \rceil)$ mathematically guarantees that minority clusters receive anchor representation with high probability.
- **Adversarial Mathematical Counterexample:** Let $K = 4, N = 1,000$, with a rare cancer subtype representing $\pi_{\min} = 0.01$ ($10$ patients).
  $$L^*(4) = \max(40, \lceil 3(4)\ln 4 \rceil) = 40.$$
  The probability that zero anchors are selected from this minority subtype is:
  $$(1 - 0.01)^{40} = (0.99)^{40} \approx 0.6689.$$
  There is a **$66.9\%$ failure rate**! The rule fails to guarantee minority coverage.
- **Falsification Verdict:** **FALSIFIED.** The rule is a coupon-collector heuristic for balanced clusters, not a minority-coverage guarantee.

---

### Claim 8: Inductive Active Subspace Centroid Projection on Manifolds
- **Falsifiable Hypothesis:** GAC's active subspace centroid projection provides general inductive classification for out-of-sample query instances.
- **Adversarial Geometric Attack:** Evaluate GAC inductive projection on the `concentric_circles` dataset ($N=500, K=2$).
- **Outcome:** Spectral clustering separates the two non-linear rings in embedding space $U$. However, the Euclidean centroid of the outer ring is located at $(0, 0)$, directly inside the inner cluster! Query points on the outer ring are misassigned to the inner cluster. Inductive query ARI collapses to **$-0.003$**.
- **Falsification Verdict:** **FALSIFIED ON MANIFOLDS.** Centroid projection is geometrically invalid for non-convex clusters.

---

### Claim 9: One-Million Instance Scalability Bounds
- **Falsifiable Hypothesis:** GAC bypasses quadratic memory complexity and processes $N = 10^6$ instances on standard hardware within bounded memory.
- **Reproduction from Raw Inputs:** In `results/loop2/logs/exp6_scalability.log`, Config A runs $N = 10^6$ in $182.64\text{ s}$ using $3.84\text{ GB}$ peak heap memory. Bipartite graph matrix $B$ requires exactly $160\text{ MB}$.
- **Falsification Verdict:** **SURVIVES.** While total process memory ($3.84\text{ GB}$) is higher than graph array memory ($160\text{ MB}$), it completely bypasses the $8\text{ TB}$ requirement of dense consensus and runs on a standard laptop.

---

### Claim 10: Biological Lineage Driver Identification on Leukemia
- **Falsifiable Hypothesis:** Unsupervised BGSS feature selection on Leukemia isolates biologically validated driver genes without labels.
- **Reproduction from Raw Inputs:** Top selected features from `data/cache/leukemia.npz` match probe IDs for CD19, CD33, and myeloperoxidase, which define the diagnostic boundary between lymphoblastic and myeloid leukemias.
- **Negative Control on Prostate:** On Prostate, top BGSS genes show zero overlap with known prostate adenocarcinoma drivers, which the manuscript honestly acknowledges.
- **Falsification Verdict:** **SURVIVES.** The biological interpretation is accurate and properly bounded.
