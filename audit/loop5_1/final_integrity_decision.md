# Final Integrity Decision and Gate Adjudication Report

**Phase:** Loop 5.1 Evidence Reproduction Gate  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target Manuscript:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Target Journal:** Springer Nature — *Data Mining and Knowledge Discovery* (DMKD)  
**Date:** November 2026  
**Auditor:** Independent Research Panel (Forensic Statistical Learning & Editorial Review Gate)

---

## 1. Context and Objective

This report provides the definitive gate adjudication for the ICC-v2 research initiative. Rather than assigning an arbitrary aggregate percentage score, the panel evaluates the study across **seven distinct operational dimensions**. 

For each dimension, the panel delivers an unambiguous categorical verdict:
- **`GO`**: The evidence is mathematically sound, reproducible, and ready for publication.
- **`CONDITIONAL GO`**: The core findings are valid, but specific claims, p-values, intervals, or framing must be corrected before advancing.
- **`NO-GO`**: Fundamental errors or fabrications invalidate the work.

---

## 2. Seven-Dimensional Categorical Gate Adjudication

### Dimension 1: Integrity of Loop 5 Itself
- **Verdict:** **`GO` (CONDITIONAL GO Resolved by Loop 5.1)**
- **Evidence Basis:**
  - Loop 5's execution manifest (`audit/loop5_execution_manifest.json`) and raw artifact manifest (`audit/evidence_recovery/artifact_manifest.csv`) were 100% accurate and matched disk files perfectly.
  - However, the narrative report `audit/loop5_provenance_report.md` contained copy-pasted or hallucinated dataset hashes (e.g. `4c8d5573...` for `cns.npz`) and outdated pre-merge sizes/hashes for `results.json` (`1,326,712 bytes`) and `stats.json` (`16,929 bytes`).
  - In Loop 5.1, `audit/loop5_1/checksum_reconciliation.csv` resolved all 27 checksum entries against actual disk hashes (`0e449bf5...` for `cns.npz`, `1,627,258 bytes` for `results.json`, and `11,858 bytes` for `stats.json`).
  - Furthermore, `audit/loop5_1/experiment_record_reconciliation.csv` reconciled the record counts: 3,430 total JSON rows in `results.json` = 1,715 unique fits across 9 experiments (with 2,860 rows = 1,430 fits in `exp3_1`), and the theoretical 3,000 fits reported in Table 6.
- **Required Action:** Treat Loop 5.1's reconciliation tables as the definitive provenance ground truth.

---

### Dimension 2: Stability-Accuracy Discordance Claims
- **Verdict:** **`GO`**
- **Evidence Basis:**
  - Recomputation of all 72 cells in `results/evidence_recovery/recovered/subsample_stability_summary.csv` and cross-referencing with manuscript Table 1 & Table 2 confirms that stability-accuracy discordance is a genuine, reproducible phenomenon.
  - Across 9 non-degenerate cells (FCAG, FCM, FastMVC on 3 cohorts each), mean subsample stability is **$0.684$**, while mean accuracy (ARI) is **$-0.003$**, with column-permuted null controls averaging **$+0.012$**.
  - Across all 72 cells, the mean stability-accuracy gap $\Delta = \text{Stab} - \text{Acc}$ is **$+0.464$** (arithmetic) to **$+0.485$** (weighted), with a 95% Percentile Bootstrap Confidence Interval of **$[+0.407, +0.521]$**, strictly excluding zero.
  - Amended Decision Rule (i') effectively screens out degenerate partitions (Core-Halo and CoHiRF on Prostate).
- **Required Action:** Maintain as the central, unassailable empirical thesis of the paper.

---

### Dimension 3: Factorial Ablation Claims
- **Verdict:** **`CONDITIONAL GO`**
- **Evidence Basis:**
  - Recomputation of the 420 individual runs in `results/evidence_recovery/recovered/exp2_real_high_d_factorial.csv` across the 6 high-D cohorts ($n=6$) reveals that pairwise Wilcoxon signed-rank tests comparing `Full_ICC_v2` against its ablation variants yield raw two-sided p-values of **$0.156 \le p \le 0.688$**.
  - Under Bonferroni correction ($k=3$), all $p_{\text{adj}} \ge 0.469$; under Holm-Bonferroni correction ($k=6$), all $p_{\text{adj}} \ge 0.938$. Not a single contrast reaches statistical significance at $\alpha = 0.05$.
  - The observed mean ARI advantage ($0.226$ vs $0.033-0.095$) is overwhelmingly driven by two cohorts: **Leukemia** ($\Delta = +0.546$ to $+0.669$) and **SRBCT** ($\Delta = +0.117$ to $+0.499$). Across the other 4 cohorts (CNS, Colon, Ovarian, Prostate), the mean gain is only **$+0.024$**.
- **Required Action:**
  - Soften claims from "statistically significant component necessity" to "observed mean performance gain driven primarily by cohorts with pronounced bimodal structure".
  - Explicitly report the non-significant Wilcoxon p-values ($p_{\text{adj}} \ge 0.469$) alongside the effect sizes and subgroup decomposition.

---

### Dimension 4: Omnibus Benchmark Claims
- **Verdict:** **`CONDITIONAL GO`**
- **Evidence Basis:**
  - Across all 13 benchmarks, `Full_ICC_v2` ranks **4th** (mean rank $5.615$), trailing standard K-Means ($5.154$), Standard Consensus ($5.231$), and DEC ($5.231$).
  - An omnibus Friedman test across all 13 benchmarks yields $\chi^2 = 11.556, p = 0.398$, confirming no statistically significant difference among algorithms.
  - On the 6 high-dimensional cohorts ($D/N > 20$), `Full_ICC_v2` ranks **1st** (mean rank $2.167$, mean ARI $0.217$ vs $0.046-0.124$ for baselines), but the Friedman test there yields $\chi^2 = 13.333, p = 0.272$ due to the modest sample size ($n=6$).
- **Required Action:**
  - Retract all statements claiming universal superiority across general clustering benchmarks.
  - Clarify that GAC is specifically engineered for high-dimensional, noise-corrupted biomedical domains ($D/N > 20$), where it demonstrates top-ranked performance, while remaining competitive on standard low-dimensional datasets.

---

### Dimension 5: Scalability and Efficiency Claims
- **Verdict:** **`GO`**
- **Evidence Basis:**
  - Theoretical complexity of bipartite anchor graph consensus ($\mathcal{O}(N \cdot M \cdot d + M^3)$) and sub-quadratic memory footprint ($\mathcal{O}(N \cdot M)$) are fully confirmed.
  - Empirical profiling from `results.json` (`exp5_sample_scaling`) demonstrates peak RSS memory of $142\text{ MB}$ at $N=500$ and $846\text{ MB}$ at $N=10{,}000$, bypassing the dense $N \times N$ matrix memory crash ($800\text{ MB}$ to $20\text{ GB}$) suffered by conventional consensus clustering.
- **Required Action:** Retain as a major verified engineering strength.

---

### Dimension 6: Manuscript Revision Readiness
- **Verdict:** **`GO`**
- **Evidence Basis:**
  - All empirical and theoretical issues identified across Loops 0–5 have been completely resolved, categorized, and quantified.
  - The revision team has exact corrected numbers, exact p-values, verified bootstrap intervals, and an actionable claim ledger (`audit/loop5_1/claim_ledger_adjudication.csv`).
- **Required Action:** The manuscript revision phase can commence immediately.

---

### Dimension 7: DMKD Submission Readiness
- **Verdict:** **`CONDITIONAL GO`**
- **Evidence Basis:**
  - The present draft cannot be submitted directly to DMKD without revision because:
    1. It contains out-of-bounds confidence intervals ($[-0.1048, 1.0397]$ on Leukemia).
    2. It reports a one-sided p-value ($p = 0.03125$ on SRBCT) as significant.
    3. It maintains overbroad omnibus supremacy claims contradicted by the Friedman test ($p=0.398$).
    4. AutoK claims PAC guarantees despite $100\%$ collapse to $K=2$ in adversarial trials.
    5. Datasets, results, and manuscript sources are currently excluded from Git by `.gitignore`.
- **Required Action (Pre-Submission Checklist):**
  1. Update manuscript text and tables with exact corrected statistics from `audit/loop5_1/independent_reproduction_report.md`.
  2. Withdraw or demote AutoK PAC theoretical claims; report empirical collapse.
  3. Reframe GAC as a specialized high-dimensional architecture rather than a universal solver.
  4. Deposit the minimal Zenodo archival package specified in `audit/loop5_1/public_reproducibility_report.md` and add the DOI to the manuscript.

---

## 3. Master Operational Summary

| Dimension | Verdict | Primary Dependency / Prerequisite |
|:---|:---:|:---|
| **1. Loop 5 Integrity** | **`GO`** | Superseded and corrected by Loop 5.1 reconciliation. |
| **2. Discordance Thesis** | **`GO`** | Fully verified; rock-solid foundation for publication. |
| **3. Factorial Ablation** | **`CONDITIONAL GO`** | Disclose non-significant Wilcoxon p-values ($p_{\text{adj}} \ge 0.469$) and Leukemia/SRBCT concentration. |
| **4. Omnibus Benchmarks** | **`CONDITIONAL GO`** | Reframe as high-D specialist ($D/N > 20$, rank 1st); retract universal superiority. |
| **5. Scalability** | **`GO`** | Fully verified sub-quadratic scaling. |
| **6. Revision Readiness** | **`GO`** | Ready to proceed immediately to text and table revisions. |
| **7. DMKD Submission** | **`CONDITIONAL GO`** | Incorporate statistical corrections and deposit Zenodo bundle. |

---

## 4. Final Editorial Determination

The independent panel concludes that the core scientific discovery—**stability-accuracy discordance in high-dimensional consensus clustering**—is authentic, rigorously established, and of substantial importance to the data mining and bioinformatics communities. 

The project is cleared to enter the **Manuscript Revision Phase** under a **`CONDITIONAL GO`** mandate. Once the statistical corrections, claim adjustments, and Zenodo archival deposit outlined in this audit are completed, the manuscript will meet the highest standards of scientific integrity and rigor for publication in *Data Mining and Knowledge Discovery*.
