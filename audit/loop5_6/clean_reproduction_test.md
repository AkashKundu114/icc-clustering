# Clean reproduction test

The aggregate-only ZIP was extracted to a fresh temporary directory and its standard-library script executed without relying on developer caches. It successfully recomputed the listed 72-cell aggregate metrics (test evidence: `clean_reproduction_test.json`). This is a scoped clean reproduction of summary arithmetic only.

A clean-clone reproduction of the original experiment was **not** achieved: clone lacks ignored caches, all 4,320 partition arrays, all 4,320 per-fit records, and upstream acquisition/preprocessing identity. No complete environment lockfile and input hashes tied to run records exist. Consequently dataset acquisition, hash validation, fit rerun, output comparison cannot be completed. Do not describe the full analysis as publicly reproducible.
