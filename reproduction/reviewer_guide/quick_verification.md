# Reviewer guide: saved-output arithmetic checks

This workflow verifies calculations only after the reviewer has lawfully obtained the exact saved inputs. The repository does not provide those inputs, and this guide is not evidence that a public clean clone can reproduce the paper's results.

**There is currently no configured public archive or controlled reviewer-access route for these inputs. A reviewer with only the public repository cannot reproduce the numerical results. The authors need to establish a lawful evidence-access route before claiming reviewer reproducibility.**

## Required inputs

For the six-cohort check, obtain the six cohort NPZ caches, all 4,320 partition NPY files, all 4,320 per-fit Parquet files, and the historical aggregate CSV from the authors through a permitted route. Confirm that the provider terms allow access and processing. The verifier assumes each saved partition row index maps to the same row in its cohort cache; the cache has no stable upstream sample identifier that independently proves this mapping.

For the 13-dataset score check, obtain both historical score CSVs with `dataset`, `model`, `seed`, and `ari` columns. The checks reproduce summary arithmetic; they do not validate that every score came from a fair, independent, successful fit.

## Environment and commands

From a fresh clone, install the project and verifier dependencies:

```powershell
python -m pip install -e .
python -m pip install pyarrow scipy
```

Then run each verifier to a new empty output directory:

```powershell
python reproduction/scripts/recompute_saved_stability.py `
  --data-root <authorized-evidence-root> `
  --output-dir <new-output-directory>
```

```powershell
python reproduction/scripts/recompute_benchmark_scores.py `
  --scores <pass-f-scores.csv> <cohirf-scores.csv> `
  --output-dir <new-output-directory>
```

Each tool writes recalculated CSV/JSON outputs and dynamically computed SHA-256 manifests. To test integrity checking, provide an expected-hash JSON with a deliberately incorrect digest; the command must fail and report the mismatch. Never use expected hashes copied from an unauthenticated report as proof of source identity.

## Expected checks

The six-cohort tool expects a 6 × 12 × 2 × 30 partition grid, matching Parquet records, matching sample counts and repeat seed/split structures, and 435 pairwise intersection comparisons per cell and mode. It recomputes external ARI and stability from supplied files. Outputs are `recomputed_cells.csv`, `recomputation_summary.json`, and `output_manifest.json`.

The summary distinguishes (a) cells passing the post-hoc 5% minimum-cluster
fraction in at least 27 of 30 repeats, (b) cells passing the original numeric
stability/ARI screen, and (c) their intersection. The repeat-level screen also
requires predicted K to be at least the number of reference classes, so it is
label-informed. These selections are exploratory and are not confirmation.

The benchmark tool reports score cell summaries, ranks, tie-corrected Friedman arithmetic, missing/duplicate keys, zero scores, and hashes. Outputs are `benchmark_cell_summary.csv` and `benchmark_recalculation.json`.

Compare outputs to the authors' cited archived values, then inspect all reported mismatches. The tools do not infer a corrected experiment definition from output values.

## What this does not verify

- The historical experiment producer or execution commit.
- The exact source identity and ordering of cached cohort samples.
- Whether the recorded null transformation was actually applied.
- Whether historical method implementations or benchmark comparisons were fair.
- Fresh model fits or initialization robustness.
- Public reproduction from the repository without author-provided inputs.

For those reasons this is an archived-output arithmetic check, not full experimental reproduction. A publication claim of public reproducibility requires a rights-cleared input/archive or a lawful reviewer-access arrangement and a successful clean-clone test using only that access route.
