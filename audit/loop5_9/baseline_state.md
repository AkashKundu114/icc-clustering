# Loop 5.9 baseline state

Captured after `git fetch origin` and before any Loop 5.9 evidence analysis or deliverable generation.

## Repository identity

- Target: `D:\icc-clustering`, branch `main` tracking `origin/main`.
- Target baseline `HEAD` and fetched `origin/main`: `d0c4665af327ec284d931c94f9658309ec13763c`.
- Commit timestamp: `2026-11-02T17:36:12+05:30`; subject `Loop 5.8`.
- Initial tracked working tree: clean (`main...origin/main`, no status entries).
- `git ls-remote --heads origin` showed only `refs/heads/main` at the same SHA. Existing tags: `v1.0.0`, `v2.0.0`, `v2.1.0`, `v2.2.0`.
- Ignored/untracked research paths were recorded with `git status --ignored`: `paper/`, `results/`, `data/raw/`, `data/cache/`, `audit/loop5_6/minimum_aggregate_package.zip`, build and Python cache directories. These are not in a fresh clone by virtue of their local presence.
- The separate local FYP repository remains at branch `research/dami-revision`, commit `60b163f22b5931da35a1ace07d1934bf3bdd65e3`; its remote is `icc-remote`. This is not the target origin/main tree.
- No original stability experiment execution commit has been identified. Loop 5.6/5.7 protocol, source and artifact commits are not treated as execution attestations.

## Manuscript identity and files

The public target Git tree does not track `paper/`. However, the local ignored target workspace contains a canonical submission workspace per `paper/README.md`:

- `paper/manuscript/main.tex`, SHA-256 `A0C4274EC5DFBB40311D3D33D7AD8179B17DEE145851FD2E5B255E498054E75F`.
- Its local README calls it the canonical DMKD source, references `numbers.tex`, `references.bib`, generated tables and figures, and says it was copied from a private archive with the same SHA. It remains ignored/untracked, so there is no target Git commit binding it to the baseline.
- `paper/archive/main_dami_revision_historical.tex` SHA-256 `BB09E87B34E529E3D8CA83BBF69BDFBBCB57AEDF75B2BC3BB49D6336A7911C53`; this matches the separate FYP `paper/main.tex` byte-for-byte and is not the current canonical target source.
- The unmanaged local directory `D:\icc-clustering-private-archive` is not a Git repository, but contains `paper/main.tex` and `springer_manuscript/main.tex` with SHA-256 `A0C4274EC5DFBB40311D3D33D7AD8179B17DEE145851FD2E5B255E498054E75F`, byte-identical to the target canonical local source. Its `paper` tree has summary/consumer code and publication assets, but Agent A found no stability partition/Parquet producer or run binaries there.
- Separate FYP candidate: `D:\Final Year Project\paper\main.tex`, SHA-256 `BB09E87B34E529E3D8CA83BBF69BDFBBCB57AEDF75B2BC3BB49D6336A7911C53`; it is not interchangeable with target `paper/manuscript/main.tex`.
- `manuscript_version_inventory.csv` records 981 available manuscript-adjacent files across target local workspace, FYP and unmanaged private archive (LaTeX, bibliography, figures, tables, submissions, supplementary and related artifacts) with dynamic SHA-256, sizes, timestamps and worktree/tracking context. `target_paper_inventory.csv` is the preliminary local target paper tree listing.

The target local README identifies the intended canonical manuscript candidate, but the file is not version-controlled or frozen in the Git baseline. We therefore review it as the best evidenced intended local source, while submission certification remains blocked until its authors confirm and version it.

## Audit history

The latest committed audit deliverable is Loop 5.8 at the baseline commit above. Previous committed audit commits include Loop 5.7 `29bcc279589d4a6c1e6747885cc857085ac8d6d0`, audit 5.6 `4fd21edaf7e4f45a8bea6acc8a052ad5f55275ba`, and earlier Loop 5.5 `313e1542d524ddd2b38fa8c7e2ae885f9c52b7ca`. The latest Loop 5.6–5.8 artifacts are enumerated in `baseline_sha256sums.txt`; the 5.6–5.8 registers/reports are reconciled in `historical_finding_register.csv`.

At baseline no Loop 5.9 work existed. All subsequent files remain under `audit/loop5_9/`; no production source, historical result, manuscript, Git index, or history was changed. No push/release was made.
