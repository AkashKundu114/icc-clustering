# Independent Research Audit & Adversarial Verification Reports

This directory archives the complete, unvarnished documentation from the independent adversarial research audit of the **Invariant Core Consensus (ICC-v2)** codebase, conducted across remediation stages A1–A4, E1, and E3.

---

## 1. Audit Report Architecture

| Report | Title / Scope | Key Findings & Remediation |
| :--- | :--- | :--- |
| [`00_executive_review.md`](./00_executive_review.md) | Executive Summary | Initial audit assessment, claim verification criteria, and prioritized remediation milestones. |
| [`01_repository_inventory.md`](./01_repository_inventory.md) | Repository Inventory | Exhaustive catalog of code, configs, test suites, datasets, and committed experimental artifacts. |
| [`02_claim_evidence_matrix.md`](./02_claim_evidence_matrix.md) | Claim-Evidence Matrix | Systematic mapping of every theoretical and empirical claim in documentation to underlying evidence. |
| [`03_mathematical_audit.md`](./03_mathematical_audit.md) | Mathematical Audit | Proof audit of finite-sample Sarle Bimodality Coefficient, Bipartite Transfer-Cut equivalence, and anchor bounds. |
| [`04_algorithm_code_traceability.md`](./04_algorithm_code_traceability.md) | Code Traceability | Verification of algorithmic alignment between LaTeX equations and NumPy/SciPy implementations. |
| [`05_novelty_and_related_work.md`](./05_novelty_and_related_work.md) | Prior Art & Novelty | Differentiation against LWEA/LWGP (Huang et al.), FastMICE (TKDE 2023), and bipartite spectral consensus. |
| [`06_experiment_audit.md`](./06_experiment_audit.md) | Experiment Audit | Re-computation of benchmark matrices, detection of rank dynamics, and discovery of the 5%–15% pool window. |
| [`07_red_flag_register.md`](./07_red_flag_register.md) | Defect Register | Systematic tracking and verification log of all identified empirical anomalies and resolution steps. |
| [`08_experiment_plan.md`](./08_experiment_plan.md) | Remediation Plan | Formal specification of verification experiments: controls (A2), embedding checks (A3), baselines (A4), and pool curve (E3). |
| [`09_remediation_roadmap.md`](./09_remediation_roadmap.md) | Remediation Roadmap | Chronological execution timeline, parameterization updates, and calibration of scientific claims. |
| [`10_final_reviewer_report.md`](./10_final_reviewer_report.md) | Reviewer Report | Final adversarial review assessment, evaluating defensibility and publication readiness for IEEE TKDE. |
| [`11_verification_log.md`](./11_verification_log.md) | Verification Log | Hash-verified execution records of test sweeps, patch integrations, and numerical replications. |
| [`remediation_reports/`](./remediation_reports/) | Technical Defense Reports | Author's mathematical defense notes, closed-form derivations, and reproducibility proofs. |

---

## 2. Accompanying Experimental Code & Data

All executable scripts and numerical CSVs produced during the audit are located in:
* **Scripts:** [`experiments/audit_controls/src/`](../../experiments/audit_controls/src/)
  * `a2_controls.py`, `a2_filter_controls.py`, `a2_random_control.py` (Feature screening controls)
  * `a3_embedding.py`, `a3_paths.py` (Principal eigenspace and branch equivalence checks)
  * `e3_pool_curve.py` (Pool-size sensitivity sweep: BC-ranked vs. random control)
  * `e3_label_free_selector.py`, `e3b_label_free_selector.py` (Unsupervised pool-size selection evaluation)
  * `e5_exp1_rerun.py`, `e5_missing_rerun.py` (Re-runs of Exp1 multi-classifier sweep and missing-data benchmarks)
  * `e6_scaling_one.py` (Per-process scaling benchmark testing linear runtime and RSS memory growth)
  * `e1_extended_benchmarks.py` (Extended 21-dataset multi-domain benchmark suite)
* **Results Data:** [`experiments/audit_controls/data/`](../../experiments/audit_controls/data/)
  * `a2_syn.csv`, `a2_real.csv`, `a2_filter_controls.csv`, `a2_random_control.csv`
  * `e3_pool_curve.csv`, `e3_label_free_selector_eval.csv`, `e3_label_free_selector_summary.csv`, `e3b_selector.csv`
  * `e5_exp1_pseudolabel_rerun.csv`, `e5_missing_rerun.csv`
  * `e6_scaling.csv` (Empirical scaling measurements for $N \in [500, 32{,}000]$)
  * `e1_extended_benchmarks.csv`, `e1_extended_summary.csv`
