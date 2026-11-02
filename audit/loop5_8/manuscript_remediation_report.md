# Manuscript remediation review — FYP candidate version

## Version boundary

The target checkout at `29bcc279589d4a6c1e6747885cc857085ac8d6d0` contains no tracked manuscript, and `paper/manuscript/main.tex` is absent. The accessible manuscript reviewed here is `D:\Final Year Project\paper\main.tex`, SHA-256 `BB09E87B34E529E3D8CA83BBF69BDFBBCB57AEDF75B2BC3BB49D6336A7911C53`, from the separate `research/dami-revision` worktree at `60b163f22b5931da35a1ace07d1934bf3bdd65e3`. This FYP draft is materially broader than the Loop 5.7 target manuscript: it includes confirmatory biobank, simulation, ablation, runtime/scaling, biological marker, theoretical, and clinical-adjacent claims. Findings for it must not be attributed automatically to an unprovided submission file.

The TeX source is largely packed into a small number of physical lines; locations below use actual source lines where available, section/table/figure identifiers, and source offsets from the claim-matrix generator. The expanded matrix has two layers: high-priority claim adjudications with recommendations, plus exact quoted lead paragraphs for every section/subsection, inline figure/table captions and generated `gen/table*.tex` input. The latter rows are explicitly **Not audited** and exist to make remaining coverage visible; they do not represent a completed evidentiary review of every sentence, result cell, bibliography item or supplement. The full manuscript was read at section level and high-impact claims were traced, but not every ancillary experiment was rerun.

## Adversarial summary

The narrow six-cohort descriptive finding survives from saved partitions: for 72 dataset-method cells, average pairwise overlap ARI across 435 dependent repeat pairs is distinct from average external ARI across 30 partitions; the overall cell gap mean is 0.464274 and median 0.448407. Saved run records use label-stratified 80% subsamples, shared split schedules and fixed model seed; this does not assess initialization robustness. It is a bounded empirical observation, not proof that stability generally fails as a validity indicator.

The nine-cell selection is post hoc. The 60 nondegenerate cells have a cell-weighted mean gap 0.485376. The manuscript interval `[.379,.662]` is based on a cohort-resampling statistic with equal cohort weights, whose point center is 0.499925, not 0.485376. Do not state that this CI estimates the .485 cell-weighted quantity. Prefer to remove the interval from the primary manuscript and show cohort-specific descriptive results, or present a separately labeled exploratory equal-cohort estimand with its exact center and the six-cohort limitation.

There is a second key selection ambiguity. “All 18 cells” in the manuscript is the 3 recurrent methods × all 6 cohorts (mean stability .638304, ARI .045733); the Rule(i′) set of 18 cells instead has means .720011 and .003873. Define both explicitly or remove the phrase “all 18 cells.” The nine cells are exactly the three recurrent methods on selected cohorts and are not an independent confirmation.

The broad benchmark count and Friedman statistic can be recalculated from 3,000 saved ARI rows (13 datasets, 12 methods, 156 complete cells; χ²=11.556213, df=11, p=.397908). Saved Pass F and CoHiRF seed schedules differ and are not paired: Pass F uses 0–29/0–9 and CoHiRF uses 42–71/42–51. This count is saved-score evidence, not authenticated model-fit execution. The target public clone lacks these CSVs.

The public data/code claims are false for the current public repository state: the FYP has local data/results, while the fresh target clone does not contain the partition/run files, caches, raw benchmark records or exact reviewed manuscript. The cited Zenodo record has restricted access and no files. Do not claim full public availability until an actual rights-cleared archive and clean reproduction pass exist.

## Claim corrections

Use `manuscript_claim_evidence_matrix.csv` for claim-level statuses and `remaining_claims_audit_plan.csv` for experiments not audited in this review. Highest-priority modifications before considering submission:

1. Remove unsupported causal phrasing connecting high dimensionality to the observed empirical discordance. Keep simulation statements limited to their synthetic setup, with that data-generating process verified separately.
2. State that six-cohort resampling is descriptive/exploratory; no universal cohort-population inference follows from six convenience cohorts.
3. Explicitly disclose reference-label-informed stratification, overlapping sample subsets, shared cohort splits and fixed solver seed; call this subsampling sensitivity under that protocol, not general algorithmic robustness.
4. Treat the nine-cell and 18-cell post-hoc subsets as supplementary exploratory analyses; report full eligible population and selection chronology.
5. Remove the mismatched confidence interval from the primary claim until estimand and code are corrected.
6. Correct seed schedules and distinguish saved ARI score records from authenticated fit executions.
7. Remove “all data, seeds and code are publicly available” and the Zenodo archive assertion until actual access and content are verified.
8. Remove or rewrite high-priority unreviewed claims (GAC/BGSS superiority, clinical use, Prostate mechanism, confirmatory validation, causal simulations, theoretical guarantee, scalability) unless supported by separate, version-matched raw evidence and source audits. The FYP red-team report contains material contrary findings, including label-informed construction, baseline surrogate/fidelity concerns and dataset leakage; those must be adjudicated before retaining headline claims.

## Review limitations

The target repository's intended submission manuscript is missing; the FYP manuscript is a candidate, not established as the submission version. This review did not execute confirmatory biobank, GAC/BGSS ablation, synthetic causal, scaling, clinical marker, or theoretical analyses. The current FYP draft claims some of these are preregistered/confirmatory; the claims remain unverified here, and conflicting red-team findings require explicit resolution. This report is not an editorial/formatting certification.
