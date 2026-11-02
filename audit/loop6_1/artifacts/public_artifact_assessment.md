# Public artifact assessment

At baseline, `git ls-files results` contained zero files. Tracked data paths are only repository instructions, registry/config metadata and `.gitkeep` placeholders; no raw matrices, feature caches, partitions, fit records, or benchmark score CSVs were tracked outside internal audits. There are 92 relevant tracked code/metadata/result-related paths inventoried in `public_artifact_inventory.csv`; audit files are individually marked to exclude from the next public snapshot.

The aggregate summary used for Tier 1 is tracked under `audit/loop5_6/minimum_aggregate_package/`. Its calculated values were checked in Loop 6.0, but the source partitions are local/untracked, historical producer/execution is unauthenticated, and the Loop 6.0 rights matrix does not clear derived cohort artifacts for redistribution. Thus this review does not approve that summary as a public result artifact. No result files are to be moved into a public `results/` tree.

No third-party dataset artifact should be distributed. The 13-dataset rights matrix records raw/cached/partition release states as uncleared for most datasets and Yale B as not distributable absent permission. See `audit/loop6_0/release/data_rights_matrix.csv` (internal source of truth).
