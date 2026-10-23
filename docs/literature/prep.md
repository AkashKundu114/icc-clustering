# Research Preparation & Algorithmic Foundations Dossier (CSE_PROJECT_68)

**Course / Degree Project (Original Allotment):** *Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data* (`CSE_PROJECT_68`)  
**Early Proposal Blueprint Title (Capstone Proposal):** *Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes*  
**Canonical Manuscript Title (Springer Nature DAMI):** *When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination*  
**Algorithmic Framework / Package:** Inductive Consensus Clustering / Invariant Core Consensus (ICC-v2, v2.1.0) and `cicc` (Conformal Inductive Consensus Clustering)  
**Team Members:** Akash Kundu (Lead), Trinankur Guha, Rupankar Ghatak, Anubhav Naskar  
**Faculty Mentor:** Prof. Kalyan Kumar Das  
**Department:** Computer Science and Engineering  
**Target Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI), document class `sn-jnl.cls` (`sn-mathphys-num.bst`), manuscript `paper/main.tex`.  
**Canonical Release Version:** v2.1.0  

---

## 1. Project Deconstruction & Theoretical Paradigm

Standard undergraduate engineering projects assemble off-the-shelf components into an end-to-end classification pipeline (e.g., standard data ingestion -> scikit-learn K-Means -> Random Forest -> UI). This project explicitly **rejects that paradigm**. In accordance with our mentor's directives, our objective was to formulate, mathematically audit, implement, and benchmark a **foundational scientific invention**: **Dual-Space Invariant Core Consensus (ICC-v2)**.

The research title contains four load-bearing scientific concepts:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   FOUR LOAD-BEARING PILLARS                                      │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
  1. CLUSTER STABILITY:
     Perturbation invariance across bootstrap resamples, random seeds, and subspace projections.
     Quantified via pairwise co-association determinacy, not assumed.
  
  2. ENSEMBLE CONSENSUS:
     Fusing diverse, imperfect base partitions into an optimal consensus partition that provably
     outperforms any single constituent model.
  
  3. NOISY DATA REGIMES:
     Manifolds corrupted by high-variance continuous feature noise, irrelevant distractor coordinates,
     outliers, and missing data (MCAR).
  
  4. ULTRA-HIGH DIMENSIONALITY (D >> N):
     Manifolds where pairwise distances concentrate (Beyer et al., 1999), causing Euclidean distances
     to degenerate and classical clustering models to collapse into identical noise artifacts.
```

The core research question investigated is:
> *When does feature gating and anchor consensus improve high-dimensional clustering, and what are the exact operating boundaries where it succeeds vs fails?*

---

## 2. Fulfillment of the Mentor's Directives (Points 1, 2, and 5)

Our research centers strictly around the three foundational pillars emphasized by Prof. Kalyan Kumar Das:

```
====================================================================================================
                        INVARIANT CORE CONSENSUS (ICC-v2) ARCHITECTURAL PIPELINE
====================================================================================================

 [ PILLAR 1: POINT 1 ]          [ PILLAR 2: POINT 2 ]                 [ PILLAR 3: POINT 5 ]
 NOISE-AWARE BASE CLUSTERING    EXACT LINEAR DETERMINACY &            MULTI-DOMAIN BENCHMARKING,
 VIA VSSG MULTIMODALITY         REDUCED BIPARTITE TRANSFER-CUT        AUDIT CONTROLS & GENERALIZATION
 ───────────────────────────    ──────────────────────────────        ───────────────────────────────
 ┌─────────────────────────┐    ┌────────────────────────────┐        ┌─────────────────────────────┐
 │ Input Data X (N x D)    │    │ Base Partitions {Π^(m)}    │        │ Consensus Graph S*          │
 │ D >> N, Noisy Manifolds │    │ Variational Subspaces      │        │ Invariant Core Anchors L    │
 └───────────┬─────────────┘    └─────────────┬──────────────┘        └──────────────┬──────────────┘
             │                                │                                      │
             ▼                                ▼                                      ▼
 ┌─────────────────────────┐    ┌────────────────────────────┐        ┌─────────────────────────────┐
 │ Finite-Sample Sarle BC  │    │ Contingency Tensor Identity│        │ Downstream Inductive Margin │
 │ Null Threshold BC > 5/9 │───►│ Exact Linear Determinacy:  │───────►│ Generalization on Core      │
 │ Candidate Subspace Pool │    │ σ_i in O(M^2 N + M^2 K^2)  │        │ (SVM / RF / KNN / MLP)      │
 └───────────┬─────────────┘    └─────────────┬──────────────┘        └──────────────┬──────────────┘
             │                                │                                      │
             ▼                                ▼                                      ▼
 ┌─────────────────────────┐    ┌────────────────────────────┐        ┌─────────────────────────────┐
 │ M Diverse Base Models   │    │ Bipartite Transfer-Cut:    │        │ ASPP Stability Diagnostics  │
 │ Subspace Feature Proj.  │    │ Solve L x L Anchor System  │        │ 5 Perturbation Families     │
 │ Diversity Repulsion     │    │ Scalable Linear Runtime    │        │ Certified PSI_k Metrics     │
 └─────────────────────────┘    └────────────────────────────┘        └─────────────────────────────┘
====================================================================================================
```

### 2.1 Pillar 1 (Point 1): Noise-Aware Base Clustering via Variance-Stabilized Subspace Gating (VSSG / BGSS)
- **Theoretical Flaw in Prior Work:** Random subspace sampling (Jing et al., 2015) in $D \gg N$ spaces draws $>90\%$ pure noise coordinates with near certainty. Classical feature selection relying on Euclidean metrics collapses due to distance concentration.
- **The ICC-v2 Formulation:** We screen features using the **finite-sample corrected Sarle Bimodality Coefficient**:
  $$BC(\mathbf{f}_d) = \frac{g_{1, d}^2 + 1}{g_{2, d} + 3 \cdot c_N + \epsilon}, \quad c_N = \frac{(N-1)^2}{(N-2)(N-3)}$$
  where $g_{1,d}$ is sample skewness and $g_{2,d}$ is sample excess kurtosis.
- **Proposition 1 (Null-Calibrated Threshold):** For any continuous symmetric unimodal distribution, $\lim_{N \to \infty} BC(\mathbf{f}_d) \le 5/9 \approx 0.5556$. Selecting features with $BC \ge 5/9$ provably filters unimodal distractor noise without requiring label supervision.
- **Remark 1 (The Zero-Inflation Boundary):** When data matrices exhibit high zero-inflation (e.g., scRNA-seq dropouts $p_0 \to 1$), kurtosis inflates, causing $BC \to 1.0$. This analytically identifies why VSSG / BGSS is primarily designed for continuous measurement manifolds.

### 2.2 Pillar 2 (Point 2): Exact Linear Determinacy & Reduced Bipartite Spectral Transfer-Cut
- **Theoretical Flaw in Prior Work:** Traditional sample determinacy (Li et al., 2019) and spectral consensus (Liu et al., 2017) require constructing and diagonalizing the full $N \times N$ co-association matrix $S$, incurring quadratic $\mathcal{O}(N^2)$ memory and cubic $\mathcal{O}(N^3)$ computational time.
- **Proposition 2 (Exact Linear Determinacy Identity):** We prove that sample determinacy $\sigma_i = \frac{1}{N-1} \sum_{j \neq i} S_{ij}^2$ can be computed **exactly in $\mathcal{O}(M^2 N + M^2 K^2)$ time and $\mathcal{O}(N + MK)$ memory** using cross-model contingency tables $C_{m_1, m_2} \in \mathbb{N}^{K \times K}$:
  $$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i))$$
  with zero truncation error down to floating-point precision ($10^{-16}$).
- **Scalable Bipartite Consensus:** We select $L \ll N$ anchors from the dataset, construct the $N \times L$ bipartite transition matrix $B$, and project eigenvectors via Transfer-Cut, reducing spectral consensus to $\mathcal{O}(N L^2 + L^3)$ operations.

### 2.3 Pillar 3 (Point 5): Multi-Domain Benchmarking, Adversarial Audit & ASPP
- **Benchmark Suite:** Evaluated across 13 primary benchmark datasets (including ALLAML, GLIOMA, CLL_SUB, Colon, SRBCT, PBMC68k-reduced, Madelon, 20 Newsgroups, Zheng68k, Sonar, Prostate, Ovarian, Extended Yale B).
- **11 Baselines:** Rigorously compared against K-Means, Ward, Spectral, SEC, CSPA, MCLA, LWEA, LWGP, FastMICE, DEC, and Li et al. Core-Halo Consensus.
- **ASPP Theory:** Introduced **Anchor-Space Perturbation Profiling (ASPP)**, profiling cluster stability across 5 perturbation operators (sampling, feature dropout, measurement noise, batch shifts, random seeds) strictly in $\mathcal{O}(N L)$ memory to yield certified Perturbation Sensitivity Indices ($PSI_k$).

---

## 3. Empirical Findings from the Adversarial Research Audit (from `paper/numbers.tex`)

Between August and October 2026, an exhaustive adversarial research audit was conducted across 12 audit stages (A1 through A4, E1, E3, E5, E6), stress-testing all claims and establishing the true empirical operating envelope across 2,750 model fits:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   VERIFIED AUDIT FINDINGS SUMMARY                                │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
  [ 1. Continuous Biomedical Manifolds (D/N > 20, 6 Datasets) ]
  • ICC-v2 commands Rank #1 dominance with Mean ARI = 0.217 (median 0.036).
  • Substantially outperforms Standard Consensus (0.037), DEC (0.045), and K-Means (0.056).
  • Golub Leukemia: ARI = 0.600 +/- 0.367, 54.0% oncogenic marker recovery (27 of top 50 markers).
  • Khan SRBCT: ARI = 0.546 +/- 0.102.
  • Ovarian: ARI = 0.050, 5.1x speedup over dense consensus.

  [ 2. General 13-Dataset Multi-Domain Suite (2,750 Model Fits, 11 Solvers) ]
  • Grand Mean ARI = 0.152 (overall rank 5.23 of 11).
  • Omnibus Friedman test: chi^2_F = 9.59, p = 0.48, Nemenyi CD = 4.19.
  • Demonstrates no statistically significant difference globally across heterogeneous multi-domain suite.

  [ 3. Sparse Count / Zero-Inflated Manifolds (Text & scRNA-seq) ]
  • Hierarchical Ward and DEC outperform ICC-v2 on 20 Newsgroups and Zheng68k.
  • Zero-inflation violates the continuous unimodal distractor assumption (Remark 1).

  [ 4. Feature Pool-Size Dynamics (E3 & E3b Negative Result) ]
  • Signal benefit lives in a narrow 5% to 15% pool fraction window.
  • Unsupervised label-free pool selection falls below fixed-fraction priors.
  • A fixed bc_frac = 0.10 default is the empirically defensible recommendation.

  [ 5. Section 5.2 Extended Component Knockout Ablation Study ]
  • Knockout 1: No Gating (V5 -> V3): -78.8% drop (mean ARI collapses from 0.217 to 0.046).
  • Knockout 2: No Anchors (V5 -> V2): -0.139 ARI drop (mean ARI collapses from 0.217 to 0.077).
  • Knockout 3: No Ensembling (V5 -> V1): degrading to 0.070 overall (-0.017 ARI on Leukemia).
  • Knockout 4: Certified vs Random Anchors (V5 -> V4): null result (Delta = +0.019, p = 0.84).
    Confirms bipartite graph compression rather than anchor certification is the primary driver.

  [ 6. Missing-Data Resilience (MCAR Sweep) ]
  • High retention up to 20% MCAR (~80% retention); degrades to baseline level by 30% dropout.

  [ 7. Scalable vs Dense Path Scaling & Extreme Scale ]
  • Dense path (N <= 2000): quadratic O(N^2) memory growth.
  • Scalable anchor path (N > 2000): linear runtime (slope 0.66).
  • N = 10^6 in 55.6 s with peak RSS of 3.05 GB and 240 MB graph memory (99.6% reduction over dense 8 TB).
```

---

## 4. Section 6 Practical Real-World Applications & Clinical Case Studies

1. **Translational Oncology & Cancer Subtyping (`examples/clinical_cancer_subtyping.py`):** Unsupervised subtyping on Golub Leukemia (ARI = 0.600) and Khan SRBCT (ARI = 0.546), recovering 54.0% of top oncogenic driver genes.
2. **Point-of-Care Inductive Biopsy Decision Support (`examples/realtime_patient_projection.py`):** Inductive query evaluation in **22.6 microseconds** per patient biopsy with $(1 - \alpha = 90\%)$ conformal validity guarantees.
3. **Million-Scale Single-Cell Transcriptomics:** Clusters $N = 10^6$ cells in 55.6 s with 240 MB graph memory, bypassing the dense 8 TB RAM barrier.
4. **Conformal Inductive Consensus Clustering (`src/cicc/`):** Split-conformal prediction sets (`conformal.py`), target-decoy / knockoff FDR feature screening with mirror statistics $W_d = |T_d| - |\tilde{T}_d|$ (`decoy.py`), and episodic semantic agent memory (`memory.py`).

---

## 5. Team Execution & Scientific Division of Labor

The project successfully concluded with all four team members fulfilling their designated research responsibilities under the supervision of Prof. Kalyan Kumar Das:

| Member | Designated Role | Realized Deliverable & Contribution |
| :--- | :--- | :--- |
| **Akash Kundu (Lead)** | System Architecture, Mathematics, Lead Author | Formulated the Exact Linear Determinacy Tensor Identity (Proposition 2) and Reduced Bipartite Spectral Transfer-Cut solver. Authored core ICC-v2 consensus engine and Springer Nature manuscript. |
| **Trinankur Guha** | Feature Gating & Base Model Architecture | Derived finite-sample Sarle Bimodality Coefficient corrections (Definition 1, Proposition 1) and implemented VSSG multimodality feature pool generator and subspace diversity constraints. |
| **Rupankar Ghatak** | Experimental Harness, Scaling & Statistics | Built the synthetic phase-transition harness, execution scaling benchmarks (E6 per-process test), missing-data sweeps, and non-parametric Wilcoxon/Friedman test suites. |
| **Anubhav Naskar** | Baselines Integration & Downstream Validation | Implemented and calibrated the 11 baseline algorithms (SEC, CSPA, MCLA, LWEA, LWGP, FastMICE, DEC, Li et al.) and curated the 13-dataset benchmark matrix and downstream validation pipeline. |

---

## 6. Summary of Defensible Novelty for Peer Review (Springer Nature DAMI)

1. **Resolving the "Hallucinated Stability" Blindspot:** First consensus clustering framework to prove analytically and empirically that distance concentration induces artificial consensus in ultra-high dimensions, and to provide a principled multimodality gating solution.
2. **Exact Linear-Memory Sample Determinacy:** First algorithm to compute sample-level co-association determinacy in $\mathcal{O}(M^2 N + M^2 K^2)$ time and $\mathcal{O}(N)$ space, eliminating the $N \times N$ matrix bottleneck.
3. **Anchor-Space Perturbation Profiling (ASPP):** First diagnostic suite to quantify multi-operator cluster vulnerability strictly in anchor space ($\mathcal{O}(N L)$ memory), generating certified out-of-sample confidence scores.
4. **Empirically Calibrated Scientific Integrity:** Full publication of operating envelopes, including negative results (label-free selector limitations, zero-inflation boundary, anchor determinacy null result $p=0.84$), delivering a defensible, reproducible benchmark for the machine learning community.
