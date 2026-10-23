# PHASE 1 REMEDIATION REPORT: REPRODUCE AND FREEZE

**Repository**: `github.com/AkashKundu114/icc-clustering`  
**Canonical Manuscript Title**: "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue**: Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version**: `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Branch**: `remediation/phase1`  
**Git Tag**: `results-frozen`  
**Date**: October 2026  

---

## 1. Executive Summary

Phase 0 (Reconnaissance) and Phase 1 (Reproduce and Freeze) have concluded with complete execution and raw log capture across the test suite and all experiments (Exp 0 through Exp 5). No algorithm code on `remediation/phase1` was modified or tuned; bug fixes were logged strictly as non-applied patch diffs in `REMEDIATION/patches/`.

All 3,430 empirical run observations have been aggregated into an immutable, single source-of-truth file at `results/results.json`, accompanied by full SHA256 provenance in `results/MANIFEST.md`.

---

## 2. Verification Scoreboard

All 201 quantitative claims identified across the manuscript were systematically evaluated against the frozen empirical outputs:

| Claim Category | Total Evaluated | Bit-for-Bit / Tolerance MATCH | Empirical MISMATCH | Match Rate |
|---|---|---|---|---|
| **Table 3 Benchmark Matrix (13 Datasets × 11 Models)** | 143 | 143 | 0 | **100.0%** |
| **Table 3 Aggregates & Ranks** | 19 | 17 | 2 | 89.5% |
| **Biomedical Discrepancies (Leukemia, SRBCT, Ovarian)** | 12 | 8 | 4 | 66.7% |
| **Synthetic Ablation (Exp 2 & 2.1)** | 9 | 7 | 2 | 77.8% |
| **Inductive Generalization (Exp 1)** | 6 | 1 | 5 | 16.7% |
| **Scalability & Anchor Fidelity (Exp 4 & 4.3)** | 6 | 6 | 0 | **100.0%** |
| **Extreme Scale & Missing Data (Exp 5 & 3.5)** | 6 | 6 | 0 | **100.0%** |
| **TOTAL** | **201** | **188** | **13** | **93.5%** |

---

## 3. Confirmed Stop Conditions & Critical Discrepancies

### Stop Condition 1: Dataset Duplication (CNS == Glioma)
- **Finding**: `cns.npz` and `glioma.npz` located in `experiments/exp3_real_world_benchmarks/data/cache/` are **100% byte-for-byte identical** (`SHA256: 0e449bf55f8e5682de8de4264c986c1b85b27f25ca0092b5a8a98ca2bb2a87ff`).
- **Impact**: In legacy Figure 6/14 audit heatmaps, duplicate rows were reported under different names. Table 3 in the manuscript included CNS and correctly omitted Glioma, avoiding double-counting in the primary matrix.

### Stop Condition 2: Leukemia Re-run Divergence & Seed Instability
- **Finding**: 
  - Section 5.2 claimed Leukemia ICC-v2 ARI = `0.846 ± 0.154`.
  - Table 3 claimed Leukemia ICC-v2 ARI = `0.6801 ± 0.2311`.
  - Legacy Fig 6 reported `0.323` (15% anchors).
  - Fresh Exp 2 Ablation yielded `0.6208 ± 0.3342`.
- **Root Cause**: Deep inspection of seed-level runs in Exp 3.1 revealed that 2 out of 10 seeds collapsed (`-0.0290` and `0.0192`), while 8 seeds achieved `~0.85`. The 0.846 claim in Sec 5.2 reflects an informal exclusion of failed seeds. Furthermore, in fresh ablation sweeps, V4 (uniform random anchors) outperformed V5 (determinacy-certified anchors) on both Leukemia (`0.628` vs `0.621`) and SRBCT (`0.650` vs `0.614`).

### Stop Condition 3: VSSG Failure on Non-Linear Interactions (Madelon XOR)
- **Finding**: On the Madelon benchmark ($D=500, D_{\text{informative}}=20$), VSSG PR-AUC is `0.156` (claimed `0.892`), and Recall@50 is `0.400` (claimed `0.95`).
- **Root Cause**: Bimodality Coefficient ($b_d = \frac{\gamma^2 + 1}{\kappa}$) assesses marginal 1D distributions. Madelon is governed by pairwise XOR interactions where marginal projections are strictly unimodal Gaussians. Maximum observed $b_d$ across all 500 features was `0.5042`, well below the Sarle uniform threshold ($5/9 \approx 0.5556$). VSSG fails theoretically on XOR structures.

### Stop Condition 4: Exp 1 Inductive Pseudo-Labeling Baseline at High Noise
- **Finding**: At $D_{\text{noise}} \ge 1,000$, pseudo-label test accuracy hovers between `31.2%` and `37.8%` (near 3-class random chance `33.3%`).
- **Root Cause**: Distilling noisy cluster pseudo-labels through standard inductive classifiers without feature selection cannot overcome the curse of dimensionality. Core-set training does not rescue this failure mode at $D=5,000$ (Core accuracy is $0.290$ vs All $0.340$).

### Stop Condition 5: Statistical Claims & Critical Difference Calibration
- **Finding**: Section 5.4 reported Nemenyi Critical Difference $\text{CD} = 2.62$.
- **Correction**: $\text{CD} = 2.62$ corresponds to $k=9$ models across $N=21$ datasets. For the actual Table 3 benchmark ($k=11$ models, $N=13$ datasets), the true two-tailed $\alpha=0.05$ Critical Difference is $\mathbf{4.21}$.
- **Omnibus Test**: Friedman test $p = 0.33$ confirms no statistically significant difference across the omnibus 13 datasets. Statistical superiority only holds on the pre-specified high-dimensional subgroup ($D/N > 20$).

---

## 4. Remediation Phase 1 Deliverables

| Deliverable | Path | Status |
|---|---|---|
| Environment Specification & Freeze | `REMEDIATION/ENV.md` | Verified & Locked |
| Issue Ledger (N1-N12, M1-M9, S1-S6, L1-L3, F1, P1-) | `REMEDIATION/LEDGER.md` | Initialized & Linked |
| Master Quantitative Claims Register (201 claims) | `REMEDIATION/CLAIMS.md` | Evaluated (188 Match, 13 Mismatch) |
| Architecture & Data-Leakage Audit | `REMEDIATION/AUDIT_PHASE0.md` | Verified Clean (No Leakage) |
| Spot-Check Audit | `REMEDIATION/AUDIT_SPOTCHECK.md` | Verified (Table 3 Bit-for-Bit Verified) |
| Immutable Results Database | `results/results.json` | 3,430 runs frozen |
| Integrity Manifest | `results/MANIFEST.md` | 73 SHA256 hashes |
| Bug Patches (Non-applied diffs) | `REMEDIATION/patches/` | Diff files preserved |

---

## 5. Transition to Phase 2 (Science)

The baseline is frozen. Phase 2 must proceed on branch `remediation/phase2` under strict preregistration (`REMEDIATION/PREREG.md`):
1. **Theory Alignment**: Correct Proposition 1 bound to $1.854$, align Transfer-Cut bipartite formulation, and document the 1D marginal unimodality limitation of VSSG.
2. **Fair Baselines**: Evaluate variance filtering, PCA preprocessing, Laplacian score, and sparse $k$-means on high-dimensional benchmarks into `results/phase2/`.
3. **Manuscript Softening**: Adjust claims in the manuscript to reflect true empirical values (e.g. Leukemia ARI 0.680, Nemenyi CD 4.21, Madelon XOR limitation).
