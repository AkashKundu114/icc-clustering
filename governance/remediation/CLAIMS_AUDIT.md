# Discrepancy & Claims Audit Ledger (README vs. Manuscript vs. Results)

**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Date:** October 2026  
**Auditor:** Senior Research Governance & Reproducibility Auditor  
**Standard of Truth:** `paper/numbers.tex`, `results/passF/`, `paper/main.tex`  

---

## 1. Seeded Discrepancy Matrix (D1-D11)

| ID | Subject / Topic | Old README Claim | Ground Truth (Manuscript & `results/`) | Verdict | Evidence / Resolution Path |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **D1** | **Overall Grand Mean & Rank** | "ICC-v2 mean ARI 0.1718 Rank #1 and statistically significantly outperforming under Wilcoxon p<0.05" | Reconciled to frozen Pass F single source of truth: Grand Mean ARI **0.152** (Rank **5.23** of 11), Friedman omnibus $\chi_F^2 = 9.59, p = 0.48$, Nemenyi Critical Difference $CD = 4.19$ (no global dominance). On target high-D biomedical assays ($D/N > 20$), ICC-v2 commands Rank #1 with Mean ARI = **0.217** (vs Standard Consensus 0.037, DEC 0.045, K-Means 0.056). | **CORRECTED** | `paper/numbers.tex`, Table 3/4 in `paper/main.tex`. Updated in README. |
| **D2** | **Test Count** | Static badge "68/68 passed", text says "62" | Pytest test suite expanded to **84 tests** in release v2.1.0, 84 passed, 0 failed, full coverage across `src/icc` and `src/cicc`. | **CORRECTED** | `tests/`, CI test suite. Badge and text set to 84/84. |
| **D3** | **Meaningless Vanity Badge** | Fabricated "Compliant (Grade A+)" badge | Peer-review submission grades do not exist; vanity badge permanently purged from repository. Manuscript venue is Springer Nature DAMI. | **REMOVED** | Removed from README and purged. |
| **D4** | **Venue & Authorship** | Baseline table labeled ICC-v1/ICC-v2 as "TKDE 2026"; BibTeX listed 1 author | Canonical title: "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination". Manuscript has 5 authors: Akash Kundu, Trinankur Guha, Rupankar Ghatak, Anubhab Naskar, Kalyan Kumar Das. Target venue: Springer Nature DAMI. | **CORRECTED** | `paper/main.tex`, `CITATION.cff`, `README.md`. |
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
