# Instructions for Zenodo Integration and DOI Assignment

**Repository:** `AkashKundu114/icc-clustering`  
**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Tag:** `v2.1.0`  
**Prior Historical Release Baseline:** `v2.0.0` (Archived: 2026-10-17)

---

## 1. Connecting Zenodo to GitHub

1. Log in to [Zenodo](https://zenodo.org/) using your GitHub account.
2. Navigate to **GitHub settings** in Zenodo: `https://zenodo.org/account/settings/github/`.
3. Locate `AkashKundu114/icc-clustering` in the repository list and switch the toggle to **ON**.
4. Zenodo configures a webhook on the repository for automated snapshot capture on release tagging.

---

## 2. Publishing Active Release `v2.1.0`

When publishing the canonical release tag on GitHub:
```bash
git tag -a v2.1.0 -m "Release v2.1.0: Conformal Inductive Consensus Clustering, Clinical Cancer Subtyping & Figures"
git push origin v2.1.0
```

Zenodo automatically triggers an archival snapshot, mints a permanent Digital Object Identifier (DOI), and provides citation metadata.

*(Note: Prior historical baseline release `v2.0.0` was tagged on 2026-10-17 as the foundational remediation release).*

---

## 3. Active Release Scope (`v2.1.0`)

The active release `v2.1.0` permanently registers:
1. **Core Package (`src/icc/`):** Bipartite anchor consensus, BGSS/VSSG feature gating, Transfer-Cut projection, and ASPP reliability profiling.
2. **Conformal Package (`src/cicc/`):** Finite-sample distribution-free $(1 - \alpha)$ coverage guarantees, target-decoy False Discovery Rate feature screening, and point-of-care clinical safety triage.
3. **Clinical Diagnostic Examples (`examples/`):** Real-world oncology pipelines evaluating Golub Leukemia and Khan SRBCT (`clinical_cancer_subtyping.py`, `realtime_patient_projection.py`).
4. **Publication Figure Tracking (`paper/figures/`):** 58 verified publication benchmark figures.
5. **Verified Experimental Results (`paper/numbers.tex`):**
   - 13 benchmark datasets, 2,750 individual model fits, 11 baseline solvers.
   - Omnibus Friedman test: $\chi_F^2 = 9.59, p = 0.48$, Nemenyi $CD = 4.19$ (no global dominance).
   - High-D subgroup ($D/N > 20$): ICC-v2 Rank #1 with Mean ARI = 0.217 (vs Standard Consensus 0.037, DEC 0.045, K-Means 0.056).
   - Grand Mean ARI: 0.152 (Rank 5.23).
   - Golub Leukemia: ARI = 0.600, Khan SRBCT: ARI = 0.546.
   - Asymptotic scaling: $N = 10^6$ in 55.6 s (3.05 GB peak RSS, 240 MB graph memory, 99.6% reduction over dense 8 TB).

---

## 4. Data & Code Availability Statement for Manuscript

Update the manuscript's Availability section with the minted DOI:

```latex
\section*{Data and Code Availability}
The source code, benchmark configuration files, reproduction scripts, and publication figures supporting the findings of this study are openly available on GitHub at \url{https://github.com/AkashKundu114/icc-clustering} (Active Release tag: \texttt{v2.1.0}, Historical baseline: \texttt{v2.0.0}) and permanently archived on Zenodo under DOI: \url{https://doi.org/10.5281/zenodo.XXXXXXX}.
```
