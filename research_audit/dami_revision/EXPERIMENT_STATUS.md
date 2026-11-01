# Experiment Status Ledger: DAMI Revision

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Revision Branch:** `research/dami-revision`  
**Date:** November 1, 2026  
**Gate Status:** **Gate G0 Complete / Awaiting Human Approval for Gate G1**  

---

## 1. Experiment Overview & Execution Matrix

| Experiment ID | Title | Scope & Design | Pre-Requisites | Current Status |
| :--- | :--- | :--- | :--- | :--- |
| **E1** | All-Cell & Threshold Sensitivity | Evaluates stability-accuracy discordance across all eligible cells unconditionally and across a threshold grid. | Gate G1 Approval | **PENDING G1 APPROVAL** |
| **E2** | Unconditional Estimands & Cohort Inference | Recomputes primary estimands (mean, median, IQR, bootstrap CIs) treating cohort as unit. | Gate G1 Approval | **PENDING G1 APPROVAL** |
| **E3** | Preprocessing Ablation | Evaluates 5 pre-specified preprocessing variants without external labels. | Gate G1 Approval | **PENDING G1 APPROVAL** |
| **E4** | Independent Cohort Expansion | Downloads, audits, and executes the benchmark suite on newly discovered independent biological cohorts. | Gate G1 Approval & Candidate Freeze | **PENDING G1 APPROVAL** (Candidates Cataloged) |
| **E5** | Positive Controls & Planted Signal | Simulates known cluster structure under varying noise dimensions ($D_{\text{noise}} = 0$ to $10{,}000$). | Gate G1 Approval | **PENDING G1 APPROVAL** |
| **E6** | Consensus Configuration Analysis | Disentangles feature gating from anchor selection and consensus aggregation in matched configurations. | Gate G1 Approval | **PENDING G1 APPROVAL** |
| **E7** | Partition Confounding & Technical Drivers | Correlates discovered partitions with PC1–PC3, sequencing depth, and batch annotations across all cohorts. | Gate G1 Approval | **PENDING G1 APPROVAL** (Prostate Diagnostic Verified) |
| **E8** | BGSS vs. Matched Random Gating | Paired cohort comparison matching feature budgets, anchor counts, and base models. | Gate G1 Approval | **PENDING G1 APPROVAL** |

---

## 2. Infrastructure & Artifact Readiness

- **Cohort Discovery Tools:** Verified under `research_audit/cohort_discovery/` (`analyze_candidates.py`, `candidate_catalog.csv`, `download_manifest.csv`).
- **Statistical Suite:** Verified under `scripts/make_stats.py`, `scripts/make_tables.py`, `scripts/make_stability_outputs.py`.
- **Core Package:** Verified under `src/icc/` (`consensus_v2.py`, `aspp.py`, `core.py`, `metrics.py`, `diagnostics.py`).
- **Baseline Implementations:** Verified under `src/icc/baselines/` (`classical.py`, `consensus.py`, `anchor.py`, `cohirf.py`, `sparse_kmeans.py`, `deep.py`).
