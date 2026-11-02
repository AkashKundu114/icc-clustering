# Loop 4: Peer Review Panel Simulation Reports

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DMKD)  
**Manuscript Title:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Authors:** Kalyan Kumar Das, Akash Kundu, Anirban Mukhopadhyay  
**Evaluated Commit:** `7ddbe830`  
**Date of Review:** November 2, 2026  

---

## Editorial Overview

The manuscript has been evaluated by five independent peer reviewers representing distinct sub-disciplines:
1. **Reviewer 1:** Clustering and Consensus-Clustering Specialist
2. **Reviewer 2:** Statistical Learning Theory and Conformal Prediction Specialist
3. **Reviewer 3:** High-Dimensional Biomedical Data and Cancer Genomics Specialist
4. **Reviewer 4:** Computational Complexity and Spectral Graph Methods Specialist
5. **Reviewer 5:** Reproducibility, Open Science, and Experimental Methodology Specialist

Below are the unabridged, independent review reports.

---

# Reviewer 1: Report

**Expertise:** Clustering algorithms, ensemble learning, consensus clustering, stability selection  
**Recommendation:** Major Revision  

### 1. Summary of the Manuscript
The manuscript investigates a fundamental dilemma in unsupervised learning: the relationship between subsample stability and partition accuracy in the high-dimensional, small-sample regime ($D \gg N$). While consensus clustering is widely deployed in bioinformatics under the assumption that stability implies biological validity, the authors demonstrate that multiple established consensus and multi-view clustering pipelines (FCAG, FCM, FastMVC) frequently converge to highly reproducible, stable partitions that exhibit zero or near-zero agreement with diagnostic reference classes ($\text{ARI} \le 0.05$). Through controlled isotropic simulations and six high-dimensional biomedical microarray cohorts ($D/N > 20$), the authors characterize this "stability-accuracy discordance." To dissect what algorithmic mechanisms help recover signal, they study Gated Anchor Consensus (GAC) as an experimental vehicle combining marginal bimodality screening (BGSS), random-subspace base clusterers, and bipartite anchor-graph compression.

### 2. Primary Strengths
1. **Important and Timely Empirical Falsification:** For over two decades (since Monti et al., 2003), consensus clustering has been the dominant unsupervised methodology in cancer subtype discovery. Demonstrating that high subsample stability ($\text{Stab} \approx 0.684$) can co-occur with zero diagnostic accuracy ($\text{Acc} = -0.003$) on real biomedical cohorts under non-degeneracy audits is an essential service to the data mining and bioinformatics communities.
2. **Exemplary Candor Regarding Negative and Omnibus Results:** The authors do not attempt to sell GAC as a universally superior algorithm. They transparently report that omnibus differences across 13 diverse benchmarks are not statistically significant (Friedman $p = 0.40$), and that determinacy-based anchor selection yields no measurable benefit ($\Delta = +0.019$, $p = 0.84$). This intellectual honesty is refreshing.
3. **Controlled Factorial Decomposition:** The $2 \times 2$ factorial ablation crossing feature gating (none, random, BGSS) with consensus architecture (dense, bipartite) effectively isolates the source of performance gains on Leukemia and SRBCT.

### 3. Major Weaknesses
1. **Confounding in the Dense Consensus Baseline on Leukemia:** In Section 7.3 (Table 12), the authors report that BGSS + Dense Consensus ($V_2$) attains an ARI of only $0.077$, which is substantially worse than BGSS + Bipartite Consensus ($V_5$, $0.217$). The authors explain that this is caused by a degenerate collapse in Leukemia, where 23 of 30 seeds latch onto a small cluster ($N = 9\text{--}16$). However, why does standard dense consensus fail so catastrophically on the exact same feature pool where bipartite consensus succeeds? Does the bipartite anchor graph act as an implicit low-rank regularizer, or is this an artifact of K-Means initialization on the bipartite embedding matrix $U$? Without isolating this mechanism, the claim that bipartite consensus "rescues" the gating remains incompletely explained.
2. **Absence of Monti's Empirical Consensus CDF Diagnostics:** The consensus clustering literature relies heavily on Monti's consensus CDF curve and the proportion of ambiguous clustering (PAC) to assess stability and determine $K$. The manuscript relies entirely on pairwise Adjusted Rand Index across subsamples. While pairwise ARI is a valid metric, the paper should explicitly discuss how subsample ARI relates to Monti's CDF area and PAC metrics.
3. **Boundary Conditions of BGSS Feature Selection:** GAC's positive gains are almost entirely concentrated in two datasets: Leukemia ($+0.398$) and SRBCT ($+0.447$). On Prostate, CNS, Colon, and Ovarian, GAC shows negligible improvement or severe discordance. The manuscript attributes this to the absence of marginal multimodality, but needs to provide a clearer diagnostic criteria: when should a practitioner apply BGSS versus standard variance filtering?

### 4. Minor Weaknesses
- Table 1 refers to "Core-Halo Consensus," but the algorithmic description of Core-Halo is only briefly mentioned in the text. A formal mathematical definition should be provided in the Supplementary Material.
- In Figure 1(b), the distance concentration formula is written as $(d_{\max}-d_{\min})/d_{\min} \to 0$. It would be helpful to cite Beyer et al. (1999) directly in the figure caption.
- In Section 4.2, the anchor budget is set to $L = 40$. While the ablation shows flat performance for $L \in [20, 80]$, what happens when $K$ is large (e.g., $K=26$ on Isolet)? The rule $\max(40, 10K)$ should be benchmarked explicitly.

### 5. Technical Questions for the Authors
1. *Bipartite Regularization:* In Section 7.3, you observe that bipartite consensus with random subspaces prevents the $N=9\text{--}16$ local mode collapse seen in dense consensus on Leukemia. Can you prove or empirically demonstrate whether this regularization is driven by the random subspace draws or by the low-rank rank-$L$ projection of the anchor graph?
2. *Ambiguous Subsamples:* In your 30 subsample draws, how sensitive is the stability estimate to the subsample ratio ($80\%$ vs. $50\%$ or $90\%$)?
3. *Comparison with Monti CDF:* How does the stability-accuracy gap correlate with Monti's Delta Area metric on these six cohorts?

---

# Reviewer 2: Report

**Expertise:** Statistical learning theory, non-parametric inference, spectral graph theory, conformal prediction  
**Recommendation:** Major Revision  

### 1. Summary of the Manuscript
The authors evaluate stability-accuracy discordance in high-dimensional consensus clustering. The paper presents three theoretical results: Proposition 1 (a conditional multimodality separation bound using Sarle's Bimodality Coefficient), Proposition 2 (an exact determinacy identity computing sample determinacy in $O(M^2 N + M^2 K^2)$ without materializing the co-association matrix), and Theorem 1 (time and auxiliary memory complexity bounds for the GAC pipeline). The empirical study evaluates 12 algorithms across 13 datasets.

### 2. Primary Strengths
1. **Proposition 2 is an Elegant, Exact Algorithmic Identity:** The algebraic transformation in Equation (4), exchanging the double summation over ensemble partitions into contingency matrix lookups, is mathematically exact, computationally elegant, and eliminates the $O(N^2)$ memory bottleneck for determinacy estimation.
2. **Sound Application of Clustered Bootstrap:** The use of a dataset-clustered bootstrap ($B = 10{,}000$) to estimate the stability-accuracy gap interval ($[+0.379, +0.662]$) correctly treats the cohort (rather than the resampled seed) as the independent unit of variation.
3. **Prudent Omission of Unverified Conformal Claims:** The authors have wisely avoided claiming finite-sample conformal clustering guarantees in the main text, noting split-conformal inference only as a future research direction.

### 3. Major Weaknesses
1. **Over-Generalized Formulation in Proposition 1:** 
   - Proposition 1 states that continuous uniform noise yields $b_d = 5/9 \approx 0.556$, and that a balanced Gaussian mixture exceeds $5/9$ iff component separation $\Delta / \sigma_0 > 1.854$.
   - The text implies that $b_d \le 5/9$ serves as an upper bound separating unimodal from multimodal distributions. **This is mathematically false for asymmetric unimodal distributions.**
   - While Sarle's $BC \le 5/9$ holds for symmetric unimodal distributions, skewed unimodal densities (e.g., Log-normal, Chi-squared, or Gamma distributions) can easily attain $BC > 5/9$ due to extreme skewness ($\gamma^2$).
   - Proposition 1 and the accompanying text MUST be explicitly restricted: the $5/9$ bound applies *strictly to symmetric unimodal distributions*. Without this qualification, the proposition is theoretically invalid.
2. **Geometric Failure of Centroid Induction on Manifolds:**
   - In Section 4.3 (Equations 9--10), inductive inference for query instances is performed via Euclidean nearest-neighbor assignment against determinacy-weighted centroids $\boldsymbol{\mu}_k$ in $\mathbb{R}^{|\mathcal{F}_{\text{active}}|}$.
   - While spectral bipartite clustering is theoretically capable of learning non-convex manifold clusters (e.g., concentric rings, interlocking spirals), Euclidean centroid projection inherently assumes convex, hyper-spherical clusters.
   - For non-convex manifolds, the centroid $\boldsymbol{\mu}_k$ can lie completely outside the support of the cluster (e.g., in the empty central void of a circle).
   - The authors must explicitly state this geometric limitation in Section 4.3 and Section 8.3, clarifying that this closed-form operator is valid only under convex cluster geometry.
3. **Absence of Uniform Convergence Guarantees:**
   - While the paper frames GAC as an experimental vehicle, Section 4.1 introduces BGSS as filtering "continuous unimodal noise coordinates." The authors should state what sample size $N$ is required for the sample moments $\hat{\gamma}_d$ and $\hat{\kappa}_d$ to converge uniformly to their population counterparts across $D$ dimensions. With $D = 15{,}154$ and $N = 253$, sample kurtosis has high variance.

### 4. Minor Weaknesses
- In Equation (1), the finite-sample correction term for excess kurtosis uses $3 \cdot \frac{(N-1)^2}{(N-2)(N-3)}$. The exact reference to Sarle (1983) or SAS/STAT should be verified and cited precisely.
- Theorem 1 lists the time complexity as linear in $N$ ($O(N)$), but note that this holds strictly under the assumption that $L = O(1)$ and $M = O(1)$. If $L$ scales with $N$ (e.g., $L = \sqrt{N}$), the eigensolver would scale as $O(N^{1.5})$.

### 5. Technical Questions for the Authors
1. *Proposition 1 Counterexamples:* Have you evaluated the false positive rate of BGSS on unimodal distributions with high skewness (e.g., log-normal gene expression)? How does log-transformation of microarray data mitigate this?
2. *Manifold Extension:* Why did you choose Euclidean centroid projection over an out-of-sample Nyström or Transfer-Cut spectral projection for query instances?
3. *Kurtosis Estimator Bias:* Given that sample kurtosis $\hat{\kappa}_d$ has severe finite-sample negative bias for small $N$ ($N \le 60$ in CNS and Colon), how does this bias affect the empirical bimodality coefficient $\hat{b}_d$?

---

# Reviewer 3: Report

**Expertise:** High-dimensional biomedical data, cancer transcriptomics, clinical genomics, bioinformatics  
**Recommendation:** Major Revision  

### 1. Summary of the Manuscript
The paper evaluates consensus clustering and stability on six high-dimensional biomedical microarray cohorts (CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT) where $D/N$ ranges from $27.8$ to $123.5$. The authors observe that several consensus and multi-view clustering pipelines reproduce stable partitions that have zero correlation with clinical reference labels, and test whether marginal bimodality gating (BGSS) in a bipartite consensus framework can recover true diagnostic classes.

### 2. Primary Strengths
1. **Critical Clinical Reality Check:** In medical informatics, computational biologists frequently run consensus clustering on tumor samples, observe high cophenetic correlation or subsampling stability, and claim the discovery of novel tumor subtypes without external or functional validation. This paper provides clear empirical proof that this practice is vulnerable to spurious stability.
2. **Deep Diagnostic Forensic of the Prostate Cohort:** The geometric analysis in Section 3.2—revealing that Ward and K-Means isolate PCA-space outliers, whereas spectral and anchor consensus methods align with PC1 and total library depth ($r = -0.52$ to $-0.59$)—is outstanding forensic data science. It explains *why* these partitions are stable: they are tracking dominant technical or biological batch effects rather than diagnostic labels.
3. **Biological Validation of BGSS on Leukemia:** The unsupervised feature saliency audit in Section 7.5 (Figure 10) demonstrates that the top features selected by BGSS on Leukemia correspond to canonical hematopoietic lineage markers (CD19, CD33, myeloperoxidase), providing biological credibility to the gating mechanism where it works.

### 3. Major Weaknesses
1. **Microarray Vintage and Batch Annotations:**
   - The six high-dimensional datasets used in the study are legacy microarray datasets from the late 1990s and early 2000s (e.g., Golub et al. 1999 for Leukemia; Singh et al. 2002 for Prostate; Alon et al. 1999 for Colon).
   - In modern cancer genomics, bulk RNA-seq and single-cell RNA-seq have replaced microarrays. The authors should discuss whether stability-accuracy discordance persists in modern count-based transcriptomic data (e.g., with zero-inflation and overdispersion).
   - Furthermore, the authors note that the Prostate archive lacks batch annotations. In public repositories, batch effects in these legacy cohorts are well-documented. If the "discordant" clusters correspond to true experimental batches, the clustering is not technically "wrong"—it is simply discovering batch rather than disease status. The authors must discuss this distinction more deeply.
2. **Sample Size Limitations ($N < 100$):**
   - Four of the six cohorts have very small sample sizes: CNS ($N=60$), Colon ($N=62$), Leukemia ($N=72$), and SRBCT ($N=83$).
   - Can one reliably make claims about high-dimensional asymptotic geometry when sample sizes are this small? The authors should temper their broader claims about "high-dimensional consensus clustering" to specifically reflect "small-sample biomedical cohorts."
3. **Nature of the Biological Signal in Leukemia and SRBCT:**
   - GAC succeeds primarily on Leukemia ($\text{ARI} = 0.600$) and SRBCT ($\text{ARI} = 0.546$).
   - Biologically, Leukemia represents a dramatic lineage dichotomy (Acute Lymphoblastic Leukemia vs. Acute Myeloid Leukemia), and SRBCT represents four histologically distinct pediatric cancers (neuroblastoma, rhabdomyosarcoma, non-Hodgkin lymphoma, Ewing sarcoma). These are massive expression differences that manifest as strong bimodal marginals.
   - In contrast, Prostate (tumor vs. normal) and CNS (medulloblastoma treatment response) involve subtle regulatory shifts without bimodal gene expression. The authors should explicitly highlight that BGSS is effective for distinct lineage dichotomies, but unsuitable for graded or polygenic transcriptional shifts.

### 4. Minor Weaknesses
- The dataset naming should be consistent: the paper interchangeably refers to "SRBCT" and "Small Round Blue Cell Tumors."
- In Table 2, please clarify whether the reported ARI is computed against the primary disease label or sub-phenotypes.
- For PBMC68k, please specify whether data were normalized via log1p-CPM or raw UMI counts.

### 5. Technical Questions for the Authors
1. *Batch vs. Biology:* If an algorithm reliably clusters samples by collection date or plate batch with $\text{Stab} = 0.85$, is that "stability-accuracy discordance" or simply confounding between technical stability and clinical diagnostic accuracy?
2. *Single-Cell Applicability:* On PBMC68k-red ($N=700, D=765$), GAC achieves an ARI of only $0.218$, ranking behind K-Means ($0.231$) and Spectral ($0.222$). Why does BGSS fail to provide an advantage in sparse single-cell data?
3. *Non-Microarray Validation:* Would the authors expect the same discordance on high-dimensional clinical tabular data (e.g., EHR cohorts or metabolomics)?

---

# Reviewer 4: Report

**Expertise:** Computational complexity, spectral graph theory, randomized linear algebra, numerical algorithms  
**Recommendation:** Minor Revision  

### 1. Summary of the Manuscript
The manuscript analyzes the computational and mathematical properties of Gated Anchor Consensus (GAC), a bipartite graph ensemble pipeline. The paper formulates an exact identity for quadratic sample determinacy (Proposition 2) and establishes time and memory bounds (Theorem 1), accompanied by empirical scaling benchmarks up to $N = 1{,}000{,}000$ instances.

### 2. Primary Strengths
1. **Rigorous Elimination of Quadratic Memory Bottleneck:** Standard consensus clustering requires materializing an $N \times N$ dense matrix ($762.9\text{ MB}$ at $N=10^4$; $\approx 8\text{ TB}$ at $N=10^6$). GAC's bipartite formulation replaces this with an $N \times L$ matrix, requiring only $160\text{ MB}$ at $N=10^6$. The $99.6\%$ memory reduction at $N=10^4$ is mathematically sound and empirically verified.
2. **Computational Verification of Proposition 2:** The authors demonstrate that sample determinacy $\sigma_i = \frac{1}{N-1}(\sum_j S_{ij}^2 - 1)$ can be computed directly from base partition contingency matrices in $O(M^2 N + M^2 K^2)$ time. This is a genuinely useful linear-time identity.
3. **Execution Scaling up to 1 Million Samples:** Demonstrating full pipeline execution on $N=10^6$ instances in under three minutes ($182.64\text{ s}$) on a standard laptop workstation confirms the scalability claims.

### 3. Major Weaknesses
1. **Interpretation of the Empirical Power-Law Exponent:**
   - In Section 6.1 (Fig. 5a), the authors report a fitted empirical power-law exponent of $\beta = 0.548 \pm 0.013$ for $N \in [500, 10{,}000]$, and $\beta = 0.755 \pm 0.074$ for $N \in [10^4, 10^6]$.
   - Theoretically, any algorithm that processes $N$ samples must have time complexity at least $\Omega(N)$ (i.e., $\beta \ge 1.0$).
   - A sub-linear exponent ($\beta < 1.0$) in empirical benchmarking is an artifact of fixed constant overheads (Python interpreter initialization, library loading, small-array allocation) dominating at smaller $N$, combined with multi-threaded BLAS parallelism.
   - The authors must clarify in the text that $\beta < 1.0$ is an effective scaling parameter in the pre-asymptotic regime, and cannot represent true asymptotic sub-linear complexity.
2. **Anchor Laplacian Condition Number:**
   - The anchor affinity kernel $W_{\text{anchor}} = B_{\text{norm}}^T B_{\text{norm}} \in \mathbb{R}^{L \times L}$ requires computing the degree matrix $D_A = \operatorname{diag}(W_{\text{anchor}} \mathbf{1}_L)$ and inverting $D_A^{1/2}$.
   - If an anchor $a$ is isolated (i.e., rarely co-assigned with any other points), the corresponding diagonal entry of $D_A$ approaches zero, causing numerical instability in $L_{\text{anchor}}$.
   - The authors should specify whether regularized degree clamping ($\max(D_A, \epsilon)$) is implemented, and discuss the numerical stability of the eigensolver.

### 4. Minor Weaknesses
- In Equation (6), the Transfer-Cut embedding formula includes a clamp $\max(1 - \boldsymbol{\lambda}, 10^{-4})^{-1/2}$. Please briefly explain why eigenvalues close to 1 are regularized.
- In Theorem 1, the term $M I_{\text{km}} N |\mathcal{F}_{\text{sub}}| K$ should clearly define $I_{\text{km}}$ as the maximum number of K-Means iterations.

### 5. Technical Questions for the Authors
1. *Memory Bandwidth Bottleneck:* In Table 5, as $N$ increases from $10^5$ to $10^6$, the local growth exponent jumps to $\beta = 1.085$. Does this reflect cache misses during the bipartite matrix multiplication $B_{\text{norm}}^T B_{\text{norm}}$?
2. *Anchor Scaling with $K$:* If $K$ is large ($K=50$ or $100$), does the anchor budget $L = 40$ lead to rank deficiency in $W_{\text{anchor}}$? What is the condition on $L$ relative to $K$?

---

# Reviewer 5: Report

**Expertise:** Experimental methodology, benchmarking standards, reproducibility, open science  
**Recommendation:** Minor Revision  

### 1. Summary of the Manuscript
The authors present a large-scale empirical audit of consensus clustering across 13 datasets, 12 algorithms, and 3,000 model fits. The study introduces rigorous controls, including column-permuted nulls, non-degeneracy audits, pre-specified seed sequences, and clustered bootstrap confidence intervals. The codebase and all raw data are made publicly available.

### 2. Primary Strengths
1. **Exceptional Transparency and Scientific Integrity:**
   - The authors openly report that an earlier version of their experimental script had a bug (cascading BGSS filtering inside the random gating control arm), explain how they caught it, and report the corrected baseline ($0.047$ vs. $0.155$).
   - They report the exact commit hashes for when hypotheses, protocols, and post-hoc criteria were added (`commit 3307380`, `commit 49f3882`, `commit 548d68d`).
   - They report non-significant omnibus test results ($p = 0.40$) without p-hacking or selective reporting.
2. **Complete Public Artifact Availability:** All 13 datasets are accessible via standard OpenML or Scanpy identifiers, download scripts are provided, and random seeds are fully synchronized across Python, NumPy, Scikit-learn, and PyTorch.
3. **Thorough Degradation and Degeneracy Audit:** Table 16 documents the exact subsample degeneracy frequencies across all models, revealing critical failure modes in published algorithms (e.g., CoHiRF collapsing in $56\%\text{--}100\%$ of subsamples).

### 3. Major Weaknesses
1. **Post-Hoc Status of Rule (i'):**
   - The non-degeneracy rule (Rule i': smallest cluster $\ge 5\%$ in $\ge 90\%$ of subsamples) was added *after* observing Core-Halo's collapse on Prostate.
   - While the authors honestly disclose this post-hoc addition, the manuscript must be careful not to present Rule (i') as a pre-planned hypothesis test. The paper should clearly demarcate between the pre-registered confirmatory findings (Rule i) and the exploratory post-hoc refinements (Rule i').
2. **Standardized vs. Tuned Baseline Hyperparameters:**
   - In Section 5.2, the authors state that all algorithms were run with fixed default hyperparameters (e.g., default kernel bandwidths for Spectral Clustering, standard scikit-learn defaults for K-Means, heuristic sparsity for Sparse K-Means).
   - While this prevents label-leakage and optimistic tuning bias, it may place certain complex baselines at a disadvantage. For instance, DEC (Deep Embedding Clustering) is known to be highly sensitive to autoencoder pretraining learning rates and latent dimension sizes. The authors should explicitly discuss whether baseline tuning could have mitigated the observed discordance in baselines like FCAG or FastMVC.

### 4. Minor Weaknesses
- Table 6 presents the omnibus ARI results. It would be helpful to include average rank columns alongside the mean ARI values.
- Please verify that the Zenodo DOI in Declarations is active and properly indexed.

### 5. Technical Questions for the Authors
1. *Sensitivity to Rule (i') Threshold:* How sensitive are the discordance counts if the non-degeneracy threshold is changed from $5\%$ to $2\%$ or $10\%$?
2. *Software Environment Consistency:* Given that Python 3.14.6 and NumPy 2.4.6 were used, did you observe any numerical differences when running on earlier LTS versions (e.g., Python 3.10 / NumPy 1.26)?

---

## Editor's Synthesis and Recommendation

**Overall Assessment:**  
All five reviewers recognize the manuscript as an exceptionally candid, rigorous, and valuable empirical study that addresses a critical flaw in high-dimensional consensus clustering. The transparency in reporting negative results, omnibus null findings, and corrected control arms is exemplary.

However, the panel converges on two critical issues that require mandatory revision before the manuscript can be published in *Data Mining and Knowledge Discovery*:
1. **Mathematical Qualification of Proposition 1:** Proposition 1 must be amended to explicitly state that the $BC \le 5/9$ bound holds strictly for *symmetric* unimodal distributions, and acknowledge that asymmetric unimodal distributions can exceed $5/9$.
2. **Explicit Boundary Disclosure for Inductive Centroid Projection:** The authors must explicitly disclose that the Euclidean active subspace centroid projection fails on non-convex manifolds (citing the Concentric Circles counterexample), and clarify that it is valid only for convex cluster geometries.

**Editorial Decision:** **Major Revision**  
The authors are invited to submit a revised manuscript and an itemized response to the review panel addressing all points above.
