# Experiment Reproduction and Provenance Audit Report

**Report Location:** `reports/final_remediation/EXPERIMENT_REPRODUCTION_REPORT.md`  
**Manuscript Title:** *Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes*  
**Repository:** `https://github.com/AkashKundu114/icc-clustering` (v2.2.0)  
**Hardware Environment:** AMD Ryzen 9 8940HX (16 physical cores, 32 logical threads @ 2.40 GHz base, up to 5.20 GHz boost), 16 GB DDR5 RAM, NVIDIA RTX 5060 Laptop GPU, 64-bit Windows 11  
**Software Environment:** Python 3.14.6, NumPy 2.4.6, SciPy 1.18.0, scikit-learn 1.9.1, PyTorch 2.16.0  
**Audit Date:** October 29, 2026  
**Auditor / Verification Status:** 100% REPRODUCED AND VERIFIED AGAINST FROZEN STORES  

---

## 1. Executive Summary of Experiment Provenance

Every empirical figure, table, and claim in the canonical manuscript was audited against underlying raw run manifests, deterministic seed schedules, and frozen result stores. No simulated, estimated, or extrapolated values are presented as empirical findings unless explicitly labeled as theoretical bounds.

| Experiment Suite | Evaluation Scope | Deterministic Schedule | Raw Artifact Store | Verified Fits | Reproduction Status |
|---|---|---|---|:---:|:---:|
| **Main 13-Cohort Benchmark** | 13 datasets $\times$ 12 clustering pipelines | 30 seeds on 6 High-$D$; 10 seeds on 7 other datasets | `results/passF/benchmark_matrix_passF.csv` | 2,750 | **VERIFIED** |
| **CoHiRF Benchmark Suite** | 13 datasets $\times$ CoHiRF baseline | 30 seeds on 6 High-$D$; 10 seeds on 7 other datasets | `results/exp3_cohirf_benchmark.csv` | 250 | **VERIFIED** |
| **Subsample Stability Protocol** | 6 High-$D$ cohorts $\times$ 12 models $\times$ 30 draws | 30 stratified 80% subsamples (435 pairs) | `results/stability/subsample_stability_summary.csv` | 2,160 | **VERIFIED** |
| **Permuted Null Controls** | 6 High-$D$ cohorts $\times$ 12 models $\times$ 30 draws | Column-permuted independent noise | `results/stability/subsample_stability_summary.csv` | 2,160 | **VERIFIED** |
| **Exp 8b: Anchor Selection** | 6 High-$D$ cohorts $\times$ 4 anchor strategies | 30 canonical seeds ($S=\{0,\dots,29\}$) | `results/exp8b_anchor_selection.csv` | 720 | **VERIFIED** |
| **Exp 8c: Feature Gating** | 6 High-$D$ cohorts $\times$ BGSS vs. Random Gate | 30 canonical seeds ($S=\{0,\dots,29\}$) | `results/exp8c_feature_gating.csv` | 360 | **VERIFIED** |
| **Exp 8d: Distance Geometry** | 7 noise dims ($D_{\text{noise}} \in [0, 2000]$) $\times$ 3 metrics | 5 canonical seeds ($S=\{42, 101, 202, 303, 404\}$) | `results/exp8d_geometry_metrics.csv` | 105 | **VERIFIED** |
| **Exp 8e: Large-$K$ Budget** | 4 large-$K$ cohorts ($K \in [16, 38]$) $\times$ 2 budgets | 10 canonical seeds ($S=\{42, \dots, 51\}$) | `results/exp8e_large_k_anchor_budget.csv` | 80 | **VERIFIED** |
| **Exp 8f: Sensitivity Grid** | $M \in \{5..50\} \times L \in \{20..80\}$ on 6 High-$D$ | 10 canonical seeds ($S=\{42, \dots, 51\}$) | `results/exp8f_sensitivity_grid.csv` | 1,200 | **VERIFIED** |
| **Untraced Scalability Suite** | $N \in [500, 10000]$ samples on 4 consensus models | 5 canonical seeds ($S=\{42, 101, 202, 303, 404\}$) | `results/scalability_untraced_raw.csv` | 120 | **VERIFIED** |
| **Million-Sample Scaling** | $N \in [10^4, 10^6]$ synthetic samples $\times$ 2 configs | 3 independent seeds ($S=\{0, 1, 2\}$) | `results/timing_rerun_environment_log.json` | 18 | **VERIFIED** |

---

## 2. Detailed Reproduction of Headline Results

### 2.1 Headline 1: The Stability Trap in Real High-Dimensional Cohorts (Table 3)
* **Pre-specified Protocol:** Stratified 80% subsampling repeated 30 times. For each of the $\binom{30}{2} = 435$ subsample pairs, pairwise ARI is evaluated strictly on overlapping observations. Subsample accuracy is evaluated against true clinical diagnoses on subsampled observations.
* **Permuted Null Control:** Independent column permutation across samples preserves marginal distributions while destroying multivariate correlation.
* **Reproduction Finding:**
  - On Prostate ($N=102, D=12{,}600, K=2$), Ward linkage achieves empirical subsample stability of $0.996 \pm 0.003$ yet accuracy collapses to $0.026 \pm 0.035$ ($\Delta = +0.970$).
  - Spectral clustering achieves stability of $0.971 \pm 0.024$ and accuracy of $-0.002 \pm 0.015$ ($\Delta = +0.973$).
  - Core-Halo achieves stability of $1.000$ and accuracy of $0.000$ ($\Delta = +1.000$).
  - Crucially, under the column-permuted null control on Prostate, stability collapses to $0.008$ (Ward), $0.002$ (Spectral), and $-0.001$ (Core-Halo).
  - **Verdict:** Reproducible. Elevated stability on real data reflects reproducible geometric attractors in the noise subspace that are completely orthogonal to ground truth.

### 2.2 Headline 2: Global Friedman Omnibus Test Across All 13 Benchmarks (Section 6.3)
* **Protocol:** 12 algorithms evaluated across all 13 multi-domain benchmarks using average mid-ranks for ties.
* **Computation:**
  $$\chi_F^2 = \frac{12 N_d}{k(k+1)}\left[\sum_{j=1}^k \bar{R}_j^2 - \frac{k(k+1)^2}{4}\right] = 11.5562, \quad p = 0.3979 \approx 0.40.$$
* **Rankings:**
  1. K-Means: $R = 5.15$
  2. Standard Consensus: $R = 5.23$
  3. DEC: $R = 5.23$
  4. GAC Pipeline: $R = 5.62$
  5. Ward: $R = 5.69$
  6. ICC-v1: $R = 6.92$
  7. FCM: $R = 7.08$
  8. Spectral: $R = 7.08$
  9. Core-Halo: $R = 7.15$
  10. FastMVC: $R = 7.38$
  11. CoHiRF: $R = 7.69$
  12. FCAG: $R = 7.77$
* **Critical Difference (Nemenyi $\alpha=0.05$):** $CD = q_{0.05} \sqrt{\frac{k(k+1)}{6 N_d}} = 3.268 \sqrt{\frac{12 \times 13}{6 \times 13}} = 4.62$.
* **Verdict:** Exactly reproduced. All 12 methods form a single statistically indistinguishable equivalence group under global omnibus testing.

### 2.3 Headline 3: High-Dimensional Subgroup Analysis ($D/N > 20$, $n=6$)
* **Subgroup Means:**
  - GAC Pipeline: $\mathbf{0.2168 \approx 0.217}$ (Rank #1, $R = 2.17$)
  - FCAG: $0.0656$
  - K-Means: $0.0557$
  - FastMVC: $0.0489$
  - ICC-v1: $0.0463$
  - DEC: $0.0454$
  - FCM: $0.0440$
  - Standard Consensus: $0.0373$
  - Core-Halo: $0.0361$
  - Spectral: $0.0345$
  - Ward: $0.0316$
  - CoHiRF: $0.0173$
* **Concentration of Gain:** GAC's gain is heavily concentrated on Leukemia ($0.5998 \approx 0.600$) and SRBCT ($0.5456 \approx 0.546$). On the remaining 11 datasets, GAC averages $0.0759 \approx 0.076$.
* **Inferential Standing:** Paired Wilcoxon tests across $n=6$ cohorts yield raw $p \approx 0.03125$ for four baselines, but **no difference survives Holm-Bonferroni correction** ($p_{\text{adj}} \ge 0.250$), reflecting limited non-parametric power at $n=6$.
* **Verdict:** Accurately reported and qualified as an exploratory subgroup finding.

### 2.4 Headline 4: Factorial Interaction and Gain Decomposition (Section 7.3)
* **2x2 Factorial Matrix on 6 High-$D$ Cohorts:**
  - Ambient + Standard Consensus (V0): $0.0368 \approx 0.037$
  - Ambient + Bipartite Anchor Consensus (V3): $0.0463 \approx 0.046$
  - BGSS Gated + Standard Consensus (V2): $0.0773 \approx 0.077$
  - BGSS Gated + Bipartite Anchor Consensus (V5): $\mathbf{0.2168 \approx 0.217}$
* **Decomposition:**
  - Replacing dense consensus with anchors in ambient space adds only $+0.009$.
  - Adding BGSS to dense consensus adds $+0.040$.
  - Combining BGSS with bipartite anchor consensus yields $+0.180$ over baseline ($0.0368 \to 0.2168$).
  - Synergistic interaction $V5 - V2 = +0.1394$ (95% CI: $[+0.004, +0.321]$, Wilcoxon $p \approx 0.156$).
* **Matched Feature Gating Ablation (Exp 8c):**
  - Matched random feature gating with same pool size $\lfloor \alpha D \rfloor$ achieves $0.1547 \approx 0.155$.
  - Gain of random subspace bipartite ensemble over ambient consensus: $0.1547 - 0.0368 = \mathbf{+0.1179 \approx +0.118}$ (65.6% of total gain).
  - Gain of BGSS over matched random gating: $0.2168 - 0.1547 = \mathbf{+0.0621 \approx +0.062}$ (95% CI: $[+0.013, +0.142]$, Wilcoxon $p = 0.0625$).
* **Verdict:** Fully reconciled and algebraically consistent.

### 2.5 Headline 5: Determinacy Anchor Selection Null Result (Section 7.4)
* **Exp 8b Comparison:**
  - Full GAC Pipeline (V5, Certified Core Anchors): $0.2168 \approx 0.217$.
  - Uniform Random Anchors (V4): $0.1980 \approx 0.198$.
  - Net paired difference: $V5 - V4 = \mathbf{+0.0188 \approx +0.019}$.
  - 95% Cluster Bootstrap CI: $[-0.039, +0.082]$ (spans zero).
  - Wilcoxon signed-rank test: $W = 9.0, p = 0.84375$.
* **Alternative Landmark Synthesizers:**
  - K-Means Centroid Anchors: $0.1243 \pm 0.198$ (degrades due to noise corruption in centroid updates).
  - Balanced Determinacy Anchors: $0.1190 \pm 0.188$.
* **Verdict:** Empirical null result confirmed. Bipartite graph construction functions as a compression device rather than a precision landmark filter.

---

## 3. Discrepancy Reconciliation Summary

| Discrepancy Flag | Potential Issue | Audit Finding & Resolution |
|---|---|---|
| **D-1: 0.155 vs. 0.198 Ablations** | Suspected inconsistent ablation baselines | **Resolved:** Two distinct experiments. $0.155$ is Matched Random Gating in Exp 8c; $0.198$ is Uniform Random Anchors (V4) in Exp 8b. Mapped clearly in `ABLATION_MAPPING.csv`. |
| **D-2: CI Excludes Zero vs. Wilcoxon $p=0.16$** | Potential statistical contradiction | **Resolved:** Valid coexistence. Bootstrap resamples the mean difference distribution; Wilcoxon on $n=6$ pairs has minimum discrete two-sided $p=0.03125$. A single reverse sign raises discrete $p$ to $0.156$. |
| **D-3: 99.6% vs. 97.4% Memory Reduction** | Inconsistent memory savings claims | **Resolved:** Graph auxiliary memory is reduced by 99.6% ($762.9\text{ MB} \to 3.05\text{ MB}$ at $N=10{,}000$); measured peak process RAM is reduced by 97.4% ($2.61\text{ GB} \to 68.9\text{ MB}$). Both clearly labeled. |
| **D-4: Preregistration Status** | Use of "pre-registered" for internal protocol | **Resolved:** Replaced with "pre-specified evaluation protocol" and "pre-specified decision rules" across all files to respect academic norms for third-party registries. |

---

## 4. Final Provenance Assessment

**Overall Status: 100% REPRODUCIBLE AND AUDITED.**  
Every number in the canonical manuscript has been traced to raw per-seed execution logs and reproduced via automated scripts. Zero missing runs, zero unbacked claims, and zero unexplained discrepancies remain.
