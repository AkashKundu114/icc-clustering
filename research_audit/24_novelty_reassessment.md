# ADVERSARIAL PEER REVIEW & NOVELTY AUDIT REPORT
**Target Journal:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Track:** Research / Survey Track  
**Manuscript Title:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Repository Audited:** `AkashKundu114/icc-clustering` (Release v2.1.0)  
**Lead Author / Faculty Mentor:** Akash Kundu / Prof. Kalyan Kumar Das  
**Auditor Persona:** `roo_reviewer` (Specialized Scientific Peer-Reviewer & DMKD Area Chair Auditor)  
**Date of Audit:** November 1, 2026  

---

## 1. Executive Summary & Review Disposition

### 1.1 Overall Assessment
The submitted manuscript undertakes an investigation of a recognized vulnerability in unsupervised learning: the **stability–accuracy discordance trap**, wherein resampling-based cluster stability metrics exhibit high agreement ($\text{Stab} \ge 0.50$) while cluster partitions exhibit near-zero agreement with biological reference labels ($\text{ARI} \le 0.05$). The authors use an experimental vehicle dubbed **Gated Anchor Consensus (GAC)**—combining Sarle's Bimodality Coefficient (BGSS), random subspace ensembling, and bipartite anchor graph compression—to dissect which algorithmic components mitigate or fail to mitigate this discordance.

The manuscript benefits from an empirical re-orientation: earlier drafts claiming universal algorithmic superiority have been replaced with a self-critical narrative that acknowledges non-significant omnibus results (Friedman $p = 0.40$), documents negative results (e.g., determinacy anchor certification adding nothing over random anchors, $p = 0.84$), and admits that performance gains are heavily concentrated in just two oncology cohorts (Leukemia and SRBCT).

However, from the standpoint of an adversarial reviewer for **Springer Data Mining and Knowledge Discovery (DMKD)**, several critical technical and methodological vulnerabilities preclude immediate acceptance. Most egregiously, the repository's baseline suite relies on an unfaithful surrogate stub for FastMICE (labeled "FastMVC" in the manuscript), while failing to cite the underlying literature. Furthermore, the theoretical contributions (Propositions 1 and 2) represent standard statistical moment calculations and known matrix identities rather than publishable theoretical advances, and Proposition 2 computes a determinacy metric that the authors' own ablations prove is empirically useless.

### 1.2 Explicit Disposition Recommendation
**Recommendation:** **MAJOR REVISION** (Borderline Reject if baseline attribution and surrogate evaluation are not resolved immediately).

```
┌────────────────────────────────────────────────────────────────────────┐
│                        EVALUATION SCORECARD                            │
├───────────────────────────────────┬──────────────┬─────────────────────┤
│ Evaluation Dimension              │ Score (1-10) │ Reviewer Assessment │
├───────────────────────────────────┼──────────────┼─────────────────────┤
│ Scientific Rigor & Transparency   │ 8.5 / 10     │ High (honest stats) │
│ Methodological Soundness          │ 6.0 / 10     │ Surrogate baseline  │
│ Novelty of Algorithmic Pipeline   │ 4.5 / 10     │ Component assembly  │
│ Novelty of Theoretical Derivation │ 4.0 / 10     │ Textbook identities │
│ Empirical Breadth & Generalization│ 5.5 / 10     │ 2-cohort dominance  │
│ Citation Vintage & Completeness   │ 7.0 / 10     │ Key omissions       │
│ Reproducibility & Code Artifacts  │ 9.0 / 10     │ Frozen seed audits  │
└───────────────────────────────────┴──────────────┴─────────────────────┘
```

---

## 2. Deep Comparison Against the Closest 5 Prior Art Algorithms

To evaluate whether GAC constitutes genuine innovation or incremental component assembly, we audit it against the five closest prior art frameworks across mathematical formulations, input assumptions, and operational failure modes.

### Comparative Algorithmic Taxonomy Matrix

| Algorithm | Canonical Reference | Core Optimization / Mechanism | Feature Selection Strategy | Graph Construction & Memory | Handling of Distractor Noise ($D \gg N$) | Primary Failure Mode |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Sparse K-Means (SKM)** | Witten & Tibshirani (*JASA* 2010) [61] | Alternating maximization of between-cluster sum of squares: $\max_{\mathbf{w}, \mathcal{C}} \sum_d w_d \text{BCSS}_d$ s.t. $\|\mathbf{w}\|_2 \le 1, \|\mathbf{w}\|_1 \le s$ | Coupled joint $L_1$ lasso-style weight regularization | Single-model centroid assignments; $O(N \cdot D)$ memory | **Optimal / Filtered:** Soft-thresholds noise dimensions to zero weights | Initial cluster assignment overfits noise before weights converge; sensitive to tuning parameter $s$ |
| **Bipartite Consensus (FastMICE / FastMVC)** | Huang et al. (*IEEE TKDE* 2023) [201]; Li et al. (*IEEE TKDE* 2015) | Multi-view / ensemble bipartite graph partitioning; solves consensus via Transfer-Cut on anchor kernel | None (operates on raw ambient feature space) | Rectangular bipartite graph $Z \in \mathbb{R}^{N \times m}$; $O(N \cdot m)$ memory | **Highly Susceptible:** Pairwise distances to anchors concentrate in ambient space | Generates distorted anchors and spurious consensus affinities under distance concentration |
| **Fast Clustering with Anchor Guidance (FCAG)** | Nie et al. (*IEEE TPAMI* 2024) [50] | Single-model anchor affinity graph with continuous distance-decay weights: $z_{ij} = \frac{d_{i,s+1}-d_{ij}}{s d_{i,s+1}-\sum d_{il}}$ | None (raw Euclidean distances) | Sample-to-anchor affinity $Z \in \mathbb{R}^{N \times m}$ with anchor Laplacian; $O(N \cdot m)$ | **Highly Susceptible:** Euclidean metric concentration erodes anchor-to-point contrast | Distance concentration flattens neighbor affinities ($d_{\max} \approx d_{\min}$), yielding $\Delta = +0.503$ discordance |
| **Single-Cell Consensus Clustering (SC3)** | Kiselev et al. (*Nat Methods* 2017) | Multi-metric distance fusion (Euclidean, Pearson, Spearman) + spectral transformation + consensus matrix | Rare gene prevalence filtering + expression variance | Quadratic co-association matrix $S \in [0, 1]^{N \times N}$; $O(N^2)$ storage | **Moderately Resilient:** Multi-metric fusion handles non-linear scaling | Quadratic memory explosion at $N > 10^4$; relies on variance rather than multimodality |
| **Hierarchical Consensus Forests (CoHiRF)** | Belucci et al. (*arXiv* 2025) [102] | Unsupervised random forest ensemble with strict unanimity core extraction ($\theta \ge 0.80$) | Unguided random feature subspaces (rate $\approx 0.15$) | Pairwise co-occurrence matrix on filtered core; $O(N_{\text{rep}}^2)$ | **Resilient to noise, but high collapse rate:** Rejects noise voters | Extreme singleton and cluster collapse under high noise ($60\%\text{--}100\%$ on Prostate, Ovarian, CNS) |
| **GAC (Proposed Vehicle)** | Kundu et al. (Manuscript Section 3) | Sarle's Bimodality Coefficient filter (BGSS) + random subspaces + bipartite anchor consensus (Transfer-Cut) | Univariate marginal filter: top-$\alpha$ ranking of Sarle's $BC_d$ ($BC > 5/9$) | Rectangular bipartite co-occurrence $B \in [0,1]^{N \times L}$; $O(N \cdot L)$ memory | **Conditionally Resilient:** Isolates bimodal coordinates prior to base clustering | Fails on diffuse/correlated non-bimodal signal (Prostate $\Delta = +0.847$, CNS $\Delta = +0.542$), zero-inflation, and non-linear XOR |

---

### Detailed Mathematical & Algorithmic Distinctions

#### 1. GAC vs. Sparse K-Means (Witten & Tibshirani, 2010)
- **Feature Selection Coupling:** SKM solves a constrained continuous optimization problem where feature weights $w_d$ and cluster partitions $\mathcal{C}$ are jointly optimized. GAC completely *decouples* feature screening from cluster discovery: BGSS acts as a pre-clustering marginal filter that ranks features by Sarle's $BC$ in $O(ND)$ time, discarding the bottom $(1-\alpha)$ fraction before any base model runs.
- **Ensemble vs. Single-Model:** SKM is a single-model iterative centroid solver prone to getting trapped in local optima when $D \gg N$. GAC generates an ensemble of $M$ base partitions across random subsets drawn from the pre-screened pool $\mathcal{F}_{\text{active}}$.
- **Empirical Contrast:** On the six high-$D$ biomedical cohorts, SKM attains an average ARI of only $0.051 \pm 0.046$ (Table 8 in manuscript), failing to beat ambient K-Means ($0.051$). GAC achieves $0.217 \pm 0.312$. However, SKM's optimization framework is mathematically principled and guarantees convergence to a stationary point of the penalized objective, whereas GAC's pipeline is a heuristic cascade of independent stages.

#### 2. GAC vs. Bipartite Consensus / FastMICE (Huang et al., 2023; Li et al., 2015)
- **Where Bipartite Graphs Are Built:** FastMICE and Li et al. (2015) construct bipartite graphs either directly on base cluster indicators across ambient features or by projecting ambient samples to anchors. Under $D \gg N$, distance concentration erodes ambient anchors. GAC executes random subspace base clustering *strictly within* the BGSS-filtered candidate pool $\mathcal{F}_{\text{active}}$, ensuring that the partitions forming the bipartite graph $B \in [0, 1]^{N \times L}$ are built on informative dimensions.
- **Spectral Solver Equivalence:** Once the rectangular bipartite matrix is constructed, GAC's downstream Transfer-Cut projection ($W_{\text{anchor}} = B_{\text{norm}}^T B_{\text{norm}}$, $L_{\text{anchor}} V = \lambda V$, $U = B_{\text{norm}} V$) is *algebraically identical* to the bipartite spectral solvers established by Li et al. (2015) and Nie et al. (2024). GAC introduces **no algorithmic novelty** in the bipartite spectral solver stage.

#### 3. GAC vs. Anchor Guidance / FCAG (Nie et al., 2024)
- **Nature of the Graph:** FCAG constructs continuous distance-decay affinity weights $Z_{ij} \in \mathbb{R}$ based on continuous Euclidean distances to $s$-nearest anchors in ambient space. GAC builds a discrete co-occurrence matrix $B_{ia} \in [0, 1]$ voting whether instance $i$ and anchor $a$ co-occur in the same cluster across $M$ subspace ensemble partitions.
- **Failure Mode in High Dimensions:** FCAG collapses under high-dimensional noise because ambient distances to anchors concentrate ($d_{\max} - d_{\min} \to 0$), driving FCAG into stability-accuracy discordance on Colon, CNS, and Prostate (mean accuracy $-0.003$, stability $0.684$). GAC bypasses continuous distance concentration in graph construction by operating on discrete cluster co-membership.

#### 4. GAC vs. Single-Cell Consensus Clustering / SC3 (Kiselev et al., 2017)
- **Consensus Scale & Memory:** SC3 builds a full $N \times N$ consensus matrix $S$, incurring $O(N^2)$ memory and $O(N^3)$ spectral decomposition. GAC builds an $N \times L$ bipartite graph, scaling in $O(NL)$ memory and $O(L^3)$ eigensolving.
- **Screening Criterion:** SC3 relies on gene dropout rates and variance thresholds. As proven in the manuscript's interpretability audit (Section 6.5, Fig. 10), variance thresholds select pure distractor noise in microarray data (hypergeometric $p = 0.481$), whereas Sarle's $BC$ successfully captures 27 of 50 diagnostic markers ($p = 1.38 \times 10^{-10}$).
- **Omission in Manuscript:** SC3 is the universal gold standard for consensus clustering in high-dimensional genomics ($D \sim 10^4$). The manuscript's failure to benchmark against SC3 or discuss it in Section 2 is a significant omission.

#### 5. GAC vs. CoHiRF (Belucci et al., 2025)
- **Consensus Strategy:** CoHiRF applies random forest trees on random subspaces and enforces strict unanimity ($\theta \ge 0.80$) to extract a core partition, setting discordant pairs to zero.
- **Degeneracy Breakdown:** CoHiRF's strict thresholding causes catastrophic singleton collapse under extreme noise: in Table 16 of the manuscript, CoHiRF exhibits degeneracy rates of $56.7\%$ (Colon), $93.3\%$ (CNS), $86.7\%$ (Leukemia), $60.0\%$ (Prostate), and $100.0\%$ (Ovarian). GAC uses smooth spectral Transfer-Cut, avoiding singleton fragmentation (degeneracy rate $0.0\%$ across all cohorts).

---

## 3. Evaluation of Theoretical Contributions

The manuscript presents two formal propositions in Section 3: **Proposition 1** (Conditional Multimodality Separation Bound) and **Proposition 2** (Exact Determinacy Identity). An adversarial audit reveals severe concerns regarding novelty and practical relevance.

### 3.1 Proposition 1: Conditional Multimodality Separation Bound ($\Delta / \sigma_0 > 1.854$)
- **Formal Statement in Manuscript:** For a symmetric two-component Gaussian mixture $0.5\mathcal{N}(-\Delta, \sigma_0^2) + 0.5\mathcal{N}(\Delta, \sigma_0^2)$, Sarle's Bimodality Coefficient satisfies $BC > 5/9$ if and only if component separation exceeds $\frac{\Delta}{\sigma_0} > \sqrt{\frac{3 + \sqrt{15}}{2}} \approx 1.854$.
- **Mathematical Audit:**
  - Let $\theta = (\Delta / \sigma_0)^2$. Mixture variance is $\sigma^2 = \sigma_0^2(1 + \theta)$.
  - The fourth central moment is $\mu_4 = \sigma_0^4(3 + 6\theta + \theta^2)$.
  - Pearson kurtosis is $\beta_2 = \frac{\mu_4}{\sigma^4} = \frac{3 + 6\theta + \theta^2}{(1 + \theta)^2}$.
  - Skewness $\gamma = 0$ by symmetry. Thus, $BC = \frac{1}{\beta_2} = \frac{(1 + \theta)^2}{3 + 6\theta + \theta^2}$.
  - Setting $BC > 5/9 \iff 9(1 + 2\theta + \theta^2) > 5(3 + 6\theta + \theta^2) \iff 2\theta^2 - 6\theta - 3 > 0$.
  - Solving the quadratic gives $\theta > \frac{3 + \sqrt{15}}{2} \approx 3.4365$, whence $\frac{\Delta}{\sigma_0} > \sqrt{3.4365} \approx 1.85377 \approx 1.854$.
  - **Verdict on Correctness:** The algebraic derivation is completely correct.
- **Verdict on Theoretical Novelty:** **NEGLIGIBLE (Standard Textbook Exercise)**.
  - Deriving the kurtosis of an equal-weight two-component Gaussian mixture dates back to Karl Pearson (1894).
  - Solving for $BC = 5/9$ is an elementary algebraic consequence of Sarle's 1983 definition, documented in standard psychometric and statistical literature (e.g., Knapp 2007; Pfister et al. 2013; Freeman & Dale 2013).
  - Elevating this standard moment exercise to a numbered "Proposition" claiming theoretical insight for DMKD represents inflation of mathematical novelty.
- **Statistical Fragility & Real-World Breakdown:**
  - The derivation assumes equal component weights ($p = 0.5$) and identical variances. In clinical oncology, subtype prevalences are heavily imbalanced (e.g., $90\% / 10\%$). For an imbalanced mixture, skewness $\gamma \neq 0$ and kurtosis changes non-linearly, rendering the threshold $1.854$ invalid.
  - Remark 1 in the manuscript admits that under zero-inflation (common in single-cell count data), $BC \to 1.0$ for pure noise. Thus, the bound is brittle and cannot be applied without strict continuous, symmetric Gaussian assumptions.

---

### 3.2 Proposition 2: Exact Linear-Memory Determinacy Identity
- **Formal Statement in Manuscript:** For an ensemble partition matrix $P \in \{0, \dots, K-1\}^{M \times N}$, quadratic sample determinacy $\sum_{j=1}^N S_{ij}^2$ can be computed in $O(M^2 N + M^2 K^2)$ time and $O(N + K^2)$ auxiliary memory using base contingency matrices:
$$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i))$$
- **Mathematical Audit:**
  - Let $H \in \{0, 1\}^{N \times MK}$ denote the block cluster membership matrix. The co-association matrix is $S = \frac{1}{M} H H^T$.
  - The squared matrix is $S^2 = \frac{1}{M^2} H (H^T H) H^T$.
  - The inner matrix $H^T H \in \mathbb{N}^{MK \times MK}$ is composed of $M \times M$ block contingency matrices $C_{m_1, m_2} = H_{m_1}^T H_{m_2} \in \mathbb{N}^{K \times K}$.
  - The $i$-th diagonal element of $S^2$ (or row sum of element-wise squares) directly equals the stated contingency lookup.
  - **Verdict on Correctness:** Algebraically sound and computationally verifiable.
- **Verdict on Theoretical Novelty:** **LOW (Known Matrix Factoring Trick)**.
  - Representing co-association operations via the cluster incidence matrix product $H (H^T H) H^T$ is a recognized formulation in ensemble clustering (e.g., Fern & Brodley 2004; Li et al. 2015; Huang et al. 2017).
  - Calling this an original theoretical discovery overstates standard matrix manipulation.
- **The "Useless Core" Paradox (Fatal Reviewer Vulnerability):**
  - The entire theoretical justification for Proposition 2 is to enable efficient sample determinacy calculation $\sigma_i$ so that high-determinacy "core" anchors can be selected for bipartite consensus.
  - However, in the manuscript's own ablation study (Section 6.4, Table 13, Knockout 4):
    $$V_5 \text{ (Certified Core Anchors)} - V_4 \text{ (Uniform Random Anchors)} = +0.019 \quad (95\%\text{ CI: } [-0.040, +0.082], p = 0.84)$$
  - **The authors' own empirical data prove that determinacy-based anchor certification yields NO measurable benefit over simple uniform random sampling ($p = 0.84$)!**
  - Proposition 2 therefore computes a metric that is empirically inert within the GAC pipeline. Highlighting a computational shortcut for an empirically useless component as a core theoretical contribution is an invitation for rejection.

---

## 4. Audit of Citation Vintage, Coverage & Baseline Integrity

### 4.1 Citation Vintage Analysis
An analysis of `paper/references.bib` shows healthy representation of contemporary literature:
- Total references: 47
- Papers from 2024–2026: **22 references (46.8%)**
- Journals represented: *Data Mining and Knowledge Discovery* (Fettal et al. 2026, Patron et al. 2026), *IEEE TPAMI* (Nie et al. 2024), *IEEE TKDE* (Zhao et al. 2026, Xu et al. 2026, Gao et al. 2026, Ma et al. 2025), *Journal of the American Statistical Association* (Wang & Ye 2026), *Annals of Statistics* (Zhang & Zhou 2024), *Pattern Recognition* (Zhang et al. 2025, Wang et al. 2026).
- The manuscript satisfies DMKD expectations for contemporary literature engagement.

---

### 4.2 Critical Omissions in Foundational Literature

Despite recent citations, the manuscript exhibits conspicuous blind spots in five seminal areas:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               IDENTIFIED LITERATURE BLIND SPOTS                                  │
├──────────────────────────┬──────────────────────────────────────────┬────────────────────────────┤
│ Domain Area              │ Crucial Missing Citations                │ Impact on Manuscript       │
├──────────────────────────┼──────────────────────────────────────────┼────────────────────────────┤
│ 1. Consensus Foundations │ • Monti et al. (Mach Learn 2003)         │ Foundational consensus     │
│                          │ • Wilkerson & Hayes (Bioinform 2010)     │ clustering in oncology     │
│                          │ • Tibshirani et al. (JRSS-B 2001)        │ completely unacknowledged  │
├──────────────────────────┼──────────────────────────────────────────┼────────────────────────────┤
│ 2. Statistical           │ • Hartigan & Hartigan (Ann Stat 1985)    │ Sarle (1983) is an un-     │
│    Multimodality         │ • Silverman (JASA 1981)                  │ reviewed tech report; Dip  │
│                          │ • Wang et al. (Biometrics 2009)          │ Test is the gold standard  │
├──────────────────────────┼──────────────────────────────────────────┼────────────────────────────┤
│ 3. Anchor Graph Pioneers │ • Liu et al. (ICML 2010 Anchor Graph)    │ Cites Nie 2024 but omits   │
│                          │ • Chen & Cai (IJCAI 2011 Landmark)       │ the original foundational  │
│                          │ • Li et al. (IEEE TKDE 2015 Bipartite)   │ anchor graph inventors     │
├──────────────────────────┼──────────────────────────────────────────┼────────────────────────────┤
│ 4. Single-Cell & High-D  │ • Kiselev et al. (Nat Methods 2017 SC3)  │ Leading high-D consensus   │
│    Genomics              │ • Hao et al. (Cell 2021 Seurat)          │ baseline omitted from both │
│                          │ • Lin et al. (Genome Biol 2017 CIDR)     │ benchmarks and related work│
├──────────────────────────┼──────────────────────────────────────────┼────────────────────────────┤
│ 5. Model Order Selection │ • Senbabaoglu (2014 PAC) cited, but      │ Unknown-K evaluation lacks │
│    Under Noise           │   ConsensusClusterPlus & Gap missing     │ comparative baselines      │
└──────────────────────────┴──────────────────────────────────────────┴────────────────────────────┘
```

1. **Monti et al. (2003) & Wilkerson & Hayes (2010):** Monti et al. (*Machine Learning*, 2003) introduced consensus clustering specifically for class discovery in cancer genomics. Wilkerson & Hayes (*Bioinformatics*, 2010) created `ConsensusClusterPlus`, the de facto standard tool used across computational oncology. Omitting both while claiming to study consensus stability on cancer cohorts is unacceptable.
2. **Hartigan & Hartigan (1985) Dip Test:** Warren Sarle's 1983 paper is an un-reviewed SAS Technical Report (A-108). In mathematical statistics, the definitive non-parametric test for unimodality vs. multimodality is **Hartigan's Dip Test** (*The Annals of Statistics*, 1985). The manuscript must discuss why a heuristic moment-based coefficient was selected over the dip test.
3. **Liu et al. (2010) & Chen & Cai (2011):** The manuscript cites Nie et al. (2024) for anchor graphs but fails to cite the foundational papers that invented anchor graph spectral clustering: Liu, He, and Chang (*ICML* 2010) and Chen & Cai (*IJCAI* 2011).

---

### 4.3 Critical Baseline Integrity Crisis: The "FastMVC" Surrogate Stub

An inspection of the repository source code reveals an alarming methodological and ethical issue:

- **What the Manuscript Claims:**
  In Table 1, Table 2, Table 3, Table 16, and in the Abstract (Line 58) and Introduction (Line 86), the authors report evaluations of **FastMVC**, explicitly naming it alongside FCAG and FCM as one of only three algorithms displaying non-degenerate stability-accuracy discordance across three cohorts.
- **What the Code Actually Implements:**
  In `src/icc/baselines/anchor.py` (lines 5–7 and 281–283):
  ```python
  # FastMVC: [STUB] random-subspace anchor-graph SURROGATE.
  # It is NOT a faithful implementation of FastMICE (Huang, Wang, Lai;
  # IEEE TKDE 2023, doi:10.1109/TKDE.2023.3236698), the closest published method.
  # Do not report it as that method.
  ```
- **The Bibliographic Disconnect:**
  Neither FastMVC (Tao et al., 2017) nor FastMICE (Huang et al., 2023) has a citation entry in `paper/references.bib` or is cited with `\cite{...}` in `paper/main.tex`.
- **Reviewer Assessment:**
  **This is a critical flaw.** Reporting an internal surrogate stub as an established baseline, using it to substantiate the paper's core empirical thesis ("FastMVC exhibits discordance on three cohorts"), and failing to cite the publication violates scientific benchmarking standards. If an external DMKD reviewer inspects the code, this will trigger an immediate rejection.

---

## 5. Overclaiming, Rhetoric, and Tone Audit

### 5.1 Manuscript Calibration vs. Repository Hype
The authors deserve credit for cleaning up the manuscript text (`paper/main.tex`):
- The title was changed from an algorithmic claim to an empirical investigation: *"An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts"*.
- The abstract and conclusions openly report that the omnibus Friedman test is not significant ($p = 0.40$), that determinacy anchors add no benefit ($p = 0.84$), and that gains are concentrated in Leukemia ($+0.398$) and SRBCT ($+0.447$).

However, **severe overclaiming persists in the repository documentation and docstrings**, which reviewers will inspect:
1. `README.md` (Lines 19–24): Claims that ICC-v2 *"resolves these fundamental challenges through four mathematically calibrated mechanisms"* and highlights *"conformal uncertainty quantification with finite-sample coverage guarantees"*, none of which are validated in the DMKD manuscript.
2. `docs/literature/papers.md` (Line 131): Proclaims *"ICC-v2 attains Rank #1 dominance with Mean ARI = 0.217... outperforming Standard Consensus"*, contradicting the manuscript's own Friedman test ($p = 0.40$) linking all 12 methods in a single equivalence clique.
3. `paper/main.tex` (Line 139, Table 1): GAC is classified as *"Resilient"* to high-dimensional noise, while other methods are labeled *"Susceptible"*. In reality, GAC exhibits catastrophic discordance on Prostate ($\Delta = +0.847$) and CNS ($\Delta = +0.542$). It is not resilient; it is conditionally effective when marginal multimodality is present.

---

## 6. Categorized Findings & Severity Audit

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 AUDIT FINDINGS BY SEVERITY                                       │
├──────────┬──────────────────────────────────────────────────────┬────────────────────────────────┤
│ Severity │ Finding Description                                  │ Required Remediation           │
├──────────┼──────────────────────────────────────────────────────┼────────────────────────────────┤
│ CRITICAL │ 1. FastMVC baseline is an unfaithful surrogate stub  │ Replace with genuine FastMICE  │
│          │    explicitly warned against in source code          │ ADMM solver or remove from core│
│          │                                                      │ discordance claims; add citation│
├──────────┼──────────────────────────────────────────────────────┼────────────────────────────────┤
│ CRITICAL │ 2. Omission of seminal consensus (Monti 2003) and    │ Add formal bibliographic       │
│          │    statistical multimodality (Hartigan 1985) priors  │ coverage in Section 2          │
├──────────┼──────────────────────────────────────────────────────┼────────────────────────────────┤
│ MAJOR    │ 3. Two-dataset concentration: GAC gain rests almost  │ Frame GAC strictly as a case   │
│          │    entirely on Leukemia (+0.398) and SRBCT (+0.447)  │ study; state clearly that it   │
│          │                                                      │ fails on diffuse cohorts       │
├──────────┼──────────────────────────────────────────────────────┼────────────────────────────────┤
│ MAJOR    │ 4. "Useless Core" disconnect: Proposition 2 computes │ Demote Proposition 2 to an     │
│          │    a determinacy score that ablation proves inert   │ implementation remark; remove  │
│          │    (Knockout 4, p = 0.84)                            │ claims of theoretical breakthrough│
├──────────┼──────────────────────────────────────────────────────┼────────────────────────────────┤
│ MAJOR    │ 5. Proposition 1 overstatement: standard moment      │ Re-label Proposition 1 as an   │
│          │    derivation framed as theoretical insight          │ analytical property of Sarle's │
│          │                                                      │ index; note asymmetry limits   │
├──────────┼──────────────────────────────────────────────────────┼────────────────────────────────┤
│ MINOR    │ 6. Discrepancy between repository marketing          │ Synchronize README.md with the │
│          │    (README.md / papers.md) and honest manuscript     │ restrained manuscript narrative│
├──────────┼──────────────────────────────────────────────────────┼────────────────────────────────┤
│ MINOR    │ 7. Asymptotic linear claims vs. hardware power-law:  │ Acknowledge memory-bus scaling │
│          │    empirical beta reaches 1.09-1.20 past N = 10^5    │ constraints past N = 10^5      │
└──────────┴──────────────────────────────────────────────────────┴────────────────────────────────┘
```

---

## 7. Reviewer Rejection Vectors (Adversarial Simulation)

If submitted in its current state, an experienced DMKD reviewer will deploy the following technical rejection arguments:

1. **Rejection Vector 1: Surrogate Baseline Misrepresentation.**  
   *"The authors claim that FastMVC suffers from stability-accuracy discordance. Yet, examining their repository reveals that 'FastMVC' is a 20-line stub with random feature subsets that the authors themselves annotate as 'NOT a faithful implementation of FastMICE... Do not report it as that method.' Furthermore, neither FastMVC nor FastMICE is cited in the references. Benchmarking against self-constructed surrogate models to demonstrate competitor failure violates empirical rigor standards."*

2. **Rejection Vector 2: Lack of Generalizability (Two-Cohort Phenomenon).**  
   *"The empirical advantage of the proposed BGSS filter is confined to two datasets from the early 2000s: Golub Leukemia ($N=72, D=7{,}129$) and Khan SRBCT ($N=83, D=2{,}308$). Across the remaining 11 benchmark datasets, GAC provides no statistically meaningful improvement, yielding an omnibus Friedman test of $p = 0.40$. On Prostate ($D=12{,}600$) and CNS ($D=7{,}129$), GAC exhibits the exact same discordance trap it claims to diagnose ($\text{ARI} \le 0.012, \text{Stab} \ge 0.549$). The method is not a general solution for high-dimensional noise."*

3. **Rejection Vector 3: Theoretical Superfluity.**  
   *"Section 3 dedicates substantial formal space to Proposition 2 (linear determinacy identity). Yet in Section 6.4 (Table 13), the authors report that filtering anchors by determinacy achieves an ARI difference of only $\Delta = +0.019$ ($p = 0.84$) compared to picking anchors uniformly at random. Why is DMKD publishing an exact computational identity for an algorithmic step that is proven to have no statistical or empirical utility?"*

4. **Rejection Vector 4: Omission of Domain De Facto Standards.**  
   *"The paper repeatedly positions itself within computational biology and transcriptomics. Yet it omits SC3 (Nature Methods 2017), ConsensusClusterPlus (Bioinformatics 2010), and Seurat (Cell 2021). Comparing exclusively against classical Lloyd's K-Means and standard Ward linkage while ignoring the tools biologists actually use in high-dimensional clustering undermines the practical relevance of the findings."*

---

## 8. Actionable Remediation Checklist for DMKD Submission Readiness

To neutralize these rejection vectors and make the manuscript submission-ready for DMKD, complete the following mandatory revisions:

- [ ] **1. Cleanse Baseline Nomenclature and Replace FastMVC Stub:**
  - Either integrate the true ADMM-based FastMICE solver from Huang et al. (2023) or re-label the baseline as *"Random-Subspace Anchor Bipartite Baseline (RS-AB)"*, explicitly clarifying in Section 4 and Table 1 that it is an ablation baseline rather than an official competitor.
  - Add formal citations for Huang et al. (TKDE 2023) and Li et al. (TKDE 2015) in `references.bib` and `paper/main.tex`.
- [ ] **2. Demote and Re-Frame Theoretical Propositions:**
  - Re-frame **Proposition 1** as *"Lemma 1 (Analytical Separation Bound for Symmetric Gaussian Mixtures)"*, noting explicitly that it represents an analytical characterization of Sarle's (1983) coefficient under idealized assumptions, and discuss the impact of sample imbalance ($p \neq 0.5$) and zero-inflation.
  - Re-frame **Proposition 2** as *"Proposition 2 (Contingency Table Determinacy Evaluation)"*. Add a candid sentence in Section 3 and Section 6.4 stating: *"While Proposition 2 provides an exact algebraic acceleration for sample determinacy, our ablation in Section 6.4 reveals that determinacy-certified anchors perform comparably to uniform random anchors in practice ($p = 0.84$); we provide the identity for algorithmic completeness."*
- [ ] **3. Expand Foundational Bibliography:**
  - Add **Monti et al. (2003)** and **Wilkerson & Hayes (2010)** to Section 2.1 (*Stability, Consensus, and Their Limits*).
  - Add **Hartigan & Hartigan (1985)** to Section 2.2 and Section 3.1, providing a brief theoretical justification for using Sarle's moment coefficient ($O(ND)$ time complexity) over the computationally heavier Dip Test ($O(N \log N \cdot D)$ with sorting).
  - Add **Liu et al. (ICML 2010)** as the original inventor of anchor graph spectral clustering in Section 2.3.
  - Cite **SC3 (Kiselev et al., Nature Methods 2017)** as the leading consensus clustering method in computational oncology.
- [ ] **4. Sanitize Repository Documentation:**
  - Update `README.md` and `docs/literature/papers.md` to remove uncalibrated claims of "Rank #1 dominance", "universal superiority", or "conformal guarantees". Ensure the public GitHub landing page exactly matches the restrained, empirical diagnostic framing of `paper/main.tex`.
- [ ] **5. Soften Table 1 Taxonomy:**
  - In Table 1 (`tab:taxonomy_comparison`), change the GAC "High-$D$ Noise" column from *"Gated Subspace"* to *"Conditionally Resilient (Bimodal Signals Only)"*, and change "Core Filtering" to *"Core Anchors (Empirically Equivalent to Random)"*.

---
*Report compiled and audited under strict Springer Nature DMKD peer-review guidelines.*