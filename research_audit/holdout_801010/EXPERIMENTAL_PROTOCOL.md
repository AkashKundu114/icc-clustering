# ICC 80/10/10 Inductive + Transductive Experimental Protocol

Protocol ID: ICC-HOLDOUT-801010-v1.0  
Status: prespecified design; no empirical results implied.

## 1. Objective and estimands

Evaluate two different capabilities of ICC/GAC on each approved biological cohort:

- **Track A — inductive generalization (primary):** fit on training samples only and assign validation/test samples using a fixed, training-derived out-of-sample rule.
- **Track B — transductive structure recovery (secondary):** after choices are frozen using train/validation, cluster the complete unlabeled cohort jointly and score only the pre-designated test subset. Test feature vectors are visible to clustering; test labels remain sealed.

Never pool these tracks or describe Track B as unseen-sample prediction. Optionally retain a conventional full-cohort clustering as a descriptive reference, not as a holdout score.

## 2. Split design

For every cohort, generate repeated group-aware 80/10/10 partitions: 80% train, 10% validation, 10% test. Target 30 prespecified seeds, with identical split manifests across methods. Split at patient/donor level whenever possible; keep paired specimens, aliquots, repeated timepoints and technical replicates from one patient in one partition. Record actual sample and group proportions after integer/group constraints.

Optional external-label stratification is permitted solely to construct balanced split manifests. Labels must never enter model-facing APIs, preprocessing, fitting, feature selection, K selection, validation selection, assignment or stopping. If stratification is used, record it and run a label-blind group-random sensitivity analysis. Never violate patient grouping to obtain exact percentages.

For small cohorts, a 10% test set may be too small for reliable ARI/NMI. Always report test size, group count and class counts. Mark low-information/non-estimable metrics explicitly; do not turn them into zero or drop rare classes. Add repeated group-aware 5-fold evaluation as a separate sensitivity analysis where feasible. Split seeds are not independent biological replicates.

## 3. Track A: inductive protocol (primary)

1. Split X and metadata into train/validation/test using a frozen manifest.
2. Fit imputation, scaling, variance filtering, feature ranking, BGSS, dimensionality reduction, feature selection, anchor construction, graph/consensus state and ICC only on X_train.
3. Apply frozen transforms and model state to X_validation. Select hyperparameters only with prespecified label-free criteria (e.g. stability, consensus/PAC diagnostics, internal scores, coverage and predeclared degeneracy constraints).
4. Freeze the complete pipeline, K policy, feature set, assignment rule, confidence threshold, random-seed policy and tie-break rules.
5. Predict X_test without refitting, recalculating BGSS, rebuilding anchors, using query-set statistics or jointly reclustering test samples.
6. Persist/fingerprint predictions and fitted state before opening y_test. Then compute external test metrics.

The estimator must have a mathematically valid out-of-sample rule learned from training data. If `predict` uses test/query distribution, updates the model, reconstructs anchors/graph, or refits anything, it is not inductive. Mark that method `inductive_unsupported` unless a principled, tested extension is implemented. Do not invent centroid assignment for methods whose objective does not define it.

Audit ICC's documented closed-form prediction claim against source code, especially stored BGSS features, preprocessing state, anchors/prototypes, confidence/rejection and mutation during predict. Tests must prove prediction does not change fitted parameters; individual predictions are invariant to query order/batching; test samples cannot alter the fitted model; and all learned transforms use training data only.

## 4. Track B: transductive protocol (secondary)

1. Generate the same split manifest and seal test labels.
2. Use train/validation only for development and label-free selection; freeze algorithm family, hyperparameter search space, K policy, preprocessing, stopping and tie-break rules.
3. Run the final unsupervised clustering on X_all = X_train + X_validation + X_test. Test feature vectors are intentionally visible to the algorithm; no labels are.
4. Extract the assignments for the pre-designated test indices and only then score against y_test.

Name this endpoint `transductive_test_subset`, never `test prediction` or `out-of-sample accuracy`. Transductive preprocessing may fit unsupervised transforms on all X because the estimand explicitly permits access to all feature vectors. Keep its preprocessing state and results separate from Track A.

## 5. K, tuning and fairness

Report known-K and unknown-K separately. For known-K, use only a pre-registered reference class count sourced from the cohort protocol/original publication; do not infer K from labels during execution. For unknown-K, use a frozen label-free procedure and candidate range. Never select K using ARI/NMI/AMI, labels, class proportions or test scores.

Use a finite, prespecified search grid and deterministic tie-break. Report every tried configuration and failure. Give methods equal validation/search budgets or disclose differences. Classify every baseline as `native_inductive`, `principled_extension`, `transductive_only` or `unsupported`. Preserve all-noise, one-cluster, empty-cluster, abstention, timeout and failure outcomes.

## 6. Metrics

Primary external endpoint: test ARI. Also report AMI, NMI (state averaging convention) and V-measure. Report test assignment coverage, unassigned/abstention fraction, noise fraction, number and size of predicted clusters, singleton fraction, selected feature count, discovered K, runtime, peak memory and status/failure reason.

For abstaining methods, report both conditional metrics on assigned points and coverage; add a predeclared sensitivity that treats noise as a cluster. A metric is null with a reason if it cannot be estimated (e.g. fewer than two reference classes in test), not zero. Report class and group counts with every score.

## 7. Preprocessing and leakage

Inductive: every learned transform is fitted on X_train only and applied unchanged to validation/test. BGSS statistics and selected features are training-only. No supervised DE/marker selection, label-informed ranking, outcome-informed filtering or global scaling before split. Fixed source-provided transformations may be retained only when documented as immutable upstream processing.

Transductive: label-blind unsupervised transformations may be fitted on X_all, explicitly recorded as transductive. Do not reuse Track A fitted state.

No survival, recurrence, response or other clinical outcomes may be used as primary biological cluster truth or as tuning targets. Respect cohort label taxonomy: subtype/lineage labels, tumour-vs-normal, molecular phenotype and inferred labels must be reported in separate strata with circularity assessed.

## 8. Statistical analysis

Summarize repeated splits within each cohort first (prespecify median test ARI as the primary cohort-level summary; also mean, SD, interval, coverage and failure rate). Compare methods with paired split-level differences descriptively, but do not treat split seeds as independent n.

Cross-cohort inference uses independent cohorts as the inferential unit. Report per-cohort paired differences, cohort-level mean/median effects, uncertainty intervals, heterogeneity where defensible, paired nonparametric tests where justified, and Holm correction for prespecified multiple comparisons. Account for overlapping/derivative cohorts; preserve disease and assay strata. With few cohorts, emphasize descriptive evidence and uncertainty. Analyze Track A and B separately; Track A is primary and Track B secondary.

## 9. Reproducible artifacts

Use a dedicated namespace such as `experiments/exp10_holdout_801010/` (adapt to existing conventions without duplicating infrastructure). Include:
- versioned YAML config and protocol/config SHA-256;
- deterministic split manifests with sample/group IDs and manifest hashes;
- method capability registry;
- separate inductive and transductive runners;
- preprocessing/model fingerprints;
- per-split predictions/partitions, validation search traces and failure logs;
- raw result table, cohort summaries, cohort-level paired effects, statistical report, figures and deviation log;
- tests for split disjointness, group integrity, deterministic replay, no leakage, inductive immutability/query invariance, transductive semantics and metric edge cases.

Every result row should include protocol/track/cohort/method/capability, split seed and hash, partition sizes/groups, test class counts, preprocessing fingerprint, selected feature count, requested/discovered K, validation criterion, test metrics/coverage/noise, runtime/memory, status/failure reason, git commit, config hash and data checksum.

Do not commit raw biological matrices. Do not overwrite Pass F, canonical result stores, manuscript tables or main branch.

## 10. Staged execution and acceptance

Stage 0: repository/API reconnaissance. Stage 1: freeze protocol/config and hashes. Stage 2: synthetic leakage and contract tests. Stage 3: one-cohort engineering pilot (not confirmatory). Stage 4: full approved cohort/method runs. Stage 5: freeze predictions before test-label scoring. Stage 6: statistical analysis. Stage 7: independent red-team audit.

Ready for confirmatory execution only if splits are valid/group-aware, preprocessing is leakage-free, ICC's inductive contract is proven or explicitly unsupported, Track A/B are separate, test labels are isolated until scoring, all methods/failures/coverage are reported, cohort-level inference avoids pseudoreplication, tests pass and red-team review has no unresolved critical/high findings.

Interpretation: strong Track B with weak Track A indicates transductive structure but weak unseen-sample assignment. High conditional ARI with low coverage is not an unqualified win. Stability is not biological validity. No performance claim is authorized by this protocol alone.
