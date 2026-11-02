# Loop 6.0 benchmark verdict

## Direct recalculation

The lead audit executed `benchmark/reconcile_loop6.py` against the local FYP `results/passF/benchmark_matrix_passF.csv` and `results/exp3_cohirf_benchmark.csv`. It did not fit clusterers. The 3,000 rows form 13 × 12 = 156 complete dataset-method cells, with no duplicate dataset-method-seed keys and expected 30 rows in six high-dimensional cohorts / 10 rows in seven other datasets. All 3,000 records are saved scores; no fit-event provenance is attached.

From the per-row ARIs, cell means, dataset-wise average ranks (higher ARI ranks better), and Friedman test were recomputed: χ²=11.556213, df=11, p=0.397908; ICC-v2 mean rank=5.615385. This reproduces the saved-score statistic, not independent model execution or a confirmatory comparison. A non-significant omnibus result does not establish equivalence or superiority.

## Provenance and fairness limits

- Pass F matrix SHA-256: `4f5659c93393054d5fdaa6eb82895e167aa784b214b3f849a35a591696da2b8c`; CoHiRF CSV SHA-256: `559040232a29e03c148da0cddebe6249bebed6c52e3b21f5dd425859100716da`. Row-level assessments are in `row_provenance.csv` and exact schedules in `seed_schedule_audit.csv`.
- High-D Ward rows for seeds 10–29 repeat seed-0 metrics; ICC-v2 high-D score rows seeds 10–29 were imported from Pass E, per the Loop 5.9 merge/source inspection. Thus rows are not all independent fits.
- `scripts/run_phase3_experiments.py` declares CoHiRF seeds 0–29 (six high-D cohorts) and 0–9 (other seven) and matches the saved CoHiRF CSV schedule. A separate `experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py` declares `[42, 101, 202, 303, 404, 505, 606, 707, 808, 909]`; the historical outputs belong to different pipeline generations and are not a common seed-paired benchmark.
- Reference class count supplies K; the saved full-data ARIs are transductive and label-informed in model specification.
- Compute budgets vary substantially: single-fit methods vs 25-base-partition consensus methods vs neural DEC. ICC-v2's base engine varies for small N. FastMVC implementation explicitly calls itself a surrogate rather than a faithful literature implementation.
- The saved Pass F CSV has no fit status field. Its exact zeros cannot be identified as failed fits from that file; 42 Core-Halo zero ARI/NMI records need resolution using contemporaneous logs. DEC code paths convert some exceptions to zero scores, so zero metrics are ambiguous.

## Decision

Report this only as a separate descriptive comparison of the saved score matrix, if retained at all. Do not call 3,000 independent fits, do not claim matched-seed inference, and do not infer ICC superiority, robustness or generalization. The six-cohort stability analysis remains separate. Baseline fidelity, copied/imported values, seed differences, supplied K and missing failure status prevent a fair confirmatory ranking.

## Files and reproducibility

`reconcile_loop6.py` writes `row_provenance.csv`, `seed_schedule_audit.csv`, `method_fidelity_matrix.csv`, `failure_status_audit.csv`, `recalculated_benchmark.csv`, and `recalculation.json`. Required local inputs are above; source paths and dynamic input hashes are in JSON. Environment: current project Python with SciPy installed. The script exit code was 0. No new baseline fits were executed.
