# Benchmark claim verdict

This report independently checks the saved score matrix and reviews the source/assembly audit. `audit_benchmark.py` and `benchmark_assembly_check.json` reconstruct 2,750 Pass F rows from saved merge inputs within stated tolerances and add 250 CoHiRF records. They do not run clusterers.

- **13×12 complete score matrix:** verified as saved files (156 cells, no duplicate keys, each cell has its defined 10 or 30 row count).
- **“3,000 model fits”:** unsupported as a fit-event count. It is a count of saved score rows. Ward high-D seeds 10–29 copy seed 0; ICC-v2 high-D seeds 10–29 are imported from an ARI-only Pass E file. The unique fit event count cannot be authenticated.
- **Seed matching:** contradicted. Pass F and CoHiRF use different seed ranges; copied and imported rows also are not independent replications. No paired-seed inference.
- **Friedman χ²=11.5562, df=11, p=.3979; ICC-v2 rank 4/12:** verified from saved per-row scores after dataset-method aggregation. It is exploratory/descriptive ranking, not evidence of equality, superiority, or robustness.
- **Fairness:** limited. K is supplied using reference class count; full datasets are clustered transductively; implementation and compute budgets vary; ICC-v2 changes base engine for small N; FastMVC is a surrogate; Core-Halo has ambiguous zero score records. These are comparisons among local implementations under this pipeline.
- **Scalability/generalization:** not inferred from the omnibus ARI rows; separate runtime and holdout experiments remain unaudited in this loop.

Keep the 13-dataset score benchmark separate from the six-cohort stability analysis. The source CSVs are local FYP artifacts, absent from the clean target clone.
