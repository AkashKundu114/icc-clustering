# Provenance verdict

**Decision: reconstructed but not authenticated.** Independent Loop 5.9 code loaded and validated the 4,320 partition files and 4,320 matching one-row Parquet records. It found no malformed payloads, missing Parquet records, multirow records, or non-success status rows. It recomputed 72 cell metrics and 62,640 pairwise values and matched the stored aggregates at floating-point precision.

No producer that writes the audited partition/Parquet schema was recovered in target code, FYP branches/history, current FYP tree, candidate/fresh clone or unmanaged private archive. The extant `run_real_data_stability.py` writes full-data label arrays under `results/stability/labels`; `audit_degeneracy.py` and `make_stability_outputs.py` read existing subsample partitions. Neither is the missing producer.

The full evidence chain is missing at source commit→execution, cache/preprocessing hash→fit, row index→stable sample ID, model invocation→output bytes and output file→Parquet digest. “success” and runtime columns are saved metadata, not independent execution attestation. Therefore none of the 4,320 historical fits can be called authenticated. The current saved bytes support a reproducible local metric reconstruction and bounded descriptive result only.

All 140 duplicate groups remain conservatively `CANNOT CLASSIFY`. Degenerate partitions make several matches plausible, but output reuse or overwrite cannot be ruled out. The Prostate StdCons-null/UngatedAC-real 80/1 match is especially unexplained. These duplicates are across method/mode cells rather than repeated repeats within one cell, so do not mechanically double-count a pair inside a single cell; still, their provenance weakens trust in claimed independent generation.

A prospective protocol is supplied, but a future rerun would be a new experiment and cannot retroactively authenticate these historical artifacts.
