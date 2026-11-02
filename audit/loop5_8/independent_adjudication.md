# Independent adjudication of Loop 5.8 evidence

## Scope and independence

I reviewed the completed duplicate, bootstrap, benchmark, reproducibility and rights deliverables as a separate adjudicator. I did not execute their analysis scripts or recompute their numerical results. I checked whether their stated conclusions agree with each other and with the cited evidence. I inspected:

- `duplicate_partition_forensics.md`, `duplicate_partition_code_trace.md`, `duplicate_partition_inventory.csv`, `named_duplicate_comparisons.json`.
- `bootstrap_estimand_audit.md`, `bootstrap_estimand_comparison.csv`, `bootstrap_seed_sensitivity.csv`, `bootstrap_recalculation.json`, `scripts/bootstrap_estimand.py`.
- `benchmark_seed_reconciliation.md`, `benchmark_seed_schedule.csv`, `benchmark_configuration_provenance.csv`.
- `reproducibility_release_plan.md`, `data_rights_matrix.csv`, `artifact_manifest.csv`.

The manuscript review was not yet present at the time of this adjudication; the current target repository does not track the manuscript path named in prior loops. Thus this is an evidence-audit adjudication, not a fresh manuscript line-by-line review. No model fits were run.

## Findings

### Duplicate partitions

The report makes the right distinction between byte identity and generator provenance. If its stated census is accurate, exact duplicate bytes across methods/modes do not duplicate a repeat pair inside any single cohort-method-mode cell, because no same-cell repeated-repeat digest group was found. That means there is no direct arithmetic reason to subtract those cross-cell copies from the 435-pair within-cell calculation. It does not establish that experiment labels or method outputs were generated independently.

The two collapsed outputs offer plausible algorithmic explanations (especially K=1), but equality of `.npy` bytes plus a successful metadata row is insufficient to distinguish a legitimate fit from result reuse. The sparse Prostate StdCons/UngatedAC equality remains especially unexplained. The absence of the partition-writing script is the central provenance issue; “successful” Parquet status cannot authenticate the output.

**Adjudication:** duplicate census and named payload equality are conditionally verified by the investigator's direct byte/load audit; actual generation path is unverified. No corruption claim is justified, and no “expected algorithmic behavior” claim is justified for the sparse match.

### Bootstrap estimand — blocking internal contradiction

The bootstrap report’s prose does not match its machine-readable results or its script. `bootstrap_estimand_comparison.csv` and `bootstrap_recalculation.json` report fresh seed-42 E1 cell-weighted ratio interval `[0.37712136998, 0.64498453772]` and E2 equal-cohort interval `[0.37858116697, 0.66171594417]`. The prose instead states E1 `[0.378037, 0.644776]` and E2 `[0.378581, 0.653002]`. The first is not the seed-42 interval in the accompanying CSV/JSON; the second is the historical sequential-RNG interval, not the fresh E2 seed-42 interval. The script's hard-coded report text contains those stale values while its output-writing code computes the correct CSV/JSON values. A reader cannot safely know which interval the report endorses until this is corrected.

The substantive recommendation—remove the inferential interval from the primary manuscript—is sound. The six selected cohorts are not shown to be a random/exchangeable draw, and the bootstrap resamples only six cohort-level aggregates; it does not propagate uncertainty in the 30 ARIs or 435 dependent pairwise ARIs. The manuscript’s point/interval mismatch is real: cell-weighted point 0.485376 is paired with an equal-cohort bootstrap interval. Even a corrected ratio bootstrap does not by itself provide confirmatory population inference.

One label also needs care: “E3” is described as a cohort-clustered bootstrap method but the CSV uses the historical equal-cohort interval alongside an E1 cell-weighted point. A cluster bootstrap is a resampling design, not a distinct estimand; name the target statistic and bootstrap distribution separately.

**Adjudication:** point estimates are descriptive; exact intervals are not audit-ready until the prose is repaired. The primary manuscript should report cohort-specific values and optionally a clearly labelled descriptive six-cohort summary without a population CI.

### Benchmark seed reconciliation

The distinction between observed row schedules and generator provenance is appropriately conservative. Raw rows directly support Pass F seeds 0–29/0–9 and CoHiRF seeds 42–71/42–51. The competing source code (`[42,101,...]`, current 0-based schedule, and historical 42-based schedule) means the saved raw rows do not authenticate their generating configuration. Friedman recalculation from dataset-method means can remain numerically reproducible even if seed schedules differ; it must not be described as matched-seed inference.

The “authoritative” schedule is authoritative only for the saved CSV contents, not for the actual experimental configuration. Manuscript wording should explicitly call these observed saved-row schedules and disclose that Pass F generator lineage remains unresolved.

**Adjudication:** row counts/schedules conditionally verified from saved raw score CSVs; source execution provenance unverified.

### Public reproducibility and data rights

The release plan correctly separates Tier 1 aggregate arithmetic, Tier 2 saved-partition reconstruction, and Tier 3 fresh fitting. These tiers are not interchangeable. A Tier 1 package has now been prepared, but it is a limited package and cannot establish the original repeated experiment. Tier 2 remains local-only; Tier 3 is not demonstrated.

The rights table is conservative, appropriately marking redistribution as uncleared for most datasets. The Yale B caveat bars bundling images into a larger public database absent permission; a source/acquisition instruction is safer. Local presence or upstream public access is not redistribution authorization. The current report does not prove legal clearance for derived caches/partitions, which could retain third-party restrictions.

The clean clone tested by the lead auditor at commit `29bcc279...` confirms the aggregate-only script runs, with exact output values; it does not establish Loop 5.8 release reproduction because the deliverables are uncommitted and the clone lacks source-derived repeated evidence. Label the package Tier 1 only.

**Adjudication:** aggregate-only clean reproduction verified at the current remote commit; public partition/full experiment reproduction contradicted by absent artifacts. Rights status is unresolved for distribution beyond aggregate derived results.

## Disagreements and limitations

1. Bootstrap prose versus CSV/JSON/script differs as listed above. Do not publish the bootstrap report until reconciled and regenerated.
2. Prior Loop 5.7 stated the Pass F schedule was matched by its historical runner; this review found an extant runner with a third schedule that does not generate the saved Pass F output path. The stronger conclusion is unresolved generator provenance, not confirmed matching source lineage.
3. Duplicate outputs are internally consistent with their Parquet metadata, but the lack of a producer script prevents ruling out copy/overwrite. Calling all 140 duplicates “expected deterministic agreement” would exceed the evidence.
4. The target repository has no tracked current manuscript, so exact manuscript corrections cannot be applied to an authenticated submission version. The accessible FYP manuscript is a separate local file and has a different SHA/version from the earlier archived manuscript.
5. I did not inspect the actual source code line-by-line for all original producers or verify licenses against every upstream legal instrument. The specialist reports’ descriptions are accepted conditionally, not as legal opinions.

## Overall independent assessment

The central six-cohort gap survives as **descriptive arithmetic on recovered local partition files**, subject to unauthenticated execution/input lineage. The bootstrap mismatch and now-discovered Loop 5.8 report inconsistency must be corrected before any manuscript uses an interval. Benchmark row schedules can be described as observed but not tied confidently to generator configurations. The nine-cell subset remains post-hoc exploratory. Public reproducibility currently supports aggregate arithmetic only.

**Confidence:** high for identifying the cross-file contradictions; moderate for the reports’ underlying numeric claims because I did not rerun their scripts; low for historical execution authenticity and population inference. This independent review supports a **HOLD** pending report correction, manuscript-version identification, provenance recovery, and rights/release work.

## Addendum — post-reconciliation review

The lead auditor corrected and regenerated the bootstrap outputs after the discrepancy above was reported. I re-opened `bootstrap_estimand_audit.md`, `bootstrap_estimand_comparison.csv`, `bootstrap_recalculation.json`, and `bootstrap_seed_sensitivity.csv`. The previously identified prose/CSV/JSON conflict is **resolved**: fresh seed-42 E1 ratio interval is consistently `[0.377121, 0.644985]`; fresh E2 equal-cohort interval is `[0.378581, 0.661716]`; historical sequential-RNG equal-cohort interval is `[0.381104, 0.653002]`. The manuscript’s `.485376` point and `[.379,.662]` interval remain an estimand mismatch; corrected reporting does not make the six-cohort interval confirmatory.

I also reviewed `clean_clone_reproduction_report.md` and `clean_clone_tier1_output.json`. The current remote `main` clone at `29bcc279589d4a6c1e6747885cc857085ac8d6d0` runs the tracked aggregate arithmetic script and returns 72 rows with the recorded mean/median values. This verifies Tier 1 only. Tier 2 inputs are absent from the clone, Tier 3 was not run, and the Loop 5.8 package itself is not committed as a public release. This evidence strengthens the aggregate-only reproducibility statement but does not change the public reproducibility blocker.

The FYP manuscript remediation report is now available. It correctly emphasizes the version boundary: the target repository has no tracked submission manuscript, while `D:\Final Year Project\paper\main.tex` is a separate candidate draft. It also flags unsupported/unverified confirmatory, causal, clinical, superiority, scaling and biological claims rather than treating the earlier six-cohort reconstruction as evidence for them. I did not independently re-audit every ancillary manuscript result, so those statuses remain conditional/unverified, not adjudicated as false.

**Updated disposition:** the reporting inconsistency in the bootstrap deliverable is fixed. Overall verdict remains **HOLD** because execution provenance, package/public evidence, source manuscript identity, rights and unreviewed high-priority claims remain unresolved.

## Addendum — manuscript claim review

I inspected the now-present `manuscript_remediation_report.md`, `manuscript_claim_evidence_matrix.csv`, `abstract_revised.md`, `data_availability_revised.md`, `code_availability_revised.md`, `remaining_claims_audit_plan.csv`, and `reviewer_objections_updated.md`.

The version boundary is sufficiently prominent: the target checkout at `29bcc279...` lacks a tracked submission manuscript, while the reviewed FYP draft is explicitly identified by local path, separate branch/commit and SHA-256. The reports repeatedly caution that those candidate-draft findings must not be attributed to an unidentified target manuscript. The proposed abstract/data/code statements are explicitly interim and unapplied, which is appropriate.

The claim matrix distinguishes contradicted, conditional, unsupported, contested, and not-audited items. The remaining-claims plan gives priority to confirmatory study identity, baseline comparisons, benchmark provenance, synthetic claims, scaling, Prostate mechanism, biomarkers, theory, clinical implications, novelty, licensing, and figures/tables. The remediation does not present unreviewed claims as disproven; it calls for separate evidence or removal/narrowing. Its proposed abstract accurately confines the verified stability finding to six cohorts, states label-stratified subsampling, identifies dependence, and separates the 13-dataset ARI benchmark.

Two limitations remain. First, the claim matrix's `exact_claim_or_quote` entries are mostly concise claim summaries rather than verbatim manuscript text, and several rows combine multiple locations/claims. It is a strong adjudication index, but not yet a literal exhaustive quotation-level concordance for every sentence, figure, table and supplement. Second, no authenticated submission manuscript is available, so even a complete review of the FYP candidate cannot certify the intended submission package. These limits are transparently stated and do not undermine the focused recommendations, but the matrix should not be represented as a final package-wide line-by-line signoff.

**Final independent disposition remains HOLD.** The narrow six-cohort descriptive result is supported by reconstructed local partitions; original run-to-input provenance and public Tier 2/3 reproduction are missing. The manuscript identity is unresolved, important non-core claims remain unaudited or contested, and dataset redistribution rights are not cleared. Before submission, identify and version the intended manuscript and full package; remove/qualify the mismatched bootstrap and post-hoc subset claims; resolve generator/run provenance and remaining P0 claims; and publish only after clean reproduction and rights review.

## Addendum — expanded manuscript matrix

I re-opened the expanded 81-row `manuscript_claim_evidence_matrix.csv` and the updated remediation report. The matrix now has 21 high-priority adjudication rows and 60 additional section/subsection, caption and generated-table coverage rows. It explicitly marks 62 rows as not audited and distinguishes those coverage entries from claims whose evidence has been reviewed. This resolves my prior concern that the matrix was only a short high-level index: it is now a useful coverage map and accurately avoids implying that the unreviewed rows were validated.

The remaining qualification is scope: coverage rows capture lead paragraphs/captions/table inputs and are explicitly not a sentence-by-sentence audit of every result cell, citation, supplementary file or ancillary experiment. The report says so. Thus the prior matrix-coverage concern is **substantially resolved as a transparent audit map**, but not as full manuscript-wide evidentiary clearance. Because 62 items remain not audited and the intended target manuscript remains absent, no submission signoff follows from the expanded matrix.

**Final independent verdict: HOLD.** The six-cohort descriptive reconstruction and Tier 1 aggregate reproduction are supported; the corrected bootstrap prose is internally consistent; but original execution provenance, public Tier 2/3 reproduction, rights clearance, intended manuscript identity and high-priority unaudited/contested claims remain material blockers.
