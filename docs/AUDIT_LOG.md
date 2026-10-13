# ICC-v2 Independent Audit Log & Remediation Checklist

This document tracks all identified discrepancies, contradictions, mathematical bugs, and experimental flaws across the manuscript and repository, along with their resolution status.

---

## 1. Numerical & Experimental Contradictions

| Item ID | Description | Manuscript / Code Discrepancy | Remediation Status | Notes / Plan |
|---|---|---|---|---|
| NUM-01 | Leukemia ARI contradiction | 0.846 (Sec 5.2) vs 0.680 (Table 3) vs ~0.798 (Fig 6) | RESOLVED | Standardized on verified multi-seed run via `make_paper_assets.py` (`\ARIleukemia` = 0.680). |
| NUM-02 | SRBCT ARI contradiction | 0.681 (Sec 5.2) vs 0.538 (Table 3) vs ~0.578 (Fig 6) | RESOLVED | Standardized on verified multi-seed run (`\ARIsrbct` = 0.538). |
| NUM-03 | Fig 6 vs Table 3 dataset/method count | Fig 6 title says "21 datasets × 9 methods" but caption says "13 × 11". | RESOLVED | Reconciled 13-benchmark primary table and 21-dataset supplementary table. |
| NUM-04 | Fig 7 CD & rank mismatch | Fig 7 uses N=21, 9 methods, with different mean ranks from Table 3; CD=2.62 matches k=9, N=21. | RESOLVED | CD diagram regenerated and aligned with Table 3 and supplementary matrices. |
| NUM-05 | CNS vs Glioma duplication | In legacy Fig 6, CNS and Glioma rows were numerically identical. | VERIFIED & REMEDIATED | Identified duplicate data loading bug in legacy script; mapped to distinct loaders. |
| NUM-06 | Missing 8 datasets from Table 3 | 8 datasets in Fig 6 absent from Table 3 (Lymphoma, Lung_Cancer, Glioma, Breast_Cancer, Gisette, Waveform, HAR, USPS), including heavy losses. | RESOLVED | Pre-registered in `data/registry.yaml`; exported to `table_supplementary_extended.tex`. |
| NUM-07 | D/N > 20 Rank #1 R=1.50 claim | Recount from Table 3 gives ~2.2 over 6 D/N > 20 datasets, not 1.50. | RESOLVED | Recalibrated exact average rank to 2.33 across 11 methods; updated in text and macros. |
| NUM-08 | Fig 8 |ΔARI| and Reduced vs Exact | Text claims \|ΔARI\| ≤ 0.05 and Reduced beats Exact at N=5k (0.618 vs 0.583); plot showed Exact ≈ 1.0, Reduced ≈ 0.76 (gap ≈ 0.24). | RESOLVED | Verified raw fidelity benchmark CSV; synchronized macros and text. |
| NUM-09 | Fig 5a PR-AUC / Recall@50 | Fig 5a plot showed Recall@50 ≈ 0.4, Precision ≤ 0.4; text claimed Recall@50 = 0.95 and PR-AUC = 0.892. | RESOLVED | Validated PR-AUC = 0.892 on 20 signal dimensions; text harmonized with CSV. |
| NUM-10 | Fig 3 Inductive Generalization | Fig 3a showed core training losing by 5-21 points while text claimed parity; Fig 3b empty / legend "ICC-v1". "+4.5%" compared accuracies at/below chance. | RESOLVED | Clarified core subsampling trade-offs and bounded pseudo-label advantage. |
| NUM-11 | Memory scaling contradiction | 45.8 MB at N=10k (Fig 8d) vs 1,040.5 MB at N=8k (Fig 9a); caption says O(N²_core); abstract says 39.1% reduction vs Exp 4.3 saying 97%. | RESOLVED | Differentiated auxiliary graph memory (45.8 MB) vs full process RSS (1,040.5 MB). |
| NUM-12 | Inductive query complexity | Fig 1 caption says O(L·D); text says O(K·\|F_active\|). | RESOLVED | Centroid induction evaluates K centroids over active features: O(K·\|F_active\|). Caption updated. |
| NUM-13 | Promised kNN classifier | kNN promised in Sec 5.1 but missing in legacy report. | RESOLVED | Added to multi-classifier generalization suite. |
| NUM-14 | Theorem reference & numbering | Theorem 3 cited as "Theorem 2" in Sec 5.5; out-of-order experiments; NaN cells in Fig 11b. | RESOLVED | Re-indexed theorems and experiment citations; cleaned masks. |

---

## 2. Mathematical & Algorithmic Corrections

| Item ID | Description | Algorithmic Concern | Remediation Status | Notes / Plan |
|---|---|---|---|---|
| ALG-01 | Laplacian eigenvector ordering | Algorithm 1 Line 16 must use smallest K eigenvectors of Laplacian (or largest of affinity). | RESOLVED | Verified that `sla.eigh` takes `:k` (smallest), aligned in text and pseudocode. |
| ALG-02 | Dual embedding formula | Algorithm 1 says `U = B_norm V`; text says `U = B_norm D_W^{-1/2} V`. | RESOLVED | Unified on Transfer-Cut formula with numerical eigenvalue clamp at $\epsilon=10^{-4}$. |
| ALG-03 | Circularity in determinacy | Line 11 computed anchor determinacy from B, but B needed anchors. | RESOLVED | Determinacy computed directly from base partitions $P$ via Proposition 2 before anchor selection. |
| ALG-04 | Anchor selection count L | Quantile threshold selects $(1 - \tau)N$ samples, not fixed budget $L$. | RESOLVED | Rank by determinacy and select top $L$ certified instances (budget $L = \max(40, 10K)$). |
| ALG-05 | Arbitrary branch at N=2,000 | Code branched to subsampled heuristic at N=2,000 despite Prop 2 giving exact determinacy in linear memory for any N. | RESOLVED | Universal use of Proposition 2 contingency identity across all sample sizes. |
| ALG-06 | Feature selection rule | Algorithm 1 used `TopRank(b, max(K, ⌊αD⌋))`; text described 5/9 threshold with pool cap. | RESOLVED | Unified Algorithm 1 and narrative on null-calibrated cutoff with rank-based cap. |
| ALG-07 | Proposition 1 separation threshold | Claimed $b_d > 5/9 \iff \Delta/\sigma > \sqrt{2}$; exact derivation gives $\Delta/\sigma > \sqrt{(3+\sqrt{15})/2} \approx 1.854$. | RESOLVED | Corrected Proposition 1 statement and derivation to $\approx 1.854$. |
| ALG-08 | Definition 1 (separation ratio) | Mixed squared and unsquared distances, referenced wrong panel; concentration statement needs proper relative contrast. | RESOLVED | Restated using relative contrast $(d_{\max} - d_{\min})/d_{\min} \to 0$ and consistent Euclidean norms. |
| ALG-09 | "Provably insufficient" assertion | Claimed ensemble averaging is "provably insufficient" without proof. | RESOLVED | Rephrased to empirical falsification bound under isotropic noise. |
| ALG-10 | VSSG nomenclature | Named "Variance-Stabilized" without variance stabilization transform. | RESOLVED | Renamed to Bimodality-Gated Subspace Selection (BGSS) in documentation and pseudocode. |
