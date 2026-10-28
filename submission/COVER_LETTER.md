# Submission Cover Letter

**To:**  
The Editor-in-Chief  
*Data Mining and Knowledge Discovery* (DAMI)  
Springer Nature  

**Date:** October 28, 2026  

**Subject:** Submission of Research Manuscript: *"When Does Bimodality-Gated Feature Selection Help Consensus Clustering?"* (ICC-v2)  

Dear Editor-in-Chief and Editorial Board,

We are pleased to submit our original research manuscript titled **"When Does Bimodality-Gated Feature Selection Help Consensus Clustering?"** for consideration for publication as a regular research paper in *Data Mining and Knowledge Discovery* (DAMI).

### Context and Core Problem
Consensus clustering synthesizes diverse base clusterings to discover stable partitions. However, in modern ultra-high-dimensional regimes ($D \gg N$), distance concentration severely degrades base partition accuracy, while classical $O(N^2)$ co-association matrices prevent out-of-sample inference. Existing high-dimensional cluster ensembles either rely on transductive graph co-clustering or uniform random subspace screening, which struggle under extreme isotropic noise.

### Contributions & Key Findings
In this manuscript, we present **Invariant Core Consensus v2 (ICC-v2)** and provide an empirical examination answering precisely *when* feature gating and anchor consensus improve high-dimensional clustering:
1. **Linear Bimodality-Gated Subspace Selection (BGSS):** Unsupervised $O(N \cdot D)$ screening based on Sarle's Bimodality Coefficient with finite-sample null calibration ($BC \le 5/9$), filtering isotropic distractor features before ensemble generation.
2. **Scalable Bipartite Anchor Consensus:** Reduces auxiliary memory from $O(N^2)$ to $O(N \cdot L)$ via rectangular co-association graphs ($L \ll N$) normalized with bipartite Transfer-Cut Laplacian spectra, cutting graph memory by 99.6% at $N = 10{,}000$.
3. **Closed-Form Inductive Inference:** Stability-weighted active centroid projection requiring $O(K \cdot |\mathcal{F}_{	ext{active}}|)$ operations per query point ($22.6\ \mu	ext{s}$ per biopsy), bypassing graph recomputation.
4. **Rigorous Empirical Examination & Falsification:** Evaluated across 13 diverse benchmarks spanning 3,000 total model fits across 12 clustering pipelines. While omnibus Friedman testing indicates no significant difference across heterogeneous low-D datasets ($p = 0.40$), ICC-v2 commands **Rank #1** on ultra-high-dimensional biological cancer cohorts ($D/N > 20$, mean ARI 0.217 vs 0.037 for standard consensus).
5. **Honest Boundary Characterization:** We identify and document the exact failure boundaries of marginal feature gating: non-linear multi-feature XOR interactions (Madelon), large-$K$ multi-class coordinate blending, and ultra-sparse zero-inflated count matrices.

### Research Integrity & Reproducibility
- **Zero Fabrication:** All numerical claims originate from frozen per-seed execution stores and automated macro bindings (`paper/numbers.tex`).
- **Literature Vintage:** 80.85% (38 of 47) of references are from 2024–2026, verified via automated CrossRef and arXiv REST APIs. Every reference is cited strictly once at first mention.
- **Code and Data Availability:** The complete open-source Python library (`icc`, `cicc`), unit tests (94 passing), and deterministic reproduction scripts are available at https://github.com/AkashKundu114/icc-clustering under an open-source MIT license.

This manuscript represents original work that has not been published previously and is not under consideration for publication elsewhere. All authors have approved the manuscript and agree with its submission to *Data Mining and Knowledge Discovery*.

Thank you very much for your time and consideration of our work.

Sincerely,

**Akash Kundu** (Corresponding Author)  
Department of Computer Science and Engineering  
Techno India University, Kolkata, India  
Email: akashkundu1152@gmail.com  

*On behalf of co-authors:*  
Trinankur Guha, Rupankar Ghatak, Anubhab Naskar, and Prof. Kalyan Kumar Das (Faculty Mentor).
