# 00 — Repository Inventory & Baseline State

**Inspection Date:** October 13, 2026  
**Auditor:** Principal Research Engineer & Scientific Coordinator  
**Commit SHA:** `71754b8` (Branch: `fix/audit-remediation`)  
**Target Venue:** *Data Mining and Knowledge Discovery* (Springer Nature)  
**Target Publication Objective:** Online publication by September 2027  

---

## 1. Git Repository State

- **Active Branch:** `fix/audit-remediation`
- **Remote Branches:**
  - `origin/main`
  - `origin/submission/icde-2027`
- **Working Tree:** Clean (with untracked report `docs/REMEDIATION_REPORT.md` and new `submission_audit/`).
- **Gitignore Policies:** All generated paper packages, PDFs, and manuscript build artifacts (`paper/`, `manuscript/`, `springer_manuscript/`, `*.pdf`, `*.zip`) are ignored and untracked from Git while preserved intact on disk.

---

## 2. Manuscript Versions Inventory

| Manuscript Path | Class / Template | Citation System | Authorship / Affiliation | Current Build Status | Notes |
|---|---|---|---|---|---|
| `springer_manuscript/main.tex` | Springer Nature (`sn-jnl.cls` v3.1 Dec 2024) | Author-Year (`sn-mathphys-ay`) | Akash Kundu, Trinankur Guha, Rupankar Ghatak, Anubhab Naskar; Mentor: Kalyan Kumar Das (Techno India Univ) | Compiled (`main.pdf`, 7.50 MB) | Authoritative submission target for *Data Mining and Knowledge Discovery*. |
| `paper/main.tex` | IEEE TKDE / ArXiv format (`bare_jrnl_compsoc.tex`) | Numbered IEEE | Mentions authors and Techno India Univ | Compiled (`main.pdf`, 7.85 MB) | Single source of truth for numbers via `paper/gen/`. |
| `manuscript/main.tex` | IEEE TKDE / ArXiv format | Numbered IEEE | Same | Compiled | Older mirror retained for reference. |
| `manuscript/icde_main.tex` | IEEE Conference (`IEEEtran.cls`) | Numbered IEEE | Anonymous / Double-blind | Compiled (`icde_main.pdf`) | Previous conference submission attempt. |

---

## 3. Library & Module Inventory (`src/icc/`)

| Module Path | Primary Responsibility | Critical Functions / Classes | Complexity Profile |
|---|---|---|---|
| `src/icc/consensus_v2.py` | Core ICC-v2 algorithm | `InvariantCoreConsensusV2`, `compute_bimodality_coefficients`, `compute_sample_determinacy_linear` | $O(ND)$ gating, $O(M^2 N + M^2 K^2)$ determinacy, $O(NL)$ bipartite graph. |
| `src/icc/consensus.py` | Legacy v1 implementation | `InvariantCoreConsensus`, `evaluate_consensus_determinacy` | Contains legacy $O(N^2)$ paths; retained for baseline comparison. |
| `src/icc/core.py` | Base generator & clustering engine | `SubspaceBaseGenerator`, `ClusterEnsemble` | Draws random subspaces from candidate pool. |
| `src/icc/aspp.py` | Perturbation profiling | `AnchorSpacePerturbationProfiler`, `PerturbationFamily` | 5 perturbation families evaluated over anchor coordinates. |
| `src/icc/metrics.py` | Evaluation metrics | `adjusted_rand_index`, `normalized_mutual_info`, `clustering_accuracy` | Multi-metric cluster evaluation suite. |
| `src/icc/baselines/` | Comparative baselines | Classical (K-Means, Ward, Spectral, FCM), Consensus (StdConsensus, Li et al.), Anchor (FCAG, FastMVC), Deep (DEC) | 9 comparative methods implemented. |
| `src/icc/datasets/` | Dataset loaders & registry | `registry.py`, `genomics.py`, `image.py`, `audio.py`, `text.py`, `spectral.py`, `scrnaseq.py` | 21 datasets registered in `data/registry.yaml`. |

---

## 4. Test Suite Baseline Execution

Ran `python -m pytest tests/ -v` on Python 3.14.6:
- **Total Tests:** 78
- **Passed:** 78 (100% pass rate)
- **Execution Time:** 62.96 seconds
- **Line Coverage:** 74% overall across 2,014 statements (`aspp.py` 93%, `consensus_v2.py` 80%, `metrics.py` 88%).

*Crucial Caveat:* While the unit test suite passes with 100% green status, passing unit tests alone does NOT establish mathematical validity, empirical superiority, or novelty. The independent audit below examines those foundational dimensions.
