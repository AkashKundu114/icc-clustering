# 01 — Adversarial Journal Reviewer Red-Flag Register

**Perspective:** Senior Editorial Reviewer, *Data Mining and Knowledge Discovery* (DAMI)  
**Assessment Date:** October 13, 2026  
**Objective:** Identify all contradictions, over-claims, unproven assumptions, and vulnerabilities that would trigger objections during peer review.

---

## Ranked Findings (By Severity and Likelihood of Reviewer Objection)

| Finding ID | Severity | Category | Location | Description & Evidence | Scientific Consequence | Required Remediation / Action |
|---|---|---|---|---|---|---|
| **RF-01** | **CRITICAL** | Untested Claim | Sec 5.1 (Exp 1), Fig 3b | Claim of "+4.5% core pseudo-label accuracy advantage under extreme noise ($D \ge 1,000$)" shrunk to ~0.4% upon 10-seed re-evaluation, where baseline is at chance level. | Reviewers will challenge this as noise-fitting and p-hacking. | Formally soften claim to parity; report chance-level baseline explicitly. |
| **RF-02** | **CRITICAL** | Omnibus Significance | Sec 5.4, Table 3 | Friedman omnibus test across 13 multi-domain datasets yields $p = 0.33$ (statistically non-significant overall). | Cannot claim universal superiority or general SOTA. | Frame ICC-v2 strictly as a domain-specialized algorithm for small-$N$, high-$D$ ($D/N > 20$) regimes. |
| **RF-03** | **CRITICAL** | Mathematical Exactness | Sec 4.1, Prop 1 | Previous manuscript claimed $b_d > 5/9 \iff \Delta/\sigma > \sqrt{2}$. Exact analytic derivation requires $\Delta/\sigma > \sqrt{(3+\sqrt{15})/2} \approx 1.854$. | Erroneous theoretical statement undermined mathematical rigor. | Corrected to 1.854 with full analytic proof in theoretical foundations. |
| **RF-04** | **CRITICAL** | Baseline Fairness | `baselines/classical.py` | Single K-Means baseline historically used a single random restart (`n_init=1`), artificially lowering baseline ARI. | Overstates ICC-v2 margin against standard K-Means. | Benchmark against `k-means++, n_init=10`. |
| **RF-05** | **HIGH** | Anchor Under-sampling | Sec 5.4 (Exp 3) | Default anchor budget $L=40$ allocates $<2$ anchors per class on 20 Newsgroups ($K=20$) and Isolet ($K=26$), leading to heavy losses. | Method exhibits structural under-performance on large-$K$ benchmarks. | Acknowledge fundamental limitation; document anchor scaling rule $L = \max(40, 10K)$. |
| **RF-06** | **HIGH** | Nomenclature Discrepancy | Algorithm 1 vs Sec 4.1 | "Variance-Stabilized Subspace Gating" (VSSG) applies Sarle's Bimodality Coefficient, NOT a variance-stabilizing transform. | Reviewer objection on misleading mathematical nomenclature. | Document as Bimodality-Gated Subspace Selection (BGSS); clarify SAS origin. |
| **RF-07** | **HIGH** | Point Estimates vs Variance | Table 3 | Table 3 reports point estimates of ARI without standard deviation error bars. | Reviewers will demand multi-seed error bars to assess stability. | Add mean $\pm$ standard deviation across 10 seeds in revised table. |
| **RF-08** | **HIGH** | Selective Benchmarking | Sec 5.4 vs Supplement | Table 3 reports 13 datasets, while legacy figures evaluated 21 datasets (omitting 8 datasets where ICC-v2 has mixed results). | Perception of dataset cherry-picking. | Full pre-registration of all 21 datasets in `data/registry.yaml` and complete supplementary reporting. |
| **RF-09** | **MEDIUM** | Inductive Complexity Caption | Fig 1 caption vs Sec 4.3 | Fig 1 caption historically stated $O(L \cdot D)$ inductive complexity; text states $O(K \cdot |\mathcal{F}_{\text{active}}|)$. | Internal contradiction in algorithmic complexity. | Aligned all captions and text to $O(K \cdot |\mathcal{F}_{\text{active}}|)$. |
| **RF-10** | **MEDIUM** | Memory Scaling Distinction | Sec 5.5 vs Sec 5.6 | Stated 39.1% memory reduction at $N=8,000$ vs 97% reduction at $N=10,000$. | Confusion between total process RSS vs auxiliary consensus graph memory. | Explicitly separate auxiliary matrix memory from total OS process memory. |
| **RF-11** | **MEDIUM** | Zero-Inflation Fragility | Sec 4.1, Remark 1 | Sarle's BC degrades on zero-inflated sparse counts (e.g., scRNA-seq, sparse TF-IDF text). | Skewness/kurtosis explosion on point mass at zero. | Include explicit boundary condition advising dense embedding before gating. |
| **RF-12** | **MEDIUM** | Missing Data Imputation Bias | Sec 5.6 (Exp 3.5) | Zero-imputation artificially inflates skewness on high missingness rates ($\rho \ge 0.5$). | Algorithmic filter interacts with synthetic imputation artifacts. | Explicitly compare KNN vs Mean vs Median vs Zero imputation. |
| **RF-13** | **LOW** | Deprecated Parameters | `src/icc/consensus_v2.py` | Legacy parameter `beta` exists in `__init__` and emits `DeprecationWarning`. | Code cleanliness issue. | Addressed with clean deprecation warning; document removal in future release. |
| **RF-14** | **LOW** | Multi-Classifier Suite | Sec 5.1 | Promised kNN generalization baseline in early text. | Missing promised comparison. | Added multi-classifier generalization module in `tests/test_exp1_multiclassifier.py`. |
| **RF-15** | **LOW** | Overfull Table Formatting | `springer_manuscript/main.tex` | Table 3 column widths cause slight overfull hbox warnings in two-column mode. | Visual typography blemish. | Adjusted table formatting with `\scriptsize` and `\setlength{\tabcolsep}{3.2pt}`. |

---

## Editorial Risk Assessment

- **Risk Level:** Moderate-Low (Post-Remediation).
- **Core Scientific Defensibility:** Strong, PROVIDED the claims are strictly framed around the **small-$N$, high-$D$ noise regime ($D/N > 20$)** where the mathematical and empirical advantages over dense consensus are unequivocal.
- **Immediate Rejection Triggers Avoided:** Zero fabricated numbers, reproducible data logs, corrected mathematical proofs, transparent reporting of Friedman $p=0.33$, and complete Springer Declarations.
