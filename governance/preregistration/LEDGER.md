# Scientific Claim Ledger (LOOP/LEDGER.md)

This ledger tracks every factual and scientific claim made in the manuscript, its verification status, exact numerical macro, and backing empirical evidence in `results/`.

| Claim ID | Manuscript Location | Claim Statement | Macro / Backing File | Verification Status | Status Note |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **CLM-01** | Section 5.2 | Leukemia ICC-v2 ARI | `results/study_null_gating/tier_a_results.json` | **MISMATCH IN MS** | MS claims 0.846 (Sec 5.2) vs 0.680 (Sec 5.4) vs 0.708 (Fig 6); raw ICC-v2 ARI across 10 seeds is 0.472 (raw) and 0.693 (gated). |
| **CLM-02** | Section 5.2 | SRBCT ICC-v2 ARI | `results/study_null_gating/tier_a_results.json` | **MISMATCH IN MS** | MS claims 0.681 vs 0.538 vs 0.574/0.607; raw ICC-v2 ARI across 10 seeds is 0.566 (raw) and 0.415 (gated). |
| **CLM-03** | Section 5.4 | Dataset count in benchmark | `data/cache/` | **MISMATCH IN MS** | Figs 6-7 show 21 datasets x 9 methods, while text and Table 3 claim 13 x 11. |
| **CLM-04** | Section 5.4 | Nemenyi Critical Difference | `results/` | **INVALID CALCULATION** | CD=2.62 matches $k=9, N=21$. For $k=11, N=13$, CD is $\approx 4.2$. "Decisive separation" is mathematically false. |
| **CLM-05** | Section 5.4 | Overall Ranking of ICC-v2 | `results/` | **FALSE SUPERIORITY CLAIM** | ICC-v2 overall mean rank is 5.46 (5th out of 11), behind DEC (4.31), Std Cons (5.08), K-Means (5.31), Ward (5.31). |
| **CLM-06** | Section 4.1 | Proposition 1 Half-Separation Constant | Mathematical derivation | **MATHEMATICAL ERROR** | Constant in text is wrong; exact threshold for $\text{BC} \ge 5/9$ in equal Gaussian mixture is $\Delta/\sigma > \sqrt{\frac{3 + \sqrt{15}}{2}} \approx 1.854$. |
| **CLM-07** | Section 3.2 | Memory footprint of $O(NL)$ anchor consensus | Theoretical & empirical profiling | **CONFLICTING REPORT** | Dense $8000 \times 8000$ matrix is 512 MB; reported 1,040.5 MB peak conflicts with theoretical $O(NL)$ anchor claims. |
| **CLM-08** | Section 4.2 | Gating alone improves clustering | `results/study_null_gating/tier_a_results.json` | **REFUTED** | VSSG+KMeans scores 0.019 on Leukemia vs plain KMeans 0.101. Downstream gains stem from the ensemble/spectral stages. |
