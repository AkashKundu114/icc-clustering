# 00 Baseline Audit Snapshot and Repository Metadata

**Investigation:** Forensic Evidence Recovery & Repository Baseline Verification  
**Repository Path:** `D:\icc-clustering`  
**Remote URL:** `https://github.com/AkashKundu114/icc-clustering.git`  
**Snapshot Timestamp:** `2026-11-01T23:02:00+05:30` (IST)  
**Lead Auditor:** Senior Research Software Auditor & Scientific Reviewer  

---

## 1. Repository State & Identity

### 1.1 Commit Identifiers and Tracking
- **Local Active Branch:** `main`
- **Current Local HEAD:** `7ddbe8301b8d27c94f388c40acbc88b0dee82723`
- **Remote Tracking Reference:** `origin/main` -> `7ddbe8301b8d27c94f388c40acbc88b0dee82723`
- **Remote Default Branch HEAD:** `7ddbe8301b8d27c94f388c40acbc88b0dee82723`
- **Tracking Status:** Up to date with `origin/main` (`## main...origin/main`)
- **Working-Tree Status:** Clean. Zero tracked modifications, zero untracked files outside gitignored roots.

### 1.2 HEAD Commit Details
```text
commit 7ddbe8301b8d27c94f388c40acbc88b0dee82723
Author:     Akash Kundu <akashkundu1152@gmail.com>
AuthorDate: Sun Nov 1 22:19:09 2026 +0530
Commit:     Akash Kundu <akashkundu1152@gmail.com>
CommitDate: Sun Nov 1 22:19:09 2026 +0530

    Expand Python compatibility CI and docs
    
    Add lint and typing checks plus a Python 3.10–3.14 Windows/Linux test matrix,
    with regression coverage for runtime compatibility. Update project documentation,
    statistical API references, and XERJ indexing details.
```

---

## 2. Git References & Ancestry

### 2.1 Tags in Repository
| Tag | Commit SHA | Annotated Message |
|---|---|---|
| `v1.0.0` | `92474fdcc27cfe9f2a20fee855ae2d169620f1d7` | Release v1.0.0 with Zenodo DOI 10.5281/zenodo.23852735 |
| `v2.0.0` | `b7003ae52d665aaa1b7886ba884d9f067f9bdc59` | Release v2.0.0: Inductive Consensus Clustering (ICC-v2) |
| `v2.1.0` | `ad7a73c387eb6e2ed58a235a9bc143129733a0bb` | Release v2.1.0: Conformal Inductive Projection and Real-World Applications |
| `v2.2.0` | `943e55e1bc965e17eeaae81359d5413baf4b7adc` | feat(release): prepare public v2.2.0 release for peer review and independent reproduction |

### 2.2 Remote Pull Request References Advertised on GitHub
The remote repository advertises 22 public pull-request head refs (`refs/pull/*/head`):
- `refs/pull/1/head` (`ba6ea4b`) to `refs/pull/22/head` (`588bc47`)

### 2.3 Verification of Historical Ancestry: `e3f54cc`
- Historical Commit: `e3f54cc0951d173f0e13a4b524628328f318e746`
- Command: `git merge-base --is-ancestor e3f54cc0951d173f0e13a4b524628328f318e746 HEAD`
- Exit Code: `0` (Confirmed True Ancestor)
- Topological Distance to HEAD: Exactly 12 commits.

---

## 3. Environment & Toolchain Snapshot

### 3.1 System Architecture
- **Operating System:** Windows 11 Enterprise / Pro (Build 10.0.26300, SP0)
- **Architecture:** AMD64 (x86_64)
- **Python Version:** CPython 3.14.6 (`tags/v3.14.6:2ce98b3`, Feb 10 2026)
- **Git Version:** 2.56.0.windows.4
- **Working Directory:** `D:\icc-clustering`

### 3.2 Core Scientific Libraries Installed
| Package | Version | Role in ICC-Clustering |
|---|---|---|
| `numpy` | `2.4.6` | Linear algebra, array processing, matrix decomposition |
| `scipy` | `1.18.0` | Sparse matrices, statistical tests, SVD |
| `scikit-learn` | `1.9.1` | Base clusterers, evaluation metrics, preprocessing |
| `pandas` | `3.0.5` | Tabular data analysis, benchmark manifests |
| `numba` | `0.66.0` | JIT compilation for distance kernels |
| `matplotlib` | `3.11.1` | Visualizations, ASPP diagnostic plots |
| `seaborn` | `0.13.2` | Statistical heatmaps, co-association plotting |
| `tabulate` | `0.10.0` | Formatted summary tables |
| `torch` | `2.16.0.dev20261017+cu134` | Deep clustering baselines (DEC, IDEC, CC, SCAN) |

---

## 4. Verification of Designated Audit Paths

Git ignore checks confirmed that the designated audit and evidence directories are strictly ignored:
- `audit/` (Rule: `.gitignore:2:/audit/`)
  - `audit/evidence_recovery/` — Ignored
  - `audit/remediation/` — Ignored
- `results/` (Rule: `.gitignore:3:/results/`)
  - `results/evidence_recovery/recovered/` — Ignored
  - `results/evidence_recovery/reconstructed/` — Ignored

---

## 5. Preliminary Inconsistencies Discovered

1. **HEAD SHA Resolution:**
   - Prior audit reports alternately cited `83728a441f44c1ed56a35a5bdb07490ff559de81` and `7ddbe8301b8d27c94f388c40acbc88b0dee82723`.
   - **Resolution:** `7ddbe83` is the direct linear child of `83728a4`, committed at `Sun Nov 1 22:19:09 2026 +0530`. The working-tree modifications recorded during the earlier audit session were committed and pushed to `origin/main` as `7ddbe83`. Both local and remote are completely synchronized at `7ddbe83`.
2. **Confidentiality Sanitization Status:**
   - Commit `0565abc` (`chore(confidentiality): remove non-code documentation assets...`) was a regular working-tree deletion, **not** a Git history rewrite. All deleted sensitive assets remain reachable in commit history prior to `0565abc` and through public PR references.
