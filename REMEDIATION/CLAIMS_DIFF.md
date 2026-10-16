# CLAIMS DIFFERENTIAL LEDGER (CLAIMS_DIFF.md)

**Title**: Systematic Differential Between Original Published Claims and Remediated Scientific Truth  
**Repository**: `github.com/AkashKundu114/icc-clustering`  
**Manuscript**: *Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes* (ICC-v2)  
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
- **Remediated Claim**: Grounded on the frozen 10-seed Table 3 benchmark average:
  $$\text{ARI} = \mathbf{0.680 \pm 0.363}$$
  In ablation re-runs, V5 achieves $0.621 \pm 0.334$, while uniform random anchor sampling (V4) achieves $0.628 \pm 0.331$.
- **Rationale**: Investigation in `REMEDIATION/AUDIT_SPOTCHECK.md` revealed that 2 of 10 random seeds fail on tiny-$N$ biological manifolds ($N=72$). Reporting $0.846$ reflected selective reporting of successful runs. The revised text honestly reports the full 10-seed distribution and analyzes bimodal seed sensitivity.
- **Macros**: `\LeukemiaTableThreeARI`, `\LeukemiaAblationVFiftyARI`, `\LeukemiaAblationVFourARI`

### Claim 3: SRBCT Multiclass Cluster Recovery
- **Original Claim**: Section 5.2 claimed ICC-v2 achieves $\text{ARI} = 0.681 \pm 0.037$ on SRBCT.
- **Remediated Claim**: Grounded on the frozen 10-seed Table 3 benchmark average:
  $$\text{ARI} = \mathbf{0.538 \pm 0.110}$$
  In ablation sweeps, V5 achieves $0.614 \pm 0.180$, and V4 achieves $0.650 \pm 0.138$.
- **Rationale**: Replaces optimistic point estimates with the frozen 10-seed benchmark ground truth.
- **Macros**: `\SrbctTableThreeARI`, `\SrbctAblationVFiftyARI`, `\SrbctAblationVFourARI`

### Claim 4: VSSG Non-Linear Feature Saliency on Madelon
- **Original Claim**: Section 5.3 claimed VSSG achieves $\text{PR-AUC} = 0.892$ and $\text{Recall@50} = 0.95$ on Madelon ($D=500, D_{\text{signal}}=20$).
- **Remediated Claim**: Formally declared as an architectural negative scope boundary:
  $$\text{Recall@50} = \mathbf{0.400}, \quad \text{Precision@50} = \mathbf{0.156}$$
  Maximum observed Bimodality Coefficient across all 500 features is $\mathbf{0.5042} < 5/9$.
- **Rationale**: Madelon cluster geometry is determined by pairwise XOR interactions. Projecting XOR features onto 1D marginals yields unimodal Gaussian distributions. Because VSSG is a marginal 1D filter, it cannot theoretically isolate non-linear interactions without marginal shifts.
- **Macros**: `\VssgMadelonMaxBC`, `\VssgMadelonRecallFifty`, `\VssgMadelonPrecisionFifty`

### Claim 5: Nemenyi Critical Difference Calibration
- **Original Claim**: Section 5.4 reported Nemenyi Critical Difference threshold $\text{CD} = 2.62$.
- **Remediated Claim**: Corrected to the true two-tailed Studentized range critical value for $k=11$ models across $N=13$ datasets:
  $$\mathbf{\text{CD} = 4.21}$$
- **Rationale**: $\text{CD} = 2.62$ belonged to an earlier audit script evaluating $k=9$ models across $N=21$ datasets. For Table 3 ($k=11, N=13$), $q_{0.05} \sqrt{\frac{11 \times 12}{6 \times 13}} = 3.219 \times 1.3009 = 4.21$. The text claim of "decisive omnibus separation" is softened to note that Friedman omnibus testing ($p = 0.33$) indicates no statistical dominance across all heterogeneous domains simultaneously.
- **Macro**: `\TrueNemenyiCD`, `\TableThreeFriedmanPValue`

### Claim 6: Biomedical Subgroup Ranking ($D/N > 20$)
- **Original Claim**: Section 5.4 text claimed ICC-v2 achieves an average rank of $1.50$ on the $D/N > 20$ subgroup.
- **Remediated Claim**: Corrected to the exact Table 3 subgroup average rank:
  $$\mathbf{R = 2.33}$$
  (Ranking #1 overall, with DEC at $5.00$, FCM at $5.67$, K-Means at $5.83$, Standard Consensus at $6.33$, and Li et al. at $7.83$).
- **Rationale**: The true rank of ICC-v2 on the 6 datasets with $D/N > 20$ (Colon, Leukemia, SRBCT, CNS, Ovarian, Prostate) is 2.33. While remaining the top-ranked model, the text over-claim of 1.50 is corrected.
- **Macro**: `\RankBioICCvTwo`, `\TableThreeIccVTwoHighDRank`

### Claim 7: Fair Baseline Comparison on High-D Regimes
- **Original Claim**: Only un-gated ambient baselines (K-Means, Ward, Spectral, FCM) were benchmarked against ICC-v2.
- **Remediated Addition**: Evaluated Variance Filter, PCA/SVD, Laplacian Score, and Sparse K-Means across all 13 benchmarks over 10 seeds:
  - On the $D/N > 20$ high-D cancer datasets, ICC-v2 achieves a Mean ARI of $\mathbf{0.258}$, outperforming K-Means with Variance Filtering ($0.050$), Sparse K-Means ($0.044$), PCA + K-Means ($0.042$), and Laplacian Score ($0.041$).
- **Rationale**: Preempts reviewer critique regarding unfair comparisons by demonstrating that ICC-v2's ensembling and Transfer-Cut architecture provides an ~5x advantage over simple pre-filtering.
- **Macros**: `\FairBaselinesIccVTwoHighDMean`, `\FairBaselinesKmVarFiltHighDMean`

### Claim 8: Direct Inductive Out-of-Sample Prediction
- **Original Claim**: Inductive extension was evaluated primarily as downstream classifier training on pseudo-labels.
- **Remediated Addition**: Evaluated direct Nystrom out-of-sample centroid projection in the active subspace on held-out 20% test splits:
  - On Leukemia, direct Nystrom projection achieves test $\text{ARI} = \mathbf{0.714}$ vs. $0.172$ for K-Means and $0.203$ for PCA + K-Means.
  - On SRBCT, direct Nystrom projection achieves test $\text{ARI} = \mathbf{0.455}$ vs. $0.083$ for K-Means.
- **Rationale**: Directly validates the out-of-sample projection mechanism of ICC-v2 on independent test splits.
- **Macros**: `\InductiveLeukemiaNystromARI`, `\InductiveSrbctNystromARI`
