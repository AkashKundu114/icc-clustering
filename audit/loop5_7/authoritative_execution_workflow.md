# Authoritative evidence workflow

1. Start with target code commit `313e1542d524ddd2b38fa8c7e2ae885f9c52b7ca`; separately record the Loop 5.6 audit-deliverables commit `4fd21edaf7e4f45a8bea6acc8a052ad5f55275ba`. The exact original fit-execution commit is **UNVERIFIABLE**.
2. Confirm the six FYP caches and all expected `results/stability/partitions` and `runs` files exist; calculate SHA-256 dynamically. Verify local `data/cache/*.npz` against the tracked `experiments/exp3_real_world_benchmarks/data/cache/*.npz` copies. Do not infer execution linkage from cache identity alone.
3. Run `python audit/loop5_7/scripts/independent_reconcile.py` from a checkout where `D:\Final Year Project` is present and required Python dependencies are installed. This independently reads all 4,320 partitions and 4,320 Parquet records; it performs no model fits and writes only beneath `audit/loop5_7/`.
4. Run `python audit/loop5_7/scripts/build_final_deliverables.py`. It rebuilds source inventory/manifests and benchmark mean comparison from raw score CSVs. Do not run Loop 5.6 `reconstruct_loop5_6.py` after the partition-level reconciliation; it is aggregate-only and can overwrite root outputs.
5. Review `independent_reconstruction_summary.json`, all 72 rows in `recomputed_cell_results.csv`, per-repeat observations, nine-cell sensitivity outputs, bootstrap reconciliation, and the benchmark raw-score checks. Then review the current manuscript claim matrix.
6. Verify `SHA256SUMS` only after all output files are final. It is a digest list of Loop 5.7 deliverables; it is not a signature or proof of public availability.

## Scope and reproducibility

This procedure reproduces metrics from saved partitions. It does **not** reproduce the clustering fits that produced the saved partitions. A fresh GitHub clone reproduces only aggregate CSV arithmetic through the tracked minimum-package script. The ZIP referenced by the Loop 5.6 test is ignored/untracked. A full independent clone+data-acquisition+fit rerun is not available.

The numeric algorithms are deterministic for fixed input bytes and software behavior; the Loop 5.6 scan manifests are not byte-deterministic because they include filesystem timestamps/order. The Loop 5.7 scripts include execution timestamps in summaries, so report bytes will change even when numeric calculations do not.
