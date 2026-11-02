# Authoritative Loop 5.8 audit workflow

## Source hierarchy and commit roles

1. Original feature caches and local saved partitions/Parquet rows are direct bytes but local-only; hashes identify files, not the historic fitting event.
2. Original tracked protocol/code commits are lineage evidence only. Target baseline code-under-audit: `313e1542d524ddd2b38fa8c7e2ae885f9c52b7ca` (per Loop 5.7). The local FYP checkout head is `60b163f22b5931da35a1ace07d1934bf3bdd65e3`; neither is established as experiment execution commit.
3. Loop 5.7 `scripts/independent_reconcile.py` is the independent partition metric reconstruction used for the existing 72-cell outputs. It reads a hardcoded `D:\Final Year Project` path and writes into `audit/loop5_7`, so run only on a disposable copy when reproducing historical outputs; do not run it as a Loop 5.8 finalizer.
4. Loop 5.8 scripts under `scripts/` separately perform bootstrap reconciliation, duplicate forensics, and benchmark provenance inventory. They are audit-only. Raw historical files remain read-only.
5. Loop 5.8 generated reports and CSV/JSON artifacts are reconstructed evidence. The final manuscript commit is unavailable: `paper/manuscript/main.tex` is not tracked/present. The FYP branch's manuscript SHA is recorded in `baseline_state.md` and is a different local candidate.
6. Original execution identity: **UNVERIFIABLE**. Loop 5.8 reconstruction/audit execution identity: baseline commit `29bcc279589d4a6c1e6747885cc857085ac8d6d0` plus uncommitted scripts and local-only inputs. Loop 5.8 final deliverables commit/public release commit: **NONE**.

## Safe execution order

1. Verify `git status`, fetch remote, record target commit. Do not run on a dirty source tree except for the new audit directory.
2. Validate local root and expected inputs: six `data/cache/{cohort}.npz`, 4,320 partitions, 4,320 Parquet rows, source aggregate, benchmark CSVs and exact manuscript candidate. Fail if required files are absent; never substitute summaries for raw runs.
3. Hash every input dynamically and record path, size, hash, repository/commit if tracked, and artifact class.
4. Run `python audit/loop5_8/scripts/partition_forensics.py` (read-only partition census) and `python audit/loop5_8/scripts/bootstrap_estimand.py` (aggregate-cell cohort bootstrap only). Run benchmark inventory only against explicit FYP checkout.
5. Run the Tier 1 package `python audit/loop5_8/reproduction/scripts/reproduce_aggregate.py`. This package is separate and aggregate-only.
6. Compare scripts' outputs and prose/JSON/CSV; fail release QA on contradictory displayed values. Do not run Loop 5.6 `reconstruct_loop5_6.py` after partition reconstruction; it writes aggregate-only outputs to the same names.
7. Generate manifests/checksums after all reports are final. Hash source files dynamically. Exclude the checksum file itself from its own checksum list; verify every listed digest.
8. Run from a fresh clone of the intended immutable release commit. Tier 1, Tier 2, Tier 3 results must be reported separately.

## Determinism and limitations

Partition hash census and metric recomputation are deterministic for fixed bytes and library versions. Bootstrap intervals are deterministic per seed and code; changing seed/RNG call order changes endpoints. Inventory timestamps and absolute paths are environment-specific, so whole-report byte identity is not promised. The 5.8 outputs record the execution snapshot. The local recovered evidence is not publicly available, and generator provenance, run-to-input hashes and full refit are not established.

No production code, historical audit output, dataset, manuscript, or Git history was changed. No commit was made.
