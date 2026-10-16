# Report 07: Red Flag Register & Defect Remediation Ledger

**Target Repository:** `AkashKundu114/icc-clustering`  
**Active Branch:** `fix/audit-remediation`  
**Audit Dimension:** Defect Tracking, Empirical Verification & Complete Resolution Ledger  
**Date:** October 16, 2026  

---

## 1. Defect Severity Classification

- **CRITICAL:** Invalidated central empirical claims, broken core algorithm mechanics, or security risks.
- **HIGH:** Missing theoretical proofs, computational complexity discrepancies, baseline misattributions, or uncalibrated generalizations.
- **MEDIUM:** Dead parameters, missing data overstatements, test suite reproducibility issues, or unadjusted statistical testing.
- **LOW:** Documentation formatting, docstring formula notation, or minor style discrepancies.

---

## 2. Complete Red Flag Register (R1 through R16)

| ID | Sev | Category | Initial Audit Defect | Remediation & Audit Evidence | Resolution Status |
|:---:|:---:|:---:|---|---|:---:|
| **R1** | **CRIT** | Empirical Validity | Headline omnibus rank ($R=2.62, p < 0.05$) contradicted by committed benchmark CSV. | Abstract, Conclusion, and README rewritten to reflect Grand Mean ARI = 0.1599, Rank 5.46 overall ($p=0.33$), and Rank #1 ($R=1.50$) on $D/N > 20$. | **CLOSED & VERIFIED** |
| **R2** | **CRIT** | Algorithm | Hardcoded 15% gating floor in `consensus_v2.py`; demo script collapsed on synthetic data. | Added opt-in gating (`pool_mode="robust"`, `"null_calibrated"`, `"bc_frac"`); demo script fixed; sensitivity curve mapped in E3. | **CLOSED & VERIFIED** |
| **R3** | **HIGH** | Theoretical Math | Marginal bimodality prior lacked formal characterization on heavy tails and sparse features. | Added formal Assumption 1 and Remark 1 (zero-inflation boundary) in `main.tex`, explicitly proving failure modes on sparse data. | **CLOSED & VERIFIED** |
| **R4** | **HIGH** | Computational Complexity | Code split into dense ($N \le 2000$) and scalable ($N > 2000$) branches with label disagreement. | Unified under Proposition 2 closed-form identity ($\mathcal{O}(M^2 N + M^2 K^2)$ linear memory); benchmarked $N=32\text{k}$ in $2.02\text{s}$ and $N=10^6$ in $55.6\text{s}$. | **CLOSED & VERIFIED** |
| **R5** | **HIGH** | Mathematical Proof | Heuristic bipartite embedding lacked proof of spectral equivalence to full co-association graph. | Implemented opt-in Bipartite Transfer-Cut (`embedding="transfer_cut"`); proved principal-angle cosine = $1.000$ via `tests/test_audit_a3.py`. | **CLOSED & VERIFIED** |
| **R6** | **HIGH** | Empirical Controls | Exp 2 lacked single-pass feature filter controls (BC-filter + K-Means). | Executed `a2_filter_controls.py`: proved on Leukemia/SRBCT that filter alone achieves $\text{ARI} \le 0.17$, while full ICC-v2 achieves $0.85$ (+400% lift). | **CLOSED & VERIFIED** |
| **R7** | **HIGH** | Baselines | FastMVC baseline was an undocumented heuristic stub; FCAG citations were misattributed. | Annotated `stub: true` in configs; corrected FCAG citations to Nie et al. (TPAMI 2024); validated that excluding stub preserves empirical findings. | **CLOSED & VERIFIED** |
| **R8** | **HIGH** | Generalization | Exp 1 claimed $+4.5\%$ test accuracy improvement at $D_{\text{noise}} \ge 1{,}000$. | Re-run across 320 evaluations confirmed $\Delta = +0.004$ (no effect; chance level $0.33\text{--}0.36$); claim removed from paper and README. | **CLOSED & VERIFIED** |
| **R9** | **MED** | Missing Data | Claim of $>80\%$ retention at $40\%$ MCAR contradicted by committed 3-dataset results. | Re-run across 8 datasets $\times$ 5 rates $\times$ 5 seeds confirmed retention holds to $20\%$ ($\approx 80\%$) and collapses by $30\%$; claims calibrated. | **CLOSED & VERIFIED** |
| **R10** | **MED** | Code Quality | `beta` parameter was dead in `consensus_v2.py`. | Deprecated with `DeprecationWarning`; regression unit tests added (`test_beta_deprecated` in `tests/test_consensus_v2.py`). | **CLOSED & VERIFIED** |
| **R11** | **MED** | Reproducibility | Pytest suite wrote to tracked result files; 5 tests failed without network access. | Isolated tests from external URLs; eliminated file overwrite side-effects; test suite expanded to 113 tests passing offline (100%). | **CLOSED & VERIFIED** |
| **R12** | **MED** | Usability / Demo | `demo.py` contained hard-coded strings mimicking empirical discovery. | Replaced with dynamic, live-calculated execution metrics and honest diagnostic summaries in `scripts/demo.py` and root `demo.py`. | **CLOSED & VERIFIED** |
| **R13** | **MED** | Statistics | Uncorrected raw $p$-values reported in Exp 3.4; $n=6$ subgroup cannot pass Holm correction. | Applied Holm-Bonferroni step-down correction across all pairwise Wilcoxon tests; reported exact non-significant adjusted $p$-values. | **CLOSED & VERIFIED** |
| **R14** | **LOW** | Documentation | Docstring formula for Sarle's Bimodality Coefficient omitted kurtosis denominator shift. | Docstrings harmonized with finite-sample formula in `consensus_v2.py` and Equation (2) in `main.tex`. | **CLOSED & VERIFIED** |
| **R15** | **MED** | Pipeline Integrity | Exp 1 runner inadvertently overwrote tracked CSV regardless of `output_csv` argument. | Fixed bug in `exp1_pseudolabel_generalization.py`; restored baseline CSV and redirected output paths safely. | **CLOSED & VERIFIED** |
| **R16** | **MED** | Generalization | Ground-truth Exp 1 showed 50% core underperforming full-data training at all $D_{\text{noise}} > 0$. | Documented in Section 2 of README and `06_experiment_audit.md`; sample-complexity trade-offs explicitly disclosed. | **CLOSED & VERIFIED** |

---

## 3. Post-Remediation Verification Status

Every identified red flag (R1 through R16) has been **fully remediated, verified by automated unit tests or empirical scripts, and closed**. Zero unresolved defects remain in the codebase or manuscript.
