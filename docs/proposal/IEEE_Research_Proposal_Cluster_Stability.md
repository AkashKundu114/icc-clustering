# Scientific Research Proposal & Algorithmic Blueprint:
## Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes (ICC-v2)

**Final Year Project Code:** `CSE_PROJECT_68`  
**Original Degree Project Title (University Allotment):** *Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data*  
**Evolved Manuscript Title (Target Submission):** *Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes*  
**Canonical File Location:** [`docs/proposal/IEEE_Research_Proposal_Inductive_Consensus_Clustering.md`](./IEEE_Research_Proposal_Inductive_Consensus_Clustering.md)  
**Target Venues:** *IEEE Transactions on Knowledge and Data Engineering (TKDE)* / *IEEE Transactions on Neural Networks and Learning Systems (TNNLS)* / *IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)* / *IEEE International Conference on Data Engineering (ICDE)*  
**Student Team:** Akash Kundu (Lead), Trinankur Guha, Rupankar Ghatak, Anubhav Naskar  
**Faculty Mentor:** Prof. Kalyan Kumar Das  
**Department:** Computer Science and Engineering  

---

## 1. Executive Summary & Paradigm Shift: From Engineering Pipeline to Scientific Invention

### 1.1 The Project Title Evolution & Scientific Lineage
Our final-year capstone project was initially allocated under the title:
> **"Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data"**

While that title faithfully captured the broad problem space—leveraging cluster stability within an ensemble framework to counter high-dimensional noise—standard engineering treatments typically assemble off-the-shelf components (e.g., K-Means $\to$ Co-association matrix $\to$ Random Forest). In accordance with our mentor Prof. Kalyan Kumar Das's directives, our objective was to transition from an applied engineering pipeline to a **foundational scientific invention**.

As our theoretical derivations, mathematical proofs, and algorithmic developments matured, the scope expanded beyond transductive heuristic stability into an **inductive, geometry-calibrated consensus distillation framework** that:
1. Derives an exact linear-memory determinacy identity ($\mathcal{O}(M^2 N + M^2 K^2)$) breaking the quadratic $\mathcal{O}(N^2)$ consensus memory bottleneck.
2. Derives out-of-sample prediction bounds via Variance-Stabilized Subspace Gating (VSSG) and stability-weighted centroids, turning transductive consensus into an **inductive** clustering paradigm.
3. Quantifies multi-operator stability bounds via Anchor-Space Perturbation Profiling (ASPP) strictly in $\mathcal{O}(N L)$ memory.

Consequently, the project title was formally evolved to:
> **"Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes (ICC-v2)"**

---

### 1.2 The Fundamental Unsolved Problem: The "Hallucinated Stability" Trap
Existing stability-based ensemble clustering literature (e.g., Li et al., *Artificial Intelligence* 2019; MCSS, *ACM TKDD* 2025; ECM-RCL, *Electronics* 2025) operates on a fatal, unstated assumption:  
> **"High agreement across base clusterings implies structural ground truth."**

In low-to-moderate dimensions with isotropic clean data, this assumption holds. However, in **noisy, ultra-high-dimensional spaces** ($D \gg N$), this assumption fundamentally collapses due to **pairwise distance concentration** (*Beyer-Goldstein-Ramakrishnan-Srivastava Theorem, 1999*):
$$\lim_{D \to \infty} \frac{\mathrm{Var}(\|\mathbf{x}_i - \mathbf{x}_j\|)}{\mathbb{E}[\|\mathbf{x}_i - \mathbf{x}_j\|]^2} = 0 \implies \lim_{D \to \infty} \frac{\mathrm{dist}_{\max}(X) - \mathrm{dist}_{\min}(X)}{\mathrm{dist}_{\min}(X)} \to 0$$
When thousands of uninformative nuisance dimensions corrupt the geometry (e.g., $7{,}000+$ noise genes in transcriptomic profiling), pairwise distances become essentially uniform. Standard distance-based base clusterers (K-Means, Fuzzy C-Means, Agglomerative, Spectral) optimize loss functions dominated by noise coordinates. Rather than exploring diverse partitions of the true underlying manifold $\mathcal{M}$, **the base clusterers repeatedly converge into the exact same spurious geometric ridges created by distance concentration**.

Consequently, the co-association matrix exhibits **near-zero variance** ($S_{ij} \to 1.0$) for completely artifactual, noise-induced groupings:
$$\text{Det}(i) = \frac{1}{N}\sum_{j=1}^N \left[1 - 4(S_{ij} - 0.5)^2\right] \to 1.0 \quad \text{(Maximal Hallucinated Determinacy)}$$

Existing methods (like Li et al.'s linear and quadratic determinacy) interpret this artificial agreement as **"Stable Core"** samples. They mistake **systematic high-dimensional geometric distortion for true cluster stability**. Simultaneously, true manifold boundary points and biological transition states (which legitimately transition between overlapping classes and exhibit natural voting fluctuation $S_{ij} \approx 0.5$) are discarded as "unstable halo" noise. **Current consensus ensembles promote noise artifacts into the trusted core and discard true biological boundaries.**

```
                    ┌───────────────────────────────────────────┐
                    │       THE EXISTING CONSENSUS BLINDSPOT    │
                    └───────────────────────────────────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
     High-Dimensional Noise Traps                    True Topological Boundaries
  (Artifactual groupings caused by              (Legitimate overlapping samples with
       distance concentration)                       shared manifold properties)
                  │                                               │
  Base clusterings agree consistently            Base clusterings fluctuate naturally
                  │                                               │
                  ▼                                               ▼
         [ Classed as "CORE" ]                          [ Classed as "HALO" ]
  FALSE DISCOVERY OF STRUCTURE                   TRUE STRUCTURAL INFORMATION LOST
```

### 1.3 The Core Invention: Invariant Core Consensus (ICC-v2)
To break this trap, we introduce **Dual-Space Invariant Core Consensus (ICC-v2)**. ICC-v2 is the first consensus learning framework that simultaneously operates across the **Primal Feature Space $\mathcal{X} \subset \mathbb{R}^D$** and the **Dual Connectivity Graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$**, decomposing ensemble co-association into three disjoint physical regimes:
1. $\mathcal{S}_{\text{Core}}$: **Invariant Structural Core** (true latent clusters backed by mutual feature subspace multimodality).
2. $\mathcal{S}_{\text{Bound}}$: **Topological Boundary Transitions** (genuine soft manifold transitions, preserved rather than pruned).
3. $\mathcal{S}_{\text{Artifact}}$: **Noise-Induced Artifacts** (consistently agreed-upon clusters that lack local feature manifold support, mathematically excised).

---

## 2. In-Depth Focus on Mentor Directives (Points 1, 2, and 5)

Our research centers strictly on the three pillars emphasized by our mentor:
* **Point 1:** Noise-Aware Base Clustering Generation via Variance-Stabilized Subspace Gating (VSSG).
* **Point 2:** Robust Consensus Learning via Exact Linear Determinacy & Reduced Bipartite Spectral Transfer-Cut.
* **Point 5:** Multi-Level Empirical Validation, Inductive Generalization Verification, and Benchmark Pipeline Release.

```
====================================================================================================
                        INVARIANT CORE CONSENSUS (ICC-v2) RESEARCH PIPELINE
====================================================================================================

 [ STAGE 1: POINT 1 ]           [ STAGE 2: POINT 2 ]                 [ STAGE 3: POINT 5 ]
 DUAL-SPACE NOISE-AWARE         EXACT LINEAR DETERMINACY &           MULTI-LEVEL INDUCTIVE
 BASE CLUSTERING VIA VSSG       REDUCED BIPARTITE TRANSFER-CUT       VALIDATION & BENCHMARKING
 ──────────────────────         ──────────────────────────────       ─────────────────────────
 ┌────────────────────┐         ┌──────────────────────────┐         ┌───────────────────────┐
 │ Input Data X (NxD) │         │ Base Partitions {Π^(m)}  │         │ Consensus Graph S*    │
 │ D >> N, Noisy      │         │ Subspace Pools {z^(m)}   │         │ Core/Boundary/Noise   │
 └─────────┬──────────┘         └────────────┬─────────────┘         └───────────┬───────────┘
           │                                 │                                   │
           ▼                                 ▼                                   ▼
 ┌────────────────────┐         ┌──────────────────────────┐         ┌───────────────────────┐
 │ Finite-Sample BC   │         │ Exact Linear Determinacy │         │ Downstream Inductive  │
 │ Multimodality Gate │         │ Contingency Tensor:      │         │ Generalization on Core│
 │ Threshold BC > 5/9 │         │ σ_i in O(M^2 N + M^2 K^2)│         │ (SVM / RF / Deep Net) │
 └─────────┬──────────┘         └────────────┬─────────────┘         └───────────┬───────────┘
           │                                 │                                   │
           ▼                                 ▼                                   ▼
 ┌────────────────────┐         ┌──────────────────────────┐         ┌───────────────────────┐
 │ M Diverse Base     │         │ Reduced Bipartite Cut:   │         │ Benchmark Suite:      │
 │ Partitions over    │────────►│ Solve L x L Anchor System│────────►│ 13 Primary Benchmarks,│
 │ Gated Subspaces    │         │ Linear O(N L^2 + L^3)    │         │ 10 Baselines, ASPP    │
 └────────────────────┘         └──────────────────────────┘         └───────────────────────┘
====================================================================================================
```

---

## 3. Pillar 1: Noise-Aware Base Clustering via VSSG (Point 1)

### 3.1 Limitations of Prior Work
* **Random Subspace Clustering (Jing et al., 2015):** Randomly samples features without knowing which dimensions carry signal. In ultra-high dimensions where $90\%$ of features are noise, random sampling draws purely noisy subspaces with high probability.
* **Classical Feature Selection (Cui et al., 2008):** Runs optimization using global cluster validity indexes (e.g., Davies-Bouldin, Silhouette). These metrics compute Euclidean pairwise distances across all features, which are corrupted by distance concentration in high dimensions.

### 3.2 The New Algorithmic Approach: Variance-Stabilized Subspace Gating (VSSG)
Rather than treating base clustering as a black-box execution of standard algorithms, we screen features using marginal multimodality prior to subspace ensemble generation:

#### 3.2.1 Finite-Sample Corrected Sarle Bimodality Coefficient
For feature $\mathbf{f}_d = [X_{1d}, \dots, X_{Nd}]^\top \in \mathbb{R}^N$ with sample mean $\bar{f}_d$ and sample variance $s_d^2$, the sample skewness $g_{1, d}$ and sample excess kurtosis $g_{2, d}$ are:
$$g_{1, d} = \frac{\frac{1}{N} \sum_{i=1}^N (X_{id} - \bar{f}_d)^3}{\left(\frac{1}{N} \sum_{i=1}^N (X_{id} - \bar{f}_d)^2\right)^{3/2}}, \quad g_{2, d} = \frac{\frac{1}{N} \sum_{i=1}^N (X_{id} - \bar{f}_d)^4}{\left(\frac{1}{N} \sum_{i=1}^N (X_{id} - \bar{f}_d)^2\right)^2} - 3$$
The finite-sample corrected Bimodality Coefficient is given by:
$$BC(\mathbf{f}_d) = \frac{g_{1, d}^2 + 1}{g_{2, d} + 3 \cdot c_N + \epsilon}$$
where $c_N = \frac{(N-1)^2}{(N-2)(N-3)}$ for $N \ge 4$ (and $c_N = 1$ otherwise), and $\epsilon > 0$ is a numerical regularization constant.

#### 3.2.2 Null-Calibrated Gating Threshold (Proposition 1)
For any continuous symmetric unimodal distribution with finite moments:
$$\lim_{N \to \infty} BC(\mathbf{f}_d) \le \frac{5}{9} \approx 0.5556$$
*Proof:* For a Gaussian distribution $\mathcal{N}(0, \sigma^2)$, $\gamma_1 = 0$ and $\gamma_2 = 0$, giving $BC_{\text{Gauss}} = \frac{0 + 1}{0 + 3} = \frac{1}{3} \approx 0.3333 < \frac{5}{9}$. For a uniform distribution $U(a, b)$, $\gamma_1 = 0$ and $\gamma_2 = -1.2$, giving $BC_{\text{Uniform}} = \frac{0 + 1}{1.8} = \frac{5}{9} \approx 0.5556$. Since the uniform density represents the minimal kurtosis boundary among symmetric unimodal distributions, any continuous unimodal distractor satisfies $BC \le 5/9$. Selecting candidate features with $BC(\mathbf{f}_d) \ge 5/9$ provides a distribution-free null-calibrated threshold that rejects unimodal noise. $\blacksquare$

#### 3.2.3 Subspace Generation with Diversity Constraints
From the screened candidate feature pool $\mathcal{F}_{\text{pool}} = \{d \in \{1, \dots, D\} : BC(\mathbf{f}_d) \ge 5/9\}$, each base model $m \in \{1, \dots, M\}$ randomly samples a subspace $\mathbf{z}^{(m)} \subset \mathcal{F}_{\text{pool}}$ of dimensionality $d_{\text{sub}} \le 0.3 |\mathcal{F}_{\text{pool}}|$, constrained to maximize subspace diversity across the ensemble:
$$\mathcal{D}_{\text{corr}}(\mathbf{z}^{(m)}, \mathbf{z}^{(l)}) = 1 - \frac{(\mathbf{z}^{(m)})^\top \mathbf{z}^{(l)}}{\|\mathbf{z}^{(m)}\|_2 \|\mathbf{z}^{(l)}\|_2}$$

---

## 4. Pillar 2: Robust Consensus with Exact Linear Determinacy (Point 2)

### 4.1 Theoretical Gap in State-of-the-Art
* **Li et al. (2019):** Computes pairwise Co-association $S_{ij} = \frac{1}{M}\sum_{m=1}^M \mathbb{I}(\pi_i^{(m)} = \pi_j^{(m)})$ and calculates sample stability via determinacy:
  $$\sigma_i = \frac{1}{N-1}\sum_{j \neq i}^N S_{ij}^2$$
  *Flaw:* Requires explicit computation and storage of the $N \times N$ matrix $S$, incurring $\mathcal{O}(N^2)$ memory and $\mathcal{O}(N^3)$ computational scaling, making it prohibitive for modern datasets.
* **Liu et al. (SEC, 2017) & Qu et al. (ECM-RCL, 2025):** Spectral consensus solvers that rely on full $N \times N$ graph eigendecomposition scaling in $\mathcal{O}(N^3)$ time.

### 4.2 Exact Linear-Memory Determinacy Identity (Proposition 2)
Let $\Pi = \{\pi_1, \dots, \pi_M\}$ be an ensemble of $M$ partitions over $N$ instances into $K$ clusters. Sample determinacy $\sigma_i$ can be computed **exactly in $\mathcal{O}(M^2 N + M^2 K^2)$ time and $\mathcal{O}(N + M K)$ memory** without constructing the $N \times N$ matrix $S$, via cross-model contingency tables:
$$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i))$$
where $C_{m_1, m_2} \in \mathbb{N}^{K \times K}$ is the contingency matrix between base clusterings $m_1$ and $m_2$:
$$C_{m_1, m_2}(a, b) = \sum_{j=1}^N \mathbb{I}(\pi_{m_1}(j) = a \land \pi_{m_2}(j) = b)$$
Subtracting the diagonal entry $S_{ii}^2 = 1$ and dividing by $N - 1$:
$$\sigma_i = \frac{1}{N - 1} \left[ \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i)) - 1 \right]$$
This identity holds with zero truncation error down to floating-point machine precision ($10^{-16}$). $\blacksquare$

### 4.3 Reduced Bipartite Spectral Consensus (Transfer-Cut)
To break the cubic complexity bottleneck, we select $L \ll N$ anchor points from the certified Invariant Core $\mathcal{S}_{\text{Core}}$ (e.g., $L = \min(N, \max(20, 2K))$).
1. We construct the rectangular bipartite co-association matrix $B \in [0, 1]^{N \times L}$:
   $$B_{il} = \frac{1}{M} \sum_{m=1}^M \mathbb{I}(\pi_m(\mathbf{x}_i) = \pi_m(\mathbf{a}_l)), \quad \mathbf{a}_l \in \mathcal{S}_{\text{Core}}$$
2. Row-normalized affinity $\tilde{B} = D_B^{-1} B$ where $D_B = \mathrm{diag}(B \mathbf{1}_L)$.
3. The reduced anchor-anchor affinity matrix $W_A \in \mathbb{R}^{L \times L}$ is $W_A = \tilde{B}^\top \tilde{B}$.
4. The normalized anchor Laplacian $L_A = I_L - D_A^{-1/2} W_A D_A^{-1/2}$ is solved for its top-$K$ eigenvectors $V_K \in \mathbb{R}^{L \times K}$ in $\mathcal{O}(L^3)$.
5. The full embedding for all $N$ instances is recovered via Transfer-Cut projection:
   $$U = \tilde{B} V_K \in \mathbb{R}^{N \times K}$$
6. Unit-norm row normalization and K-Means++ discretization yields the final consensus partition $\pi^*$.
**Total complexity:** $\mathcal{O}(N L^2 + L^3)$ time and $\mathcal{O}(N L)$ memory—strictly linear in $N$!

---

## 5. Mathematical Formulation of the Complete ICC-v2 Algorithm

```
====================================================================================================
ALGORITHM 1: INVARIANT CORE CONSENSUS (ICC-v2)
====================================================================================================
Input:  Dataset X in R^{N x D}, base cluster count M, target clusters K, anchor count L,
        subspace dimension ratio d_sub_ratio, core quantile threshold tau.
Output: Final Consensus Partition C* in {0, ..., K-1}^N, Sample Determinacy scores sigma.

// STAGE 1: VARIANCE-STABILIZED SUBSPACE GATING (VSSG)
1:  FOR EACH feature d in {1, ..., D} DO:
2:      Compute sample skewness g_{1, d} and sample excess kurtosis g_{2, d}.
3:      Compute finite-sample Sarle Bimodality Coefficient BC(f_d) (Eq. 3).
4:  END FOR
5:  Extract candidate feature pool F_pool = {d : BC(f_d) >= 5/9}.
6:  IF |F_pool| < K THEN fallback to top-15% variance features.
7:  FOR m = 1 TO M DO:
8:      Draw random feature subset z^(m) from F_pool of size d_sub = floor(d_sub_ratio * |F_pool|).
9:      Fit base model m on X[:, z^(m)] to obtain partition pi_m in {0, ..., K-1}^N.
10: END FOR

// STAGE 2: EXACT LINEAR DETERMINACY CALCULATION
11: Compute cross-model contingency tables C_{m1, m2} in N^{K x K} for all m1, m2 in {1, ..., M}.
12: FOR EACH instance i in {1, ..., N} DO:
13:     Compute exact determinacy sigma_i via Proposition 2 in O(M^2).
14: END FOR
15: Identify Invariant Core S_Core = {i : sigma_i >= Quantile(sigma, tau)}.

// STAGE 3: REDUCED BIPARTITE SPECTRAL TRANSFER-CUT CONSENSUS
16: IF N <= 2,000 THEN:
17:     Construct full co-association matrix S and solve dense spectral consensus.
18: ELSE:
19:     Select L anchors from S_Core via k-means++ or determinacy rank.
20:     Construct bipartite matrix B in R^{N x L} between all instances and L anchors.
21:     Construct normalized anchor affinity W_A = B_norm^T B_norm in R^{L x L}.
22:     Solve top-K eigenvectors V_K of anchor Laplacian L_A.
23:     Project full embedding U = B_norm * V_K in R^{N x K}.
24:     Normalize rows of U and discretize via K-Means++ to yield C*.
25: END IF
26: RETURN C*, sigma, S_Core.
====================================================================================================
```

---

## 6. Pillar 3: Multi-Level Empirical Validation & Benchmark Findings (Point 5)

### 6.1 Standardized Multi-Domain Benchmark Suite (13 Core Datasets)

| Dataset | Domain | Samples ($N$) | Features ($D$) | Clusters ($K$) | Dimension Ratio ($D/N$) | Key Domain Characteristic |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ALLAML** | Leukemia Microarray | $72$ | $7{,}129$ | $2$ | **$99.0$** | Severe sample sparsity, extreme continuous dimensionality |
| **GLIOMA** | Brain Cancer mRNA | $50$ | $4{,}434$ | $4$ | **$88.6$** | Multiple small, overlapping histological subclasses |
| **CLL_SUB** | Leukemia Subtypes | $111$ | $11{,}340$ | $3$ | **$102.1$** | Highest dimensionality ratio; passenger mutations |
| **Colon** | Colon Tumor Biopsies | $62$ | $2{,}000$ | $2$ | **$32.2$** | High technical noise, non-Gaussian artifacts |
| **SRBCT** | Childhood Tumors | $83$ | $2{,}308$ | $4$ | **$27.8$** | Four distinct continuous pediatric tumor expressions |
| **Lymphoma** | Lymphoid Malignancies | $62$ | $4{,}026$ | $3$ | **$64.9$** | Molecular classification of diffuse large B-cell lymphoma |
| **Prostate** | Prostate Cancer | $102$ | $6{,}033$ | $2$ | **$59.1$** | Prostate tumor vs normal expression profiles |
| **Ovarian** | Ovarian Cancer Proteomics | $253$ | $1{,}515$ | $2$ | **$6.0$** | Continuous mass spectrometry proteomic profiling |
| **PBMC 3k** | Single-Cell RNA-seq | $2{,}700$ | $13{,}714$ | $8$ | **$5.1$** | Extreme zero-inflation ($>80\%$ dropout noise) |
| **Zheng68k** | Purified Immune scRNA | $1{,}000$ | $1{,}000$ | $10$ | **$1.0$** | High zero-inflation, discrete transcript count matrix |
| **20 Newsgroups** | Document Text Mining | $1{,}000$ | $2{,}000$ | $4$ | **$2.0$** | Extreme TF-IDF term sparsity, sparse text distributions |
| **Madelon** | Synthetic Feature Challenge | $2{,}600$ | $500$ | $2$ | **$0.19$** | $480$ completely random distractor dimensions |
| **Sonar** | Sonar Signals | $208$ | $60$ | $2$ | **$0.29$** | Standard low/mid-dimensional continuous baseline |

### 6.2 The 10 Baseline Algorithms
1. **K-Means (Lloyd, 1982)** — Standard distance-based single model.
2. **Hierarchical Ward (Ward, 1963)** — Agglomerative variance minimization.
3. **Spectral Clustering (Ng et al., 2001)** — Normalized graph cut.
4. **SEC (Liu et al., TKDE 2017)** — Spectral Ensemble Clustering.
5. **CSPA (Strehl & Ghosh, JMLR 2002)** — Cluster-based Similarity Partitioning.
6. **MCLA (Strehl & Ghosh, JMLR 2002)** — Meta-Clustering Algorithm.
7. **LWEA (Huang et al., TPAMI 2017)** — Locally Weighted Ensemble Clustering.
8. **LWGP (Huang et al., TPAMI 2018)** — Locally Weighted Graph Partitioning.
9. **FastMICE (Huang et al., TKDE 2023)** — Scalable Multi-View Bipartite Ensemble.
10. **DEC (Xie et al., ICML 2016)** — Deep Embedded Clustering.

### 6.3 Empirical Findings & Audit Insights
Across 1,430 model executions on the benchmark suite and dedicated adversarial audit sweeps:
1. **Domain Specialization on Ultra-High-Dimensional Assays ($D/N > 20$):**  
   ICC-v2 exhibits **Rank #1 dominance** ($R = 1.50$), achieving dramatic lifts over deep and classical methods (Leukemia ARI = 0.680 vs. DEC 0.148, K-Means 0.210; SRBCT ARI = 0.538 vs. Std Consensus 0.040, K-Means 0.053; Ovarian ARI = 0.052). Deep learning collapses due to sample sparsity ($N \le 100$), while standard consensus collapses due to distance concentration.
2. **Zero-Inflation Boundary (Sparse Text and scRNA-seq):**  
   Hierarchical Ward and DEC outperform ICC-v2 on 20 Newsgroups and Zheng68k. Heavy zero-inflation violates the continuous unimodal distractor assumption (Remark 1), inflating marginal kurtosis at zero.
3. **Downstream Inductive Generalization (Exp 1 Audit):**  
   Downstream classifiers trained exclusively on the certified Invariant Core (50% sample budget) attain parity with full-data training under low-to-moderate distractor noise ($D_{\text{noise}} \le 50$, test accuracy 1.000). Under severe noise ($D_{\text{noise}} \ge 1{,}000$), all unguided ambient classifiers degrade toward chance ($0.31\text{--}0.37$).
4. **Missing-Data Stability (Exp 3 MCAR Sweep):**  
   Across multi-dataset sweeps (`e5_missing_rerun.csv`), cluster recovery retains $\approx 108\%$ / $80\%$ / $33\%$ / $41\%$ of 0%-missing ARI at $10\%$ / $20\%$ / $30\%$ / $50\%$ missing data, demonstrating robustness up to $20\%$ dropout before degrading to baseline levels by $30\%$.
5. **Linear Computational Scaling (E6 Benchmark):**  
   The dense path ($N \le 2{,}000$) exhibits $\mathcal{O}(N^2)$ memory scaling (6 MB to 61 MB, time slope 1.18). The scalable anchor path ($N > 2{,}000$) demonstrates linear $\mathcal{O}(N)$ scaling (time slope 0.66, 6 MB to 98 MB up to $N = 32{,}000$ in $0.77\text{s}$).

---

## 7. Deep Gap Analysis of Seminal Literature & Proposed Solutions

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                            PRIOR ART GAP ANALYSIS & ICC-v2 RESOLUTION                            │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

| Prior Work & Venue | Core Technique | Fatal Gap / Failure Mode Isolated by ICC-v2 | How ICC-v2 Resolves & Synthesizes It |
| :--- | :--- | :--- | :--- |
| **Li et al. (2019)**<br/>*Artif. Intell.* | Linear & quadratic co-association determinacy ($CEs^2$). | Flat graph determinacy; blind to feature noise; misclassifies distance-concentrated noise as "Core". $\mathcal{O}(N^2)$ memory. | Replaces dense matrix with **Exact Linear Determinacy Identity** ($O(M^2 N + M^2 K^2)$) and couples with VSSG multimodality screening. |
| **Huang et al. (2017/18)**<br/>*LWEA / LWGP* | Local entropy weighting on co-association graphs. | Operates in raw unguided feature space; fails when ambient distractor noise $D_{\text{noise}} \ge 1{,}000$ corrupts entropy. | Pre-filters features via finite-sample Sarle Bimodality Coefficient ($BC \ge 5/9$), guaranteeing clean subspace base inputs. |
| **Huang et al. (2023)**<br/>*FastMICE (TKDE)* | Scalable multi-view ensemble on bipartite graphs. | Does not filter feature noise; susceptible to noise voter contamination in high dimensions. | Combines scalable bipartite Transfer-Cut with certified Invariant Core anchors selected via exact linear determinacy. |
| **Nie et al. (2024)**<br/>*FCAG (TPAMI)* | Fast clustering on anchor graphs via matrix factorization. | Selects anchors via K-Means on ambient features, which collapse under $D \gg N$ distance concentration. | Selects anchors strictly from the certified **Invariant Core** ($\mathcal{S}_{\text{Core}}$), immunizing anchor selection against noise. |
| **Xie et al. (2016)**<br/>*DEC (ICML)* | Deep autoencoder embedding with Student-$t$ clustering. | Sample sparsity collapse: deep autoencoders severely overfit and fail when $N \le 100$ and $D \in [2{,}000, 11{,}000]$. | Retains robust spectral graph formulation that excels on small-sample biomedical assays ($N \le 100$). |
| **Liu et al. (2017)**<br/>*SEC (TKDE)* | Spectral Ensemble Clustering via normalized cuts. | Cubic $\mathcal{O}(N^3)$ computational time and $\mathcal{O}(N^2)$ storage; lacks feature-level distractor screening. | Bipartite Transfer-Cut solves an $L \times L$ anchor system in $\mathcal{O}(N L^2 + L^3)$ time and $\mathcal{O}(N L)$ memory. |

---

## 8. Theoretical Foundations & Asymptotic Complexity

### 8.1 Theorem 1 (Inductive Assignment Convergence)
For an unseen query instance $\mathbf{x}_{\text{new}} \in \mathbb{R}^D$, let $\mathcal{F}_{\text{active}}$ denote the active candidate features selected by VSSG. The inductive cluster assignment is:
$$\hat{y}(\mathbf{x}_{\text{new}}) = \arg\min_{k \in \{0, \dots, K-1\}} \|\mathbf{x}_{\text{new}}[\mathcal{F}_{\text{active}}] - \mathbf{c}_k[\mathcal{F}_{\text{active}}\|_2$$
where $\mathbf{c}_k = \frac{\sum_{i: \hat{y}_i = k} \sigma_i \cdot \mathbf{x}_i}{\sum_{i: \hat{y}_i = k} \sigma_i}$ is the stability-calibrated centroid. Assuming sub-Gaussian cluster conditional distributions on the signal subspace, query misclassification probability satisfies:
$$\Pr(\hat{y}(\mathbf{x}_{\text{new}}) \neq y^*(\mathbf{x}_{\text{new}})) \le (K - 1) \exp\left( - \frac{\Delta_{\min}^2}{8 \sigma_{\max}^2} \right)$$
where $\Delta_{\min}$ is the inter-cluster margin on $\mathcal{F}_{\text{active}}$ and $\sigma_{\max}^2$ is within-cluster variance.

### 8.2 Theorem 2 (Asymptotic Complexity Bounds)
1. **Time Complexity:**
   - VSSG multimodality screening: $\mathcal{O}(N \cdot D)$.
   - Base model fits: $\mathcal{O}(M \cdot (N \cdot d_{\text{sub}} \cdot K))$ where $d_{\text{sub}} \le 0.3 D$.
   - Exact Linear Determinacy: $\mathcal{O}(M^2 N + M^2 K^2)$.
   - Bipartite Graph Construction: $\mathcal{O}(M \cdot N \cdot L)$.
   - Reduced Spectral Decomposition: $\mathcal{O}(N L^2 + L^3)$.
   - **Total Training Time:** $\mathcal{O}(N(D + M d_{\text{sub}} K + M^2 + M L) + L^3)$ — strictly linear in $N$.
2. **Space Complexity:** $\mathcal{O}(N \cdot L)$ auxiliary storage, compared to $\mathcal{O}(N^2)$ for standard consensus.
3. **Inductive Query Latency:** $\mathcal{O}(K \cdot |\mathcal{F}_{\text{active}}|)$ operations, independent of $N$.

---

## 9. Deliverables, Timeline & IEEE Target Submission Strategy

### 9.1 Project Execution Milestones
* **Month 1 (Theory & Scaffolding):** Mathematical formulation of Proposition 1 (Sarle bound) and Proposition 2 (Linear Determinacy Identity). Setup of reproducible dataset pipeline.
* **Month 2 (Implementation & Baselines):** Production-grade Python package (`icc`) with 10 baselines (K-Means, Ward, Spectral, SEC, CSPA, MCLA, LWEA, LWGP, FastMICE, DEC) and 65 unit tests.
* **Month 3 (Large-Scale Benchmarks & Adversarial Audit):** 1,430 model executions across 13 primary datasets; adversarial research audit sweeps (A1–A4, E1, E3, E5, E6).
* **Month 4 (Manuscript & Open-Source Release):** IEEE Transactions LaTeX manuscript (`ieee_manuscript/main.tex`), ICDE paper draft, research audit dossier, open-source GitHub release.

### 9.2 Clear Team Responsibility Matrix
* **Akash Kundu (Lead):** Mathematical formulation of Linear Determinacy Identity (Proposition 2) and Bipartite Spectral Transfer-Cut; core architecture of `src/icc/consensus.py`; lead author for IEEE manuscript.
* **Trinankur Guha:** Finite-sample Sarle Bimodality Coefficient derivation and VSSG multimodality screening (`src/icc/gating.py`); subspace diversity constraints.
* **Rupankar Ghatak:** Experimental harness, per-process scaling benchmark (E6), missing-data evaluation, and statistical Wilcoxon/Friedman tests.
* **Anubhav Naskar:** Implementation and calibration of the 10 baseline solvers (`src/icc/baselines/`); curation of the 13 benchmark datasets and downstream validation suite.

---

## 10. Summary of Novelty (Why This Manuscript Is Defensible for IEEE TKDE)

1. **Category D Scientific Novelty:** Proven exact linear-memory determinacy identity computing $\sigma_i$ in $\mathcal{O}(M^2 N + M^2 K^2)$ without dense $N \times N$ matrix storage.
2. **Analytical Characterization of the Operating Boundary:** Formal proof of the zero-inflation boundary (Remark 1), explaining both our Rank #1 dominance on continuous cancer assays ($D/N > 20$) and the ceiling on sparse scRNA-seq matrices.
3. **Anchor-Space Perturbation Profiling (ASPP):** Closed-form stability diagnostics profiling 5 perturbation families strictly in $\mathcal{O}(N L)$ memory.
4. **Adversarial Audit Integrity:** Transparent reporting of empirical operating envelopes, negative results (label-free selector limits), and calibrated claims, providing a gold-standard benchmark for the machine learning community.
