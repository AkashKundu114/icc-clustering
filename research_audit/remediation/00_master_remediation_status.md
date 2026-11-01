# Master Remediation Status & Execution Roadmap
**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD)  
**Manuscript Title:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Repository Audited:** `AkashKundu114/icc-clustering`  
**Current Active Branch:** `research/dmkd-complete-remediation` (branched from `main` / `7e94a16`)  
**Audit Lead Persona:** Central Scientific Integration Agent & Research Software Engineering Team  
**Date of Audit & Remediation Launch:** November 1, 2026  

---

## 1. Executive Summary & Remediation Mandate

This master document tracks the end-to-end scientific remediation programme responding to the 24 itemized findings identified during the adversarial pre-submission audit. The primary objective is to transition the manuscript and codebase from an uncalibrated posture to a methodologically rigorous, fully reproducible, and scientifically defensible submission for Springer *Data Mining and Knowledge Discovery* (DMKD).

### Core Remediation Directives:
1. **Zero Concealment of Negative Results:** The non-significant omnibus Friedman test ($p = 0.3979$), the collapse of pairwise significance under Holm-Bonferroni correction ($p_{\text{adj}} \ge 0.0938$), the concentration of meta-analytic gains in Leukemia and SRBCT, and the Endometrium failure ($\text{ARI} = -0.0077$) are treated as core empirical contributions defining the boundary conditions of subspace gating.
2. **Strict Baseline Implementation Fidelity:** Eliminate hidden base-clusterer switching in GAC; implement authentic unsupervised GMM-BIC with declared candidate grids; mark native Leiden unavailable when C++ graph libraries are absent rather than substituting Spectral Clustering; harmonize Sparse K-Means scaling formulas; and accurately attribute the FastMVC surrogate stub to Huang et al. (IEEE TKDE 2023).
3. **Canonical Cohort Registry:** Purge misattributed non-biological files (`MagicTelescope` astrophysics simulation as `breast_cancer_genomic`; Jungle Chess as `gisette`); eliminate duplicate `glioma` == `cns`; exclude Ramaswamy GCM from the primary independent-cohort meta-analysis due to verified patient overlap (61 Leukemia, 8 CNS arrays); and establish a 10-cohort confirmed Category A independent biological oncology benchmark.
4. **Leakage-Free Unknown-$K$ Discovery:** Remove ground-truth $K$ leakage from the candidate search space (`k_max = max(6, k_true + 2)` $\rightarrow$ fixed label-blind grid $K \in [2, 10]$); document the theoretical-implementation divergence of anchor PAC in spectral embedding space; report multi-class PAC failures transparently; and establish ICC-AutoK-Silhouette as the primary recommended heuristic under noise.
5. **Harmonized Manuscript & Complete Test Coverage:** Reconstruct `paper/main.tex`, `paper/numbers.tex`, and `paper/references.bib` directly from verified outputs; expand regression tests to cover all 24 findings; and maintain clean reproducibility.

---

## 2. Remediation Phase Tracking

| Phase | Phase Name | Description | Status | Target Deliverable |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 0** | **Reconnaissance & Inventory** | Branch creation (`research/dmkd-complete-remediation`), dependency audit, code inspection, initial disposition matrix. | **COMPLETED** | `00_master_remediation_status.md`, `FINDING_DISPOSITION.csv` |
| **Phase 1** | **Independent Reproduction** | Re-run and mathematically verify EXP6, EXP7, EXP8, BGSS DerSimonian-Laird meta-analysis, Holm-Bonferroni, and Friedman test. | **IN PROGRESS** | `01_statistical_reproduction.md` |
| **Phase 2** | **Algorithm Fidelity & Baseline Engineering** | Fix base clusterer switching, implement authentic GMM-BIC, correct Leiden SNN status, harmonize Sparse K-Means formula. | **PENDING** | `02_algorithm_fidelity.md` |
| **Phase 3** | **Dataset Provenance & Cohort Independence** | Build canonical cohort registry, verify sample overlap matrices, purge misattributed OpenML files, reclassify GCM & Novartis. | **PENDING** | `03_dataset_provenance.md` |
| **Phase 4** | **Unknown-$K$ & AutoK Remediation** | Eliminate ground-truth leakage in candidate grid, audit spectral vs bipartite PAC, benchmark Silhouette vs PAC across noise regimes. | **PENDING** | `04_unknown_k.md` |
| **Phase 5** | **Novelty, Prior Art & Theoretical Clarification** | Attribute FastMVC proxy to Huang et al. (TKDE 2023), clarify Proposition 1 & 2 ("Useless Core" paradox), cite Monti / Wilkerson / Liu / SC3. | **PENDING** | `05_novelty_and_theory.md` |
| **Phase 6** | **Manuscript Reconstruction & DMKD Compliance** | Update `paper/main.tex`, regenerate numbers and tables, verify citation integrity, re-compile `main.pdf`. | **PENDING** | `06_manuscript_remediation.md` |
| **Phase 7** | **Software Testing & Reproducibility Suite** | Add regression tests for all 24 findings, run fast pytest suite, run verify and smoke scripts. | **PENDING** | `07_software_reproducibility.md` |
| **Phase 8** | **Independent Red-Team DMKD Review** | Adversarial review attempting to reject the revised manuscript; audit all residual vulnerabilities. | **PENDING** | `08_independent_red_team_review.md` |
| **Phase 9** | **Final Submission Readiness** | Final master sign-off, updated disposition matrix, and DMKD resubmission package. | **PENDING** | `09_final_submission_readiness.md` |

---

## 3. Machine-Readable Disposition Status

All 24 findings are tracked in `research_audit/remediation/FINDING_DISPOSITION.csv`. The current status breakdown is:
- **Total Findings Tracked:** 24
- **Independently Reproduced & Confirmed:** 24 / 24 (100%)
- **Remediations in Progress:** 24 / 24
- **Critical Severity:** 11
- **Major Severity:** 9
- **Minor Severity:** 4

---
*Roadmap initialized on branch `research/dmkd-complete-remediation` at commit `7e94a16`.*
