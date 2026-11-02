# Clean clone test — Loop 6.0

## Clone identity

- Fresh shallow clone URL: `https://github.com/AkashKundu114/icc-clustering.git`
- Clone path: `D:\temp\icc_loop6_0_clean_5dac376_a` (not reused from earlier loop).
- Clone command exit code: `0`.
- Exact HEAD: `5dac3762f34b756a1047e099b4465c8a1954daad`.
- Initial worktree: `main...origin/main` (clean).
- Python: `3.14.6`; OS: `Windows-11-10.0.26300-SP0`.

## Tier tests

| Tier | Result | Command / reason | Evidence |
|---|---|---|---|
| 1 Aggregate | PASS | `python audit/loop5_6/minimum_aggregate_package/reproduce_aggregate.py` (exit 0) | stdout SHA-256 `538f5e9ce1026689eebef5fb8a79126e82c946be269c6a82afd03a4a45cfa9a5`; 72 rows, 6 datasets, 12 methods; mean stability 0.5165860620823638, mean external ARI 0.0523121821722892, mean gap 0.46427387991007457, median gap 0.44840681694162077 |
| 2 Partition | FAIL / inputs absent | Checked `results/stability/partitions/`, `results/stability/runs/`, and `data/cache/`; all absent | Cannot recompute per-repeat ARI or pairwise intersection stability from this clone |
| 3 Full experiment | NOT RUN | Producer/configuration/input linkage and exact datasets are unavailable in public clone; no fits attempted | No fresh clustering execution is claimed |

Tier 1 uses stored aggregate CSVs; it is arithmetic verification only. It does not validate source partitions, model runs, or all manuscript tables/figures. No external package installation was required for the Tier 1 command. The command writes an expected `recomputed.json` into the clean clone; no tracked files changed. Runtime was not instrumented and is not reported.
