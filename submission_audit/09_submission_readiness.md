# 09 — Springer Submission Readiness Checklist

**Journal:** *Data Mining and Knowledge Discovery* (DAMI), Springer Nature  
**Article Type:** Regular Research Paper  
**Author Guidelines Verification Date:** October 13, 2026  
**Guidelines URL:** `https://link.springer.com/journal/10618/submission-guidelines`  

---

## Compliance Checklist

| Item | DAMI Requirement | Implementation in `springer_manuscript/` | Status |
|---|---|---|---|
| **LaTeX Template** | Springer Nature template recommended (`sn-jnl.cls`) | Dec 2024 v3.1 `sn-jnl.cls` utilized. | **PASSED** |
| **Citation System** | Harvard / Author-Year citation format | Configured `\documentclass[pdflatex,sn-mathphys-ay]{sn-jnl}` with `sn-mathphys-ay.bst`. | **PASSED** |
| **Reference List** | Alphabetized by first author surname with DOIs | Natbib alphabetization verified; full DOI URLs added. | **PASSED** |
| **Abstract Length** | 150 to 250 words | Exactly 154 words. | **PASSED** |
| **Keywords** | 4 to 6 relevant keywords | 7 domain-specific keywords provided. | **PASSED** |
| **Section Numbering** | Decimal numbering, max 3 levels | Standard decimal headings used throughout. | **PASSED** |
| **Author Block** | Full names, affiliations, email, ORCID | Akash Kundu (lead & corresponding, ORCID: 0009-0003-8246-7316); mentor Kalyan Kumar Das included. | **PASSED** |
| **Institutional Address** | Department, Institution, Postal Address | Techno India University, EM-4, Sector V, Bidhannagar, Kolkata, 700091, India. | **PASSED** |
| **Declarations Section** | Required sections before references: | Formally included: | **PASSED** |
| - *Funding* | Disclose funding or state none received | *"The authors did not receive support from any organization for the submitted work."* | **PASSED** |
| - *Competing Interests* | Financial/non-financial interests disclosed | *"The authors have no competing interests to declare."* | **PASSED** |
| - *Ethics Approval* | State applicability | *"Not applicable. This study does not involve human participants or animal subjects."* | **PASSED** |
| - *Data Availability* | Public access repository link | Public link provided: `https://github.com/AkashKundu114/icc-clustering`. | **PASSED** |
| - *Author Contributions* | Formal CRediT statement | Full CRediT breakdown provided for all 5 authors. | **PASSED** |
| **Figure & Artwork** | Legible, high resolution, vector EPS/PNG | High-res PNG figures in `figures/` directory. | **PASSED** |
| **Reproducibility** | Complete source files & generated PDF | `springer_overleaf.zip` (21.65 MB) and `main.pdf` generated. | **PASSED** |
| **Residual Venue Language** | No IEEE/TKDE template remnants | Scanned: 0 occurrences of IEEE/TKDE submission tags. | **PASSED** |
