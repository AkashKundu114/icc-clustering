# Pre-registration Fix Pass C: Harmonization, Unified Seeds, & Single Source of Truth

**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Registrant:** Akash Kundu  
**Date:** October 2026  
**Status:** APPROVED & RESOLVED (SUPERSEDED BY PASS F PROTOCOL)  
**Label:** Pre-specified, not blind (all datasets and baseline models are previously known; designed to resolve defects D1 through D9 from Pass C audit).

---

## 1. Motivation and Objectives

Fix Pass C resolves systematic discrepancies (D1, D2, D3, D4, D6) in `main_780366.pdf` caused by fractured legacy scripts, differing random seed sets (`seeds 0..9` vs `[42, 101, ..., 909]`), hardcoded macros in `scripts/make_numbers.py`, and uncoordinated text updates.

To satisfy Research Integrity rules (Rule 1: zero fabricated data/refs; Rule 2: zero hand-edited numbers; Rule 3: zero process notes in manuscript):
1. **Unified Seed Protocol:** Every experiment across all tables and figures will use strictly seeds $s \in \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9\}$ (10 fixed seeds).
2. **Unified Data Architecture:** All results will be saved to `results/passC/`.
3. **Single Programmatic Macro Generator:** `scripts/make_numbers.py` will read exclusively from `results/passC/` artifacts and compute every LaTeX macro dynamically (zero hardcoded string numbers).
4. **Subsampling and Mappings Reconciliation:** Dataset dimensions, labels, and subsampling specs will be harmonized across catalog metadata, code, tables, figures, and manuscript text.

---

## 2. Experimental Design & Pre-Specified Cohorts

### 2.1 Benchmark Cohort (All 13 Datasets)
All 13 benchmark datasets from the unified registry:
1. **CNS:** $N=60, D=7{,}129, K=2$ (Microarray, $D/N=118.8$)
2. **Colon:** $N=62, D=2{,}000, K=2$ (Microarray, $D/N=32.3$)
3. **Indian Pines:** $N=10{,}249, D=200, K=16$ (Hyperspectral AVIRIS, background excluded)
4. **Isolet:** $N=7{,}797, D=617, K=26$ (Spoken Letter Audio)
5. **Leukemia:** $N=72, D=7{,}129, K=2$ (Microarray, $D/N=99.0$)
6. **Madelon:** $N=500, D=500, K=2$ (Synthetic Manifold with distractors)
7. **20 Newsgroups:** Full $N=18{,}846, D=10{,}000, K=20$ (TF-IDF Text; earlier text mentioning subsampling was an errant insertion and is corrected)
8. **Ovarian:** $N=253, D=15{,}154, K=2$ (Mass Spectrometry, $D/N=59.9$)
9. **Prostate:** $N=102, D=12{,}600, K=2$ (Microarray, $D/N=123.5$)
10. **Sonar:** $N=208, D=60, K=2$ (Acoustic Sensing)
11. **SRBCT:** $N=83, D=2{,}308, K=4$ (Genomics, $D/N=27.8$)
12. **Extended Yale B:** Full $N=2{,}414, D=1{,}024, K=38$ (Face Biometrics)
13. **Zheng68k:** Evaluated on standard filtered PBMC subset $N=700, D=765, K=10$ (scRNA-seq; Table 3 will be corrected from catalog $68.6\text{k}$ to explicitly reflect the evaluated $N=700$ subset).

The **High-Dimensional Subgroup ($D/N > 20$)** comprises the 6 biomedical benchmarks: CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT.

### 2.2 Models and Configurations
1. **K-Means:** $k$-means++ initialization, `max_iter=300`, `n_init=10`.
2. **Ward:** Agglomerative clustering with Ward minimum variance criterion.
3. **Spectral:** Normalized graph cut via Scikit-Learn `SpectralClustering`.
4. **FCM:** Fuzzy C-Means ($m=2.0$, max iter 150).
5. **Standard Consensus (Std Cons):** Dense $N \times N$ co-association matrix over $M=25$ base partitions, followed by spectral graph partitioning.
6. **Core-Halo Consensus (Core-Halo):** Determinacy-based core-halo consensus heuristic ($M=25$).
7. **DEC:** Deep Embedded Clustering with autoencoder pretraining + student-t self-training.
8. **FCAG:** Fast bipartite anchor graph ensemble ($L=40, M=25$).
9. **FastMVC:** Fast multi-view anchor consensus ($L=40, M=25$).
10. **ICC-v1:** Bipartite anchor consensus on ambient features without BGSS gating ($L=40, M=25$).
11. **ICC-v2 (Ours):** BGSS feature selection ($\alpha=0.15, \min=100$), Determinacy Core certified anchors ($L=40, \tau_{\text{core}}=0.50$), bipartite Transfer-Cut embedding ($M=25$), stability-weighted inductive centroids.

---

## 3. Pre-Specified Sub-Experiments

### 3.1 Task C1: Benchmark Matrix (Table 3, Fig 6, Fig 7)
- Run all 13 datasets $\times$ 11 methods $\times$ 10 seeds ($s \in \{0, \dots, 9\}$) = 1,430 fits.
- Compute Adjusted Rand Index (ARI) and Normalized Mutual Information (NMI).
- Output: `results/passC/benchmark_13x11.csv`.
- Metrics: Mean $\pm$ SD and Median per dataset/method.
- Statistical Tests: Friedman omnibus test across 13 datasets; Nemenyi Critical Difference with exact formula $CD = q_{0.05} \sqrt{\frac{k(k+1)}{6N}} = 3.219 \sqrt{\frac{11 \times 12}{6 \times 13}} = 4.19$ ($k=11, N=13$).

### 3.2 Task C1 / Task B8: Fair High-Dimensional Baseline Suite (Table 4)
- Run on the 6 high-D datasets ($D/N > 20$) over seeds $s \in \{0, \dots, 9\}$.
- Feature budget for all baselines: $|\mathcal{F}_{\text{active}}| = \min(D, \max(K, \lfloor 0.15 D \rfloor))$.
- Evaluated methods:
  - K-Means (Ambient)
  - K-Means (Variance Filtered)
  - K-Means (PCA / Truncated SVD, $d=\min(N-1, 50)$)
  - K-Means (Laplacian Score)
  - Sparse K-Means (Witten & Tibshirani 2010)
  - Std Cons (Ambient)
  - Std Cons (Variance Filtered)
  - Std Cons (PCA)
  - ICC-v2 (Ours)
- Output: `results/passC/fair_baselines.csv`.

### 3.3 Task C4: Ablation Suite & Anchor Certification (Table 2, Fig 5)
- Run 6 ablation variants on the 6 high-D datasets over seeds $s \in \{0, \dots, 9\}$:
  - V0: Ambient Dense Consensus
  - V1: BGSS + K-Means
  - V2: BGSS + Dense Consensus
  - V3: Ambient Bipartite Anchor Consensus
  - V4: BGSS + Random Anchor Consensus
  - V5: Full ICC-v2 (BGSS + Determinacy Core Anchors)
- Output: `results/passC/ablation_variants.csv`.
- Compute bootstrap 95% confidence intervals (1,000 resamples) for $\Delta(\text{V5} - \text{V4})$ and $\Delta(\text{V5} - \text{V2})$.
- Report overlapping CIs truthfully: certified anchors show modest gains on average, but do not statistically dominate random anchors across all datasets.
- Explicitly disclose and discuss bimodal seed behavior on Leukemia and below-baseline performance on Prostate.

### 3.4 Task C3: Unified Efficiency & Scalability Suite (Exp 4.3, Fig 8)
- Benchmark synthetic samples $N \in [200, 500, 1000, 2000, 5000, 10000]$ with fixed $D=500, K=5$, over 5 random seeds.
- Measure:
  - Peak Dynamic RAM (MB) via `tracemalloc`.
  - Wall-clock runtime (s) for Std Cons vs ICC-v2.
- Scaling test at $N=50{,}000$: verify empirical runtime and memory.
- Synchronize all efficiency claims across Abstract, Section 5.3, Table, and Fig 8 caption.
- Output: `results/passC/efficiency.csv`.

### 3.5 Task C6: Direct Inductive Inference Suite (Section 5.3, Table 5)
- Run held-out inductive test splits (80% train, 20% test) on Leukemia and SRBCT across 10 seeds ($s \in \{0, \dots, 9\}$).
- Compare:
  - Direct Centroid Assignment ($O(K \cdot |\mathcal{F}_{\text{active}}|)$)
  - Full Transductive Refit
  - Nyström Spectral Extension
  - $k$-Nearest Neighbors ($k\text{NN}$) in ambient space
- Output: `results/passC/inductive_direct.csv`.

---

## 4. Execution Plan & Hardware Safeguards

- **Hardware:** NVIDIA GeForce RTX 5060 Laptop GPU (8GB VRAM), Intel Core i7 (16 cores), 16GB RAM.
- **Worker Policy:** `n_workers = 2` to prevent memory thrashing and disk saturation.
- **Verification Script:** `scripts/make_numbers.py` dynamically compiles `results/passC/numbers.tex`.
- **Zero Hardcoding Guarantee:** All numeric values in `springer_manuscript/main.tex` must be macro references generated by `make_numbers.py`.

---

## 5. Human Gate A Checkpoints

Prior to executing the heavy benchmark scripts, the user must review and approve:
1. **Dataset Dimensions & Subsampling:** Zheng68k confirmed as $N=700$ filtered subset; 20 Newsgroups ($N=18{,}846$) and Yale B ($N=2{,}414$) evaluated on full sets.
2. **Unified Seeds:** Strictly seeds $0..9$ across all sub-experiments.
3. **Hardware Policy:** Concurrency bounded to 2 workers.
