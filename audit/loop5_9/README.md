# Loop 5.9 audit package

This package reconciles Loops 5.6–5.8 and provides new provenance, statistics, benchmark, reproducibility, manuscript and prospective protocol artifacts. It is audit-only; no production source, original data, historical result, or manuscript was edited. No push or release was made.

## Evidence levels

- Local 4,320 partition/4,320 Parquet evidence is present in the separate local FYP worktree and not publicly available from a clean clone. Reconstructed metrics are saved-artifact calculations, not fresh fits or authenticated historic execution.
- The 3,000 benchmark records are local score rows with copied/imported entries; they are not 3,000 verified fit events.
- The canonical target manuscript is an ignored local file at SHA listed in `baseline_state.md`; it is not tied to target Git commit. A frozen copy is under `manuscript/pre_remediation/`.
- Public clean clone supports Tier 1 aggregate arithmetic only. See `reproducibility/tier_status.md`.
- No third-party dataset redistribution is cleared by this audit.
- Agents A and C completed independent evidence investigations. Agents B, D, and E hit usage limits after partial work; the lead executed the full stats reconstruction, a fresh clone test, and the canonical manuscript review. Agent F completed independent adjudication and directly recomputed the benchmark statistic. No original clustering fits were rerun.

## Re-execution

From the target repo root, with the local FYP path and scientific dependencies available:

```text
python audit/loop5_9/provenance/recompute_forensics.py
python audit/loop5_9/statistics/reconstruct_stats.py
python audit/loop5_9/benchmark/audit_benchmark.py
python audit/loop5_9/scripts/audit_target_manuscript.py
```

These scripts read local evidence and write into audit output directories; the stats and benchmark runs do not fit models. They are not all executable from a clean clone because raw inputs are absent. Bootstrap resampling endpoint can vary with cohort ordering and is exploratory. Do not run older Loop 5.6 aggregate-only scripts as a finalizer over partition-derived tables.

## Verdict

Loop 5.9 final verdict is **HOLD**. See `final_submission_verdict.md`, `historical_finding_register.csv`, `contradiction_register.csv`, and `independent_adjudication.md`.

The seed-42 equal-cohort bootstrap upper endpoint differs between Loop 5.8 and 5.9 because cohort ordering changes the finite Monte Carlo mapping from random indices to cohort labels. This discrepancy is retained in the contradiction register; neither variant repairs the mismatch with the cell-weighted point estimate.
