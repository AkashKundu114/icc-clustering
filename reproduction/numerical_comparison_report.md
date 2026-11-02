# Numerical comparison and evidence status

## Scope

This ledger summarizes historical claims checked against locally available saved outputs. It does not assert that every number appears in one identified final manuscript: multiple manuscript candidates exist, and a canonical submission candidate has not been authenticated. It also does not claim fresh execution of the clustering experiments.

## Six-cohort saved-output reconstruction

The local evidence contains 4,320 partition arrays and 4,320 fit records for six cohorts, 12 methods, 30 repeats, and real/null modes. Independent recalculation from those files produced:

| Quantity | Historical claim | Recalculated from local saved outputs | Absolute difference |
|---|---:|---:|---:|
| Mean stability | 0.516586 | 0.5165860621 | < 1.2e-16 vs saved summary |
| Mean external ARI | 0.052312 | 0.0523121822 | < 1.0e-16 vs saved summary |
| Mean stability − ARI | 0.464274 | 0.4642738799 | derived from recalculated cell values |
| Median cell gap | 0.448407 | 0.4484068169 | derived from recalculated cell values |
| Mean null stability | 0.006620 | 0.0066196808 | < 1.0e-16 vs saved summary |

The gap is computed per cohort-method cell as that cell's stability summary minus its external ARI summary, then averaged or median-aggregated across the 72 cells. It is a descriptive contrast between two different measurements; it is not a universal metric of excess reproducibility over validity.

These comparisons verify arithmetic conditional on the local saved files and the assumption that array row indices match the corresponding cache rows. They do not authenticate the historical partition producer, cache lineage, sample identity, or whether the null transformation ran as intended. The local inputs and outputs are absent from the public clone, so a reviewer cannot independently reproduce these values from this repository alone.

## Selected-cell summaries

The historical Rule (i), Rule (i-prime), and Rule (iii) subsets contain 20, 18, and 9 cells, respectively, when recalculated from the local cell table. Rule (iii) is post-hoc and exploratory. The nine-cell summary must not be described as independent confirmation. An 18-cell summary of FCAG, FCM, and FastMVC across all six cohorts is numerically 0.638304 stability and 0.045733 external ARI; those methods overlap the post-hoc selected set, so that summary is also selection-conditioned.

## Separate 13-dataset benchmark

From local saved score tables, 3,000 rows cover 13 datasets, 12 methods, and 156 dataset-method cells. Recalculation gives Friedman chi-square 11.5562130178, 11 degrees of freedom, p=0.3979076148, and ICC-v2 average rank 5.6153846154 (rank 4 of 12). This is a separate external-ARI score benchmark, not a 13-dataset stability experiment. Score arithmetic does not verify fair implementations, independent fit execution, equivalent tuning budgets, or unambiguous handling of zero-valued failures.

## Recalculation tools and public limitations

The public tools are `scripts/recompute_saved_stability.py` and `scripts/recompute_benchmark_scores.py` under this directory. They independently calculate from user-supplied evidence, dynamically hash inputs, validate structural expectations, and fail on expected-hash mismatch. They do not ship evidence inputs. Their local positive runs used files outside a clean clone; they are not public reproduction passes.

The machine-readable claim ledger is [`claim-to-evidence-matrix.csv`](claim-to-evidence-matrix.csv). Source artifacts remain local and are not bundled because exact-source and derived-artifact redistribution rights are unresolved for several variants. Historical execution provenance remains unverified. Public reproduction Tier 1 and Tier 2 are unavailable; Tier 3 has not been run.

