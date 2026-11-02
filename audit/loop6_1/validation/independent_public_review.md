# Independent public-release review — Loop 6.1

## Review scope

Reviewed the current proposed public documentation at the working-tree snapshot based on commit `5dac3762f34b756a1047e099b4465c8a1954daad`, the root `.gitignore`, tracked path inventory, and Loop 6.1 baseline summary. This review did not edit public documentation, execute the package test suite, or inspect the private manuscript. Local Markdown links were checked for existence across `README.md`, `docs/*.md`, and `data/README.md` (19 files); no broken local links were found.

## Findings

### Positive findings

- The README distinguishes resampling stability from external reference alignment and sampling robustness from initialization robustness.
- It clearly separates the six-cohort stability analysis from the 13-dataset external-ARI benchmark.
- It does not publish the prior numerical summary estimates as verified public results.
- `docs/results.md` and `docs/reproducibility.md` state that the result package is absent, Tier 2 is unavailable, and Tier 3 was not run. This matches the Loop 6.0 record.
- Dataset guidance appropriately treats the MIT license as software-only, warns against redistributing uncleared variants, and gives a specific Yale B restriction caution.
- No manuscript copy, manuscript-like prose, local workspace path, or private manuscript checksum was found in the reviewed public-facing README/docs.
- Local links in the reviewed docs resolve in the working tree.

### Release-blocking or material findings

1. **Current tracked snapshot contradicts README layout claim.** The README says there is no internal-audit directory in the current repository snapshot, but the baseline inventory shows 335 tracked files under `audit/`. The new `.gitignore` rule cannot hide already tracked files. This statement only becomes true for the candidate tree after the tracked audit paths are explicitly omitted from its index. Correct the wording or make it conditional on that candidate snapshot, and verify the candidate tree.
2. **Public Git history still exposes internal audit history.** Removing tracked audit files in a new commit will not remove their contents from prior reachable commits. Since rewriting history is prohibited and no push approval exists, this is a documented but material privacy/release blocker for any claim that internal audit materials are not publicly accessible through GitHub history. The candidate can prevent future tip-level inclusion, but not historical exposure.
3. **No numerical findings package is included.** This is an honest disclosure, but it means the repository is currently software documentation rather than a reproducible release of the research results. Tier 1, Tier 2, and Tier 3 are not all available in the public candidate as reviewed; no Tier 1 command or data is exposed.
4. **Release metadata is inconsistent.** `CITATION.cff` and `pyproject.toml` say version 2.2.0, while `CHANGELOG.md` starts with 2.2.1 dated 2026-11-01. The citation file requests citation of a tagged release but does not identify/tag a version explicitly beyond its metadata. Resolve the intended public software version before release. No DOI was asserted, which is appropriate.
5. **Author identity is not fully reconciled.** CFF includes an email and single author matching pyproject metadata. The source evidence checked by the rights/citation audit should be used to confirm whether this is the complete intended author/contributor list before publishing citation metadata; I cannot independently attest authorship from the package files alone.
6. **Dataset documentation is cautious but not a fully verified source/license catalog.** Several rows explicitly say to confirm citation/source terms, and most variants are not cleared. The document properly avoids treating this as permission, but it should be understood as provisional access guidance, not a rights clearance. No dataset or sample-level derived artifact should be released from these claims.
7. **The public installation clone command targets the default remote branch.** Until the candidate is actually merged/published as the intended branch, a user following it would receive the existing remote default tree, which still contains tracked `audit/` files and may not include the working-tree docs. Do not advertise the new documentation as the public remote state until a reviewed, approved publication occurs.

## Documentation/link checks

- Local Markdown links: passed for the 19 scanned files.
- Numerical result claims: README avoids exact values; `docs/results.md` contains no reproduced metric table and accurately withholds numerical results.
- Publication path/hash disclosure: none detected.
- Internal loop numbering: none found in public-facing README/docs. The generic use of “audit” in explanatory prose is not itself a path disclosure.
- Dataset exact-variant identity and licensing: stated as unresolved where the evidence is incomplete.
- Software test/install commands: not executed in this review; no claim of test success is made here.

## Verdict

**PUBLIC-RELEASE BLOCKED** for a public release today. The proposed docs are substantially more scientifically cautious and navigable, but no independent release test has been performed yet, tracked internal audit content remains in the current repository tip until a local candidate omission commit is made, historical Git commits retain that content, and software version/citation metadata conflict. The public research result package is intentionally absent, so the project must not describe this snapshot as reproducing the paper's results.

## Evidence inspected

- `README.md`
- `.gitignore`
- `CITATION.cff`
- `pyproject.toml`
- `CHANGELOG.md`
- `docs/api.md`, `docs/data.md`, `docs/datasets.md`, `docs/faq.md`, `docs/index.md`, `docs/limitations.md`, `docs/methodology.md`, `docs/reproducibility.md`, `docs/research-overview.md`, `docs/results.md`, `docs/software-architecture.md`, `docs/statistical-analysis.md`, and existing setup/usage/development/theory guides
- `data/README.md`
- `audit/loop6_1/baseline/baseline_summary.md`
- `audit/loop6_1/baseline/tracked_private_files.csv`
- `git ls-files` output at review time

## Limitations of this review

This is an independent documentation and release-snapshot review, not a scientific reanalysis, license opinion, privacy counsel review, software test run, or clean-clone reproduction. The final candidate branch/commit had not yet been created at the time of review.
