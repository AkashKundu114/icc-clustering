# Overnight Research Audit: Experiment Orchestration & Execution Plan

**Document Reference:** `research_audit/overnight/EXECUTION_PLAN.md`  
**Related Results:**  
- `results/overnight/EXECUTION_MANIFEST.csv`  
- `results/overnight/primary_icc/`  
- `results/overnight/bgss/`  
- `results/overnight/baselines/`  
- `results/overnight/unknown_k/`  
- `results/overnight/synthetic/`  
**Audit Date:** 2026-11-01  
**Auditor:** Agent E — Experiment Orchestration & Reproducibility  

---

## 1. Orchestration Architecture & Safety Constraints

To guarantee zero memory crashes and prevent data corruption over the overnight execution window:

```
+---------------------------------------------------------------------------------------+
|                               ORCHESTRATION PIPELINE                                  |
+---------------------------------------------------------------------------------------+
|  1. Memory Guard: Strict single-worker sequential execution (n_jobs=1).               |
|  2. Atomic Persistence: Every completed seed flushes immediately to CSV.              |
|  3. Checkpoint Resumption: Completed (dataset, model, seed) tuples are auto-skipped.  |
|  4. Fail-Safe Logging: Exceptions are trapped, logged, and skipped without halt.      |
|  5. Result Isolation: All new data written strictly to results/overnight/.            |
+---------------------------------------------------------------------------------------+
```

---

## 2. Central Execution Schedule

| Milestone | Target Output Path | Priority | Scope & Methods | Estimated Wall Time |
| :---: | :--- | :---: | :--- | :---: |
| **M1** | `research_audit/overnight/` | P0 | Environment, dataset manifest, audit dossiers | Complete |
| **M2** | `results/overnight/primary_icc/` | P0 | Primary ICC (v2 adaptive) across 10 Category A cohorts + Zheng68k + Sonar/Madelon (5 seeds) | ~20 min |
| **M3** | `results/overnight/bgss/` | P1 | Full ICC vs ICC w/o BGSS vs Matched Random Gating (5 seeds) | ~25 min |
| **M4** | `results/overnight/baselines/` | P1 | 8 Baselines (K-Means, GMM-BIC, Spectral, Sparse K-Means, HDBSCAN, Ward, FCM, Std Consensus) | ~35 min |
| **M5** | `results/overnight/unknown_k/` | P1 | Model Order Selection (ICC-AutoK, GMM-BIC, Spectral Eigengap, HDBSCAN) on 8 Synthetic + 7 Real Cohorts | ~40 min |
| **M6** | `results/overnight/synthetic/` | P2 | Non-convex failure stress tests (moons, circles, varying noise) | ~15 min |
| **M7** | `research_audit/overnight/FINAL_REPORT.md` | P0 | Final aggregation, meta-analysis & DMKD synthesis | ~15 min |

---

## 3. Checkpointing & Incremental Result Persistence

Every execution script follows the incremental append pattern:
1. Load existing CSV if present; extract `(dataset, model, seed)` keys into a `completed_set`.
2. Check if current task is in `completed_set`. If so, skip immediately.
3. If not, execute clustering fit, measure wall time via `time.perf_counter()`, evaluate metrics.
4. Append single result row to CSV and flush to disk.
5. Record execution log in `results/overnight/EXECUTION_MANIFEST.csv`.
