# Scientific Integrity and Technical Audit Log

**Project:** Inductive Consensus Clustering (ICC-v2)  
**Repository:** `AkashKundu114/icc-clustering`  
**Manuscript:** *When Does Feature Gating and Anchor Consensus Salvage High-Dimensional Clustering? An Empirical and Geometric Analysis*  
**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DAMI)  
**Lead Researcher:** Akash Kundu  
**Audit Protocol:** Autonomous Multi-Disciplinary Scientific Review (Goal Execution)  
**Status:** ALL FINDINGS RESOLVED / MITIGATED  

---

## 1. Audit Summary Matrix

| ID | Category | Severity | Description | Target Component | Resolution Status | Verified By |
|---|---|---|---|---|---|---|
| **AUD-01** | Mathematical | HIGH | Subspace Separation Ratio Definition 1 normalization check | `paper/main.tex`, Sec 2 | RESOLVED | Mathematical derivation |
| **AUD-02** | Mathematical | HIGH | Proposition 1 Sarle's coefficient threshold & mixture condition | `paper/main.tex`, Sec 3.1 | RESOLVED | First-principles proof |
| **AUD-03** | Mathematical | MEDIUM | BGSS candidate pool floor semantics vs text description | `src/icc/consensus_v2.py`, `paper/main.tex` | RESOLVED | Code & text synchronized |
| **AUD-04** | Mathematical | CRITICAL | Proposition 2 Contingency Identity algebraic derivation & numerical stability | `src/icc/consensus_v2.py`, Sec 3.2 | RESOLVED | `scripts/verify_determinacy_identity.py` (max error $< 10^{-14}$) |
| **AUD-05** | Terminology | HIGH | Overclaiming in "certified core" terminology (implies ground-truth correctness) | `paper/main.tex`, `springer_manuscript/main.tex` | RESOLVED | Replaced with "high-determinacy core" |
| **AUD-06** | Experimental | CRITICAL | Discrepancy in total benchmark model fit count (2,750 vs 3,000) | `paper/main.tex` L303, `springer_manuscript/` | RESOLVED | Reconciled arithmetic: $(6 \times 12 \times 30) + (7 \times 12 \times 10) = 3{,}000$ |
| **AUD-07** | Data Provenance | HIGH | Absence of formal machine-readable dataset registry | `data/` | RESOLVED | Created `data/registry.yaml` for all 13 benchmarks |
| **AUD-08** | Methodology | MEDIUM | Lack of automated end-to-end consistency verification tool | `tools/` | RESOLVED | Created `tools/check_consistency.py` |
| **AUD-09** | Statistics | MEDIUM | Characterization of high-D cohort win rate and omnibus significance | `paper/main.tex`, Abstract & Sec 5 | RESOLVED | Framed high-D rank #1 as exploratory ($n=6$, non-sig after Holm) |
| **AUD-10** | Statistics | MEDIUM | True $2 \times 2$ factorial interaction contrast calculation | `paper/main.tex`, Sec 6.2 | RESOLVED | Verified contrast $+0.131$ (Wilcoxon $p \approx 0.094$, 95% CI $[0.010, 0.315]$) |
| **AUD-11** | Bibliographic | HIGH | Strict 2024–2026 citation recency and single-citation policy | `refs.bib`, `results/refs_report.csv` | RESOLVED | `scripts/verify_refs.py` reports 100% OK/MANUAL, $\ge 80\%$ recent |
| **AUD-12** | Governance | HIGH | Strict attribution separation between repo metadata and academic manuscript | Repo metadata, `CITATION.cff`, `LICENSE` | RESOLVED | Sole author Akash Kundu across repo; institutional co-authors on paper |
| **AUD-13** | Architecture | CRITICAL | Decoupling of exploratory new method into independent repository | `d:\nullconsensus` | RESOLVED | Established standalone repo, preregistered Candidate 12 (NullGate) |

---

## 2. Detailed Audit Findings & Resolutions

### AUD-01: Subspace Separation Ratio ($\operatorname{SSR}$) Metric Normalization
- **Severity:** HIGH
- **Context:** Definition 1 defines the Subspace Separation Ratio to quantify high-dimensional geometric degradation under isotropic distractor noise.
- **Finding:** A previous draft used ambiguous notation suggesting all $K^2$ ordered pairs in the numerator centroid distance summation.
- **Audit Verification:** Inspected `paper/main.tex` line 165. The definition strictly uses:
  $$\operatorname{SSR}(\mathcal{X}, \mathbf{y}^*) = \frac{\frac{2}{K(K-1)} \sum_{1 \le k < l \le K} \|\boldsymbol{\mu}_k - \boldsymbol{\mu}_l\|_2}{\frac{1}{K} \sum_{k=1}^K \frac{1}{|C_k|} \sum_{\mathbf{x} \in C_k} \|\mathbf{x} - \boldsymbol{\mu}_k\|_2}$$
  This averages over the $\binom{K}{2} = \frac{K(K-1)}{2}$ unique unordered cluster pairs. The metric is scale-consistent, unsquared in both numerator and denominator, and bounded non-negative.
- **Status:** RESOLVED. Mathematical formulation is formally verified.

---

### AUD-02: Proposition 1 (Sarle's Bimodality Coefficient Threshold & Separation Limit)
- **Severity:** HIGH
- **Context:** Proposition 1 asserts that for symmetric unimodal distributions, $BC \le 5/9 \approx 0.5556$, and derives the minimum component separation for Gaussian mixtures to cross this threshold.
- **Finding:** Needs rigorous algebraic proof from first principles for a balanced two-component homoscedastic Gaussian mixture $\frac{1}{2}\mathcal{N}(-\Delta, \sigma_0^2) + \frac{1}{2}\mathcal{N}(\Delta, \sigma_0^2)$.
- **Audit Derivation:**
  1. Let $\theta = \Delta^2 / \sigma_0^2$. By symmetry, odd central moments vanish: $\mu_1 = 0, \mu_3 = 0 \implies \gamma_1 = 0$.
  2. Second central moment: $\mu_2 = \sigma_0^2 + \Delta^2 = \sigma_0^2(1 + \theta)$.
  3. Fourth central moment: $\mu_4 = 3\sigma_0^4 + 6\sigma_0^2\Delta^2 + \Delta^4 = \sigma_0^4(\theta^2 + 6\theta + 3)$.
  4. Pearson kurtosis: $\beta_2 = \frac{\mu_4}{\mu_2^2} = \frac{\theta^2 + 6\theta + 3}{(\theta + 1)^2}$.
  5. Bimodality coefficient: $BC = \frac{\gamma_1^2 + 1}{\beta_2} = \frac{(\theta + 1)^2}{\theta^2 + 6\theta + 3}$.
  6. Threshold condition $BC > \frac{5}{9}$:
     $$9(\theta^2 + 2\theta + 1) > 5(\theta^2 + 6\theta + 3) \iff 4\theta^2 - 12\theta - 6 > 0 \iff 2\theta^2 - 6\theta - 3 > 0$$
  7. Positive quadratic root:
     $$\theta^* = \frac{6 + \sqrt{36 - 4(2)(-3)}}{4} = \frac{6 + \sqrt{60}}{4} = \frac{3 + \sqrt{15}}{2} \approx \frac{3 + 3.87298}{2} = 3.43649$$
  8. Normalized separation ratio:
     $$\frac{\Delta}{\sigma_0} > \sqrt{\theta^*} = \sqrt{3.43649} \approx 1.85377 \approx 1.854$$
  9. Inter-cluster centroid distance: $2\Delta > 2 \times 1.85377 \sigma_0 \approx 3.708 \sigma_0$.
- **Status:** RESOLVED. Derivation is mathematically exact and documented in `docs/THEORETICAL_FOUNDATIONS.md`.

---

### AUD-03: BGSS Candidate Pool Floor Semantics
- **Severity:** MEDIUM
- **Context:** In `src/icc/consensus_v2.py`, `pool_mode == "legacy"` computes:
  ```python
  top_frac = min(1.0, max(0.15, 100.0 / D))
  pool_size = max(k, int(top_frac * D))
  ```
- **Finding:** Line 210 in `paper/main.tex` previously stated that the selection rule applied a "minimum cap $\min(100, D)$", which creates confusion because 100 is a *minimum floor* ensuring at least 100 features are preserved for diversity when $D \ge 100$.
- **Audit Verification & Remediation:**
  - When $D < 100$: $\text{pool\_size} = D$.
  - When $100 \le D \le 666$: $\text{pool\_size} = \max(K, 100) = 100$.
  - When $D > 666$: $\text{pool\_size} = \max(K, \lfloor 0.15 D \rfloor) = \lfloor 0.15 D \rfloor$.
  - Closed-form expression: $\text{pool\_size} = \min(D, \max(K, \max(100, \lfloor \alpha \cdot D \rfloor)))$ with $\alpha = 0.15$.
  - Updated line 210 of `paper/main.tex` and `springer_manuscript/main.tex` to explicitly use this formula and clarify the minimum floor mechanism.
- **Status:** RESOLVED.

---

### AUD-04: Proposition 2 Contingency Identity Formulation & Numerical Stability
- **Severity:** CRITICAL
- **Context:** Proposition 2 eliminates the $O(N^2)$ memory requirement of dense consensus by computing quadratic sample determinacy directly from contingency tables across base partitions.
- **Finding:** Potential risk of division-by-zero, indexing mismatch, or floating-point drift.
- **Audit Verification:**
  - Implemented standalone exhaustive audit script `scripts/verify_determinacy_identity.py`.
  - Tested across 9 distinct scenarios: Tiny ($N=10, K=2, M=3$), Small ($N=50, K=3, M=5$), Standard ($N=200, K=5, M=15$), Large ($N=1000, K=10, M=25$), Extreme $K=N$ ($N=30, K=30, M=5$), Single partition $M=1$ ($N=100, K=4$), Degenerate identical partitions ($N=100, K=3, M=10$), Imbalanced clusters ($N=300, K=4, M=10$), and Unclustered noise ($N=150, K=5, M=20$).
  - In all 9 tests, the fast identity matched the dense $O(N^2)$ brute force computation within $\le 7.11 \times 10^{-15}$ (pure machine epsilon).
- **Status:** RESOLVED. Proposition 2 is mathematically and computationally robust.

---

### AUD-05: Retiring "Certified Core" Overclaim
- **Severity:** HIGH
- **Context:** Earlier drafts referred to points with sample determinacy $\sigma_i \ge \tau_{\text{core}}$ as the "certified core" ($\mathcal{C}_{\text{core}}$).
- **Finding:** In statistical learning theory and unsupervised clustering, the word "certified" denotes a formal mathematical guarantee against ground-truth labels (e.g., certificate of optimality or certifiable robustness). Sample determinacy $\sigma_i$ measures ensemble stability/consensus agreement, not ground-truth correctness.
- **Remediation:**
  - Replaced all 7 occurrences in `paper/main.tex` and `springer_manuscript/main.tex`:
    - "certified core" $\to$ "high-determinacy core"
    - "anchor certification" $\to$ "determinacy-based anchor selection"
    - "certified anchors" $\to$ "high-determinacy core anchors"
- **Status:** RESOLVED.

---

### AUD-06: Benchmark Model Fit Count Discrepancy (2,750 vs 3,000)
- **Severity:** CRITICAL
- **Context:** The text in `paper/main.tex` line 303 stated $(6 \times 11 \times 30) + (7 \times 11 \times 10) = 2{,}750$ model fits, whereas the abstract and benchmark tables evaluated 12 algorithms (adding CoHiRF), yielding $(6 \times 12 \times 30) + (7 \times 12 \times 10) = 3{,}000$ model fits.
- **Remediation:**
  - Updated line 303 in `paper/main.tex` and `springer_manuscript/main.tex` to:
    `This design yields $(6 \times 12 \times 30) + (7 \times 12 \times 10) = 3{,}000$ total benchmark model fits across the 12 evaluated pipelines.`
  - Verified with `tools/check_consistency.py` that all fit-count arithmetic matches the frozen result matrices in `results/passF/benchmark_matrix_passF.csv`.
- **Status:** RESOLVED.

---

### AUD-07 & AUD-08: Data Registry and Automated Consistency Tooling
- **Severity:** HIGH / MEDIUM
- **Remediation:**
  - Created `data/registry.yaml` defining metadata, samples, dimensions, classes, OpenML IDs, licenses, and preprocessing hashes for all 13 benchmark datasets.
  - Authored `tools/check_consistency.py` validating dataset registry counts, high-dimensional cohort partitions, fit arithmetic, `numbers.tex` macro sync, lexical scans for stale tokens, and result file integrity.
- **Status:** RESOLVED. Automated checker passes cleanly with exit code 0.

---

### AUD-09 & AUD-10: Restrained Statistical Claims and Factorial Contrast
- **Severity:** MEDIUM
- **Context:** Ensuring empirical conclusions are strictly evidence-based without over-generalization.
- **Remediation:**
  - Manuscript explicitly reports the omnibus Friedman test across all 13 benchmarks is non-significant ($\chi_F^2 = 9.59, p = 0.40$), with K-Means (5.15), Standard Consensus (5.23), and DEC (5.23) achieving better mean ranks than ICC-v2 (5.62).
  - ICC-v2's #1 mean rank on the six $D/N > 20$ cohorts is explicitly qualified as an exploratory subgroup finding ($n=6$, non-significant after Holm step-down correction).
  - True $2 \times 2$ factorial interaction contrast $(V_5 - V_2) - (V_3 - V_0) = +0.131$ (95% bootstrap CI $[0.010, 0.315]$, Wilcoxon $W=2.0, p \approx 0.094$) is clearly presented as suggestive and driven primarily by Leukemia ($+0.565$).
- **Status:** RESOLVED.

---

### AUD-11: Bibliographic Verification
- **Severity:** HIGH
- **Context:** Target venue requirements and integrity rules require 100% verified bibliographic entries against CrossRef/arXiv APIs, $\ge 80\%$ recent literature (2024–2026), and single-citation policy.
- **Audit Verification:** `scripts/verify_refs.py` executes against `refs.bib` with zero unresolved MISMATCH or NOT_FOUND entries.
- **Status:** RESOLVED.

---

### AUD-12 & AUD-13: Attribution and Track B Separation
- **Severity:** CRITICAL
- **Context:** Strict separation between repository attribution and formal academic paper, and isolation of new exploratory method (Track B).
- **Remediation:**
  - Repository metadata (`pyproject.toml`, `LICENSE`, `CITATION.cff`, `README.md`) exclusively attributes Akash Kundu. Academic manuscript (`paper/main.tex`, `submission/arxiv_source/main.tex`) preserves institutional capstone co-authors.
  - Track B (`nullconsensus`) initialized in a clean, standalone repository at `d:\nullconsensus` with Candidate 12 (NullGate) and Candidate 2 (HurdleGate), unit tested and frozen under tag `prereg-v1`.
- **Status:** RESOLVED.
