# Prospective stability experiment protocol

This is a design for a **new experiment**, not a repair of historical provenance. Execute only after data rights, exact cohort/version, and compute estimates are approved. Pre-register the primary analyses, subset rules and exclusions before inspecting outcomes. Prefer a label-blind sampling protocol for a new robustness study; if preserving the historical label-stratified 80% design for comparability, explicitly treat its reference-label information as part of the design and do not call it label-blind.

## Immutable run package

1. Pin Git commit and archive its source tree; hash configuration, dependency lockfile, runner, dataset acquisition manifest and preprocessing scripts.
2. For each dataset, record upstream accession/version/URL/retrieval time, license and attribution, raw/cache SHA-256, feature matrix shape/dtype/hash, label-vector hash, and an ordered stable sample-ID manifest. Keep IDs separate from labels until prespecified sampling requires class stratification.
3. Record preprocessing operations, fitted parameters, feature order, filters, missing-data decisions, and post-preprocess matrix hash.
4. Use a configuration file with cohort, method, mode, target K source, model parameters, subsample fraction, replacement policy, repeat index, sub-seed, null transformation and null seed. Derive a unique run ID from the canonical JSON config plus input hashes; never reuse output paths.
5. For each run, write start/end UTC, host/OS/hardware, Python and package versions, command, process exit code, stdout/stderr log hash, input/cache/preprocess hashes, sample-index list and hash, algorithm parameters, seed(s), output-label hash, serialized partition hash, ARI and status. Write to a temporary path then atomic rename, keeping the record immutable.
6. Store each fit in a unique directory, with a run record bound to partition SHA-256. Never infer association from filename alone.

## Integrity gates

Before summaries are computed, fail the run if any condition holds: duplicate run ID; missing or duplicate fit record; run-record-to-file hash mismatch; unknown dataset/method/mode; unexpected seed; duplicate/out-of-range sample index; sample ID/index mismatch; label count differs from index count; unsupported K; non-finite metric where required; status not explicitly successful; missing input hash; output overwrite; missing null transformation record; or a duplicate output hash without an explicit review flag. Do not automatically reject legitimate identical partitions; independently re-run the fit from the same recorded inputs and compare outputs, while preserving both run IDs and logs.

## Analysis plan

1. Primary descriptive metric remains mean pairwise ARI over the 435 pairwise overlaps among 30 subsamples; save every pair metric with repeat IDs and intersection sample IDs/counts.
2. External ARI is computed per subsample against the same cohort's reference labels for the sampled IDs. The design must predeclare whether class stratification is used.
3. Keep stability and external ARI summaries linked by dataset, method and exact sample schedule. Do not treat the 435 pair values or 30 repeats as independent biological cohorts.
4. Report all cells first. Any degeneracy filtering is secondary and prespecified. No nine-cell recurrence analysis unless independently justified before data inspection.
5. Null partitions must record the transform seed and transformed matrix hash; real/null fits must share only the intended sample indices and must have separate, auditable data matrix hashes.
6. A clean runner should recompute from immutable input hashes, produce a complete manifest, and compare numeric metrics under explicit tolerances. Public release remains subject to dataset rights.
