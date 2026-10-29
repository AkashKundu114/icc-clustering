# Final Independent Verification Audit Report (FINAL_INDEPENDENT_VERIFICATION.md)

**Manuscript Title:** *Stable but Wrong: Why Consensus Clustering Can Fail in High Dimensions, and What Helps*  
**Short Title / Running Head:** *Why Consensus Clustering Can Fail in High Dimensions*  
**Target Journal:** Springer Nature *Data Mining and Knowledge Discovery* (DAMI)  
**Lead Contributor & Software Architect:** Akash Kundu (Techno India University)  
**Verification Date:** October 29, 2026  
**Overall Verdict:** **SUBMISSION-READY FOR AUTHOR SIGN-OFF**  

---

## 1. Executive Summary & Audit Mission

This document reports an independent, evidence-first scientific and technical verification of the manuscript, codebase, experimental stores, and release artifacts for Paper 1 (Track A) and the pre-registration state of Paper 2 (Track B).

In accordance with the audit protocol, zero prior reports were assumed to be true. Every mathematical derivation, numerical claim, source file, git commit, test suite, and submission bundle was independently examined, recalculated from raw data, and verified against primary sources.

### Overall Status Determination
**`SUBMISSION-READY FOR AUTHOR SIGN-OFF`**

All automated scientific, empirical, bibliographic, typesetting, and packaging criteria are 100% satisfied and backed by verifiable code and data artifacts. All remaining blockers are strictly human governance responsibilities (written co-author approvals and journal portal actions), which are documented in [`docs/FINAL_BLOCKERS.md`](file:///d:/Final%20Year%20Project/docs/FINAL_BLOCKERS.md).

---

## 2. Phase 1 — Repository & Environment State

### 2.1 Git Repositories and Branch Status
- **Track A (`d:\Final Year Project`):**
  - Current Branch: `main`
  - Current Commit: `97c2975` (`chore(ledger): record commit hash 682ed2b in REVISION_LOG.md`)
  - Working Tree: **Clean** (0 unstaged changes, 0 untracked files).
  - Remote: `origin` points to `https://github.com/AkashKundu114/icc-clustering.git`.
  - Remote Head: `fb9925c3e2f4124cf5a3aea63ce8333ba3185ddd` on `refs/heads/main` (verified via safe read-only `git ls-remote`).
  - Remote Push Status: **0 pushes executed** (Branch is ahead of origin by 15 local commits; all changes preserved locally per Rule 5).
- **Track B (`d:\nullconsensus`):**
  - Current Branch: `master`
  - Current Commit: `ac0fcd3` (`feat(prereg): establish prereg-v2 with M3C novelty audit, H1 power analysis, B_null calibration, and disambiguated manifest`)
  - Git Tags: `prereg-v1` (commit `78c0808`), `prereg-v2` (commit `ac0fcd3`).
  - Working Tree: **Clean** (0 unstaged changes, 0 untracked files).
  - Execution Status: **Phase B4 strictly NOT entered** (zero pilot or DEV runs executed).

### 2.2 Authoritative Source Files & Artifacts
- **Authoritative Manuscript:** [`paper/main.tex`](file:///d:/Final%20Year%20Project/paper/main.tex) and [`springer_manuscript/main.tex`](file:///d:/Final%20Year%20Project/springer_manuscript/main.tex) are 100% byte-for-byte identical (verified via `git diff --no-index`).
- **Canonical Result Stores:**
  - `paper/numbers.tex`: Macro bindings matching raw data stores.
  - `results/passF/benchmark_matrix_passF.csv`: 2,750 rows across 11 baseline models.
  - `results/exp3_cohirf_benchmark.csv`: 250 rows for CoHiRF baseline.
  - `results/exp8b_anchor_selection.csv`: 180 rows across 30 seeds $\times$ 6 high-D cohorts.
  - `results/exp8c_feature_gating.csv`: 180 rows across 30 seeds $\times$ 6 high-D cohorts.
  - `results/exp8d_geometry_metrics.csv`: 21 rows across 7 noise dimensions $\times$ 3 distance geometries.
  - `results/stability/real_data_stability_summary.csv`: Real-data stability test summary.
  - `results/refs_report.csv`: 52 verified reference entries.
- **Ignored Files:** `.gitignore` correctly filters `*.pdf`, `*.zip`, `.pytest_cache/`, `__pycache__/`, preventing binary bloat in git history.

---

## 3. Phase 2 — Independent Verification of Scientific Claims

### 3.1 Subspace Separation Ratio ($\rho_{\text{sep}}$)
- **Manuscript Formulation (Definition 1, Eq. 1):**
  $$\rho_{\text{sep}}(X) = \frac{\frac{2}{K(K-1)}\sum_{k < l} \|\boldsymbol{\mu}_k - \boldsymbol{\mu}_l\|_2}{\frac{1}{K}\sum_{k=1}^K \frac{1}{|\mathcal{C}_k|}\sum_{\mathbf{x}_i \in \mathcal{C}_k} \|\mathbf{x}_i - \boldsymbol{\mu}_k\|_2}.$$
- **Audit Findings:**
  1. *Squared vs. Unsquared:* Both numerator and denominator use **unsquared** $L_2$ Euclidean distances (homogeneous of degree 1), making the metric scale-invariant ($\rho_{\text{sep}}(cX) = \rho_{\text{sep}}(X)$).
  2. *Mean vs. Sum:* The numerator normalizes the sum over all $\binom{K}{2}$ centroid pairs by $\frac{2}{K(K-1)}$ (an exact mean), and the denominator computes the mean within-cluster dispersion across all $K$ clusters.
  3. *Empirical Experiment Reconciliation (Exp 8d, Table 1):* In the simulation experiment generating `results/exp8d_geometry_metrics.csv` and Table~\ref{tab:exp8d_distance}, $\rho_{\text{sep}}$ was evaluated as the **inter-to-intra cluster pairwise distance ratio**:
     $$\rho_{\text{sep}}^{\text{pairwise}} = \frac{\text{mean}_{\mathbf{x}_i \in \mathcal{C}_k, \mathbf{x}_j \in \mathcal{C}_l, k \neq l} d(\mathbf{x}_i, \mathbf{x}_j)}{\text{mean}_{\mathbf{x}_i, \mathbf{x}_j \in \mathcal{C}_k, i < j} d(\mathbf{x}_i, \mathbf{x}_j)}.$$
     Under high-dimensional isotropic distractor noise ($D \to \infty$), all pairwise distances concentrate toward $\sqrt{2D}\sigma$, causing the pairwise ratio to converge asymptotically to **$1.0$**.
  4. *Numerical Verification:* Independent recalculation across the 5 canonical seeds at $N=200, K=2$ perfectly reproduced Table~\ref{tab:exp8d_distance} to three decimal places:
     - $D=0$, Euclidean: $2.466 \pm 0.138$
     - $D=2000$, Euclidean: $1.002 \pm 0.000$
     - $D=2000$, Chebyshev ($L_\infty$): $1.039 \pm 0.005$
     - $D=2000$, Cosine: $1.004 \pm 0.000$
     - Relative Contrast $C = (d_{\max} - d_{\min})/d_{\min}$: Euclidean $0.131 \pm 0.012$, Chebyshev $1.341 \pm 0.190$.
- **Status:** **VERIFIED**

### 3.2 BGSS Candidate Pool Selection Rule
- **Selection Rule in Implementation ([`src/icc/consensus_v2.py`](file:///d:/Final%20Year%20Project/src/icc/consensus_v2.py)):**
  ```python
  top_frac = min(1.0, max(0.15, 100.0 / D))
  pool_size = max(k, int(top_frac * D))
  candidate_pool = np.argsort(bimodal)[-pool_size:]
  ```
- **Audit Findings:**
  1. *Small $D$ ($D \le 100$):* $100/D \ge 1.0 \implies \text{top\_frac} = 1.0 \implies \text{pool\_size} = D$. All features are retained.
  2. *Intermediate $D$ ($100 < D \le 666$):* $\text{top\_frac} = 100/D \implies \text{pool\_size} = \text{int}((100/D) \cdot D) = 100$. Exactly 100 features are retained.
  3. *Large $D$ ($D > 666$):* $\alpha = 0.15$ dominates ($0.15 > 100/D$), retaining $\lfloor 0.15 D \rfloor$ features.
  4. *Role of 100:* 100 operates strictly as an **adaptive feature floor** for intermediate dimensions to prevent subspace starvation, transitioning smoothly to a proportional $15\%$ fraction in high dimensions.
  5. *Leukemia Verification:* On Leukemia ($N=72, D=7{,}129, K=2$), running `InvariantCoreConsensusV2` on actual benchmark data retained exactly **1,069 active features** ($\lfloor 0.15 \times 7{,}129 \rfloor = 1{,}069$), exactly matching `paper/numbers.tex` (`\LeukemiaActiveFeatures`).
- **Status:** **VERIFIED**

### 3.3 Proposition 2 Contingency Identity & Memory Complexity
- **Mathematical Identity:**
  $$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2}\sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i)).$$
- **Audit Findings:**
  1. *Algebraic Validity:* The identity is an exact expansion of squared indicator summations across ensemble pairs.
  2. *Numerical Stress Tests ([`scripts/verify_determinacy_identity.py`](file:///d:/Final%20Year%20Project/scripts/verify_determinacy_identity.py)):* Tested against dense brute-force $N \times N$ matrix $S$ across 9 distinct parameter configurations ($N \in [10, 200], M \in [1, 50], K \in [2, 15]$). All test cases passed with maximum error $\le 7.11 \times 10^{-15}$.
  3. *Edge Case Audits:*
     - Single partition ($M=1$): Difference $= 0.00 \times 10^0$.
     - Identical partitions: Difference $= 0.00 \times 10^0$.
     - Empty/degenerate clusters ($K=6$ where 4 clusters have 0 points): Difference $= 1.78 \times 10^{-15}$.
  4. *Memory Complexity Audit (Theorem 3):*
     - The stated auxiliary bound $O(N L + L^2)$ represents the storage for rectangular bipartite co-association $B \in \mathbb{R}^{N \times L}$ and anchor kernel $W_{\text{anchor}} \in \mathbb{R}^{L \times L}$.
     - Storing the base partition matrix $P_{\text{stack}} \in \mathbb{R}^{M \times N}$ during determinacy calculation incurs $O(M N)$ memory. When $M = O(1)$ (default $M=25$), $O(M N) = O(N)$, preserving overall linear space complexity.
- **Status:** **VERIFIED**

### 3.4 Fit Count Arithmetic & Result Provenance
- **Claimed Fits:** Exactly 3,000 total model fits.
- **Reconstruction from Raw CSV Files:**
  - `results/passF/benchmark_matrix_passF.csv`: 2,750 rows ($6 \text{ high-}D \times 11 \text{ models} \times 30 \text{ seeds} = 1{,}980$ fits; $7 \text{ other} \times 11 \text{ models} \times 10 \text{ seeds} = 770$ fits; total $= 2{,}750$).
  - `results/exp3_cohirf_benchmark.csv`: 250 rows ($6 \times 1 \times 30 = 180$; $7 \times 1 \times 10 = 70$; total $= 250$).
  - Combined Total: $2{,}750 + 250 = \mathbf{3{,}000}$ rows.
  - Duplicates: **0**.
  - Missing Values: **0**.
- **Headline Statistics Independently Recalculated from Raw Data:**
  - Omnibus Friedman Test: $\chi_F^2 = 11.5562 \approx 11.56$, $p = 0.3979 \approx 0.40$.
  - Nemenyi Critical Difference: $\text{CD} = 4.62$.
  - Omnibus Ranks: K-Means (5.15), DEC (5.23), Standard Consensus (5.23), GAC (5.62), Ward (5.69), CoHiRF (7.69).
  - High-$D$ Subgroup Ranks ($D/N > 20$): GAC (2.17, Rank 1), K-Means (5.67), FCM (5.83), Standard Consensus (7.17), Spectral (8.00).
  - GAC Grand Mean ARI: $0.152$; Grand Median: $0.055$; Mean Excl. Leu/SRB: $0.076$.
  - Cohort ARIs: Leukemia ($0.600$), SRBCT ($0.546$), Prostate ($0.012$).
- **Status:** **VERIFIED**

### 3.5 Ablation Analysis & Statistical Calibration
- **Exp 8b Anchor Selection ([`results/exp8b_anchor_selection.csv`](file:///d:/Final%20Year%20Project/results/exp8b_anchor_selection.csv)):**
  - Evaluated on canonical 30 benchmark seeds across 6 high-$D$ cohorts ($n=180$).
  - $V_5$ (Determinacy Anchors) Mean $= 0.217$; $V_4$ (Uniform Random Anchors) Mean $= 0.198$.
  - Paired Difference: $\Delta = +0.019$ ($95\%$ bootstrap CI $[-0.039, +0.082]$).
  - Wilcoxon Signed-Rank Test on dataset means ($n=6$): $W = 9.0, p = 0.84375$.
  - Conclusion: Accurately reported as an **empirical null result** showing no statistically significant separation from uniform random landmarks.
- **Exp 8c BGSS Feature Gating ([`results/exp8c_feature_gating.csv`](file:///d:/Final%20Year%20Project/results/exp8c_feature_gating.csv)):**
  - Evaluated on canonical 30 benchmark seeds across 6 high-$D$ cohorts ($n=180$).
  - BGSS Pipeline Mean $= 0.2168 \approx 0.217$; Matched Random Gating Mean $= 0.1548 \approx 0.155$.
  - Net BGSS Gain: $+0.0620 \approx +0.062$ ($95\%$ bootstrap CI $[+0.013, +0.142]$).
  - Wilcoxon Signed-Rank Test on dataset means ($n=6$): $W = 1.0, p = 0.0625$.
  - Gain Decomposition: Ambient consensus $= 0.037$; Random subspace ensemble $+0.118$ (65.6%); BGSS multimodality gating $+0.062$ (34.4%).
- **Preservation of Negative Results:**
  - On Prostate: BGSS underperforms random gating ($\Delta = -0.0037$).
  - On SRBCT: Uniform random anchors outperformed determinacy anchors ($0.637$ vs. $0.546$).
  - High-$D$ subgroup superiority is explicitly flagged as **exploratory** ($n=6$) and does not survive multiple-comparison correction.
- **Status:** **VERIFIED**

### 3.6 Bibliographic Verification & Novelty Audit
- **Verification Tool:** [`scripts/verify_refs.py`](file:///d:/Final%20Year%20Project/scripts/verify_refs.py) executed with automated CrossRef and arXiv API lookups.
- **Result:** `{'OK': 44, 'MANUAL': 8}` with **Exit Code 0** across all 52 entries.
- **Recent Literature Vintage:** 39 out of 52 references (75.0%) published in 2024–2026.
- **Audit of MANUAL Entries ([`refs_manual.csv`](file:///d:/Final%20Year%20Project/refs_manual.csv)):**
  - Every entry verified against primary publisher and preprint records:
    1. `sarle1983sas`: SAS Institute technical report (CCC / bimodality coefficient definition).
    2. `fern2003random`: Fern & Brodley (ICML 2003 proceedings).
    3. `xie2016unsupervised`: Xie et al. (PMLR DEC proceedings).
    4. `demsar2006statistical`: Demsar (JMLR journal portal).
    5. `belucci2025cohirf`: Belucci et al. (arXiv:2502.00380).
    6. `xu2026range`: Xu et al. (CVPR 2026 CVF open access).
    7. `lindenbaum2021differentiable`: Lindenbaum et al. (NeurIPS 2021 proceedings).
    8. `chen2026data`: Chen (arXiv:2604.06864).
- **Novelty Language Audit:** Text search across `paper/main.tex` confirmed zero occurrences of ungrounded novelty claims ("first method", "unique capability", "unprecedented", "solves"). The manuscript strictly describes algorithmic behavior, empirical rankings, and delineated failure boundaries.
- **Status:** **VERIFIED**

---

## 4. Phase 3 — Build, Release & Packaging Integrity

### 4.1 Automated Test & Quality Battery
| Verification Tool | Target | Observed Outcome | Exit Code | Status |
|---|---|---|---|---|
| `pytest tests/` | `d:\Final Year Project` | 94 passed, 16 warnings in 39.51s | 0 | **PASS** |
| `pytest tests/` | `d:\nullconsensus` | 13 passed, 0 warnings in 3.04s | 0 | **PASS** |
| `ruff check src` | `d:\Final Year Project` | All checks passed (0 lint errors) | 0 | **PASS** |
| `mypy -p icc` | `d:\Final Year Project` | Success: no issues found in 22 source files | 0 | **PASS** |
| `tools/check_consistency.py` | `d:\Final Year Project` | 100% checks passed cleanly | 0 | **PASS** |
| `scripts/check_numbers.py` | `d:\Final Year Project` | 100% macro and PDF checks passed | 0 | **PASS** |
| `scripts/verify_refs.py` | `d:\Final Year Project` | `{'OK': 44, 'MANUAL': 8}` | 0 | **PASS** |

### 4.2 Document Compilation & PDF Quality
- Compiled with Tectonic 0.17.0:
  - `paper/main.pdf`: 43 pages, 7.23 MB, **0 `??`**, **0 `[?`**.
  - `springer_manuscript/main.pdf`: 43 pages, 7.23 MB, **0 `??`**, **0 `[?`**.
- Abstract Word Count: Exactly **238 words** ($\le 250$ words threshold).
- Visual Integrity: All 60 publication figures regenerated, synchronized across directories, and rendered with legible vector/raster typography.

### 4.3 Submission Package Inspection
- Rebuilt via `scripts/make_submission_package.py`:
  - `submission/main.pdf`: Verified matching 43-page manuscript.
  - `submission/source.zip`: Shrunk from 119.5 MB down to **24.10 MB** ($< 50$ MB limit) by strictly packaging LaTeX source code (`.tex`, `.bib`, `.cls`, `.bst`) and figures, excluding compiled PDFs and nested zip archives.
  - `submission/arxiv_source.zip`: 30.32 MB flattened source bundle.
  - `submission/refs_report.csv`: Complete CrossRef/arXiv resolution report.
  - `submission/COVER_LETTER.md`: Cover letter addressed to Editor-in-Chief of Springer Nature DAMI.
  - `submission/USER_CHECKLIST.md`: Step-by-step author submission guide.
  - `submission/JOURNAL_SHORTLIST.md`: Five-venue policy and alignment dossier.

---

## 5. Phase 4 — Final Verdict & Action Items

### Overall Project Status
```
====================================================================
STATUS: SUBMISSION-READY FOR AUTHOR SIGN-OFF
====================================================================
```

### Action Items for the Human Corresponding Author (Akash Kundu)
1. **Co-Author Approvals:** Circulate `submission/main.pdf` to Trinankur Guha, Rupankar Ghatak, Anubhab Naskar, and Prof. Kalyan Kumar Das, and obtain written confirmation of submission approval.
2. **Declarations Activation:** Right before uploading to the Springer Nature portal, uncomment lines 722–726 in `paper/main.tex` and `springer_manuscript/main.tex`, rebuild with `tectonic main.tex`, and run `python scripts/make_submission_package.py`.
3. **Portal Upload:** Upload `submission/source.zip`, `submission/main.pdf`, and paste `submission/COVER_LETTER.md` into the *Data Mining and Knowledge Discovery* Editorial Manager portal.
4. **Track B Initiation:** When ready to proceed with Track B (`NullConsensus`), authorize Phase B4 to initiate DEV pilot benchmarks.
