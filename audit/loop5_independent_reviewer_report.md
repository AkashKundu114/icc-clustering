# Loop 5: Independent Peer Reviewer Report

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DMKD)  
**Manuscript Title:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Authors:** Kalyan Kumar Das, Akash Kundu, Anirban Mukhopadhyay  
**Reviewer Persona:** Independent Reviewer for DMKD (Editorial Board Perspective)  
**Date:** November 2, 2026  
**Final Recommendation:** **Major Revision**  

---

## 1. Summary of the Manuscript

The paper investigates a ubiquitous yet poorly examined assumption in unsupervised data mining: that subsample stability serves as a reliable surrogate for clustering correctness in the high-dimensional, small-sample regime ($D \gg N$). 

Through controlled isotropic simulations and six high-dimensional biomedical microarray cohorts ($D/N > 20$), the authors demonstrate that multiple consensus and multi-view algorithms (including FCAG, FCM, and FastMVC) reproduce non-degenerate, highly stable partitions under resampling ($\text{Stab} \approx 0.684$) that have essentially zero correlation with clinical reference labels ($\text{Acc} \approx -0.003$). Using column-permuted null controls and a post-hoc non-degeneracy audit, the authors confirm that this stability is data-driven rather than a permutation artifact. 

To explore what algorithmic design choices can recover signal, the authors investigate Gated Anchor Consensus (GAC) as an experimental vehicle coupling marginal bimodality screening (BGSS), random-subspace base clusterers, and bipartite anchor-graph consensus. Across an omnibus benchmark of 13 datasets and 3,000 model fits, the authors honestly report that differences among the 12 evaluated methods are statistically indistinguishable (Friedman $p = 0.40$), and that GAC's gains are concentrated in cohorts exhibiting distinct marginal multimodality (Leukemia and SRBCT).

---

## 2. Major Strengths

1. **Vital Conceptual Contribution to Data Mining:** The consensus clustering literature has long operated under the heuristic that stability implies cluster validity. This paper provides clear, reproducible evidence that this heuristic fails dramatically in small-sample genomics, demonstrating that algorithms can converge stably onto technical artifacts or uninformative variance.
2. **Exemplary Methodological Candor:** The authors reject the temptation to present their experimental vehicle (GAC) as a universal breakthrough. They transparently report:
   - A non-significant omnibus benchmark ($p = 0.40$).
   - A definitive null result for sample determinacy anchor selection ($\Delta = +0.019, p = 0.84$).
   - A corrected historical control arm in random feature gating.
3. **Computational Scalability:** The bipartite anchor formulation effectively eliminates the quadratic memory barrier of dense consensus, scaling to $10^6$ instances in under 3 minutes on workstation hardware.

---

## 3. Major Concerns (Must Be Addressed in Revision)

1. **Proposition 1 Requires Formal Restriction to Symmetric Densities:**
   - Proposition 1 implies that $BC \le 5/9$ serves as a universal bound separating unimodal from multimodal distributions.
   - This holds strictly for *symmetric* unimodal distributions. Asymmetric unimodal distributions (such as log-normal or skewed exponential mixtures) regularly produce $BC > 5/9$ due to skewness ($\gamma^2$).
   - The authors must amend Proposition 1 to explicitly state the symmetry requirement and provide a Remark warning practitioners to log-transform skewed biological data.
2. **Inductive Centroid Projection Collapse on Non-Convex Manifolds:**
   - Equations (9)--(10) define an out-of-sample projection using Euclidean nearest centroids in the gated active subspace.
   - While spectral bipartite clustering uncovers non-linear manifold clusters in embedding space $U$, projecting back to Euclidean centroids in $\mathbb{R}^{|\mathcal{F}_{\text{active}}|}$ causes complete failure on non-convex manifolds (e.g., Concentric Circles, where inductive ARI collapses to $-0.003$).
   - The authors must explicitly state this geometric boundary condition in Section 4.3 and Section 8.3.
3. **Disentangling Technical Confounding from Biological Discordance on Prostate:**
   - The geometric forensic in Section 3.2 shows that spectral and anchor consensus partitions on Prostate correlate strongly with PC1 ($r = 0.77\text{--}0.86$) and total library depth ($r = -0.52\text{--}-0.59$).
   - The authors should explicitly discuss that these partitions are tracking unmodeled technical batch variation or RNA quality (Leek et al., 2010), rather than chance noise.
4. **Metadata Discrepancy:**
   - Line 39 of `paper/manuscript/main.tex` still contains the legacy PDF title in `\hypersetup`. This must be updated to match the accepted title.

---

## 4. Minor Concerns

- In Theorem 1, clarify that the linear time complexity $O(N)$ holds strictly for bounded anchor budgets ($L = O(1)$).
- In Section 6.1, clarify that empirical power-law exponents ($\beta < 1.0$) represent pre-asymptotic behavior due to constant overheads and BLAS multi-threading, rather than asymptotic sub-linear complexity.
- Ensure all citations in the revision plan (Beyer et al. 1999, Leek et al. 2010, Demšar 2006, Darlington 1970) are added to `references.bib`.

---

## 5. Technical Questions for the Authors

1. *Asymmetric Noise Filtering:* In the presence of log-normal distractor noise without log-transformation, what fraction of uninformative genes are retained by BGSS?
2. *Batch Harmonization:* If ComBat or another batch-correction algorithm is applied to the Prostate cohort prior to clustering, does the stability-accuracy gap shrink?
3. *Single-Cell Applicability:* On single-cell RNA-seq (PBMC68k-red), zero-inflation distorts higher moments. How do the authors propose extending BGSS to zero-inflated distributions?

---

## 6. Recommendation

**Major Revision.** The manuscript makes a valuable and highly reproducible contribution to the data mining literature. Once the mathematical qualification of Proposition 1 and the geometric boundary of centroid induction are incorporated, the paper will be fully suited for publication in *Data Mining and Knowledge Discovery*.
