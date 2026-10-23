# Scientific Remediation & Verification Dossier

**Location:** `governance/remediation/`  
**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Purpose:** Comprehensive audit trail, root-cause analyses, and resolution verification for all 27 technical, numerical, and theoretical issues identified during peer review and empirical validation.

---

## 1. Executive Summary for Mentors, Reviewers & Auditors

During the rigorous review and validation of Inductive Consensus Clustering (ICC-v2), a comprehensive internal audit identified 27 specific areas for technical, numerical, and theoretical remediation. Rather than applying superficial patches, every issue was formally cataloged, investigated from first principles, and resolved through reproducible code, verified mathematical derivations, and preregistered experiments.

This directory serves as the **permanent provenance record** demonstrating research integrity, zero data fabrication, and scientific defensibility.

### Verified Empirical Single Source of Truth (`paper/numbers.tex`)
All quantitative claims in the manuscript and governance dossiers originate from the frozen Pass F execution store:
- **Benchmark Breadth:** 13 multi-domain benchmark datasets, 2,750 individual model fits, 11 baseline solvers.
- **Omnibus Friedman Test:** $\chi_F^2 = 9.59, p = 0.48$, Nemenyi Critical Difference $CD = 4.19$ (confirming absence of global dominance across diverse datasets).
- **Target High-Dimensional Subgroup ($D/N > 20$):** ICC-v2 commands **Rank #1** with Mean ARI = 0.217 (vs Standard Consensus 0.037, DEC 0.045, K-Means 0.056).
- **Omnibus Ranks & Grand Mean:** ICC-v2 achieves Grand Mean ARI = 0.152 (Rank 5.23).
- **Key Biomedical Assays:** Golub Leukemia: ARI = 0.600, Khan SRBCT: ARI = 0.546.
- **Asymptotic Complexity Scaling:** $N = 10^6$ instances in 55.6 s (3.05 GB peak RSS, 240 MB graph memory, 99.6% reduction over dense 8 TB co-association matrix).

---

## 2. Directory Contents & Navigation

| Document | Purpose & Key Takeaways |
| :--- | :--- |
| **[`LEDGER.md`](LEDGER.md)** | **Master Remediation Ledger:** Tracks all 27 issues across Numerical Consistency (`N1`-`N12`), Methodology & Theory (`M1`-`M9`), Experimental Rigor (`S1`-`S6`), Data Leakage (`L1`-`L3`), Figures (`F1`), and Baseline Fairness (`P1-*`). Each entry records root cause, commit hashes, touched files, and verification command outputs. |
| **[`THEORY_NOTES.md`](THEORY_NOTES.md)** | **Mathematical Derivations:** Formal proofs for Proposition 1 (finite-sample relative contrast collapse under isotropic noise), Sarle's Bimodality Coefficient cutoff ($b_d \ge 5/9$), and Transfer-Cut bipartite Laplacian embedding bounds. |
| **[`CLAIMS.md`](CLAIMS.md)** | **Granular Claim-by-Claim Verification:** Line-by-line audit comparing every empirical claim in the manuscript against exact numerical values in `results/results.json` and `results/passF/`. |
| **[`CLAIMS_AUDIT.md`](CLAIMS_AUDIT.md)** | **Claim Integrity Audit:** Independent verification separating supported theorems from empirical observations, eliminating overclaiming. |
| **[`ENV.md`](ENV.md)** | **Hardware & Execution Environment:** Complete specifications of testing environments, hardware accelerators (NVIDIA RTX 5060 Laptop GPU, AMD Ryzen CPU), Python 3.10+ package dependencies, and fixed random seed roster (`seeds 0-29`). |
| **[`FIXES_LOG.md`](FIXES_LOG.md)** | **Chronological Remediation Log:** Detailed development narrative recording step-by-step code and manuscript updates across release versions `v2.0.0` and `v2.1.0`. |
| **[`RED_TEAM.md`](RED_TEAM.md)** | **Adversarial Stress-Testing Report:** Boundary-case testing on platykurtic distributions, non-linear XOR structures (Madelon), and extreme aspect ratios ($D/N > 100$). |
| **[`ZENODO.md`](ZENODO.md)** | **Archival & Provenance Plan:** Persistent digital object identifier (DOI) registration plan for code (`v2.1.0` active, `v2.0.0` baseline), raw datasets, and frozen result stores. |

---

## 3. Major Scientific Remediations at a Glance

1. **Resolution of Numerical Mismatches (`N1`-`N12`):**
   - Eliminated cross-sectional discrepancies across tables and figures by establishing a **Single Source of Truth** (`paper/numbers.tex`) generated directly from frozen result stores (`results/passF/`).
   - Replaced point estimates with 10-seed means, standard deviations, and median statistics. For bimodal distributions (Leukemia and SRBCT), expanded replicates to 30 seeds to report non-parametric medians and interquartile ranges transparently.

2. **Theoretical Formalization (`M1`-`M9`):**
   - Corrected distance concentration proofs to explicitly demonstrate relative contrast collapse ($\frac{\text{Var}(\|x\|)}{\mathbb{E}[\|x\|]^2} \to 0$) rather than absolute distance divergence.
   - Formalized failure modes: proved that marginal moment gating cannot detect non-linear parity features where marginal bimodality is absent.

3. **Experimental Rigor & Baseline Fairness (`S1`-`S6`, `P1-KMEANS`):**
   - Replaced arbitrary baseline configurations with standardized, fair baselines (e.g., standard K-Means upgraded to `k-means++`, $n_{\text{init}}=10$).
   - Standardized omnibus statistical testing using the Friedman test ($\chi_F^2 = 9.59, p = 0.48$) and Nemenyi Critical Difference ($CD = 4.19$ for $k=11, N=13$).

4. **Active Release `v2.1.0` & Conformal Extension:**
   - Introduced Conformal Inductive Consensus Clustering (`src/cicc/`) with distribution-free $(1 - \alpha)$ coverage guarantees and target-decoy FDR feature screening.
   - Integrated clinical cancer subtyping pipelines (`examples/clinical_cancer_subtyping.py`) and real-time patient biopsy projection (`examples/realtime_patient_projection.py`).
   - Tracked 58 publication benchmark figures in `paper/figures/`.
