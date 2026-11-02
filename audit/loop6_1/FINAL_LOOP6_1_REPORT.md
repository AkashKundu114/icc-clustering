# Loop 6.1 final report

## 1. Baseline repository state

Baseline was captured before edits at commit `5dac3762f34b756a1047e099b4465c8a1954daad` on `main` (2026-11-02 18:16:35 +05:30). The initial worktree was clean except for a pre-existing untracked `audit/loop6_0/` directory; there were no submodules. Exact baseline inventories and checksums are under `baseline/`.

The audit found 484 tracked paths, including 335 tracked internal audit files. No manuscript sources, submission PDFs, or reviewer correspondence were tracked at the baseline tip. A separate FYP checkout was present at `D:\Final Year Project`, branch `research/dami-revision`, commit `60b163f22b5931da35a1ace07d1934bf3bdd65e3`; it was not treated as identical to the public checkout. The private manuscript remained outside tracked candidate files. No private manuscript content or identifying private path/hash is included in public documentation.

## 2. Loop 6.0 evidence consumed

The final Loop 6.0 report was available and concluded HOLD. Its local reconstruction reported six cohorts, 12 method labels, 72 cells, 30 draws, mean stability 0.5165860621, mean external ARI 0.0523121822, mean cell gap 0.4642738799, median gap 0.4484068169, and null stability 0.0066196808. These are not promoted into public docs: the historical producer was not authenticated, derived artifacts were not cleared for redistribution, and underlying data/partitions were absent from the public clone.

The Loop 6.0 public evidence status was: Tier 1 arithmetic checker had passed on a prior snapshot but its input/script were inside internal audit; Tier 2 unavailable; Tier 3 not run. Dataset rights remained uncleared, especially Yale B. The 13-dataset external-ARI benchmark is a distinct experiment and is not described as a stability analysis.

## 3. Public architecture and files changed

A local branch `codex/loop6_1-public-candidate` was created. Candidate commit `78a4b025ff152157736f7fff6002e0fb55f19e26` adds the documentation/release snapshot. A follow-up commit `356173c258e540bc92eb3f5783f0269fc290d6f2` restores validated literature references required by an existing regression test, without restoring unsupported formal guarantees.

The root source paths were preserved. New docs explain research scope, methods, access restrictions, result status, statistical limitations, reproducibility, software layout, and practical questions. README was rewritten without manuscript text or numerical result claims. `.gitignore` now excludes future audit/private paths; because ignore patterns do not untrack files, the candidate snapshot explicitly removes the 335 tracked audit files from its index. Files remain physically present in the internal worktree (624 files including ignored Loop 6.1 artifacts), and no Git history was rewritten.

## 4. Manuscript and audit exclusion

At candidate HEAD, the clean clone has zero tracked `audit/` paths, zero manuscript/submission-like paths, and zero `.tex`, `.bib`, `.pdf`, or `.docx` files. Earlier Git commits still contain historic audit files. No push was made; public GitHub remains at the baseline remote state. A future release owner must decide how to handle historic exposure; the no-history-rewrite constraint means this candidate removal alone does not erase it.

The private manuscript was not copied, edited, summarized verbatim, or built. Audit history remains in the original local workspace and is ignored going forward.

## 5. Dataset rights and citation/licensing

`docs/datasets.md` covers all 13 registry variants and distinguishes configured dimensions from source-verified dimensions. It records cautious access and attribution notes from the internal reassessment and instructs users not to redistribute unverified variants or derivatives. Yale B images are not to be repackaged without permission. The MIT license is explicitly scoped to software, not datasets.

The software release metadata is not fully reconciled: `pyproject.toml` and `CITATION.cff` say 2.2.0, while the changelog begins with 2.2.1. CFF identifies the tagged 2.2.0 release and names the package author currently declared in pyproject; complete contributor authorship/consent metadata was not independently verified. This is a release blocker to resolve before tagging. No DOI was invented.

## 6. Reproducibility

Public docs accurately state that no result package is included. Tier 1 is unavailable in this snapshot (previously tested materials were internal); Tier 2 unavailable; Tier 3 not run. Installation/synthetic API quickstart does not claim to reproduce research findings. Dataset acquisition is not tested because rights and exact variant identity are unresolved.

The fresh clone was created at `D:\loop6_1_clean_clone`, HEAD `356173c258e540bc92eb3f5783f0269fc290d6f2`. It had no audit/manuscript artifacts. Local Markdown links resolved (19 files; 0 missing) and no explicit internal loop/path references were found. An initial test run on the first candidate commit exposed one test regression: six required background citation identifiers were missing from `docs/theory.md`. Corrected references and cautious scope were committed in the follow-up. The final clean-clone `python -m pytest -q` exited 0 after one earlier documentation regression was corrected. `python -m pip install --no-deps -e .` also succeeded; both used the pre-existing Python 3.14.6 environment, not a fresh virtual environment. Exact output is recorded in `validation/clean_clone_validation.log`.

## 7. Security, privacy, and public artifact checks

The independent privacy review found no credential or private local path issue in the reviewed tracked public docs. The clean snapshot contains no manuscript/submission file patterns. `public_file_manifest.csv` and `public_artifact_checksums.sha256` are computed from actual tracked candidate bytes. `private_exclusion_manifest.csv` records the candidate exclusions and any pattern matches.

No results, data, caches, partitions, or derived sample-level artifacts were added. Candidate result data are absent because provenance and rights were not cleared.

## 8. Independent public-release review

An independent reviewer checked docs, ignore behavior, tracked paths, candidate scope and metadata. The reviewer found cautious scientific wording and no checked local-link breakage. The reviewer conclusion was PUBLIC-RELEASE BLOCKED because of tracked audit exposure before this candidate tip, continuing exposure in earlier Git history, and inconsistent release metadata. The reviewer did not run tests or clean clone; lead audit ran the clone checks and tests separately.

## 9. Exact changes and test status

Repository candidate changes: rewrite README; update `.gitignore`, `CITATION.cff`, `data/README.md`, and existing docs; add nine public research/software docs; remove 335 tracked `audit/` paths from the candidate tree while preserving them locally. No production source, tests, manuscript, data, or experimental results were modified.

Test outcomes and exact output are in `validation/clean_clone_validation.log`. The first pytest invocation failed one foundational-reference assertion; the docs were corrected. The final clean-clone test run exited 0, and editable installation without dependency resolution succeeded. No TeX build or fresh dependency environment was attempted.

## 10. Unresolved issues

- Previous public Git history contains tracked audit files and cannot be purged under current no-history-rewrite rules.
- No numerical results package has been rights-cleared and included.
- Tier 1–3 research reproduction is not available from the candidate snapshot.
- Dataset variant identity and redistribution terms remain unresolved for most registry entries; Yale B requires permission for redistribution.
- Package version and release metadata disagree (2.2.0 vs 2.2.1); complete CFF authorship verification is incomplete.
- Full clean-environment dependency installation has not been tested.
- Dataset downloads, result generation and TeX compilation were not run.

## 11. Final public-release verdict

**PUBLIC-RELEASE BLOCKED.** The local candidate is substantially clearer, excludes private artifacts from its current tree, and documents the actual evidence limitations. It is not ready to publish because earlier Git history remains exposed, release metadata is inconsistent, no research-result reproduction tier is available from public materials, and dataset rights are unresolved. Nothing was pushed or released.


Final report prepared against candidate commit 356173c258e540bc92eb3f5783f0269fc290d6f2. Internal outputs remain ignored and local; no changes were pushed or released.

