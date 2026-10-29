# Confirmatory Pre-Registration Protocol (PREREGISTRATION.md)

**Title:** Permutation-Null Calibrated Consensus Clustering for High-Dimensional Manifolds (`nullconsensus`)  
**Lead Investigator & Software Architect:** Akash Kundu  
**Host Institution:** Techno India University, Kolkata, India  
**Pre-Registration Tag:** `prereg-v1`  
**Date:** October 28, 2026  

---

## 1. Study Overview & Mission
This pre-registration protocol establishes a strict, falsification-driven experimental contract for evaluating **Permutation-Null Calibrated Consensus Clustering (`NullConsensus`)** against classical and contemporary clustering algorithms.

To prevent p-hacking, publication bias, and post-hoc rationalization, all hypotheses, baselines, hyperparameters, datasets, seeds, and statistical tests are pre-registered and permanently frozen prior to unsealing the independent test suite.

---

## 2. Experimental Data Partitioning (Rule R2)

### A. Development (DEV) Suite (Seen Data)
Used exclusively for initial parameter calibration, ablation testing, and bounded design iterations ($\le 5$ rounds):
- The 13 datasets of Paper 1: CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT, Sonar, Madelon, Isolet, PBMC68k, 20 Newsgroups, Indian Pines, Extended Yale B.
- Controlled synthetic generators (`nullconsensus.data.synthetic`): Gaussian shift distractor mixtures, 2D XOR parity interactions, and zero-inflated Poisson count dropouts.

### B. Confirmatory Test (TEST) Suite (Sealed Data)
The test suite consists of **27 fresh public benchmark datasets** documented in `paper2/data/test_manifest.json` that have never been used in Paper 1 or during method design:
- 15 high-dimensional cancer microarrays from the curated Souto et al. collection (Armstrong, Bhattacharjee, Chowdary, Dyrskjot, Gordon, Pomeroy, Ramaswamy, Shipp, Singh, Su, West, Yeoh, Alizadeh, Nutt, Lapointe).
- 4 zero-inflated scRNA-seq cohorts (Zheng B-Cells, Zheng T-Cells, Klein Stem Cells, Baron Pancreas).
- 5 large-$K$ benchmarks with $K \ge 15$ (COIL-20, UMIST-Faces, Texture-16, Letter-Recognition, News-20-Subset).
- 3 low-dimensional biomedical/physical controls (Parkinsons, WDBC, Ionosphere).

**Technical Enforcement:** Access to any TEST dataset is programmatically gated by `nullconsensus.data.guard.verify_test_access_allowed()`. Any attempt to load TEST data prior to git tag `freeze-v1` and a clean working tree raises a fatal `DataPeekingViolation`.

---

## 3. Pre-Registered Hypotheses

### Primary Hypothesis (H1: Superior High-D Ranking)
> Across the high-dimensional cancer cohorts ($D/N > 20$) in the TEST suite, `NullConsensus` achieves a statistically superior average rank in Adjusted Rand Index (ARI) compared to standard consensus clustering and ambient K-Means. Specifically, the paired difference $\Delta\text{ARI} = \text{ARI}_{\text{NullConsensus}} - \text{ARI}_{\text{StdCons}}$ yields a 95% dataset-clustered bootstrap confidence interval whose lower bound strictly exceeds zero, and survives Holm-Bonferroni correction at $\alpha = 0.05$.

### Secondary Hypothesis (H2: Count-Data Recovery via HurdleGate)
> On zero-inflated count benchmarks (scRNA-seq), `NullConsensus` operating in count-aware mode (`mode="hurdle"`) significantly outperforms marginal bimodality screening (ICC-v2) by at least $+0.05$ mean ARI, demonstrating that two-part hurdle decomposition prevents dropout-driven false bimodality.

### Secondary Hypothesis (H3: Resilience to Stability-Accuracy Trap)
> Under pure isotropic distractor noise ($D_{\text{noise}} \ge 500$ with zero true cluster separation), `NullConsensus` detects absence of structure via null-referenced stability ($\Delta\text{PAC} \le 0$), successfully abstaining or flagging noise partitions where classical consensus asserts falsely confident agreement ($> 0.80$).

### Secondary Hypothesis (H4: Subspace Stability without Seed Bimodality)
> Saliency-weighted soft subspace sampling eliminates the bimodal failure distribution observed in uniform random subspaces on small-sample high-D cohorts (reducing the coefficient of variation across seeds by at least 30% relative to uniform sampling).

---

## 4. Evaluated Baselines & Frozen Defaults

All baselines are evaluated using standard scikit-learn compatible interfaces with published canonical hyperparameters:

| Method Code | Algorithmic Class | Reference / Implementation Source | Frozen Hyperparameters |
| :--- | :--- | :--- | :--- |
| `kmeans` | Classical Partitioning | Lloyd (1982), `sklearn.cluster.KMeans` | `n_init=10`, `random_state=seed` |
| `ward` | Hierarchical Agglomerative | Ward (1963), `sklearn.cluster.AgglomerativeClustering` | `linkage='ward'` |
| `spectral` | Graph Spectral | Ng, Jordan, Weiss (2001), `sklearn.cluster.SpectralClustering` | `affinity='nearest_neighbors'`, `n_neighbors=10` |
| `std_consensus` | Dense Cluster Ensemble | Monti et al. (2003), Fred & Jain (2005) | $M=25$ base K-Means, dense $N \times N$ average co-association |
| `core_halo` | Stability-Weighted Consensus | Li et al. (Artificial Intelligence 273, 2019) | $M=25, \tau_{\text{core}}=0.50$ |
| `fcag` | Anchor Graph Spectral | Nie et al. (IEEE TPAMI 46(4), 2024) | $L=40$ balanced anchors, $d=10$ nearest anchors |
| `sparse_kmeans` | Sparse Feature Weighting | Witten & Tibshirani (JRSS-B, 2010) | Heuristic $L_1$ bound tuning over 10 grid points |
| `cohirf` | Random Subspace K-Means | Belucci, Lounici, Meziani (arXiv:2502.00380, 2025) | $M=25, d_{\text{sub}}=\lfloor 0.15 D \rfloor$ random features |
| `icc_v2` | Inductive Consensus (Paper 1) | Kundu et al. (2026), `icc.consensus_v2` | $M=25, L=40, \alpha=0.15, \tau_{\text{core}}=0.50$ (Frozen) |
| `nullconsensus` | **Proposed Method** | `nullconsensus.NullConsensus` | $M=25, L=40, \alpha=0.15, B_{\text{null}}=10, \tau=1.0$ |

---

## 5. Seed Allocation & Experimental Battery

- **High-D Cohorts ($D/N > 20$):** 30 independent seeds per method ($\text{seed} \in [1000, 1029]$).
- **General / Multi-Class Cohorts ($D/N \le 20$):** 10 independent seeds per method ($\text{seed} \in [1000, 1009]$).
- **Independence:** All TEST seeds ($[1000, 1029]$) are strictly disjoint from Paper 1 / DEV seeds ($[0, 29]$).
- **Total Planned Model Fits on TEST:**  
  - 15 cancer cohorts ($D/N > 20$): $15 \times 10 \text{ methods} \times 30 \text{ seeds} = 4{,}500$ fits.
  - 12 remaining cohorts: $12 \times 10 \text{ methods} \times 10 \text{ seeds} = 1{,}200$ fits.
  - Total: **5,700 independent model evaluations**.

---

## 6. Execution Caps & Failure Handling

- **Time Cap:** Maximum 30 minutes per single model fit; maximum 6.0 hours per experiment battery.
- **Memory Cap:** Maximum 13.0 GB RAM per process (on 16 GB host).
- **Failure Accounting:** Any fit that crashes, exceeds memory limits, or times out is logged as a **failed run** (assigned $\text{ARI} = 0.0$ for ranking purposes). Failures are never discarded, re-run with relaxed constraints, or omitted from reporting.

---

## 7. Statistical Testing & Decision Framework

1. **Primary Omnibus Test:** Non-parametric Friedman rank test across all 27 TEST datasets with post-hoc two-tailed Nemenyi Critical Difference at $\alpha = 0.05$.
2. **Pairwise Comparisons:** Two-sided Wilcoxon signed-rank tests with Holm-Bonferroni multiple-comparison correction across all 9 competitor baselines.
3. **Effect Sizes & Uncertainty:** Vargha-Delaney $A_{12}$ non-parametric effect sizes and 10,000-iteration clustered bootstrap confidence intervals.
4. **Falsification & Fallback Decision Tree:**
   - **Branch A (Method Paper):** H1 is supported (paired Wilcoxon Holm $p < 0.05$, bootstrap CI strictly $> 0$, and Rank #1 on $D/N > 20$).
   - **Branch B (Regime Paper):** H1 fails globally, but H2 or H3 is supported with statistical significance in a clearly delineated regime (e.g. scRNA-seq count dropouts or pure noise screening).
   - **Branch C (Benchmark & Diagnostic Paper):** If neither H1 nor H2 yields a statistically significant advantage over the strongest baseline (ICC-v2 or CoHiRF), the paper transitions unconditionally to a benchmark and diagnostic paper reporting the null-stability diagnostic and failure taxonomy with equal scientific rigor.

---

## 8. Protocol Sign-Off & Hash Verification

- **Protocol Version:** 1.0.0
- **Pre-Registration Commit Tag:** `prereg-v1`
- **Integrity Guarantee:** Zero test-set evaluation runs will occur prior to this pre-registration sign-off.
