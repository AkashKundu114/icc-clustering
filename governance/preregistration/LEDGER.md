# Scientific Claim Ledger (LOOP/LEDGER.md)

**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  

This ledger tracks every factual and scientific claim made in the manuscript, its verification status, exact numerical macro, and backing empirical evidence in `paper/numbers.tex` and `results/passF/`.

| Claim ID | Manuscript Location | Claim Statement | Macro / Backing File | Verification Status | Status Note |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **CLM-01** | Section 5.2 | Leukemia ICC-v2 ARI | `paper/numbers.tex`, `results/passF/` | **RESOLVED IN PASS F** | Reconciled across 30 seeds: Golub Leukemia ARI = 0.600 +- 0.367 (median 0.787, 73.3% > 0.50) bound to macro `\LeukemiaTableThreeARI`. |
| **CLM-02** | Section 5.2 | SRBCT ICC-v2 ARI | `paper/numbers.tex`, `results/passF/` | **RESOLVED IN PASS F** | Reconciled across 30 seeds: Khan SRBCT ARI = 0.546 +- 0.102 (median 0.547) bound to macro `\SrbctTableThreeARI`. |
| **CLM-03** | Section 5.4 | Dataset count in benchmark | `data/cache/` | **MISMATCH IN MS** | Figs 6-7 show 21 datasets x 9 methods, while text and Table 3 claim 13 x 11. |
| **CLM-04** | Section 5.4 | Nemenyi Critical Difference | `results/` | **INVALID CALCULATION** | CD=2.62 matches $k=9, N=21$. For $k=11, N=13$, CD is $\approx 4.2$. "Decisive separation" is mathematically false. |
| **CLM-05** | Section 5.4 | Overall Ranking of ICC-v2 | `paper/numbers.tex`, `results/passF/` | **RESOLVED IN PASS F** | Omnibus mean rank is 5.23 (Grand Mean ARI = 0.152); commands Rank #1 with Mean ARI = 0.217 on target high-D subgroup ($D/N > 20$). |
| **CLM-06** | Section 4.1 | Proposition 1 Half-Separation Constant | Mathematical derivation | **MATHEMATICAL ERROR** | Constant in text is wrong; exact threshold for $\text{BC} \ge 5/9$ in equal Gaussian mixture is $\Delta/\sigma > \sqrt{\frac{3 + \sqrt{15}}{2}} \approx 1.854$. |
| **CLM-07** | Section 3.2 | Memory footprint of $O(NL)$ anchor consensus | Theoretical & empirical profiling | **CONFLICTING REPORT** | Dense $8000 \times 8000$ matrix is 512 MB; reported 1,040.5 MB peak conflicts with theoretical $O(NL)$ anchor claims. |
| **CLM-08** | Section 4.2 | Gating alone improves clustering | `results/study_null_gating/tier_a_results.json` | **REFUTED** | VSSG+KMeans scores 0.019 on Leukemia vs plain KMeans 0.101. Downstream gains stem from the ensemble/spectral stages. |
