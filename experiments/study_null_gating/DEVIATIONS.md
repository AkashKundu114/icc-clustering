# DEVIATIONS AND SCOPE-LIMIT LOG: STUDY 3' (NCG)

**Document Reference:** `experiments/PRE_REGISTRATION_v1.0.md`  
**Protocol Version:** v1.0 (Frozen at commit `0f1f12370a6541b843588c597e2812800e768b0e`, Git Tag `study3p-1p-prereg-frozen`)  
**Date:** October 17, 2026  
**Status:** ACTIVE LOG  

---

## 1. Deviation / Scope Limit Registration

### `DEV-01: Scope Limit on Compact / Bounded-Support Nuisance Families (F3, F4)`

- **Date:** October 17, 2026
- **Affected Hypotheses:** H1 (FDR control omnibus rate), H2 (Fixed-cutoff failure on F3/F4).
- **Rule Invoked:** Pre-Registration Section A7 (Kill and Pivot Rules), Bullet 3:
  > *"If SCB fails on F3/F4 and SN fails too, report that unimodal-null calibration is inadequate for bounded unimodal features and state the scope limit."*
- **Observed Empirical Evidence:**
  - On **Uniform $[- \sqrt{3}, \sqrt{3}]$ (F3)**: Target $\text{BC} = 0.5505$. Silverman critical bandwidth (SCB) KDE smoothing rounds boundary discontinuities, inflating decoy kurtosis from $1.8$ toward $3.0$, depressing decoy $\text{BC}$ to $0.4480$. The resulting contrast statistic $W_d = s_d - \widetilde{s}_d \approx +0.10 > 0$ triggers systematic false positive discovery ($\text{FDP} \to 0.980$).
  - On **Beta(3, 1) J-shaped (F4)**: Target $\text{BC} = 0.5745$ vs. Decoy $\text{BC} = 0.4550 \implies W_d \approx +0.12 > 0$ ($\text{FDP} \to 0.978$).
  - **Secondary Null (Skew-Normal MLE)**: Decoy $\text{BC} = 0.3446 \implies W_d \approx +0.206$, yielding even greater false discovery inflation.
- **Decision & Action:**
  1. Primary confirmatory grid execution is focused on the **validated unbounded continuous and count nuisance families (F1: Gaussian, F2: Student-$t$, F5: $\log(1+x)$ Poisson mixture)**, where $\text{FDP} \le 0.10$ and $\text{Power} \ge 0.95$ are fully confirmed.
  2. Bounded-support unimodal calibration (F3, F4) is formally documented as an intrinsic boundary-bias limitation of smooth-kernel null generators.
  3. Hypothesis H2 is confirmed on F3 and F4: the current fixed-cutoff rule ($BC \ge 5/9$) suffers catastrophic false discovery inflation ($\text{FDP} = 0.867$ on F3 and $0.867$ on F4).
