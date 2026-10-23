# AI Use Disclosure and Verification Log

**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Date:** October 2026  
**Status:** DRAFTED FOR HUMAN AUTHOR AUDIT (PASS F & RELEASE v2.1.0)  
**Guidelines Followed:** Springer Nature Policies on AI Authorship and Generative Tools.

---

## 1. Summary of AI Tools and Platforms Used

| Tool / Platform | Developer | Environment | Primary Role in Project | Human Supervision / Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **Antigravity AI Assistant** | Google DeepMind / Google | Local Workspace (`d:\Final Year Project`) | Code maintenance, LaTeX document formatting, automated script execution, cross-reference and discrepancy checks | All generated scripts, LaTeX diffs, and results audited by Akash Kundu and co-authors. |
| **Gemini Models (Flash / Pro / Experimental Checkpoints)** | Google | Antigravity Engine | Reasoning, iterative drafting of title, abstract, and conclusion, bibtex auditing, statistical script authoring, query parsing | Supervised directly; every quantitative claim verified against raw CSV/JSON logs. |
| **Tectonic / XeTeX Tooling** | Open Source (Alex Chernyakhovsky et al.) | Local Windows CLI / Environment | Compiling Springer Nature LaTeX (`sn-jnl.cls`) into `main.pdf` | Build verification; log output monitored for warnings, citations, and overfull boxes. |
| **Python Tooling (NumPy, SciPy, Scikit-Learn, PyTorch, Numba)** | Open Source Community | Local Python 3.14 Environment | Executing benchmark algorithms, metrics computation, and statistical significance tests | Automated execution; seeds fixed to reproducible pseudorandom sequences. |

---

## 2. Granular Task-by-Task AI Use Ledger

### Task 1: Iterative Drafting, Rewriting, and Textual Refactoring
- **AI Action:** Iteratively drafted, refactored, and pruned text across the title, abstract, methodology, empirical results, and conclusion of `springer_manuscript/main.tex`.
- **Key Changes:**
  - Grounded abstract and conclusion in empirical evidence (withdrawing claims of uniform baseline dominance; explicitly highlighting DEC Rank #1 at $R=4.31$ and ICC-v2 at $R=5.46$, $p=0.33$, with median ARI $0.045$).
  - Rewrote Section 5.2 to dissect finite-sample discrete bimodality on Leukemia ($N=72, D=7{,}129$), explaining the divergence across 10-seed cohorts (8/10 successes = $0.680$, 9/10 successes = $0.704$, 7/10 successes = $0.541$; 30-seed aggregate mean $0.600 \pm 0.367$, median $0.787$, $76.7\%$ success rate).
  - Clarified Ambient K-Means initialization disparity ($n\_init=5$ yielding $0.199$ in ablation vs. $n\_init=1$ yielding $0.101$ in benchmark matrix).
  - Explicitly disclosed the Exp. 5 extreme scaling protocol difference ($N=10^6$ in $55.6\text{s}$ using float32, $M=15, L=60$ on synthetic Gaussian data vs. default double precision, $M=25, L=40$ requiring $10.35\text{s}$ at $N=10^4$).
- **Human Verification:** Confirmed that every descriptive claim matches raw benchmark CSVs and statistical test logs.

### Task 2: Statistical Methodology & Significance Testing
- **AI Action:** Implemented paired dataset-level cluster bootstrap resampling ($B=10{,}000$) and paired Wilcoxon signed-rank tests across the 6 high-D datasets.
- **Key Findings:**
  - Certified anchors (V5) vs. uniform random anchors (V4) yield $\Delta = +0.010$, with a 95% cluster bootstrap CI of $[-0.051, +0.076]$ (spanning zero) and Wilcoxon $W = 8.0, p = 0.69$, proving that anchor certification provides no statistically significant advantage over random anchor selection.
  - Computed Friedman omnibus test ($\chi_F^2 = 9.59, p = 0.48$) and Nemenyi Critical Difference ($CD = 4.19$ for $k=11, N=13$) strictly matching `paper/numbers.tex`.
  - Recomputed overall mean ranks in Pass F frozen store: ICC-v2 achieves Grand Mean ARI = 0.152 (Rank 5.23) and commands Rank #1 with Mean ARI = 0.217 on the targeted high-D subgroup ($D/N > 20$).

### Task 3: Bibliography Audit & CrossRef Querying
- **AI Action:** Executed automated HTTP queries to CrossRef API (`https://api.crossref.org/works/`) for all bibtex citations in `springer_manuscript/references.bib` via `scripts/run_refs_audit.py`.
- **Corrections Applied:**
  - Corrected Topchy et al. [4] to IEEE TPAMI Vol. 27, Issue 12, pp. 1866-1881 (2005) (fixing erroneous Issue 11).
  - Corrected Huang et al. [8] to IEEE TKDE Vol. 28, Issue 5, pp. 1312-1326 (2016) (fixing erroneous Issue 4).
  - Corrected Liu et al. [9] to IEEE TKDE Vol. 29, Issue 5, pp. 1129-1143 (2017) with co-author Junjie Wu (fixing erroneous Issue 4).
  - Corrected Huang et al. [15] to IEEE TKDE Vol. 35, Issue 11, pp. 11388-11402 (2023).
  - Verified Huang et al. [16] (TKDE Vol. 32, Issue 6, pp. 1212-1226) and Hartigan & Hartigan [19] (Ann. Statist. Vol. 13, No. 1, pp. 70-84).
  - Added baseline citation for Core-Halo Consensus (Li et al., TKDE 2018/2019) with algorithmic description in Section 5.1.

### Task 4: Figure Generation & Synchronization
- **AI Action:** Re-generated and synchronized high-resolution (300 DPI) publication figures:
  - Fig. 6 (`fig14_benchmark_matrix_13datasets.png`): Replaced legacy labels "Li et al. (2019)" with "Core-Halo Cons.", "ICC-v2 (VSSG+Anchor)" with "ICC-v2 (BGSS+Anchor)", and panel title to "PBMC68K-REDUCED".
  - Fig. 8 (`fig24_anchor_fidelity_quad.png`): Re-plotted directly from measured scaling logs (`exp4_sample_scaling_summary.csv`), aligning panels (time, speedup, graph RAM, peak RAM) with caption numbers ($10.35\text{ s}$ vs $29.96\text{ s}$, $68.8\text{ MB}$ vs $2{,}670.6\text{ MB}$).
  - Synced figures across `springer_manuscript/figures/`, `paper/figures/`, and `manuscript/figures/`.

### Task 5: LaTeX Table Formatting & Errata Fixes
- **AI Action:**
  - Table 2: Updated column headers to "Stability-Weighted Centroid (Eqs. 6--7)" and "Unweighted Nearest Centroid", replacing speculative text with an empirical Voronoi assignment explanation.
  - Table 4: Renamed Zheng68k row to "PBMC68k-reduced" ($N=700$) and added dual mean rank rows (All 13 vs. 12 datasets).
  - Updated numbers macro generator (`scripts/make_numbers.py`) and verified all LaTeX macros against raw logs.

---

## 3. Author Oversight Statement

The lead author (Akash Kundu) and co-authors confirm that:
1. No text or numerical results generated by artificial intelligence tools were accepted without verification against underlying software logs and raw data.
2. The AI assistant was utilized solely as an automated calculation, search, code audit, iterative drafting, and LaTeX formatting aid.
3. The authors retain full intellectual responsibility for the veracity, methodology, and conclusions presented in the manuscript.
