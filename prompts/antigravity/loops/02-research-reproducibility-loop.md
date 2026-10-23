# Loop: Multi-Subagent Research Reproducibility & Claim Audit

Use this loop for scientific, algorithmic, and data-driven repositories to ensure zero empirical fabrication and complete claim-to-evidence traceability.

---

## Operating Budget & Roles
- **Maximum Iterations:** 3 iterations per run.
- **Subagent Roles:**
  - `Research Auditor`: Traces manuscript claims and LaTeX tables back to raw result registries.
  - `Data Integrity Auditor`: Verifies immutable raw dataset boundaries, checksums, and train/test separation.
  - `Code Engineer`: Applies focused fixes to metrics, logging, seed reservations, or configuration capture.

---

## Iteration Protocol

### 1. Identify Reproducibility Gap
Deploy the `Research Auditor` to select one specific gap:
- Untracked random seed or missing configuration snapshot.
- Unverifiable numerical claim or missing macro in numbers file.
- Leakage between train/validation and test splits.
- Outdated benchmark table or non-reproducible figure.

### 2. Evidence Gathering
Isolate the exact line in code, dataset manifest, or manuscript prose. Capture the discrepancy with concrete evidence before editing.

### 3. Surgical Remediation
- Fix configuration serialization, seed logging, or split logic.
- Synchronize numbers macro files (`numbers.tex`, `results.json`) with the verified experiment registry.
- Do not edit empirical values manually. All updates must originate from executable scripts.

### 4. Verification Checkpoint
- Run the experiment or synthetic verification script:
  ```bash
  python -m experiments.target_experiment.run
  pytest tests/test_metrics.py
  ```
- Verify that no failed runs were erased, baselines were evaluated fairly, and no synthetic values were injected.

### 5. Log & Diff Audit
Record findings, exact commands, and verified status in `prompts/antigravity/logs/`.
