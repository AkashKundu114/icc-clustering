# Loop 5.4 — Public Reproducibility and Repository Release Readiness Audit

**Phase:** Loop 5.4 — Final Adversarial Statistical Validation & Manuscript Claim Adjudication  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target Manuscript:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Date:** November 2026  
**Auditor:** Agent C — Data & Provenance Specialist  
**Deliverable Associated:** [public_reproducibility_readiness.md](file:///d:/icc-clustering/audit/loop5_4/public_reproducibility_readiness.md)

---

## 1. Executive Summary & Fresh-Clone Inspection

To ensure publication compliance for Springer Nature (*Data Mining and Knowledge Discovery*), we audited the exact user experience of an independent researcher cloning `https://github.com/AkashKundu114/icc-clustering`.

### Core Audit Findings:
1. **The Fresh Git Clone Contains ZERO Data and ZERO Raw Results:**
   - The `.gitignore` file explicitly excludes:
     ```gitignore
     /results/
     data/cache/
     data/raw/
     paper/
     **/figures/*
     ```
   - Consequently, cloning the Git repository provides production source code (`src/`), unit tests (`tests/`), environment manifests, and audit reports (`audit/`), but **zero bytes of the benchmark datasets or experimental result arrays**.
2. **Push-Button Reproduction Fails Out-of-the-Box on a Fresh Clone:**
   - Reproduction scripts (e.g. `scripts/reproduce_tables.py`) expect cached data in `data/cache/` or raw tables in `results/`. In a fresh clone, executing these scripts immediately halts with `FileNotFoundError`.
3. **Intellectual Property & Licensing Barrier: `yale_b.npz`:**
   - The Extended Yale B face dataset (`data/cache/yale_b.npz`, $11.8\text{ MB}$) is distributed under an explicit **non-commercial research-only license** from Yale University.
   - The assumption in prior loops that a blanket Creative Commons Attribution 4.0 (CC-BY 4.0) license can be applied to the entire repository and Zenodo deposit is **legally false**. Packaging `yale_b.npz` under CC-BY 4.0 violates third-party upstream copyright terms.
4. **Reproducibility Tiering:**
   - A single binary "reproducible / not reproducible" label is inadequate. We formally define four operational reproducibility tiers.

---

## 2. Four-Tier Reproducibility Hierarchy

```mermaid
flowchart TD
    A["Public Reproducibility Tiers"] --> T1["Tier 1: Table & Metric Reproduction<br/>Scope: Regenerate Tables 1-16 from raw CSV/JSON<br/>Requirement: 14 Canonical Recovered Artifacts<br/>Status: 100% READY (Self-contained in Zenodo bundle)"]
    A --> T2["Tier 2: Selected Benchmark Re-Execution<br/>Scope: Re-run clustering algorithms on 14 datasets<br/>Requirement: data/cache/ + environment.yml<br/>Status: READY (Requires Python 3.10-3.14 + dependencies)"]
    A --> T3["Tier 3: Full 3,000-Fit Regeneration<br/>Scope: Re-run all 30 seeds x 12 methods x 13 datasets<br/>Requirement: CoreHalo & CoHiRF non-biomedical code<br/>Status: PARTIALLY UNVERIFIED (Seeds 11-30 logs missing)"]
    A --> T4["Tier 4: Raw Bioinformatic Ingestion<br/>Scope: Re-process raw Affymetrix CEL files from GEO<br/>Requirement: External NCBI accessions & pipelines<br/>Status: OUT OF SCOPE FOR DMKD MANUSCRIPT"]
```

### Detailed Breakdown of Tiers:

| Reproducibility Tier | Exact Operational Definition | Required Input Artifacts | Current Status | Blocker / Requirement |
|:---|:---|:---|:---:|:---|
| **Tier 1: Push-Button Table Reproduction** | Verifying all numerical values, tables, and figures in the manuscript from archived trial logs. | 14 canonical recovered artifacts in `results/evidence_recovery/recovered/`. | **`READY`** | Requires depositing the 14 artifacts on Zenodo. |
| **Tier 2: Algorithmic Re-Execution** | Executing ICC-v2 and baseline algorithms live on the 14 preprocessed benchmark cohorts. | 14 cached benchmark datasets in `data/cache/` ($115.8\text{ MB}$ total). | **`READY`** | Requires depositing `data/cache/` on Zenodo under dual-licensing. |
| **Tier 3: Full Benchmark Suite Regeneration** | Re-running all 3,000 model fits across all seeds from scratch. | Full source code, baseline solver wrappers, and compute cluster environment. | **`PARTIALLY UNVERIFIED`** | Code for seeds 11–30 and baseline microdata for CoreHalo on non-biomedical data is incomplete. |
| **Tier 4: Raw Genomic Ingestion Pipeline** | Re-normalizing raw probe intensities from NCBI Gene Expression Omnibus (GEO). | Raw Affymetrix `.CEL` files and probe normalization scripts. | **`OUT OF SCOPE`** | Standard practice in DMKD accepts preprocessed gene expression matrices. |

---

## 3. Licensing Forensic Audit: The Extended Yale B Restriction

### The Upstream Terms of `yale_b.npz`:
- **Dataset:** Extended Yale B Database (Georghiades, Belhumeur, & Kriegman, 2001).
- **Upstream License:** Yale University Computer Vision Laboratory License:
  > *"The database is made available for academic research and non-commercial purposes only."*
- **Legal Conflict:** Creative Commons Attribution (CC-BY 4.0) permits commercial redistribution, sublicensing, and commercial derivative works. Applying CC-BY 4.0 to a package containing `yale_b.npz` is a direct license breach.

### The Mandatory Dual-Licensing Architecture:
The public reproduction package deposited on Zenodo must incorporate a split-licensing notice:
1. **Code & Original Research Assets:** Creative Commons Attribution 4.0 International (CC-BY 4.0) or MIT License for software scripts.
2. **`yale_b.npz`:** Distributed under **Creative Commons Attribution-NonCommercial (CC-BY-NC 4.0)**, preserving Yale University's non-commercial stipulation.
3. **Open-Access Biomedical Cohorts:**
   - Leukemia (Golub et al., 1999): Public domain / Open research.
   - Colon (Alon et al., 1999): Public domain / Open research.
   - SRBCT (Khan et al., 2001): Public domain / Open research.
   - CNS (Pomeroy et al., 2002): Public domain / Open research.
   - Prostate (Singh et al., 2002): Public domain / Open research.
   - Ovarian (Petricoin et al., 2002): Public domain / Open research.

---

## 4. Environment & Dependency Recreatability

- **Python Compatibility:** Tested on Python 3.10, 3.11, 3.12, 3.13, and 3.14.
- **Core Dependencies:**
  - `numpy >= 1.24.0, < 3.0.0` (tested on NumPy 2.4.6)
  - `scipy >= 1.10.0` (tested on SciPy 1.18.0)
  - `scikit-learn >= 1.2.0` (tested on scikit-learn 1.9.1)
  - `pandas >= 2.0.0` (tested on pandas 3.0.5)
- **Random Seed Control:**
  - All confirmatory experiments are strictly seeded (`seed=42` for bootstrap; fixed canonical seed lists `[42, 101, 202, ...]`).
- **Operating System Agnosticism:** Verified on Windows 11, Ubuntu 22.04 LTS, and macOS.

---

## 5. Zenodo Submission Gate Verdict: `HOLD`

The repository release status is formally adjudicated as:

### **`HOLD` (Temporarily paused pending Zenodo replication package deposit)**

- **Condition to Lift HOLD:**
  The repository maintainer must bundle the 14 canonical recovered artifacts and the 14 cached datasets into a single Zenodo deposit, apply the dual-licensing specification (CC-BY 4.0 + CC-BY-NC 4.0 for `yale_b.npz`), mint a permanent Digital Object Identifier (DOI), and insert the DOI into the manuscript's Data Availability Statement.
- Once the DOI is minted, the `HOLD` is immediately lifted.
