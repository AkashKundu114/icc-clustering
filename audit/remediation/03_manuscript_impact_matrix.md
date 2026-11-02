# Manuscript Impact and Text Revision Matrix: DMKD Submission

**Target Repository**: `AkashKundu114/icc-clustering`  
**Current HEAD**: `7ddbe8301b8d27c94f388c40acbc88b0dee82723`  
**Target Manuscript**: *Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Noise* (`main.tex`, `numbers.tex`)  
**Audit Component**: Phase 7 — Scientific Claim Tracking & Manuscript Alignment  

---

## 1. Executive Summary of Manuscript Impacts

The forensic audit identified multiple instances where text, equations, or tables in `main.tex` and `docs/theory.md` conflict with empirical microdata or mathematical theory. Submitting the manuscript without correcting these sections introduces catastrophic peer-review risk.

This document itemizes every affected section, equation, table, and macro definition, providing the required text modifications, redactions, or reframings.

---

## 2. Manuscript Revision Matrix (`main.tex` & `numbers.tex`)

| Manuscript Section / Element | Current Text / Claim | Empirical Forensic Finding | Mandatory Remediation Action | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Section 1 (Introduction)**<br>`main.tex: L88-92` | Claims GAC combines BGSS feature gating with determinacy-certified anchors to boost consensus accuracy over traditional consensus clustering. | Factorial ablation shows certified core anchors add no statistically significant accuracy lift over uniform random anchors ($\Delta = +0.019, p = 0.844$). | Reframe the core contribution: BGSS provides the accuracy recovery, while bipartite anchoring provides $\mathcal{O}(NL)$ memory scalability. | **REVISION REQUIRED** |
| **Section 4.2 (Anchor Selection)**<br>`main.tex: L240-255` | "Determinacy-filtered anchors isolate invariant core geometry and prevent noisy samples from corrupting the consensus graph cut." | Empirical ARI for Random Anchors ($0.198$) is statistically indistinguishable from Certified Core Anchors ($0.217$). | Explicitly state that while determinacy certification provides a principled heuristic, empirical accuracy is dominated by feature gating, with bipartite anchoring serving as an asymptotic compression mechanism. | **REVISION REQUIRED** |
| **Section 5.3 / Unknown $K$**<br>`main.tex` & `docs/theory.md: Sec 3` | Proposes ICC-AutoK using PAC ambiguity interval on anchor co-association matrix to select true $K^*$. | 100% failure rate across 510 trials; inner products concentrate below 0.10, forcing $\text{PAC} \equiv 0.0$ and collapsing to $K_{min}=2$. | **RETRACT** claim of robust automated model order selection. Omit AutoK from the main paper or report it as an open theoretical limitation requiring dynamic threshold calibration. | **RETRACTION REQUIRED** |
| **Section 6 (Computational Scalability)**<br>`main.tex: Table 4` & runtime text | Reports that Standard Consensus requires $0.3662\,\text{s}$ while ICC-v2 takes $0.0039\,\text{s}$ (a claimed ~94x speedup). | Standard Consensus runs in $0.1210\,\text{s}$ (3x faster than reported) with perfect $\text{ARI}=1.0$, while ICC-v2 achieved $\text{ARI}=0.4396$ on Seed 101. | Update runtime table with verified wall-clock times. Emphasize asymptotic memory reduction ($\mathcal{O}(NL)$ vs $\mathcal{O}(N^2)$) rather than unverified sub-second wall-clock speedups. | **CORRECTION REQUIRED** |
| **Section 7 (Ablation Study)**<br>`main.tex: Table 5` & lines 710-740 | Presents V5 (Full ICC-v2, $0.217$) and V4 (BGSS + Random Anchor, $0.198$) as progressive improvements. | $95\%\text{ CI } [-0.039, +0.082]$, Wilcoxon $p = 0.844$ confirms the null hypothesis. | Explicitly report the $p$-value and confidence interval. State transparently that the difference is statistically null. | **REVISION REQUIRED** |
| **`numbers.tex` Macros**<br>Lines 83–84 | `\AblationHighDSubgroupBgssRandomAnchor` ($0.198$)<br>`\AblationHighDSubgroupFullIccVTwo` ($0.217$) | Values are empirically accurate, but text lacks statistical significance context. | Add companion macros: `\AblationAnchorLiftDelta{0.019}`, `\AblationAnchorWilcoxonP{0.844}`, `\AblationAnchorCIPercent{[-0.039, +0.082]}`. | **MACRO UPDATE REQUIRED** |
| **`docs/theory.md: Sec 9.1`**<br>(Conformal Prediction Sets) | Claims CICC provides valid distribution-free coverage guarantees for clinical patient phenotyping and disease subtyping. | Empirical coverage against true clinical pathology collapses to $37.0\%$ (SRBCT) and $62.2\%$ (Leukemia), with $20\%$ toxic misclassifications. | **STRICT QUALIFICATION**: State that conformal coverage holds strictly for the clusterer's internal inductive pseudo-labels, NOT external clinical pathology. Add clinical diagnostic warning. | **REVISION REQUIRED** |
| **`docs/theory.md: Sec 9.2`**<br>(Target-Decoy / Knockoff Gating) | Claims Model-X knockoff framework controls False Discovery Rate (FDR) below user target $\alpha$. | Uses independent Gaussian noise (violating exchangeability); fallback bug at line 122 selects noise; 100% empirical FDR under pure null; dead code in `inductive.py`. | **RETRACT** claim of Model-X FDR control until true second-order Gaussian knockoffs are implemented and connected to `inductive.py`. | **RETRACTION REQUIRED** |

---

## 3. Recommended Text Revisions for `main.tex`

### 3.1 Revision to Section 4.2 (Anchor Graph and Bipartite Cut)
**Current Draft Formulation**:
> "By restricting the bipartite graph to determinacy-certified invariant core instances, GAC eliminates noisy boundary samples from corrupting the consensus spectral cut, yielding superior cluster recovery over random anchor selection."

**Mandatory Corrected Formulation**:
> "By restricting the bipartite consensus graph to $L \ll N$ anchors ($B \in \mathbb{R}^{N \times L}$), GAC reduces the consensus eigensystem from $\mathcal{O}(N^2)$ to $\mathcal{O}(N L)$ auxiliary memory. While core instances can be certified using the linear determinacy identity $\sigma_i$, controlled factorial ablation reveals that certified anchors provide a statistically null accuracy lift over uniform random anchors ($\Delta = +0.019$, Wilcoxon $p = 0.844$, $95\%\text{ CI } [-0.039, +0.082]$). Thus, the primary role of the anchor graph in GAC is computational and memory compression, while signal recovery is driven by variance-stabilized feature gating."

### 3.2 Revision to Abstract and Conclusion Regarding Overall Benchmark Performance
The manuscript must accurately reflect the omnibus benchmark reality:
> "Across 13 multi-domain benchmark cohorts, GAC achieves a grand mean ARI of $0.152$ (median $0.055$). Its principal strength emerges in high-dimensional biomedical regimes with extreme noise ($D \gg N$), where it ranks 2.17 among baseline methods. However, in non-sparse or low-dimensional regimes, classical consensus clustering and deep clustering baselines remain competitive."
