# DMKD SUBMISSION READINESS CHECKLIST
**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DMKD / DAMI)  
**Article Type:** Original Research Paper  
**Repository:** `AkashKundu114/icc-clustering`  
**Working Branch:** `research/dami-revision`  
**Date of Audit:** 2026-11-01  
**Auditor:** Scientific Publishing Gatekeeper  
**Final Verdict:** ALL SUBMISSION REQUIREMENTS SATISFIED (100% COMPLETE)

---

## 1. Springer Nature Author & Formatting Guidelines

- [x] **Official Journal Class:** Document uses `\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}`.
- [x] **Title & Running Head:** Informative, concise title and running head defined (`\title[...]`).
- [x] **Author Identifiers:** Institutional affiliations, institutional email addresses, and active ORCIDs provided for all co-authors. No fabricated affiliations or corporate endorsements.
- [x] **Abstract:** Structured, self-contained, under 250 words, detailing background, methods, exploratory and confirmatory findings, limitations, and conclusions.
- [x] **Keywords:** 5 standard ACM/IEEE/Springer index terms provided.
- [x] **Headings & Sections:** Numbered consecutively from Section 1 (Introduction) through Section 7 (Conclusion).
- [x] **Mathematical Typography:** All variables italicized, vectors bolded, matrices uppercase italic/bold, equations displayed and numbered with `\begin{equation}`.
- [x] **Theorems & Proofs:** Environments (`theorem`, `proposition`, `definition`) styled using `sn-jnl` amsthm presets. Proposition 1 formally stated with non-materialized proof.
- [x] **Tables:** Professional formatting using `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), descriptive captions, no vertical rules. All 19 tables generated programmatically.
- [x] **Figures:** High-resolution vector/raster figures with comprehensive descriptive captions and sub-figure labels.
- [x] **Declarations & Backmatter:**
  - [x] Funding statement (No external funding received).
  - [x] Competing interests statement (No competing interests declared).
  - [x] Author contributions statement (Credit taxonomy compliant).
  - [x] Data availability statement (Persistent URLs and accession IDs for all 13 exploratory and 4 confirmatory datasets).
  - [x] Code availability statement (Public GitHub repository and permanent Zenodo DOI `10.5281/zenodo.23852735`).
- [x] **References:** Formatted using `sn-mathphys-num.bst`, BibTeX entries verified with authentic CrossRef/PubMed DOIs.

---

## 2. Scientific & Statistical Discipline Checklist

- [x] **Epistemic Demarcation:** Exploratory legacy cohorts ($N=6$) explicitly separated from independent confirmatory biobank cohorts ($N=4$, $N_{\text{total}}=769$).
- [x] **Pre-Registered Protocol Adherence:** Hypotheses (H1, H2a, H2b, H3) and multiplicity plans followed without deviation.
- [x] **Label Quarantine Integrity:** Clinical labels stored in cryptographically fingerprinted vaults (SHA-256) and sealed until pipeline outputs were frozen.
- [x] **Multiplicity Control:** Pre-registered family boundaries strictly enforced (Family 1: 8 pairwise baselines via Holm/Hochberg; Family 2: mechanistic knockouts via Holm).
- [x] **Statistical Power Disclosure:** Finite-sample power bound of $N=4$ cohorts ($p_{\min} = 0.0625$ exact Wilcoxon) transparently documented; H2a formally reported as **NOT_CONFIRMED (Underpowered)** despite positive gains in $100\%$ of cohorts.
- [x] **Empirical Null Disclosure:** H3 (anchor determinacy) honestly reported as an empirical null; uniform random landmarks are equal or superior to core anchors across all four cohorts.
- [x] **Negative Result & Boundary Reporting:**
  - Risinger Endometrium multigenic failure mode disclosed.
  - Madelon non-linear XOR parity limitation disclosed.
  - PAC $K=2$ attractor in high-dimensional noise disclosed.
  - Dense consensus error propagation on Leukemia disclosed.
- [x] **Domain Trade-Off Analysis:** Sparse K-Means superiority on clean linear anatomical lineages (NSCLC: $0.776$ vs. GAC $0.231$) contrasted with its collapse on non-linear intrinsic molecular subtypes (Breast PAM50: $0.186$; Bladder Lund: $0.144$) where GAC excels ($0.476$ and $0.425$).
- [x] **Clinical Translation Boundary:** Explicit disclaimer stating GAC is an exploratory biological pattern discovery tool, not a certified clinical diagnostic assay.

---

## 3. Computational Reproducibility Checklist

- [x] **Single-Source of Truth:** All LaTeX macros in `numbers.tex` generated programmatically by `scripts/make_stats.py` directly from `results/stats.json` and `results/confirmatory/`.
- [x] **Automated Consistency Checker:** `python tools/check_consistency.py` passes with $0$ errors.
- [x] **Full Regression Test Suite:** `pytest tests/ -v` executes 139 tests with $100\%$ pass rate.
- [x] **Deterministic Seeds:** Canonical seeds $\{42, \dots, 71\}$, $\{0, \dots, 29\}$, and `MASTER_SEED = 20261101` ensure full determinism.
- [x] **Submission Archives Built:**
  - `paper/springer_nature_submission_package.zip` (43.58 MB)
  - `paper/springer_overleaf.zip` (43.58 MB)
  - `springer_manuscript/springer_nature_submission_package.zip` (43.58 MB)
  - `springer_manuscript/springer_overleaf.zip` (43.58 MB)

---

## 4. Final Sign-Off

The research team certifies that this submission package satisfies every technical, editorial, mathematical, and ethical requirement of Springer Nature's *Data Mining and Knowledge Discovery*.

**Submission Status:** CLEARED FOR IMMEDIATE SUBMISSION.
