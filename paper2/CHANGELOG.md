# Changelog

All notable changes to the `nullconsensus` package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-10-28

### Added
- **Core Estimator (`NullConsensus`):** Scikit-learn compatible estimator featuring `fit`, `predict`, and `fit_predict`.
- **Permutation-Null Feature Gating (`NullGate`):** Non-parametric column-permutation testing against empirical null benchmarks.
- **Count-Aware Hurdle Gating (`HurdleGate`):** Two-part hurdle decomposition for zero-inflated scRNA-seq and sparse text.
- **Saliency-Weighted Subspace Generation:** Soft Multinomial subspace sampling with temperature scaling.
- **Evaluation Battery:** Standardized baselines (K-Means, Ward, Spectral, Dense Consensus, Anchor Graph, CoHiRF, Sparse K-Means), paired Wilcoxon tests, and bootstrap confidence intervals.
- **Test-Set Guard (`data.guard`):** Pre-registration access barrier preventing test-set peeking prior to freeze tag.
