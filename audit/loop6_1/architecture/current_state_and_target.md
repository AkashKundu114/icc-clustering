# Repository architecture and public-release plan

## Observed tracked architecture

Baseline commit `5dac3762f34b756a1047e099b4465c8a1954daad` tracks 484 files. Top-level tracked path counts: .editorconfig: 1, .env.example: 1, .gitattributes: 1, .github: 6, .gitignore: 1, CHANGELOG.md: 1, CITATION.cff: 1, CODE_OF_CONDUCT.md: 1, CONTRIBUTING.md: 1, Dockerfile: 1, LICENSE: 1, Makefile: 1, README.md: 1, SECURITY.md: 1, SUPPORT.md: 1, audit: 335, configs: 7, data: 5, demo.py: 1, docs: 8, examples: 7, pyproject.toml: 1, requirements-lock.txt: 1, requirements.txt: 1, scripts: 6, src: 70, tests: 22. The tracked software already has a usable package layout (`src/icc`, `src/cicc`), seven YAML configurations under `configs/`, scripts, tests, examples, existing researcher docs, GitHub workflows and standard project metadata. Source imports and test paths rely on the existing `src/` layout; moving package modules or tests is not warranted in this documentation phase.

The tracked repository currently has 335 files under `audit/`, including historical audit reports from prior loops. It tracks no manuscript extensions (`.tex`, `.bib`, `.pdf`, `.docx`) and no paths under `paper/`, `submission/`, `manuscript/`, or reviewer correspondence. Local ignored `paper/` and untracked Loop 6.0 artifacts exist in the research workspace and must remain private. The current root `.gitignore` already excludes `paper/`, `submission/`, `manuscript/`, LaTeX/bibliography files, raw/cache data, result outputs and local environments; it does not exclude `audit/`.

Only five tracked files are under `data/` or `results/`: placeholders/registries and README/ignore files; no tracked data matrices, results tables or figures were found in those directories. This is consistent with Loop 6.0's finding that partition-level results are not publicly reproducible.

## Recommended public architecture

Keep the current package/module paths to avoid import breakage. Add independently written documentation in `docs/` (without manuscript text), keep `configs/`, `scripts/`, `src/`, `tests/`, and `examples/`, and publish only verified, rights-cleared aggregate outputs with an explicit provenance manifest. Retain the existing `data/` placeholders and acquisition instructions; do not add restricted caches. Add `audit/` to `.gitignore` for future new files, but stage removal of its already tracked history only in a deliberate public-release commit after an internal backup is verified. Do not move internal history into public `docs/`.

No `paper/`, `manuscript/`, or `submission/` directory should appear in the public release. The private manuscript and publication lifecycle remain in the separate research workspace; no move was performed because current paths/dependencies are not being restructured here.

## Git workflow and compatibility checks

- `git ls-files`: 484 paths; 335 tracked audit paths.
- `.github/workflows/ci.yml` and existing `src/`, `tests/`, `configs/`, `scripts/`, and `examples/` paths were inspected. The proposed documentation-only changes need not change their import paths.
- No module relocation is recommended. The exact private tracked-file list and release treatment are in `baseline/tracked_private_files.csv`.
- `.gitignore` matching is not removal: all 335 tracked `audit/` files remain in the Git tree until a future commit explicitly removes them. Never rewrite history.
