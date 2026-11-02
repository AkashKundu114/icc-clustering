# 01 Repository State Verification Report

**Audit Target:** ICC-Clustering (`D:\icc-clustering`)  
**Audit Timestamp:** 2026-11-01T22:10:30+05:30  
**Verification Lead:** Antigravity Post-Refactor Audit Harness  
**Operating System:** Windows 11 Enterprise (Version 10.0.26100 Build 26100)  
**Python Runtime:** Python 3.14.6 (`C:\Users\Akash\AppData\Local\Microsoft\WindowsApps\python.exe`)  

---

## 1. Local and Remote Git References

| Reference | Value / Commit Hash | Status / Details |
|---|---|---|
| **Local Working Directory** | `D:\icc-clustering` | Clean mount, verified local repository |
| **Local Branch** | `main` | Tracking `origin/main` |
| **Local HEAD SHA** | `83728a441f44c1ed56a35a5bdb07490ff559de81` | Commit: "Update cohort discovery paths and metadata" |
| **Local `origin/main` SHA** | `83728a441f44c1ed56a35a5bdb07490ff559de81` | Synchronized with local `main` |
| **Remote HEAD SHA (`origin`)** | `83728a441f44c1ed56a35a5bdb07490ff559de81` | Advertised by `git ls-remote --heads origin` |
| **Remote Divergence** | In sync (0 ahead, 0 behind) | Local `main` points to identical commit as `origin/main` |
| **Remote Origin URL** | `https://github.com/AkashKundu114/icc-clustering.git` | Verified fetch and push endpoints |

---

## 2. Remote Heads and Tags Inventory

### Advertised Remote Heads (`git ls-remote --heads origin`)
- `83728a441f44c1ed56a35a5bdb07490ff559de81 refs/heads/main`
*(Note: `main` is the sole public branch active on remote `origin`)*

### Advertised Remote Tags (`git ls-remote --tags origin`)
- `92474fdcc27cfe9f2a20fee855ae2d169620f1d7 refs/tags/v1.0.0`
- `57aaef45da7a2e7ba4149592002b11d5d2ecbdb1 refs/tags/v1.0.0^{}` (peeled tag object)
- `943e55e1bc965e17eeaae81359d5413baf4b7adc refs/tags/v2.2.0`

### Local vs. Remote Tag Discrepancy
Local repository contains four tags (`git tag --list`):
- `v1.0.0` (`92474fdcc27cfe9f2a20fee855ae2d169620f1d7`) — **Present on remote**
- `v2.0.0` (`b7003ae52d665aaa1b7886ba884d9f067f9bdc59`) — **Missing on remote**
- `v2.1.0` (`ad7a73c387eb6e2ed58a235a9bc143129733a0bb`) — **Missing on remote**
- `v2.2.0` (`943e55e1bc965e17eeaae81359d5413baf4b7adc`) — **Present on remote**

---

## 3. Remote Pull Request References (`refs/pull/*/head`)

Twenty-two pull-request head refs are advertised and preserved on the GitHub remote:

| PR Reference | Remote Commit SHA | Subject / Associated Context |
|---|---|---|
| `refs/pull/1/head` | `ba6ea4bb2f4b1d446649a23ea4da55e84bb75224` | Historical PR ref |
| `refs/pull/2/head` | `80dd1737f624d64a8f306178f445ea8c84b6219f` | Historical PR ref |
| `refs/pull/3/head` | `27ee38051dd9d284de2bc774ced2a31655fdd9b6` | Historical PR ref |
| `refs/pull/4/head` | `96450bac33c42c9d74472c7f25856bced0c408f1` | Historical PR ref |
| `refs/pull/5/head` | `e49e3583a488e840f0b51fbb92467c57e38fabf7` | Historical PR ref |
| `refs/pull/6/head` | `6cf329072f90b0bfd6f55ab8f534a3b488d8c10f` | Historical PR ref |
| `refs/pull/7/head` | `c6822f76904bbbf379442b3c0f9e1537641a604c` | Historical PR ref |
| `refs/pull/8/head` | `7fcd705c3efbce5330461cfb9ce776e73aca097c` | Historical PR ref |
| `refs/pull/9/head` | `ed0a0b2891d7c91910b1d7a281cf2a6bc454ce20` | Historical PR ref |
| `refs/pull/10/head`| `b3c72f60c34de0ab89b69ce5487a5fd0168e4c35` | Historical PR ref |
| `refs/pull/11/head`| `be6bdfaf30642e22ec618160d116aa2372d2377b` | Historical PR ref |
| `refs/pull/12/head`| `cc5ddffd8a33d1802552a2e65b2a3c9a5e86c1af` | Historical PR ref |
| `refs/pull/13/head`| `b18cced3b9fdee7927dde52fb3a577eb293ca233` | Historical PR ref |
| `refs/pull/14/head`| `2b6daa76c150811c4f4609aef048db2428e518e3` | Historical PR ref |
| `refs/pull/15/head`| `b3a54a1aacce22560c348d92af224ecf5292dd89` | Historical PR ref |
| `refs/pull/16/head`| `167f20c2a286227fd7ac9fb57de34c5aed82848d` | Historical PR ref |
| `refs/pull/17/head`| `8c80c3acd017b4700feac41962f483beba10e88a` | Historical PR ref |
| `refs/pull/18/head`| `58754117385c44d70eda6827af347bb4553b4db5` | Historical PR ref |
| `refs/pull/19/head`| `6ac35adf2c9cea04a7c6ecf5df95f5a45ae28270` | Historical PR ref |
| `refs/pull/20/head`| `60b163f22b5931da35a1ace07d1934bf3bdd65e3` | Historical PR ref |
| `refs/pull/21/head`| `91e4092f9a0d8808dfe20c1734653809d033752a` | Historical PR ref |
| `refs/pull/22/head`| `588bc470098581974ca614d48cf8af87147a36dc` | `integrate/consolidation` (merged in `8d190e0`) |

---

## 4. Working Tree State (Uncommitted & Untracked Changes)

At the start of the audit, the local working tree was inspected with `git status --short --branch`.

### Uncommitted Modifications to Tracked Files
The working tree contains unstaged modifications made prior to this audit:
1. `M .github/workflows/ci.yml` — Expands CI matrix from 3.10-3.12 to 3.10-3.14.
2. `M CHANGELOG.md` — Adds unreleased `[2.2.1]` documentation block.
3. `M CONTRIBUTING.md` — Updates test commands and Python range.
4. `M README.md` — Updates test badges and architecture diagram text.
5. `M docs/api.md` — Documents `icc.stats` functions.
6. `M docs/development.md` — Updates architecture tree comments.
7. `M docs/reproducibility.md` — Fixes backtick typos in code blocks.

### Untracked Files
- `?? tests/regression/test_python_compatibility.py` — New 7-test suite targeting Python 3.14/3.13 semantics.

### Audit Directory Status
- `audit/post_refactor_verification/` — Ignored by `.gitignore` (line 2: `/audit/`).
- `results/post_refactor_verification/` — Ignored by `.gitignore` (line 3: `/results/`).

---

## 5. Commit Ancestry and Lineage Verification

We independently verified the ancestry relation between commit `e3f54cc0951d173f0e13a4b524628328f318e746` and `origin/main` (`83728a441f44c1ed56a35a5bdb07490ff559de81`):

```powershell
git merge-base --is-ancestor e3f54cc0951d173f0e13a4b524628328f318e746 origin/main
# Exit code: 0 (TRUE)
```

There are exactly **11 linear commits** connecting `e3f54cc` to current `origin/main`:

```text
83728a4 (HEAD -> main, origin/main, origin/HEAD) Update cohort discovery paths and metadata
1761c1a Improve benchmarks and harden data handling
781eba5 refactor(architecture): streamline package structure, deduplicate modules, and flatten documentation
3bc8459 fix(typing): add type ignore for numpy 2D tuple shape assignment
669a235 fix(typing): preserve float32 dtype in SNN adjacency calculation
8b81794 fix(typing): use np.min(d) instead of ndarray.min() for numpy 2.x mypy typing
cc2a3a9 feat(cli): add backward-compatible reproduce CLI shim
81887a1 style: format imports and remove unused variables
0565abc chore(confidentiality): remove non-code documentation assets and standardize repository guides
8d190e0 Merge pull request #22 from AkashKundu114/integrate/consolidation
2183b29 feat(consolidation): integrate advanced evaluation protocols and holdout validation into main
e3f54cc feat(validation): complete algorithmic validation and benchmark test harness
```

**Key Finding:** Commit `e3f54cc0951d173f0e13a4b524628328f318e746` and all of its historical ancestors remain integral parts of the immutable `main` branch on `origin`. The advertised history rewrite was never force-pushed to the remote repository.
