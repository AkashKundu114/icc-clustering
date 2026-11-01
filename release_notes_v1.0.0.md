# An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts (Release v1.0.0)

Official open-source benchmark suite, experimental pipelines, and algorithmic reference implementation accompanying the manuscript:
**"An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts"** (Submitted to Springer Nature *Data Mining and Knowledge Discovery* / DAMI).

---

## Overview

Subsample stability is widely assumed to guarantee clustering reliability, and consensus clustering is assumed to resist high-dimensional noise. In this study, we empirically investigate this premise across controlled synthetic distractor simulations and six high-dimensional biomedical cancer cohorts ($D/N > 20$, $D \in [2{,}000, 15{,}154]$).

This repository contains the complete reproducible research bundle:
1. **Empirical Benchmarks:** 3,000 model fits across 13 multi-domain benchmarks evaluating 12 comparative clustering pipelines (classical, deep, fuzzy, sparse, and consensus methods).
2. **Stability–Accuracy Discordance Audit:** Stratified 80% subsampling (30 draws, 435 pairs per cohort), column-permuted null controls, and post hoc non-degeneracy audits.
3. **Gated Anchor Consensus (GAC / ICC-v2):** Linear $O(N \cdot D)$ Bimodality-Gated Subspace Selection (BGSS) using finite-sample null-corrected Sarle's Bimodality Coefficient, rectangular $O(N \cdot L)$ bipartite Transfer-Cut consensus, and closed-form inductive out-of-sample prediction.
4. **Reproducibility Test Harness:** Automated test suites verifying statistical claims, bootstrap confidence intervals, and LaTeX tables.

---

## Release v1.0.0 Contents

- `src/icc/`: Complete Python reference implementation for Gated Anchor Consensus (GAC) and baseline algorithms.
- `src/cicc/`: Conformal uncertainty quantification and decoy-assisted false discovery rate screening.
- `experiments/`: Full replication suites for synthetic noise degradation, out-of-sample inductive generalization, component knockout ablations (V0–V5), and real-world multi-domain benchmarks.
- `results/`: Raw empirical result logs, pre-computed benchmark stores (`results/stats.json`), and non-degeneracy audits.
- `paper/`: Complete LaTeX source files (`main.tex`, `numbers.tex`, `references.bib`), compiled manuscript PDF, and 300 DPI publication figures.

---

## Citation & Reference

If you use this benchmark suite, algorithm, or codebase in your research, please cite:

```bibtex
@article{kundu2026empirical,
  title   = {An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts},
  author  = {Das, Kalyan Kumar and Kundu, Akash and Mukhopadhyay, Anirban},
  journal = {Data Mining and Knowledge Discovery (Under Review)},
  year    = {2026},
  url     = {https://github.com/AkashKundu114/icc-clustering}
}
```
