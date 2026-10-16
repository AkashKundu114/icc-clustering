# Discrepancy & Claims Audit Ledger (README vs. Manuscript vs. Results)

**Date:** 2026-10-17  
**Auditor:** Subagent R (Orchestrator Independent Audit)  
**Standard of Truth:** `results/results.json`, `results/phase2/stats.json`, `manuscript/main.tex`  

---

## 1. Seeded Discrepancy Matrix (D1–D11)

| ID | Subject / Topic | Old README Claim | Ground Truth (Manuscript & `results/`) | Verdict | Evidence / Resolution Path |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **D1** | **Overall Grand Mean & Rank** | "ICC-v2 mean ARI 0.1718 Rank #1 and statistically significantly outperforming under Wilcoxon p<0.05" | Grand Mean ARI **0.1599**, overall mean rank **5.46** (5th of 11), Friedman omnibus $\chi^2 = 11.34, p = 0.33$. Pairwise Wilcoxon tests do not survive Holm-Bonferroni correction ($p \in [0.24, 0.95]$). Dominates Rank #1 ($R=2.33$) specifically on biomedical cancer assays ($D/N > 20$, Mean ARI 0.258 vs 0.050). | **CORRECTED** | `results/phase2/stats.json`, Table 3 in `manuscript/main.tex`. Updated in README. |
| **D2** | **Test Count** | Static badge "68/68 passed", text says "62" | Pytest test suite contains **76 tests**, 76 passed, 0 failed, 73% statement coverage across `src/icc`. | **CORRECTED** | `tests/`, `RELEASE/baseline/pytest_baseline.txt`. Badge and text set to 76/76. |
| **D3** | **Meaningless IEEE Badge** | "IEEE TKDE Compliant (Grade A+)" badge | Peer-review submission grades do not exist; vanity badge. | **REMOVED** | Removed from README. |
| **D4** | **Venue & Authorship** | Baseline table labeled ICC-v1/ICC-v2 as "TKDE 2026"; BibTeX listed 1 author | Manuscript has 5 authors: Akash Kundu, Trinankur Guha, Rupankar Ghatak, Anubhab Naskar, Kalyan Kumar Das. Status is "Preprint / Under Review". Venue claims removed. | **CORRECTED** | `manuscript/main.tex`, `CITATION.cff`, `README.md`. |
| **D5** | **Scalability & Missing Data Numbers** | "1,000,000 samples in under 3.5 minutes" vs 55.6 s; missing data ">80% retained at 40%" vs 38% at 30% | Extreme scale runtime on 16-core CPU is 55.6 s. Missing data retention on real datasets degrades to 38% at 30% MCAR. Memory reduction is 39.1% at $N=8,000$ and 97.0% at $N=10,000$. Exp 1 downstream accuracy improvements: SVM (+4.5%), RF (+3.8%), MLP (+4.2%). | **CORRECTED** | `results/results.json`, `numbers.tex` (`\MemoryScalingEightKReduction`, `\MemoryScalingTenKReduction`). |
| **D6** | **Baseline Count & Venues** | "evaluated against 10 baselines" vs 11 rows; Li et al. cited as Artif. Intell. 2019 | Table has 11 methods (9 external baselines + ICC-v1 ablation + ICC-v2). Li et al. core-halo consensus published in IEEE TKDE 31(8) 2019. | **CORRECTED** | Corrected table headers, venue citations, and method counts in `README.md` and `docs/`. |
| **D7** | **Figure Numbering** | Old README referenced figures up to Fig 26 | Manuscript contains 11 primary figures (`fig1` through `fig11`). Extended audit figures mapped explicitly as supplementary audit materials. | **CORRECTED** | Mapped in `docs/EXPERIMENTS.md` and `README.md`. |
| **D8** | **Dataset Properties & Madelon Structure** | Madelon described as "20 non-linear XOR features + 480 noise" | Real Madelon has 5 informative features, 15 linear combinations (redundant), and 480 distractor probes. All 13 dataset $N, D, K$ matched against `configs/datasets.yaml` and Table 3. | **CORRECTED** | Documented in `docs/DATA.md` and `README.md`. |
| **D9** | **Python API Imports & Parameter Names** | `from src.icc import ...` fails on external install; `beta` undefined in paper | Fixed imports to `from icc import ICC`. Documented `beta` as a legacy deprecated parameter retained for backward compatibility with v1 configs. | **CORRECTED** | `src/icc/__init__.py`, `pyproject.toml`, `README.md`. |
| **D10** | **Python Version Support** | Claimed Python 3.10-3.14 without verification; [deep] pulled heavy GPU frameworks | Verified CI covers Python 3.10, 3.11, 3.12 across Linux and Windows. Core package install lightweight; deep frameworks optional. | **CORRECTED** | `pyproject.toml`, `.github/workflows/ci.yml`. |
| **D11** | **Math Formatting in Markdown** | `$ +4.5% $` and `$p < 0.05$` breaking LaTeX rendering on GitHub | Cleaned mathematical expressions; percent signs escaped or moved outside math delimiters. | **CORRECTED** | Formatted throughout `README.md`. |

---

## 2. Verdict Summary
- Total Seeded Discrepancies Audited: **11**
- **Corrected:** 10
- **Removed:** 1 (Vanity badge)
- **Pending:** 0
