# Protocol Deviation and Remediation Log

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Revision Branch:** `research/dami-revision`  
**Date:** November 1, 2026  

---

## 1. Catalog of Remediations and Historical Deviations

| Finding ID | Classification | Historical Description | Root Cause | Remediated Status | File Traces |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DEV-01 (F-23)** | CRITICAL | Baseline labeled `FastMVC` was evaluated without disclosing that it was an internal random-subspace proxy rather than FastMICE. | Incomplete algorithmic implementation of Huang et al. (2023). | **REMEDIATED:** Formally renamed to `FastMVC-Surrogate` in code, tables, and text, with citation to Huang et al. (2023). | `src/icc/baselines/anchor.py`, `paper/main.tex`, `paper/references.bib` |
| **DEV-02 (F-24)** | MAJOR | Proposition 2 (sample determinacy bounds for core anchors) was described as essential despite Table 13 Knockout 4 proving $\Delta = +0.019$ ($p=0.84$). | Theoretical overclaim disconnected from empirical knockout findings. | **REMEDIATED:** Text recalibrated to frankly report core determinacy as an empirical null; Proposition 2 framed strictly as a mathematical structural identity. | `paper/main.tex`, `research_audit/dami_revision/METHOD_AUDIT.md` |
| **DEV-03 (F-25)** | MAJOR | Rule (i') non-degeneracy condition (excluding partitions with $>90\%$ in one cluster) was applied post-hoc without clear distinction from unconditional results. | Attempt to filter trivial 1-cluster collapse without prespecified protocol. | **REMEDIATED:** Rule (i') explicitly designated as post-hoc; both unconditional and conditional distributions reported side-by-side. | `paper/main.tex`, `research_audit/dami_revision/CLAIMS_AUDIT.md` |
| **DEV-04 (F-26)** | MAJOR | Reporting $+0.169$ BGSS mean ARI improvement without disclosing that it is driven by only two cohorts (Leukemia and SRBCT). | Presenting skewed mean without reporting cohort-level median ($0.061$) or leave-one-out sensitivity. | **REMEDIATED:** Median ARI ($0.061$) reported alongside mean ($0.217$); two-cohort concentration explicitly detailed; leave-one-out sensitivity reported. | `paper/main.tex`, `research_audit/dami_revision/STATISTICAL_AUDIT.md` |
| **DEV-05 (F-27)** | MINOR | Reporting uncorrected Wilcoxon $p = 0.031$ on $n=6$ cohorts as proof of significance. | Selective reporting of uncorrected $p$-value without family-wise multiplicity control. | **REMEDIATED:** Both uncorrected ($p = 0.031$) and Holm-Bonferroni adjusted ($p_{\text{adj}} = 0.25$) $p$-values are reported. | `paper/main.tex`, `research_audit/dami_revision/STATISTICAL_AUDIT.md` |

---

## 2. Deviation Policy for Confirmatory Execution

Any deviation from the approved Gate G1 experimental protocol must be logged here immediately with:
1. Exact timestamp and Git commit SHA.
2. Scientific rationale for the deviation.
3. Quantified impact on statistical power and degrees of freedom.
4. Pre-planned sensitivity analysis testing robustness to the deviation.
