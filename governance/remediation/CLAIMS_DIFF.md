# CLAIMS DIFFERENTIAL LEDGER (CLAIMS_DIFF.md)

**Title**: Systematic Differential Between Original Published Claims and Remediated Scientific Truth  
**Repository**: `github.com/AkashKundu114/icc-clustering`  
**Canonical Manuscript Title**: "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue**: Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version**: `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Date**: October 2026  

---

## 1. Executive Summary of Changes
This document details every scientific claim modified, softened, or contextualized in the manuscript during the remediation process. In accordance with Global Rule 1 ("Integrity first. Never edit a number so that two places agree. A claim that the evidence does not support must be rewritten or dropped"), all modified claims are tied directly to reproducible execution evidence and LaTeX macros in `numbers.tex`.

---

## 2. Itemized Claims Differential

### Claim 1: Proposition 1 Separation Bound
- **Original Claim**: Component separation bound for multimodality detection was stated as $\Delta / \sigma > \sqrt{2} \approx 1.414$.
- **Remediated Claim**: Bounded by the exact algebraic positive root:
  $$2\theta^2 - 6\theta - 3 = 0 \implies \frac{\Delta}{\sigma} > \sqrt{\frac{3 + \sqrt{15}}{2}} \approx \mathbf{1.854}$$
- **Rationale**: Setting Sarle's Bimodality Coefficient $b(X) > 5/9$ for a symmetric Gaussian mixture requires Pearson kurtosis $\beta_2 < 1.8$. Solving $5(3 + 6\theta + \theta^2) < 9(1 + 2\theta + \theta^2)$ yields $\theta > 3.436 \implies \sqrt{\theta} > 1.854$.
- **Verification**: Verified numerically across Student-$t$ noise regimes ($\nu \in [5, 100]$) in `scripts/verify_prop1.py` and `REMEDIATION/THEORY_NOTES.md`.
- **Macro**: `\PropOneCriticalBound`

### Claim 2: Leukemia Genomic Cluster Recovery
- **Original Claim**: Section 5.2 claimed ICC-v2 achieves $\text{ARI} = 0.846 \pm 0.154$ (and up to $1.000$ on representative seeds).
- **Remediated Claim**: Grounded on the frozen Pass F 30-seed ground truth matching `paper/numbers.tex`:
  $$\text{ARI} = \mathbf{0.600 \pm 0.367}$$
  (Non-parametric median: $0.787$, IQR: $[0.000, 0.892]$, bimodal success rate: $76.7\%$ where $\text{ARI} > 0.50$).
- **Rationale**: Investigation in `REMEDIATION/AUDIT_SPOTCHECK.md` revealed that earlier $0.846$ figures arose from cherry-picking non-zero runs. The Pass F protocol expanded replicates to 30 independent seeds, transparently reporting both parametric mean and non-parametric median to account for bimodal cluster separation.
- **Macros**: `\LeukemiaTableThreeARI`, `\LeukemiaTableThreeStd`, `\ARIleukemia`

### Claim 3: SRBCT Multiclass Cluster Recovery
- **Original Claim**: Section 5.2 claimed ICC-v2 achieves $\text{ARI} = 0.681 \pm 0.037$ on SRBCT.
- **Remediated Claim**: Grounded on the frozen Pass F 30-seed ground truth matching `paper/numbers.tex`:
  $$\text{ARI} = \mathbf{0.546 \pm 0.102}$$
  (Non-parametric median: $0.562$).
- **Rationale**: Replaces optimistic point estimates with the frozen 30-seed benchmark ground truth.
- **Macros**: `\SrbctTableThreeARI`, `\SrbctTableThreeStd`, `\ARIsrbct`

### Claim 4: VSSG Non-Linear Feature Saliency on Madelon
- **Original Claim**: Section 5.3 claimed VSSG achieves $\text{PR-AUC} = 0.892$ and $\text{Recall@50} = 0.95$ on Madelon ($D=500, D_{\text{signal}}=20$).
- **Remediated Claim**: Formally declared as an architectural negative scope boundary:
  $$\text{Recall@50} = \mathbf{0.400}, \quad \text{Precision@50} = \mathbf{0.156}$$
  Maximum observed Bimodality Coefficient across all 500 features is $\mathbf{0.5042} < 5/9$.
- **Rationale**: Madelon cluster geometry is determined by pairwise XOR interactions. Projecting XOR features onto 1D marginals yields unimodal Gaussian distributions. Because VSSG is a marginal 1D filter, it cannot theoretically isolate non-linear interactions without marginal shifts.
- **Macros**: `\VssgMadelonMaxBC`, `\VssgMadelonRecallFifty`, `\VssgMadelonPrecisionFifty`

### Claim 5: Nemenyi Critical Difference Calibration
- **Original Claim**: Section 5.4 reported Nemenyi Critical Difference threshold $\text{CD} = 2.62$.
- **Remediated Claim**: Corrected to the exact formula value for $k=11$ models across $N=13$ datasets matching `paper/numbers.tex`:
  $$\mathbf{\text{CD} = 4.19}$$
  Omnibus Friedman test: $\chi_F^2 = 9.59, p = 0.48$.
- **Rationale**: $\text{CD} = 2.62$ belonged to an earlier audit script evaluating $k=9$ models across $N=21$ datasets. For Table 3 ($k=11, N=13$), $q_{0.05} \sqrt{\frac{11 \times 12}{6 \times 13}} = 3.219 \times 1.3009 = 4.1876 \approx 4.19$. The text claim of "decisive omnibus separation" is updated to note that Friedman omnibus testing ($\chi_F^2 = 9.59, p = 0.48$) indicates no statistically significant dominance across heterogeneous benchmark domains simultaneously.
- **Macro**: `\TrueNemenyiCD`, `\TableThreeFriedmanPValue`

### Claim 6: Biomedical Subgroup Ranking ($D/N > 20$)
- **Original Claim**: Section 5.4 text claimed ICC-v2 achieves an average rank of $1.50$ on the $D/N > 20$ subgroup.
- **Remediated Claim**: Corrected to the exact Pass F subgroup ranking matching `paper/numbers.tex`:
  $$\mathbf{R = 2.00, \quad \text{Mean ARI} = 0.217}$$
  (Ranking #1 on high-D subgroup, vs Standard Consensus 0.037, DEC 0.045, K-Means 0.056).
- **Rationale**: In Pass F multi-seed evaluations across the 6 high-dimensional datasets ($D/N > 20$: Colon, Leukemia, SRBCT, CNS, Ovarian, Prostate), ICC-v2 achieves Mean ARI = 0.217 and commands Rank #1. The omnibus Grand Mean ARI across all 13 datasets is 0.152 (Rank 5.23).
- **Macro**: `\RankBioICCvTwo`, `\TableThreeIccVTwoHighDRank`, `\FairBaselinesIccVTwoHighDMean`, `\GrandMeanARI`

### Claim 7: Fair Baseline Comparison on High-D Regimes
- **Original Claim**: Only un-gated ambient baselines (K-Means, Ward, Spectral, FCM) were benchmarked against ICC-v2.
- **Remediated Addition**: Evaluated Variance Filter, PCA/SVD, Laplacian Score, and Sparse K-Means across 30 seeds on high-D datasets matching `paper/numbers.tex`:
  - On the $D/N > 20$ high-D cancer datasets, ICC-v2 achieves Mean ARI of $\mathbf{0.217}$, outperforming PCA + K-Means ($0.054$), Sparse K-Means ($0.051$), Variance Filter + K-Means ($0.046$), Laplacian Score + K-Means ($0.041$), PCA + Standard Consensus ($0.038$), and Variance Filter + Standard Consensus ($0.032$).
- **Rationale**: Demonstrates that bipartite anchor ensembling and Transfer-Cut spectral consensus provide a substantial performance margin over simple upstream dimension reduction and filtering.
- **Macros**: `\FairBaselinesIccVTwoHighDMean`, `\FairBaselinesKmPcaHighDMean`, `\FairBaselinesSparseKmHighDMean`, `\FairBaselinesKmVarFiltHighDMean`, `\FairBaselinesKmLapScoreHighDMean`

### Claim 8: Direct Inductive Out-of-Sample Prediction
- **Original Claim**: Inductive extension was evaluated primarily as downstream classifier training on pseudo-labels.
- **Remediated Addition**: Evaluated direct Nystrom out-of-sample centroid projection in the active subspace on held-out 20% test splits:
  - On Leukemia, direct Nystrom projection achieves test $\text{ARI} = \mathbf{0.714}$ vs. $0.172$ for K-Means and $0.203$ for PCA + K-Means.
  - On SRBCT, direct Nystrom projection achieves test $\text{ARI} = \mathbf{0.455}$ vs. $0.083$ for K-Means.
- **Rationale**: Directly validates the out-of-sample projection mechanism of ICC-v2 on independent test splits.
- **Macros**: `\InductiveLeukemiaNystromARI`, `\InductiveSrbctNystromARI`
### Claim 9: Asymptotic Memory & Runtime Complexity Scaling
- **Original Claim**: Quadratic consensus matrix storage and slow runtime scaling.
- **Remediated Claim**: Linear-time bipartite anchor graph formulation achieves asymptotic scaling:
  - Scaled smoothly to $N = 10^6$ instances in $55.6\text{ s}$ ($3.05\text{ GB}$ peak RSS, $240\text{ MB}$ consensus graph memory, representing a $99.6\%$ reduction over dense $8\text{ TB}$ co-association matrix).
  - At $N = 10{,}000$, graph memory reduction is $99.6\%$, dynamic memory reduction is $97.4\%$, and execution speedup is $2.9\times$.
- **Rationale**: Decouples immutable raw input data storage from auxiliary consensus graph memory, confirming linear complexity $O(NL + L^2)$ for bipartite consensus.
- **Macros**: `\MemoryScalingTenKGraphReduction`, `\AnchorRAMReduction`, `\MemoryScalingTenKSpeedup`

### Claim 10: Conformal Inductive Projection and Point-of-Care Triage (Release v2.1.0)
- **Original Scope**: Transductive co-association clustering without uncertainty quantification.
- **Remediated Addition (Release v2.1.0)**: Integrated Conformal Inductive Consensus Clustering (`src/cicc/`):
  - Distribution-free finite-sample $(1 - \alpha)$ coverage guarantees on cluster assignments.
  - Target-decoy / knockoff False Discovery Rate (FDR) feature selection.
  - Automated point-of-care patient safety triage identifying ambiguous or out-of-distribution queries with $22.6\,\mu\text{s}$ per-query latency.
- **Rationale**: Upgrades transductive ensemble clustering into a clinically deployable, uncertainty-calibrated diagnostic instrument.
