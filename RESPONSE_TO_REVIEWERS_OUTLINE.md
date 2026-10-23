# Response-to-Reviewers Outline & Defense Strategy
**Manuscript:** "Inductive Consensus Clustering in High-Dimensional Manifolds: Bipartite Anchor Certification and Subspace Gating"  
**Target:** Springer Nature (*Pattern Analysis and Applications*)  

---

## Response to Common Reviewer Inquiries

### 1. Concern: "Why does ICC-v2 rank fifth overall across the 13 multi-domain benchmark datasets?"
**Response:**
- We agree with the reviewer and report the omnibus rankings with complete transparency. As documented in Section 5.3 (Table 3), Deep Embedded Clustering (DEC, $R=4.31$) and classical hierarchical Ward linkage ($R=5.31$) perform strongly on text and image domains where sample sizes are large ($N > 1{,}000$) and features are dense.
- Consensus clustering with feature gating is explicitly tailored for the high-dimensional, small-sample regime ($D/N > 20$, e.g. cancer microarray genomics), where deep networks suffer from parameter over-fitting due to scarce training data ($N \le 100$). In this biomedical subgroup, ICC-v2 achieves Rank \#1 ($R=2.33$), yielding $+0.498$ ARI gain over standard consensus on SRBCT.

### 2. Concern: "Does marginal bimodality gating (VSSG/BGSS) alone solve clustering on complex biological manifolds?"
**Response:**
- We thank the reviewer for highlighting this key distinction. In our ablation study (Section 5.2), we demonstrate that marginal gating alone does *not* solve clustering: VSSG followed by plain K-Means on Leukemia achieves an ARI of only $0.019$, which is lower than unguided K-Means on the full feature space ($0.101$).
- The actual performance gain on real-world biological datasets stems from the synergy between subspace ensembling, bipartite anchor consensus, and stability-weighted centroid assignment. Gating serves as a dimensional filter, but manifold recovery requires spectral consensus over the anchor graph.

### 3. Concern: "How does the inductive step compare to traditional out-of-sample extensions like Nyström approximation or kNN?"
**Response:**
- In Section 5.1 (Inductive Generalization), we benchmark the proposed stability-weighted active subspace centroid projection against direct K-Means projection and Nyström spectral extension. On Leukemia, the inductive projection achieves an ARI of $0.714$, outperforming direct centroid projection ($0.172$). On SRBCT, it achieves $0.455$ vs. $0.083$ for direct projection.
- Unlike the Nyström method, which requires computing an $N \times m$ cross-affinity kernel matrix for each new query, our centroid projection assigns an out-of-sample query in $O(K \cdot |\mathcal{F}_{\text{active}}|)$ operations, providing extreme-speed inference suitable for online and streaming data.

### 4. Concern: "What are the theoretical limits of Sarle's Bimodality Coefficient in heavy-tailed or bounded noise regimes?"
**Response:**
- In Section 3 and our pre-registered confirmatory synthetic evaluation across 18,000 Monte Carlo replicates, we explicitly analyze the distribution of Sarle's BC.
- We show that while Sarle's BC is well-calibrated under Gaussian and discrete Poisson-lognormal counts ($\text{FDP} \le 0.04$), heavy-tailed distributions (such as Student-$t_5$ at $D=10{,}000$) inflate sample kurtosis variance, leading to false discovery boundary crossings. We have documented this as an explicit theoretical scope limit in Section 5.5 (Limitations) rather than claiming universal distribution-free optimality.
