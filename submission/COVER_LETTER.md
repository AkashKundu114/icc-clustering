# Cover Letter for Springer Nature (*Data Mining and Knowledge Discovery* / DAMI)

**To:**  
The Editor-in-Chief  
*Data Mining and Knowledge Discovery* (DAMI)  
Springer Nature  

**Date:** October 30, 2026  

**Subject:** Submission of Research Manuscript: *"An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts"*  

---

Dear Editor-in-Chief and Editorial Board,

We are pleased to submit our original research manuscript titled **"An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts"** for consideration for publication as a regular research paper in *Data Mining and Knowledge Discovery* (DAMI).

### Context and Core Problem
Consensus clustering synthesizes multiple base partitions to discover stable latent groupings. However, in modern high-dimensional noise regimes ($D \gg N$), distance concentration causes a counter-intuitive behavior: **stability-accuracy discordance**. Base clustering algorithms repeatedly converge on spurious noise boundaries with high apparent stability ($\text{Stability} \ge 0.50$ to $1.00$), while true partition recovery collapses ($\text{ARI} \le 0.05$). On real high-dimensional benchmarks ($D/N > 20$), our pre-specified stratified subsampling protocol demonstrates that the stability–accuracy gap reaches up to $+0.973$ (e.g., Spectral clustering on Prostate: stability $0.971$, ARI $-0.002$), while column-permuted null controls collapse to zero (mean $+0.007$).

### Contributions and Key Findings
In this manuscript, we provide a thorough empirical and geometric dissection answering precisely how consensus clustering behaves in high dimensions and what helps:
1. **Stability-Accuracy Discordance on Real and Synthetic Manifolds:** Under stratified subsampling, classical and graph-based baselines repeatedly converge to mutually agreeing partitions that do not reflect clinical reference labels. Across six high-$D$ biomedical cohorts, three methods (FCAG, FCM, FastMVC) satisfy our pre-specified non-degenerate discordance criterion on $\ge 3$ cohorts, with a paired bootstrap confirming a strictly positive overall gap of $+0.485$ (95% CI: $[+0.379, +0.662]$; unconstrained $+0.464$, 95% CI: $[+0.363, +0.607]$).
2. **What Helps: Random Subspaces and Bipartite Anchor Consensus:** We evaluate the Gated Anchor Consensus (GAC) pipeline, demonstrating that the primary empirical gains in cluster recovery stem from random-subspace ensembling combined with bipartite anchor consensus ($+0.118$ ARI gain over ambient consensus), while Bimodality-Gated Subspace Selection (BGSS) provides a targeted $+0.062$ enhancement (95% CI: $[+0.013, +0.142]$) in bimodal signal regimes.
3. **Scalability and Bipartite Compression:** Bipartite anchor graphs compress co-association memory from quadratic $O(N^2)$ to linear $O(NL)$, reducing graph memory by $99.6\%$ at $N=10{,}000$ and enabling million-sample clustering in $141\text{ s}$. Under clean, single-process, untraced benchmark runs, GAC scales sub-linearly with power-law empirical exponent $\beta = 0.55 \pm 0.01$ (95% CI: $[0.53, 0.57]$), achieving a $2.54\times$ speedup over ambient standard consensus.
4. **Empirical Boundaries and Negative Results:** In the spirit of scientific transparency, we document where consensus and feature gating fail: determinacy-based landmark certification yields an empirical null result over uniform random anchors ($\Delta = +0.019$, 95\% CI: $[-0.039, +0.082]$); on datasets with diffuse unimodal noise (Prostate, CNS), zero-inflated scRNA-seq counts, and non-linear parity (Madelon XOR), gating cannot isolate informative coordinates without detectable marginal separation.

### Declarations and Verification Standards
- **Originality and Exclusivity:** This manuscript represents entirely original work and has not been published previously, nor is it currently under consideration elsewhere.
- **Reproducibility and Code Availability:** Complete software implementations, benchmark datasets, test suites, and reproduction scripts are maintained under the MIT License at https://github.com/AkashKundu114/icc-clustering (release tag `v2.2.0`).
- **Authorship and Approval:** All listed authors (K. K. Das, A. Kundu, A. Mukhopadhyay) have reviewed, contributed to, and approved the final submitted manuscript.

We thank the editorial board and reviewers in advance for their time, consideration, and constructive evaluation.

Sincerely,

**Prof. Kalyan Kumar Das** (Corresponding Author)  
Department of Computer Science and Engineering, University of Kalyani  
Email: `kalyan.biltu@gmail.com`  

**Akash Kundu** (First Author & Lead Implementer)  
Email: `akashkundu1152@gmail.com`  

**Prof. Anirban Mukhopadhyay**  
Email: `anirban@cse.klyuniv.ac.in`  
