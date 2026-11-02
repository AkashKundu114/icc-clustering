# Provenance chain

| Stage | Evidence and identity | Finding |
|---|---|---|
| Code under audit | target Git commit `313e1542d524ddd2b38fa8c7e2ae885f9c52b7ca` | Verified code-state identity. |
| Loop 5.6 deliverables | target HEAD/origin main `4fd21edaf7e4f45a8bea6acc8a052ad5f55275ba` | Verified published main commit; contains all Loop 5.6 files. |
| Original protocol | FYP Git commit `330738037fcb7f4ec8537581051b856a63c2b0d5` | Protocol history verified; not execution evidence. |
| Post-hoc Rule(i′) amendment | FYP Git commit `548d68d54bb42bac76f20908cda1ae9a671e5b60` | Occurred after observing Prostate CoreHalo collapse; post-hoc. |
| Historical code+summary commit | FYP Git commit `49f3882fe5385913a9af1a5b89138c6ae6d95579` | Contains source/protocol/tracked summary and tracked reference cache copies; does **not** contain the ignored partition/run artifact grid. Do not call it the execution commit. |
| Actual stability run | 4,320 NPY and 4,320 Parquet files in local FYP worktree | Internal result grid complete, but exact run date/commit/config/input digest not stored per row. **Original execution commit: UNVERIFIABLE.** |
| Inputs | `D:\Final Year Project\data\cache\*.npz` and matching tracked `experiments/exp3_real_world_benchmarks/data/cache/*.npz` | Byte-identical hashes for all six; run-to-cache linkage remains conditional because run rows omit hashes/IDs. |
| Stability reconstruction | `audit/loop5_7/scripts/independent_reconcile.py` | Independently recalculates assignments/metrics. It does not rerun model fits. |
| 13-dataset benchmark raw scores | FYP `results/passF/benchmark_matrix_passF.csv` and `results/exp3_cohirf_benchmark.csv` | Tracked locally in the FYP Git history at commits 7f74f68… and 567c526…; record commits do not prove fit execution. Current target GitHub main does not contain these files. |
| Current manuscript | `paper/manuscript/main.tex`, SHA ` a0c4274ec5dfbb40311d3d33d7ad8179b17dee145851fd2e5b255e498054e75f` | Locally present but ignored/untracked by target Git; exact reviewed manuscript is not identified by a public commit. |
| Loop 5.7 execution | target checkout HEAD `4fd21edaf7e4f45a8bea6acc8a052ad5f55275ba` | Scripts executed against this checkout; local execution manifest records current time. |
| Loop 5.7 final deliverables | not committed | No Loop 5.7 commit was created. |

Current FYP local branch HEAD is `60b163f22b5931da35a1ace07d1934bf3bdd65e3`; `git ls-remote --heads` does not expose its `research/dami-revision` branch (only target `main` was observed). This means FYP-tracked artifacts are not thereby proven publicly accessible. Hashes and timestamps for every recovered item are in `source_of_truth_manifest.csv`. SHA-256 and Git blob SHA-1 are distinct and not compared as equivalent.

The published Zenodo record named in the manuscript resolves to DOI `10.5281/zenodo.23852735`, but the API snapshot `zenodo_record_snapshot.json` reports `status=published`, `access_right=restricted`, and `files=[]`. Both GitHub releases v1.0.0 and v2.2.0 have zero assets. The DOI is a metadata record, not a downloadable reproduction archive.
