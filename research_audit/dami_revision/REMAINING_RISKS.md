# Phase 0: Remaining Scientific and Strategic Risks

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Revision Branch:** `research/dami-revision`  
**Date:** November 1, 2026  

---

## 1. Technical & Statistical Risks

### Risk 1: Small-Sample Cohort Generalizability ($N=6$)
- **Description:** Population-level generalizations across biomedical cancer biology based on 6 cohorts are vulnerable to small-sample sampling variance.
- **Mitigation:**
  - Formally designate the 6 original cohorts as **exploratory**.
  - Avoid claims of universal biomedical validity.
  - Rely on the pre-registered cohort expansion protocol (E4) to provide independent confirmatory evidence.
  - Report cohort-level medians and leave-one-out sensitivity analyses.

### Risk 2: Two-Cohort Dependency of BGSS
- **Description:** If confirmatory cohorts do not exhibit clean multimodal separation (like Leukemia and SRBCT), the aggregate BGSS advantage over random gating may fall below statistical significance.
- **Mitigation:**
  - Frame GAC/BGSS transparently as a **conditional architecture** whose primary utility is in discrete multi-class cancer subtyping with bimodal coordinate separation.
  - Establish the discordance thesis itself—rather than algorithmic superiority—as the primary empirical contribution of the paper.

### Risk 3: Label Circularity in Public Benchmarks
- **Description:** Public benchmark datasets frequently possess class labels derived from prior clustering or gene-expression signatures, introducing circularity.
- **Mitigation:**
  - Apply the B1–B6 biological label taxonomy from `research_audit/cohort_discovery/COHORT_DISCOVERY_ELIGIBILITY_SPEC.md`.
  - Require histological, cytogenetic, or pathological ground truth (e.g. FAB classification in Leukemia, 4 histological categories in SRBCT).
  - Explicitly forbid using clinical survival or recurrence outcomes as ground-truth clustering labels.

---

## 2. Editorial & Journal Strategy Risks

### Risk 4: Reviewer Reaction to Empirical Nulls
- **Description:** Reviewers may question the inclusion of Proposition 2 given that Table 13 Knockout 4 proves certified core anchors yield an empirical difference of only $\Delta = +0.019$ ($p=0.84$) over uniform random landmarks.
- **Mitigation:**
  - Frame the knockout finding as a demonstration of scientific rigor and ablation honesty.
  - Clarify that Proposition 2 mathematically characterizes the sample determinacy of bipartite graphs, while the empirical finding establishes that uniform random landmark sampling provides a computationally lightweight, equally effective surrogate in practice.

### Risk 5: FastMVC Prior Art Perception
- **Description:** Reviewers familiar with FastMICE (Huang et al., IEEE TKDE 2023) might perceive the original `FastMVC` baseline as an incomplete implementation.
- **Mitigation:**
  - Consistently maintain the designation **`FastMVC-Surrogate`** across code, tables, and text.
  - Disclose in the methods section that the surrogate isolates the bipartite anchor graph mechanism in random subspaces without the full multi-view ADMM optimization.

---

## 3. Human Decision Gates Required

1. **Gate G1 Protocol Approval:** Explicit human sign-off on `HYPOTHESES_AND_ANALYSIS_PLAN.md` before generating the Git tag `prereg-dami-v1`.
2. **Confirmatory Cohort Registry Approval:** Human sign-off on the candidate datasets selected from `research_audit/cohort_discovery/candidate_catalog.csv` before running confirmatory benchmarks.
3. **Manuscript Text Approval:** Human review of the revised Abstract and Results highlighting the $0.061$ cohort median and two-cohort concentration.
