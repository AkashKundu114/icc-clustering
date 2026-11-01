# Pre-Registration Record: DAMI Scientific Revision Protocol (v2.1-RECONCILED)

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Working Branch:** `research/dami-revision`  
**Base Commit SHA:** `4624b6cf30ec146c44f77353f6ee57d2120eafc2`  
**Date of Record:** November 1, 2026  
**Proposed Git Tag:** `prereg-dami-v1` (**PENDING EXPLICIT HUMAN INVESTIGATOR AUTHORIZATION — GATE G1**)  

---

## 1. Administrative Information & Investigator Affiliations

- **Study Title:** Empirical Analysis of Stability-Accuracy Discordance and Bimodality-Gated Consensus Clustering in High-Dimensional Biomedical Cohorts
- **Lead Investigator:** Akash Kundu  
  *Affiliation:* Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India  
  *Email:* `akashkundu1152@gmail.com`  
  *ORCID:* `0009-0003-8246-7316`
- **Collaborating Investigators:**
  - Kalyan Kumar Das  
    *Affiliation:* Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India  
    *Email:* `kalyan.biltu@gmail.com`  
    *ORCID:* `0009-0004-8333-8900`
  - Anirban Mukhopadhyay  
    *Affiliation:* Department of Computer Science and Engineering, University of Kalyani, Kalyani, West Bengal, India  
    *Email:* `anirban@klyuniv.ac.in`  
    *ORCID:* `0000-0001-8128-3521`
- **Integrity Attestation:** No invented institutional affiliations, unauthorized institutional endorsements, or unverified affiliations are represented.
- **Pre-Registration Status:** **FORMALLY RECONCILED SPECIFICATION — PENDING EXPLICIT HUMAN AUTHORIZATION BEFORE FREEZE AND TAG**

---

## 2. Analytical Demarcation and Epistemic Status

1. **Exploratory Cohort Partition ($N_{\text{exp}} = 6$):**
   - The six historical cohorts (`cns`, `colon`, `leukemia`, `ovarian`, `prostate`, `srbct`) are irreversibly classified as **EXPLORATORY**.
   - These cohorts generated initial hypotheses and diagnostic post-hoc rules (e.g., Rule i' non-degeneracy condition).
   - Descriptive results from these cohorts (Full ICC-v2 cohort mean absolute ARI $= 0.217$, cohort median absolute ARI $= 0.061$, and mean paired gain over matched random gating $= +0.169$) are quarantined and shall not be pooled into confirmatory hypothesis testing.
2. **Confirmatory Cohort Partition ($J = 15$ Total, with Strict Stratum Hierarchy):**
   - Fifteen independent human clinical cancer bulk transcriptomic cohorts satisfying all Tier A/B eligibility criteria (`research_audit/cohort_discovery/COHORT_DISCOVERY_ELIGIBILITY_SPEC.md`).
   - **Primary Confirmatory Benchmark Suite ($J_{\text{Tier A}} = 10$):** Restricted strictly to Tier A intrinsic tumor subtyping (B1 ground truth): GSE62254 (Gastric), GSE39582 (Colorectal), GSE31210 (Lung), GSE13159 (Leukemia), GSE10846 (Lymphoma), GSE42568 (Breast), GSE19188 (NSCLC), GSE21653 (Breast), GSE32894 (Bladder), GSE49710 (Neuroblastoma).
   - **Secondary / Pan-Stratum Suite ($J_{\text{Total}} = 15$):** Combines the 10 Tier A cohorts with 5 Tier B cohorts: GSE14520 (B2: Liver tumor vs. normal), GSE25066 (B3: Breast ER status), GSE2034 (B3: Breast ER status), GSE72094 (B3: Lung KRAS mutation), GSE14333 (B1: Colorectal Dukes anatomical stage).
   - Labels are fingerprinted with SHA-256 digests and sealed in an encrypted vault. Models execute with zero access to external labels.
3. **Sensitivity Partition:**
   - Preprocessing ablations, threshold sensitivity grids, and leave-one-cohort-out analyses are classified as **SENSITIVITY ANALYSES**.

---

## 3. Pre-Specified Confirmatory Hypotheses and Estimands

### 3.1 Hypothesis 1: Stability–Accuracy Decoupling and False Confidence Gap

#### H1a: Stability–Accuracy Correlation Decoupling
- **Null Hypothesis ($H_{0,1\text{a}}$):** In high-dimensional cohorts ($D/N > 20$), subsample stability strongly predicts ground truth clustering accuracy across candidate algorithms:
  $$\rho_{\text{pooled}}(\text{Stability}, \text{ARI}) \ge 0.50$$
- **Alternative Hypothesis ($H_{1,1\text{a}}$):** Subsample stability is decoupled from ground truth clustering accuracy:
  $$\rho_{\text{pooled}}(\text{Stability}, \text{ARI}) < 0.30$$
- **Primary Estimand:** Cohort-averaged Fisher $z$-transformed Spearman rank correlation across candidate algorithms $\bar{z}_\rho = \frac{1}{J} \sum_{j=1}^J z(\hat{\rho}_j)$, where $\hat{\rho}_j = \text{Spearman}\left(\{\text{Stab}_{m,j}, \text{ARI}_{m,j}\}_{m \in \mathcal{M}}\right)$. Repeated-measures correlation $\rho_{\text{rm}}$ and a linear mixed-effects model ($\text{ARI}_{m,j} = \beta_0 + \beta_1 \text{Stability}_{m,j} + u_j + \epsilon_{m,j}$) serve as secondary confirmations to account for repeated method observations within cohorts. Pairwise deletion applied for aborted runs (minimum $|\mathcal{M}_j| \ge 6$).
- **Statistical Test:** One-sided one-sample Wilcoxon signed-rank test on $\{z(\hat{\rho}_j)\}_{j=1}^J$ against $z(0.50) \approx 0.5493$.
- **Decision Threshold:** Reject $H_{0,1\text{a}}$ if $p_{\text{adj}} < 0.05$ and back-transformed correlation upper $95\%$ CI bound satisfies $\rho_{\text{upper}} < 0.30$.

#### H1b: Stability-Minus-Accuracy Discordance Gap
- **Null Hypothesis ($H_{0,1\text{b}}$):** Across non-degenerate partitions in high-dimensional cohorts, subsample stability does not systematically exceed empirical accuracy beyond a minimal tolerance:
  $$\Delta_{\text{gap}} = \mathbb{E}[\text{Stability} - \text{ARI}] \le 0.05$$
- **Alternative Hypothesis ($H_{1,1\text{b}}$):** Subsample stability systematically and substantially exceeds empirical accuracy across non-degenerate partitions:
  $$\Delta_{\text{gap}} = \mathbb{E}[\text{Stability} - \text{ARI}] > 0.20$$
- **Primary Estimand:** Cohort-level mean gap across non-degenerate methods:
  $$\bar{\Delta}_j = \frac{1}{|\mathcal{M}_{\text{valid}, j}|} \sum_{m \in \mathcal{M}_{\text{valid}, j}} (\text{Stab}_{m,j} - \text{ARI}_{m,j})$$
  (evaluating partitions passing Rule i' non-degeneracy: smallest cluster holds $\ge 5\%$ of samples in $\ge 90\%$ of subsamples).
- **Statistical Test:** One-sided one-sample Wilcoxon signed-rank test on $\{\bar{\Delta}_j\}_{j=1}^J$ against $\Delta_0 = 0.05$.
- **Decision Threshold:** Reject $H_{0,1\text{b}}$ if $p_{\text{adj}} < 0.05$ and lower bound of $95\%$ bootstrap CI for median cross-cohort gap satisfies $\text{CI}_{\text{lower}} > 0.15$.

---

### 3.2 Hypothesis 2: Conditional Utility of Bimodality Gating (BGSS)

#### H2a: Primary Gating Advantage under Bipartite Consensus
- **Null Hypothesis ($H_{0,2\text{a}}$):** In high-dimensional cohorts, BGSS under bipartite consensus confers no accuracy advantage over budget-matched random feature gating:
  $$\Delta_{\text{BGSS, Bip}} = \mathbb{E}\left[\text{ARI}_{\text{BGSS, Bip}} - \text{ARI}_{\text{Random, Bip}}\right] \le 0$$
- **Alternative Hypothesis ($H_{1,2\text{a}}$):** BGSS significantly improves clustering accuracy over budget-matched random gating under bipartite consensus ($\Delta_{\text{BGSS, Bip}} > 0$).
- **Primary Estimand:** Paired difference in within-cohort median ARI across 30 seeds between Full ICC-v2 and budget-matched Random Gating:
  $$D_{2\text{a}, j} = \text{Median}_{s}\left(\text{ARI}_{\text{BGSS}, j, s}\right) - \text{Median}_{s}\left(\text{ARI}_{\text{Random}, j, s}\right)$$
- **Primary vs. Secondary Evaluation:** Primary confirmatory test executed on the **Tier A Stratum ($J_{\text{Tier A}} = 10$)**; secondary test on the pooled suite ($J=15$).
- **Statistical Test:** One-sided paired Wilcoxon signed-rank test.
- **Decision Threshold:** Reject $H_{0,2\text{a}}$ if $p_{\text{adj}} < 0.05$ under Family 2 Holm-Bonferroni control AND $\text{Median}(D_{2\text{a}}) > 0$.

#### H2b: Dense-Consensus Attenuation Interaction
- **Null Hypothesis ($H_{0,2\text{b}}$):** The marginal accuracy gain of BGSS over matched random gating is not attenuated under dense consensus compared to bipartite consensus:
  $$\Delta_{\text{attenuation}} = \mathbb{E}\left[\Delta_{\text{BGSS, Bip}} - \Delta_{\text{BGSS, Dense}}\right] \le 0$$
- **Alternative Hypothesis ($H_{1,2\text{b}}$):** The accuracy benefit of BGSS is significantly attenuated under dense consensus ($\Delta_{\text{attenuation}} > 0$).
- **Primary Estimand:** Paired interaction contrast across cohorts:
  $$D_{2\text{b}, j} = \left(\text{ARI}_{\text{BGSS, Bip}, j} - \text{ARI}_{\text{Random, Bip}, j}\right) - \left(\text{ARI}_{\text{BGSS, Dense}, j} - \text{ARI}_{\text{Random, Dense}, j}\right)$$
- **Statistical Test:** One-sided paired Wilcoxon signed-rank test across cohorts.
- **Decision Threshold:** Reject $H_{0,2\text{b}}$ if $p_{\text{adj}} < 0.05$ under Family 2 Holm-Bonferroni control AND $\text{Median}(D_{2\text{b}}) > 0$. Power limitation ($<35\%$) explicitly noted; failure to reject treated as inconclusive.

---

### 3.3 Hypothesis 3: Core Determinacy Anchor Certification (Formal Equivalence via TOST)

- **Equivalence Bounds:** $[-\delta, +\delta] = [-0.02, +0.02]$ in paired ARI difference.
  - *Justification:* On human clinical datasets ($N \in [40, 500]$), $|\Delta| < 0.02$ corresponds to reassigning 1–2 patient samples (within stochastic solver noise $\sigma \in [0.015, 0.045]$ across random initializations).
- **Composite Null Hypotheses (Two One-Sided Tests — TOST):**
  $$H_{0,3\text{a}}: \Delta_{\text{core - random}} \le -0.02 \quad (\text{Core Anchors Inferior})$$
  $$H_{0,3\text{b}}: \Delta_{\text{core - random}} \ge +0.02 \quad (\text{Core Anchors Superior})$$
- **Equivalence Alternative Hypothesis ($H_{1,3}$):**
  $$H_{1,3}: -0.02 < \Delta_{\text{core - random}} < +0.02 \quad (\text{Operational Equivalence})$$
- **Primary Estimand:** Paired cohort difference in median ARI between Full ICC-v2 (Certified Core Anchors) and Knockout 4 (Uniform Random Landmarks):
  $$D_{3, j} = \text{Median}_{s}\left(\text{ARI}_{\text{Core}, j, s}\right) - \text{Median}_{s}\left(\text{ARI}_{\text{RandomLandmarks}, j, s}\right)$$
- **Testing Procedure & Duality Standards:** The **$90\%$ bootstrap CI** is the primary binding decision standard for operational equivalence at nominal $\alpha = 0.05$. Under Holm-adjusted $\alpha_{(k)}$, the dual CI is $100(1 - 2\alpha_{(k)})\%$.
- **Three-Way Decision Outcomes:**
  1. **Equivalent (Empirical Null Certified):** Both $H_{0,3\text{a}}$ and $H_{0,3\text{b}}$ rejected; $90\%$ CI lies entirely within $[-0.02, +0.02]$.
  2. **Non-Equivalent (Difference Established):** $90\%$ CI falls outside $[-0.02, +0.02]$.
  3. **Inconclusive / Underpowered (Explicitly Mandated Outcome):** $90\%$ CI crosses either $-0.02$ or $+0.02$ bound. **The study shall NOT claim an empirical null if the outcome is inconclusive.**

---

## 4. Multiplicity Control Families and Correction Procedures

1. **Family 1: Primary Baseline Comparisons ($M=8$, FWER $\alpha = 0.05$):**
   - Full ICC-v2 evaluated against 8 comparative baselines (`StdCons_All`, `K-Means_All`, `K-Means_VarFilt`, `K-Means_PCA`, `K-Means_LapScore`, `SparseKMeans`, `FCAG`, `FastMVC-Surrogate`).
   - Primary test on Tier A ($J_{\text{Tier A}} = 10$); secondary test on pooled suite ($J=15$).
   - Correction: Holm-Bonferroni step-down.
   - **Decision Rule:** Reject $H_0$ and confirm superiority if and only if:
     $$p_{\text{adj}} < 0.05 \quad \text{AND} \quad \text{Median}(D_{\text{BM}-m}) > 0$$
2. **Family 2: Architectural Component Attribution ($M=3$, FWER $\alpha = 0.05$):**
   - H2a (BGSS vs. Random Bipartite), H2b (Dense Attenuation), H3 (TOST Equivalence).
   - Correction: Holm-Bonferroni step-down across 3 tests.
3. **Family 3: Methodological Claims ($M=2$, FWER $\alpha = 0.05$):**
   - H1a (Correlation Decoupling), H1b (Discordance Gap).
   - Correction: Fixed-sequence hierarchical testing (test H1b iff H1a rejects).
4. **Family 4: Sensitivity & Diagnostic Ablations:**
   - Preprocessing ablations (E3), cutoff scans, and LOCO checks are reported as descriptive sensitivity analyses.

---

## 5. Technical Specifications & Execution Standards

1. **$K$-Contract:** In confirmatory benchmarking, $K = |\mathcal{Y}_{\text{target}}|$, isolating partition accuracy from model order determination.
2. **Baseline Hyperparameters:**
   - `K-Means_VarFilt`: top $d = \min(2000, D)$ by variance.
   - `K-Means_PCA`: top $p = 50$ PCs (or $\ge 80\%$ variance).
   - `K-Means_LapScore`: 5-NN cosine graph, top $d = \min(2000, D)$.
   - `SparseKMeans`: $w_{\text{bound}}$ tuned over 10-point grid via 5 permutation iterations.
   - `FCAG` / `FastMVC-Surrogate`: $L = 40, s = 5$.
3. **Seed Schedule:** Exactly 30 canonical pseudo-random seeds: $\{0, 1, 2, \dots, 29\}$. Fixed RNG: `numpy.random.default_rng(seed)`.
4. **Preprocessing:** Unsupervised and label-free. Features with $>20\%$ missing values dropped (reconciled across all documents); remaining median-imputed; standardization to zero mean and unit variance; $\log_2(\text{TPM}+1)$ or RMA intensity. Zero label access.
5. **Cohort Annotations:**
   - `GSE10846` (DLBCL): Excludes 67 unclassified samples; evaluates GCB vs. ABC ($K=2, N=347$).
   - `GSE13159` (MILE Leukemia): Retains 74 normal bone marrow controls ($K=6$).
   - `GSE14333` (Jorissen CRC): Classified as Tier B Dukes anatomical stage.
6. **Algorithm Failure Policy:** Matrix regularization ($\mathbf{L} + 10^{-6}\mathbf{I}$) for singular graphs; block-diagonal eigensolving for disconnected components; dynamic reseeding for empty k-means clusters; fatal solver timeouts ($>3,600$ s) recorded as `FAILURE_ABORT` with $\text{ARI}=0$ and logged in attrition registry.
7. **Cohort Aggregation:** Within-cohort summary is median ARI across 30 seeds; bootstrap confidence intervals resample the $J$ independent cohort summary values with replacement ($B = 10{,}000$).
8. **Overlapping Cohort Adjudication:** Enforced via `overlap_graph.graphml` and `overlap_pairs.csv`. Datasets sharing $>5\%$ donors or derivative accessions are quarantined; exactly one primary representative is analyzed.

---

## 6. Pre-Registration Freeze Protocol & Stop Condition

- This document represents the reconciled, audit-verified protocol.
- **Strict Stop Condition:** Neither git tag `prereg-dami-v1` nor confirmatory experiments E1–E8 shall be launched without subsequent, explicit approval from the human investigator.
- Exploratory classification of the original six cohorts remains locked and approved.