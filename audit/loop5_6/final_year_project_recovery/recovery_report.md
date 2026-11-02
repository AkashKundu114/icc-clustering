# Final Year Project evidence recovery report

## Search scope

Recursively enumerated `D:\Final Year Project\`, including hidden and nested directories. The scan covered 16,724 files totaling 1,798,500,138 bytes at execution time, including `.git`, `.venv`, result trees, submissions, and caches. Filename/path triage and text searches targeted six cohort names and stability, subsampling, partitions, assignments, seeds, null controls, tables, and protocols. Candidate evidence was then opened and parsed. `file_inventory.csv` includes the full tree; `hash_manifest.csv` records SHA-256 for evidence candidates and supporting files.

## Material recovery

The folder contains a complete local six-cohort real/null subsampling artifact grid:

- 4,320 partition files (`results/stability/partitions/*.npy`): 6 cohorts × 12 methods × 30 repeats × 2 modes.
- 4,320 per-fit Parquet records (`results/stability/runs/*.parquet`), with the same grid.
- Six preprocessed X/y cache files, each with only `X` and `y`, no sample identifiers or embedded preprocessing/input hash.
- The 72-row `subsample_stability_summary.csv` and a separate 133-row legacy full-data seed summary.
- Historical `PLAN_STAB.md`, `scripts/stability_subsample.py`, and `scripts/audit_degeneracy.py` recoverable from Git history.

The exact experiment commit is `49f3882fe5385913a9af1a5b89138c6ae6d95579` (2026-10-29 15:33:36 +05:30) in the separate `Final Year Project` Git repository. Its commit tree contains the protocol, original stability script, and a tracked 72-row summary. The protocol’s initial commit is `330738037fcb7f4ec8537581051b856a63c2b0d5`; amended Rule (i′) is `548d68d54bb42bac76f20908cda1ae9a671e5b60`. The run/partition files and caches are local ignored artifacts, not in that commit. Parquet and partition metadata do not contain the X/y hash, sample IDs, or preprocessing provenance. Therefore the experimental outputs are structurally complete and numerically consistent, while byte-level linkage between the saved experiment and the exact input cache remains unverified.

The six caches in `D:\Final Year Project\data\cache` are byte-identical to the six local caches in `D:\icc-clustering\data\cache`. Each matches expected N, D, K and class counts; exact duplicate rows and nonfinite X values were zero. This establishes consistency between two local copies, not upstream sample identity. No raw source matrices for the six cohorts or stable sample IDs were found in the folder.

## Independent recalculation

The audit parsed all run records and partitions, verified mode, method, cohort, repetition and seed metadata, confirmed all 30 real and 30 null partitions per cell, and recomputed 30 external ARIs and 435 intersection ARIs for each cell and mode. The same split indices were used across methods and real/null modes for each cohort/repeat. Every run record reports success. Recomputed accuracy agrees with each saved real-fit accuracy exactly at stored precision; all 72 real stability, external ARI, and null-stability aggregate rows match the saved summary to floating-point error (maximum discrepancy about `1.1 × 10⁻¹⁶`). The audit produced 62,640 pairwise stability rows plus a 4,320-row per-repeat ledger.

Recomputed across the 72 dataset–method cells:

- Mean stability: **0.5165860621**.
- Mean external ARI: **0.0523121822**.
- Mean gap (`cell stability − cell mean ARI`, then equal-weight mean): **0.4642738799**.
- Median of 72 cell gaps: **0.4484068169**.
- Mean independently recomputed permuted-null stability: **0.0066196808**.

These are now independently reconstructed from saved partitions and run records, rather than merely re-averaged from an aggregate CSV. They still describe six selected cohorts and fixed method configurations; they do not establish a broad population-level law. The audit did not rerun the 4,320 model fits.

## Nine-cell subset

The 20 stored Boolean flags implement Rule (i): stability ≥ 0.50 and mean external ARI ≤ 0.05. Recomputing per-repeat smallest-cluster size with the original degeneracy script’s missing-target-cluster handling leaves 18 Rule (i′) cells; the two excluded prostate cases are CoreHalo (one observed cluster throughout) and CoHiRF (degenerate in 60% of repeats). The protocol’s Rule (iii) looks for at least three methods meeting the cohort recurrence threshold. FCM, FCAG, and FastMVC each meet Rule (i′) on three cohorts; their nine listed cells are recoverable from the partition-level data and match the claimed means: stability 0.6837644, ARI −0.0028530, mean gap 0.6866174. The median of these nine cell gaps is 0.6661357.

The nine are a criterion-conditioned descriptive subset, not all 18 Rule (i′) cells and not an independent confirmation. Rule (i′) was amended after seeing the CoreHalo prostate collapse. Keep it only with that post-hoc status and the complete 18-cell/non-degenerate results alongside it.

## Verdict

**Recovered:** exact historical protocol and script, preprocessed local X/y inputs, all six cohorts’ 30 real/null partitions, all 4,320 per-fit records, summary artifacts, and table-generation/audit materials. The 72-cell calculations and the nine named cells can now be reconstructed at repeat/partition level from the local evidence.

**Still missing or unresolved:** upstream-identified raw matrices, stable sample IDs, input/preprocessing hashes embedded in runs, proof that current caches are byte-for-byte the exact original fit inputs, a publicly available archive containing partitions/runs, and license clearance for redistributing third-party data. The original numerical finding is reproducible from the recovered local experimental outputs, but a clean independent reproduction of the underlying experiment is not currently available from a fresh clone.
