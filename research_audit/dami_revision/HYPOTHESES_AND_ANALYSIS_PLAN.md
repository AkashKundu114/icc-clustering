# Gate G1: Confirmatory Hypotheses and Statistical Analysis Plan (Protocol v2.1-RECONCILED)

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Protocol Version:** `v2.1-RECONCILED` (Post-Independent-Review Reconciled Specification)  
**Base Commit SHA:** `4624b6cf30ec146c44f77353f6ee57d2120eafc2`  
**Branch:** `research/dami-revision`  
**Date:** November 1, 2026  
**Status:** **PROPOSED PROTOCOL CORRECTION — PENDING HUMAN AUTHORIZATION FOR GATE G1 FREEZE**  

---

## 1. Study Overview, Demarcation, and Epistemic Status

This protocol establishes the confirmatory hypothesis testing framework, mathematical estimands, multiplicity control structure, algorithm failure policies, and power/precision assessment for the DMKD revision of `icc-clustering`. 

### 1.1 Transparent Analytical Separation
To prevent scientific leakage, hindsight overfitting, and circular validation, the experimental universe is strictly segregated into three non-overlapping partitions:

1. **Exploratory Cohort Partition (Frozen Baseline, $N_{\text{exp}} = 6$):**
   - The original six biomedical cohorts (`colon`, `leukemia`, `breast`/`ovarian`, `prostate`, `srbct`, `cns`) were utilized during initial model development, diagnostic failure analysis, and post-hoc criterion formulation (e.g., Rule i' non-degeneracy condition).
   - **Epistemic Classification:** Formally and irreversibly designated as **EXPLORATORY**. Inferences derived from these six datasets are descriptive, hypothesis-generating, and exploratory. They shall never be pooled into confirmatory hypothesis testing.
2. **Confirmatory Cohort Partition ($J = 15$ Total, with Strict Stratum Hierarchy):**
   - Curated human clinical bulk transcriptomic cohorts satisfying all eligibility criteria (`research_audit/cohort_discovery/COHORT_DISCOVERY_ELIGIBILITY_SPEC.md`).
   - **Primary Confirmatory Benchmark Suite ($J_{\text{Tier A}} = 10$):** Restricted strictly to Tier A intrinsic tumor subtyping (B1 ground truth): GSE62254 (Gastric), GSE39582 (Colorectal), GSE31210 (Lung), GSE13159 (Leukemia), GSE10846 (Lymphoma), GSE42568 (Breast), GSE19188 (NSCLC), GSE21653 (Breast), GSE32894 (Bladder), GSE49710 (Neuroblastoma).
   - **Secondary / Pan-Stratum Suite ($J_{\text{Total}} = 15$):** Combines the 10 Tier A cohorts with 5 Tier B cohorts: GSE14520 (B2: Liver tumor vs. normal), GSE25066 (B3: Breast ER status), GSE2034 (B3: Breast ER status), GSE72094 (B3: Lung KRAS mutation), GSE14333 (B1: Colorectal Dukes anatomical stage).
   - **Epistemic Classification:** Formally designated as **CONFIRMATORY**. Ground-truth molecular subtype labels are sealed with SHA-256 digests in an air-gapped vault. All model fits, hyperparameter configurations, and cluster outputs must be frozen prior to label unsealing.
3. **Sensitivity & Post-Hoc Partition:**
   - Parameter sweeps ($M, L, \alpha$), threshold variations (Rule i' cutoff grid), preprocessing transformations (raw vs. log vs. normalized), and leave-one-cohort-out (LOCO) perturbations are classified as **SENSITIVITY ANALYSES**.

---

## 2. Clarification and Provenance of Baseline Statistics (0.217 and 0.061)

To eliminate ambiguity between absolute performance metrics and comparative effect sizes:

1. **Cohort-Level Mean Absolute ARI ($0.217$):**
   - **Definition:** The arithmetic mean of the within-cohort median Adjusted Rand Index (ARI) achieved by Full ICC-v2 across the six exploratory cohorts.
   - **Source Trace:** Derived directly from `results/passF/benchmark_matrix_passF.csv`, `results/passF/fair_baselines_30seeds_passF.csv`, and `results/passF/ablation_30seeds_passF.csv`.
   - **Exact Cohort Breakdown:** CNS ($0.0210$), Colon ($0.0721$), Leukemia ($0.5998$), Ovarian ($0.0499$), Prostate ($0.0122$), SRBCT ($0.5456$).
   - **Calculated Mean:** $\frac{1}{6} \sum_{j=1}^6 \text{ARI}_j = 0.2168 \approx \mathbf{0.217}$.
2. **Cohort-Level Median Absolute ARI ($0.061$):**
   - **Definition:** The median of the within-cohort median ARIs achieved by Full ICC-v2 across the six exploratory cohorts.
   - **Source Trace:** Sorted cohort values: $[0.0122, 0.0210, 0.0499, 0.0721, 0.5456, 0.5998]$.
   - **Calculated Median:** $\frac{0.0499 + 0.0721}{2} = 0.0610 \approx \mathbf{0.061}$.
3. **Distinction from Comparative Effect Size ($+0.169$):**
   - Neither $0.217$ nor $0.061$ represents an improvement over random gating.
   - The **mean paired gain over matched budget random feature gating** under bipartite consensus is **$+0.169$** ($95\%$ CI $[+0.036, +0.310]$), driven by Leukemia ($+0.398$) and SRBCT ($+0.447$).
   - The **median paired gain over matched random gating** across the six exploratory cohorts is **$+0.0055$**, highlighting the severe two-cohort concentration of BGSS gains.

All text, tables, and protocol specifications must use these exact labels.

---

## 3. Formal Confirmatory Hypotheses, Estimands, and Decision Rules

### 3.1 Hypothesis 1: Stability–Accuracy Decoupling and Discordance in High Dimensions

#### Hypothesis 1a (H1a: Stability–Accuracy Correlation Decoupling)
- **Scientific Premise:** In ultra-high-dimensional biological regimes ($D/N > 20$), distance concentration flattens pairwise metric space, causing subsample stability to decouple from external ground truth recovery across candidate clustering algorithms.
- **Null Hypothesis ($H_{0,1\text{a}}$):** Algorithmic subsample stability correlates strongly and positively with empirical clustering accuracy (ARI) across candidate algorithms within high-dimensional cohorts:
  $$\rho_{\text{pooled}}(\text{Stability}, \text{ARI}) \ge 0.50$$
- **Alternative Hypothesis ($H_{1,1\text{a}}$):** Subsample stability is decoupled from ground-truth clustering accuracy:
  $$\rho_{\text{pooled}}(\text{Stability}, \text{ARI}) < 0.30$$
- **Primary Estimand:** Cohort-averaged Fisher $z$-transformed Spearman rank correlation across candidate algorithms:
  $$\bar{z}_\rho = \frac{1}{J} \sum_{j=1}^J z(\hat{\rho}_j), \quad z(\hat{\rho}_j) = \frac{1}{2} \ln\left(\frac{1 + \hat{\rho}_j}{1 - \hat{\rho}_j}\right) = \text{arctanh}(\hat{\rho}_j)$$
  where $\hat{\rho}_j = \text{Spearman}\left(\{\text{Stab}_{m,j}, \text{ARI}_{m,j}\}_{m \in \mathcal{M}}\right)$ is computed across the candidate algorithms on cohort $j$.
- **Accounting for Repeated Method Observations within Cohorts:**  
  1. Primary inference aggregates within-cohort correlations first, yielding one correlation $\hat{\rho}_j$ per independent biological cohort ($J = 15$).
  2. If an algorithm encounters `FAILURE_ABORT`, pairwise deletion is applied within cohort $j$, requiring a minimum of $|\mathcal{M}_j| \ge 6$ executed algorithms.
  3. A secondary confirmatory repeated-measures correlation ($\rho_{\text{rm}}$) and linear mixed-effects model with cohort random intercepts are estimated:
     $$\text{ARI}_{m,j} = \beta_0 + \beta_1 \text{Stability}_{m,j} + u_j + \epsilon_{m,j}, \quad u_j \sim \mathcal{N}(0, \sigma_u^2)$$
     testing $H_{0}: \beta_1 \ge \beta_{\text{target}}$ using cluster-robust standard errors.
- **Statistical Test:** One-sided one-sample Wilcoxon signed-rank test on $\{z(\hat{\rho}_j)\}_{j=1}^J$ against the transformed null value $z(0.50) \approx 0.5493$.
- **Decision Rule:** Reject $H_{0,1\text{a}}$ if $p_{\text{adj}} < 0.05$ (one-sided) and the $95\%$ bootstrap confidence interval for the back-transformed mean correlation $\rho_{\text{back}} = \tanh(\bar{z}_\rho)$ satisfies $\rho_{\text{upper}} < 0.30$.

#### Hypothesis 1b (H1b: Stability-Minus-Accuracy Discordance Gap)
- **Scientific Premise:** Subsample stability creates an illusion of cluster validity on arbitrary noise partitions, exhibiting a large positive discordance gap ($\text{Stab} - \text{ARI} \gg 0$) even when partitions fail trivial degeneracy checks.
- **Null Hypothesis ($H_{0,1\text{b}}$):** Across non-degenerate partitions in high-dimensional cohorts, subsample stability does not systematically exceed empirical accuracy beyond a minimal tolerance margin:
  $$\Delta_{\text{gap}} = \mathbb{E}[\text{Stability} - \text{ARI}] \le 0.05$$
- **Alternative Hypothesis ($H_{1,1\text{b}}$):** Subsample stability substantially and systematically exceeds empirical accuracy across non-degenerate partitions:
  $$\Delta_{\text{gap}} = \mathbb{E}[\text{Stability} - \text{ARI}] > 0.20$$
- **Primary Estimand:** Cohort-level mean discordance gap across non-degenerate candidate methods:
  $$\bar{\Delta}_j = \frac{1}{|\mathcal{M}_{\text{valid}, j}|} \sum_{m \in \mathcal{M}_{\text{valid}, j}} (\text{Stab}_{m,j} - \text{ARI}_{m,j})$$
  where $\mathcal{M}_{\text{valid}, j}$ denotes the subset of algorithms satisfying Decision Rule~(i') non-degeneracy (smallest cluster $\ge 5\%$ of samples in $\ge 90\%$ of subsamples). If all candidate methods violate Rule i' for cohort $j$ ($|\mathcal{M}_{\text{valid}, j}| = 0$), the cohort is logged as a degeneracy attrition event.
- **Statistical Test:** One-sided one-sample Wilcoxon signed-rank test on $\{\bar{\Delta}_j\}_{j=1}^J$ against $\Delta_0 = 0.05$.
- **Decision Rule:** Reject $H_{0,1\text{b}}$ if $p_{\text{adj}} < 0.05$ and the lower bound of the $95\%$ bootstrap confidence interval for the median cross-cohort gap satisfies $\text{CI}_{\text{lower}} > 0.15$.

---

### 3.2 Hypothesis 2: Conditional Utility of Bimodality Gating (BGSS)

#### Hypothesis 2a (H2a: Primary Gating Advantage under Bipartite Consensus)
- **Scientific Premise:** BGSS filters unimodal distractor coordinates prior to base clustering. Under bipartite consensus, BGSS confers an accuracy advantage over budget-matched random feature gating.
- **Null Hypothesis ($H_{0,2\text{a}}$):** In high-dimensional cohorts, BGSS under bipartite consensus confers no accuracy advantage over budget-matched random feature gating:
  $$\Delta_{\text{BGSS, Bip}} = \mathbb{E}\left[\text{ARI}_{\text{BGSS, Bip}} - \text{ARI}_{\text{Random, Bip}}\right] \le 0$$
- **Alternative Hypothesis ($H_{1,2\text{a}}$):** BGSS significantly improves clustering accuracy over budget-matched random gating under bipartite consensus ($\Delta_{\text{BGSS, Bip}} > 0$).
- **Primary Estimand:** Paired cohort difference in median ARI across 30 seeds between Full ICC-v2 (BGSS + Bipartite) and budget-matched Random Gating (Random Subspaces + Bipartite):
  $$D_{2\text{a}, j} = \text{Median}_{s}\left(\text{ARI}_{\text{BGSS}, j, s}\right) - \text{Median}_{s}\left(\text{ARI}_{\text{Random}, j, s}\right)$$
- **Primary vs. Secondary Evaluation:** Primary confirmatory test executed on the **Tier A Stratum ($J_{\text{Tier A}} = 10$)**; secondary test executed on the pooled suite ($J=15$).
- **Statistical Test:** One-sided paired Wilcoxon signed-rank test.
- **Decision Rule:** Reject $H_{0,2\text{a}}$ if $p_{\text{adj}} < 0.05$ under Family 2 Holm-Bonferroni correction AND $\text{Median}(D_{2\text{a}}) > 0$.

#### Hypothesis 2b (H2b: Dense-Consensus Attenuation Interaction)
- **Scientific Premise:** Dense co-occurrence averaging ($O(N^2)$) creates spurious dense edges under extreme noise, attenuating the signal recovered by BGSS compared to bipartite anchor distillation ($O(NL)$).
- **Null Hypothesis ($H_{0,2\text{b}}$):** The marginal accuracy gain of BGSS over matched random gating is not attenuated under dense consensus compared to bipartite consensus:
  $$\Delta_{\text{attenuation}} = \mathbb{E}\left[\Delta_{\text{BGSS, Bip}} - \Delta_{\text{BGSS, Dense}}\right] \le 0$$
- **Alternative Hypothesis ($H_{1,2\text{b}}$):** The accuracy benefit of BGSS is significantly attenuated under dense consensus:
  $$\Delta_{\text{attenuation}} = \mathbb{E}\left[\Delta_{\text{BGSS, Bip}} - \Delta_{\text{BGSS, Dense}}\right] > 0$$
- **Primary Estimand:** Paired interaction contrast across cohorts:
  $$D_{2\text{b}, j} = \left(\text{ARI}_{\text{BGSS, Bip}, j} - \text{ARI}_{\text{Random, Bip}, j}\right) - \left(\text{ARI}_{\text{BGSS, Dense}, j} - \text{ARI}_{\text{Random, Dense}, j}\right)$$
- **Statistical Test:** One-sided paired Wilcoxon signed-rank test across cohorts.
- **Decision Rule:** Reject $H_{0,2\text{b}}$ if $p_{\text{adj}} < 0.05$ under Family 2 correction AND $\text{Median}(D_{2\text{b}}) > 0$. Note: Given power limitations ($<35\%$), failure to reject is treated as inconclusive rather than disproof.

---

### 3.3 Hypothesis 3: Core Determinacy Anchor Certification (Formal Equivalence Testing via TOST)

#### Formal Equivalence Hypothesis (Two One-Sided Tests — TOST)
- **Equivalence Bounds:** $[-\delta, +\delta] = [-0.02, +0.02]$ in paired ARI difference.
  - *Justification:* On human clinical datasets ($N \in [40, 500]$), $|\Delta| < 0.02$ represents reassignment of 1 to 2 individual patient samples, falling within the stochastic noise floor of random centroid initializations ($\sigma_{\text{ARI}} \in [0.015, 0.045]$).
- **Composite Null Hypotheses:**
  $$H_{0,3\text{a}}: \Delta_{\text{core - random}} \le -0.02 \quad (\text{Core Anchors Inferior})$$
  $$H_{0,3\text{b}}: \Delta_{\text{core - random}} \ge +0.02 \quad (\text{Core Anchors Superior})$$
- **Equivalence Alternative Hypothesis ($H_{1,3}$):**
  $$H_{1,3}: -0.02 < \Delta_{\text{core - random}} < +0.02 \quad (\text{Practical Equivalence})$$
- **Primary Estimand:** Paired cohort difference in median ARI between Full ICC-v2 (Certified Core Anchors) and Knockout 4 (Uniform Random Landmark Anchors):
  $$D_{3, j} = \text{Median}_{s}\left(\text{ARI}_{\text{Core}, j, s}\right) - \text{Median}_{s}\left(\text{ARI}_{\text{RandomLandmarks}, j, s}\right)$$
- **Testing Procedure & Duality Standards:**
  1. The primary binding decision standard for establishing operational equivalence at margin $\pm 0.02$ is the **$90\%$ non-parametric bootstrap confidence interval** (dual to two one-sided tests at $\alpha = 0.05$).
  2. If evaluated under Holm-adjusted family threshold $\alpha_{(k)}$, the formal dual confidence interval is $100(1 - 2\alpha_{(k)})\%$.
- **Explicit Three-Way Decision Rule:**
  1. **Equivalent (Empirical Null Certified):** Both $H_{0,3\text{a}}$ and $H_{0,3\text{b}}$ rejected at $\alpha = 0.05$ (the $90\%$ CI lies strictly within $[-0.02, +0.02]$). Conclusion: Proposition 2 core anchor certification provides no meaningful empirical benefit over uniform random landmark sampling.
  2. **Non-Equivalent (Difference Established):** The $90\%$ CI lies strictly outside $[-0.02, +0.02]$ (or excludes zero). Conclusion: Certified core anchors confer a non-trivial accuracy difference.
  3. **Inconclusive / Underpowered (Explicitly Mandated Outcome):** If the $90\%$ CI overlaps either boundary $-0.02$ or $+0.02$ (e.g., CI spans $[-0.019, +0.057]$). Conclusion: The empirical sample size provides insufficient precision to establish equivalence at $\pm 0.02$. **The authors are strictly prohibited from declaring an empirical null if the outcome is inconclusive.**

---

## 4. Multiplicity Control Architecture and Inferential Families

```
+---------------------------------------------------------------------------------------+
| INFERENTIAL MULTIPLICITY ARCHITECTURE                                                 |
+---------------------------------------------------------------------------------------+
|  Family 1: Primary Confirmatory Baseline Benchmarks (8 Comparisons, FWER alpha=0.05)   |
|  - Full ICC-v2 vs. StdCons_All         - Full ICC-v2 vs. K-Means_LapScore             |
|  - Full ICC-v2 vs. K-Means_All         - Full ICC-v2 vs. SparseKMeans                 |
|  - Full ICC-v2 vs. K-Means_VarFilt     - Full ICC-v2 vs. FCAG                         |
|  - Full ICC-v2 vs. K-Means_PCA         - Full ICC-v2 vs. FastMVC-Surrogate            |
|  Primary stratum: Tier A (J=10). Secondary stratum: Pooled (J=15).                    |
|  Procedure: Holm-Bonferroni step-down; Decision Rule: p_adj < 0.05 AND Median(D) > 0. |
+---------------------------------------------------------------------------------------+
|  Family 2: Architectural Component Attribution (3 Comparisons, FWER alpha=0.05)       |
|  - H2a: BGSS vs. Matched Random Gating under Bipartite Consensus                      |
|  - H2b: BGSS Dense-Consensus Attenuation Interaction                                  |
|  - H3: Core Determinacy TOST Equivalence (+/- 0.02 Margin)                            |
|  Procedure: Holm-Bonferroni step-down across 3 planned tests.                         |
+---------------------------------------------------------------------------------------+
|  Family 3: Foundational Methodological Claims (2 Tests, Sequentially Gated)           |
|  - H1a: Stability-Accuracy Decoupling (Spearman rho < 0.30 vs. rho >= 0.50)           |
|  - H1b: Discordance Gap (Delta_gap > 0.20 across non-degenerate partitions)           |
|  Procedure: Fixed-sequence hierarchical testing (test H1b iff H1a rejects).           |
+---------------------------------------------------------------------------------------+
|  Family 4: Sensitivity, Robustness, & Diagnostic Ablations (Descriptive Only)         |
|  - Rule (i') cutoff grid scans, Preprocessing variations (E3), LOCO leave-out checks. |
|  Status: Exploratory / Sensitivity; no multiplicity adjustments; labeled descriptive. |
+---------------------------------------------------------------------------------------+
```

### 4.1 Family 1: Comparative Baselines and Hyperparameter Contracts ($M=8$)

To eliminate "straw-man baseline" vulnerabilities, all comparative baselines are governed by locked operational parameter contracts:
1. `BM-01: StdCons_All`: Ambient features, $M = 25$ base partitions, dense $N \times N$ co-association, average-linkage hierarchical consensus.
2. `BM-02: K-Means_All`: Ambient features, $n_{\text{init}} = 5$, Lloyd's iterations, $k$-means++ seeding.
3. `BM-03: K-Means_VarFilt`: Features ranked by sample variance; top $d = \min(2000, D)$ features retained; $n_{\text{init}} = 5$.
4. `BM-04: K-Means_PCA`: Features projected onto top $p = 50$ principal components (or top $p$ explaining $\ge 80\%$ variance, whichever is smaller, with $p \ge K$); $n_{\text{init}} = 5$.
5. `BM-05: K-Means_LapScore`: 5-nearest-neighbor cosine affinity graph; top $d = \min(2000, D)$ features retained; $n_{\text{init}} = 5$.
6. `BM-06: SparseKMeans`: Convex $\ell_1$-penalized feature-weighted clustering; $w_{\text{bound}}$ tuned over 10-point grid in $[1.1, \sqrt{D}/2]$ via 5 permutation iterations.
7. `BM-07: FCAG`: Fast Consensus with Anchor Graph; landmark count $L = 40$, nearest anchors $s = 5$.
8. `BM-08: FastMVC-Surrogate`: Multi-View Bipartite Consensus Proxy; $L = 40, s = 5$.

**Holm-Bonferroni Step-Down Procedure:**
- Sort raw $p$-values: $p_{(1)} \le p_{(2)} \le \dots \le p_{(8)}$.
- Step-down alpha: $\alpha_{(k)} = \frac{0.05}{8 - k + 1}$.
- **Binding Superiority Decision Rule:** Full ICC-v2 is confirmed superior to Baseline $m$ if and only if:
  $$p_{\text{adj}, (m)} < 0.05 \quad \text{AND} \quad \text{Median}(D_{\text{BM}-m}) > 0$$

---

## 5. Technical Specifications & Reproducibility Standards

### 5.1 Model Order Contract ($K$-Contract)
In confirmatory benchmarking against external ground-truth partitions, candidate algorithms and baselines are parameterized with:
$$K = |\mathcal{Y}_{\text{target}}|$$
where $|\mathcal{Y}_{\text{target}}|$ is the documented number of biological classes in the cohort metadata. This isolates partition accuracy from the orthogonal problem of model order determination ($K$-estimation).

### 5.2 Seed Schedules and Randomization
- **Replicate Budget:** Exactly $S = 30$ independent pseudo-random seeds per algorithm-cohort combination.
- **Canonical Seed Schedule:** Locked sequence:
  $$\mathcal{S} = \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29\}$$
- **RNG Implementation:** `numpy.random.default_rng(seed)` initialized once per seed.

### 5.3 Preprocessing and Missing-Data Protocol
All preprocessing is strictly unsupervised, label-free, and self-contained within each cohort:
1. **Missing Feature Rule:** Any gene/probe feature with $> 20\%$ missing values across samples is discarded (reconciling all protocol records).
2. **Missing Sample Rule:** Any sample with $> 20\%$ missing features across the active transcriptome is discarded and logged.
3. **Imputation:** Remaining missing entries are imputed using the cohort feature-level median. No multivariate or label-informed imputation is permitted.
4. **Transformations:** Microarray: RMA or normalized probe log2 intensity. Bulk RNA-seq: $\log_2(\text{TPM} + 1)$ or VST.
5. **Feature Standardization:** Features standardized to $\mu=0, \sigma=1$ across samples prior to distance computations.
6. **Zero External Label Leakage:** Preprocessing operates strictly on expression matrices $\mathbf{X}$; labels $\mathbf{y}$ remain sealed in the SHA-256 encrypted vault.

### 5.4 Cohort Annotations and Ground Truth Standards
- `GSE10846` (DLBCL): Excludes 67 biologically unclassifiable samples; evaluates pure GCB vs. ABC ($K=2, N=347$).
- `GSE13159` (MILE Leukemia): Retains 74 normal bone marrow samples as an established diagnostic cytogenetic control in leukemia profiling ($K=6$).
- `GSE14333` (Jorissen CRC): Classified as Tier B anatomical progression contrast (Dukes A–D).

### 5.5 Algorithm Failure and Numerical Instability Handling
1. **Spectral Graph Regularization:** $\mathbf{L}_{\text{reg}} = \mathbf{L} + 10^{-6} \mathbf{I}$ applied for ill-conditioned Laplacians.
2. **Disconnected Bipartite Components:** Eigensolver performs block-diagonal decomposition or projects onto the top $K$ generalized eigenvectors of the largest connected components.
3. **Empty Cluster Reseeding:** Base K-Means instances dynamically reseed empty centroids from the sample exhibiting the maximum residual squared error.
4. **Fatal Solver Abort Policy:** Baselines crashing or exceeding 3,600 s are designated `FAILURE_ABORT`, recorded with $\text{ARI} = 0.0$, and logged in an attrition registry.

### 5.6 Cohort-Level Aggregation & Confidence Intervals
1. Within-cohort performance across 30 seeds is collapsed to the **median ARI scalar** first.
2. Non-parametric bootstrap confidence intervals resample the $J$ independent cohort summary values with replacement ($B = 10{,}000$).

### 5.7 Treatment of Overlapping and Derivative Cohorts
Enforced via `overlap_graph.graphml` and `overlap_pairs.csv`. Candidate datasets sharing $> 5\%$ patient donors or representing derivative compendia (e.g., E-MTAB-6698) are quarantined; exactly one primary representative is admitted.

---

## 6. Stop Conditions for Confirmatory Execution

Confirmatory execution of E1–E8 and creation of git tag `prereg-dami-v1` shall remain **STRICTLY BLOCKED** until:
1. The human investigator reviews and explicitly approves this reconciled protocol.
2. The independent reviewer audit reports (`G1_INDEPENDENT_REVIEW.md`, `G1_DECISION_REPORT.md`) are verified.
3. All baseline result stores (`results/passF/`, `results/passE/`, `results/results.json`) remain untouched.