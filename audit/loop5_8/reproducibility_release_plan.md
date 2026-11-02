# Reproducibility release plan

## Current state and tiers

The current public target checkout is at the Loop 5.7 commit noted in `baseline_state.md`. Existing clean-clone evidence (Loop 5.7) established only Tier 1 aggregate arithmetic. Local FYP evidence adds Tier 2 partition-level recalculation in the audit environment, but these partitions, per-fit Parquets, input caches and raw benchmark CSVs are not part of the public target clone. Tier 3 (fresh clustering from inputs) has not been performed and cannot be claimed from saved output alone.

| Tier | What it establishes | Current status | Required release material |
|---|---|---|---|
| 1 Aggregate verification | Recalculate tables/statistics from aggregate CSV/score summaries | PARTIAL: public clone reproduced stability table arithmetic; broader raw benchmark score CSV unavailable there | Aggregate inputs, scripts, environment lock, tests and output hashes |
| 2 Partition-level verification | Recompute ARI/stability from exact run partitions | LOCAL ONLY; not independently available to a clean public clone | Rights-cleared partition archive or controlled access, sample-index schema, cache/version lineage, run records and hashes |
| 3 Full experimental reproduction | Refit all clustering methods from exact inputs/config | NOT DEMONSTRATED | Legally accessible/versioned inputs, preprocessing and fit configs, environment, seed map, code commit, hardware/runtime and deterministic comparison tolerances |

## Proposed package layout

`reproduction/README.md`; `environment.yml` or pinned requirements; `data_acquisition/` containing upstream-only acquisition instructions and version/hash checks; `configs/` for dataset and experiment parameters; `scripts/` for preprocessing, partition metric reconstruction, benchmark summaries, figures and tables; `results/` only for rights-cleared derived outputs; `manifests/` with dynamic SHA-256, source, version, role and license; `checksums/SHA256SUMS` calculated from actual package bytes.

Release data only after rights review. Never include raw or transformed third-party data absent documented permission. Yale B remains explicitly excluded until written terms permit redistribution. Derived partitions may encode dataset-specific information and are not automatically rights-free. The current manifest should provide source URLs/IDs, versions, retrieval dates, attribution, preprocessing, and expected shapes; it must not claim a hash for unavailable source bytes.

## Reproduction instructions the release must include

1. Create the pinned environment and print Python/OS/library versions.
2. Obtain each source dataset directly from its authorized upstream and record retrieval date/version.
3. Verify source hashes only when an upstream checksum exists; otherwise record computed local hash as an identity check, not upstream validation.
4. Run preprocessing with explicit label separation and stable sample-ID/order checks.
5. Run Tier 1 or Tier 2 scripts with mandatory expected inputs and fail-fast checks.
6. Generate tables/figures into a clean output directory; compare numeric outputs using documented tolerances.
7. For Tier 3, separately document estimator nondeterminism, thread settings, hardware and expected runtime/storage before any full run.

A public release is not yet assembled or tested. Do not treat the proposed Zenodo record as a data archive: prior verification found it restricted with no attached files. No third-party data are authorized for bundling by this audit.
