# Public package specification

A limited aggregate-reconstruction package was assembled in `minimum_aggregate_package/` and archived as `minimum_aggregate_package.zip`. It contains the tracked 72-row aggregate summary, a standard-library-only recomputation script, manifest, and scoped README. It recomputes descriptive aggregate arithmetic only; it does not reproduce clustering fits, subsamples, stability from assignments, or labels.

A full package would additionally need versioned source code and lockfile, acquisition/version/licensing instructions for each cohort, exact preprocessing and stable sample IDs, X/y checksums, the saved partitions and per-fit rows (or deterministic regeneration), config and seeds, environment/hardware/runtime, and all table/figure generation. Run-level files and caches recovered in FYP are ignored local files and not in target Git/release archives. License review did not establish redistribution rights for all transformed data; do not bundle datasets until permissions and attribution are verified (including Yale B where applicable). No DOI/archive release containing them was verified.

Current package status: minimum aggregate arithmetic package exists and was tested in a clean extraction; complete evidence package remains unavailable.
