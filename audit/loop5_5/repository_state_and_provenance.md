# Repository state and provenance — Loop 5.5

Fetched `origin` before inspection. `HEAD` and fetched `origin/main` are both `e745ee0c4a4ef2d79c10cb95356f359b3905b05b` (commit timestamp `2026-11-02T15:16:20+05:30`). The commit adds Loop 5.4 audit files. `git status` was clean for tracked files at start. Current audit additions are uncommitted and confined to `audit/loop5_5/`.

- Code under audit: `e745ee0c4a4ef2d79c10cb95356f359b3905b05b`.
- Audit execution commit: `e745ee0c4a4ef2d79c10cb95356f359b3905b05b`.
- Audit deliverables commit: not yet committed; no deliverables commit exists.
- Loop 5.4 manifest instead records code `4107feb9cdeda889426b39b293a9dc1c4857fd95` and execution `f9d9d44af3ba3c2f90c5bf6853858005704839ac`; these differ from current HEAD.
- Tracked `data/`, `results/`, `paper/`: none. Locally present files under results, data/raw/cache and paper are ignored. They are not available in a fresh clone.
- Current raw and cached dataset arrays: absent. Present local `results/evidence_recovery/recovered/` includes `results.json` and `subsample_stability_summary.csv`, both ignored.

`git fetch origin` completed. `git diff` from the prior commit shows the Loop 5.4 audit directory additions only. The audit execution did not modify production code, tests, data, or prior audits. Key artifacts and dynamic byte hashes are in `artifact_provenance_manifest.csv`.

**Prior report file references:** all inspected Loop 5.4 report files listed in its execution manifest are present under `audit/loop5_4/`. Its cited result inputs also happen to exist locally, but are ignored and have no fresh-clone guarantee. Some prior statements do not follow from these inputs; see discrepancy register.
