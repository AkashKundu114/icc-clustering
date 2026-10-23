# Record of Deviations (LOOP/DEVIATIONS.md)

**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*

### DEV-01: Boundary-Bias Scope Limit on Compact Supports (F3, F4)
- **Date:** 2026-10-17
- **Source:** Development seed validation (`dev_validate_ncg.py`, `LOOP/dev/ncg_one.py`, `LOOP/dev/bc_check.py`).
- **Nature of Deviation:** Pre-Registration Section A1 H1 originally specified error control across all five nuisance families F1-F5. Under continuous kernel smoothing (SCB and Skew-Normal), compact bounded supports (Uniform $[0,1]$ and Beta$(3,1)$) systematically violate the exchangeability condition between target and decoy features because smoothing introduces infinite tails, depressing decoy Sarle BC below target BC.
- **Affected Outcomes:** FDP control on F3 and F4 fails ($\text{FDP} \to 0.92\text{-}0.98$).
- **Remediation & Action:** Per Section A7 pivot rule and DEC-01, confirmatory claims are restricted to unbounded continuous and count nuisance (F1, F2, F5) where $\text{FDP} \le 0.10$ holds strictly. Bounded support is reported as an explicit boundary-bias limitation.

--

### DEV-02: Withdrawal of Downstream Clustering Performance Claims (H4 Failure)
- **Date:** 2026-10-17
- **Source:** Tier-A confirmatory real-data evaluation (`experiments/study_null_gating/run_tier_a_benchmark.py`).
- **Nature of Deviation:** Hypothesis H4 required mean ARI improvement $\ge +0.02$, bootstrap lower CI $> 0$, $\ge 5/6$ non-negative datasets, and sign-flip $p \le 0.025$. Observed results failed on all four criteria against both G2 (mean diff $-0.0035$) and G4 (mean diff $-0.0319$).
- **Affected Outcomes:** Downstream clustering superiority claims in Tier-A biological transcriptomes.
- **Remediation & Action:** Enacted Kill Rule A7. All claims of downstream clustering improvement are withdrawn. NCG is reported as an error-calibrated feature diagnostic and filter.
