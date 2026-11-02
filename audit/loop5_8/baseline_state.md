# Loop 5.8 baseline state

Recorded before Loop 5.8 deliverable creation/modification (2026-11-02 local time; Asia/Calcutta).

- Target repository: `D:\icc-clustering`, branch `main` tracking `origin/main`.
- `git fetch origin` completed. Both local `HEAD` and fetched `origin/main` were `29bcc279589d4a6c1e6747885cc857085ac8d6d0`, timestamp `2026-11-02T17:13:17+05:30`, subject `5.7`.
- Initial tracked working tree was clean. After baseline inventory creation, only `audit/loop5_8/` is untracked; no existing source, manuscript, dataset, result, or history files were changed.
- Ignored local paths include `data/cache/`, `data/raw/`, `paper/`, `results/`, the Loop 5.6 aggregate ZIP, build/cache directories. `git status --ignored` confirmed these are not a clean-clone guarantee.
- The target repository does not track `paper/manuscript/main.tex`; that path is absent locally. Therefore there is no target-repository manuscript SHA to report.
- The accessible separate project directory is `D:\Final Year Project`; branch `research/dami-revision`, HEAD `60b163f22b5931da35a1ace07d1934bf3bdd65e3`, timestamp `2026-11-01T16:25:40+05:30`, subject `feat(submission): complete Gates G3-G5 DMKD manuscript integration and submission audits`; it tracks `icc-remote/research/dami-revision`. This is a separate worktree/repository and not evidence of target `origin/main` contents.
- The current FYP manuscript candidate `D:\Final Year Project\paper\main.tex` has SHA-256 `BB09E87B34E529E3D8CA83BBF69BDFBBCB57AEDF75B2BC3BB49D6336A7911C53`. It contains many additional sections and confirmatory claims beyond the earlier Loop 5.7 reviewed draft. It is not substituted for the missing target manuscript.
- `baseline_audit_inventory.csv` records file names, byte lengths and modification times for Loop 5.6/5.7 before new outputs. Existing Loop 5.6/5.7 files were read-only inputs.
- Available local stability artifacts are under `D:\Final Year Project\results\stability`; the prior Loop 5.7 script/output set is under target `audit/loop5_7/`.

This audit's future execution identity is the current baseline commit plus local, uncommitted Loop 5.8 scripts and outputs. No new execution or deliverables commit exists at baseline.
