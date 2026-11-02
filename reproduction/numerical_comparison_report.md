# Numerical claim verification status

## Distribution status

This public repository does not publish the numerical values or dataset-derived result tables from the stability experiment or the 13-dataset benchmark. The Loop 6.3 source-specific rights review did not clear the configured datasets, partitions, per-fit records, score tables, or aggregate derived outputs for redistribution. The MIT software license does not apply to those materials. Their values are therefore withheld here until rights are established.

The machine-readable [`claim-to-evidence-matrix.csv`](claim-to-evidence-matrix.csv) identifies which claims were historically reported, which structural checks were performed locally, and what evidence is missing from a public clone. “Locally recalculated” does not mean publicly reproducible. No numerical claim is verified by this report merely because a prior report contains the same value.

## Six-cohort stability experiment

The recovered protocol source is available in public Git history at [commit `49f3882`](https://github.com/AkashKundu114/icc-clustering/commit/49f3882fe5385913a9af1a5b89138c6ae6d95579). This source describes six cohorts, 12 methods, 30 repeats, and real/null modes, with label-stratified sampling and a fixed model seed. The commit documents a protocol and producer implementation; it does not authenticate when or how the historical files were generated.

A complete local run of this protocol was executed on 2026-11-02. The local output files and numerical results are not included because the relevant input and derived-output rights have not been cleared. The run does not authenticate historical execution. Reviewers cannot reproduce either the saved-output calculations or this local run from a clean clone.

The calculation distinguishes mean pairwise ARI over intersections of repeated sample subsets from external ARI against reference labels. The pairwise values reuse partitions and samples and are dependent. Cell-level summaries are nested within six cohorts and shared methods. Any future public numerical report must identify its exact input bundle, output hashes, weighting, missingness, selection rules, and cohort/method scope.

## Separate 13-dataset external-ARI benchmark

Historical saved score files were reaggregated locally with a script that checks file hashes, grid structure, seed-key duplicates, missing cells, and the Friedman calculation. The run did not fit the algorithms again and does not authenticate the saved fit events, copied/imported scores, implementation fidelity, parameter fairness, or ambiguous failure rows. The score inputs and numerical statistics are not included pending rights clearance. This experiment is not a 13-dataset stability analysis.

## Selection analyses

Historical and fresh-run post-hoc selection analyses were recalculated locally from partition assignments. The selection criteria use observed cluster sizes, reference-label-derived K checks, and outcome thresholds. Their numeric summaries and membership tables are not published here because the underlying derived artifacts have not been cleared. No selected subset is independent confirmation; all such analyses must be labelled exploratory if later cleared for publication.

## Verification tools

The public tools `scripts/recompute_saved_stability.py` and `scripts/recompute_benchmark_scores.py` accept researcher-supplied evidence. They dynamically hash inputs, validate structural expectations, and fail on expected-hash mismatch. The clean-clone tests show that these tools cannot run the scientific calculations from this repository alone because the required evidence inputs are absent. They do not recreate model fits or establish a public reproduction pass.

Until source-specific rights and stable input identity are resolved, use the repository to inspect software and protocol code only. Do not cite this package as a complete scientific evidence archive or as proof that the historical or fresh numerical results can be independently reproduced.
