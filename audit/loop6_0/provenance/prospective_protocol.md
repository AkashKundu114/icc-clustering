# Prospective protocol and run architecture

## Status

This is a proposed, versioned new protocol. No biomedical model fit was executed for this workstream. Historical outputs remain untouched and are not used as pilot output.

## Feasibility assessment

The local FYP worktree has six cohort cache NPZs and the historical partition/Parquet files, but those caches do not carry a stable source-sample manifest or a per-fit cache hash; rights for redistributing caches and derived partitions remain uncleared. The original null transform and full producer are unavailable. Thus a scientifically comparable full run cannot yet be started from the recovered state.

The 4,320 historical Parquet rows report summed runtime of 17,056.1 seconds (~4.74 serial hours), median 0.129 seconds, 95th percentile 8.71 seconds, maximum 151.73 seconds. This is a rough lower-fidelity planning reference from unauthenticated old rows, not a prospective runtime estimate; setup, I/O, environment, and methods may differ. Existing partition files are small, but exact total package size has not been certified for release. A full rerun is therefore not launched. Running a single KMeans fit against an unverified cache would not resolve the missing method/null protocol and could be mistaken for comparable evidence.

## Prospective experiment design (to freeze before any scientific run)

1. Assign an immutable experiment ID and run UUID per method × dataset × mode × repeat. Never reuse output paths.
2. Freeze source commit, clean-tree status, configuration bytes, dependency lock, operating system, hardware, and thread limits. For a pilot executed from an uncommitted audit worktree, explicitly set dirty=true and hash the exact source files; do not call it a release run.
3. Acquire each dataset using an authorized source/version and record accession, download date, terms/attribution decision, raw SHA-256, transformed matrix SHA-256, preprocessing config SHA-256, and stable sample-ID file SHA-256. If no stable source IDs are available, use immutable row ordinals bound to the feature-matrix hash and explicitly say these are cache-row IDs, not biological identifiers.
4. Freeze the preprocessing before seeing analysis outcomes. Record missingness/filtering, transformations, feature normalization, and sample order.
5. Primary protocol should be unstratified without-replacement subsampling if the scientific question is label-independent sampling robustness. This is a new protocol and must not be presented as the original experiment. If a strict replication of the historical design is attempted, reproduce its reported 80% class-stratified sampling and disclose label-informed sampling; do not claim the sampling is label-blind.
6. Record K source. If K is taken from reference-label class count, call the analysis label-informed and do not interpret ARI as wholly independent validation.
7. Pre-register exact methods, implementations, parameters, failure policy, model seeds, and null transformation. Do not include a null condition until its transformation has been recovered or a new transformation has been specified and validated independently.
8. Separate sampling sensitivity from initialization sensitivity. First use one frozen model seed across subsamples; then, in a separately named factorial experiment, vary model initialization while holding sample subsets fixed.
9. Save ordered indices and sample IDs, input/mode hashes, predictions, status, logs, runtime, full exception text or its hash, and all file hashes at each invocation.
10. Recompute external ARI per partition and pairwise ARI only on explicitly recorded intersections. Derive aggregates in a separate deterministic script; do not use pairwise comparisons as independent replicates.
11. Store only authorized derived artifacts in the release. Until data rights are established, retain private local inputs and publish acquisition instructions/checksums.

## Pilot decision

No dataset/model pilot was run. This is intentional: the available cache lacks an authenticated source-ID mapping, applicable redistribution terms remain unsettled, and the missing historical null transformation makes a partial replication ambiguous. The validator was tested on synthetic metadata-only fixtures; it did not fit any model.
