# Phase 0: Manuscript and Claim Audit Report

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Audit Persona:** Agent A2 — Manuscript and Claim Auditor  
**Date:** November 1, 2026  
**Companion Artifact:** `research_audit/dami_revision/CLAIMS_LEDGER.csv`  

---

## 1. Executive Summary

This audit evaluates all quantitative, methodological, and theoretical claims presented in `paper/main.tex` and supporting supplementary documents against raw result artifacts, execution logs, and baseline implementations in `icc-clustering`.

### Key Audit Classifications:
- **Total Claims Audited:** 15 core quantitative and methodological claims.
- **VERIFIED:** 8 claims (53.3%)
- **VERIFIED_WITH_QUALIFICATION:** 6 claims (40.0%)
- **CONTRADICTED:** 1 claim (6.7%) — The baseline labeled `FastMVC` was an internal random-subspace bipartite proxy that did not implement FastMICE (Huang et al., 2023). It has been re-attributed as `FastMVC-Surrogate`.
- **UNSUPPORTED / OVERSTATED:** 0 unmitigated after recent audit passes, though several claims require vital caveats regarding inferential units and cohort concentration.

---

## 2. In-Depth Audit of Critical Claim Domains

### 2.1 The Six Biomedical Cohorts & The Discordance Thesis (Claims CLM-01, CLM-02, CLM-09)
- **The Claim:** In high-dimensional biomedical cohorts ($D/N > 20$), subsample stability is decoupled from clustering accuracy. Across 9 discordant cells, mean stability is 0.684, while mean ARI is $-0.003$ (column-permuted null $\approx 0.01$).
- **Evidence Verification:**
  - File: `results/stability/subsample_stability_summary.csv`
  - Recomputed: 30 stratified 80% subsamples (435 pairs per cell).
  - The 9 discordant cells across the 6 cohorts (`colon`, `leukemia`, `breast`, `prostate`, `srbct`, `cns`) reproduce the exact values: mean stability 0.684, mean ARI $-0.003$.
- **Required Qualifications:**
  1. **Post-Hoc Non-Degeneracy Rule:** Discordance is evaluated conditional on Rule (i'), which excludes trivial 1-cluster solutions where $>90\%$ of samples fall into a single cluster. Unconditional analysis (all 18 cells) exhibits lower nominal stability due to degenerate partitions. Both unconditional and conditional results must be reported transparently.
  2. **Pseudoreplication & Statistical Units:** The 6 biological cohorts cannot be expanded into "independent observations" by treating 30 random splits or multiple models on the same cohort as independent data points. The biological cohort is the primary inferential unit. With $N=6$, population-level conclusions must be framed as exploratory.

### 2.2 BGSS vs. Random Gating & Factorial Ablation (Claims CLM-03, CLM-04, CLM-05)
- **The Claim:** Bipartite consensus alone (0.046) and random feature gating (0.046 dense, 0.047 bipartite) do not improve on ambient consensus (0.037). BGSS raises ARI to 0.217 under bipartite consensus (+0.169 over matched random gating, 95% CI [+0.036, +0.310], Wilcoxon $p=0.031$). Under dense consensus, BGSS raises ARI to only 0.077.
- **Evidence Verification:**
  - File: `results/passF/ablation_stats_passF.json`, `results/passF/fair_baselines_30seeds_passF.csv`
  - 2x2 Factorial Decomposition:
    - V0 (Ambient Dense): ARI = $0.037 \pm 0.042$
    - V1 (Random Dense): ARI = $0.046 \pm 0.044$
    - V2 (BGSS Dense): ARI = $0.077 \pm 0.089$
    - V3 (Ambient Bipartite): ARI = $0.046 \pm 0.051$
    - V4 (Random Bipartite): ARI = $0.047 \pm 0.050$
    - V5 (Full ICC-v2 / BGSS Bipartite): ARI = $0.217 \pm 0.261$
- **Required Qualifications:**
  1. **Cohort Skewness / Two-Cohort Concentration:** The mean ARI of 0.217 is heavily driven by two cohorts: **Leukemia** (ARI = $0.600 \pm 0.367$) and **SRBCT** (ARI = $0.546 \pm 0.102$). The remaining 4 cohorts (`colon`, `breast`, `prostate`, `cns`) have mean ARIs ranging between $0.030$ and $0.076$. The **median** ARI is only **0.061**.
  2. **Statistical Multiplicity:** The paired Wilcoxon signed-rank test yields $W=0.0, p=0.031$ uncorrected on $n=6$. When corrected across the prespecified comparison family (Holm-Bonferroni across baseline comparisons), this comparison does not retain statistical significance at $\alpha=0.05$. The text must clearly report both uncorrected and corrected $p$-values.

### 2.3 Theoretical Bound & Core Anchor Determinacy (Claim CLM-06)
- **The Claim:** Proposition 2 derives sample determinacy bounds to certify core anchors in the bipartite graph.
- **Audit Finding & Qualification:**
  - Table 13, Knockout 4: Comparing certified core anchors (V5) against uniform random landmark anchors (V4) shows $\Delta = +0.019$ ($p=0.84$).
  - **Scientific Reality:** Certified core anchors yield an empirically indistinguishable difference from uniform random selection. Theoretical claims asserting that determinacy certification is essential for the empirical performance of ICC-v2 are contradicted by the authors' own knockout experiment. The manuscript must explicitly characterize core-anchor determinacy as an empirical null.

### 2.4 Baseline Fidelity & FastMVC (Claim CLM-11)
- **The Claim:** FastMVC baseline represents FastMICE (Huang et al., IEEE TKDE 2023).
- **Audit Finding (CONTRADICTED):**
  - Inspection of `src/icc/baselines/anchor.py` reveals that the baseline was an internal random-subspace bipartite proxy that did not faithfully implement FastMICE exemplar selection or bipartite spectral partition.
  - **Remediation Action:** The method has been formally designated as **`FastMVC-Surrogate`**, with explicit attribution to Huang et al. (2023) in `paper/references.bib` and disclosure of its surrogate nature in Table 3.

### 2.5 Omnibus Benchmark Suite Performance (Claim CLM-07)
- **The Claim:** Across 13 multi-domain benchmarks (3000 model fits across 10 methods), omnibus differences are not statistically significant (Friedman $p = 0.40$, critical difference $CD = 4.62$).
- **Evidence Verification:**
  - File: `results/stats.json`
  - Overall Rank of ICC-v2: $5.62$ (5th of 10 methods).
  - DEC rank: $5.23$, Standard Consensus rank: $5.23$, K-Means rank: $5.15$.
  - **Verdict:** Fully verified. The paper does not make false omnibus superiority claims; it accurately reports that omnibus benchmark performance is statistically indistinguishable and that ICC-v2's distinct profile emerges only in high-dimensional bimodal regimes.

### 2.6 Confounding & Technical Artifacts (Claim CLM-10)
- **The Claim:** Spurious high-stability partitions correlate strongly with PC1 ($r = 0.77 - 0.86$) and sequencing depth / library size in the Prostate cohort.
- **Evidence Verification:**
  - File: `results/prostate_pca_diagnosis.csv`
  - Confirmed: In uncurated high-dimensional biomedical matrices, unsupervised consensus clustering frequently latches onto technical depth or total intensity variations, yielding high apparent stability without biological ground truth.

---

## 3. Discrepancy Resolution: README vs. Docs vs. Manuscript

| Document | Stated Cohort Count | Model Fits Count | Baseline Designations | Status / Action |
| :--- | :--- | :--- | :--- | :--- |
| `README.md` | 6 biological + 7 general (13 total) | 3,000 model fits (10 methods × 10 seeds × 30 runs) | Updated to include `FastMVC-Surrogate` | Consistent |
| `docs/DATA.md` | 13 datasets listed with accessions | Benchmark suite manifest | Accurately distinguishes bulk microarray from synthetic | Consistent |
| `docs/REPRODUCIBILITY.md`| Exact reproduction commands | Commands match `scripts/reproduce.py` scopes | Verified against test suite | Consistent |
| `paper/main.tex` | 13 datasets (6 biomedical) | Single source of truth in `paper/numbers.tex` | Synchronized via `scripts/make_stats.py` | Consistent |

---

## 4. Recommendations for Gate G1 Protocol

1. Formally retain `FastMVC-Surrogate` designation across all manuscript figures and tables.
2. In all text reporting the $+0.169$ BGSS improvement, cite the median ($+0.015$) alongside the mean and explicitly state that the effect is driven by Leukemia and SRBCT.
3. Present both unconditional stability-accuracy distributions and conditional (non-degenerate) distributions.
4. Maintain that the 6 cohorts serve as exploratory evidence for stability-accuracy discordance; confirmatory claims require independent cohorts from the cohort expansion protocol.
