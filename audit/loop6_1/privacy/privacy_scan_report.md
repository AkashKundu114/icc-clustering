# Public repository privacy and private-material scan

## Scope and method

Reviewed 484 paths from `git ls-files`, the full current `git status --ignored --short` output, the local top-level tree, `CITATION.cff`, `.env.example`, README/docs, workflows and source/config/scripts. Pattern-scanned tracked public-facing source and documentation for Windows user paths, Unix home paths, credential-like strings, private-key headers, passwords, API keys and secrets. Used `git ls-files` path/extension searches for manuscript and submission materials.

## Findings

- **Tracked manuscript/publication source:** none found among tracked paths with `.tex`, `.bib`, `.pdf`, `.docx` extensions or under `paper/`, `manuscript/`, `submission/`, `reviewer-responses/`, `supplementary-private/`. The private local `paper/` directory is ignored. Do not add its contents to public docs or metadata.
- **Tracked internal audit material:** 335 tracked `audit/` files. These include internal reports and manuscript claim analyses. They remain publicly present on the current Git branch until a future explicit removal commit; `.gitignore` alone cannot conceal them. The complete list is in `baseline/tracked_private_files.csv`.
- **Tracked raw data and results:** five tracked files in `data/`/`results/`, all registry/README/placeholder-style; no cohort matrices or scored result outputs were tracked. Ignored local `data/cache/`, `data/raw/`, and `results/` exist and include private research artifacts.
- **Local paths / personal data / credentials:** no obvious credentials, private key, or local Windows/home path patterns were found in tracked public-facing README/docs/source/config/test files. One scan match was an upstream URL containing `/home/dengcai/` in a Yale B downloader source; it is a web path, not a local user path. The internal tracked audit tree contains paths, author identity and private research context; this is one reason it should be removed from future public-release snapshots. No credentials were printed.
- **Citation metadata:** inspect `CITATION.cff` separately before rewriting; keep only verified contributor names/ORCID/software metadata. Do not add manuscript title or manuscript-source details there.
- **Publication privacy:** no manuscript content was copied into these privacy findings. No private worktree path should be used in public docs.

## Recommended exclusions

Keep `audit/`, `paper/`, `manuscript/`, `submission/`, reviewer files, `data/raw/`, `data/cache/`, result caches and local environments out of future public snapshots. Preserve the private research source and audit history in its current local environment. `audit/` is currently tracked (335 files), so use the explicit removal plan rather than relying on ignore rules.

## Limitations

This is a pattern and path scan, not a formal secrets scanner, a human-subjects privacy review, or a complete license audit. It does not guarantee that no sensitive information exists in all public source/history. Git history was not rewritten or scrubbed, and no push occurred.
