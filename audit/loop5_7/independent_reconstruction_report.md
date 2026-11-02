# Independent reconstruction report

## Execution performed

The lead auditor independently executed `scripts/independent_reconcile.py` against local FYP inputs: 4,320 `results/stability/partitions/*.npy`, 4,320 `results/stability/runs/*.parquet`, six `data/cache/*.npz`, and the tracked `subsample_stability_summary.csv`. It loaded the stored assignments, recalculated each real and null pairwise intersection ARI, recalculated each repeat ARI against the cache labels, and checked fit-row fields by key. This is a **partition-level metric reconstruction**, not a fresh rerun of 4,320 model fits. Agent A independently calculated the same result.

- Expected/found partition files: 4,320 / 4320
- Expected/found Parquet records: 4,320 / 4320
- Repeats parsed: 4320
- Pairwise stability comparisons: 62,640 = 72 × 435 × 2 modes
- Failed fits: 0
- Malformed/status/metadata/size/index/split errors: 0
- Missing expected artifacts: partitions 0; records 0
- Cross-method/mode split mismatches: 0; unique row splits per cohort: 30
- Maximum cell errors versus stored summary: stability 1.11e-16; ARI 9.71e-17; null stability 9.92e-17.

All 72 cells matched at floating-point precision. Mean stability=0.5165860621; mean external ARI=0.0523121822; mean cell gap=0.4642738799; median cell gap=0.4484068169; mean null stability=0.0066196808. The gap is computed as each cell's mean of 435 pairwise intersection ARIs **minus** that cell's mean of 30 label ARIs, then equally averaged over 72 cells. The median is the median of those 72 cell gaps. Because the design is balanced, equal cell weighting equals equal dataset-first or method-first weighting. It is not a general calibrated “excess reproducibility” score.

The two cell summaries are matched at cohort, method and split protocol because they use the same 30 assignments. They are not one-to-one repeated observations: stability contains 435 dependent pair values and ARI contains 30 per-repeat values. The pairwise values reuse the same partitions and overlapping samples.

## Authenticity and duplicate findings

The files are internally consistent, not cryptographically authenticated as the original execution. Run rows do not store cache SHA, input path, sample IDs or source commit. Six ignored `data/cache/*.npz` copies are byte-identical to tracked FYP reference copies under `experiments/exp3_real_world_benchmarks/data/cache/`; this establishes a recoverable cache version but does not attest which cache bytes each fit loaded.

Across 4,320 partition files there are 4,169 distinct binary hashes: 140 duplicate-hash groups affect 291 files (151 excess copies). Parquet records have zero duplicate binary hashes. Three duplicate groups cross real/null or method/mode outputs: CNS CoHiRF real/null repeat 17 (identical one-cluster-vs-47 labels); Prostate CoHiRF-null/CoreHalo-real repeat 5; Prostate StdCons-null/UngatedAC-real repeat 16. They are suspicious and require provenance/root-cause explanation; exact label identity alone does not establish corruption.

## Weighting and conditional subsets

All 72 cells: gap mean .464274, median .448407. The 60 cells passing the post-hoc non-degeneracy screen have cell-weighted gap mean .485376 and median .464041. The 18 cells satisfying Rule(i′) across any method have means stability .720011, ARI .003873, gap .716138; that is **not** the manuscript's different “18 cells” shorthand. The manuscript's .638304 stability and .045733 ARI are the 18 cohort×method cells for the three recurrent methods FCAG/FCM/FastMVC across all six cohorts. Nine Rule(iii)-recurrence cells are listed in `nine_cell_final_verification.csv`; their mean stability .683764, ARI −.002853, gap .686617, median gap .666136.
