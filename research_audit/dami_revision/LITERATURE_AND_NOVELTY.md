# Phase 0: Scientific Literature, Prior Art and Novelty Audit

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Audit Persona:** Agent A5 — Literature and Novelty Auditor  
**Date:** November 1, 2026  
**Dedicated Revision Branch:** `research/dami-revision`  

---

## 1. Executive Summary

This literature and novelty audit evaluates the position of the manuscript within modern data mining, machine learning, and bioinformatics literature. It analyzes prior art across seven thematic pillars, verifies all bibliographic entries against Crossref and publisher records, establishes a structured literature matrix, and delineates the genuine scientific contribution from claims that must be recalibrated or qualified.

### Central Novelty Assessment:
1. **The Genuine Scientific Contribution:**  
   The primary, defensible contribution of this manuscript is **empirical and diagnostic**:
   - It provides a rigorous demonstration that **subsampling stability is decoupled from clustering accuracy** in high-dimensional biomedical cohorts ($D/N > 20$).
   - It shows that consensus clustering—widely deployed in cancer subtype discovery—can exhibit high stability ($>0.65$) on partitions that are biologically uncorrelated with diagnostic ground truth (mean $\text{Acc} \le 0.00$), driven by distance concentration and uncurated technical confounders (such as sequencing depth and library size, $r=0.77\text{--}0.86$ with PC1 in Prostate).
   - Through a 2x2 factorial ablation, it proves that bipartite graph compression alone ($0.046$) or random gating alone ($0.047$) does not improve on ambient consensus ($0.037$), whereas bimodality gating (BGSS) provides a **conditional benefit** concentrated in discrete multi-class cohorts (Leukemia, SRBCT).
2. **What is Established Prior Art (Not Novel):**  
   - Bipartite anchor graph spectral partitioning is well-established (Liu et al., *ICML* 2010; Li et al., *IEEE TKDE* 2015, 2019; Nie et al., *IEEE TPAMI* 2024).
   - Sarle's Bimodality Coefficient is a classical univariate statistic (Sarle, 1983; Knapp, 2007).
   - Sparse clustering via regularized feature weighting was formulated by Witten & Tibshirani (*JASA* 2010).
3. **Calibrated Theoretical Claims:**  
   - Proposition 2 (sample determinacy bounds for core anchors) is mathematically derived but empirically an **indistinguishable null** ($\Delta = +0.019, p = 0.84$), as shown in Knockout 4. It cannot be framed as a requisite driver of clustering accuracy.

---

## 2. Seven-Pillar Structured Literature Matrix

| Domain / Area | Canonical Citation & DOI | Core Research Question & Method | Dataset Scope | Key Finding & Limitations | Relationship to Present Work |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Cluster Stability & Instability** | **von Luxburg (2010)**  
*Found. Trends ML*  
DOI: [10.1561/2200000008](https://doi.org/10.1561/2200000008) | How does clustering stability behave asymptotically and in finite samples? Formal perturbation analysis. | Synthetic mixtures & standard metrics | Stability reflects the uniqueness of the objective minimizer, NOT the "correctness" of cluster boundaries. An algorithm can stably converge to an arbitrary geometric artifact. | Theoretical foundation for our discordance thesis: stability measures self-consistency, not biological validity. |
| **2. Consensus Clustering** | **Monti et al. (2003)**  
*Machine Learning*  
DOI: [10.1023/A:1023949509487](https://doi.org/10.1023/A:1023949509487) | Can resampling and consensus matrices reliably reveal molecular subtypes in cancer microarrays? | Leukemia (Golub), Medulloblastoma, diffuse B-cell lymphoma | Pioneered consensus matrices and CDF area tracking. Widely adopted in cancer genomics.  
*Limitation:* Does not account for distance concentration in ambient $D \gg N$. | Baseline benchmark (`StdCons`). Serves as the primary target of our discordance evaluation. |
| **3. Null Consensus & Spurious Structure** | **Senbabaoglu et al. (2014)**  
*Sci. Rep.*  
DOI: [10.1038/srep06207](https://doi.org/10.1038/srep06207) | Does consensus clustering find spurious clusters in unimodal null data? Evaluates PAC (proportion of ambiguous clustering). | Simulated unimodal Gaussians & TCGA profiles | Consensus clustering readily generates visually convincing sigmoid CDF curves on unimodal null data with no true clusters. PAC overestimates $K$. | Validates our column-permuted null controls and the necessity of non-degeneracy rules. |
| **4. Distance Concentration** | **Beyer et al. (1999)**  
*ICDT*  
DOI: [10.1007/3-540-49257-7_15](https://doi.org/10.1007/3-540-49257-7_15) | Under what conditions do nearest-neighbor distances become meaningless as dimension $D \to \infty$? | High-dimensional Euclidean spaces | Ratio of distance to nearest vs. farthest point approaches 1: $\lim_{D \to \infty} \frac{d_{\max} - d_{\min}}{d_{\min}} = 0$. Contrast vanishes. | Explains why ambient consensus clustering collapses to chance accuracy on high-D cohorts. |
| **5. Sparse Clustering & Gating** | **Witten & Tibshirani (2010)**  
*JASA*  
DOI: [10.1198/jasa.2010.tm09415](https://doi.org/10.1198/jasa.2010.tm09415) | How to cluster samples while simultaneously selecting a sparse subset of discriminative features? $L_1$-penalized K-Means. | Breast cancer & microarray cohorts | Directly optimizes feature weights via alternating BCSS maximization.  
*Limitation:* Highly sensitive to initialization; susceptible to local minima in $D/N > 20$. | Modern baseline (`SparseKMeans`). Evaluated in Table 3 and fair baseline comparisons. |
| **6. Anchor Graph Spectral Clustering** | **Nie et al. (2024)**  
*IEEE TPAMI*  
DOI: [10.1109/TPAMI.2023.3323062](https://doi.org/10.1109/TPAMI.2023.3323062) | How to achieve scalable spectral clustering without building an $N \times N$ affinity matrix? Bipartite anchor graph. | Large-scale vision & speech benchmarks | Constructs $N \times m$ sample-to-anchor graph, reducing spectral eigensolve from $O(N^3)$ to $O(m^3)$.  
*Limitation:* Operates in ambient space; distance concentration distorts anchor assignments. | Key architectural baseline (`FCAG`). Demonstrates that anchor acceleration without gating collapses on high-D. |
| **7. Multi-View Ensemble Bipartite Consensus** | **Huang et al. (2023)**  
*IEEE TKDE*  
DOI: [10.1109/TKDE.2023.3236698](https://doi.org/10.1109/TKDE.2023.3236698) | Fast multi-view clustering via ensembles (FastMICE) using bipartite anchor graphs. | Multi-view benchmark suites | Fuses bipartite graphs across views with adaptive weights and ADMM optimization.  
*Limitation:* Requires multi-view structure; ambient views suffer noise concentration. | Addressed in Finding F-23: our proxy baseline is officially designated as `FastMVC-Surrogate`. |

---

## 3. Bibliographic Integrity & Vintage Audit

All 75 citations in `paper/references.bib` have been verified for:
1. **DOI Validity:** Every major journal and conference reference has a direct resolvable DOI.
2. **Author and Title Accuracy:** Reconciled against Crossref and publisher APIs (IEEE, Springer, Nature, ACM, Oxford University Press).
3. **No Fabricated References:** Zero phantom citations or hallucinated literature.
4. **Citation Vintage Distribution:**
   - 2020–2026: 28 citations (37.3%) — incorporates modern anchor methods (Nie et al. 2024; Huang et al. 2023; Belucci et al. 2024).
   - 2010–2019: 25 citations (33.3%) — establishes foundation in single-cell, deep clustering, and stability theory (Kiselev et al. 2017; Xie et al. 2016; Senbabaoglu et al. 2014; von Luxburg 2010; Witten & Tibshirani 2010).
   - Pre-2010: 22 citations (29.3%) — classical foundational works (Monti et al. 2003; Golub et al. 1999; Hubert & Arabie 1985; Sarle 1983; MacQueen 1967; Ward 1963).

---

## 4. Nuanced Framing of the Manuscript Contribution

To ensure scientific defensibility for *Data Mining and Knowledge Discovery*:

1. **Avoid Universal Dominance Claims:**  
   The paper must not claim that GAC (ICC-v2) is an omnibus winner across all data regimes. The Friedman test ($p=0.40$) proves that across general low-to-medium dimensional benchmarks, top methods perform comparably.
2. **Precision in High-D Bimodal Regimes:**  
   Frame GAC specifically as an architecture designed for high-dimensional regimes ($D \gg N$) where genuine cluster separation is driven by a sparse subset of coordinates with strong bimodal marginal distributions (e.g. lineage-specific oncogenes in ALL vs. AML).
3. **Empirical Frankness Regarding Core Anchors:**  
   Present Proposition 2 as a mathematical characterization of sample determinacy, while candidly noting that in practice uniform random landmark sampling performs equally well in bipartite consensus.
4. **Transparent Confounding Disclosures:**  
   Emphasize the finding that unsupervised consensus methods frequently lock onto technical sequencing depth ($r=0.77\text{--}0.86$ with PC1 in Prostate) as an urgent methodological warning to the bioinformatics community.
