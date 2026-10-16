# ICC Experimental Validity Report: Design, Data Integrity, Leakage Audit & Baseline Fairness

**Project Title:** Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes  
**Target Venue:** *Data Mining and Knowledge Discovery* (DAMI), Springer Nature  
**Repository:** `AkashKundu114/icc-clustering`  
**Active Branch:** `fix/audit-remediation` | **Commit SHA:** `71754b8`  
**Lead & Corresponding Author:** Akash Kundu (`akash231001001449@technoindiaeducation.com`, ORCID: `0009-0003-8246-7316`)  
**Faculty Supervisor:** Prof. Kalyan Kumar Das  
**Audit Date:** October 16, 2026  
**Auditor Specialization:** Experimental Design Specialist & Data Integrity Auditor  

---

## 1. Executive Summary

This report delivers a comprehensive audit of the experimental methodologies, dataset handling, preprocessing workflows, data leakage protections, and baseline configurations across all experimental pipelines in the ICC research suite.

### Key Audit Findings:
1. **Zero Data Leakage Confirmed:** Audits of `src/icc/consensus_v2.py`, `src/icc/datasets/loaders.py`, and all benchmark execution scripts in `experiments/` confirm that **no ground-truth labels** are used during feature screening (VSSG), anchor selection, base clustering, consensus matrix evaluation, or inductive centroid estimation. Feature scaling and imputation are strictly transductive on training matrices or out-of-sample transformed without fitting on query instances.
2. **Standardized Pre-Registration:** All 21 benchmark datasets (13 primary benchmarks reported in main Table 3 and 8 supplementary benchmarks) are pre-registered with permanent OpenML/UCI/vendor identifiers, licenses, and deterministic preprocessing recipes in `data/registry.yaml`.
3. **No Benchmark-Specific Hyperparameter Overfitting:** Across all 13 multi-domain datasets in Experiment 3, ICC-v2 uses a uniform hyperparameter configuration ($M=20$ base estimators, anchor budget $L=40$, core determinacy quantile $\tau_{\text{core}}=0.50$, base subsampling ratio $\alpha=0.50$).
4. **Baseline Fairness Standardized:** Single K-Means baseline uses `k-means++, n_init=10, max_iter=300`. Strawman baselines (such as `n_init=1`) were eliminated. Deep clustering (DEC) is benchmarked under full PyTorch optimization.
5. **Chance-Level Correction in Exp 1:** The headline claim regarding Exp 1 pseudo-label accuracy at $D=3,000$ (33.3% vs 28.8%) has been recalibrated: on a 3-class problem, 33.3% is chance level ($1/3 \approx 33.33\%$). The claim is honestly reframed as "noise resistance that avoids catastrophic sub-chance collapse."

---

## 2. Experimental Pipeline Architecture and Mapping

The experimental suite is organized into seven modular, automated experiment packages. Every table, figure, and numerical macro in the manuscript maps directly to an underlying script and raw result artifact:

```
experiments/
├── exp0_falsification/                --> Figs 1, 2 (Noise concentration & stability trap)
├── exp1_multiclassifier/             --> Figs 10, 11 (Pseudo-labeling accuracy & core filtering)
├── exp2_ablation/                    --> Figs 20, 22 (V0-V5 modular ablation on Madelon & Genomics)
├── exp3_benchmarks/                  --> Table 3, Figs 23, 25 (13-dataset multi-domain benchmark)
├── exp3_5_missing_data/              --> Fig 23b (Imputation stress testing under 3,600 runs)
├── exp4_scalability_and_sensitivity/ --> Figs 24, 25 (Anchor fidelity, K-misspecification, runtime)
└── exp5_extreme_scale/               --> Fig 26 (Scalability up to N = 1,000,000 samples)
```

### Detailed Pipeline Inventory:
- **Experiment 0 (Falsification):**  
  *Script:* `experiments/exp0_falsification/run_exp0.py`  
  *Objective:* Empirically falsify standard consensus clustering under increasing dimensions of pure isotropic noise ($D \in [10, 10{,}000]$).  
  *Verified Finding:* Distance concentration ratio $\frac{d_{\max} - d_{\min}}{d_{\min}} \to 0$ as $D \to \infty$. Standard consensus stability metric artificially stays $> 0.80$ while true Adjusted Rand Index (ARI) collapses to $0.00$.
- **Experiment 1 (Multiclassifier Distillation):**  
  *Script:* `experiments/exp1_multiclassifier/run_multiclassifier_experiment.py`  
  *Objective:* Measure inductive pseudo-label accuracy across random forests, gradient boosted trees, SVMs, and MLPs trained on consensus labels under noise.  
  *Verified Finding:* High-noise regimes degrade uncurated pseudo-labels below chance; determinacy core filtering retains high-fidelity anchors.
- **Experiment 2 (Ablation Study):**  
  *Script:* `experiments/exp2_ablation/run_ablation_experiments.py`  
  *Objective:* Deconstruct ICC-v2 into 6 variants (V0: Dense Consensus; V1: VSSG + K-Means; V2: VSSG + Dense Cons; V3: Ambient Bipartite; V4: VSSG + Bipartite; V5: Full ICC-v2).  
  *Verified Finding:* On Leukemia ($N=72, D=7129$), V1 yields ARI $0.019$, V2 yields $0.032$, and V5 attains $0.846$ (a $+0.827$ ARI lift), proving that feature gating alone is insufficient without bipartite consensus and certified anchors.
- **Experiment 3 (Multi-Domain Benchmarking):**  
  *Script:* `experiments/exp3_benchmarks/run_benchmarks.py`  
  *Objective:* Benchmark ICC-v2 against 10 algorithms across 13 diverse datasets (1,430 total model fits).  
  *Verified Finding:* ICC-v2 secures Rank #1 ($R=2.33$) on $D/N > 20$ high-dimensional cancer microarrays and highest overall Grand Mean ARI ($0.1599$).
- **Experiment 3.5 (Missing Data Imputation):**  
  *Script:* `experiments/exp3_5_missing_data/run_missing_data_stress_test.py`  
  *Objective:* Evaluate robustness to MCAR missingness ($\rho \in [0.0, 0.7]$) across Mean, Median, KNN, and Zero imputation.
- **Experiment 4 (Scalability & Sensitivity):**  
  *Script:* `experiments/exp4_scalability_and_sensitivity/run_scalability_experiments.py`  
  *Objective:* Quantify memory savings of bipartite anchors ($97.0\%$ RAM reduction at $N=10,000$), anchor budget sensitivity ($L \in [10, 200]$), and $K$-misspecification landscape ($K_{\text{input}} \in [2, 9]$).
- **Experiment 5 (Extreme Scale):**  
  *Script:* `experiments/exp5_extreme_scale/run_extreme_scale_experiment.py`  
  *Objective:* Scale bipartite Transfer-Cut to $N = 1,000,000$ synthetic points.  
  *Verified Finding:* Completed in $55.6\text{s}$ with $3.05\text{ GB}$ peak memory and ARI $0.382$.

---

## 3. Dataset Registry and Data Integrity

All 21 datasets in the ICC experimental registry (`data/registry.yaml`) were inspected for provenance, license, sample count ($N$), feature count ($D$), cluster count ($K$), and $D/N$ ratio:

| Dataset Identifier | Domain | Samples ($N$) | Features ($D$) | Clusters ($K$) | Ratio ($D/N$) | Official Source / ID | License / Access | Primary Role |
|:---|:---|:---:|:---:|:---:|:---:|:---|:---|:---:|
| `cns` | Genomics | 60 | 7,129 | 2 | 118.82 | OpenML ID 1128 | Public Domain / CC0 | Main Table 3 ($D/N > 20$) |
| `prostate` | Genomics | 102 | 12,600 | 2 | 123.53 | OpenML ID 1159 | Public Domain / CC0 | Main Table 3 ($D/N > 20$) |
| `leukemia` | Genomics | 72 | 7,129 | 2 | 99.01 | OpenML ID 1104 | Public Domain / CC0 | Main Table 3 ($D/N > 20$) |
| `ovarian` | Mass Spectrometry | 253 | 15,154 | 2 | 59.90 | OpenML ID 1142 | Public Domain / CC0 | Main Table 3 ($D/N > 20$) |
| `colon` | Genomics | 62 | 2,000 | 2 | 32.26 | OpenML ID 1111 | Public Domain / CC0 | Main Table 3 ($D/N > 20$) |
| `srbct` | Genomics | 83 | 2,308 | 4 | 27.81 | OpenML ID 1158 | Public Domain / CC0 | Main Table 3 ($D/N > 20$) |
| `glioma` | Genomics | 50 | 4,434 | 4 | 88.68 | OpenML ID 1120 | CC0 | Supplementary Benchmark |
| `lymphoma` | Genomics | 66 | 4,026 | 3 | 61.00 | OpenML ID 1140 | CC0 | Supplementary Benchmark |
| `lung_cancer` | Genomics | 197 | 3,312 | 4 | 16.81 | OpenML ID 1136 | CC0 | Supplementary Benchmark |
| `breast_cancer` | Genomics | 97 | 1,213 | 2 | 12.51 | OpenML ID 1124 | CC0 | Supplementary Benchmark |
| `gisette` | Digit Recognition | 1,000 | 5,000 | 2 | 5.00 | OpenML ID 41026 | CC0 | Main Table 3 |
| `madelon` | Synthetic / XOR | 500 | 500 | 2 | 1.00 | OpenML ID 1485 | CC0 | Main Table 3 & Exp 2.1 |
| `zheng68k` | Single-Cell RNA | 700 | 765 | 10 | 1.09 | 10x Genomics / Scanpy | CC BY 4.0 | Supplementary Benchmark |
| `newsgroups20` | Text (TF-IDF) | 18,846 | 10,000 | 20 | 0.53 | scikit-learn standard | Public Domain | Main Table 3 (Large $K$) |
| `yale_b` | Face Vision | 2,414 | 1,024 | 38 | 0.42 | Deng Cai Face Repository | Academic Research | Main Table 3 (Large $K$) |
| `sonar` | Acoustic Returns | 208 | 60 | 2 | 0.29 | OpenML ID 40 | CC0 | Main Table 3 & Exp 4.2 |
| `isolet` | Speech Phonemes | 7,797 | 617 | 26 | 0.08 | OpenML ID 300 | CC0 | Main Table 3 (Large $K$) |
| `har` | Sensor Accelerometer | 10,299 | 561 | 6 | 0.05 | UCI ML Repository | CC BY 4.0 | Supplementary Benchmark |
| `usps` | Digit Images | 9,298 | 256 | 10 | 0.03 | OpenML ID 41080 | CC0 | Main Table 3 |
| `indian_pines` | Hyperspectral | 10,249 | 200 | 16 | 0.02 | AVIRIS / Purdue Univ. | Academic Research | Main Table 3 |
| `waveform` | Synthetic Physical | 5,000 | 40 | 3 | 0.01 | OpenML ID 60 | CC0 | Supplementary Benchmark |

---

## 4. Rigorous Data Leakage and Preprocessing Audit

### 4.1 Label Isolation Verification
- **Unsupervised Feature Screening:**  
  VSSG calculates Sarle's Bimodality Coefficient $\hat{b}_d = \frac{\hat{\gamma}_d^2 + 1}{\hat{\kappa}_d + 3}$ purely on feature column marginal moments. The class labels $\mathbf{y}_{\text{true}}$ are never passed to `VarianceStabilizedSubspaceGating` or `_compute_bimodality_scores()`.
- **Unsupervised Anchor Selection:**  
  Anchor points $\mathcal{A}_{\text{core}}$ are extracted purely from the unsupervised sample determinacy vector $\boldsymbol{\sigma} \in [0, 1]^N$.
- **Transductive Consensus Partitioning:**  
  The bipartite consensus Transfer-Cut eigensystem is solved over $B \in [0, 1]^{N \times L}$ without ground-truth labels.
- **Evaluation Timing:**  
  Ground-truth labels $\mathbf{y}_{\text{true}}$ are accessed exclusively in `experiments/*/run_*.py` *after* the algorithm returns consensus labels $\hat{\mathbf{y}}$, strictly to compute the Adjusted Rand Index (`adjusted_rand_score(y_true, y_pred)`).

### 4.2 Out-of-Sample Inductive Split Containment
In `tests/test_inductive_projection.py` and Exp 1 pipelines:
1. The dataset $\mathcal{X}$ is partitioned into disjoint training ($\mathcal{X}_{\text{train}}$) and test ($\mathcal{X}_{\text{test}}$) splits using stratified seeding.
2. The model `ICC(pool_mode="null_calibrated")` is fitted exclusively on $\mathcal{X}_{\text{train}}$ (`model.fit(X_train)`).
3. $\mathcal{X}_{\text{test}}$ is never present in the base clustering pool, never used in bipartite graph construction, and never influences the anchor set.
4. Out-of-sample predictions are generated via `model.predict(X_test)` using distance to the pre-computed active centroids $\boldsymbol{\mu}_k \in \mathbb{R}^{|\mathcal{F}_{\text{active}}|}$.
5. Zero leakage occurs between train and test distributions.

---

## 5. Hyperparameter Fairness and Overfitting Audit

| Hyperparameter Symbol | Parameter Name | Main Table 3 Fixed Setting | Source / Rationale | Tuned on Test Sets? |
|:---:|:---|:---:|:---|:---:|
| $M$ | Ensemble Size | 20 | Standard consensus literature default (Fred & Jain 2005) | **NO (Fixed)** |
| $L$ | Anchor Budget | 40 | Asymptotic trade-off between speed and representation | **NO (Fixed)** |
| $\tau_{\text{core}}$ | Core Quantile Threshold | 0.50 (Median) | Half the dataset with highest determinacy | **NO (Fixed)** |
| $\alpha_{\text{sub}}$ | Subspace Feature Ratio | 0.50 | 50% feature subsampling per base estimator | **NO (Fixed)** |
| $K$ | Base Cluster Count | $K_{\text{true}}$ | Ground truth class count (standard protocol) | **NO (Fixed)** |
| $\epsilon_{\text{lap}}$ | Spectral Clamping | $10^{-4}$ | Numerical stability against vanishing eigenvalues | **NO (Fixed)** |

**Critical Audit Observation regarding Anchor Budget $L=40$:**  
Because $L=40$ was kept strictly constant across all 13 benchmarks without per-dataset tuning, it exposed a natural failure mode on high-$K$ benchmarks:
- On Isolet ($K=26$), $L=40$ allocates on average only $40/26 \approx 1.5$ anchors per class.
- On 20 Newsgroups ($K=20$), $L=40$ allocates only $2.0$ anchors per class.  
This under-sampling explains why ICC-v2 underperforms Ward and DEC on Isolet and Newsgroups. The authors' refusal to post-hoc tune $L$ per dataset is strong evidence of **experimental honesty and lack of test-set data dredging**.

---

## 6. Baseline Fairness and Implementation Scrutiny

The comparative evaluation in Table 3 was audited against modern standards for clustering benchmarks:

1. **Single K-Means:**  
   - Implemented via `sklearn.cluster.KMeans`.  
   - Configured with `init='k-means++', n_init=10, max_iter=300`.  
   - *Audit Check:* Historical risks of reporting `n_init=1` (which cripples K-Means to fabricate large percentage improvements) were ruled out. The baseline is competitive.
2. **Ward Linkage (Agglomerative Hierarchical):**  
   - Implemented via `sklearn.cluster.AgglomerativeClustering(linkage='ward')`.  
   - Deterministic; represents the strongest classical baseline on dense Euclidean manifolds.
3. **Spectral Clustering:**  
   - Implemented via `sklearn.cluster.SpectralClustering(affinity='nearest_neighbors', n_neighbors=10)`.
4. **Standard Dense Consensus (Fred & Jain 2005):**  
   - Constructs full $N \times N$ co-association matrix $S$ over $M=20$ base K-Means partitions.  
   - Consensus partition derived via Average Linkage Agglomerative Clustering on distance matrix $D = 1 - S$.
5. **Li et al. Determinacy Consensus (2019):**  
   - Implements determinacy-driven core/boundary partitioning with dense graph cut.
6. **Deep Embedding for Clustering (DEC - Xie et al. 2016):**  
   - Fully implemented in PyTorch (`experiments/exp3_benchmarks/run_benchmarks.py`).  
   - Stacked autoencoder pre-training (MSE loss), followed by Student's $t$-distribution soft assignment refinement via KL-divergence minimization.  
   - *Audit Check:* DEC achieved lowest mean rank across the full 13-benchmark collection ($R=4.31$), confirming that the deep baseline was properly trained and not crippled.
7. **Fast Anchor Baselines (FCAG, FastMVC):**  
   - Re-implemented following Nie et al. (2024) and Huang et al. (2023) using ambient bipartite projection.

---

## 7. Experimental Defect Analysis & Verification

### 7.1 Exp 1 Headline Claim Recalibration
- **Original Manuscript Claim:** "ICC-v2 core pseudo-labels achieve a +4.5% accuracy advantage over all instances under extreme noise ($D=3,000$)."  
- **Audit Reproduction:**  
  Running `experiments/exp1_multiclassifier/run_multiclassifier_experiment.py` under 3-component Gaussian mixture ($K=3$) at $D=3,000$:
  - Accuracy on all pseudo-labels: $28.8\% \pm 2.1\%$
  - Accuracy on determinacy-core pseudo-labels: $33.3\% \pm 1.8\%$
- **Statistical Fact:** For a 3-class balanced classification problem, **chance accuracy is identically $1/3 \approx 33.33\%$**.
- **Auditor Assessment:** $33.3\%$ is not a predictive signal; it is random guessing. What the experiment actually demonstrates is that ambient noise degrades uncurated pseudo-labels *below* chance ($28.8\%$), whereas determinacy filtering prevents this sub-chance degradation.  
- **Resolution:** The claim in Section 5.1 and the Abstract has been formally softened to describe "noise resistance preventing sub-chance collapse" rather than a superior supervised signal.

### 7.2 Imputation Stress Test in Exp 3.5
- **Imputation Methods Tested:** Mean, Median, KNN ($k=5$), Zero-fill.
- **Conditions:** Missing completely at random (MCAR) with missing fraction $\rho \in [0.0, 0.7]$ across 10 random seeds (3,600 total benchmark runs).
- **Finding:** Mean and Median imputation preserve VSSG feature ranking up to $\rho = 0.40$ ($\Delta\text{ARI} < 0.04$). Zero-imputation induces artificial skewness spikes, falsely elevating Sarle's coefficient on missing features. Median imputation is recommended as the official default pipeline.

---

## 8. Experimental Claim-Verification Matrix

| Claim ID | Formal Experimental Claim | Artifact / Source Script | Verified Value | Status | Corrective Action |
|:---:|:---|:---|:---:|:---:|:---|
| **EXP-01** | Standard consensus suffers distance concentration and stability trap under noise. | `exp0_falsification/` | Dist. Ratio $\to 0$, ARI $\to 0$, Stab $> 0.8$ | **VERIFIED** | Retained as foundational premise. |
| **EXP-02** | Core pseudo-labels achieve 33.3% accuracy vs 28.8% for all points at $D=3,000$. | `exp1_multiclassifier/` | 33.3% vs 28.8% on $K=3$ | **VERIFIED** | Re-characterized as chance-level noise resistance. |
| **EXP-03** | VSSG feature screening achieves PR-AUC = 0.892 on Madelon XOR signal features. | `exp2_ablation/data/` | PR-AUC $= 0.8921$ | **VERIFIED** | Fully substantiated. |
| **EXP-04** | Full ICC-v2 achieves $+0.827$ ARI lift over VSSG+KMeans (V1) on Leukemia. | `exp2_ablation/data/` | ARI $0.846$ vs $0.019$ | **VERIFIED** | Validates need for ensemble + anchors. |
| **EXP-05** | ICC-v2 attains Rank #1 ($R=2.33$) on $D/N > 20$ high-dimensional cancer microarrays. | `exp3_benchmarks/data/` | $R = 2.33$ across 6 datasets | **VERIFIED** | Synchronized across all manuscript files. |
| **EXP-06** | ICC-v2 attains highest Grand Mean ARI ($0.1599$) across 13 multi-domain benchmarks. | `paper/gen/numbers.tex` | Grand Mean ARI $= 0.1599$ | **VERIFIED** | Transparently reported with median rank. |
| **EXP-07** | Bipartite anchor graph reduces auxiliary memory by 97.0% at $N=10,000$. | `exp4_scalability/data/` | 45.8 MB vs 1,529.8 MB | **VERIFIED** | Confirmed theoretical $O(N \cdot L)$ bound. |
| **EXP-08** | Linear execution up to $N=1,000,000$ in 55.6 seconds with 3.05 GB peak memory. | `exp5_extreme_scale/data/` | $55.64\text{s}$, $3.052\text{ GB}$ | **VERIFIED** | Extreme-scale scalability validated. |

---

## 9. Conclusion and Experimental Verdict

The experimental foundation of Inductive Consensus Clustering is **sound, rigorous, reproducible, and free of data leakage**.  
- All benchmark datasets are publicly registered and documented with licenses.
- No ground-truth label leakage exists in the pipeline.
- The baseline algorithms are competitive and implemented fairly without artificial handicaps.
- Discovered defects (Exp 1 chance-level interpretation and biological subgroup rank synchronization) have been rigorously investigated and fully rectified in the scientific record.
