# Independent adjudicator review — Loop 6.0

## Scope and independent checks

I independently reviewed the candidate manuscript and key Loop 5.9/6.0 statistics, provenance, duplicate, benchmark and clean-clone artifacts. I inspected:

- `audit/loop6_0/manuscript/candidate/main.tex`, generated aggregate tables/macros, `aggregate_results.json`, `validate_candidate.py`, and the LaTeX build report.
- `audit/loop6_0/statistics/reconstructed_72_cells.csv`, `posthoc_selection_audit.csv`, `selection_threshold_sensitivity.csv`, `cohort_sensitivity.csv`, `bootstrap_reanalysis.csv`, `statistical_methods_note.md`, and `reproduction_checks.json`.
- `audit/loop6_0/provenance/historical_provenance_verdict.md`, `duplicate_reconciliation.csv`, and Loop 5.9 duplicate/provenance records.
- `audit/loop6_0/benchmark/benchmark_verdict.md`, `recalculation.json`, `method_fidelity_matrix.csv`, and benchmark source CSVs in `D:\Final Year Project`.
- `audit/loop6_0/release/clean_clone_test.md`, `data_rights_matrix.csv`, and the release README review.

I independently ran a read-only Python calculation over the six local `D:\Final Year Project\data\cache\*.npz` label arrays, all 4,320 real/null partition NPYs, 4,320 Parquet rows, and `results/stability/subsample_stability_summary.csv`. I recomputed real and null intersection ARIs and external ARIs. Counts: 72 cells; no missing partition/record files, malformed records, failed statuses, or split mismatches. Maximum per-cell difference from saved aggregates: stability `1.1102230246251565e-16`, ARI `9.71445146547012e-17`; recomputed means were stability `0.5165860620823639`, external ARI `0.052312182172289196`, gap `0.46427387991007457`, median gap `0.44840681694162077`, null stability `0.00661968076299296`. This is saved-output reconstruction, not a fresh fit or historical execution authentication.

I also independently concatenated `results/passF/benchmark_matrix_passF.csv` and `results/exp3_cohirf_benchmark.csv`, recomputing the 13×12 dataset-method mean ARI matrix and Friedman test: 3,000 score rows, no duplicate dataset-method-seed keys, complete matrix, `Q=11.556213017751475`, `df=11`, `p=0.3979076148432822`. This supports arithmetic over stored scores, not 3,000 authenticated independent fits.

I did not rerun the clustering algorithms, the full bootstrap matrix, the benchmark reconciler, the clean-clone process, or the LaTeX build. I did not re-fetch upstream datasets or establish licensing rights. The bootstrap and sensitivity outputs were inspected but not regenerated in this independent review.

## Adjudication

The bounded six-cohort descriptive result is arithmetically sound on the recovered local partitions and reference labels. The candidate appropriately avoids treating 72 cells or 435 pairwise comparisons as independent observations and does not claim that the gap is a universal scale. It also appropriately states that label-informed sampling/K and unauthenticated historical producer constrain interpretation. The principal scientific observation survives as a conditional saved-output reconstruction; authenticity of historical fits and external reproducibility do not.

The candidate is not yet a submission-ready manuscript. Its own build report says it is a standalone `article` document, not a Springer `sn-jnl` source, and the required `pdflatex` build was unavailable. It is a defensible content replacement draft, not a validated submission artifact.

## Objections by severity

| Severity | Objection | Independent assessment |
|---|---|---|
| **Fatal to fit-authenticity claims** | No recovered producer/writer trace or contemporaneous execution logs bind the saved partitions to actual declared model calls. | Do not say the historical fits have been independently authenticated. The numerical reconstruction establishes internal consistency only. |
| **Major** | Public Tier 2 reproduction is absent; run-level partitions and records are not in the clean public clone. | Keep data/code claims scoped to aggregate arithmetic or publish a lawful, complete evidence package. |
| **Major** | Recovered partitions include exact duplicate assignments across some method/mode cells, including a real/null pair. | Duplicate bytes are verified; cause is not. The existing review correctly preserves `CANNOT_CLASSIFY`. Do not treat `status=success`/runtime as proof of independent calls. Explain or prospectively eliminate with immutable output lineage. |
| **Major** | Reference labels determine both stratified draw composition and requested K. | This is not fully label-blind validation. State this prominently and avoid framing labels as complete biological ground truth. |
| **Major** | Six convenience cohorts and shared methods/repeats limit inference. | Descriptive and exploratory claims only. A bootstrap over six cohorts is not confirmatory population inference; the candidate reasonably omits the CI headline. |
| **Major** | Exact 13-dataset benchmark files exist locally and reproduce the 3,000-row/12-method Friedman arithmetic, but records have mixed seed schedules, imported/copied rows, fidelity/budget differences and missing statuses. | Retain only a separate descriptive saved-score benchmark, if necessary. Do not call these 3,000 authenticated independent fits, or use `p≈.40` to claim equality/superiority. |
| **Moderate** | Candidate says equal cell weighting is “not equal cohort weighting” although the design is balanced at 12 methods per each of six cohorts. | Numerically, equal weighting of all 72 cells gives each cohort equal total weight. Clarify that it gives each method-cell equal weight and each cohort equal weight here due to balance; these become distinct with missing cells. |
| **Moderate** | Candidate labels recovered files as “saved subsample partitions” and provides exact protocol, but some protocol details derive from historical documentation rather than an authenticated writer invocation. | Retain with the existing “metadata describe” and unauthenticated-producer language; avoid presenting archived plan as proof of the exact executed code path. |
| **Moderate** | The one-way aggregate package/clean-clone check is not a Tier 2 full reproduction. | Current release report describes this correctly; use “aggregate arithmetic check,” not unqualified “reproducible study.” |
| **Minor** | Bibliography and tables have only targeted validation; candidate is not Springer-formatted and visual PDF review was not possible. | Complete references, template conversion, compilation and visual QA before submission. |

## Claim statuses

- **Verified (arithmetic only):** 72 saved cell summaries; 4,320 partition/fit artifact count; per-repeat ARI and pairwise-intersection ARI recomputation; aggregate mean/median gap; 13×12 Friedman statistic over the saved per-seed score CSVs.
- **Conditional:** saved artifacts correspond to the originally intended inputs and executions; the historical protocol faithfully describes the producer; interpretation of external labels as relevant reference classes.
- **Descriptive/exploratory:** cohort/method heterogeneity, leave-one-cohort-out direction, Rule (i)/(i′)/Rule (iii) subsets, six-cohort bootstrap.
- **Unsupported by these records:** ICC superiority or equivalence, causal effect of high dimensionality in the biomedical cohorts, clinical utility, population-wide generalization, and complete public reproduction.
- **Not resolved:** why identical NPY outputs occur across certain methods/modes; legal permission to redistribute transformed cohort data; a clean Springer build.

## Final reviewer gate

**HOLD for DMKD submission.** The candidate is a materially safer manuscript basis than the canonical broad-claim version, and the central six-cohort contrast is defensible as a bounded descriptive reconstruction. Before submission, the authors need to (1) freeze and template/build a complete manuscript; (2) correct the weighting sentence; (3) retain the historical execution caveat; (4) resolve or explicitly report duplicate assignment groups; (5) keep the 13-dataset saved-score benchmark distinct and non-confirmatory; (6) complete citation/table/figure review; and (7) make a truthful availability statement and provide lawful public evidence sufficient for the claimed reproducibility tier. A prospective traceable study would be needed to upgrade historical fit authenticity, but it cannot retroactively authenticate the existing local files.
