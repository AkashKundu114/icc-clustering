# Loop 6.0 final report — DMKD submission candidate

## 1. Executive summary

**Verdict: HOLD.** The central six-cohort observation survives as a numerically reproducible descriptive reconstruction from locally recovered saved partitions. It is not authenticated as a historical set of independent model executions, and it is not publicly reproducible at partition level. The revised evidence-bounded candidate is materially safer than the canonical broad-claim manuscript, but it is not a validated Springer submission: the canonical source remains unchanged, the candidate is standalone `article` class, TeX is unavailable, broad manuscript claims remain unaudited, and dataset/derived-data redistribution rights are unresolved.

## 2. Baseline and manuscript identity

- Repository: branch `main`, baseline commit `5dac3762f34b756a1047e099b4465c8a1954daad`, timestamp `2026-11-02T18:16:35+05:30`; fetched `origin/main` matched. No submodules. The tracked tree was clean before Loop 6.0 began.
- Exact canonical local candidate: `paper/manuscript/main.tex`, SHA-256 `A0C4274EC5DFBB40311D3D33D7AD8179B17DEE145851FD2E5B255E498054E75F`, verified before changes. It is ignored/untracked and therefore not in the public commit. It remains unchanged at the same hash.
- Separate FYP checkout: `D:\Final Year Project`, branch `research/dami-revision`, HEAD `60b163f22b5931da35a1ace07d1934bf3bdd65e3`, clean working tree. The recovered outputs and caches are ignored/untracked; FYP HEAD does not authenticate their creation.
- Frozen pre-change inventory dynamically hashed 12,096 files across target local data/results/paper, Loop 5.9, and FYP stability/data/paper. See `baseline/`.

## 3. Work completed by each agent

| Role | Concrete work | Independent check / limit |
|---|---|---|
| A — manuscript remediation | Evidence-bounded Markdown and LaTeX candidate, claim matrix, change log, abstract comparison, related-work review, reviewer matrix, generated tables | Lead reran static validation and table generation; F flagged and lead corrected equal-weight wording. No TeX/PDF build. |
| B — statistics | Independent reconstruction script, 72-cell outputs, bootstrap/subset/cohort sensitivity and methods note | Lead reran script; Agent F separately recomputed aggregates. No fresh model fits. |
| C — provenance/prospective | Direct reload of three duplicate pairs; 291-row/140-group duplicate inventory; trace schema, validator and prospective protocol | Four synthetic validator tests passed; no biomedical pilot or historical producer recovered. |
| D — benchmark | Row provenance, seed schedule, fidelity/failure matrices, recalculated score matrix and benchmark verdict | Lead reran script; F separately recalculated Friedman from saved rows. No baseline fits. |
| E — reproducibility/rights | Fresh-clone Tier 1 test, tier matrix, rights matrix, release README/manifest | Tier 2 unavailable and Tier 3 not run; no data released. |
| F — independent adjudication | Independent full saved-output reconstruction and benchmark calculation; adversarial findings | Did not rerun models, bootstrap suite, clean clone or LaTeX compilation. |

## 4. Manuscript changes

A conservative candidate is packaged at `DMKD_submission_candidate_loop6_0/` and source files at `manuscript/candidate/`. It narrows the contribution to the six-cohort saved-output reconstruction; distinguishes pairwise resampling agreement from reference-label ARI; discloses label-informed sampling and reference-derived K; removes the mismatched primary bootstrap interval; labels the nine-cell subset post-hoc; separates the 13-dataset score benchmark; and omits unaudited GAC/ablation, causal, theoretical, clinical, Prostate-mechanism, and scalability claims. Omitting these claims is not a finding that they are false.

The canonical `paper/manuscript/main.tex` was not edited. The candidate is a standalone `article`-class draft, not yet in Springer `sn-jnl` form. Static validation and dynamically generated results tables pass; the `pdflatex` attempt failed because TeX is unavailable, and no PDF or visual check exists. A verified weighting correction states that the mean of the 72 cells is also equally weighted by cohort because each cohort has 12 cells; the median remains over 72 cell differences.

## 5. Six-cohort reconstruction

The lead reran `statistics/reconstruct_loop6.py`; Agent B authored the independent reconstruction, and Agent F performed a separate direct reconstruction. All calculated from the local FYP cache NPZs, 4,320 partition NPYs, 4,320 one-row Parquet records, and saved summary CSV.

- 72 cohort-method cells; 12 methods; 30 real and 30 null partitions per cell.
- 2,160 real external-ARI observations; 31,320 real and 31,320 null pairwise intersection ARIs.
- No missing partition/record keys, malformed records, failed statuses or split mismatches in the checked local files.
- Mean stability `0.5165860621`; mean external ARI `0.0523121822`; mean cell-wise stability-minus-ARI `0.4642738799`; median cell difference `0.4484068169`; mean null stability `0.0066196808`.
- Maximum per-cell discrepancy from saved aggregate: stability `1.11e-16`; external ARI `9.71e-17`; null `9.92e-17`.

**Meaning:** stability is the mean ARI across 435 unordered pairs, restricted to shared sample indices. External alignment is the mean ARI over 30 partition-to-reference comparisons. These are related at cohort-method-protocol level, not one-to-one paired observations. Pair scores reuse partitions and samples. Fixed model seed 0 assesses the stored subsampling schedule at one initialization setting, not initialization robustness. Reference labels informed stratified sampling and requested K. The gap is only the arithmetic difference of two averages over different comparison populations, not a calibrated universal metric.

## 6. Statistical corrections

Rule(i) selects 20 cells; Rule(i-prime) selects 18; recurrence Rule(iii) selects nine. They are distinct populations; the “three recurring methods × all six cohorts” 18-cell set is not Rule(i-prime). The nine-cell mean gap `0.686617` is post-hoc and selection-conditioned, not independent confirmation. Threshold sensitivity is in `statistics/selection_threshold_sensitivity.csv`.

Leave-one-cohort-out mean gap remains positive but ranges from `0.398341` when Prostate is omitted to `0.497300` when Leukemia is omitted; Prostate has the largest cohort mean gap (`0.793939`). This supports direction consistency over this small set, while showing material magnitude heterogeneity; it is not generalization evidence.

The equal-cell point estimate `0.485376` differs from equal-cohort estimate `0.499925`. Historical/bootstrap intervals are seed/order sensitive and do not support population inference from six convenience cohorts. The candidate removes the inferential interval. The 435 pairwise scores are never treated as independent observations.

## 7. Historical provenance verdict

**UNVERIFIED.** The recovered bytes form an internally consistent grid, but no original partition writer, contemporaneous process logs, execution commit, source/input/cache linkage, stable sample-ID mapping or invocation-output chain was found. The local files are untracked in the separate FYP checkout. Saved status/runtime metadata cannot authenticate model calls. A future prospective experiment cannot retroactively authenticate these files.

## 8. Prospective experiment status

A versioned protocol, execution trace schema, validator, and synthetic integrity tests are present under `provenance/`. Four unit tests passed, including synthetic valid partition, duplicate run-ID rejection, hash-mismatch rejection and empty-manifest validation. The prospective manifest is explicitly `NOT_RUN` with zero empirical fits. The unauthenticated saved runtimes sum to about 17,056 seconds (4.74 serial hours) but do not predict a future run. Missing null-generation lineage, sample-ID provenance and data rights mean even a one-method pilot would not resolve the historical comparability question; no biomedical pilot was run.

## 9. Duplicate partition findings

The 140 identical-hash groups (291 files) were preserved and re-inventoried. All are `CANNOT_CLASSIFY`; identical bytes do not establish identical invocations or benign degeneracy. The three priority pairs have equal ordered sample indices and assignments: CNS CoHiRF real/null repeat 17 (47/1 sizes), Prostate CoHiRF-null/CoreHalo-real repeat 5 (K=1), and Prostate StdCons-null/UngatedAC-real repeat 16 (80/1). The third nontrivial sparse cross-method/mode match remains unexplained. The duplicates are across cells, not repeated files inside the same cell, so do not automatically duplicate a within-cell pairwise comparison; they still weaken provenance confidence.

## 10. Benchmark fairness and corrected results

The separate 13-dataset external-ARI benchmark has 3,000 saved score rows, 13 datasets, 12 methods, 156 complete dataset-method cells and no duplicate dataset-method-seed keys. Recalculation gives Friedman `Q=11.556213`, `df=11`, `p=0.397908`; ICC-v2 mean rank `5.615385` (rank 4/12). These are saved-score calculations, not 3,000 authenticated model fits. High-dimensional Ward seed rows are copied from seed 0; ICC-v2 rows are imported from Pass E; schedules differ; K is reference-derived; budgets and engine choices differ; FastMVC is a surrogate; zero score records lack sufficient failure status. No superiority, equivalence, robustness or generalization claim is supported. This benchmark remains distinct from the six-cohort stability experiment.

## 11. Novelty and related work

A targeted literature check found direct prior work comparing stability with ground-truth recovery (Amorim & Cardoso, 2015), cluster-wise stability cautions (Hennig, 2007), and later reviews/frameworks. The broad “not previously quantified” claim is not defensible. The candidate narrows its contribution to a descriptive reconstruction under these six cohorts/protocol; novelty for that narrow scope remains conditional because no systematic literature review was conducted.

## 12. Data rights and reproducibility tiers

The exact clean clone of baseline commit `5dac3762f34b756a1047e099b4465c8a1954daad` passed Tier 1 aggregate arithmetic using Python 3.14.6; output hash `538f5e9ce1026689eebef5fb8a79126e82c946be269c6a82afd03a4a45cfa9a5`. Tier 2 is unavailable because partitions, run records and caches are absent. Tier 3 was not run. No data package was created. Most raw and derived-data terms are unresolved; Yale B cannot be redistributed without permission. The rights matrix is research documentation, not legal clearance.

## 13. Independent reviewer objections

The independent review calls for: authentication caveat; public Tier 2 reproduction or precise limitation; explanation or disclosure of duplicates; prominent label-informed-design qualification; small-cohort/descriptive inference; distinct and qualified benchmark; fuller references; Springer build and visual review; and full claim-to-evidence audit for retained results. See `reviewer/major_objections.csv` and `reviewer/independent_adjudicator_review.md`. One weighting objection was corrected after review; the matrix records the pre-correction observation.

## 14. Unresolved blockers

See `reconciliation/unresolved_blockers.csv`. Material blockers are: canonical manuscript remains ignored/untracked; historical producer/execution unauthenticated; duplicates unexplained; public Tier 2 unavailable; most data rights uncleared; candidate not in Springer format/compiled; broad current-source claims remain unaudited; and full manuscript figures/tables/references are not validated.

## 15. Exact changed files

Only new files under `audit/loop6_0/` were created or changed. No production code, tests, manuscript source at `paper/manuscript/main.tex`, bibliography, historical data/results, FYP files, or Git history were modified. No data were bundled and no commit or release was made. Complete paths and hashes are in the final dynamic manifest/checksum files.

## 16. Test and compilation results

- `python audit/loop6_0/statistics/reconstruct_loop6.py`: exit 0; full saved-output reconstruction; no model fitting.
- `python audit/loop6_0/benchmark/reconcile_loop6.py`: exit 0; saved-score rows only.
- `python -m unittest discover -s audit/loop6_0/provenance/tests -v`: 4 tests passed; synthetic validation only.
- `python audit/loop6_0/manuscript/candidate/validate_candidate.py`: PASS static structure, citations, inputs and aggregate linkage.
- `python audit/loop6_0/manuscript/candidate/build_candidate_tables.py`: 72 cells/6 cohorts/12 methods regenerated.
- Clean-clone Tier 1 command: exit 0. Tier 2 unavailable; Tier 3 not run.
- `pdflatex`: unavailable; no compilation or PDF visual QA.

## 17. Final submission verdict

**HOLD.** Scientific contribution is potentially defensible as a narrow descriptive reconstruction, but only after the manuscript is frozen and built in Springer format, claims beyond audited evidence are removed or verified, data availability is corrected, and reproduction/provenance limitations are transparent. The public package does not reproduce the primary result from raw partition evidence.

## 18. Next required actions, ordered by priority

1. Author-confirm and freeze the exact revised submission manuscript; convert the evidence-bounded candidate to Springer `sn-jnl`, compile in a clean TeX environment, and visually inspect PDF/tables/references.
2. Remove or separately audit every retained ablation, synthetic, theory, runtime/scaling, Prostate mechanism, superiority, clinical and generalization claim in the current canonical version.
3. Decide whether to accept a saved-output descriptive paper with explicit unauthenticated provenance, or conduct a new fully logged six-cohort experiment with lawful inputs and a prespecified protocol.
4. Resolve or explicitly disclose all duplicate groups; do not modify the historical artifacts.
5. Complete upstream-specific data and derived-artifact rights checks; then publish/test a rights-cleared Tier 2 package or give an exact access pathway.
6. Finish a documented related-work review and verify all citations against DMKD style.
7. Reassess submission only after all included tables, figures, scripts and claims are version-matched and evidence-linked.

### Would I submit this exact manuscript today?

**No.** The canonical source still contains broad claims not validated in this loop, the submission candidate is not yet in the journal template and has not compiled, and reviewers cannot reproduce the central result from the public clone. The six-cohort numerical contrast survives saved-output reconstruction, but that alone is not enough for submission readiness.
