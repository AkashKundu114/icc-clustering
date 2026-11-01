# Adversarial Red-Team Audit Report: Experimental Pipeline, Baselines, and Cohort Integrity

**Target Publication:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Auditor:** Dr. Evelyn Reed, Adversarial Red-Team Reviewer & Senior Editorial Board Member  
**Repository Audited:** `AkashKundu114/icc-clustering`  
**Dedicated Revision Branch:** `research/dami-revision`  
**Date of Record:** November 1, 2026  
**Review Verdict:** **MAJOR REVISION / RE-BENCHMARK MANDATE** (Conditional on Strict Remediation of All Critical Baseline and Methodological Defects)

---

## 1. Executive Summary

An adversarial peer-review and forensic code audit of the `AkashKundu114/icc-clustering` repository was conducted to assess compliance with Springer Nature DMKD submission standards. While the underlying algorithm (Bimodality-Gated Subspace Selection with Bipartite Consensus) demonstrates legitimate mathematical formulation, the experimental pipeline contains multiple critical vulnerabilities:

1. **Supervised Information Leakage:** Explicit class-label stratified subsampling in synthetic benchmark construction (`src/icc/datasets/genomics.py:154-165`) and evaluation on non-separable clinical survival/metastasis endpoints directly contradicting repository exclusion specifications.
2. **Unfair Baseline Comparisons & Surrogate Stubs:** Deployment of an unvalidated random-subspace surrogate proxy branded as "FastMVC" (with citations to Huang et al., IEEE TKDE 2023), a $3\times$ discrepancy between the reported and executed $L_1$ penalty in Sparse K-Means, silent substitution of Spectral Clustering for missing Leiden community detection, and asymmetric base-clusterer switching favoring the proposed method on small cohorts ($N \le 100$).
3. **Statistical Fragility & Pseudoreplication:** Performance advantages are almost exclusively concentrated in two cohorts (Golub Leukemia and Khan SRBCT); leaving both out reduces the pooled effect size to zero ($\Delta\text{ARI} = +0.0243, p = 0.182$). The core anchor determinacy certification derived in Proposition 2 is an empirical null ($\Delta\text{ARI} = +0.0188, p = 0.8438$).
4. **Cohort Contamination & Duplicate Re-use:** Inclusion of bit-for-bit duplicate cohorts (OpenML 1107), secondary meta-compendia violating cohort isolation (E-MTAB-6698), composite patient overlap (Ramaswamy GCM ingesting 61/72 Golub patients), and catastrophic misattributions of non-biological files in legacy benchmark scripts.

The itemized evidence, exact line references, quantitative impact assessments, and required remediations are detailed below.

---

## 2. Itemized Red-Team Findings

### 2.1 Supervised Stratified Subsampling on Madelon
- **Location:** `src/icc/datasets/genomics.py:154-165`
- **Code Mechanism:**
  ```python
  if "subsample_n" in cfg and cfg["subsample_n"] < raw_X.shape[0]:
      rng = np.random.default_rng(42)
      indices = []
      unique_classes = np.unique(raw_y)
      per_class = cfg["subsample_n"] // len(unique_classes)
      for c in unique_classes:
          c_idx = np.where(raw_y == c)[0]
          sampled = rng.choice(c_idx, size=min(per_class, len(c_idx)), replace=False)
          indices.extend(sampled)
      sub_indices = np.array(indices)
      raw_X = raw_X[sub_indices]
      raw_y = raw_y[sub_indices]
  ```
- **Critical Critique:** In unsupervised clustering evaluation, subsampling benchmark data using the ground-truth targets `raw_y` (`per_class = cfg["subsample_n"] // len(unique_classes)`) enforces artificial class-prior balance ($250/250$ in Madelon). An unsupervised clustering method cannot condition sample selection on external class labels. This introduces supervised label information into the evaluation set prior to clustering.
- **Remediation:** Replace class-stratified subsampling with purely uniform random subsampling (`rng.choice(raw_X.shape[0], size=cfg["subsample_n"], replace=False)`).

### 2.2 Clinical Outcomes Used as Ground Truth vs. Internal Exclusion Log Contradiction
- **Location:**
  - Runner: `experiments/exp6_cohort_expansion/src/run_exp6.py:6` and `line 52`
  - Results: `experiments/exp6_cohort_expansion/data/expanded_cohort_benchmark.csv:37-54`
  - Exclusion Log: `research_audit/dami_revision/COHORT_EXCLUSION_LOG.csv:10`
  - Audit Spec: `tests/test_g1_protocol_remediation.py:161-163`
- **Empirical Reality:**
  - `run_exp6.py` includes van 't Veer et al. (Nature 2002) as a primary biological cohort (`Breast`, $N=97, D=24,481, K=2$) with the target variable defined as *5-year distant metastasis prognosis*.
  - In `COHORT_EXCLUSION_LOG.csv` line 10, the repository's own governance protocol states:
    > `OPENML_45085_VAN_T_VEER_PROGNOSIS, OpenML 45085, REJECT, B4, Failed Label Eligibility (Section 4.2): Target variable is a B4 clinical outcome endpoint (distant metastasis <= 5 years). The spec explicitly mandates that clinical outcomes must never be used as biological cluster ground truth.`
  - Clinical survival and recurrence are multigenic, non-deterministic physiological outcomes governed by treatment modality, surgical margins, and host microenvironment. They do not form compact cluster manifolds in baseline transcriptome space.
  - In `expanded_cohort_benchmark.csv`, all algorithms collapse to near-zero ARI on this dataset (GAC: $-0.0001$ to $0.0046$; K-Means: $0.0022$ to $0.0391$). Presenting clinical endpoints as clustering ground truth in EXP6 while simultaneously citing their exclusion in protocol remediation creates an irreconcilable self-contradiction.
- **Remediation:** Remove van 't Veer metastasis prognosis from all biological clustering benchmark tables. If breast carcinoma transcriptomics is evaluated, replace the endpoint with intrinsic molecular subtypes (e.g. PAM50: Luminal A, Luminal B, HER2-enriched, Basal-like) or hormone receptor status ($ER^+ / ER^-$).

### 2.3 "FastMVC-Surrogate" Represented as Published Baseline
- **Location:**
  - Code Warning: `src/icc/baselines/anchor.py:6` and `lines 241-247`
  - Config: `configs/baselines.yaml:218-233`
  - Manuscript Text: `springer_manuscript/main.tex:751`, Table 3, and `submission/COVER_LETTER.md:23`
- **Mechanism:**
  - In `src/icc/baselines/anchor.py`, the module docstring confesses:
    > `FastMVC: [STUB] random-subspace anchor-graph SURROGATE. It is NOT a faithful implementation of FastMICE (Huang, Wang, Lai; IEEE TKDE 2023, doi:10.1109/TKDE.2023.3236698), the closest published method. Do not report it as that method.`
  - In `configs/baselines.yaml`, line 221 designates `stub: true # surrogate, NOT a faithful FastMICE implementation; exclude from headline comparisons`, yet formally lists the academic citation as *Huang et al., IEEE TKDE 2023*.
  - In `springer_manuscript/main.tex` and the DMKD submission cover letter, this method is stripped of its "Surrogate" designation, branded as "FastMVC", and used to claim empirical findings: *"Three of twelve methods (FCAG, FCM, FastMVC) meet our non-degenerate discordance criterion on at least three cohorts."*
- **Scientific Verdict:** Constructing an internal ad-hoc heuristic stub, testing it, and publishing comparative deficiencies attributed to a major IEEE TKDE paper constitutes scientific misattribution and unfair baseline benchmarking.
- **Remediation:** Either execute the official published open-source codebase of FastMICE / FastMVC with authors' original optimization routines, or remove FastMVC entirely from baseline rankings and claims.

### 2.4 Sparse K-Means $s$-Rule Discrepancy ($3\times$ Divergence)
- **Location:**
  - Default Code: `src/icc/baselines/sparse_kmeans.py:100` and `lines 142-145`
  - Docstring confession: `src/icc/baselines/sparse_kmeans.py:117-120`
  - Manuscript Description: `paper/main.tex:405` (Table 2 description)
- **Discrepancy:**
  - The executed default in code is `s_rule = "witten_scaled"`:
    $$s_{\text{code}} = \max\left(1.1, 0.15\sqrt{D} + 1.0\right)$$
  - The manuscript explicitly asserts that Sparse K-Means was run using:
    $$s_{\text{table2}} = \max\left(1.1, 1.1 + 0.5(\sqrt{D} - 1.1)\right)$$
  - On Colon ($D=2000$), the code evaluates $s = 0.15\sqrt{2000} + 1.0 = 7.71$, whereas the manuscript claims $s = 1.1 + 0.5(\sqrt{2000} - 1.1) = 22.91$.
  - This is a **$3\times$ divergence in $L_1$ lasso constraint strength**. Furthermore, Sparse K-Means was never tuned using the permutation gap statistic search prescribed by Witten & Tibshirani (JASA 2010), freezing it at a handicapped heuristic.
- **Remediation:** Re-run Sparse K-Means across benchmark cohorts with permutation-tuned gap selection or harmonize code with the exact formula reported in Table 2.

### 2.5 Leiden SNN Silent Fallback to Spectral Clustering
- **Location:**
  - Implementation: `src/icc/baselines/leiden_snn.py:83-93` and `lines 187-220`
  - Benchmark Runner: `experiments/exp7_modern_baselines/src/run_exp7.py:79`
- **Mechanism:**
  - When `igraph` or `leidenalg` is missing from the host environment, earlier executions silently fell back to normalized Spectral Clustering on the SNN graph (`sc = SpectralClustering(n_clusters=k_eff)`).
  - In `run_exp7.py`, `target_k=k_true` was explicitly passed to Leiden SNN, transforming an unsupervised community detection baseline into a supervised $K$-guided spectral partitioner. The resulting metric was published as "Leiden SNN" in Table 7.
- **Remediation:** Enforce `allow_fallback=False` across all benchmarking runners. Install C-compiled `igraph` and `leidenalg` in the benchmark Docker image.

### 2.6 DEC (Deep Embedded Clustering) Handicapping
- **Location:**
  - Config: `configs/baselines.yaml:149` (`requires_gpu: true`)
  - Implementation: `src/icc/baselines/deep.py:376-407`
- **Critique:**
  - In `configs/baselines.yaml`, DEC is marked as requiring a GPU, which was used to justify excluding it from EXP7. However, `src/icc/baselines/deep.py` contains full CPU-compatible PyTorch/TensorFlow execution branches.
  - Network architecture is rigidly fixed to `[D, 500, 500, 2000, 10]` with static learning rates ($0.001$) and fixed epochs ($200$ pretrain / $100$ finetune) across all datasets.
  - For small oncology cohorts ($N=60, D=7129$ in CNS), this fully connected architecture contains over $4.5\text{M}$ trainable parameters for 60 data points ($75,000$ parameters per sample), guaranteeing severe divergence/overfitting in the autoencoder bottleneck without dataset-adaptive regularization.
- **Remediation:** Implement standard dimension-proportional encoder scaling (e.g. $[D, \min(D, 256), 64, K]$) or standard weight-decay regularization when evaluating deep baselines on $N \ll D$ regimes.

### 2.7 Hidden Base-Clusterer Switching in GAC (`base_clusterer="auto"`)
- **Location:** `src/icc/consensus_v2.py:245-247`
- **Code Mechanism:**
  ```python
  if self.base_clusterer == "auto":
      base_engine = "spectral" if N <= 100 else "kmeans"
  ```
- **Asymmetric Advantage:**
  - GAC was benchmarked against `Standard_Consensus` (which is hardcoded to single-restart K-Means in `src/icc/baselines/consensus.py:53` with `n_init=1`).
  - However, for cohorts where $N \le 100$ (Colon $N=62$, SRBCT $N=83$, CNS $N=60$, Leukemia $N=72$), GAC secretly replaced K-Means base models with **Spectral Clustering** (building 25 separate 10-NN graphs and eigensolves).
  - On cohorts with $N > 100$ (Prostate $N=102$, Ovarian $N=253$), GAC switched back to K-Means base models. Crucially, on Prostate, **Standard Consensus outperforms GAC** ($\text{ARI} = 0.0491$ vs. $0.0259$, `experiments/exp7_modern_baselines/data/modern_baselines_summary.csv:45,52`).
  - Attributing GAC's performance gains on Leukemia and SRBCT entirely to bipartite consensus is confounded by this hidden base-clusterer substitution.
- **Remediation:** Benchmark GAC and Standard Consensus under strictly matched base clusterers (either both using K-Means with identical `n_init` or both using Spectral base models).

### 2.8 Pseudoreplication in Seed Pooling
- **Location:** `research_audit/remediation/FINDING_DISPOSITION.csv:6` (Finding F-05)
- **Critique:** Stochastic seeds evaluate algorithmic optimization variance, not biological or population-level generalizability across cancer types. Pooling seeds directly deflates standard errors by a factor of $\sqrt{S}$ ($\approx \sqrt{5}$ to $\sqrt{30}$), generating artificially narrow confidence intervals and falsely low $p$-values.
- **Remediation:** Collapse within-cohort runs to cohort-level medians prior to cross-cohort hypothesis testing, or employ hierarchical linear mixed models with random effects for cohorts.

### 2.9 Two-Cohort Concentration (Collapse upon Leave-{Leukemia, SRBCT}-Out)
- **Quantitative Evidence (DerSimonian-Laird Random-Effects Meta-Analysis):**

| Evaluated Cohort Set | Pooled $\Delta\text{ARI}$ | Standard Error | 95% Confidence Interval | Heterogeneity ($I^2$) | $p$-value |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **All 6 High-D Oncology Cohorts** | $+0.0712$ | $0.0210$ | $[+0.030, +0.112]$ | $90.7\%$ | $0.0007$ |
| **Leave-Colon-Out** | $+0.0754$ | $0.0253$ | $[+0.026, +0.125]$ | $92.3\%$ | $0.0028$ |
| **Leave-CNS-Out** | $+0.0768$ | $0.0249$ | $[+0.028, +0.126]$ | $92.5\%$ | $0.0020$ |
| **Leave-Prostate-Out** | $+0.0789$ | $0.0245$ | $[+0.031, +0.127]$ | $91.7\%$ | $0.0013$ |
| **Leave-Ovarian-Out** | $+0.0769$ | $0.0248$ | $[+0.028, +0.125]$ | $92.3\%$ | $0.0019$ |
| **Leave-{Leukemia, SRBCT}-Out ($n=4$)** | **$+0.0243$** | **$0.0182$** | **$[-0.011, +0.060]$** | **$0.0\%$** | **$0.182$ (NS)** |

- **Scientific Conclusion:**
  - When Leukemia ($\Delta\text{ARI} = +0.6428$) and SRBCT ($\Delta\text{ARI} = +0.5240$) are excluded, the pooled improvement over baselines drops by **$65.9\%$** and becomes **statistically indistinguishable from zero ($p = 0.182$)**.
  - Across all 13 multi-domain benchmarks (`results/stats.json`), the omnibus Friedman test across all 12 algorithms is non-significant ($p = 0.40, \text{CD} = 4.62$).
  - The method does not possess universal high-dimensional superiority. Its benefit is strictly concentrated in cohorts with clean 1D bimodal driver expression. Where multimodality is absent (Prostate, CNS), GAC collapses to the same stability-accuracy discordance as classical baselines.

### 2.10 Core Determinacy Null Result (Knockout 4: The "Useless Core" Paradox)
- **Empirical Reality:**
  - Proposition 2 derives analytical sample determinacy bounds to certify "core anchors" for bipartite graph construction.
  - In the repository's own ablation study (Table 13, Knockout 4: $V_5 \to V_4$), comparing certified core anchors ($V_5$, ARI $0.217$) against uniform random landmark anchors ($V_4$, ARI $0.198$) yields:
    $$\Delta\text{ARI} = +0.0188 \approx +0.019, \quad 95\% \text{ CI}: [-0.0389, +0.0824], \quad \text{Wilcoxon } W = 9.0, \quad p = 0.8438$$
  - Certified core anchors provide **zero statistically measurable benefit** over uniform random landmark anchors. Bipartite graph compression is the sole operational mechanism; core certification is an empirical null.

### 2.11 OpenML 1107 Bit-for-Bit Duplicate Cohort
- **Evidence:** In `experiments/audit_controls/src/e1_extended_benchmarks.py:72`, OpenML ID 1107 was mapped under the key `glioma`. Upstream metadata and SHA-256 hash matching confirmed it is `tumors_C` (Pomeroy et al. 2002 CNS embryonal tumors, $N=60, D=7129$). All 60 samples and 7,129 features are **100% bit-for-bit identical to `cns` (OpenML 45086)**:
  `SHA-256: 0E449BF55F8E5682DE8DE4264C986C1B85B27F25CA0092B5A8A98CA2BB2A87FF`
- **Critique:** Evaluating both `cns` and `glioma` gave the Pomeroy medulloblastoma dataset double-weight in benchmark macro-averages.

### 2.12 Composite Patient Overlap in Ramaswamy GCM (OpenML 1106)
- **Evidence:** Pairwise expression profile fingerprinting across all 7,129 Affymetrix Hu6800 probes revealed that the Global Cancer Map (Ramaswamy et al. 2001) is a secondary multi-study compilation:
  - **61 of the 72 Golub Leukemia patients** appear in GCM with Pearson $r \ge 0.990$ (maximum $r = 0.99917$, all labeled `'Leukemia'`).
  - **8 of the 60 Pomeroy CNS patients** appear in GCM with Pearson $r > 0.90$ (maximum $r = 0.98538$, all labeled `'CNS'`).
- **Critique:** Evaluating GCM alongside Leukemia or CNS in cross-cohort generalizability testing constitutes patient-level pseudoreplication.

### 2.13 Derivative Compendia (E-MTAB-6698)
- **Evidence:** `E-MTAB-6698` ($N=1393$) is a secondary meta-compendium that absorbed primary GEO series, including 566 samples from `GSE39582` (CIT colorectal) and 290 from `GSE14333` (Jorissen). ComBat cross-study batch correction destroyed per-cohort benchmark isolation. Its exclusion under Gate I was confirmed.

### 2.14 Catastrophic Legacy Dataset Misattributions
- **Evidence:** Legacy benchmark script `experiments/audit_controls/src/e1_extended_benchmarks.py` contained severe misattributions:
  1. `breast_cancer_genomic` was assigned OpenML ID 1120, which is **`MagicTelescope`** ($N=19,020, D=10, K=2$), an astrophysics Monte Carlo simulation of Cherenkov gamma-ray showers with zero biological content.
  2. `gisette` was assigned OpenML ID 41027, which is **`jungle_chess_2pcs_raw_endgame_complete`** ($N=1000, D=6, K=3$), a combinatorial board game tablebase, rather than Isabelle Guyon's NIPS challenge ($D=5000$).
  3. `lung_cancer` (OpenML 1106, GCM) was executed with $K=2$, forcing 14 distinct tumor types into two clusters.
  4. Claiming "21 biological oncology cohorts" when 11 were non-biological negative controls and 2 were misattributed astrophysics/board-game files represents severe academic negligence.

---

## 3. Required Actionable Remediation Protocol for DMKD

To bring this repository and manuscript into compliance with DMKD scientific integrity standards, the following revisions are mandatory:

1. **Purge Supervised Subsampling:** In `src/icc/datasets/genomics.py`, eliminate class-conditional filtering in lines 154–165. Implement label-blind uniform subsampling.
2. **De-brand FastMVC-Surrogate:** Rename all occurrences of "FastMVC" in tables, figures, text, and cover letters to **`FastMVC-Surrogate`**. Add explicit text stating that it is an internal random-subspace heuristic proxy, or replace it entirely with official FastMICE code.
3. **Correct Sparse K-Means Sparsity:** Either re-run Sparse K-Means with the manuscript Table 2 parameter ($s = 1.1 + 0.5(\sqrt{D} - 1.1)$) or update Table 2 to reflect the executed $0.15\sqrt{D} + 1.0$ rule. Implement gap-statistic permutation tuning.
4. **Enforce Base-Clusterer Parity:** Eliminate the hidden `base_clusterer="auto"` switch in `src/icc/consensus_v2.py`. Re-run comparison with Standard Consensus under identical base engines (e.g. K-Means across all sample sizes).
5. **Recalibrate Theoretical Claims Regarding Proposition 2:** Explicitly disclose in Section 3 and Section 6 that certified core anchors are an empirical null ($\Delta\text{ARI} = +0.0188, p = 0.8438$) relative to uniform random landmarks. Frame Proposition 2 strictly as a mathematical structural identity rather than an operational driver of accuracy.
6. **Disclose Two-Cohort Performance Concentration:** Transparently report the Leave-{Leukemia, SRBCT}-Out sensitivity analysis in the primary results section, acknowledging that the method's performance advantage over standard baselines is non-significant ($p = 0.182$) when cohorts lacking bimodal oncogenic drivers are evaluated.
7. **Quarantine Inappropriate Clinical Endpoints & Contaminated Cohorts:** Remove van 't Veer 5-year metastasis prognosis from biological benchmark suites. Exclude Ramaswamy GCM from joint independent benchmark averages due to its 61-patient overlap with Golub Leukemia.

---
*Report submitted to Editorial Review Board, Data Mining and Knowledge Discovery.*
