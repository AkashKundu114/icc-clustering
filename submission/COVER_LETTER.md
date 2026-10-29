# Submission Cover Letter

**To:**  
The Editor-in-Chief  
*Data Mining and Knowledge Discovery* (DAMI)  
Springer Nature  

**Date:** October 29, 2026  

**Subject:** Submission of Research Manuscript: *"Stable but Wrong: Why Consensus Clustering Can Fail in High Dimensions, and What Helps"*  

Dear Editor-in-Chief and Editorial Board,

We are pleased to submit our original research manuscript titled **"Stable but Wrong: Why Consensus Clustering Can Fail in High Dimensions, and What Helps"** for consideration for publication as a regular research paper in *Data Mining and Knowledge Discovery* (DAMI).

### Context and Core Problem
Consensus clustering synthesizes multiple base partitions to discover stable latent groupings. However, in modern high-dimensional noise regimes ($D \gg N$), distance concentration causes a counter-intuitive failure mode: the **stability trap**. Base clustering algorithms repeatedly converge on spurious noise boundaries with high apparent stability ($\text{Stability} > 0.80$), while true partition recovery collapses to zero ($\text{ARI} \to 0.0$). On real benchmarks, we document that this stability-accuracy gap $\Delta = \text{Stability} - \text{ARI}$ reaches up to $0.852$ (e.g. Spectral on Colon: stability $0.852$, ARI $0.000$).

### Contributions & Key Findings
In this manuscript, we provide a thorough empirical and geometric dissection answering precisely *why* consensus clustering fails in high dimensions and *what helps*:
1. **The Stability Trap on Real and Synthetic Manifolds:** We document the stability-accuracy gap across 13 diverse benchmark datasets and controlled distractor regimes, proving that consensus stability alone is fundamentally uninformative in high dimensions without explicit feature gating.
2. **What Helps: Random Subspaces and Bipartite Anchor Consensus:** We demonstrate that the primary empirical gains in cluster recovery stem from random-subspace ensembling combined with bipartite anchor consensus (+0.118 ARI gain), which scales co-association in linear $O(NL)$ space.
3. **What Gating Adds:** Bimodality-Gated Subspace Selection (BGSS) adds a focused $+0.062$ ARI gain over random gating ($95\%\ \text{CI}: [+0.021, +0.108]$, Wilcoxon $p = 0.031$), concentrated specifically in small-sample cohorts with pronounced marginal bimodal signal (Leukemia: $0.436$, SRBCT: $0.347$).
4. **Honest Boundary Characterization:** We identify and document the exact boundaries of marginal gating: non-linear multi-feature XOR parity (Madelon), large-$K$ multi-class coordinate blending, and ultra-sparse count dropouts.

### Research Integrity & Reproducibility
- **Zero Fabrication:** All numerical claims originate from frozen per-seed execution stores and automated macro bindings (`paper/numbers.tex`).
- **Literature Vintage:** 75.0% (39 of 52) of references are from 2024–2026, verified via automated CrossRef and arXiv REST APIs. Every reference is cited strictly once at first mention.
- **Code and Data Availability:** The complete open-source Python library (`icc`, `cicc`), unit tests (94 passing), and deterministic reproduction scripts are available at https://github.com/AkashKundu114/icc-clustering under an open-source MIT license. The repository name `icc-clustering` is historical and unrelated to the Iterative Consensus Clustering of Race and Meyer.

This manuscript represents original work that has not been published previously and is not under consideration for publication elsewhere. All authors have approved the manuscript and agree with its submission to *Data Mining and Knowledge Discovery*.

Thank you very much for your time and consideration of our work.

Sincerely,

**Akash Kundu** (Corresponding Author)  
Department of Computer Science and Engineering  
Techno India University, Kolkata, India  
Email: akashkundu1152@gmail.com  

*On behalf of co-authors:*  
Trinankur Guha, Rupankar Ghatak, Anubhab Naskar, and Prof. Kalyan Kumar Das (Faculty Mentor).
