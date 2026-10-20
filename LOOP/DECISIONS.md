# Record of Decisions (LOOP/DECISIONS.md)

This log records every architectural, algorithmic, and statistical decision made during the autonomous improve-verify loop, along with explicit reasons and timestamps.

---

### [2026-10-17] DEC-01: Gating Scope Decision for Study 3'
- **Context:** Bounded unimodal features (F3 Uniform, F4 Beta(3,1)) produce $\text{FDP} \approx 0.92\text{--}0.98$ under Silverman Critical Bandwidth (SCB) and Skew-Normal (SN) null generators because smoothing adds tails and suppresses decoy kurtosis.
- **Alternatives Considered:**
  1. Option (a): Redesign null generator with boundary-corrected or compact kernels.
  2. Option (b): Switch primary statistic from Sarle's BC to Hartigan's Dip test (collapses novelty into existing literature).
  3. Option (c): Restrict confirmatory scope to unbounded continuous and count nuisance (F1 Gaussian, F2 Student-$t$, F5 log-counts) and document bounded support as a boundary-bias scope limit.
- **Decision:** **Option (c) adopted.** Confirmatory H1–H3 claims focus on F1, F2, F5. Bounded compact support is documented transparently in `LOOP/DEVIATIONS.md` and the manuscript as a fundamental limitation of smooth-kernel null generators.

---

### [2026-10-17] DEC-02: Execution of Pre-Registration Kill Rule A7 (Downstream Clustering)
- **Context:** Tier-A real-world benchmarks ($D/N > 20$: CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT) evaluated across 10 pre-registered seeds for Hypothesis H4.
- **Observed Evidence:**
  - Vs. G2 (Fixed BC): Mean ARI difference $-0.0035$, bootstrap 95% CI $[-0.0169, +0.0101]$, non-negative count 2/6, exact sign-flip $p = 0.6875$.
  - Vs. G4 (Hartigan Dip Matched-k): Mean ARI difference $-0.0319$, bootstrap 95% CI $[-0.0810, +0.0044]$, non-negative count 3/6, exact sign-flip $p = 0.8281$.
- **Decision:** All four conjunctive criteria failed against both comparators. Per Kill Rule A7, **the claim that NCG improves downstream clustering over heuristic gating is formally withdrawn**. NCG is repositioned strictly as a finite-sample false-discovery control diagnostic / feature filter.

---

### [2026-10-17] DEC-03: Single Study Scope Enforcement (Reality Clause 4)
- **Context:** The prompt mandates: *"One manuscript, one main claim (at most three contributions). Do not merge separate studies into one paper."*
- **Decision:** Keep the ICC-v2 paper and Study 1' (Amortized Conformal Clustering Sets) strictly separated. Study 1' maintains its own pre-registration and repository harness, and will not be conflated with the ICC-v2 manuscript.

---

### [2026-10-17] DEC-04: Target Journal Selection
- **Context:** Identified candidate Springer Nature venues for regular research article submission.
- **Decision:** Selected *Pattern Analysis and Applications* (PAAP) as primary target venue, with *Data Mining and Knowledge Discovery* (DAMI) as alternative.

---

### [2026-10-19] DEC-05: Confirmatory Synthetic Grid Execution on GPU
- **Context:** Ran 18,000 Monte Carlo replicates for Study 3' across 60 cells on RTX 5060 GPU with memory paging limits.
- **Decision:** Results confirmed H3 (Power $\ge 0.80$ in 91.7% of separable cells) and identified H1 boundary limit under heavy tails (66.7% pass rate).

---

### [2026-10-20] DEC-06: Initiation of Fix Pass B
- **Context:** Detailed audit of `springer_manuscript/main.pdf` revealed 10 unresolved citation markers (`[?]`), table column truncation, missing subgroup CD (~6.16), Nemenyi CD formula calculation mismatch (4.19 vs 4.21), contradictory memory/runtime statements, unverified ablation parity, and inaccurate statements regarding unimodal skewness inflating the bimodality coefficient.
- **Decision:**
  1. Reopened ISSUE-01..06 in `LOOP/STATE.json`.
  2. Registered ISSUE-09 through ISSUE-20 covering tasks B1 to B12.
  3. Removed `GATE_4_READY` status; set phase to `FIX_PASS_B` and active gate to `GATE_A`.
  4. Work organized strictly under `LOOP/ITERATIONS/passB/`.
