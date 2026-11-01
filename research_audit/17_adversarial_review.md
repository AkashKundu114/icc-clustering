# Research Audit 17: Independent Adversarial Multi-Perspective Peer Review

**Target Journal:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Manuscript Under Review:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Date:** 2026-10-31  

---

## Reviewer A — Senior DMKD Action Editor

### Meta-Review Summary & Recommendation
**Recommendation:** **MAJOR REVISION**  
**Core Assessment:** This manuscript presents a timely and scientifically provocative premise: challenging the widespread belief that resampling stability guarantees clustering validity in high-dimensional biological data. The empirical documentation of stability–accuracy discordance on real biomedical microarrays is compelling. However, as currently drafted, the paper sits on the boundary between an algorithmic benchmark and an empirical study. To meet DMKD’s regular-paper standards, the authors must address three critical structural concerns:

### Major Concerns
1. **Scope and Framing:** Earlier sections of the paper flirted with presenting GAC as a universally superior clustering algorithm, yet the omnibus Friedman test ($p = 0.40$) proves that all 12 evaluated methods are statistically indistinguishable across the 13 multi-domain benchmarks. The authors must definitively reframe the paper around the *diagnosis and boundary conditions of stability-accuracy discordance* rather than manufacturing an algorithmic victory.
2. **Limited Cohort Inference ($n=6$):** The primary high-dimensional findings rest on only six oncology microarrays. An uncorrected Wilcoxon $p = 0.031$ across three gating comparisons is not statistically conclusive under multiplicity control.
3. **Surrogate Baselines:** FastMVC is documented in code as an ad-hoc random-subspace surrogate, yet earlier text cited Huang et al. (TKDE 2023). This must be purged from headline claims or replaced with a faithful solver.

---

## Reviewer B — Clustering & Machine Learning Specialist

### Review Summary & Recommendation
**Recommendation:** **MAJOR REVISION**  
**Core Assessment:** The paper makes several valuable mathematical and algorithmic points, notably the proof that bipartite graph compression eliminates $O(N^2)$ memory without accuracy loss, and the demonstration that sample determinacy provides no benefit over uniform random landmarks. However, there are major baseline omissions:

### Major Concerns
1. **Absence of Modern Sparse Baselines:** In high dimensions ($D \gg N$), Sparse K-Means (Witten & Tibshirani, JASA 2010) is the canonical statistical benchmark. The paper must compare BGSS’s univariate $O(ND)$ filter directly against Sparse K-Means’ joint $L_1$ lasso weights.
2. **Absence of scRNA-seq Graph Methods:** The single-cell community relies universally on SNN graph modularity (Leiden/Louvain). Demonstrating how Leiden behaves under high-dimensional noise is essential for contemporary relevance.
3. **Absence of Genuinely Unknown-$K$ Experiments:** Monti et al. (2003) consensus clustering was invented to estimate $K$. All benchmarks here assume oracle $K=K^*$. The paper must evaluate whether discordance worsens when $K$ must be discovered unsupervised.

---

## Reviewer C — Statistician & Biomedical Reviewer

### Review Summary & Recommendation
**Recommendation:** **MAJOR REVISION**  
**Core Assessment:** The statistical rigor of the paper is generally above average—specifically the use of cohort-clustered bootstraps ($B=10{,}000$) and the honest reporting of negative results (e.g. determinacy anchors $\Delta = +0.019, p = 0.84$). However, several vulnerabilities must be resolved:

### Major Concerns
1. **Concentration of Gating Gains in Two Cohorts:** The $+0.169$ gain of BGSS is driven almost entirely by Leukemia ($+0.398$) and SRBCT ($+0.447$). On Prostate, CNS, and Ovarian, the gain is essentially zero. The authors must formally explain why this occurs (lineage oncogene binarization vs. continuous polygenic staging) and test whether the effect survives a Leave-(Leukemia+SRBCT)-Out test.
2. **OpenML ID 1107 Duplication in Audit:** In `experiments/audit_controls`, `glioma` and `cns` produced identical numbers because OpenML 1107 is `tumors_C` (CNS). This dataset duplication must be excised from all extended analyses.
3. **Multiplicity Correction:** The uncorrected $p = 0.031$ on $n=6$ must be clearly qualified with Holm–Bonferroni adjusted $p$-values ($p_{\text{adj}} \approx 0.094$).

---

## 4. Rebuttal & Implementation Revision Plan

| Reviewer Critique | Action Taken in Revision | Verified Artifact / Deliverable |
| :--- | :--- | :--- |
| **Reframing Contribution** | Completely reframed paper around the diagnosis and mechanics of stability-accuracy discordance; purged universal superiority claims. | `research_audit/06_novelty_and_positioning.md` |
| **Cohort Expansion ($n=6 \to 12$)** | Expanded suite with 6 new independent bulk oncology cohorts ($D/N > 20$) and 6 scRNA-seq cohorts. | `research_audit/08_dataset_provenance.csv`, `experiments/exp6_cohort_expansion/` |
| **Sparse K-Means & Leiden** | Implemented exact Sparse K-Means ($L_1$ BCSS) and Leiden SNN graph modularity baselines. | `research_audit/11_baseline_fidelity.csv`, `src/icc/baselines/sparse_kmeans.py` |
| **Unknown-$K$ Discovery** | Designed and executed EXP8/EXP6 (Unknown-$K$ Benchmark) across 560 synthetic configurations and 12 real cohorts. | `research_audit/13_unknown_k_protocol.md`, `experiments/exp8_unknown_k/` |
| **Leukemia/SRBCT Outlier Test** | Executed Leave-(Leukemia+SRBCT)-Out validation and DerSimonian–Laird random-effects meta-analysis with forest plots. | `research_audit/15_statistical_analysis_plan.md`, `experiments/exp7_modern_baselines/` |
| **Purging OpenML 1107 Duplicate** | Identified root cause of CNS/Glioma duplication; registered true Glioma under OpenML 45089 ($N=50, D=12625$). | `research_audit/09_dataset_overlap_audit.md` |
| **Multiplicity Correction** | Applied Holm–Bonferroni step-down correction to all pairwise gating and baseline tests. | `research_audit/15_statistical_analysis_plan.md` |
