# Goal: Hypothesis, Theorem & Claim-to-Evidence Matrix Audit

Deploy this goal to perform an exhaustive audit verifying that every mathematical assertion, theorem, proposition, and empirical claim in the repository is strictly grounded in verifiable evidence.

---

## Assigned Subagent Personas
1. **Mathematical Auditor (`roo_ask` / Domain Specialist)**: Inspects theoretical proofs, bounds, matrix identities, and notation consistency.
2. **Empirical Verifier (`roo_reviewer`)**: Traces numerical claims in the manuscript back to execution logs and frozen registries.
3. **Traceability Engineer (`roo_coder`)**: Binds free-floating values to single-source macro definitions.

---

## Audit Checklist & Verification Protocol

### 1. Theoretical Proof & Proposition Audit
- Inspect all formal propositions, theorems, and lemmas in `docs/` and `paper/`.
- Verify mathematical conditions:
  - Are dimensionality constraints explicit ($N > D$, or $D \gg N$)?
  - Are eigenvalues, matrix ranks, and PSD (positive semi-definite) assumptions rigorously maintained?
  - Are edge-case boundaries (e.g. zero-inflation, singular matrices, uncalibrated gating thresholds) proved or acknowledged as limitations?

### 2. Empirical Hypothesis Validation
For each stated hypothesis ($H_1, H_2, \dots$):
- **Criterion Check:** Does the corresponding experiment isolate the tested variable with appropriate negative controls?
- **Falsification Threshold:** Is there an explicit mathematical condition for what constitutes hypothesis failure?
- **Seed Invariance:** Are conclusions consistent across random seeds (at least 5–10 distinct seeds), rather than cherry-picked from an anomalous seed?

### 3. Claim-to-Evidence Macro Traceability
- Locate all numerical figures, accuracy percentages, runtimes, and p-values cited in paper prose and tables.
- **Strict Single-Source Verification:**
  - Verify every number originates from a centralized macro file (e.g., `paper/numbers.tex`) populated directly by frozen result dictionaries (e.g., `results/results.json`).
  - Flag any hardcoded numbers in LaTeX tables or text as **P0 Violations**.

---

## Deliverables
- **Claim-to-Evidence Matrix:** A markdown table listing:
  | Claim ID | Paper Citation / Line | Stated Claim / Value | Supporting File & Function | Macro Name | Audit Status (`VERIFIED` / `UNVERIFIED` / `CONTRADICTED`) |
- **Remediation Plan:** Surgical changes required to eliminate ungrounded statements or parameterize hardcoded values.
