# Report 05: Prior Art, Novelty Analysis & Literature Positioning

**Target Manuscript:** `ieee_manuscript/main.tex` (Section II: Related Work)  
**Literature Base:** IEEE TPAMI, IEEE TKDE, ACM SIGKDD, NeurIPS, ICML  
**Audit Dimension:** Novelty Defensibility, Baseline Attribution & Theoretical Differentiation  
**Date:** October 16, 2026  

---

## 1. Literature Landscape & Prior Art Survey

Consensus clustering methods generally divide into four distinct historical paradigms:

```
                            Consensus Clustering Paradigms
                                          │
       ┌────────────────────┬─────────────┴─────────────┬────────────────────┐
       ▼                    ▼                           ▼                    ▼
[Classical Dense Co-Assoc] [Anchor Bipartite Graphs]  [Feature Selection]  [Deep Clustering]
 • Fred & Jain (2005) EAC   • Huang et al. (U-SPEC)     • Wasserman (2014)   • Xie et al. (DEC 2016)
 • Strehl & Ghosh (CSPA)    • Nie et al. (FCAG 2024)    • Bimodality (Sarle) • Guo et al. (IDEC 2017)
 • Li et al. (2019) Halo    • Huang et al. (FastMICE)   • Sparse K-Means     • Li et al. (CC 2021)
```

### 1.1 Pairwise Co-Association Ensembles
- **Foundational Works:** Fred & Jain (IEEE TPAMI 2005; Evidence Accumulation Clustering - EAC); Strehl & Ghosh (JMLR 2002; CSPA, HGPA, MCLA).
- **Theoretical Bottleneck:** Storing and decomposing the dense $N \times N$ co-association matrix requires $\mathcal{O}(N^2)$ memory and $\mathcal{O}(N^3)$ spectral decomposition time.
- **Transductive Limitation:** Incapable of out-of-sample projection; new instances require re-clustering the combined corpus.

### 1.2 Scalable Anchor & Bipartite Graph Consensus
- **U-SPEC / U-SENC:** Huang, Wang, Wu, Lai, Kwoh (IEEE TKDE / TPAMI / arXiv:1903.01057). Introduces representative anchors and Transfer-Cut bipartite spectral consensus.
- **FCAG:** Nie, Xue, Yu, Li (IEEE TPAMI 2024, doi:10.1109/TPAMI.2023.3318603). Formulates fast bipartite anchor consensus graphs with out-of-sample extension.
- **FastMICE:** Huang, Wang, Lai (IEEE TKDE 2023, doi:10.1109/TKDE.2023.3236698). Fast multi-view consensus clustering using compact matrix factorizations.
- **Limitation Addressed by ICC-v2:** While these methods achieve near-linear complexity in $N$, they assume all feature dimensions are informative. In ultra-high-dimensional regimes ($D \gg N$) with $99\%$ distractor noise, pairwise distances concentrate, and anchor affinities degrade into uniform random connections.

### 1.3 High-Dimensional Feature Screening & Bimodality
- **Multimodal Screening:** Wasserman, Azizyan, Singh (arXiv:1406.2240; minimax multimodality testing for high-dimensional clustering).
- **Sarle's Bimodality Coefficient:** SAS Technical Report (1990); widely surveyed in computational genomics (e.g., Wang et al., *Cancer Informatics* 2009; *Frontiers in Genetics* 2021).
- **Role in ICC-v2:** ICC-v2 does not claim to invent the Bimodality Coefficient; rather, it introduces **Variance-Stabilized Subspace Gating (VSSG)** as an unsupervised gating mechanism that couples finite-sample corrected Sarle scores with diverse guided subspace ensembles.

---

## 2. Four-Quadrant Novelty Matrix

| Quadrant | Description | Methods / Concepts | ICC-v2 Distinction |
|:---:|---|---|---|
| **Quadrant A** | *Established in Prior Literature* | - Sarle Bimodality Coefficient (SAS 1990)<br>- Bipartite Transfer-Cut (Li et al. 2015; Huang et al. 2020)<br>- Centroid-based out-of-sample assignment | ICC-v2 rigorously cites foundational papers and disclaims invention of individual standard components. |
| **Quadrant B** | *Novel Synthesis of Established Mechanisms* | - Coupling VSSG candidate pool filtering with guided subspace ensembles.<br>- Constructing anchor graphs exclusively from stability-certified core points. | Integrates feature-space screening with instance-space core certification to defeat distance concentration. |
| **Quadrant C** | *Genuine Novel Theoretical & Methodological Contributions* | - **Proposition 2:** Exact closed-form determinacy identity $\sum_j S_{ij}^2$ in $O(M^2 N + M^2 K^2)$ without $N \times N$ matrix.<br>- **ASPP Framework:** Multi-family stability profiling in anchor space with linear $O(NL)$ memory.<br>- Empirical discovery of the $5\%\text{--}15\%$ biological gating window. | First consensus framework providing certified closed-form sample stability and multi-family stability fingerprints without quadratic tensors. |
| **Quadrant D** | *Disproven or Refracted Novelty Claims* | - Universal superiority across low-dimensional vision/sensor data.<br>- Downstream classifier test accuracy lift ($+4.5\%$) under heavy noise. | Honestly disclaimed in `main.tex` and `README.md`; documented as negative/calibrated findings. |

---

## 3. Baseline Attribution Corrections

During the audit, two historical attribution errors in the codebase were identified and rectified:
1. **FCAG Attribution:** In `src/icc/baselines/anchor.py`, FCAG was previously attributed to incorrect authors. The reference has been formally corrected to **Nie, Xue, Yu, Li, *IEEE TPAMI* 2024** (`doi:10.1109/TPAMI.2023.3318603`).
2. **FastMVC Clarification:** The codebase included a baseline labeled `FastMVC` marked as a stub. It was clarified that `FastMVC` is an internal benchmark stub approximating the multi-view principles of **FastMICE (Huang et al., *IEEE TKDE* 2023)**. In all configuration files and benchmark logs, it is explicitly flagged with `stub: true`, and all statistical tables are reported both with and without the stub to prevent baseline bias.
