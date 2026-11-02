# Tracked private/internal material removal plan

## Findings

At baseline, 335 files under `audit/` are tracked in the current public Git history. The tracked `audit/` tree includes scientific audit reports, claim ledgers, raw-result reconciliation, code traceability, manuscript revision/adversarial reports, reproduction records and internal findings. A recursive `git ls-files` search found no tracked manuscript `.tex`, `.bib`, `.pdf`, `.docx` files or tracked `paper/`, `submission/`, `manuscript/`, `reviewer-responses/` directories. Tracked file paths are enumerated in `../baseline/tracked_private_files.csv`.

## Safe future public-release procedure

1. Preserve the complete internal `audit/` tree in the existing private research environment and verify its baseline checksum inventory.
2. Add `audit/` to `.gitignore` so new audit material is not accidentally added. This does not untrack the 335 existing paths.
3. Before any public-release commit, create a separate review branch and explicitly stage removal of the tracked audit tree from that branch's next snapshot (for example, `git rm --cached -r audit/` after confirming the local private copy and a backup). This leaves working files available locally; verify the local audit tree remains intact.
4. Inspect `git diff --cached --name-status`, `git ls-files`, `git status`, and a fresh clone of the candidate branch. Verify no audit paths or manuscript/submission artifacts are present.
5. Do not force-push, rewrite, filter, or delete earlier Git history. Prior commits remain historically accessible; if historical exposure is unacceptable, a separate repository and a reviewed migration strategy are required.
6. Do not publish/push or create a release without the user's explicit approval.

No files were untracked, moved, deleted or staged by this audit. The public `main` currently continues to include the audit history because these files are tracked.
