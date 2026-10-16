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
