# Independent adjudication — Loop 5.9

## Role and evidence inspected

This review is a separate adjudication of specialist work, not a new full experiment. I inspected the following generated files and source:

- `provenance/provenance_verdict.md`, `provenance/producer_search.md`, `provenance/duplicate_reaudit.csv`, `provenance/three_priority_cases.md`, `provenance/prospective_rerun_protocol.md`, and `provenance/recompute_forensics.py`.
- `statistics/estimand_reconciliation.md`, `statistics/cell_reconstruction.csv`, `statistics/selection_reconstruction.csv`, `statistics/bootstrap_reanalysis.csv`, `statistics/reconstruct_stats.py`.
- `benchmark/benchmark_claim_verdict.md`, `benchmark/benchmark_assembly_check.json`, `benchmark/seed_provenance_matrix.csv`, `benchmark/fairness_matrix.csv`, `benchmark/method_implementation_audit.md`, and `benchmark/audit_benchmark.py`.
- `reproducibility/tier_status.md`, `reproducibility/clean_clone_log.md`, `reproducibility/data_rights_matrix.csv`, `reproducibility/zenodo_record_check.json`, `reproducibility/github_releases_check.json`.
- Frozen target local candidate `manuscript/pre_remediation/canonical_local_candidate/manuscript/main.tex`, `numbers.tex`, `references.bib`, relevant `gen/` tables, figure set, `manuscript_claim_matrix.csv`, `table_figure_audit.csv`, `section_review.md`, and static `build/build.log`.

Agents A and C supplied source-based investigations and their artifacts. Agent B and D reached execution limits after partial artifact creation; the lead ran the statistical reconstruction and fresh clone test. Agent E also reached usage limit before reviewing the canonical target manuscript; the lead reviewed the target version and generated the claim audit. Agent F (this review) independently adjudicated the specialist evidence. No original clustering fits were run.

## Direct independent checks executed

1. Ran `python audit/loop5_9/benchmark/audit_benchmark.py`: exit 0; output confirmed 2,750 Pass F rows, 250 CoHiRF rows, 3,000 combined saved rows, 156 cells, no duplicate keys, exact Pass F matrix assembly from merge inputs and no Ward copy mismatches relative to the source copy operation. This verifies saved-row assembly, not fit execution.
2. Independently ran a short SciPy calculation directly against the two local raw score CSVs, grouping ARI by dataset×method and calculating Friedman and average ranks: χ²=11.556213017751475, df=11, p=0.3979076148432822; ICC-v2 average rank 5.615384615384615, position 4/12. This reproduces arithmetic from saved rows.
3. Rechecked target manuscript hashes: `paper/manuscript/main.tex` and its frozen copy are `a0c4274...`; the separate FYP `paper/main.tex` and target `paper/archive/main_dami_revision_historical.tex` are `bb09e87...`. This confirms the version distinction. The canonical file is ignored/uncommitted, despite being named by local `paper/README.md`.
4. Read the full stability reconstruction script and confirmed its intersection-ARI calculation matches the stated 435 unordered repeat pairs; it checks saved ARI against Parquet rows and cell aggregate values. I did not independently rerun all 62,640 pair computations in this adjudicator role; the lead ran the specialist reconstruction script.
5. Read the current clean-clone and rights evidence; I did not rerun the clone in this adjudicator role. Lead reports an exact baseline clone at `d0c4665...`, Tier 1 pass, Tier 2 absent inputs and Tier 3 not run.

## Findings and adjudication

### Stability–accuracy result

The result survives as a descriptive calculation on locally recovered partitions: cell-level stability is a mean over 435 pairwise ARIs on overlapping samples; external ARI is a mean over 30 partition/reference comparisons. Across the 72 saved cells, means and gaps recalculate to the previously reported values. These are not independent cell-level observations, nor is each scalar stability value paired to a single ARI repeat. Shared cohorts, sample subsets, methods and pairs limit inferential claims. Label-stratified sampling and K specified from reference labels mean the protocol is not fully label-blind. Fixed model seed assesses subset perturbation at that seed, not initialization robustness.

### Historical authenticity and duplicate files

The partition grid is internally complete and metadata-consistent according to Agent A's independent byte scan, but its generating script and execution log were not recovered across the FYP history and unmanaged archive. No per-fit source/cache/preprocessing hash or partition hash is in the run record. Therefore the 4,320 files cannot be authenticated as outputs of the claimed run process. The 140 exact duplicate groups and three priority pairs have exact payload equality; the two degenerate cases have plausible but unproven algorithmic explanations. The 80/1 Prostate StdCons-null/UngatedAC-real equality is unexplained. Classify duplicates as **cannot classify**, not as proven legitimate or proven corrupted.

### Bootstrap and subsets

The interval and point estimate are not paired: .485376 weights 60 eligible cells equally; the historical bootstrap averages cohort means. Six nonrandom cohorts do not justify confirmatory population inference; intervals also ignore within-cell repeat/pair uncertainty. There is an additional finite-bootstrap endpoint discrepancy: Loop 5.8's fresh seed-42 E2 interval is reported as [.378581,.661716], whereas Loop 5.9's executed script, using a different cohort order, yields [.378581,.653002]. The historical `make_stability_outputs.py` order is `colon,srbct,cns,leukemia,prostate,ovarian`; Loop5.9's reconstruction script order is `cns,colon,leukemia,ovarian,prostate,srbct`. With fixed random index draws, reassigning draws to cohort labels changes finite-B endpoints. Neither supports the manuscript's cell-weighted point/CI pairing. Remove inferential interval from primary abstract/conclusion; retain descriptive cohort and full 72-cell summaries. Nine-cell and post-hoc 18-cell analyses should be supplementary/exploratory only.

### Broad benchmark

The 3,000 figure refers to saved score rows, not 3,000 independently authenticated fits. Pass F assembly is reconstructible; Ward high-D seeds 10–29 are copied from seed 0, and ICC-v2 rows 10–29 were imported from another ARI file. CoHiRF uses a separate seed schedule. The raw rows produce the non-significant Friedman test and ICC-v2 rank 4/12, but this does not establish equality, superiority, robustness or held-out generalization. K is supplied from reference classes and method budgets/base learners differ; FastMVC is explicitly a surrogate.

### Manuscript and availability

The target-local paper README identifies `paper/manuscript/main.tex` as canonical, but the file is ignored and not tied to the target commit. Its full local package was frozen and statically audited; TeX compilation was unavailable and `Orcidlogo` missing. Most ancillary table/figure metrics were not independently regenerated. The separate FYP manuscript is historical and must not substitute. Availability claims are contradicted by fresh clone contents and the Zenodo snapshot (`access_right=restricted`, files=[]). Dataset-specific redistribution rights remain uncleared; no broad release is legal-cleared by this audit.

The narrow empirical claim is potentially defensible after source revision: in these six cohorts and under this particular resampling procedure, high pairwise subsample agreement can coexist with low external-reference ARI. It does not show that stability is useless or that ARI is complete biological truth.

## Unresolved disagreements / confidence

The finite-bootstrap endpoint discrepancy should be reconciled by fixing the cohort order and resampling code; because the interval is recommended for removal from primary claims, this does not change the disposition. The canonical manuscript is locally identifiable but not committed; author confirmation/freeze remains necessary. The claim matrix has 18 focused summaries and a 31-row figure/table path inventory, not full cell-by-cell statistical verification. Literature novelty, ablations, synthetic mechanisms, theory, scaling, clinical relevance and Prostate explanation remain unverified.

Confidence is high for direct arithmetic on saved benchmark rows and direct manuscript identity comparison; conditional for saved partition reconstruction because the full pair calculation was not independently rerun in this role; low for historical execution authenticity and dataset redistribution clearance.

**Independent verdict: HOLD.** Numerical reconstruction is not equivalent to authenticated execution or publication readiness.
