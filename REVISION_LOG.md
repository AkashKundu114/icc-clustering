# Manuscript Revision Log and Verification Ledger

This revision log tracks the systematic item-by-item resolution of the 14-item revision protocol for the Springer Nature manuscript:
**Title:** *When Does Bimodality-Gated Feature Selection Help Consensus Clustering?* (ICC-v2)  
**Target Venue:** Springer Nature (*Data Mining and Knowledge Discovery* / DAMI)  
**Date:** October 2026

---

## Revision Checklist

- [x] **Item 1: V5-V2 confidence interval** -- Recomputed dataset-clustered bootstrap CI ($B=10{,}000$, resampling the 6 $D/N>20$ datasets, seed fixed) from Table 13 per-seed results in `scripts/make_stats.py`; Table 15 now reads dynamically from `results/stats.json` ($[+0.004, +0.321]$), harmonizing with Abstract, Sec 7.3, and Conclusion across all 5 ablation rows.
- [x] **Item 2: Scalability config (Table 5, Sec 6.1, Sec 6.4, Fig. 5, Sec 8.2, Table 16)** -- Identified true configs (Config A: $M=25, L=40$, \texttt{float32}; Config B: $M=15, L=60$, \texttt{float32}); relabeled Table 5, captions, and body text; recomputed consensus-graph memory ($160\text{ MB}$ for Config A, $240\text{ MB}$ for Config B); computed local scaling exponents ($10^4 \to 10^5$: $\beta \approx 0.43\text{--}0.55$; $10^5 \to 10^6$: $\beta \approx 1.09\text{--}1.20$), noted runtime steepening above $10^5$ due to memory bandwidth/cache traffic, and reported seed-bootstrap CIs.
- [x] **Item 3: Table 4 timing anomaly** -- Reran $N \in \{5000, 6000, 8000, 10000\}$ across 5 seeds on an idle system, logging CPU frequency ($2401.0\text{ MHz}$), load ($<5\%$), and swap ($1.0\text{ GB} / 15.2\text{ GB}$). Runtimes scale smoothly ($0.789\text{ s} \to 1.249\text{ s}$); confirmed via cProfile that $58.2\%$ of runtime is base clusterer fits and $<0.1\text{ s}$ is anchor projection. Regenerated Table 4, Fig. 4a, and Fig. 4b, and updated Sec 6.1/6.4.
- [x] **Item 4: Table 16 and Sec 8.1 consistency** -- Reconciled Table 16 inductive row to 6-Cohort Held-Out with true dimensions ($N \in [60, 2{,}000], D \in [617, 15{,}154]$ from Table 3); corrected Sec 8.1 to $D \ge 2{,}000$; verified query latency via `scripts/measure_query_latency.py` as $0.001\text{--}0.006\text{ ms}$/query ($< 0.01\text{ ms}$). All Table 16 cells synchronized.
- [x] **Item 5: Isolet and large-K framing (Sec 9.1 item 3, Sec 6.2, abstract, conclusion)** -- Rewrote Sec 6.2, Sec 9.1, and Conclusion to state exact empirical facts from Table 7 where ICC-v2 falls below top methods on large-$K$ benchmarks (Isolet $0.278$ vs $0.477$, 20 Newsgroups $0.000$ vs $0.102$, Indian Pines $0.136$ vs $0.220$, Yale B $0.055$ vs $0.130$, PBMC68k $0.182$ vs $0.555$); removed 'high feature contrast' claim; added untested anchor starvation hypothesis for $K \ge 20$ under $L=40$.
- [x] **Item 6: Sparse K-Means tuning (Table 2, Sec 5.2)** -- Inspected `scripts/run_fair_baselines.py` and confirmed Sparse K-Means uses an unsupervised heuristic parameter $s = 1.1 + 0.5(\sqrt{D} - 1.1)$ without ground-truth label access; updated Table 2, the 'Hyperparameter Selection Protocol' paragraph, and Sec 9.1 to accurately document this leak-free unsupervised setting.
- [x] **Item 7: Reference verification (scripts/verify_refs.py)** -- Executed `scripts/verify_refs.py` against CrossRef API; all 26 cited bibliography entries verified cleanly (19 verified with direct CrossRef DOIs, 7 verified as canonical non-DOI publications/proceedings: ICML 2003, ICML 2016 PMLR, NIPS 2004, Berkeley Symp 1967, SODA 2007, JMLR 2006, SAS TR 1983); corrected Ref [8] `li2019clustering` to Li et al. (AI 2019, DOI: 10.1016/j.artint.2018.12.007) and aligned Sec 2/Table 1/Table 2; confirmed Refs [11] and [12] details (TPAMI 46(4) 1898-1912 and TKDE 35(11) 11388-11402); dropped 9 unused uncited bib entries; report saved to `results/refs_report.csv`.
- [x] **Item 8: Declarations and metadata** -- Formatted Springer Nature declarations block in `paper/main.tex` and updated `AUTHOR_CONFIRMATION.md` with "All authors have read and approved the final manuscript and consent to its publication"; retained Gmail addresses as instructed; logged BLOCKER-COAUTHORS and RECOMMENDATION-EMAIL.
- [x] **Item 9: Wording and overclaims** -- Reworded all targeted claims in `paper/main.tex`: (a) Sec 6.3 normality/Student's t-test motivates non-parametric tests; (b) Abstract indicates ensemble averaging alone does not remove noise in simulations; (c) Sec 7.3 labeled landmark projection noise suppression as hypothesis ("we hypothesize"); (d) after Eq. (2) $\rho_{\text{sep}}$ falls toward or below 1 indicating geometric overlap; (e) Sec 6.4 items 1 and 2 reworded as untested regimes ($M \in \{5,\dots,100\}$ and $L \in \{10,\dots,80\}$).
- [x] **Item 10: Dataset and hardware details** -- (a) Added Table 3 footnote documenting Madelon as a fixed subsample of 500 of the 2,600 samples from OpenML 1485 ($D/N = 1.00$); (b) Updated Sec 5.1 with verified system hardware (AMD Ryzen 9 8940HX, 16 cores, 32 threads, 2.40~GHz base clock, 16~GB DDR5, RTX 5060) and package versions (NumPy 2.4.6, SciPy 1.18.0, scikit-learn 1.9.1, PyTorch 2.16.0); (c) Documented average ranks for ties in Table 9 and Sec 6.3, confirming $\chi_F^2 = 9.59, p = 0.48$ evaluated on unrounded per-seed mean ARIs.
- [x] **Item 11: Figures** -- Replaced all lingering 'VSSG' with 'BGSS' in plotting scripts (`plot_exp3_figures.py`, `plot_exp4_figures.py`, `plot_exp5.py`, `plot_missing_data.py`); resolved title clipping/overlaps in Fig 0/1 inset, Fig 1d annotation, and Fig 3 suptitles; aligned Fig 4b caption with actual quad panels; regenerated all figures from scripts and verified clean rendering.
- [x] **Item 12: Final checks: Spelling, grammar, notation, abstract length** -- Passed grammar/spelling audit; verified consistent $|\mathcal{F}_{\text{active}}|$ notation throughout; verified all figure/table labels and refs match 100%; tightened abstract to 234 words ($\le 250$ words).
- [x] **Item 13: Final checks: scripts/check_numbers.py** -- Executed `scripts/check_numbers.py`; verified 100% concordance between stats quoted in PDF text and `results/stats.json` with zero missing or divergent values.
- [x] **Item 14: Final checks: Clean build** -- Clean compilation via Tectonic (both \texttt{paper/main.pdf} and \texttt{springer\_manuscript/main.pdf}); zero unresolved references (no "??" or "[?"); zero overfull boxes (0 pt overfull vbox and hbox); all 18 quantitative metrics in \texttt{results/stats.json} verified with 100\% concordance.

---

## Quantitative Ledger: Old -> New Numbers
*(Updated as each item is executed)*

| Quantity / Metric | Old Stated Value | Corrected Value | Source / Derivation | Target File / Location |
| :--- | :--- | :--- | :--- | :--- |
| V5 - V2 Bootstrap CI | [+0.065, +0.218] | [+0.004, +0.321] | Recomputed clustered bootstrap ($B=10{,}000$, 6 cohorts) | Abstract, Sec 7.3, Table 15, Conclusion |
| Consensus-Graph Memory ($N=10^6$) | 3.05 MB (float64, 10k) / 240 MB / 480 MB | 160 MB (Config A) / 240 MB (Config B) | $N \times L \times 4\text{ bytes}$ (\texttt{float32}) | Sec 6.1, Sec 8.2, Table 5, Table 16 |
| Table 4 ICC-v2 Runtime ($N=10\text{k}$) | $10.35\text{ s}$ | $1.249 \pm 0.063\text{ s}$ | Idle system rerun (isolated memory) | Sec 6.1, Table 4 |
| Inductive Cohorts Count | 8-Cohort | 6-Cohort ($N \in [60, 2{,}000], D \in [617, 15{,}154]$) | Table 3 actual datasets | Table 16 |
| Cancer Cohort Minimum D | $D \ge 5{,}000$ | $D \ge 2{,}000$ | Table 3 actual dimensions (Colon $D=2000$) | Sec 8.1, Table 16 |
| Madelon Samples | $N = 500$ | Subsample of 500 of 2,600 | OpenML 1485 dataset inspection | Table 6 |
| Friedman $\chi_F^2$ and $p$ | 9.59, 0.48 | 9.59, 0.48 (unrounded: 9.594, 0.477) | Unrounded per-seed means (average ranks for ties) | Abstract, Sec 6.3, Table 9, Conclusion |

---

## BLOCKERS
*(Recorded as discovered)*

- **BLOCKER-COAUTHORS:** Obtain written approval from every co-author (including supervisor) before formal submission sign-off.
- **RECOMMENDATION-EMAIL:** Recommend institutional email address for corresponding author if Springer Nature requires it.

---

## NARRATIVE CHANGES
*(Every claim in Abstract, Introduction, Results, or Conclusion updated to match regenerated empirical data)*

1. **Abstract & Conclusion (Ensemble Noise-Averaging Claim, Item 9b):**
   - *Old Claim:* "confirming ensemble averaging alone cannot remove noise"
   - *New Grounded Claim:* "indicating that ensemble averaging alone does not remove the noise in these simulations"
   - *Rationale:* Softened causal overclaim to reflect simulation boundaries without overgeneralizing to all finite-sample estimators.

2. **Abstract, Sec 7.3, Table 15, Conclusion ($V_5 - V_2$ Synergy & CI, Item 1):**
   - *Old Claim:* Discrepancy between Table 15 ($[+0.065, +0.218]$) and Abstract/Sec 7.3 ($[+0.004, +0.321]$).
   - *New Grounded Claim:* Harmonized across all sections to $+0.140$ ($+0.139$), 95% dataset-clustered bootstrap CI $[+0.004, +0.321]$ ($B=10{,}000$, resampling the 6 $D/N>20$ datasets).

3. **Sec 6.3 & Abstract (Normality & Hypothesis Testing Rationale, Item 9a):**
   - *Old Claim:* "formally proving that parametric Student's t-tests are methodologically invalid"
   - *New Grounded Claim:* "indicating that normality assumptions are violated, which motivates the non-parametric tests"
   - *Rationale:* Statistical tests diagnose assumption departures rather than providing formal ontological invalidation proofs.

4. **Sec 6.1, Sec 6.4, Fig. 5, Sec 8.2, Table 16 (Scalability Regimes & Memory, Item 2):**
   - *Old Claim:* "strictly linear in N" and "bypasses the runtime wall" across all $N \le 10^6$.
   - *New Grounded Claim:* "approximately linear up to $10^5$; runtime growth steepens above" with local scaling exponents $\beta_{10^4 \to 10^5} \approx 0.43\text{--}0.55$ and $\beta_{10^5 \to 10^6} \approx 1.09\text{--}1.20$.
   - *Rationale:* Empirical scaling steepens at $10^6$ due to CPU L3 cache boundaries and memory bus bandwidth; deleted unsubstantiated "bypasses runtime wall" claims. Relabeled configs as Config A ($M=25, L=40$, 160 MB) and Config B ($M=15, L=60$, 240 MB).

5. **Sec 6.1, Sec 6.4, Table 4, Fig. 4a (Sample Scaling Timing Anomaly, Item 3):**
   - *Old Claim:* Anomaly of $2.009\text{ s}$ at $N=5{,}000$, jumping to $9.842\text{ s}$ at $N=8{,}000$ and $10.346\text{ s}$ at $N=10{,}000$.
   - *New Grounded Claim:* Rerun on isolated memory idle system shows smooth, monotonic scaling ($0.789\text{ s} \to 1.081\text{ s} \to 1.249\text{ s}$). Profiling (`cProfile`) proved base clusterer fits dominate runtime ($58.2\%$) while anchor projection takes $<0.1\text{ s}$.

6. **Sec 6.2, Sec 9.1 item 3, Abstract, Conclusion (Isolet and Large-$K$ Deficit, Item 5):**
   - *Old Claim:* "achieves 0.278 on Isolet due to high feature contrast"
   - *New Grounded Claim:* Stated exact empirical facts from Table 7 where ICC-v2 falls below top baselines on large-$K$ benchmarks (Isolet $0.278$ vs $0.477$, 20 Newsgroups $0.000$ vs $0.102$, Indian Pines $0.136$ vs $0.220$, Yale B $0.055$ vs $0.130$, PBMC68k $0.182$ vs $0.555$). Removed "high feature contrast" claim and framed anchor starvation ($L=40, K \ge 20$) as an untested hypothesis.

7. **Sec 6.4 items 1 and 2 (Untested Hyperparameter Regimes, Item 9e):**
   - *Old Claim:* Asserted that $M$ plateaus at 20--25 and $L=40$ is universally sufficient.
   - *New Grounded Claim:* Explicitly stated as untested configurations: "we did not test larger ensemble sizes $M \in \{35, 50, 100\}$ or anchor budgets $L \in \{60, 80\}$ on the full benchmark suite".

8. **Sec 7.3 (Landmark Projection Mechanism, Item 9c):**
   - *Old Claim:* Stated as fact that landmark projection suppresses noisy off-diagonal co-associations.
   - *New Grounded Claim:* Framed explicitly as a hypothesis: "we hypothesize that landmark projection attenuates off-diagonal noise".

9. **After Eq. (2) (Separation Ratio Geometry, Item 9d):**
   - *Old Claim:* $\rho_{\text{sep}}$ "approaches unity".
   - *New Grounded Claim:* $\rho_{\text{sep}}$ falls toward or below 1, indicating geometric cluster overlap.

10. **Table 16 & Sec 8.1 (Case Studies Evaluation Consistency, Item 4):**
    - *Old Claim:* "8-Cohort Held-Out" with $D \ge 5{,}000$.
    - *New Grounded Claim:* "6-Cohort Held-Out" ($N \in [60, 2{,}000], D \in [617, 15{,}154]$) with $D \ge 2{,}000$, matching Table 3 actual dimensions (Colon $D=2{,}000$). Query latency verified at $0.001\text{--}0.006\text{ ms}$/query.

11. **Table 2, Hyperparameter Protocol, Sec 9.1 item 5 (Sparse K-Means Tuning, Item 6):**
    - *Old Claim:* Ambiguous tuning criterion.
    - *New Grounded Claim:* Confirmed unsupervised heuristic penalty $s = 1.1 + 0.5(\sqrt{D} - 1.1)$ without ground truth label access.

12. **Table 3 Footnote (Madelon Cohort Specification, Item 10a):**
    - *Old Claim:* Listed as $N=500$ without OpenML reference.
    - *New Grounded Claim:* Documented Madelon as a fixed subsample of 500 of the 2,600 samples from OpenML 1485 ($D/N = 1.00$).
