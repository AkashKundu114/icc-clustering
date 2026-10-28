def update_revision_log():
    with open("REVISION_LOG.md", "r", encoding="utf-8") as f:
        text = f.read()

    new_section = """- [x] **Item 26: Clean build verification and automated number checking** -- Created and executed `scripts/check_numbers.py` verifying zero unresolved references (`??` or `[?`), zero presence of deprecated CD 3.65, and exact concordance between `results/stats.json`, `paper/numbers.tex`, and PDF text for all 16 core metrics; executed final clean compilation with Tectonic.

---

## Quantitative Ledger: Old -> New Numbers
*(Updated as each item is executed)*

| Quantity / Metric | Old Stated Value | Corrected Value | Source / Derivation | Target File / Location |
| :--- | :--- | :--- | :--- | :--- |
| ICC-v2 Grand Mean ARI | 0.183 / 0.217 | 0.152 | `results/stats.json` (mean across all 13 benchmarks) | Abstract, Sec 1, Sec 6.2, Table 7, Conclusion |
| Standard Consensus Grand Mean | Unstated / ~0.129 | 0.126 | `results/stats.json` | Table 7, Sec 6.2 |
| K-Means Grand Mean | 0.129 | 0.124 | `results/stats.json` | Table 7, Sec 6.2 |
| ICC-v2 Grand Median ARI | 0.072 | 0.055 | `results/stats.json` (median across all 13 benchmarks) | Abstract, Sec 6.2, Table 7, Conclusion |
| ICC-v2 Mean Excl. Leu/SRBCT | 0.112 | 0.076 | `results/stats.json` (11 benchmark subset) | Abstract, Sec 6.2, Conclusion |
| Friedman Test Statistic & $p$ | Ambiguous / ~0.48 | $\\chi_F^2 = 9.59, p = 0.48$ | `scripts/make_stats.py` ($k=11, N=13$) | Abstract, Sec 6.2, Table 7, Conclusion |
| Nemenyi Critical Difference | 3.65 or 4.19 | 4.19 | Analytical: $q_{0.05}=3.219 \\implies CD = 4.1876$ | Sec 5.4, Sec 6.2, Table 7, Conclusion |
| Omnibus Mean Rank (StdCons) | Unstated / ~4.85 | 4.85 (Rank 1) | `results/stats.json` | Abstract, Sec 6.2, Table 7, Conclusion |
| Omnibus Mean Rank (DEC) | 5.08 | 5.08 (Rank 2) | `results/stats.json` | Sec 6.2, Table 7 |
| Omnibus Mean Rank (K-Means) | 5.00 | 5.00 (Rank 3) | `results/stats.json` | Sec 6.2, Table 7 |
| Omnibus Mean Rank (ICC-v2) | 2.00 / 5.23 | 5.23 (Rank 4) | `results/stats.json` | Abstract, Sec 1, Sec 6.2, Table 7, Conclusion |
| High-$D$ ($D/N > 20$) Mean Rank | 2.17 | 2.00 (Rank 1, $n=6$) | `results/stats.json` (exploratory, Holm NS) | Abstract, Sec 6.2, Conclusion |
| Total Benchmark Model Fits | 4,290 vs 2,750 | 2,750 | Exact: $6 \\times 11 \\times 30 + 7 \\times 11 \\times 10$ | Abstract, Sec 5.2, Table 7, Fig 6, Conclusion |
| Bipartite Graph Memory Reduction | 97.4% ($29.96\\text{ MB}$) | 99.6% ($762.9 \\to 3.05\\text{ MB}$) | Exact float64: $N \\times L \\times 8$ vs $N \\times N \\times 8$ | Abstract, Table 4, Sec 6.1, Conclusion |
| Peak Process Dynamic RAM | Unseparated | 97.4% ($2,670.6 \\to 68.8\\text{ MB}$) | `tracemalloc` process RSS delta ($N=10{,}000$) | Sec 6.1, Table 4 |
| Scalability Run Seeds ($N=10^6$) | 30 seeds claimed | 3 seeds ($\\mathcal{S}_{\\text{scale}}=\\{0,1,2\\}$) | Real scaling run logs ($141.2 \\pm 20.3\\text{ s}$) | Sec 5.2, Sec 6.1, Table 5, Conclusion |
| Extreme Scaling Exponent | Sub-linear ($\\beta < 1$) | Approximately linear ($\\beta = 0.873$) | Power-law fit, 95% CI $[0.693, 1.054]$ includes 1.0 | Sec 6.1, Fig 5 caption, Conclusion |
| Sarle Bimodality Coeff. (Exp) | $0.556$ (Uniform only) | $5/9 \\approx 0.556$ (Analytical) | Sample $BC = \\frac{\\gamma^2 + 1}{\\kappa} = \\frac{4 + 1}{9} = 5/9$ | Remark 1, Sec 4.1 |
| Separation Ratio Definition | $\\rho = \\frac{\\mu_{\\text{inter}}}{\\sigma_{\\text{intra}}}$ | $\\rho = \\frac{\\bar{d}_{\\text{between}}}{\\bar{d}_{\\text{within}}}$ | Normalized all-pairs: $\\frac{2}{K(K-1)}\\sum_{k < l}$ | Definition 1, Eq. (1) |
| Active Feature Pool (Leukemia) | 3,564 / 1,000 | 1,069 ($\\lfloor 0.15 \\times 7{,}129 \\rfloor$) | Exact formula $\\min(D, \\max(K, \\lfloor \\alpha D \\rfloor))$ | Sec 4.1, Sec 5.2, Table 2 |
| Prostate Dimensions | $D = 5,966$ | $N = 102, D = 12,600, D/N = 123.53$ | Cached OpenML 45099 / 1159 array dimensions | Table 6, Sec 5.1 |
| PBMC68k Dimensions | 68,579 cells | $N = 700, D = 765, D/N = 1.09$ | Real cached `pbmc68k_reduced.npz` array | Table 6, Sec 5.1 |
| 20 Newsgroups Dimensions | $D = 20,000$ | $N = 18,846, D = 10,000, D/N = 0.53$ | Real cached `20newsgroups.npz` array | Table 6, Sec 5.1 |
| Factorial Interaction ($V_5 - V_2$) | Unmeasured / negative | $+0.140$ (95% CI $[+0.004, +0.321]$) | Factorial ablation on high-$D$ cohorts | Abstract, Sec 1, Sec 6.4, Table 14 |
| Anchor Cert. Effect ($V_5 - V_4$) | Significant | $+0.019$ (95% CI $[-0.039, +0.082]$) | Empirical null result (CI spans zero) | Abstract, Sec 1, Sec 6.4, Table 15 |
| Inductive Label Agreement | 94–99% claimed | 94.1%--99.2% (mean 95.3%) | Real test split predictions | Table 3, Sec 6.1, Sec 7.2 |

---

## BLOCKERS
*(Recorded as discovered)*

- **BLOCKER-CONFIG:** Discrepancy between Pass F benchmark run ($M=25, L=40, \\alpha=0.15, \\tau_{\\text{core}}=0.50$) and legacy tables ($M=20, L=50, \\alpha=0.50$); resolved in favor of the active benchmark execution logs in `results/benchmark_results.csv` and frozen in `results/INVENTORY.md`.
- **BLOCKER-CD:** Ambiguity between Nemenyi CD values 3.65 and 4.19; resolved by exact mathematical derivation: for $k=11$ methods and $N=13$ datasets, $q_{0.05} = 3.219 \\implies CD = 3.219 \\sqrt{\\frac{11 \\times 12}{6 \\times 13}} = 4.1876 \\approx 4.19$. Purged all occurrences of 3.65 across the manuscript.
- **BLOCKER-MEMORY:** Table 4 originally printed dense execution runtimes in seconds ($29.96$) under the memory column ($29.96\\text{ MB}$); resolved by separating theoretical consensus-graph memory ($3.05\\text{ MB}$, $99.6\\%$ reduction) from peak dynamic RSS/tracemalloc ($68.8\\text{ MB}$, $97.4\\%$ reduction).

---

## NARRATIVE CHANGES
*(Recorded as claims are updated)*

- **Demoted Universal Superiority:** Replaced broad superiority claims with rigorous Friedman test results: across 13 benchmarks, there is no statistically significant difference among methods ($\\chi_F^2 = 9.59, p = 0.48$). Standard Consensus achieves the top omnibus rank (4.85), and ICC-v2 ranks fourth (5.23).
- **Contextualized Grand Mean ARI:** Clarified that ICC-v2's high Grand Mean ($0.152$) is driven almost entirely by dramatic separation on two cancer microarrays (Leukemia $0.600$, SRBCT $0.546$). Across the remaining 11 datasets, ICC-v2 averages $0.076$ with a median of $0.055$, underperforming simple K-Means on Prostate ($0.012$ vs $0.049$).
- **Reframed Anchor Certification:** Acknowledged that determinacy-based anchor certification yields an empirical null result ($\\Delta = +0.019$, 95% CI $[-0.039, +0.082]$) compared to uniform random landmarks; bipartite graph compression ($O(NL)$) is the sole operational driver of efficiency.
- **Scaling Exponent Reframing:** Replaced "sub-linear scaling" claims with "approximately linear scaling", as the empirical 95% bootstrap CI on the extreme scaling exponent ($\\beta = 0.873$, CI $[0.693, 1.054]$) spans $1.0$.
- **Demoted ASPP & Conformal Inference:** Demoted speculative adaptive perturbation profiling (ASPP) and split-conformal calibration from empirical contribution claims to analytical future work in Section 8.2."""

    target = """- [ ] **Item 26: Clean build verification and automated number checking"""
    idx = text.find(target)
    if idx == -1:
        print("Target not found!")
        return

    updated_text = text[:idx] + new_section + "\n"
    with open("REVISION_LOG.md", "w", encoding="utf-8") as f:
        f.write(updated_text)
    print("Successfully updated REVISION_LOG.md")

if __name__ == "__main__":
    update_revision_log()
