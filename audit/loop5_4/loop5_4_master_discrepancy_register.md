# Loop 5.4 — Master Discrepancy & Forensic Issue Register

**Phase:** Loop 5.4 — Final Adversarial Statistical Validation & Manuscript Claim Adjudication  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target Manuscript:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Target Journal:** Springer Nature — *Data Mining and Knowledge Discovery* (DMKD)  
**Date:** November 2026  
**Auditor:** Independent Research Panel (Forensic Audit Group)  
**Deliverable Associated:** [loop5_4_master_discrepancy_register.md](file:///d:/icc-clustering/audit/loop5_4/loop5_4_master_discrepancy_register.md)

---

## 1. Executive Summary & Purpose

This register provides the definitive historical reconciliation of every mathematical, statistical, empirical, procedural, and licensing discrepancy identified across all audit iterations (Loop 0 through Loop 5.4).

Each discrepancy is categorized by its origin, severity, mathematical diagnosis, and final status (Resolved, Expunged, or Reframed).

---

## 2. Comprehensive Forensic Discrepancy Matrix

| Discrepancy ID | Operational Scope | Originating Loop | Initial Flawed Claim / Defect | Forensic Root Cause | Resolution / Final Status |
|:---:|:---|:---:|:---|:---|:---:|
| **DISC-01** | **ARI Theoretical Support** | Loop 5 / 5.1 / 5.2 / 5.3 | Asserted ARI has support strictly on $[0, 1]$; rejected negative endpoints. | Misunderstanding of Hubert & Arabie (1985) chance-correction formula, which can be negative down to $-1.0$. | **RESOLVED & CORRECTED.** Negative ARI is valid. Upper bound ($> 1.0$) remains strictly invalid. |
| **DISC-02** | **Leukemia Parametric Student-$t$ CI** | Loop 2 / Loop 5 | Reported $[-0.1048, 1.0397]$ as valid 95% confidence interval. | Applied symmetric unbounded Gaussian $t$-distribution ($df=4$) to small ($n=5$) bimodal data, exceeding $\max(\text{ARI})=1.0$. | **EXPUNGED.** Replaced with verified 10-seed non-parametric bootstrap interval $[0.430, 0.859]$ (BCa $[0.409, 0.853]$). |
| **DISC-03** | **Spurious Leukemia Ledger Entry** | Loop 5.2 | Recorded `Bootstrap [0.3800, 0.7960] is valid` in reproduction ledger. | Administrative copy-paste error; copied point ARI measurements from `exp4_anchor_budget.csv`. Contradicted script stdout. | **EXPUNGED.** Permanently removed from all audit ledgers. |
| **DISC-04** | **Untraceable Loop 5.1 Leukemia CI** | Loop 5.1 | Reported $[0.0076, 0.8879]$ as percentile bootstrap interval. | Executed an unpreserved bootstrap run without saving script, seed, or input vector; irreproducible from raw data. | **EXPUNGED.** Replaced with canonical 10-seed percentile bootstrap. |
| **DISC-05** | **SRBCT Wilcoxon Test Significance** | Loop 2 / Loop 5 | Claimed GAC achieves statistically significant gain on SRBCT with $p = 0.03125$. | Reported one-sided p-value as two-sided. On $n=5$ paired seeds, exact two-sided p-value is $p = 0.0625$ (non-significant at $\alpha=0.05$). | **RESOLVED & CORRECTED.** Report two-sided $p = 0.0625$ on 5 seeds; report two-sided $p = 0.00195$ on 10 canonical seeds. |
| **DISC-06** | **Loop 5.2 Pseudo-Holm Heuristic** | Loop 5.2 | Claimed to implement Holm-Bonferroni correction by setting `holm = min(1.0, p * 6)`. | Multiplied every p-value by $m=6$, which is standard Bonferroni, not the Holm step-down procedure. | **RESOLVED & CORRECTED.** Implemented genuine step-down Holm-Bonferroni in `generate_task2.py` ($p_{\text{adj}} \ge 0.938$). |
| **DISC-07** | **Pass-Through Friedman Statistics** | Loop 5.2 | Claimed live audit execution of 13-dataset Friedman test by loading `stats.json`. | Read precomputed dictionary fields `stats_data['N13']` without running `scipy.stats.friedmanchisquare` on raw arrays. | **RESOLVED & CORRECTED.** Recalculated directly from raw array in `generate_friedman_validation.py` ($\chi^2=11.3427, p=0.3315$). |
| **DISC-08** | **Clustered Bootstrap Script Omission** | Loop 5.2 | Presented clustered bootstrap results in markdown, but script only computed arithmetic means. | The clustered bootstrap code was omitted from `execute_recomputations.py` and missing from the execution ledger. | **RESOLVED & IMPLEMENTED.** Full standalone scripts executed in Loop 5.3 and Loop 5.4 (`clustered_bootstrap_independent_verification.py`). |
| **DISC-09** | **Hallucinated Scalability Numbers** | Loop 5.1 / 5.2 | Claimed peak RSS is $142\text{ MB at } N=500$ and $846\text{ MB at } N=10{,}000$. | Invented numbers in Loop 5.1 text; copied uncritically into Loop 5.2 ledger. $N=500$ does not exist in `results.json`. | **EXPUNGED.** Permanently removed. Citing exact Table 4 traced RAM ($3.1\text{ MB}$ at $N=500$ vs $68.8\text{ MB}$ at $N=10{,}000$). |
| **DISC-10** | **Manuscript Table 6 3,000-Fit Claim** | Manuscript / Loop 5 | Table 6 caption claims "3,000 Total Model Fits". | Master results archive contains raw microdata for 1,430 core fits; seeds 11–30 and non-biomedical CoreHalo runs are missing. | **REFRAMED & AMENDED.** Table 6 caption updated to cite verified 1,430 core benchmark fits. 3,000-fit claim marked UNVERIFIED. |
| **DISC-11** | **Loop 5.3 Hardcoded Input Hash Typo** | Loop 5.3 | `clustered_bootstrap.py` recorded input SHA-256 as `577cbab7e376...`, mismatching disk file. | Author manually typed corrupted hash string starting with `577cbab7...` instead of computing `hashlib.sha256()`. File on disk was unchanged. | **RESOLVED & CORRECTED.** True hash `577cbab79913...` verified dynamically in Loop 5.4. |
| **DISC-12** | **AutoK PAC Bound Collapse** | Loop 2 / Loop 5 | Presented AutoK as a mathematically guaranteed automated cluster count selector. | In 510/510 adversarial trials (100.0%), AutoK collapsed to $K_{\min}=2$ (95.3% zero scores); PAC penalty dominates for small $N$. | **REFRAMED & MOVED TO FUTURE WORK.** AutoK demoted from theoretical solver to heuristic; finite-sample redesign proposed for future work. |
| **DISC-13** | **Extended Yale B Licensing Conflict** | Loop 5.1 / 5.2 | Assumed CC-BY 4.0 license applies to entire public repository and Zenodo archive. | `yale_b.npz` is subject to an upstream Yale University academic/non-commercial restriction. CC-BY allows commercial use. | **RESOLVED VIA DUAL-LICENSING.** Zenodo bundle structured with CC-BY 4.0 for code/results and CC-BY-NC 4.0 for `yale_b.npz`. |
| **DISC-14** | **Git Blob vs. File SHA-256 Conflation** | Loop 5 / 5.1 | Repeated phantom hash mismatches across audit manifests. | Conflated Git object blob SHA-1 (`git hash-object`) with physical file SHA-256 (`hashlib.sha256`). | **RESOLVED & DOCUMENTED.** Both hashing schemes side-by-side reconciled in `provenance_reconciliation.csv`. |

---

## 3. Discrepancy Lifecycle Status

- **Total Discrepancies Registered:** 14
- **Resolved via Recalculation / Script Implementation:** 7 (DISC-01, DISC-05, DISC-06, DISC-07, DISC-08, DISC-11, DISC-14)
- **Permanently Expunged (Fictional / Unsound):** 4 (DISC-02, DISC-03, DISC-04, DISC-09)
- **Reframed in Manuscript / Future Work:** 3 (DISC-10, DISC-12, DISC-13)
- **Unresolved / Blocking Fatal Bugs:** **0**

All discrepancies have been addressed, verified by code, and backed by traceable file bytes.
