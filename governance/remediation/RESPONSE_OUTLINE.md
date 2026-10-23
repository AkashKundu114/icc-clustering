# REVIEWER RESPONSE & DEFENSE STRATEGY (RESPONSE_OUTLINE.md)

**Canonical Manuscript Title**: "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue**: Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version**: `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Authors**: Antigravity Remediation Team  
**Date**: October 2026  

---

## Reviewer Critique 1: Fairness of Baseline Comparisons
> *"In the primary benchmark, ICC-v2 incorporates Variance-Guided Subspace Generation (VSSG) to filter features, whereas the baseline algorithms (K-Means, Ward, Spectral Clustering, FCM) are evaluated on the entire ambient feature space. Isn't this an unfair advantage?"*

### Author Response:
We thank the reviewer for this critical observation. We have directly addressed this concern by conducting an extensive fair baseline evaluation (`results/phase2/fair_baselines.csv`) across all 13 benchmark datasets and 10 seeds:
1. **Evaluated Pipelines**: We benchmarked K-Means and Standard Consensus equipped with standard feature selection and dimensionality reduction:
   - **Variance Filtering (top 15% features)**: Matches the feature budget of ICC-v2.
   - **Principal Component Analysis (PCA/SVD)**: Preserves top orthogonal variance components.
   - **Laplacian Score**: State-of-the-art unsupervised graph-based feature ranking.
   - **Sparse K-Means**: Witten & Tibshirani $L_1$-penalized feature-weighted clustering.
2. **Empirical Evidence (Pass F Frozen Ground Truth)**:
   - On the high-dimensional cancer datasets ($D/N > 20$), ICC-v2 achieves a Mean ARI of **0.217**, substantially outperforming PCA + K-Means (**0.054**), Sparse K-Means (**0.051**), K-Means with Variance Filtering (**0.046**), Laplacian Score (**0.041**), PCA + Standard Consensus (**0.038**), and Variance Filter + Standard Consensus (**0.032**).
   - Simple feature pre-filtering fails to resolve cluster structure because marginal variance does not account for multi-partition stability. ICC-v2’s performance stems synergistically from coupling null-calibrated bimodality screening with multi-subspace ensembling and bipartite Transfer-Cut spectral clustering.

---

## Reviewer Critique 2: Statistical Significance & Omnibus Separation
> *"The Friedman omnibus test across all 13 benchmarks yields $p = 0.48$, and the true Nemenyi Critical Difference is $\text{CD} = 4.19$. Doesn't this mean ICC-v2 is statistically indistinguishable from baseline methods across the omnibus collection?"*

### Author Response:
We appreciate this incisive critique. We have revised the manuscript to be completely transparent regarding statistical power and regime boundaries:
1. **Regime-Specific Specialization**: ICC-v2 is tailored for continuous high-dimensional noise regimes ($D \gg N$). It is not designed to replace classical methods in low-dimensional dense domains or large-sample acoustic/NLP datasets (such as 20 Newsgroups with $K=20$ or Isolet with $K=26$), where hierarchical Ward linkage or deep clustering naturally excels.
2. **Targeted Subgroup Superiority**: When evaluating the targeted high-dimensional biomedical regime ($D/N > 20$, 6 datasets):
   - ICC-v2 achieves **Rank #1 with Mean ARI = 0.217** (vs Standard Consensus 0.037, DEC 0.045, K-Means 0.056).
   - Across all 13 benchmarks, the omnibus Grand Mean ARI is **0.152** (Rank 5.23).
   - We have reported the exact formula-derived Nemenyi threshold $\text{CD} = 4.19$ for $k=11, N=13$ and Friedman omnibus test ($\chi_F^2 = 9.59, p = 0.48$), transparently confirming that no algorithm achieves global dominance across heterogeneous domains simultaneously.

---

## Reviewer Critique 3: Seed Sensitivity on Leukemia
> *"The reported ARI on Leukemia shows considerable standard deviation ($0.600 \pm 0.367$), with some early text claiming $0.846$. What accounts for this instability?"*

### Author Response:
We thank the reviewer for highlighting this important behavior. We have conducted a granular multi-seed audit:
1. **Bimodal Seed Behavior**: On Leukemia ($N=72, D=7{,}129$), across 30 independent random seeds, 23 of 30 seeds ($76.7\%$) achieve robust cluster recovery with ARI $> 0.50$, yielding a non-parametric median ARI of $0.787$, while 7 seeds experience spectral sensitivity resulting in near-zero ARI.
2. **Cherry-Picking Elimination**: The early figure of $0.846$ reflected selective reporting of non-zero runs. In the Pass F protocol, we expanded to 30 independent seeds, reporting the full empirical distribution ($0.600 \pm 0.367$) via automated LaTeX macros (`\LeukemiaTableThreeARI`) alongside Khan SRBCT ($0.546 \pm 0.102$).
3. **Manifold Sparsity Analysis**: We have added an explicit discussion explaining that on tiny-sample biological manifolds ($N=72$), spectral embedding is inherently sensitive to initialization anchors. We recommend running ensemble restarts or increasing anchor counts when sample size is under 100.

---

## Reviewer Critique 4: Structural Limitations of Marginal Saliency (Madelon)
> *"Can Variance-Stabilized Subspace Gating (VSSG) detect all types of feature relevance, such as non-linear feature interactions?"*

### Author Response:
We agree completely with the reviewer. In Section 5.3 and our theoretical foundations (`REMEDIATION/THEORY_NOTES.md`), we have explicitly documented the mathematical boundary conditions of VSSG:
1. **Marginal 1D Limitation**: VSSG computes Sarle's Bimodality Coefficient along 1D marginal projections. For datasets governed by non-linear parity or XOR interactions (such as Madelon, where clusters cannot be separated by any single feature in isolation), marginal distributions are strictly unimodal Gaussians.
2. **Empirical Boundary**: Across all 500 features of Madelon, the maximum observed $b_d$ is $0.5042$, which is strictly below the Sarle uniform threshold ($5/9 \approx 0.5556$).
3. **Transparent Reporting**: We replaced earlier over-claims with the empirical truth: VSSG achieves Recall@50 = **0.400** and Precision@50 = **0.156** on Madelon. We explicitly state this as an architectural negative scope boundary, noting that non-linear interaction discovery requires non-linear metric learning or neural autoencoders prior to consensus clustering.

---

## Reviewer Critique 5: Out-of-Sample Inductive Evaluation
> *"How is the inductive capability of ICC-v2 validated on independent, unseen test instances?"*

### Author Response:
We have conducted a dedicated out-of-sample inductive evaluation across 9 benchmark datasets using stratified 80% train / 20% test splits over 10 independent seeds (`results/phase2/inductive_direct.csv`):
1. **Direct Nystrom Centroid Projection**: Unseen query points are projected onto geometry-calibrated centroids in the active VSSG subspace (`model.predict(X_test, subspace=True)`).
2. **Empirical Validation**:
   - On Leukemia: Direct Nystrom subspace projection achieves a test-set ARI of **0.714**, substantially outperforming standard out-of-sample K-Means (**0.172**) and PCA + K-Means (**0.203**).
   - On SRBCT: Direct Nystrom subspace projection achieves a test-set ARI of **0.455** vs. **0.083** for K-Means.
   - These findings confirm that inductive projection within the certified subspace successfully generalizes to unseen biological samples.

---

## Reviewer Critique 6: Point-of-Care Clinical Reliability & Conformal Prediction (Release v2.1.0)
> *"Standard consensus clustering produces hard partition labels without query-level confidence or patient safety guarantees. How does this system ensure safety in clinical oncological settings?"*

### Author Response:
In active release `v2.1.0`, we addressed this clinical translational requirement through Conformal Inductive Consensus Clustering (`src/cicc/`):
1. **Finite-Sample Error Guarantees**: We introduced split-conformal p-values providing distribution-free $(1 - \alpha)$ coverage guarantees for cluster membership sets.
2. **Target-Decoy FDR Screening**: Implemented knockoff/decoy feature filtering ensuring strict control over False Discovery Rates under high-dimensional noise.
3. **Point-of-Care Patient Safety Triage**: The system automatically flags ambiguous or out-of-distribution biopsy queries for clinical pathological review whenever the conformal prediction set contains multiple clusters or an empty set, executing in $22.6\,\mu\text{s}$ per query.
