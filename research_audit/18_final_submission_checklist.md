# Research Audit 18: Springer DMKD Submission Readiness Checklist

**Target Journal:** Springer Nature *Data Mining and Knowledge Discovery* (DMKD / DAMI)  
**Article Type:** Regular Paper (Original Research)  
**Submission URL:** `https://link.springer.com/journal/10618/submission-guidelines`  
**Date:** 2026-10-31  

---

## 1. Compliance Audit Matrix

| Guideline Item | Springer DMKD Requirement | Current Status in Manuscript | Compliance Verdict |
| :--- | :--- | :--- | :--- |
| **Article Type** | Original Research Regular Paper | Configured in `sn-jnl.cls` (`sn-standardnature` or `default`) | **PASS** |
| **Title Format** | Concise, descriptive, informative; no acronyms in title | *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts* | **PASS** |
| **Abstract Length** | 150 to 250 words structured or unstructured | Exactly **232 words** in `springer_manuscript/main.tex` | **PASS** |
| **Keywords** | 4 to 6 keywords separated by commas | 5 keywords: `Consensus clustering`, `Stability-accuracy discordance`, `High-dimensional noise`, `Feature gating`, `Bipartite graphs` | **PASS** |
| **Citation Format** | Springer Nature name-year in-text format (`\citep`, `\citet`) | Verified against `references.bib` with alphabetized reference list | **PASS** |
| **DOI Requirement** | Required for all modern citations | Automated CrossRef API audit verified in `results/refs_report.csv` | **PASS** |
| **Mathematical Style** | Standard LaTeX math; equations numbered sequentially | Equations (1)–(15) sequentially numbered without gaps | **PASS** |
| **Figure Quality** | High-resolution 300 DPI vector PDF or PNG; self-explanatory captions | Vector graphics in `paper/figures/` and `springer_manuscript/figures/` | **PASS** |
| **Table Formatting** | LaTeX booktabs (`\toprule`, `\midrule`, `\bottomrule`); no vertical lines | Formatted in `gen/table*.tex` adhering to booktabs standards | **PASS** |
| **Data Availability** | Mandatory Data Availability Statement | Present in Section *Declarations* with exact OpenML/GEO accessions | **PASS** |
| **Code Availability** | Mandatory Code Availability Statement with URL/commit | Present in Section *Declarations* linking to GitHub repository | **PASS** |
| **Competing Interests** | Mandatory Conflict of Interest Disclosure | Explicitly stated: *The authors declare no competing interests.* | **PASS** |
| **Author Contributions** | Mandatory CRedit statement | Formal CRediT authorship breakdown included | **PASS** |

---

## 2. Springer DMKD Editor Cover Letter

```text
To:
Prof. Johannes Fürnkranz and the Editorial Board
Data Mining and Knowledge Discovery (DMKD)
Springer Nature

Subject: Submission of Original Research Article - "An Empirical Analysis of Stability-Accuracy
Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts"

Dear Editors,

We are pleased to submit our original research manuscript entitled "An Empirical Analysis of
Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical
Cohorts" for consideration as a Regular Paper in Data Mining and Knowledge Discovery.

A cornerstone assumption across unsupervised learning, data mining, and computational biology is
that cluster stability under subsampling indicates partition reliability. Consensus clustering is
widely deployed in high-dimensional genomic studies under the belief that ensembling protects
against high-dimensional noise. In this paper, we conduct a controlled empirical and theoretical
falsification of this premise.

Using an expanded suite of 12 independent high-dimensional oncology cohorts (D/N > 20) alongside
single-cell transcriptomic and multi-domain controls (over 3,000 model fits across 12 algorithmic
pipelines), we systematically characterize "stability-accuracy discordance": the phenomenon where
clustering algorithms repeatedly converge onto the same partition under row resampling (subsample
stability >= 0.50) while external agreement with verified diagnostic reference labels remains at
or below chance (ARI <= 0.05). Across non-degenerate discordant cells, the stability-accuracy gap
averages +0.485 (95% cohort-clustered bootstrap CI [+0.379, +0.662]), while column-permuted null
controls confirm stability ~ 0.01.

Through geometric diagnostics on clinical prostate and central nervous system cohorts, we show
that discordant partitions latch onto dominant sample-level nuisance axes (sequencing depth,
leading principal components, and geometric outliers) rather than target pathology. Furthermore,
we present a controlled factorial decomposition of algorithmic mechanisms designed to recover
signal, demonstrating that bipartite anchor graph compression and random feature subsampling
fail on their own, and that univariate bimodality gating (BGSS) provides substantial gains if
and only if informative marker coordinates exhibit detectable marginal multimodality. Finally,
we extend our investigation to genuinely unsupervised cluster-number discovery (unknown K),
identifying the failure modes of standard model selection heuristics under distractor noise.

In accordance with DMKD's commitment to reproducible research, all raw per-seed experimental
outputs, configuration manifests, dataset loading pipelines, and LaTeX source files are tracked
and publicly accessible.

This manuscript is original, has not been published previously, and is not under consideration
for publication elsewhere. All authors have approved the manuscript and agree with its submission.

Thank you for your time and consideration of our work.

Sincerely,

Akash Kundu
Department of Computer Science & Engineering
Techno India University, Kolkata, India
Email: akashkundu1152@gmail.com
```
