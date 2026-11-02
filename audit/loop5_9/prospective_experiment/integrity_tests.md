# Prospective run integrity tests

Required automated gates before computing summary results:

1. **Unique keys:** no duplicate run UUID or duplicate `(experiment,dataset,method,mode,repeat)` key. Retries use new run UUIDs and explicit retry linkage.
2. **Required metadata:** fail if source commit/config/environment/data/preprocessing/sample-ID hashes or mode-specific seeds are absent.
3. **Hash checks:** recompute SHA-256 from actual input and output bytes; compare to recorded expected values and fail closed on mismatch.
4. **Partition shape:** predicted label vector length equals ordered sample-ID count; no NaN labels; output sample IDs exactly match input sample IDs in order.
5. **Index validity:** all sampled row indices are integer, unique when without replacement, in bounds, expected size and match stored ordered sample IDs.
6. **Seed consistency:** subsample seeds reproduce the index selection; model and null seeds match frozen configuration; real arm has no null transform and null arm records transform and null seed.
7. **Record-to-file linkage:** Parquet/JSON run ID, configuration, metadata and output digest match the referenced partition; exactly one final status record exists per run ID.
8. **Status integrity:** failed fits remain failed; a success requires exit code zero and valid partition. No missing cell/repeat can be silently filled.
9. **Cluster diagnostics:** recompute observed K and sorted cluster sizes; flag unexpected K, singleton collapse and min-cluster threshold breaches; never drop without prespecified rule.
10. **Duplicate output hash audit:** group all identical partition hashes across all run keys. Require an explanation based on actual separate run IDs and inputs; preserve each run record. Flag cross-method/cross-mode identical non-degenerate assignments for investigation.
11. **Pair metrics:** recompute sample intersections and pairwise ARI from saved labels, verify each unordered repeat pair appears once, and retain intersection sizes. Do not treat pairs as independent.
12. **Aggregate reconciliation:** regenerate cell and cohort summaries from lowest-level records; compare only after exact key completeness is established; report discrepancies and fail when outside stated tolerances.
13. **Clean reproduction:** execute Tier 2 and Tier 3 in a fresh clone/environment with no local ignored data; record commands, versions, exit codes, runtime, hashes and numerical tolerances.

This protocol is prospective. Passing it would create auditable new evidence, not authenticate historic Loop 5.6/5.7 runs.
