# Cover Letter Draft
**Target Journal:** *Pattern Analysis and Applications* (Springer Nature)  
**Article Type:** Original Research Article  
**Title:** Inductive Consensus Clustering in High-Dimensional Manifolds: Bipartite Anchor Certification and Subspace Gating  
**Authors:** Anubhab Naskar, Kalyan Kumar Das  
**Affiliation:** Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India  

---

Dear Editor-in-Chief and Editorial Board,

We submit our original research manuscript titled **"Inductive Consensus Clustering in High-Dimensional Manifolds: Bipartite Anchor Certification and Subspace Gating"** for consideration as a regular research article in *Pattern Analysis and Applications*.

### Context & Contribution
Consensus clustering ensembles provide robust, initialization-resilient data partitions across biomedical and machine learning domains. However, standard formulations face two fundamental constraints:
1. **The Transductive Bottleneck:** Operating on an $N \times N$ dense co-association matrix requires $O(N^2)$ storage and forbids inductive assignment to unseen out-of-sample queries without re-solving the global consensus graph from scratch.
2. **High-Dimensional Distractor Noise:** In small-sample, high-dimensional regimes ($D \gg N$), distance concentration degrades Euclidean metrics, trapping standard ensemble consensus in arbitrary noise boundaries.

To resolve these challenges without incurring quadratic computational overhead, we introduce **Inductive Consensus Clustering (ICC-v2)**. Our framework combines:
- A linear $O(N \cdot D)$ marginal feature screening filter based on Sarle’s Bimodality Coefficient (Bimodality-Gated Subspace Selection, BGSS) that isolates multimodal candidate dimensions;
- A determinacy-based bipartite anchor consensus mechanism that reduces auxiliary storage from $O(N^2)$ to $O(N \cdot L)$ ($L \ll N$); and
- A stability-weighted centroid assignment for $O(K \cdot |\mathcal{F}_{\text{active}}|)$ instant inductive out-of-sample projection.

### Empirical Rigor & Benchmark Scope
Across an extensive benchmark of 13 multi-domain datasets spanning 11 candidate algorithms (1,430 total model fits), we provide a strictly calibrated evaluation. While Deep Embedded Clustering (DEC) achieves the lowest omnibus mean rank across diverse domains ($R=4.31$), ICC-v2 attains the highest Grand Mean Adjusted Rand Index (0.160) and attains Rank \#1 ($R=2.33$) on the high-dimensional biomedical subgroup ($D/N > 20$, with ARI = 0.680 on Leukemia and 0.538 on SRBCT, achieving an absolute ARI improvement of $+0.498$ over standard consensus). Furthermore, our bipartite anchor formulation reduces consensus auxiliary memory by $97.0\%$ at $N=10{,}000$ and scales smoothly to $N=1{,}000{,}000$ instances in $55.6$ seconds.

### Editorial & Reproducibility Declarations
- **Originality:** This work has not been published previously and is not under consideration elsewhere.
- **Reproducibility:** All datasets, experiment runners, pre-registration specifications, and the full PyTorch/Python codebase are completely open-source and hosted in our public GitHub repository. Every empirical value in the manuscript is generated through automated, single-source LaTeX macro bindings.
- **AI Use Disclosure:** Formatted strictly in compliance with Springer Nature author guidelines; generative AI tools were employed solely for code optimization and automated grammar/syntax verification, with no role in scientific ideation, derivations, or experimental design.

Thank you for your time and consideration of our manuscript.

Sincerely,  
**Anubhab Naskar** (Corresponding Author)  
Department of Computer Science and Engineering, Techno India University  
Email: `anubhab231001001443@technoindiaeducation.com`  

**Kalyan Kumar Das**  
Department of Computer Science and Engineering, Techno India University  
Email: `kalyankumar.das@technoindiaeducation.com`  
