# Scientific Research Proposal & Algorithmic Blueprint:
## Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes (ICC-v2)

**Final Year Project Code:** `CSE_PROJECT_68`  
**Original Degree Project Title (University Allotment):** *Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data*  
**Early Proposal Blueprint Title (Capstone Proposal):** *Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes*  
**Canonical Manuscript Title (Springer Nature DAMI):** *When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination*  
**Canonical File Location:** [`docs/proposal/inductive_consensus_proposal.md`](./inductive_consensus_proposal.md)  
**Target Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI), document class `sn-jnl.cls` (`sn-mathphys-num.bst`).  
**Canonical Release Version:** v2.1.0  
**Student Team:** Akash Kundu (Lead), Trinankur Guha, Rupankar Ghatak, Anubhav Naskar  
**Faculty Mentor:** Prof. Kalyan Kumar Das  
**Department:** Computer Science and Engineering  

---

## 1. Executive Summary & Paradigm Shift: From Engineering Pipeline to Scientific Invention

### 1.1 The Project Title Evolution & Scientific Lineage
Our final-year capstone project was initially allocated under the title:
> **"Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data"**

While that title faithfully captured the broad problem space, leveraging cluster stability within an ensemble framework to counter high-dimensional noise, standard engineering treatments typically assemble off-the-shelf components (e.g., K-Means -> Co-association matrix -> Random Forest). In accordance with our mentor Prof. Kalyan Kumar Das's directives, our objective was to transition from an applied engineering pipeline to a **foundational scientific invention**.

As our theoretical derivations, mathematical proofs, and algorithmic developments matured, the scope expanded beyond transductive heuristic stability into an **inductive, geometry-calibrated consensus distillation framework** that:
1. Derives an exact linear-memory determinacy identity ($\mathcal{O}(M^2 N + M^2 K^2)$) breaking the quadratic $\mathcal{O}(N^2)$ consensus memory bottleneck.
2. Derives out-of-sample prediction bounds via Variance-Stabilized Subspace Gating (VSSG / BGSS) and stability-weighted centroids, turning transductive consensus into an **inductive** clustering paradigm.
3. Quantifies multi-operator stability bounds via Anchor-Space Perturbation Profiling (ASPP) strictly in $\mathcal{O}(N L)$ memory.

During the early capstone phase, the proposal was titled:
> **"Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes (ICC-v2)"**

Through rigorous empirical examination, pre-registered testing, and frozen Pass F benchmark audits, this research evolved into its canonical journal manuscript:
> **"When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"**  
> Published in the **Springer Nature Journal *Data Mining and Knowledge Discovery* (DAMI)**.

---

### 1.2 The Fundamental Unsolved Problem: The "Hallucinated Stability" Trap
Existing stability-based ensemble clustering literature (e.g., Li et al., *Artificial Intelligence* 2019; MCSS, *ACM TKDD* 2025; ECM-RCL, *Electronics* 2025) operates on a fatal, unstated assumption:  
> **"High agreement across base clusterings implies structural ground truth."**

In low-to-moderate dimensions with isotropic clean data, this assumption holds. However, in **noisy, ultra-high-dimensional spaces** ($D \gg N$), this assumption fundamentally collapses due to **pairwise distance concentration** (*Beyer-Goldstein-Ramakrishnan-Srivastava Theorem, 1999*):
$$\lim_{D \to \infty} \frac{\mathrm{Var}(\|\mathbf{x}_i - \mathbf{x}_j\|)}{\mathbb{E}[\|\mathbf{x}_i - \mathbf{x}_j\|]^2} = 0 \implies \lim_{D \to \infty} \frac{\mathrm{dist}_{\max}(X) - \mathrm{dist}_{\min}(X)}{\mathrm{dist}_{\min}(X)} \to 0$$
When thousands of uninformative nuisance dimensions corrupt the geometry (e.g., $7{,}000+$ noise genes in transcriptomic profiling), pairwise distances become essentially uniform. Standard distance-based base clusterers (K-Means, Fuzzy C-Means, Agglomerative, Spectral) optimize loss functions dominated by noise coordinates. Rather than exploring diverse partitions of the true underlying manifold $\mathcal{M}$, **the base clusterers repeatedly converge into the exact same spurious geometric ridges created by distance concentration**.

Consequently, the co-association matrix exhibits **near-zero variance** ($S_{ij} \to 1.0$) for completely artifactual, noise-induced groupings:
$$\text{Det}(i) = \frac{1}{N}\sum_{j=1}^N \left[1 - 4(S_{ij} - 0.5)^2\right] \to 1.0 \quad \text{(Maximal Hallucinated Determinacy)}$$

Existing methods (like Li et al.'s linear and quadratic determinacy) interpret this artificial agreement as **"Stable Core"** samples. They mistake **systematic high-dimensional geometric distortion for true cluster stability**. Simultaneously, true manifold boundary points and biological transition states (which legitimately transition between overlapping classes and exhibit natural voting fluctuation $S_{ij} \approx 0.5$) are discarded as "unstable halo" noise. Current consensus ensembles promote noise artifacts into the trusted core and discard true biological boundaries.

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
To break this trap, we introduce **Dual-Space Invariant Core Consensus (ICC-v2)**. ICC-v2 operates across the **Primal Feature Space $\mathcal{X} \subset \mathbb{R}^D$** and the **Dual Connectivity Graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$**, decomposing ensemble co-association into three disjoint physical regimes:
1. $\mathcal{S}_{\text{Core}}$: **Invariant Structural Core** (true latent clusters backed by mutual feature subspace multimodality).
2. $\mathcal{S}_{\text{Bound}}$: **Topological Boundary Transitions** (genuine soft manifold transitions, preserved rather than pruned).
3. $\mathcal{S}_{\text{Artifact}}$: **Noise-Induced Artifacts** (consistently agreed-upon clusters that lack local feature manifold support, mathematically excised).

---

## 2. In-Depth Focus on Mentor Directives (Points 1, 2, and 5)

Our research centers strictly on the three pillars emphasized by our mentor:
* **Point 1:** Noise-Aware Base Clustering Generation via Variance-Stabilized Subspace Gating (VSSG / BGSS).
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
 │ Gated Subspaces    │         │ Linear O(N L^2 + L^3)    │         │ 11 Baselines, ASPP    │
 └────────────────────┘         └──────────────────────────┘         └───────────────────────┘
====================================================================================================
```

---

## 3. Pillar 1: Noise-Aware Base Clustering via VSSG / BGSS (Point 1)

### 3.1 Limitations of Prior Work
* **Random Subspace Clustering (Jing et al., 2015):** Randomly samples features without knowing which dimensions carry signal. In ultra-high dimensions where $90\%$ of features are noise, random sampling draws purely noisy subspaces with high probability.
* **Classical Feature Selection (Cui et al., 2008):** Runs optimization using global cluster validity indexes (e.g., Davies-Bouldin, Silhouette). These metrics compute Euclidean pairwise distances across all features, which are corrupted by distance concentration in high dimensions.

### 3.2 The Algorithmic Approach: Variance-Stabilized Subspace Gating (VSSG / BGSS)
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
To break the cubic complexity bottleneck, we select $L \ll N$ anchor points from the dataset:
1. We construct the rectangular bipartite co-association matrix $B \in [0, 1]^{N \times L}$:
   $$B_{il} = \frac{1}{M} \sum_{m=1}^M \mathbb{I}(\pi_m(\mathbf{x}_i) = \pi_m(\mathbf{a}_l)), \quad \mathbf{a}_l \in \mathcal{A}$$
2. Row-normalized affinity $\tilde{B} = D_B^{-1} B$ where $D_B = \mathrm{diag}(B \mathbf{1}_L)$.
3. The reduced anchor-anchor affinity matrix $W_A \in \mathbb{R}^{L \times L}$ is $W_A = \tilde{B}^\top \tilde{B}$.
4. The normalized anchor Laplacian $L_A = I_L - D_A^{-1/2} W_A D_A^{-1/2}$ is solved for its top-$K$ eigenvectors $V_K \in \mathbb{R}^{L \times K}$ in $\mathcal{O}(L^3)$.
5. The full embedding for all $N$ instances is recovered via Transfer-Cut projection:
   $$U = \tilde{B} V_K \in \mathbb{R}^{N \times K}$$
6. Unit-norm row normalization and K-Means++ discretization yields the final consensus partition $\pi^*$.
**Total complexity:** $\mathcal{O}(N L^2 + L^3)$ time and $\mathcal{O}(N L)$ memory, strictly linear in $N$!

---

## 5. Algorithmic Pseudocode & Complexity Proof

```
Algorithm 1: Invariant Core Consensus (ICC-v2)
Input: Data matrix X in R^{N x D}, target clusters K, base models M=25, anchors L=40, subspace rate 0.3
Output: Final Consensus Partition C* in {0, ..., K-1}^N, Sample Determinacy scores sigma in [0, 1]^N

1. // Stage 1: Feature Gating
2. Compute Sarle's Bimodality Coefficient BC(f_d) for all d in {1, ..., D} via Eq. (2).
3. Form active candidate feature pool F_pool = {d : BC(f_d) >= 5/9}.
4. If |F_pool| < max(10, 0.05 * D), retain top 10% highest BC features.

5. // Stage 2: Subspace Ensemble Generation
6. For m = 1 to M do:
7.   Sample random subspace z^(m) subset of F_pool of size d_sub = max(2, int(0.3 * |F_pool|)).
8.   Train base clusterer pi_m on X[:, z^(m)] to obtain cluster labels in {0, ..., K-1}.

9. // Stage 3: Exact Linear Determinacy
10. Compute M x M contingency matrices C_{m_1, m_2} in R^{K x K} for all model pairs.
11. Compute sample determinacy sigma_i for all i in {1, ..., N} via Eq. (6).

12. // Stage 4: Reduced Bipartite Spectral Consensus
13. Select L anchors from X.
14. Construct bipartite co-association matrix B in R^{N x L} via Eq. (7).
15. Compute row-normalized matrix B_tilde = D_B^{-1} B.
16. Construct reduced anchor affinity matrix W_A = B_tilde^T B_tilde in R^{L x L}.
17. Compute normalized Laplacian L_A = I_L - D_A^{-1/2} W_A D_A^{-1/2}.
18. Compute top-K eigenvectors V_K in R^{L x K} of L_A.
19. Project full embedding U = B_tilde V_K in R^{N x K}.
20. Normalize rows of U to unit L2 norm: U_{ik} = U_{ik} / ||u_i||_2.
21. Run K-Means++ on U to obtain final consensus partition C*.
22. Return C*, sigma.
```

---

## 6. Pillar 3: Multi-Domain Benchmarking, Empirical Hypotheses & Verified Results (Point 5)

### 6.1 The 13 Benchmark Datasets
| Dataset | Domain | Instances ($N$) | Features ($D$) | Clusters ($K$) | Dimension Ratio ($D/N$) | Regime Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ALLAML** | Leukemia Microarray | $72$ | $7{,}129$ | $2$ | **$99.0$** | Severe sample sparsity, extreme continuous dimensionality |
| **GLIOMA** | Brain Cancer mRNA | $50$ | $4{,}434$ | $4$ | **$88.6$** | Multiple small, overlapping histological subclasses |
| **CLL_SUB** | Leukemia Subtypes | $111$ | $11{,}340$ | $3$ | **$102.1$** | Highest dimensionality ratio; passenger mutations |
| **Colon** | Colon Tumor Biopsies | $62$ | $2{,}000$ | $2$ | **$32.2$** | High technical noise, non-Gaussian artifacts |
| **SRBCT** | Childhood Tumors | $83$ | $2{,}308$ | $4$ | **$27.8$** | Four distinct continuous pediatric tumor expressions |
| **Lymphoma** | Lymphoid Malignancies | $62$ | $4{,}026$ | $3$ | **$64.9$** | Molecular classification of diffuse large B-cell lymphoma |
| **Prostate** | Prostate Cancer | $102$ | $6{,}033$ | $2$ | **$59.1$** | Prostate tumor vs normal expression profiles |
| **Ovarian** | Ovarian Cancer Proteomics | $253$ | $15{,}154$ | $2$ | **$59.9$** | Continuous mass spectrometry proteomic profiling |
| **PBMC 3k** | Single-Cell RNA-seq | $2{,}700$ | $13{,}714$ | $8$ | **$5.1$** | Extreme zero-inflation ($>80\%$ dropout noise) |
| **Zheng68k** | Purified Immune scRNA | $1{,}000$ | $1{,}000$ | $10$ | **$1.0$** | High zero-inflation, discrete transcript count matrix |
| **20 Newsgroups** | Document Text Mining | $18{,}846$ | $10{,}000$ | $20$ | **$0.53$** | Extreme TF-IDF term sparsity, sparse text distributions |
| **Madelon** | Synthetic Feature Challenge | $500$ | $500$ | $2$ | **$1.0$** | $480$ completely random distractor dimensions |
| **Sonar** | Sonar Signals | $208$ | $60$ | $2$ | **$0.29$** | Standard low/mid-dimensional continuous baseline |

### 6.2 The 11 Baseline Algorithms
1. **K-Means (Lloyd, 1982)**: Standard distance-based single model.
2. **Hierarchical Ward (Ward, 1963)**: Agglomerative variance minimization.
3. **Spectral Clustering (Ng et al., 2001)**: Normalized graph cut.
4. **SEC (Liu et al., TKDE 2017)**: Spectral Ensemble Clustering.
5. **CSPA (Strehl & Ghosh, JMLR 2002)**: Cluster-based Similarity Partitioning.
6. **MCLA (Strehl & Ghosh, JMLR 2002)**: Meta-Clustering Algorithm.
7. **LWEA (Huang et al., TPAMI 2017)**: Locally Weighted Ensemble Clustering.
8. **LWGP (Huang et al., TPAMI 2018)**: Locally Weighted Graph Partitioning.
9. **FastMICE (Huang et al., TKDE 2023)**: Scalable Multi-View Bipartite Ensemble.
10. **DEC (Xie et al., ICML 2016)**: Deep Embedded Clustering.
11. **Li et al. (2019) Core-Halo Consensus**: Sample stability-weighted co-association consensus.

### 6.3 Verified Single Source of Truth Metrics (from `paper/numbers.tex`)
Across 2,750 model executions over the benchmark suite and dedicated adversarial audit sweeps:
1. **Ultra-High-Dimensional Biomedical Cancer Subgroup ($D/N > 20$, 6 Datasets):**  
   ICC-v2 commands **Rank #1 dominance** with Mean ARI = **0.217** (median 0.036), substantially outperforming Standard Consensus (0.037), DEC (0.045), and K-Means (0.056).
   - **Golub Leukemia ($N=72, D=7{,}129, K=2$):** ARI = **0.600 +/- 0.367**, with **54.0%** oncogenic marker recovery (27 of top 50 known driver markers recovered label-free).
   - **Khan SRBCT ($N=83, D=2{,}308, K=4$):** ARI = **0.546 +/- 0.102**.
   - **Ovarian Proteomics ($N=253, D=15{,}154, K=2$):** ARI = **0.050**, with a **5.1x speedup** over dense consensus.
2. **Omnibus Multi-Domain Benchmark Suite (13 Datasets, 11 Baselines):**  
   Across all 13 heterogeneous datasets, ICC-v2 achieves a Grand Mean ARI of **0.152** (Rank **5.23** of 11). An omnibus Friedman rank sum test yields $\chi^2_F = 9.59, p = 0.48$, with a Nemenyi critical difference $\text{CD} = 4.19$. This proves that across heterogeneous multi-domain suites, no single algorithm universally dominates, and performance differences do not reach statistical significance globally.
3. **Zero-Inflation Boundary (Sparse Text and scRNA-seq):**  
   Hierarchical Ward and DEC outperform ICC-v2 on 20 Newsgroups and Zheng68k. Heavy zero-inflation violates the continuous unimodal distractor assumption (Remark 1), inflating marginal kurtosis at zero.
4. **Missing-Data Stability (MCAR Sweep):**  
   Cluster recovery retains $\approx 108\%$ / $80\%$ / $33\%$ / $41\%$ of 0%-missing ARI at $10\%$ / $20\%$ / $30\%$ / $50\%$ missing data, demonstrating robustness up to $20\%$ dropout before degrading to baseline levels by $30\%$.
5. **Linear Computational Scaling & Extreme Scale:**  
   At extreme scale, ICC-v2 clusters $N = 10^6$ instances in **55.6 s** with peak RSS of **3.05 GB** and auxiliary bipartite graph memory of **240 MB**, achieving a **99.6% reduction** over the dense 8 TB matrix.

---

## 7. Extended Knockout Ablation Study (Section 5.2)

To isolate the operative mechanism within ICC-v2, Section 5.2 evaluates a factorial component knockout across all 6 high-dimensional biological benchmarks ($D/N > 20$, 30 random seeds):
1. **Knockout 1: Removing Feature Gating (V5 -> V3):** Subgroup mean ARI collapses from **0.217** to **0.046** (a **-78.8%** drop). On Leukemia, ARI falls from 0.600 to 0.155; on SRBCT, from 0.546 to 0.101. Feature gating is indispensable against distance concentration.
2. **Knockout 2: Removing Bipartite Anchor Graph (V5 -> V2):** Replacing bipartite anchor consensus with full dense consensus drops subgroup mean ARI from **0.217** to **0.077** ($\Delta = -0.139$, 95% CI: $[+0.065, +0.218]$). Dense averaging across noisy base partitions creates spurious dense edges, whereas anchor distillation concentrates consensus weights exclusively on stable manifold anchors.
3. **Knockout 3: Removing Consensus Ensembling (V5 -> V1):** Replacing multi-clusterer consensus with a single K-Means partition degrades subgroup mean ARI to **0.070**, with complete collapse on Leukemia (-0.017 ARI).
4. **Knockout 4: Anchor Determinacy Null Result (V5 -> V4):** Certified core anchors (V5, ARI 0.217) vs uniform random anchors (V4, ARI 0.198) yields a null result ($\Delta = +0.019$, 95% CI: $[-0.039, +0.082]$, paired Wilcoxon $W = 9.0, p = 0.84$). Bipartite graph compression rather than anchor certification is the primary operational driver.

---

## 8. Practical Real-World Applications & Clinical Case Studies (Section 6)

1. **Translational Oncology & Cancer Subtyping (`examples/clinical_cancer_subtyping.py`):** Unsupervised subtyping on Golub Leukemia (ARI = 0.600) and Khan SRBCT (ARI = 0.546), recovering 54.0% of top oncogenic driver genes.
2. **Point-of-Care Inductive Biopsy Decision Support (`examples/realtime_patient_projection.py`):** Inductive query evaluation in **22.6 microseconds** per patient biopsy with $(1 - \alpha = 90\%)$ conformal validity guarantees.
3. **Million-Scale Single-Cell Transcriptomics:** Clusters $N = 10^6$ cells in 55.6 s with 240 MB graph memory, bypassing the dense 8 TB RAM barrier.
4. **Conformal Inductive Consensus Clustering (`src/cicc/`):** Split-conformal prediction sets (`conformal.py`), target-decoy / knockoff FDR feature screening with mirror statistics $W_d = |T_d| - |\tilde{T}_d|$ (`decoy.py`), and episodic semantic agent memory (`memory.py`).

---

## 9. Theoretical Foundations & Asymptotic Complexity

### 9.1 Theorem 1 (Inductive Assignment Convergence)
For an unseen query instance $\mathbf{x}_{\text{new}} \in \mathbb{R}^D$, let $\mathcal{F}_{\text{active}}$ denote active candidate features selected by VSSG / BGSS. The inductive cluster assignment is:
$$\hat{y}(\mathbf{x}_{\text{new}}) = \arg\min_{k \in \{0, \dots, K-1\}} \|\mathbf{x}_{\text{new}}[\mathcal{F}_{\text{active}}] - \mathbf{c}_k[\mathcal{F}_{\text{active}}\|_2$$
where $\mathbf{c}_k = \frac{\sum_{i: \hat{y}_i = k} \sigma_i \cdot \mathbf{x}_i}{\sum_{i: \hat{y}_i = k} \sigma_i}$ is the stability-calibrated centroid. Assuming sub-Gaussian cluster conditional distributions on the signal subspace, query misclassification probability satisfies:
$$\Pr(\hat{y}(\mathbf{x}_{\text{new}}) \neq y^*(\mathbf{x}_{\text{new}})) \le (K - 1) \exp\left( - \frac{\Delta_{\min}^2}{8 \sigma_{\max}^2} \right)$$
where $\Delta_{\min}$ is the inter-cluster margin on $\mathcal{F}_{\text{active}}$ and $\sigma_{\max}^2$ is within-cluster variance.

### 9.2 Theorem 2 (Asymptotic Complexity Bounds)
1. **Time Complexity:**
   - VSSG multimodality screening: $\mathcal{O}(N \cdot D)$.
   - Base model fits: $\mathcal{O}(M \cdot (N \cdot d_{\text{sub}} \cdot K))$ where $d_{\text{sub}} \le 0.3 D$.
   - Exact Linear Determinacy: $\mathcal{O}(M^2 N + M^2 K^2)$.
   - Bipartite Graph Construction: $\mathcal{O}(M \cdot N \cdot L)$.
   - Reduced Spectral Decomposition: $\mathcal{O}(N L^2 + L^3)$.
   - **Total Training Time:** $\mathcal{O}(N(D + M d_{\text{sub}} K + M^2 + M L) + L^3)$: strictly linear in $N$.
2. **Space Complexity:** $\mathcal{O}(N \cdot L)$ auxiliary storage, compared to $\mathcal{O}(N^2)$ for standard consensus.
3. **Inductive Query Latency:** $\mathcal{O}(K \cdot |\mathcal{F}_{\text{active}}|)$ operations, independent of $N$.

---

## 10. Deliverables, Timeline & Publication Strategy

### 10.1 Project Execution Milestones
* **Phase 1 (Theory & Scaffolding):** Mathematical formulation of Proposition 1 (Sarle bound) and Proposition 2 (Linear Determinacy Identity). Setup of reproducible dataset pipeline.
* **Phase 2 (Implementation & Baselines):** Production-grade Python package (`icc`) with 11 baselines (K-Means, Ward, Spectral, SEC, CSPA, MCLA, LWEA, LWGP, FastMICE, DEC, Li et al. Core-Halo).
* **Phase 3 (Large-Scale Benchmarks & Adversarial Audit):** 2,750 model executions across 13 primary datasets; adversarial research audit sweeps (A1 through A4, E1, E3, E5, E6).
* **Phase 4 (Journal Manuscript & Open-Source Release):** Springer Nature DAMI submission (`paper/main.tex`), research audit dossier, open-source GitHub release v2.1.0.

### 10.2 Clear Team Responsibility Matrix
* **Akash Kundu (Lead):** Mathematical formulation of Linear Determinacy Identity (Proposition 2) and Bipartite Spectral Transfer-Cut; core architecture of `src/icc/consensus_v2.py`; lead author for journal manuscript.
* **Trinankur Guha:** Finite-sample Sarle Bimodality Coefficient derivation and VSSG multimodality screening; subspace diversity constraints.
* **Rupankar Ghatak:** Experimental harness, per-process scaling benchmark (E6), missing-data evaluation, and statistical Wilcoxon/Friedman tests.
* **Anubhav Naskar:** Implementation and calibration of the 11 baseline solvers (`src/icc/baselines/`); curation of the 13 benchmark datasets and downstream validation suite.

---

## 11. Summary of Defensible Novelty for Springer Nature DAMI

1. **Exact Linear-Memory Sample Determinacy:** First algorithm to compute sample-level co-association determinacy in $\mathcal{O}(M^2 N + M^2 K^2)$ time and $\mathcal{O}(N)$ space, eliminating the $N \times N$ matrix bottleneck.
2. **Analytical Characterization of the Operating Boundary:** Formal proof of the zero-inflation boundary (Remark 1), explaining both Rank #1 dominance on continuous cancer assays ($D/N > 20$, ARI 0.217) and the ceiling on sparse scRNA-seq matrices.
3. **Anchor-Space Perturbation Profiling (ASPP):** Closed-form stability diagnostics profiling 5 perturbation families strictly in $\mathcal{O}(N L)$ memory.
4. **Adversarial Audit Integrity:** Transparent reporting of empirical operating envelopes, negative results (label-free selector limits, anchor determinacy null result $p=0.84$), and calibrated claims, providing a gold-standard benchmark for the machine learning community.
