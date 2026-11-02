# Clean-clone reproduction report

A fresh shallow clone of GitHub `main` was created at commit `4fd21edaf7e4f45a8bea6acc8a052ad5f55275ba` under a temporary audit path and then removed after the test. It lacked `data/cache/*.npz`, `results/stability/partitions/`, `results/stability/runs/`, `results/passF/benchmark_matrix_passF.csv`, `results/exp3_cohirf_benchmark.csv`, and the local ZIP. It also did not contain the ignored current manuscript.

In that clean clone, the tracked `audit/loop5_6/minimum_aggregate_package/reproduce_aggregate.py` ran successfully using the included aggregate CSV and the standard library. It reproduced 72-row arithmetic: mean stability 0.516586, external ARI 0.052312, gap 0.464274, median gap 0.448407. This is **aggregate arithmetic reproduction only**. The ZIP named by the Loop 5.6 test JSON is not in the commit; the tracked package directory is.

No dataset acquisition, hash validation of raw partitions, fresh clustering rerun, or output comparison for the 4,320 fits was possible from the clone. The recovered FYP branch is local and not advertised on the configured GitHub remote. Zenodo DOI files are restricted/empty. **Complete public reproduction: FAIL.**
