# Manuscript Revision Log and Verification Ledger

**Manuscript Title:** *When Does Feature Gating and Anchor Consensus Salvage High-Dimensional Clustering? An Empirical and Geometric Analysis* (ICC-v2)  
**Target Venue:** Springer Nature (*Data Mining and Knowledge Discovery* / DAMI)  
**Date:** October 2026  

---

## Revision Checklist

- [x] **Item 1: Literature search (2024-2026)** -- Searched CrossRef, arXiv, OpenAlex, Semantic Scholar; saved verified 2024-2026 candidates with source URLs to `results/lit_candidates.csv`.
- [x] **Item 2: Complete and verify 12 specific candidate leads** -- Verified full bibliographic metadata for all 12 candidate leads (Nie 2024, Belucci 2025, Peng 2025, Xu 2025, Xu 2026, Zhang 2025, Zhang 2025 InfFus, Zhao 2026, Xie 2025, Wang 2026, Zhou 2024, Wani 2024).
- [x] **Item 3: CrossRef verification script (scripts/verify_refs.py)** -- Executed automated CrossRef and arXiv metadata verification script (`scripts/verify_refs.py`), confirming 51/51 entries verified (100%) in `results/refs_report.csv` with 0 unverified.
- [x] **Item 4: Filter candidates and record sentence mappings (results/refs_map.csv)** -- Mapped every bibliography entry in `results/refs_map.csv` as `(bibkey, section, sentence, why)`, establishing that zero unmapped padding citations exist.
- [x] **Item 5: Reference vintage target (>= 50% 2024-2026)** -- Verified via `scripts/ref_stats.py`: 26 of 51 citations (51.0%) published in 2024-2026, meeting the target threshold.
- [x] **Item 6: Integrate new citations into manuscript** -- Integrated verified modern citations into Sec 1, 2.1-2.4, 3, 6.2, and Table 1, adding comprehensive methodological descriptions of CoHiRF and bipartite anchor algorithms.
- [x] **Item 7: Audit manuscript claims against recent literature** -- Audited all text claims, explicitly qualifying novelty claims ("first", "unique") and positioning ICC-v2 within the 2024-2026 anchor and random subspace literature.
- [x] **Item 8: Experimental plan and execution (results/PLAN.md)** -- Committed frozen protocol in `results/PLAN.md`; kept ICC-v2 configuration frozen ($M=25, L=40, \alpha=0.15, \tau_{\text{core}}=0.50$); executed Exp 8a through 8f:
  - 8a: Ran CoHiRF on all 13 benchmarks across 250 model fits (`results/exp3_cohirf_benchmark.csv`).
  - 8b: Evaluated anchor selection on 6 high-$D$ cohorts across 180 runs (`results/exp8b_anchor_selection.csv`): Certified core V5 ($0.225$) beats random V4 ($0.190$), KMeans ($0.108$), and balanced KMeans ($0.101$).
  - 8c: Evaluated feature gating on 6 high-$D$ cohorts across 180 runs (`results/exp8c_feature_gating.csv`): BGSS ($0.225$) beats random gating ($0.161$) with a $+0.064$ gain.
  - 8d: Evaluated distance concentration across $D_{\text{noise}} \in [0, 2000]$ (`results/exp8d_distance_metrics.csv`): Euclidean collapse ($0.914 \to 0.019$) vs. Chebyshev and Cosine retention.
  - 8e: Evaluated large-$K$ anchor budget scaling on 4 cohorts (`results/exp8e_large_k_anchor_budget.csv`): $L=40 \to 0.123$ vs. $L=10K \to 0.132$ ($\Delta = +0.009$), refuting anchor starvation.
  - 8f: Evaluated sensitivity grid $M \in \{5,10,15,25,50\} \times L \in \{20,40,60,80\}$ (`results/exp8f_sensitivity_grid.csv`): asymptotic plateau for $M \ge 15$ ($0.226\text{--}0.228$) and flat response across $L$ ($\Delta \le 0.003$).
- [x] **Item 9: Regenerate benchmark tables and statistical battery** -- Recomputed Table 7 (12 methods, 13 datasets), Table 8, Friedman rank test ($\chi_F^2 = 11.56, p = 0.40$), Nemenyi CD ($4.62$), Wilcoxon-Holm tests, updated `results/stats.json`, and synchronized `paper/numbers.tex`.
- [x] **Item 10: Ground narrative in new empirical findings** -- Updated Abstract, Contributions, Sec 3, Sec 6.2-6.4, Sec 7.4, Sec 9.1, and Conclusion with honest reporting of all new empirical data without softening.
- [x] **Item 11: Format Declarations** -- Kept Funding, Data availability, and Code availability active; commented out remaining declarations with `% RESTORE BEFORE SUBMISSION...`; logged `BLOCKER-DECLARATIONS`.
- [x] **Item 12: Detailed Data and Code availability** -- Provided upstream OpenML IDs and repository URLs for all 13 benchmarks; referenced `scripts/fetch_data.py`; verified GitHub URL and release tag `v2.1.0` via `git tag -l`.
- [x] **Item 13: Automated audits** -- Executed `scripts/verify_refs.py` (51/51 verified), `scripts/ref_stats.py` (51.0% vintage), and `scripts/check_numbers.py` (100% numerical consistency).
- [x] **Item 14: Final build and polish** -- Compiled cleanly with Tectonic (`tools/bin/tectonic.exe -X compile paper/main.tex`), confirmed zero `??` or `[?` in PDF text, zero overfull `\hbox` warnings ($0\text{ pt} \le 5\text{ pt}$), and abstract length $\le 250$ words (243 words).
- [x] **Item 15: Reference vintage upgrade (>= 80% 2024-2026)** -- Curated bibliography to 47 verified references, with 38 published in 2024-2026 (80.85% vintage across IEEE TKDE, IEEE TNNLS, PR, InfFus, DAMI, JASA), verified with zero errors via `scripts/verify_refs.py`.
- [x] **Item 16: Single-citation policy enforcement** -- Audited `paper/main.tex` and `springer_manuscript/main.tex` to ensure every reference is cited exactly once at first mention (47 citations in `.tex`, 47 references in `.bib`, 0 duplicates, 0 missing).
- [x] **Item 17: Reference verification test suite** -- Implemented unit test suite `tests/test_verify_refs.py` (8 unit tests) and added `refs-check` target to `Makefile`. Total test suite passes cleanly at 94/94 tests (100%).
- [x] **Item 18: Narrative and table synchronization** -- Reconciled PBMC68k, 20 Newsgroups, Indian Pines, Yale B, and Table 8 K-Means numbers in narrative text with Pass F Table 7; accurately qualified synergy claim with Wilcoxon $p \approx 0.16$ ($n=6$).

---

## Quantitative Ledger: Old -> New Numbers

| Quantity / Metric | Old Stated Value | Corrected Value | Source / Derivation | Target File / Location |
| :--- | :--- | :--- | :--- | :--- |
| Evaluated Models Count | 11 models | 12 models (added CoHiRF) | `results/exp3_cohirf_benchmark.csv` | Abstract, Sec 6.2, Sec 10, Table 7 |
| Total Benchmark Model Fits | 2,750 fits | 3,000 fits | $2{,}750 + (6 \times 30 + 7 \times 10) = 3{,}000$ | Abstract, Sec 6.2, Sec 10, Table 7 caption |
| Omnibus Friedman Statistic $\chi_F^2$ | 9.59 ($k=11$) | 11.56 ($k=12$) | `scipy.stats.friedmanchisquare` on 13 cohorts | Sec 6.3, Sec 10, `numbers.tex` |
| Omnibus Friedman $p$-value | 0.48 | 0.40 | `scipy.stats.friedmanchisquare` on 13 cohorts | Abstract, Sec 6.3, Sec 10, `numbers.tex` |
| Nemenyi Critical Difference (CD) | 4.19 ($k=11$) | 4.62 ($k=12$) | $q_{0.05} \sqrt{k(k+1)/(6N)}$ ($q_{0.05}=3.268$) | Table 9, Sec 6.3, Sec 10, `numbers.tex` |
| Standard Consensus Omnibus Rank | 4.85 | 5.23 | Average rank across 13 datasets | Abstract, Sec 6.2, Sec 6.3, `numbers.tex` |
| K-Means Omnibus Rank | 5.00 | 5.15 (Rank 1) | Average rank across 13 datasets | Abstract, Sec 6.2, Sec 6.3, `numbers.tex` |
| DEC Omnibus Rank | 5.08 | 5.23 | Average rank across 13 datasets | Abstract, Sec 6.2, Sec 6.3, `numbers.tex` |
| ICC-v2 Omnibus Rank | 5.23 | 5.62 (Rank 4) | Average rank across 13 datasets | Abstract, Sec 6.2, Sec 6.3, `numbers.tex` |
| CoHiRF Omnibus Rank | N/A | 7.69 | Average rank across 13 datasets | Sec 6.2, Sec 6.3, `numbers.tex`, Table 7 |
| High-$D$ Subgroup Rank ICC-v2 | 2.00 | 2.17 (Rank 1) | Average rank across 6 cohorts ($D/N > 20$) | Sec 6.2, Sec 6.3, `numbers.tex` |
| High-$D$ Subgroup Rank CoHiRF | N/A | 7.67 | Average rank across 6 cohorts ($D/N > 20$) | Sec 6.2, Sec 6.3, `numbers.tex` |
| 20 Newsgroups CoHiRF ARI | N/A | $+0.105 \pm 0.010$ (Rank 1) | `results/exp3_cohirf_benchmark.csv` | Table 7, Sec 6.2 |
| Isolet CoHiRF ARI | N/A | $+0.430 \pm 0.012$ | `results/exp3_cohirf_benchmark.csv` | Table 7, Sec 6.2 |
| PBMC68k CoHiRF ARI | N/A | $+0.300 \pm 0.166$ | `results/exp3_cohirf_benchmark.csv` | Table 7, Sec 6.2 |
| Large-$K$ Anchor Budget Gain | Untested | $+0.009$ ($0.123 \to 0.132$) | `results/exp8e_large_k_anchor_budget.csv` | Sec 6.2, Sec 9.1, Sec 10 |
| BGSS vs. Random Subspaces Gain | Untested | $+0.064$ ($0.225$ vs. $0.161$) | `results/exp8c_feature_gating.csv` | Sec 6.2, Sec 7.3 |
| Certified Anchors vs. KMeans Anchors | Untested | $+0.117$ ($0.225$ vs. $0.108$) | `results/exp8b_anchor_selection.csv` | Sec 7.4 |
| Sensitivity Grid Plateau | Untested | $M \ge 15$ plateau ($0.226\text{--}0.228$) | `results/exp8f_sensitivity_grid.csv` | Sec 6.4 |
| Distance Concentration $D_{\text{noise}}=2000$ | Qualitative | Euclidean $0.019$, Cheb $0.597$, Cos $0.308$ | `results/exp8d_distance_metrics.csv` | Sec 3 |

---

## BLOCKERS

- **BLOCKER-COAUTHORS:** Obtain written approval from every co-author before formal submission sign-off.
- **BLOCKER-DECLARATIONS:** Restore commented-out Springer Nature declarations (competing interests, ethics, consent, author contributions, AI-use disclosure) before formal submission if required by target journal.

---

## NARRATIVE CHANGES

1. **Abstract:** Updated benchmark scope to 12 clustering pipelines and 3,000 total model fits; reported omnibus Friedman $p = 0.40$; reported K-Means rank (5.15), Standard Consensus rank (5.23), DEC rank (5.23), and ICC-v2 rank (5.62); confirmed abstract word count is strictly 243 words ($\le 250$).
2. **Empirical Motivation (Sec 3):** Grounded the theoretical distance concentration analysis of Peng et al. (2025) in quantitative empirical simulations (Exp 8d), reporting exact clustering collapse across Euclidean $L_2$ ($0.914 \to 0.019$), Chebyshev $L_\infty$ ($0.597$), and Cosine distance ($0.308$) up to $D_{\text{noise}}=2{,}000$.
3. **Benchmark Omnibus Results (Sec 6.2):** Integrated CoHiRF into Table 7 and text narrative, highlighting its #1 rank on 20 Newsgroups ($0.105 \pm 0.010$) and strong speech performance ($0.430 \pm 0.012$ on Isolet), while noting its struggle in extreme high-$D$ noise regimes ($0.017$ subgroup mean).
4. **Anchor Starvation Hypothesis Refuted (Sec 6.2, 9.1, 10):** Replaced earlier "untested hypothesis" statements with empirical findings from Exp 8e ($L = \max(40, 10K)$ yielding an average gain of only $+0.009$ ARI across large-$K$ benchmarks), demonstrating that performance ceilings are governed by multi-class coordinate blending in 1D projections rather than landmark sparsity.
5. **Feature Gating vs. Random Subspaces (Sec 6.2):** Added Exp 8c comparative results directly benchmarking BGSS against matched-budget random feature selection (as in CoHiRF), demonstrating a $+0.064$ subgroup ARI gain across the six cohorts.
6. **Parameter Sensitivity Surface (Sec 6.4):** Replaced previous "untested parameter regime" phrasing with systematic sensitivity grid findings from Exp 8f, proving an asymptotic stability plateau for $M \ge 15$ and broad insensitivity across $L \in [20, 80]$ ($\Delta \le 0.003$).
7. **Anchor Selection Evaluation (Sec 7.4):** Integrated Exp 8b findings showing that K-Means centroids ($0.108$) and balanced K-Means anchors ($0.101$) degrade substantially relative to certified core anchors ($0.225$) and uniform empirical anchors ($0.190$) due to noise-corrupted prototype convergence in $D/N > 20$ regimes.
8. **Conclusion (Sec 10):** Synchronized all macro-derived statistics ($\chi_F^2 = 11.56, p = 0.40, \text{CD} = 4.62$, 3,000 model fits across 12 methods), transparently reporting both high-$D$ gains and multi-class/sparse-count boundary conditions.
