# Producer search and source trace

## Search executed

Worktree: `D:\Final Year Project`, current branch `research/dami-revision`, HEAD `60b163f22b5931da35a1ace07d1934bf3bdd65e3`. Local ignored partition/run/cache directories were inspected. `git log --all -S` was run for `sub_seed`, `null_seed`, `results/stability/partitions`, and `subsample_stability_summary`; `git ls-files` and recursive text search covered Python, notebooks, Markdown, YAML, JSON, and CSV, excluding binary data/cache/run payloads. Relevant paths, saved inputs and hashes are represented in `duplicate_reaudit.csv` and `audit/loop5_9/provenance/recompute_forensics.py`.

## What the extant code does

- `scripts/run_real_data_stability.py` (including versions at commits `49f3882fe5385913a9af1a5b89138c6ae6d95579` and `5cfd721c28458db7525efe208d33a4a5e07bf91f`) is a **different full-data seed stability experiment**. It calls `load_dataset`, fits each model on full `X`, saves label vectors under `results/stability/labels`, then computes pairwise ARI across seeds. It does not create `sub_idx`, real/null data variants, `results/stability/partitions/*.npy`, or `runs/*.parquet`. Its 30/10 seeds are not the six-cohort subsampling repeats.
- `scripts/audit_degeneracy.py` reads `sub_idx` from existing partition files and computes repeat ARI/pairwise summaries. It is a downstream consumer, not a producer.
- `scripts/make_stability_outputs.py` reads summaries and partitions to make reports/tables; it does not invoke the audited fitting loop or create Parquet run records.
- `scripts/replot_fig2_subsample.py` is plotting/reporting code.
- Search hits such as `experiments/audit_controls/src/e3_label_free_selector.py`, `sensitivity_sweep.py`, and `anchor_fidelity_benchmark.py` use their own local subsample indices for separate analyses. No code in those files writes the exact stability grid or expected Parquet schema.

## Git history result

All-refs history contains stability-summary and consumer-code commits, including `49f3882...`, `5cfd721...`, and cleanup lineage. The tracked path list includes `results/stability/subsample_stability_summary.csv` and `scripts/run_real_data_stability.py`, but no tracked partition/run producer. The additional local `D:\icc-clustering-private-archive` and its `full_branches/dami-revision` copy contain duplicated summaries and consumer scripts, but no partition or Parquet files; token search there likewise found no producer. The archive itself is not a Git worktree, although it contains private Git mirror/bundle directories; those were not extracted or rewritten. Separate `icc-clustering-candidate` and `icc-clustering-fresh-clone` checkouts were also searched and contain only source snippets for unrelated model subsampling, not this partition grid. The local FYP Git status reports `results/stability/partitions/`, `runs/`, and `labels/` ignored. These binary files therefore have no per-file tracked-commit lineage.

## Conclusion

The producer is **not recovered**. A protocol description and a script that computes from a saved partition do not authenticate the process that produced the partition. No execution log, notebook cell, orchestration, subprocess log, temporary checkpoint, explicit null transformation trace, output-write event, or cache-to-fit hash record was located. A full-data seed script cannot be substituted for the missing subsampling producer.
