# Pre-registration Fix Pass B: Real-Data High-D Ablations & Fair Baselines

**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Registrant:** Akash Kundu  
**Date:** October 2026  
**Status:** APPROVED BY HUMAN AUTHOR (GATE A)  
**Label:** Pre-specified, not blind (empirical datasets and initial benchmarks are previously known).

---

## 1. Context and Objective
In Fix Pass B, two empirical components require formal pre-specification prior to computational execution:
1. **Task B6: 2x2 Factorial Ablation + Anchor Selection on $D/N > 20$ Benchmarks**
   - Disentangles the individual and interaction effects of:
     - Factor 1: BGSS feature gating (Active Subspace vs. Full Ambient Features).
     - Factor 2: Bipartite Spectral Anchor Consensus vs. Standard Consensus / K-Means.
     - Factor 3: Anchor Selection Strategy (Determinacy Core Certified Anchors vs. Uniform Random Anchors vs. K-Means Centroid Anchors).
2. **Task B8: Fair High-Dimensional Baseline Suite**
   - Evaluates standard clustering architectures (K-Means, Standard Consensus, Sparse K-Means) under identical feature budgets ($|F_{\text{active}}|$) matched directly to ICC-v2 candidate selection.

---

## 2. Pre-Specified Benchmark Cohort ($D/N > 20$)
The evaluation is pre-specified on the 6 biomedical benchmarks satisfying $D/N > 20$:
1. **CNS:** $N=60, D=7{,}129, K=2$ ($D/N = 118.8$)
2. **Colon:** $N=62, D=2{,}000, K=2$ ($D/N = 32.3$)
3. **Leukemia:** $N=72, D=7{,}129, K=2$ ($D/N = 99.0$)
4. **Ovarian:** $N=253, D=15{,}154, K=2$ ($D/N = 59.9$)
5. **Prostate:** $N=102, D=12{,}600, K=2$ ($D/N = 123.5$)
6. **SRBCT:** $N=83, D=2{,}308, K=4$ ($D/N = 27.8$)

---

## 3. Pre-Specified Experimental Design

### 3.1 Task B6: 2x2 Factorial Ablation & Anchor Mechanics
For each of the 6 datasets and each seed $s \in \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9\}$ (10 fixed seeds):
- **Cell (0, 0): Ambient K-Means** (No gating, full $D$ features, single model).
- **Cell (1, 0): BGSS + K-Means** (BGSS candidate pool $\mathcal{F}_{\text{active}}$, single model; Control 1 / V1).
- **Cell (0, 1): Ambient Consensus** (No gating, full $D$ features, dense co-association / V0).
- **Cell (1, 1a): BGSS + Dense Consensus** (BGSS candidate pool, dense co-association / V2).
- **Cell (1, 1b): BGSS + Random Anchors** (BGSS candidate pool, bipartite anchor consensus with uniform random anchors / V4).
- **Cell (1, 1c): BGSS + K-Means Anchors** (BGSS candidate pool, bipartite anchor consensus with K-Means centroids as anchors).
- **Cell (1, 1d): Full ICC-v2** (BGSS candidate pool, determinacy core certified anchors, bipartite Transfer-Cut / V5).

**Hyperparameters:**
- Base clusterers $M = 25$.
- Anchor budget $L = 40$.
- Candidate pool fraction $\alpha = 0.15$ with minimum cap $\min(100, D)$.
- Determinacy core quantile $\tau_{\text{core}} = 0.50$.

### 3.2 Task B8: Matched-Feature Fair Baselines
To eliminate the confounder of feature dimensionality, baselines are provided with exactly the same active feature budget $|\mathcal{F}_{\text{active}}| = \min(D, \max(K, \lfloor 0.15 D \rfloor))$:
1. **K-Means (All Features):** Raw ambient space $D$.
2. **K-Means (Variance Filtered):** Top $|\mathcal{F}_{\text{active}}|$ highest variance features.
3. **K-Means (Truncated SVD / PCA):** Top $d = \min(N-1, 50)$ components.
4. **K-Means (Laplacian Score):** Top $|\mathcal{F}_{\text{active}}|$ unsupervised graph-preserving features.
5. **Sparse K-Means (Witten & Tibshirani 2010):** $L_1$ penalized feature weights with permutation-tuned sparsity parameter $s$.
6. **Standard Consensus (All Features):** Dense co-association on full $D$.
7. **Standard Consensus (Variance Filtered):** Dense co-association on top $|\mathcal{F}_{\text{active}}|$ variance features.
8. **Standard Consensus (PCA):** Dense co-association on top $d = \min(N-1, 50)$ components.
9. **ICC-v2 (Ours):** Full ICC-v2 on same candidate features.

**Seeds:** Fixed seeds $s \in \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9\}$.

---

## 4. Primary Metrics and Decision Rules
- **Primary Metric:** Adjusted Rand Index (ARI) against ground-truth classes.
- **Secondary Metric:** Normalized Mutual Information (NMI).
- **Decision Rules:**
  1. All 10 seeds are reported as Mean $\pm$ Standard Deviation and Median.
  2. Subgroup mean and median ARI are computed strictly across all 6 datasets without omitting negative or near-zero outcomes.
  3. Every number reported in the text and tables must be generated directly by automated scripts into `springer_manuscript/numbers.tex`.
  4. Unfavourable and null results (e.g. failure to achieve statistically significant separation under Holm-adjusted Wilcoxon testing) will remain fully disclosed in the manuscript.

---

## 5. Execution Environment & Safety Guardrails
- **Host Hardware:** NVIDIA GeForce RTX 5060 Laptop GPU (8GB VRAM), Intel Core i7 CPU (16 cores), 16GB RAM.
- **Concurrency Policy:** `n_workers = 2`, avoiding RAM/SSD thrashing.
- **Execution Target:** Scripts located in `experiments/` and `scripts/`. Output artifacts stored in `results/passB/`.
