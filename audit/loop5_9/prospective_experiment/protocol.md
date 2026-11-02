# Prospective stability experiment protocol (new experiment; not historical authentication)

## Purpose and status

The Loop 5.6–5.9 audit did not recover an authenticated producer/execution trace for the historical 4,320 partition files. This protocol specifies a prospective rerun that would create auditable evidence. A rerun answers whether the descriptive result is reproducible under a specified current protocol; it cannot prove that the historical files were produced by that protocol.

## Immutable run setup

1. Create a new repository commit and a signed, immutable experiment tag. Capture `git diff --exit-code`, full commit SHA, branch, dirty state, and submodule commits.
2. Store environment lock and runtime report: OS/kernel, Python, NumPy, SciPy, scikit-learn, pandas, PyArrow, BLAS/OpenMP implementation, thread counts, hardware, GPU/CPU and memory.
3. Acquire each dataset through rights-cleared upstream instructions. Record accession/version, retrieval timestamp, upstream license/terms and computed raw-file SHA-256. Do not commit data absent permission.
4. Canonicalize and hash sample IDs before any filtering. Persist a separate ID manifest and a row-order hash. Hash raw matrix, labels (restricted separately if needed), transformed matrix, preprocessing configuration and feature list.
5. Freeze all model and sampling configuration in a signed JSON file before execution. State that class-stratified sampling uses reference-label proportions; if label-blind sampling is intended, use a separately pre-registered arm rather than changing the existing protocol silently.

## Per-fit execution

For every dataset × method × mode × repeat, create a unique UUID and write into a write-once path. Record original input SHA, transformed input SHA, sample-ID manifest SHA, exact ordered subsample-index SHA/list, partition output SHA, model source commit and dirty status, method/version/parameters, requested K and how K was selected, model seed, subsampling seed, null transformation seed, start/end time, exit code, exception/traceback, cluster count/sizes, labels SHA and metric outputs. Write a JSONL execution event before and after fitting; after completion write a Parquet record referencing the same UUID and artifact hashes.

Real and null arms must link to the same declared subsample indices when paired by design. Null transformation must be applied and hashed before fit. Output labels must be mapped back to the stable sample-ID order. Use temporary write plus atomic rename to immutable unique filenames; refuse to overwrite any existing run identifier or artifact.

## Metrics

Compute external ARI from each saved partition and labels under a documented missing-sample policy. Compute pairwise stability from the intersection of the exact two sample-ID sets, record both sample-index hashes and intersection size, and save every pairwise score with pair IDs. Keep per-repeat values, per-pair values and aggregates separate. Report pair dependence and do not use the 435 pairs as iid inference units.

## Reproducibility checks

Before analysis, run integrity tests from `integrity_tests.md`. The analysis must fail closed if any required hash, run record, sample-ID link, seed, expected cohort/method/mode/repeat key or status is missing. Reproduce from a clean clone and a new environment from the lockfile. Record Tier 2 and Tier 3 separately. Preserve failed runs and retries as separate records; never replace a failure with a success row or silently reuse a partition.

## Storage and rights

Keep restricted datasets in authorized storage. Publish only code, configurations, non-identifying manifests, aggregates and derived artifacts specifically cleared by each upstream terms review. Where partition outputs could be considered redistributable only with permission, publish a DOI to authorized access or omit them and clearly downgrade to Tier 1.
