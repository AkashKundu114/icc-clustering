# Benchmark seed reconciliation

**Scope.** I inspected the local saved score CSVs, current FYP source and historical version of the CoHiRF script. This audit did not rerun clustering fits. Files in the FYP worktree are local-only; their tracked status does not authenticate the execution event.

## Authoritative saved-row schedules

The row-level seed column is the authority for describing the saved score artifact:

- Pass F (`results/passF/benchmark_matrix_passF.csv`): 2,750 rows, 11 methods. Each of the six high-dimensional cohorts (CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT) has 30 rows/method with seeds 0–29. Each of the other seven datasets has 10 rows/method with seeds 0–9. No within-cell duplicate seeds were observed.
- CoHiRF (`results/exp3_cohirf_benchmark.csv`): 250 rows. The same six cohorts use seeds 42–71, and the other seven use 42–51.
- Combined records: 3,000 rows, 156 dataset-method cells, no duplicate `(dataset, method, seed)` keys. Seed identities differ between Pass F and CoHiRF; observations are not seed-paired across method families.

Exact per-dataset/method seed lists and row counts are in `benchmark_seed_schedule.csv`.

## Source/configuration conflict

The CoHiRF generator in historical FYP commit `567c5260972f1ce29124ce8449a907bebe8b3983` declares `SEEDS_30=range(42,72)` and `SEEDS_10=range(42,52)`, matching its CSV. The current local FYP checkout (`60b163f...`) instead declares `range(0,30)` and `range(0,10)`, matching Pass F. This suggests later source synchronization, but source modification time is not proof that it generated the saved CoHiRF output. The CoHiRF CSV is attributed in Loop 5.7 to historical commit `567c526...`, but that commit/file tracking is not an execution log.

Pass F's extant general matrix runner `experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py` declares a third schedule (`[42,101,202,...,909]`) and 10 trials. It does not mention the Pass F output path. A complete tracked generator for the exact `benchmark_matrix_passF.csv` row schema was not located in this inspection. The artifact's 0–29/0–9 schedule is directly observed; the precise generating script/configuration and fit execution are therefore **unverified**. Do not infer a generating configuration from the CSV's later tracked commit.

## Recommended manuscript correction

Describe the observed schedules separately and state that seed schedules differed across benchmark components. Do not state that all algorithms shared one seed schedule or use “matched seeds” unless assignment-level proof is recovered. Friedman comparison is on dataset-by-method aggregate ARI values, not matched per-seed differences. Preserve both raw files unchanged and add their checksums and provenance in a release manifest.

**Status:** Saved seed values: VERIFIED. Generator identity for Pass F and execution identity for both CSVs: UNVERIFIED. Statistical recomputation from saved scores is separate from fresh-fit reproduction.
