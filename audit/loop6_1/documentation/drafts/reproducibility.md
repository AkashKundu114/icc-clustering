# Reproducibility status

Reproducibility is reported in three distinct tiers. Passing a lower tier does not imply a higher one.

| Tier | Status | Required inputs | Public command and expected result |
|---|---|---|---|
| Tier 1 — aggregate reproduction | **Tested on the currently inspected repository snapshot; not ready for the intended public tree** | Aggregate summary CSV and Python standard library | The aggregate check passed in a fresh clone of the inspected snapshot and emitted 72 rows with mean stability 0.516586, mean external ARI 0.052312, mean gap 0.464274, and median gap 0.448407. Its current script/input are housed with internal audit material and are not a public-facing reproduction command. Migrate a rights-cleared aggregate artifact and checker to a public path, then rerun the clean-clone test before calling Tier 1 available in the restructured release. |
| Tier 2 — partition-level reproduction | **UNAVAILABLE** | Exact cache arrays, 4,320 partition NPY files, 4,320 per-fit records, stable sample-index mapping and metric script | No command can run from the clean public clone: partitions, fit records, and caches are absent. |
| Tier 3 — full experimental reproduction | **NOT RUN** | Authorized/versioned datasets, a frozen experiment producer/configuration, environment and per-fit provenance | No historical-fit reproduction command exists; the historical producer and input linkage were not recovered. |

The Tier 1 test validates arithmetic over stored aggregate rows only. It does not reconstruct repeated observations, validate every reported result, or rerun algorithms. The 72-cell values were reconstructed using local partition evidence not present in the clean public clone. If internal audit materials are excluded from the public tree, Tier 1 must remain unavailable until its minimal inputs and script are independently reviewed for accuracy and distribution rights, relocated, and clean-clone tested.

Dataset access instructions are not a data release. Check each source's current terms before acquisition or redistribution. Do not redistribute Yale B files without written permission.
