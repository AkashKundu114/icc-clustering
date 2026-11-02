# Loop 5.2 — Final Independent Adjudication and Gate Report

**Phase:** Loop 5.2 — Artifact, Estimand & Reproduction Consistency Audit  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target Manuscript:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Target Journal:** Springer Nature — *Data Mining and Knowledge Discovery* (DMKD)  
**Date:** November 2026  
**Auditor:** Independent Research Panel (Forensic Statistical Learning & Editorial Review Gate)

---

## 1. Executive Summary

This report delivers the definitive independent adjudication for Loop 5.2. In strict accordance with the instructions, the evaluation is structured across **eleven operational dimensions**, using exclusively the categorical verdicts:
- **`GO`**: Fully verified, mathematically sound, and supported by primary evidence.
- **`CONDITIONAL GO`**: Scientifically sound, but requires specified adjustments to claims, p-values, intervals, or framing.
- **`HOLD`**: Temporarily paused pending mandatory external action (e.g., repository un-ignoring or Zenodo deposit).
- **`NO-GO`**: Fatal defect or scientific fraud.
- **`UNVERIFIED`**: Reported claim lacks primary trial-level execution records in the local repository.

No arbitrary numerical readiness scores are used. Verified empirical facts are rigorously separated from author-reported claims and unresolved assumptions.

---

## 2. Eleven-Dimensional Categorical Gate Adjudication

| # | Operational Dimension | Categorical Verdict | Verified Empirical Facts | Author-Reported Claims & Unresolved Assumptions | Actionable Requirement |
|:---:|:---|:---:|:---|:---|:---|
| **1** | **Artifact Integrity** | **`GO`** | All 14 recovered artifacts in `results/evidence_recovery/recovered/` and 14 cached datasets in `data/cache/` match their physical byte sizes and SHA-256 hashes **100%**. | Prior audit reports contained hallucinated hashes in report trees; now completely superseded by [canonical_artifact_manifest.csv](file:///d:/icc-clustering/audit/loop5_2/canonical_artifact_manifest.csv). | Adopt canonical manifest as definitive record. |
| **2** | **Fit-Count Integrity** | **`UNVERIFIED`** | Master results database (`results.json`) contains primary microdata for **1,430 fits** in `exp3_1` (and 1,715 fits total). | The claim of "3,000 total model fits" in Table 6 cannot be verified; run records for seeds 11–30 and baselines `CoreHalo` and `CoHiRF` are missing from the raw archive. | Formally mark 3,000-fit claim UNVERIFIED; replace manuscript wording with verified 1,430-fit statement. |
| **3** | **Discordance Thesis** | **`GO`** | Stability-accuracy discordance is authentic and reproducible. Nine non-degenerate cells average $0.684$ stability and $-0.003$ accuracy (null $\approx 0.012$). All 72 cells have mean gap $+0.464$ (clustered 95% bootstrap CI $[+0.364, +0.608]$). | None. The central empirical discovery is unassailable. | Maintain as core publication thesis. |
| **4** | **Confidence Interval Validity** | **`CONDITIONAL GO`** | Naive Student-$t$ intervals on 5 seeds produce out-of-bounds intervals ($[-0.1048, 1.0397]$ on Leukemia). Percentile bootstrap intervals on 10 seeds ($[0.4296, 0.8590]$) are strictly bounded in $[0, 1]$. | Loop 2 and Loop 5 cited the invalid Student-$t$ interval. | Replace all parametric $t$-intervals with non-parametric bootstrap intervals in text and tables. |
| **5** | **Factorial Ablation** | **`CONDITIONAL GO`** | Pairwise two-sided Wilcoxon tests across 6 cohorts yield raw $p \ge 0.156$ (Bonferroni $p_{\text{adj}} \ge 0.469$). GAC's mean advantage is driven by Leukemia (+0.566) and SRBCT (+0.499), dropping to +0.024 across the other 4 cohorts. | Manuscript claimed "statistically significant component necessity". | Soften claims to "observed empirical mean advantage concentrated in multimodal cohorts"; report non-significant p-values. |
| **6** | **Omnibus Benchmark** | **`CONDITIONAL GO`** | Across all 13 benchmarks, GAC ranks **4th** (mean rank $5.615$; Friedman $p = 0.398$, non-significant). On the 6 high-D cohorts, GAC ranks **1st** (mean rank $2.167$; Friedman $p = 0.272$, non-significant). | Manuscript claimed universal superiority across all benchmarks. | Retract global supremacy claim; frame GAC as a specialized architecture for high-dimensional biomedical regimes ($D/N > 20$). |
| **7** | **Scalability** | **`GO`** | Bipartite anchor graph scales sub-quadratically ($\mathcal{O}(N \cdot M \cdot d + M^3)$ in time; $\mathcal{O}(N \cdot M)$ in memory), requiring only $846\text{ MB}$ peak RSS at $N=10{,}000$ (and $<35\text{ MB}$ internal arrays), avoiding dense consensus memory crashes. | None. Verified by live empirical profiling. | Retain as verified engineering strength. |
| **8** | **Independent Reproducibility** | **`GO`** | All eight headline results were independently re-executed live via `audit/loop5_2/execute_recomputations.py` with exit code `0` and documented in [reproduction_execution_ledger.csv](file:///d:/icc-clustering/audit/loop5_2/reproduction_execution_ledger.csv). | An experiment is not reproduced merely because a CSV exists; execution must be verified. | Completed and verified in Loop 5.2. |
| **9** | **Public Reproducibility** | **`HOLD`** | `.gitignore` excludes `/results/`, `data/cache/`, `paper/`, and `**/figures/*`. A fresh clone contains code and tests, but zero data and zero raw results. `yale_b.npz` carries an explicit non-commercial restriction. | Assumption that CC-BY 4.0 applies to all datasets is legally false for `yale_b.npz`. | Create and deposit the Zenodo archive with dual-licensing (CC-BY-NC for `yale_b.npz`) before resubmission. |
| **10** | **Manuscript Revision Readiness** | **`GO`** | The revision team is equipped with exact canonical checksums, verified fit counts, clustered bootstrap intervals, and an actionable claim ledger. | None. All forensic obstacles have been cleared. | Revision phase can begin immediately. |
| **11** | **DMKD Submission Readiness** | **`HOLD`** | The current manuscript draft contains uncorrected out-of-bounds CIs, one-sided p-values presented as two-sided ($p=0.03125$), overbroad supremacy claims, and an unverified 3,000-fit claim. | Assumption that current draft is submittable as-is is rejected. | Hold submission until manuscript text revisions and Zenodo DOI minting are complete. |

---

## 3. Explicit Division: Verified Facts vs. Unverified Claims

### 3.1 Verified Empirical Facts (Established by primary local data)
1. **Discordance Phenomenon:** Subsample stability is demonstrably decoupled from accuracy in high dimensions ($D/N > 20$). Across 9 non-degenerate cells, mean stability is $0.684$ while mean ARI is $-0.003$ (permuted null $\approx 0.012$). Across all 72 cells, the mean gap is $+0.464$, with a clustered block bootstrap 95% CI of $[+0.364, +0.608]$, strictly excluding zero.
2. **AutoK PAC Failure:** In 510 out of 510 adversarial validation trials ($100.0\%$), AutoK selected $K_{\min} = 2$. In 486 trials ($95.29\%$), PAC scores were identically zero across all candidate $K$, rendering the selection a tie-breaking artifact.
3. **Sub-Quadratic Scalability:** Bipartite anchor graph consensus bypasses the dense $N \times N$ consensus matrix, consuming under $35\text{ MB}$ internal memory at $N=10{,}000$.
4. **Primary Benchmark Archive:** Primary run microdata exists for exactly **1,430 fits** in `exp3_1` (and 1,715 fits total in `results.json`).

### 3.2 Unverified Claims (Missing primary data or mathematically ungrounded)
1. **The 3,000-Fit Claim:** Primary execution microdata for seeds 11–30 on the high-D cohorts and for methods `CoreHalo` and `CoHiRF` is absent from `results.json`. The claim of 3,000 executed fits is **UNVERIFIED**.
2. **Factorial Statistical Significance:** Pairwise Wilcoxon tests between Full GAC and its ablation variants fail to reach significance ($p \ge 0.156$; $p_{\text{adj}} \ge 0.469$). The claim of statistically significant component necessity is **CONTRADICTED**.
3. **Global Benchmark Supremacy:** Across all 13 benchmarks, GAC ranks 4th (Friedman $p = 0.398$). The claim of outperforming all 11 baselines across diverse benchmarks is **CONTRADICTED**.
4. **SRBCT Statistical Significance on 5 Seeds:** The reported $p = 0.03125$ was one-sided. The valid two-sided exact p-value is $p = 0.0625$ (non-significant at $\alpha = 0.05$).
5. **Leukemia Confidence Interval:** The parametric interval $[-0.1048, 1.0397]$ is mathematically invalid on the bounded domain $[0, 1]$.

---

## 4. Final Editorial Roadmap to Publication

1. **Step 1: Textual Revision (Immediate - `GO`):**
   - Update Table 6 caption to reflect the verified 1,430 core fits.
   - Replace the invalid Leukemia Student-$t$ CI with the non-parametric bootstrap interval $[0.430, 0.859]$.
   - Report two-sided Wilcoxon p-values for SRBCT ($p=0.0625$) and factorial contrasts ($p_{\text{adj}} \ge 0.469$).
   - Reframe GAC as a specialized architecture for high-dimensional biomedical regimes ($D/N > 20$, where it ranks 1st) rather than a universal winner.
   - Demote AutoK from a PAC-guaranteed theoretical solver to an empirical heuristic.
2. **Step 2: Zenodo Replication Package Deposit (`HOLD` until completed):**
   - Package the 14 canonical recovered artifacts and 14 cached datasets.
   - Attach the dual-licensing notice (CC-BY 4.0 for author files; CC-BY-NC 4.0 for `yale_b.npz`).
   - Deposit bundle on Zenodo, mint a DOI, and insert the DOI into the manuscript's Data Availability Statement.
3. **Step 3: Journal Resubmission to DMKD (`CONDITIONAL GO`):**
   - Upon completion of Steps 1 and 2, the `HOLD` is lifted, and the manuscript is cleared for submission to Springer Nature — *Data Mining and Knowledge Discovery*.
