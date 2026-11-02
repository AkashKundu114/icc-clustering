# Reproducibility assessment for the public repository candidate

## Tier 1 — Aggregate reproduction: PASS (narrow)

Loop 6.0 tested the exact baseline commit `5dac3762f34b756a1047e099b4465c8a1954daad` in a fresh shallow clone on Windows 11 / Python 3.14.6 with no non-standard dependencies. Command: `python audit/loop5_6/minimum_aggregate_package/reproduce_aggregate.py`; exit code 0. Output SHA-256: `538f5e9ce1026689eebef5fb8a79126e82c946be269c6a82afd03a4a45cfa9a5`. It reads a tracked 72-row aggregate CSV. It is an arithmetic consistency check only, not reproduction of raw evidence or all tables/figures.

## Tier 2 — Partition-level reproduction: UNAVAILABLE

Fresh clone lacks `results/stability/partitions/`, `results/stability/runs/`, and `data/cache/`. No command can recompute 30-draw external ARIs and 435 intersection ARIs from the public snapshot. The local FYP recovered files are not tracked or released.

## Tier 3 — Full experimental reproduction: NOT RUN

No authenticated historical partition producer, complete source/input/configuration chain, or authorized dataset bundle is available. No model fits were run in Loop 6.0.

## Current public candidate

Until a reviewed public-snapshot commit exists, the live repository's current baseline still contains historical `audit/` files in its Git tree. `.gitignore` cannot hide already tracked files. A future snapshot removal and clean-clone test must occur before calling the reorganized repository public-release-ready.
