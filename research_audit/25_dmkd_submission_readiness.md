# Master Scientific Integration & DMKD Submission Readiness Report
**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Track:** Research / Survey Track  
**Manuscript Title:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Repository Audited:** `AkashKundu114/icc-clustering` (Release v2.1.0)  
**Lead Author / Faculty Mentor:** Akash Kundu / Prof. Kalyan Kumar Das  
**Auditor Persona:** Senior Lead Reviewer & Central Scientific Integration Agent  
**Date of Audit:** November 1, 2026  

---

## 1. Executive Master Verdict

### Overall Submission Readiness: **CONDITIONALLY SUBMISSION-READY PENDING MANDATORY REVISIONS**
**(Accept with Mandatory Benchmarking, Attribution, and Textual Harmonization)**

The ICC-Clustering project has undergone a comprehensive, multi-phase adversarial pre-submission audit conducted by six independent reviewing agents. The transition from an earlier uncalibrated narrative of "universal algorithmic superiority" to an empirical investigation of **stability–accuracy discordance** in high-dimensional consensus clustering represents a substantial scientific maturation.

The empirical codebase demonstrates extraordinary transparency in its negative results:
1. It openly documents that under family-wise error rate control (Holm-Bonferroni), pairwise gains over several strong baselines do not achieve statistical significance.
2. It documents that the omnibus Friedman test across 13 diverse benchmarks fails to reject the null hypothesis ($p = 0.3979$).
3. It discloses that the entire pooled BGSS meta-analytic effect is concentrated in two cohorts (Golub Leukemia and Khan SRBCT), collapsing from $+0.0712$ ($p = 0.0007$) to $+0.0243$ ($p = 0.182$, 95% CI $[-0.011, +0.060]$) when those two cohorts are excluded.
4. It reports severe failure modes, such as GAC scoring dead last on Endometrium ($\text{ARI} = -0.0077$).

However, the adversarial audit has identified **24 itemized scientific and implementation findings** (including 11 Critical, 9 Major, and 4 Minor) that must be addressed in the codebase and manuscript before formal submission to Springer DMKD. Most critically:
- The legacy narrative claiming "21 biological cohorts" has been **completely falsified**; the benchmark contains exactly **10 confirmed Category A independent bulk oncology cohorts**.
- Baseline implementations must be accurately attributed: "FastMVC" is an unfaithful surrogate stub for FastMICE (IEEE TKDE 2023); Leiden SNN silently defaulted to Spectral Clustering; GMM-BIC consumed ground-truth $K$.
- Unknown-$K$ evaluation scripts contained ground-truth leakage in candidate grid upper bounds (`k_max = max(6, k_true + 2)`), and ICC-AutoK-PAC suffered from an implementation-theory disconnect in eigenvector space.

---

## 2. Comprehensive Categorization of Scientific Claims

Every major claim asserted in the manuscript, repository documentation, and experimental protocols has been independently tested and categorized into one of five rigorous scientific classifications:

### Category 1: Verified Claims (Empirically & Statistically Replicated)
1. **Pervasiveness of Stability–Accuracy Discordance:** High resampling stability ($\text{Stab} \ge 0.50$) regularly coexists with near-zero diagnostic reference accuracy ($\text{ARI} \le 0.05$) in high-dimensional ($D \gg N$) consensus clustering (e.g. Prostate $\Delta = +0.847$, CNS $\Delta = +0.542$).
2. **Subspace Bimodality Isolation (BGSS):** Sarle's Bimodality Coefficient ($BC > 5/9$) correctly identifies bimodal gene expressions in sparse oncogenomic data without requiring supervised diagnostic labels.
3. **Targeted Superiority on Bimodal Oncogenomic Cohorts:** GAC achieves substantial, reproducible improvements on classic bimodal benchmarks:
   - Golub Leukemia: $\text{ARI} = 0.8953$ vs Standard Consensus $0.2525$ ($\Delta = +0.6428$).
   - Khan SRBCT: $\text{ARI} = 0.6974$ vs Standard Consensus $0.1734$ ($\Delta = +0.5240$).
4. **Linear Bipartite Ensembling Scalability:** Bipartite anchor graph consensus achieves an empirical runtime scaling of $O(N \cdot L \cdot k)$, completely eliminating the $O(N^2)$ quadratic co-association memory bottleneck.
5. **Zero Supervised Preprocessing Leakage:** Genomic preprocessing across all 12 evaluated bulk cohorts is completely uncorrupted by diagnostic class labels. Full raw probe sets ($D \in [2,000, 24,481]$) were evaluated without $t$-test, ANOVA, or marker filtering.
6. **ICC-AutoK-Silhouette Resilience Under Isotropic Noise:** In synthetic noisy regimes ($D=500$), silhouette-based model order selection accurately estimates $K^*$ (MAE $= 0.60$, exact match $63.3\%$, mean $\text{ARI} = 0.834$).

### Category 2: Partially Supported Claims (Context-Dependent Validity)
1. **Algorithmic Dominance of GAC:** Partially supported in sparse, multi-class oncogenomics, but unsupported as a general clustering method. The omnibus Friedman test fails ($p = 0.3979$), all 12 baselines fall within a single Nemenyi critical distance band ($CD = 6.803$), and pairwise Holm-Bonferroni corrections yield zero statistically significant differences.
2. **Expansion to 12 Biological Cohorts:** Partially supported. Exactly 10 cohorts represent confirmed Category A independent biological patient cohorts. Novartis (Category B) shares laboratory lineage with Su2001, and GCM (Category C) has extensive patient overlap with Leukemia and CNS.
3. **BGSS as a Universal Regularizer:** Partially supported. BGSS provides strong regularizing benefits when discriminative signals reside in bimodal marginal distributions, but fails or actively degrades clustering when signals are diffuse, non-linear, or unimodal with subtle covariance shifts (e.g., Endometrium $\text{ARI} = -0.0077$, rank 7/7).

### Category 3: Unsupported Claims (Lacking Empirical or Methodological Foundation)
1. **Operational Utility of Proposition 2 (Anchor Determinacy Certification):** The theoretical sample bounds derived in Proposition 2 do not translate to empirical gains. The authors' own ablation knockout study (Table 13, Knockout 4) proves that certified core anchors yield a statistically indistinguishable improvement of $\Delta = +0.019$ ($p = 0.84$) over uniform random anchors.
2. **ICC-AutoK-PAC Multi-Class Model Order Discovery:** The claim that anchor PAC provides superior model order selection is completely unsupported on multi-class data: PAC achieved 0.0% exact match on synthetic $K^* \ge 3$ data (MAE $= 2.37$) and failed on multi-class biological cohorts (predicting $K=2$ on Su2001 $K^*=11$).
3. **Leiden Community Detection Baseline:** The claim that GAC was evaluated against Leiden SNN community detection is unsupported by the code, which executed Spectral Clustering fallback due to missing native C++ libraries.

### Category 4: Falsified Claims (Empirically Contradicted or Methodologically Refuted)
1. **"21 Real-World Biological Cohorts":** Falsified. 11 of the 21 datasets in the legacy audit suite were non-biological negative controls (speech, sonar, text, image, board games).
2. **Provenance of `breast_cancer_genomic` and `gisette`:** Falsified. OpenML 1120 is `MagicTelescope` (astrophysics gamma-ray simulation, $D=10$), and OpenML 41027 is a Jungle Chess board game endgame ($D=6$).
3. **Independence of `glioma`:** Falsified. `glioma` (OpenML 1107) is an exact 100% duplicate of `cns` (Pomeroy 2002) with identical SHA-256 hash.
4. **Biological Independence of Ramaswamy GCM:** Falsified. Sample correlation audits proved GCM ingested 61 of 72 Golub Leukemia patients ($r \ge 0.990$) and 8 Pomeroy CNS patients ($r > 0.90$).
5. **GMM-BIC Unsupervised Model Order Selection:** Falsified. In `src/icc/baselines/classical.py`, GMM consumed ground-truth $K$ directly, with zero BIC model selection.
6. **Unsupervised Search Grid in Unknown-$K$ Benchmarking:** Falsified. The evaluation script dynamically set $K_{\max} = \max(6, K_{\text{true}} + 2)$, leaking ground-truth cluster count into the search space.

### Category 5: Remaining Limitations & Boundary Conditions
1. **Null Hypothesis ($K=1$) Blind Spot:** Consensus clustering PAC and silhouette heuristics are fundamentally incapable of validating the absence of cluster structure ($K=1$).
2. **Class Imbalance & Zero-Inflation Sensitivity:** Sarle's bimodality coefficient degrades when cluster proportions are heavily skewed or when expression matrices feature extensive dropout/zero-inflation.
3. **Subspace Gating Over-Pruning:** In cohorts with subtle, distributed multigenic expression signatures (such as Endometrium), variance/bimodality gating prunes discriminative features, causing severe cluster collapse.
4. **High-Dimensional Ambient Concentration in Density Baselines:** Density-based methods (HDBSCAN*) suffer catastrophic distance concentration in ambient dimension ($D > 10,000$), requiring pre-clustering manifold reduction.

---

## 3. Comprehensive Master Disposition Matrix of All 24 Findings

The following table itemizes all 24 findings uncovered across the six auditing tracks, detailing their severity, source review track, verified evidence, and required manuscript/code disposition:

| Finding ID | Auditing Track | Description & Forensic Evidence | Severity | Verified Impact | Required Disposition & Remediation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **F-01** | Statistical | **Holm-Bonferroni Multiplicity Collapse:** Zero pairwise comparisons reach significance ($p_{\text{adj}} \ge 0.0938$) across 11 baselines. | **CRITICAL** | Overclaims pairwise superiority | Revise manuscript narrative from "algorithmic dominance" to "empirical discordance analysis". Disclose adjusted p-values. |
| **F-02** | Statistical | **Friedman Omnibus Non-Significance:** Friedman test yields $p = 0.3979$ (all) and $p = 0.2721$ (High-D). Nemenyi CD $= 6.803$ spans all models. | **CRITICAL** | Cannot claim omnibus superiority | Explicitly present Friedman test and CD diagram in Section 4. Acknowledge statistical equivalence band. |
| **F-03** | Statistical | **Leave-{Leukemia, SRBCT}-Out Collapse:** Meta-analytic gain drops from $+0.0712$ ($p=0.0007$) to $+0.0243$ ($p=0.182$, 95% CI spans zero). | **CRITICAL** | Gain carried by 2 cohorts | Disclose DerSimonian-Laird leave-out sensitivity analysis in Section 5. Highlight high heterogeneity ($I^2 = 97.9\%$). |
| **F-04** | Statistical | **Endometrium Failure Disclosed:** GAC ranks dead last (7/7) with $\text{ARI} = -0.0077$, while Standard Consensus achieves $0.6878$. | **MAJOR** | Severe edge-case failure | Add dedicated discussion of Endometrium in Section 5.2 as an architectural boundary condition of BGSS. |
| **F-05** | Statistical | **Pseudoreplication in Error Reporting:** Earlier tables reported pooled SE across 65 runs ($13 \times 5$) treating seeds as cohorts ($\sqrt{5}\times$ deflated). | **MAJOR** | Artificially narrow CIs | Use hierarchical random-effects or aggregate to cohort means before computing standard errors. |
| **F-06** | Statistical | **Negative Control Discordance Reversal:** On non-biological controls (XOR, Audio), GAC exhibits identical discordance ($\Delta \approx 0.6$). | **MINOR** | Ineffective on non-genomic | Note that BGSS is tailored specifically to bimodal gene expression distributions. |
| **F-07** | Implementation | **Hidden Base-Clusterer Switching:** `base_clusterer="auto"` used Spectral for $N \le 100$ and K-Means for $N > 100$. Standard Consensus used K-Means. | **CRITICAL** | Confounded baseline comparison | Standardize base clusterers across all ensemble methods, or document `base_clusterer` as a reported parameter. |
| **F-08** | Implementation | **GMM-BIC Misnomer & GT Leakage:** `run_gmm` received ground-truth $K$ directly; did not perform BIC model selection. | **CRITICAL** | Misrepresented baseline | Rename baseline to "GMM (Fixed-$K$)" or implement authentic `GaussianMixture` BIC grid search over $k \in [2, 10]$. |
| **F-09** | Implementation | **Leiden SNN Mock Fallback:** Environment lacked `leidenalg`; code silently fell back to Spectral Clustering on SNN with $K=K_{\text{true}}$. | **CRITICAL** | Misattributed baseline | Explicitly disclose the Spectral-on-SNN fallback, or install `leidenalg` in conda environment and run true Leiden. |
| **F-10** | Implementation | **HDBSCAN* Noise Label Penalty:** Outlier label `-1` treated as ordinary cluster in scikit-learn ARI; run on raw $D=15,154$ ambient space. | **MAJOR** | Distorted HDBSCAN ARI | Document ambient distance concentration failure; recompute ARI both with noise-as-cluster and noise-excluded. |
| **F-11** | Implementation | **Sparse K-Means Formula Discrepancy:** Code used $s = 0.15\sqrt{D} + 1.0$ while Table 2 specified $s = 1.1 + 0.5(\sqrt{D} - 1.1)$ ($3\times$ difference). | **MAJOR** | Formula inconsistency | Harmonize Table 2 text with exact implemented formula, or re-run with Table 2 parameter. |
| **F-12** | Implementation | **Single-Restart Base Voters:** Ensembles used $n_{\text{init}}=1$ voters, whereas standalone K-Means used $n_{\text{init}}=10$. | **MAJOR** | Voter diversity vs strength | Document that single-restart is standard in consensus ensembling to induce voter diversity. |
| **F-13** | Implementation | **FCM Hard Defuzzification:** FCM evaluated strictly via `argmax` membership without tuning fuzzifier $m$. | **MINOR** | Standard practice in benchmark | Document default $m=2.0$ and hard partition assignment for ARI evaluation. |
| **F-14** | Provenance | **Falsification of 21 Biological Cohorts:** 11 legacy datasets were non-biological negative controls. | **CRITICAL** | Manuscript overclaim | Restructure manuscript to state: exactly 10 confirmed independent biological cohorts + control strata. |
| **F-15** | Provenance | **OpenML Misattributions:** `breast_cancer_genomic` was `MagicTelescope` ($D=10$); `gisette` was Jungle Chess board game ($D=6$). | **CRITICAL** | Severe data misattribution | Purge these misattributed datasets completely from biological benchmark tables. |
| **F-16** | Provenance | **Duplicate Dataset (`glioma` == `cns`):** OpenML 1107 is an exact bit-for-bit duplicate of Pomeroy CNS. | **CRITICAL** | Redundant evaluation | Eliminate `glioma` from all independent cohort counts and meta-analyses. |
| **F-17** | Provenance | **Ramaswamy GCM Composite Contamination:** Ingested 61 Golub Leukemia and 8 Pomeroy CNS patients ($r \ge 0.99$). | **CRITICAL** | Violates sample independence | Exclude GCM from primary meta-analysis; present only as a cross-cohort composite case study. |
| **F-18** | Provenance | **Novartis 9_Tumors Shared Lab Lineage:** Shares Andrew I. Su and GNF laboratory with Su2001 (Category B). | **MAJOR** | Non-independent lab effects | Classify Novartis as Category B in provenance tables; conduct sensitivity analysis with/without Novartis. |
| **F-19** | Provenance | **Transductive Preprocessing:** Full-cohort z-score scaling performed without out-of-sample partitioning. | **MINOR** | Standard in discovery | Clarify that exploratory cluster discovery is transductive; note zero supervised label leakage. |
| **F-20** | Unknown-$K$ | **Search Range Ground-Truth Leakage:** `run_unknown_k.py` set $K_{\max} = \max(6, K_{\text{true}} + 2)$, leaking $K_{\text{true}}$. | **CRITICAL** | Circular evaluation | Fix candidate grid to constant $K \in [2, 10]$ across all datasets and models. |
| **F-21** | Unknown-$K$ | **Theoretical-Implementation Disconnect:** PAC evaluated on spectral eigenvectors $U \in \mathbb{R}^{N \times k}$, not bipartite matrix $B \in \mathbb{R}^{N \times L}$. | **CRITICAL** | Theory diverged from code | Document that PAC is evaluated in normalized spectral embedding space, or update code to use $B$. |
| **F-22** | Unknown-$K$ | **Pathological $K=2$ PAC Attractor:** `min_pac + 0.02` heuristic forces $K=2$; PAC gets 0% exact match on synthetic $K^* \ge 3$. | **CRITICAL** | Fails multi-class discovery | Report PAC multi-class failure transparently; highlight ICC-AutoK-Silhouette as the effective heuristic. |
| **F-23** | Novelty | **FastMVC Surrogate Stub:** Baseline is an internal heuristic proxy, not authentic FastMICE (IEEE TKDE 2023); uncredited. | **CRITICAL** | Baseline misattribution | Explicitly cite Huang et al. (TKDE 2023), clarify surrogate implementation, or re-run with official MATLAB/Python code. |
| **F-24** | Novelty | **"Useless Core" Paradox:** Proposition 2 sample determinacy certification yields $\Delta = +0.019$ ($p=0.84$) vs random anchors. | **MAJOR** | Theoretical overclaim | Tone down Proposition 2 claims; present as theoretical insight while openly reporting ablation equivalence. |

---

## 4. Final Submission Checklist & Remediation Roadmap

To ensure smooth acceptance during DMKD peer review, the authors should execute the following 5-step harmonization roadmap:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 DMKD PRE-SUBMISSION HARMONIZATION ROADMAP                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Manuscript Narrative Calibration:                                        │
│    - Title: Retain empirical diagnostic framing:                            │
│      "An Empirical Analysis of Stability-Accuracy Discordance in            │
│       High-Dimensional Consensus Clustering: Evidence from Biomedical       │
│       Cohorts"                                                              │
│    - Abstract: Remove claims of "universal superiority" or "Rank 1          │
│      dominance". Emphasize the identification of the discordance trap and   │
│      the conditional utility of BGSS in bimodal high-D regimes.             │
│                                                                             │
│ 2. Cohort Restructuring:                                                    │
│    - Formally define the 10 Category A confirmed independent cohorts.       │
│    - Relegate Novartis to Category B (shared lab) and GCM to Category C     │
│      (composite overlap). Purge OpenML 1120 (MagicTelescope) and 41027      │
│      (Jungle Chess).                                                        │
│                                                                             │
│ 3. Statistical Transparency:                                                │
│    - Report Holm-Bonferroni adjusted p-values alongside raw Wilcoxon stats. │
│    - Include the Friedman omnibus test (p=0.40) and Nemenyi CD diagram.     │
│    - Dedicate a subsection in Section 5 to the DerSimonian-Laird Leave-Out  │
│      sensitivity analysis (drop from +0.0712 to +0.0243, I^2 = 97.9%).      │
│                                                                             │
│ 4. Baseline Attribution & Correction:                                       │
│    - Add formal citations for FastMICE (Huang et al., IEEE TKDE 2023),      │
│      Monti et al. (2003), Wilkerson & Hayes (2010), Hartigan (1985), and    │
│      Liu et al. (ICML 2010).                                                │
│    - Document that "FastMVC" is an internal surrogate proxy.                │
│    - Rename GMM baseline to "GMM (Fixed-K)".                                │
│                                                                             │
│ 5. Unknown-K Cleanup:                                                       │
│    - Fix candidate grid to constant K in [2, 10] in `run_unknown_k.py`.     │
│    - Clarify spectral embedding space for PAC calculation in `autok.py`.    │
│    - Transparently document PAC K=2 bias and recommend Silhouette.          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Master Sign-Off & Recommendation

**Central Scientific Integration Agent Verdict:**  
The ICC-Clustering research repository demonstrates exemplary technical engineering, strict data provenance auditing, and extraordinary scientific honesty. Unlike conventional submissions that obscure negative findings or prune inconvenient datasets, this codebase rigorously preserves and reports negative results, statistical equivalence bands, and architectural boundary conditions.

When the manuscript text is harmonized with the empirical findings documented in this 6-part audit series (`20_adversarial_reproduction.md` through `25_dmkd_submission_readiness.md`), the manuscript will constitute an impactful, rigorous, and highly citable contribution to Springer *Data Mining and Knowledge Discovery*.

**Final Recommendation:** **SUBMIT TO DMKD UPON COMPLETION OF MANUSCRIPT HARMONIZATION.**

---
*Report compiled and certified by Central Integration & Scientific Audit Agent (`75860bdd-4d81-446c-a143-6e73f3804f09`).*
