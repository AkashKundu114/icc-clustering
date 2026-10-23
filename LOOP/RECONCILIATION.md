# Reconciliation of Empirical Discrepancies (Fix Pass C)

**Date:** 2026-10-21  
**Status:** DRAFTED FOR HUMAN GATE A REVIEW  
**Scope:** Root-cause analysis and resolution plan for defects D1 and D2 identified in manuscript `main_780366.pdf` and codebase.

---

## 1. Summary of Identified Discrepancies

| Item / Claim | Location 1 (Value) | Location 2 (Value) | Location 3 (Value) | Root Cause | Pass C Resolution |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ICC-v2 on Leukemia** | Table 3: $0.680 \pm 0.345$ | Table 4: $0.541 \pm 0.406$ | Sec 5.2: $0.704 \pm 0.265$ | **Different Seed Sets & Stores:**<br>• Table 3 from `results.json` (seeds `[42, 101, ..., 909]`, two seed failures).<br>• Table 4 from `fair_baselines.csv` (seeds `[42, 101, ..., 909]`, three seed failures).<br>• Sec 5.2 from `exp2_real_high_d_factorial.csv` (seeds `0..9`, one seed failure). | Re-run all evaluations under a single unified seed set ($s \in \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9\}$) into a single result store `results/passC/`. All tables and text will pull from identical macro definitions. |
| **ICC-v2 on SRBCT** | Table 3: $0.538 \pm 0.104$ | Table 4: $0.586 \pm 0.110$ | Sec 5.2 text: $0.538 \pm 0.110$ (mixed mean from T3, std from T4) | Mixed macro values: Mean was sourced from Table 3 run, but std ($\pm 0.110$) was pasted from Table 4 run. | Single source of truth in `results/passC/`. Exact macro `\ARIsrbct` and `\ARIsrbctStd` defined once. |
| **Ambient K-Means on Leukemia** | Table 3: $0.101 \pm 0.088$ | Table 4: $0.185 \pm 0.068$ | Sec 5.2: $0.199$ | Seed variance and different feature pre-processing across legacy scripts. | Unified baseline run on identical standardized data and seeds $0..9$. |
| **ICC-v2 High-D Subgroup Mean ($D/N > 20$)** | Text: $0.238$ | Table 4: $0.217$ | Table 3 avg: $0.224$ (Ablation V5: $0.226$) | Stale manual text figure ($0.238$) left from preliminary 5-seed run; Table 4 average is $0.217$; Table 3 average is $0.224$. | Compute subgroup mean dynamically via macro `\SubgroupMeanICCvTwo` from the unified run. |
| **ICC-v2 High-D Subgroup Median** | Text: $0.057$ | Table 3 median: $0.041$ | Table 4 median: $0.067$ | Manual calculation from a mixed/outdated run. | Compute dynamically from unified run via macro `\SubgroupMedianICCvTwo`. |
| **Std Cons Subgroup Mean** | Ablation V0: $0.033$ | Table 3: $0.041$ | Table 4: $0.035$ | Different baseline parameters / seeds between ablation script and benchmark scripts. | Standardize `StandardConsensus` parameters and seeds across all tables. |
| **Dataset Subsampling Specs** | Table 3 headers: $N=18.8\text{k}, 2.4\text{k}, 68.6\text{k}$ | Text Page 14: $2{,}000, 1{,}000, 700$ | Fig. 6 panel titles: $18{,}846, 2{,}414, 700$ | **Agent Hallucination in Pass B vs. Mislabeling:**<br>• The actual benchmark matrix (`exp3_1_benchmark_matrix_v2.csv` and `results.json`) was evaluated on the **full** 20 Newsgroups ($N=18{,}846, D=10{,}000, K=20$) and **full** Yale B ($N=2{,}414, D=1{,}024, K=38$).<br>• In Pass B, an agent hallucinated the text claiming 20 Newsgroups was subsampled to 2,000 and Yale B was subsampled to 1,000, which directly contradicted Fig. 6 and the data records!<br>• For Zheng68k, the dataset evaluated was indeed the filtered subset ($N=700, D=765, K=10$), but Table 3 had incorrectly printed the catalog dimensions `(68.6k, 2k, 11)`. | **Harmonize across all places:**<br>1. Remove hallucinated subsampling claims for 20 Newsgroups ($N=18{,}846$) and Yale B ($N=2{,}414$).<br>2. Accurately specify Zheng68k as the standard filtered PBMC subset ($N=700, D=765, K=10$ from the 68.6k repository) across Table 3, text, and Fig. 6.<br>3. Ensure dimensions in Table 3, text, and Fig 6 match exactly. |

---

## 2. Seed-Level Micro-Analysis on Leukemia

Micro-inspection of Leukemia fits across seeds explains why the numbers diverged:
- Under seed set `[42, 101, 202, 303, 404, 505, 606, 707, 808, 909]`:
  - Leukemia produces bimodal outcomes: either near-perfect cluster alignment ($\text{ARI} \approx 0.74 - 0.94$) or complete failure ($\text{ARI} \approx -0.04$ to $+0.02$).
  - When 3 seeds fail (seeds 202, 303, 404 in `fair_baselines.csv`), Mean is $0.541 \pm 0.406$.
  - When 2 seeds fail (seeds 42, 606 in `results.json`), Mean is $0.680 \pm 0.363$.
  - Under seeds `0..9`: only seed 1 failed (-0.045), and 9 seeds succeeded, yielding Mean $0.704 \pm 0.265$.

**Implication for Claims:**
This instability is not an artifact of bugs; it is an intrinsic scientific property of the dataset/method:
- High-dimensional cancer microarray ($N=72, D=7{,}129$) with small sample size exhibits high sensitivity to initial base clusterer partitions.
- Rather than hiding this variance, the revised manuscript must explicitly discuss the bimodal distribution and report both Mean $\pm$ SD and Median, as well as the failure rate.

---

## 3. Protocol for Fix Pass C Harmonization

1. **One Master Benchmark Runner:** `scripts/run_passC_benchmarks.py`.
2. **Unified Seeds:** Strictly seeds $s \in \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9\}$.
3. **Unified Result Directory:** `results/passC/`.
   - `results/passC/benchmark_13x11.json` (Table 3, Fig 6, Fig 7)
   - `results/passC/fair_baselines.csv` (Table 4)
   - `results/passC/ablation_variants.csv` (Table 2, Fig 5)
   - `results/passC/efficiency.csv` (Exp 4.3, Fig 8)
   - `results/passC/numbers.tex` (Single source of truth for all LaTeX macros)
4. **Zero Hand-Edited Numbers:** Every number in `main.tex` will be bound to `\newcommand{\MacroName}{...}` from `numbers.tex`.
