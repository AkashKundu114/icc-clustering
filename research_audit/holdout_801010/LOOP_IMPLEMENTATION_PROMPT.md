# Loop Mission: Implement ICC 80/10/10 Inductive + Transductive Evaluation

Repository: `AkashKundu114/icc-clustering`  
Branch: `research/holdout-801010`  
Read first: `research_audit/holdout_801010/EXPERIMENTAL_PROTOCOL.md`.

## Mission

Implement the protocol as a reproducible experiment suite, not merely documentation. Track A (inductive) is the primary generalization endpoint; Track B (transductive) is secondary and must remain analytically separate. Add tests, run a synthetic validation suite and a one-cohort engineering pilot, and run the full suite if feasible. Report accurately what did and did not execute. Do not claim empirical improvement unless locked results support it.

## Non-negotiable safeguards

- Do not modify main branch, historical Pass F results, canonical result stores or manuscript tables.
- Do not change ICC/GAC's scientific definition to make this easier.
- Track A: fit all learned preprocessing and clustering state on X_train only. Validation/test are transform/predict only. Test features cannot influence BGSS, feature selection, anchors, graph, centroids, model selection or stopping.
- Track B: final unsupervised clustering may see X_all by definition, but never y_all. Label it transductive, not prediction/generalization.
- No external labels/ARI/NMI/AMI for feature selection, K, hyperparameter tuning, thresholds, seed selection or stopping.
- Split at patient/donor/group level. Keep paired/repeated specimens together. Never break groups to hit exact percentages.
- Split seeds are not independent biological replicates.
- Preserve failed, all-noise, one-cluster, low-coverage, unsupported and timed-out methods.
- No raw biological matrices in Git. No result-store overwrite.
- Any protocol deviation must be logged with rationale, impact and sensitivity analysis.

## Required subagents (parallelize where possible)

### Agent 1 — Repository/API reconnaissance
Inspect actual source, not just README claims:
- `src/icc/`, estimator classes, `fit`, `fit_predict`, `predict`, BGSS, preprocessing, anchors/prototypes and confidence/rejection;
- `src/icc/datasets/`, `data/registry.yaml`, dataset loaders/checksums;
- baseline configs/adapters, existing experiment framework and output conventions;
- tests and `examples/leukemia_inductive.py`.
Verify the documented closed-form inductive inference claim against implementation. Write `research_audit/holdout_801010/REPOSITORY_AUDIT.md` with exact paths, functions, findings, risks and integration plan. Do not assume a source path or API.

### Agent 2 — Split manifests
Implement deterministic 80/10/10 manifests, target 30 seeds per cohort, patient/group-aware. Use stable seed derivation (not Python's process-randomized `hash()`). Prove disjointness, group integrity and replay. Optional label stratification is only for split construction; log it and implement label-blind split sensitivity. Keep labels out of the model pipeline. Record actual proportions, sample/group counts, class counts in evaluation-only metadata, manifest checksum and infeasible cases.

### Agent 3 — Inductive runner and leakage audit
Implement train-only preprocessing and a genuine out-of-sample Track A adapter. Validate that ICC `predict` does not refit, recompute BGSS, rebuild anchors/graphs, update fitted state or use query-set statistics. Add tests for fitted-state immutability, prediction order/batch invariance, test-feature isolation and training-only transform state. If ICC's current method is not truly inductive, mark it unsupported; only add a principled extension if mathematically justified and tested. Never fake `predict`.

### Agent 4 — Transductive runner
Implement a distinct Track B final fit on X_all after model choices are frozen using train/validation only. It may fit unsupervised transforms on all X. Test labels must never enter fitting, K choice or stopping. Extract and score the predesignated test indices only after the partition is frozen. Use endpoint name `transductive_test_subset`.

### Agent 5 — Baselines and fairness
Inventory the current baseline list and determine true capabilities. Mark each `native_inductive`, `principled_extension`, `transductive_only` or `unsupported`. Do not invent out-of-sample assignment for graph/density methods. Match split manifests, K policy, validation search budget and test samples; document method-specific preprocessing. Preserve all failures and coverage.

### Agent 6 — Metrics/statistics
Implement test ARI (primary), AMI, NMI, V-measure, coverage, abstention/noise, cluster counts/size distribution, runtime and memory where available. Non-estimable metrics are null with reason, not zero. Summarize repeated splits within cohort first; perform inference across independent cohorts, not seeds. Implement paired cohort-level effects, uncertainty, heterogeneity where defensible and Holm correction for prespecified comparisons. Keep tracks separate.

### Agent 7 — Tests/reproducibility/reporting
Add config/protocol hashing, software/commit capture, split and data checksums, prediction artifacts, validation traces, failures, summaries, figures and deviation log. Add CLI and README. Run focused tests, full tests if feasible, reproduction smoke checks and one-cohort pilot. State clearly if full biological execution was not performed.

### Agent 8 — Independent red-team reviewer
Do not implement. Review final diff and outputs for leakage, patient leakage, label leakage through K/stratification/validation, invalid inductive assignment, transductive mislabeling, baseline unfairness, coverage/failure omissions, pseudoreplication and unsupported biological claims. Write `research_audit/holdout_801010/RED_TEAM_AUDIT.md` with PASS/FAIL/NOT TESTED and severity-ranked findings. Lead agent must fix critical/high findings or mark NOT READY.

## Implementation sequence

1. Read protocol and audit repository.
2. Write an implementation plan before changing core code.
3. Freeze YAML config and protocol/config hashes.
4. Implement split manifests and synthetic tests.
5. Implement separate Track A and Track B runners.
6. Audit ICC inductive API and every baseline capability.
7. Run synthetic leakage tests and focused tests.
8. Run one-cohort engineering pilot without selecting on external labels.
9. Run full approved cohort/method suite if resources permit.
10. Freeze predictions/partitions before test-label scoring.
11. Produce cohort summaries and statistical analysis.
12. Run independent red-team audit and report deviations.

## Required implementation architecture

Follow repository conventions if an equivalent framework exists; do not duplicate infrastructure. Use a dedicated experiment namespace, preferably `experiments/exp10_holdout_801010/`, with config, CLI, split utilities, preprocessing/adapters, separate track runners, metrics/statistics, tests, manifests and results.

Make leakage hard to express through API boundaries. Track A should conceptually expose:
- `fit_inductive(X_train, config, seed)`
- `select_on_validation(fitted_model, X_validation, selection_config)` — no y argument
- `predict_inductive(fitted_model, X_test)`
- `score_frozen_predictions(y_test, predictions)`

Track B should conceptually expose:
- `fit_transductive(X_all, config, seed)` — no y argument
- `extract_test_partition(full_partition, test_indices)`
- `score_frozen_predictions(y_test, test_partition)`

If labels are needed for split stratification, isolate that in the split-manifest generator; do not pass labels to model functions. Write prediction/partition artifacts before the scoring process loads test labels.

Validation selection must use prespecified label-free criteria with deterministic tie-breaks. Record the full candidate grid, values and failures. If using AutoK, audit and freeze its internals/candidate range. Never use external scores to select K.

Every result row should contain protocol ID, track, cohort, method/capability, split seed/hash, train/validation/test sizes and group counts, test class counts, preprocessing fingerprint, feature count, requested/discovered K, validation criterion/value, test metrics, coverage/noise, runtime/memory, status/failure, commit SHA, config hash and data checksum.

## Required deliverables

1. `research_audit/holdout_801010/EXPERIMENTAL_PROTOCOL.md` (provided; deviations only by explicit log).
2. `research_audit/holdout_801010/REPOSITORY_AUDIT.md`.
3. `research_audit/holdout_801010/RED_TEAM_AUDIT.md`.
4. Dedicated experiment implementation, config, tests, CLI and README.
5. `research_audit/holdout_801010/IMPLEMENTATION_REPORT.md`.
6. Split manifests, method capability registry, raw result schema, failure/deviation logs and summary artifacts.

## Stop conditions

Stop and report a blocker rather than guessing if patient grouping is unresolved, labels are ambiguous/circular, source terms are unclear, estimator inductive semantics cannot be verified, a baseline lacks a valid assignment extension, requested splits are infeasible, or existing canonical results would be overwritten.

## Definition of done

Implementation-complete only when code, tests and a pilot are complete and reported. Experiment-complete only when all approved cohorts/methods have run, locked scoring/statistics are produced and red-team review has no unresolved critical/high issue. If the full run is infeasible, explicitly report `implementation-complete / full-experiment-pending`.

## Final report

Return branch and commit SHA; files changed; architecture and CLI; exact tests with exit status; pilot cohorts/methods and output paths; whether full execution occurred; inductive capability verdict for ICC and each baseline; red-team findings; deviations/blockers; and exactly what claims are scientifically supported. Never claim improvement merely because the pipeline ran.
