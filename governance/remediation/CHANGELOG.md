# Remediation Changelog

All changes and milestone deliverables during the remediation process are logged here in chronological order.

## [Phase 0: Reconnaissance] - 2026-10-17
- Initialized `remediation/phase1` branch from commit `879fd96a282e88f5491826dd7355d24d9490661b`.
- Produced `REMEDIATION/ENV.md`: Environment specification (OS, Python 3.14.6, hardware specs, pip freeze).
- Initialized `REMEDIATION/LEDGER.md`: Master registry tracking N1-N12, M1-M9, S1-S6, L1-L3, F1, and P1- issues.
- Repo cartography: Mapped experiments 0-5, dataset pipelines, method variants, and figure-generating scripts.
- Generated `REMEDIATION/CLAIMS.md`: Exhaustive 252-row quantitative claims directory (Table 3, aggregates, and Exps 0-5).
- Completed code-vs-paper and data leakage audit in `REMEDIATION/AUDIT_PHASE0.md`:
  - Verified Sarle's BC implementation (Fisher excess kurtosis + finite-sample null correction).
  - Identified `pool_mode="legacy"` default taking top $\max(100, 0.15D)$ instead of $b_d \ge 5/9$.
  - Confirmed `embedding="legacy"` default bypassing Transfer-Cut degree/eigenvalue scaling.
  - Confirmed `n_anchors=40` uniform anchor sampling without cluster stratification.
  - Empirically verified inductive `predict()` runtime is $O(K \cdot |\mathcal{F}_{\text{active}}|)$ independent of $L$.
  - Verified `cns.npz` and `glioma.npz` byte-for-byte identity in `exp3_real_world_benchmarks/data/cache`.
  - Audited Madelon XOR structure: 0 features satisfy $b_d \ge 5/9$, actual Recall@50 is 0.40 vs claimed 0.95.
- Executed Gate 0 Checkpoint review: Cleared to proceed with Phase 1 experiment reproduction.

## [Phase 1: Reproduce and Freeze] - 2026-10-17
- Subagent E1: Ran as-published test suite (`python -m pytest tests/ --cov=src/icc --cov-report=term`). Captured raw logs to `REMEDIATION/logs/test_suite.log`. Result: 76 passed, 0 failed, 14 warnings, 74% statement coverage across `src/icc`.
- Subagent E2: Executed all experiment suites (Exp 0 falsification, Exp 1 generalization, Exp 2 ablation, Exp 2.1 VSSG, Exp 3.1 13-dataset benchmark, Exp 3.5 missing data, Exp 4 scalability, Exp 5 extreme scaling) capturing raw logs to `REMEDIATION/logs/`.
- Subagent E3: Consolidated all 3,430 empirical run observations into `results/results.json`. Generated `results/MANIFEST.md` with SHA256 hashes of 73 input, cache, and result files.
- Subagent E4: Ran spot-check verification across Table 3 cells and Leukemia ICC-v2 (`REMEDIATION/AUDIT_SPOTCHECK.md`). Populated `REMEDIATION/CLAIMS.md` with evaluated outcomes (188 MATCH, 13 MISMATCH).
- Completed and signed off `REMEDIATION/PHASE1_REPORT.md`.
- Committed baseline and tagged `results-frozen` on `remediation/phase1`.

## [Phase 2: Science & Fair Baselines] - 2026-10-17
- Initialized branch `remediation/phase2` off `results-frozen`.
- Authored pre-registration protocol in `REMEDIATION/PREREG.md` fixing all hypotheses, subgroups, fair baselines, seeds, and statistical tests prior to execution.
- Subagent B (Theory & Method):
  - Solved Proposition 1 analytic separation bound: $2\theta^2 - 6\theta - 3 = 0 \implies \Delta / \sigma_0 = \sqrt{\frac{3 + \sqrt{15}}{2}} \approx 1.854$.
  - Implemented and verified numerical quadrature across $\nu \in [5, 100]$ in `scripts/verify_prop1.py` (`REMEDIATION/logs/verify_prop1.log`).
  - Authored `REMEDIATION/THEORY_NOTES.md` detailing Transfer-Cut bipartite SVD equivalence, Sarle's criterion ($5/9$), 1D marginal unimodality boundaries on XOR, and uniform random anchor behavior on small $N$.
- Subagent C (Experiments):
  - Implemented fair baselines (Variance Filter, PCA/SVD, Laplacian Score, Sparse K-Means) across all 13 benchmark datasets and 10 seeds (`scripts/run_fair_baselines.py`), outputting 1,170 records to `results/phase2/fair_baselines.csv`.
  - Implemented direct inductive out-of-sample evaluation (`scripts/run_inductive_direct.py`) across 9 datasets and 10 seeds, outputting 540 records to `results/phase2/inductive_direct.csv`.
- Subagent D (Statistician):
  - Evaluated Friedman omnibus test ($\chi^2 = 11.34, p = 0.33$) and true Nemenyi CD ($k=11, N=13 \implies \text{CD} = 4.21$).
  - Performed subgroup analysis: on the high-D subgroup ($D/N > 20$), ICC-v2 achieves #1 average rank (2.33) and 0.258 mean ARI vs 0.050 for fair baselines.
  - Generated structured statistical findings in `results/phase2/stats.json`.
- Artifact Automation:
  - Implemented `scripts/make_numbers.py` generating 49 synchronized LaTeX macros into `paper/gen/numbers.tex`, `manuscript/gen/numbers.tex`, and `springer_manuscript/numbers.tex`.
  - Generated `results/phase2/MANIFEST.md` cataloging SHA256 checksums of Phase 2 scientific outputs.

