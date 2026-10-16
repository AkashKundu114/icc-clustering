# Architectural & Methodological Decisions Log (ICC-v2 Remediation)

| Decision ID | Date | Area | Decision | One-Line Rationale |
|---|---|---|---|---|
| DEC-001 | 2026-10-13 | Manuscript Metadata | Strip author names, affiliations, emails, submission notices, and venue names for initial draft. | User requested initial preprint draft mode with anonymous author block prior to arXiv and journal submission. |
| DEC-002 | 2026-10-13 | Directory Standard | Create `paper/` containing self-contained LaTeX source synced with `ieee_manuscript/`. | Establishes single-source standard required by audit remediation protocol. |
| DEC-003 | 2026-10-13 | Feature Selection Naming | Rename VSSG to Bimodality-Gated Subspace Selection (BGSS) in algorithmic formulations where no variance stabilization transform is applied. | Reflects mathematical reality that Sarle's BC evaluates bimodal distribution rather than stabilizing variance. |
| DEC-004 | 2026-10-13 | Feature Pool Selection | Use single label-free null-calibrated threshold ($BC \ge 5/9$) with rank cap as default; record 15% legacy in supplement. | Resolves discrepancy between fixed floor and empirical data-dependent gating without label leakage. |
| DEC-005 | 2026-10-13 | Anchor Graph Formulation | Unify exact sample determinacy calculation via Proposition 2 linear-memory contingency identity across all sample sizes. | Eliminates arbitrary heuristic branch divergence at $N=2,000$ and ensures identical mathematical semantics. |
| DEC-006 | 2026-10-13 | Transfer-Cut Numerical Stability | Clamp $(1 - \lambda)$ from below at $\epsilon=10^{-4}$ with spectral norm bound in Transfer-Cut embedding. | Prevents division-by-near-zero explosion on noisy graphs where Laplacian eigenvalues approach or exceed 1.0. |
| DEC-007 | 2026-10-13 | Benchmark Reporting | Pre-register all 21 evaluated datasets in `data/registry.yaml`; report primary 13-benchmark matrix and 8-dataset supplementary matrix. | Strictly adheres to non-negotiable rule of no dataset dropping. |
| DEC-008 | 2026-10-13 | Single Source of Truth | Route all manuscript numbers and tables exclusively through `results/` via `experiments/make_paper_assets.py` and `paper/gen/numbers.tex`. | Prevents any hand-typed or untraceable numerical claims in the paper. |
| DEC-009 | 2026-10-13 | CI Gate Enforcement | Implement `tools/check_consistency.py` validating zero discrepancy between paper macros and raw result files before every build. | Automates continuous verification and eliminates regression risks. |
| DEC-010 | 2026-10-13 | Baseline Fairness | Upgrade standalone K-Means baseline to competitive `k-means++, n_init=10` standard. | Prevents artificial inflation of ICC advantage against crippled random-init single runs. |
| DEC-011 | 2026-10-13 | Proposition 1 Exactness | Derive and report exact analytic bimodal separation threshold $\Delta/\sigma > \sqrt{(3+\sqrt{15})/2} \approx 1.854$. | Corrects erroneous $\sqrt{2}$ threshold with verified Monte Carlo and analytic proof. |
| DEC-012 | 2026-10-13 | Anchor Budget Scaling | Ensure anchor budget defaults to $L = \max(40, 10K)$ bounded by core size $|\mathcal{C}_{\text{core}}|$. | Guarantees multi-class benchmarks with large $K$ are never under-anchored. |

