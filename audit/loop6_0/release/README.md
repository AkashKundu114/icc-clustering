# ICC clustering reproduction status (Loop 6.0)

This directory documents what a reviewer can currently reproduce from the public repository. It is not a complete reproduction archive.

## Immutable source

The Loop 6.0 clean-clone check used commit `5dac3762f34b756a1047e099b4465c8a1954daad`. Verify the clone with `git rev-parse HEAD`.

## Tier 1: aggregate arithmetic (supported)

Requirements: Python 3.14.6 was used in the audit; the script relies on the standard library. From the repository root run:

```powershell
python audit/loop5_6/minimum_aggregate_package/reproduce_aggregate.py
```

Expected stdout has 72 aggregate rows, 6 datasets, 12 methods, mean stability 0.5165860620823638, mean external ARI 0.0523121821722892, mean gap 0.46427387991007457, and median gap 0.44840681694162077. These are aggregate-level descriptive calculations, not repeated-run reconstruction.

## Tier 2: partition-level verification (not available)

The public clone does not contain the feature caches, stable sample-ID mapping, 4,320 partition arrays or 4,320 per-fit Parquet records. A local copy in the FYP worktree is not a public release and cannot be acquired through this README. The required source-specific redistribution/privacy review remains incomplete. Therefore this tier is **not reproducible from the public repository**.

## Tier 3: full experimental reproduction (not available)

The historical partition writer, complete authoritative experiment configuration and execution lineage were not recovered. No original fit producer is provided here. Do not treat a future prospective run as a rerun of the historical experiment.

## Data acquisition and rights

No raw or processed third-party datasets, caches, partitions, sample identifiers or run-level data are bundled here. See `data_rights_matrix.csv` for source URLs and unresolved rights. Acquire datasets from their upstream providers, check dataset-specific current terms, cite the sources, record version/retrieval date, and compute local hashes. Yale B must not be redistributed without written permission. The Zheng68K/PBMC68k benchmark variant must be identified before acquisition instructions are treated as exact.

## Reproduction claims

Only Tier 1 was executed successfully in a fresh clone and empty Python environment. Tier 2 is unavailable due missing inputs. Tier 3 was not run. No badge or full-reproduction certification is claimed.
