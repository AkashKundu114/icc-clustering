# 06 — Remediation Plan & Task Dependency Roadmap

**Auditor / Coordinator:** Principal Research Engineer  
**Date:** October 13, 2026  
**Target:** Journal Submission Readiness  

---

## 1. Remediation Tasks & Dependencies

```
[Phase 0: Recon & Freeze] (COMPLETED)
       │
       ▼
[Phase 1: Math & Algorithmic Corrections] (COMPLETED)
  ├── ALG-01: Eigenvector ordering (sla.eigh [:k]) ──> COMPLETED
  ├── ALG-02: Transfer-Cut embedding formula ───────> COMPLETED
  ├── ALG-03: Proposition 1 derivation (1.854) ──────> COMPLETED
  └── ALG-04: Proposition 2 contingency identity ────> COMPLETED
       │
       ▼
[Phase 2: Single Source of Truth & Assets] (COMPLETED)
  ├── make_paper_assets.py generates numbers.tex ───> COMPLETED
  └── tools/check_consistency.py passes (0 errors) ─> COMPLETED
       │
       ▼
[Phase 3: Springer Journal Template Alignment] (COMPLETED)
  ├── sn-jnl.cls v3.1 Dec 2024 configured ──────────> COMPLETED
  ├── Author-year natbib styling (sn-mathphys-ay) ──> COMPLETED
  ├── Springer Declarations block added ────────────> COMPLETED
  └── tectonic compiles main.pdf without errors ────> COMPLETED
       │
       ▼
[Phase 4: Confirmatory Verification & Overleaf Export] (COMPLETED)
  ├── 78/78 pytest unit tests passing ──────────────> COMPLETED
  ├── Clean springer_overleaf.zip generated ────────> COMPLETED
  └── Independent adversarial audit report ─────────> IN PROGRESS
       │
       ▼
[Phase 5: Mentor Review & External Pre-submission Tasks] (PENDING)
  ├── Share Overleaf project with Prof. Kalyan Kumar Das
  ├── Incorporate mentor line-by-line feedback
  └── Prepare ArXiv preprint submission package
```

---

## 2. Risk Mitigation & Task Ownership

| Task ID | Description | Primary Owner | Target Date | Risk Mitigation |
|---|---|---|---|---|
| **REM-01** | Share Overleaf zip with Prof. Kalyan Kumar Das | Akash Kundu | Oct 14, 2026 | Send via email / link sharing with edit permissions. |
| **REM-02** | Incorporate mentor feedback into manuscript | Akash Kundu & Trinankur Guha | Nov 15, 2026 | Maintain single source of truth; re-run `check_consistency.py`. |
| **REM-03** | Finalize multi-seed error bars in Table 3 | Rupankar Ghatak | Nov 30, 2026 | Automated script aggregates 10 random seeds per dataset. |
| **REM-04** | Prepare cover letter for Springer DAMI | Akash Kundu & Kalyan Kumar Das | Dec 15, 2026 | State explicit research gap, scope alignment, and reproducibility links. |
| **REM-05** | ArXiv preprint posting | Author team | Dec 20, 2026 | Post pre-submission draft to establish priority. |
