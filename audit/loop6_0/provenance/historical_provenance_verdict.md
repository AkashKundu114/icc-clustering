# Historical provenance verdict — Loop 6.0

## Decision

**Historical execution: UNVERIFIED.** The recovered files support deterministic recomputation of metrics from saved partitions, but do not establish that each file was produced by the declared fitting invocation.

## Evidence inspected in this workstream

- Loop 5.9 provenance/producer_search.md, provenance_chain.csv, three_priority_cases.md, and duplicate_reaudit.csv.
- Separate FYP worktree D:\Final Year Project, branch research/dami-revision, HEAD recorded in Loop 6.0 baseline.
- Current tracked wrappers src/icc/baselines/classical.py and src/icc/core.py.
- All 4,320 existing partition files and 4,320 Parquet rows are reported and inventoried by Loop 5.9. This work did not rerun the full census.
- Direct reloading of six files and six Parquet records for the three priority duplicate pairs.

The FYP data directory is ignored/untracked. Its current bytes do not inherit provenance from the FYP Git HEAD. The tracked full-data stability runner and downstream audit scripts are not the missing partition writer. No writer for this exact NPY/Parquet grid, execution log, sample-ID manifest, or per-fit source/config/input hash chain was recovered.

## Independently reloaded priority duplicate pairs

All three pairs have byte-identical NPY files, identical ordered sub_idx, and identical assignments:

| Pair | N | Observed cluster sizes | Parquet metadata difference | Finding |
|---|---:|---|---|---|
| CNS CoHiRF null/real repeat 17 | 48 | 47/1 | same sub_seed=5017; null seeds 6017 and -1; runtimes 0.3122s/0.3133s | Exact equality verified; independent invocation and null transformation not authenticated. |
| Prostate CoHiRF null/CoreHalo real repeat 5 | 81 | 81 | same sub_seed=5005; null seeds 6005 and -1; runtimes 0.1169s/0.4060s | K=1 makes common degenerate output plausible; independent invocation not authenticated. |
| Prostate StdCons null/UngatedAC real repeat 16 | 81 | 80/1 | same sub_seed=5016; null seeds 6016 and -1; runtimes 0.3348s/0.3990s | Nontrivial cross-method/mode identity remains unexplained. |

Modification times differ, which is consistent with separate writes, but is not proof of distinct fitting calls. A saved success status and runtime are not process logs. Byte identity alone cannot identify model convergence versus copy/overwrite. Do not delete, normalize, or replace any historical file.

## Scope and limitations

This work did not execute original clustering fits and did not independently enumerate all 140 duplicate groups from their bytes. The 291-row inventory in duplicate_reconciliation.csv is a Loop 6.0 reclassification of Loop 5.9's byte-level census, with the source basis explicitly retained. The three named pairs were loaded directly. No classification beyond CANNOT_CLASSIFY is justified.

## Path to closure

Recover contemporaneous producer, logs, input/cache hashes, stable row identities and write lineage if available. Otherwise preserve the original evidence as historically unverified and use a clearly labelled prospective experiment. A prospective run can validate a new protocol; it cannot retroactively authenticate these files.
