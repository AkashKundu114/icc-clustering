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

---

### [2026-10-21] DEC-07: Progress on Fix Pass B Tasks B1-B5, B7, B9, B10
- **Context:** Executed systematic remediation of manuscript defects B1–B5, B7, B9, and B10 under zero-hallucination and evidence-based traceability rules.
- **Resolutions:**
  1. **Task B1 (Citations):** Verified all 34 BibTeX references with DOIs; resolved 100% of `[?]` citation markers; Tectonic compilation confirmed zero undefined citations.
  2. **Task B2 (Fig 7 & Stats):** Recalculated Nemenyi critical difference $CD = 3.219 \sqrt{11 \times 12 / (6 \times 13)} = 4.19$; synchronized Fig 17; removed legacy process notes.
  3. **Task B3 (Subgroup Arithmetic & Baseline Claims):** Corrected biomedical subgroup ($D/N > 20$) mean ARI to 0.238 and median to 0.057; rewritten comparisons against strongest baseline (FastMVC, $+0.388$ gain on SRBCT).
  4. **Task B4 (Table 3 Dimensions & Scaling):** Fully expanded Table 3 to show all 11 algorithms; reconciled subsampled dimensions ($N, D, K$) against Fig 6 and benchmark caches.
  5. **Task B5 (Single-Protocol Memory & Runtime):** Re-measured sample scaling across $N \in [200, 10000]$ and 5 seeds under a unified protocol; explicitly decoupled raw data array storage ($800\text{ MB}$ double / $400\text{ MB}$ single at $N=10^6$) from auxiliary consensus graph memory ($3.06\text{ MB}$ at $N=10^4$, a $99.6\%$ reduction over $762.8\text{ MB}$ dense graph) and total process peak RSS ($292.1\text{ MB}$ vs. $2894.2\text{ MB}$, an $89.9\%$ reduction); synchronized all macros and Fig 18.
  6. **Task B7 (BGSS Failure Modes & Simulation):** Quantified finite-sample detection power ($P=0.49$ at $N=60$ to $P=0.97$ at $N=1000$); updated empirical Leukemia gene count to verified 1,275.
  7. **Task B9 (Figure Discrepancies Audit):** Reconstructed Fig 0/1 with BGSS nomenclature and tight bounding; corrected line 141 $\rho_{\text{sep}}$ reference; removed misleading annotation in Fig 10; aligned Exp 2.1 text and Fig 5 caption with exact Precision@K / Recall@K metrics.
  8. **Task B10 (Naming & Notation):** Fully unified terminology to BGSS and notation $\hat{b}_d$ across text, algorithms, and figures.
  9. **Pre-Registration (PREREG_B.md):** Fully drafted for Human Gate A sign-off before running computational jobs for Tasks B6 and B8.

---

### [2026-10-21] DEC-08: Human Gate A and Gate B Approvals
- **Context:** Formal interactive human approval obtained for Gate A and Gate B.
- **Approvals & Decisions:**
  1. **Gate A Approved:** Pre-registration document `LOOP/PREREG_B.md` formally signed off by human lead author (Akash Kundu). Authorization granted to execute the pre-specified computational runs for Task B6 (2x2 factorial ablation across 6 high-D datasets) and Task B8 (fair baselines suite).
  2. **Gate B Approved (AI Disclosure):** Option B ("AI-Assisted Research Workflow & Drafting with Human Verification") selected and integrated into line 547 of `springer_manuscript/main.tex`, satisfying Springer Nature AI editorial policy with full transparency.
  3. **Gate B Approved (Author Metadata):** Author directory, affiliations, institutional emails, and CRediT contribution taxonomy confirmed in `LOOP/AUTHOR_CHECKLIST.md`.

