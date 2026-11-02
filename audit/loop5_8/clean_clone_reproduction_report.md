# Clean-clone reproduction report

## Test scope and baseline

A new shallow clone of the current public `main` was made at `D:\temp\icc_loop58_clean_20261102`. It resolved to `29bcc279589d4a6c1e6747885cc857085ac8d6d0`, matching `origin/main` at baseline. This is the current public baseline, not a Loop 5.8 release commit: Loop 5.8 outputs remain uncommitted. The clone did not reuse local untracked files.

## Tier outcomes

- Tier 1 stability aggregate arithmetic: PASS on current public baseline. `python audit/loop5_6/minimum_aggregate_package/reproduce_aggregate.py` exited 0 using the tracked 72-row input.
- Tier 1 13-dataset benchmark statistic from raw scores: unavailable in public clone because source score CSVs absent; only local FYP rows were inspected.
- Tier 2: FAIL / unavailable to public clone; partition and run files absent.
- Tier 3: NOT RUN; source inputs, run identity and environment lineage are insufficient to authenticate a full reproduction.

## Exact commands/runtime/output hashes

- Clone command: `git clone --quiet --depth 1 https://github.com/AkashKundu114/icc-clustering.git D:\temp\icc_loop58_clean_20261102`; exit 0.
- Clone identity: `29bcc279589d4a6c1e6747885cc857085ac8d6d0`.
- Runtime: Python 3.14.6; no dependency installation required (script uses standard library).
- Reproduction command: `python audit/loop5_6/minimum_aggregate_package/reproduce_aggregate.py`; exit 0.
- Script SHA-256: `3cac0aff64d4d949622cfc163e3f15cbf654759a890c908bba193c55fbeb0a04`.
- Input SHA-256: `577cbab79913020ce362b8280ccb8c7ef62952d28ea47a45950f75cca2ff4b4f`.
- Captured stdout file: `clean_clone_tier1_output.json`, SHA-256 `538f5e9ce1026689eeebf5fb8a79126e82c946be269c6a82afd03a4a45cfa9a5`.
- Output: 72 rows, 6 datasets, 12 methods; mean stability 0.5165860620823638, mean external ARI 0.0523121821722892, mean gap 0.46427387991007457, median gap 0.44840681694162077. The small last-digit stability variation versus Loop 5.7 reflects the serialized aggregate input and float arithmetic.

No runtime duration was captured, so none is asserted. Tier 2 and Tier 3 were not attempted in the clean clone because the required inputs are absent. A clean clone of a future immutable Loop 5.8 release remains necessary if these deliverables are later committed.

**Conclusion:** Complete public reproduction remains unverified/unsupported. No release is claimed by this report.

