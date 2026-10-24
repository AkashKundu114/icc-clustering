"""
Script to apply required revisions to paper/main.tex and springer_manuscript/main.tex.
Follows all prompt instructions:
- Update Title and Abstract
- Update Introduction contributions list and 3-stage pipeline reframing
- Add Related Work positioning (bimodality gene filtering, Fern & Brodley 2003, U-SENC note)
- Reconcile anchor budget in Algorithm 1 and Section 4.2
- Neutral anchor naming in Section 4.2 (null result note)
- Condense ASPP to one short paragraph as optional/future work
- Add Hyperparameter Protocol and evaluation unit in Section 5
- Fix Knockout 2 sign (+0.14)
- Add 20 Newsgroups text sparsity limitation to Section 5.5
- Replace Section 6 with 6.1 (Oncology), 6.2 (Single-cell, N=1,000,000, 240 MB, PBMC68k rank last), 6.3 (Point-of-care inductive assignment, O(K*|F_active|), bootstrap CIs span zero)
- Update Conclusion to match reframed narrative, zero em-dashes
"""

from pathlib import Path


def revise_content(text: str) -> str:
    # 1. Title
    target_title = (
        r"\title[When Does Feature Gating and Anchor Consensus Improve"
        r" High-Dimensional Clustering?]{When Does Feature Gating and Anchor"
        r" Consensus Improve High-Dimensional Clustering? An Empirical"
        r" Examination}"
    )
    repl_title = (
        r"\title[When Does Bimodality-Gated Feature Selection Help Consensus"
        r" Clustering?]{When Does Bimodality-Gated Feature Selection Help"
        r" Consensus Clustering?}"
    )
    assert target_title in text, "Target title not found"
    text = text.replace(target_title, repl_title, 1)

    # 2. Abstract
    target_abs_start = (
        r"\abstract{Consensus clustering synthesizes diverse base partitions"
        r" to discover robust data groupings."
    )
    target_abs_end = (
        r"We conclude with a detailed characterization of failure modes under"
        r" platykurtic and non-linear parity structures.}"
    )
    idx_abs_start = text.find(target_abs_start)
    assert idx_abs_start != -1, "Target abs start not found"
    idx_abs_end = text.find(target_abs_end, idx_abs_start)
    assert idx_abs_end != -1, "Target abs end not found"
    full_target_abs = text[idx_abs_start : idx_abs_end + len(target_abs_end)]

    repl_abs = (
        r"\abstract{Consensus clustering is often assumed to protect against"
        r" high-dimensional noise, and dense $N \times N$ consensus is often"
        r" assumed to be unavoidable. We test both assumptions. In"
        r" finite-sample simulations with isotropic distractor features ($D \gg"
        r" N$), base clusterers, particularly spectral and Ward, converge"
        r" stably ($\text{stability} > 0.8$) on arbitrary noise partitions"
        r" while ARI falls toward zero, so ensemble averaging alone does not"
        r" remove the noise. We then study ICC-v2, a pipeline that combines"
        r" linear-time Bimodality-Gated Subspace Selection (BGSS), a"
        r" random-subspace ensemble, bipartite anchor-graph consensus, and"
        r" closed-form centroid-based out-of-sample assignment. Across 13"
        r" benchmarks (2,750 model fits), we find no statistically significant"
        r" difference between methods (Friedman $p = 0.48$); Standard Consensus"
        r" has the best mean rank (4.85) and ICC-v2 ranks fourth (5.23)."
        r" ICC-v2's higher Grand Mean ARI (0.152) is driven by two cancer"
        r" microarray datasets, Leukemia (0.600) and SRBCT (0.546); it is near"
        r" zero on most others, and on Prostate ICC-v2 underperforms simple"
        r" baselines (0.012 vs. 0.049). On the six $D/N > 20$ cohorts, ICC-v2"
        r" ranks first (exploratory, $n = 6$, not significant after Holm"
        r" correction). Ablations show that BGSS drives the accuracy gain and"
        r" that bipartite compression, not determinacy-based anchor"
        r" certification, drives the efficiency gain: certified anchors are"
        r" statistically indistinguishable from random anchors ($\Delta ="
        r" +0.019$, 95\% CI [$-0.039, +0.082$]), while the bipartite graph"
        r" cuts consensus-graph memory by 99.6\% at $N = 10{,}000$. We"
        r" characterize failure modes under non-linear parity structure,"
        r" zero-inflated features, and large $K$.}"
    )
    text = text.replace(full_target_abs, repl_abs, 1)

    # 3. Intro pipeline and contributions
    target_intro_start = (
        r"To address these limitations, this paper investigates the"
        r" \textbf{Inductive Consensus Clustering (ICC)} framework"
        r" (Fig.~\ref{fig:conceptual_overview})."
    )
    target_intro_end = r"Section~\ref{sec:conclusion} concludes the paper."
    idx_intro_start = text.find(target_intro_start)
    assert idx_intro_start != -1, "Target intro start not found"
    idx_intro_end = text.find(target_intro_end, idx_intro_start)
    assert idx_intro_end != -1, "Target intro end not found"
    full_target_intro = text[
        idx_intro_start : idx_intro_end + len(target_intro_end)
    ]

    repl_intro = (
        r"To address these limitations, this paper investigates the"
        r" \textbf{Inductive Consensus Clustering (ICC)} framework"
        r" (Fig.~\ref{fig:conceptual_overview}). We examine the finite-sample"
        r" empirical breakdown of consensus stability under isotropic"
        r" distractor noise (Section~\ref{sec:falsification}), illustrating how"
        r" distance concentration generates consensus agreement on arbitrary"
        r" noise boundaries. Motivated by these findings, we formulate"
        r" \textbf{ICC-v2} as a three-stage pipeline coupled with an optional"
        r" post-hoc diagnostic:"
        "\n"
        r"\begin{itemize}"
        "\n"
        r"    \item \textbf{Bimodality-Gated Subspace Selection (BGSS):} An"
        r" $O(N \cdot D)$ linear feature screening mechanism utilizing Sarle's"
        r" Bimodality Coefficient ($\hat{b}_d = \frac{\hat{\gamma}_d^2 +"
        r" 1}{\hat{\kappa}_d + 3 \cdot \frac{(N-1)^2}{(N-2)(N-3)} +"
        r" \epsilon}$)~\cite{sarle1983sas,ellison1987bimodality,pfister2013assessing}"
        r" to filter unimodal distractor noise prior to base ensemble fitting."
        "\n"
        r"    \item \textbf{Bipartite Anchor Graph Consensus:} Constructs a"
        r" rectangular bipartite co-association graph $B \in [0, 1]^{N \times"
        r" L}$ over $L$ anchors, reducing auxiliary memory from $O(N^2)$ to"
        r" $O(N \cdot L)$ and accelerating spectral decomposition onto an $L"
        r" \times L$ anchor affinity space."
        "\n"
        r"    \item \textbf{Stability-Weighted Subspace Centroid Assignment:}"
        r" Provides closed-form inductive out-of-sample mapping that assigns"
        r" unseen query instances in $O(K \cdot |\mathcal{F}_{\text{active}}|)$"
        r" time without recomputing the consensus graph."
        "\n"
        r"    \item \textbf{Optional Diagnostic: Anchor-Space Perturbation"
        r" Profiling (ASPP):} An optional post-hoc diagnostic module that"
        r" probes cluster structural resilience across physical perturbation"
        r" families directly over anchor coordinates."
        "\n"
        r"\end{itemize}"
        "\n\n"
        r"The primary contributions of this work are fourfold:"
        "\n"
        r"\begin{enumerate}"
        "\n"
        r"    \item \textbf{Finite-sample evidence of a stability--accuracy"
        r" gap:} Under isotropic distractor noise ($D \gg N$), consensus"
        r" stability remains high while ARI collapses toward zero across"
        r" several noise distributions."
        "\n"
        r"    \item \textbf{A linear-time marginal-bimodality gate (BGSS):}"
        r" Analyzed with explicit failure conditions (bounded uniform support,"
        r" zero-inflation, non-linear XOR parity, and small-$N$ detection"
        r" power) and compared against variance, PCA, Laplacian-score, and"
        r" sparse $k$-means baselines under matched feature budgets."
        "\n"
        r"    \item \textbf{A factorial ablation separating accuracy from"
        r" efficiency:} BGSS supplies the accuracy gain, bipartite compression"
        r" supplies the memory and runtime gain, while anchor certification"
        r" yields a null result ($\Delta = +0.019$, 95\% CI: $[-0.039,"
        r" +0.082]$)."
        "\n"
        r"    \item \textbf{A scalability and failure-mode study:} ICC-v2 runs"
        r" at $N=10^6$ in 141--183~s, with empirical characterization of"
        r" negative results and boundary failure modes (near-zero ARI on most"
        r" datasets, $K \ge 20$, Prostate, Madelon, and sparse TF-IDF text)."
        "\n"
        r"\end{enumerate}"
        "\n\n"
        r"The remainder of this manuscript is structured as follows:"
        r" Section~\ref{sec:related} reviews related work and positions our"
        r" methodology. Section~\ref{sec:falsification} presents our empirical"
        r" analysis of distance concentration and consensus behavior."
        r" Section~\ref{sec:framework} details the mathematical architecture"
        r" and complexity analysis of ICC-v2. Section~\ref{sec:experiments}"
        r" provides empirical evaluations across generalization, ablation,"
        r" real-world benchmarks, and scalability, followed by an explicit"
        r" discussion of limitations. Section~\ref{sec:applications} details"
        r" three illustrative use cases and their limits across translational"
        r" oncology, million-scale single-cell transcriptomics, and"
        r" point-of-care inductive decision support."
        r" Section~\ref{sec:conclusion} concludes the paper."
    )
    text = text.replace(full_target_intro, repl_intro, 1)

    # 4. Related Work addition
    target_rw = (
        r"Similarly, non-parametric multimodality testing (e.g., the Dip Test"
        r" by Hartigan and Hartigan~\cite{hartigan1985dip} and Sarle's"
        r" Bimodality"
        r" Coefficient~\cite{sarle1983sas,ellison1987bimodality,pfister2013assessing})"
        r" provides statistical screening criteria. As summarized in"
        r" Table~\ref{tab:taxonomy_comparison}, ICC-v2 combines linear"
        r" bimodality subspace gating, determinacy-based bipartite anchor"
        r" consensus, and inductive centroid projection into a unified"
        r" linear-time pipeline."
    )
    repl_rw = (
        r"Similarly, non-parametric multimodality testing (e.g., the Dip Test"
        r" by Hartigan and Hartigan~\cite{hartigan1985dip} and Sarle's"
        r" Bimodality"
        r" Coefficient~\cite{sarle1983sas,ellison1987bimodality,pfister2013assessing})"
        r" provides statistical screening criteria. As summarized in"
        r" Table~\ref{tab:taxonomy_comparison}, ICC-v2 combines linear"
        r" bimodality subspace gating, bipartite anchor graph consensus, and"
        r" inductive centroid projection into a unified linear-time"
        r" pipeline."
        "\n\n"
        r"\subsection{Positioning Against Bimodality Filtering and Random"
        r" Subspaces}\label{sec:positioning}"
        "\n"
        r"Non-parametric multimodality testing has historically served in"
        r" bioinformatics as a static 1D gene pre-filter for differential"
        r" expression or single clustering algorithms. Similarly,"
        r" random-subspace cluster ensembles (Fern and"
        r" Brodley~\cite{fern2003random}) demonstrated that random feature"
        r" projections improve ensemble diversity and partition accuracy when"
        r" ambient features are informative; however, under extreme distractor"
        r" noise ($D \gg N$), unguided random subspaces sample predominantly"
        r" non-informative dimensions, causing ensemble consensus to collapse"
        r" onto noise partitions. BGSS differs by coupling linear-time marginal"
        r" bimodality gating with randomized subspace ensembling: by"
        r" restricting subspace sampling to the bimodality-screened candidate"
        r" pool $\mathcal{F}_{\text{active}}$, it preserves ensemble diversity"
        r" while preventing subspace collapse onto pure noise. In scalable"
        r" ensemble clustering, ultra-scalable bipartite anchor methods such as"
        r" U-SPEC and U-SENC~\cite{huang2020ultra} compress the co-association"
        r" graph via $k$-means anchors; however, because no standalone"
        r" implementation of U-SENC was integrated into our evaluation harness,"
        r" it was not executed as an empirical baseline in our benchmark suite."
    )
    assert target_rw in text, "Target rw not found"
    text = text.replace(target_rw, repl_rw, 1)

    # 5. Section 4.2 Anchor Naming & Budget
    target_sec42 = (
        r"\subsection{Determinacy-Based Bipartite Anchor"
        r" Consensus}\label{sec:anchor_consensus}"
    )
    repl_sec42 = (
        r"\subsection{Bipartite Anchor Graph"
        r" Consensus}\label{sec:anchor_consensus}"
    )
    assert target_sec42 in text, "Target sec42 not found"
    text = text.replace(target_sec42, repl_sec42, 1)

    target_sec42_body = (
        r"Given sample determinacy $\boldsymbol{\sigma} \in [0, 1]^N$, ICC-v2"
        r" extracts a core anchor set $\mathcal{A}_{\text{core}} = \{a_1,"
        r" \dots, a_L\}$ of size $L \ll N$ (default $L=40$) from samples"
        r" exceeding stability quantile $\tau_{\text{core}}$. ICC-v2 then"
        r" constructs a rectangular bipartite co-association matrix $B \in [0,"
        r" 1]^{N \times L}$ where $B_{ia} = \frac{1}{M}\sum_{m=1}^M"
        r" \mathbf{1}\{\pi_m(\mathbf{x}_i) = \pi_m(\mathbf{x}_a)\}$ in $O(N"
        r" \cdot L)$ memory."
    )
    repl_sec42_body = (
        r"Given sample determinacy $\boldsymbol{\sigma} \in [0, 1]^N$, ICC-v2"
        r" extracts an anchor set $\mathcal{A} = \{a_1, \dots, a_L\}$ of size"
        r" $L \ll N$ (default $L=40$) from samples exceeding stability"
        r" quantile $\tau_{\text{core}}$. All benchmark experiments used fixed"
        r" default $L=40$ ($L = \min(40, |\mathcal{C}_{\text{core}}|)$); the"
        r" dynamic rule $L = \max(40, 10K)$ is an exploratory recommendation"
        r" for datasets with $K \ge 20$, analyzed in Section~\ref{sec:limitations}."
        r" Crucially, empirical ablation (Section~\ref{sec:exp2_knockout})"
        r" reveals that determinacy-ordered anchors achieve accuracy"
        r" statistically indistinguishable from uniform random anchors ($V_5$"
        r" vs. $V_4$: $\Delta = +0.019$, 95\% CI: $[-0.039, +0.082]$),"
        r" establishing that bipartite graph compression rather than anchor"
        r" certification is the primary operational driver. ICC-v2 then"
        r" constructs a rectangular bipartite co-association matrix $B \in [0,"
        r" 1]^{N \times L}$ where $B_{ia} = \frac{1}{M}\sum_{m=1}^M"
        r" \mathbf{1}\{\pi_m(\mathbf{x}_i) = \pi_m(\mathbf{x}_a)\}$ in $O(N"
        r" \cdot L)$ memory."
    )
    assert target_sec42_body in text, "Target sec42 body not found"
    text = text.replace(target_sec42_body, repl_sec42_body, 1)

    # 6. Condense ASPP (Section 4.4)
    target_aspp_start = (
        r"\subsection{Anchor-Space Perturbation Profiling (ASPP)}\label{sec:aspp}"
    )
    target_aspp_end = (
        r"where $d_{(1)}$ and $d_{(2)}$ represent Euclidean distances to the"
        r" closest and second-closest active subspace centroids."
    )
    idx_aspp_start = text.find(target_aspp_start)
    assert idx_aspp_start != -1, "Target aspp start not found"
    idx_aspp_end = text.find(target_aspp_end, idx_aspp_start)
    assert idx_aspp_end != -1, "Target aspp end not found"
    full_target_aspp = text[
        idx_aspp_start : idx_aspp_end + len(target_aspp_end)
    ]

    repl_aspp = (
        r"\subsection{Optional Diagnostic: Anchor-Space Perturbation"
        r" Profiling (Future Work)}\label{sec:aspp}"
        "\n"
        r"Anchor-Space Perturbation Profiling (ASPP) is an optional post-hoc"
        r" diagnostic framework designed to probe cluster structural"
        r" resilience against perturbation families (instance dropout,"
        r" subspace masking, additive measurement noise, synthetic batch"
        r" shifts, and algorithmic jitter) directly over bipartite anchor"
        r" coordinates. Because ASPP introduces auxiliary computational"
        r" overhead and is not required for partition generation, it was"
        r" disabled during all benchmark evaluations to preserve strictly"
        r" linear runtime and memory complexity ($O(N \cdot D)$). We detail"
        r" its formal stability metrics, perturbation sensitivity indices"
        r" ($\mathrm{PSI}_k \in [0, 1]$), and out-of-sample query confidence"
        r" scores in the supplementary technical report as a direction for"
        r" future diagnostic exploration."
    )
    text = text.replace(full_target_aspp, repl_aspp, 1)

    # 7. Knockout 2 sign fix
    target_ko2 = (
        r"\item \textbf{Knockout 2: Removing Bipartite Anchor Graph (V5 $\to$"
        r" V2):} Replacing bipartite anchor consensus ($O(NL)$) with full"
        r" dense consensus ($O(N^2)$) under identical BGSS features causes the"
        r" subgroup mean ARI to drop from $\AblationHighDSubgroupFullIccVTwo$"
        r" to $\AblationHighDSubgroupBgssStdCons$ ($\Delta = -0.139$, $95\%$"
        r" CI: $[+0.065, +0.218]$). Standard dense co-association averaging"
        r" across the noisy base partitions creates spurious dense edges,"
        r" whereas anchor distillation concentrates consensus weights"
        r" exclusively on stable manifold anchors."
    )
    repl_ko2 = (
        r"\item \textbf{Knockout 2: Removing Bipartite Anchor Graph (V5 $\to$"
        r" V2):} Replacing bipartite anchor consensus ($O(NL)$) with full"
        r" dense consensus ($O(N^2)$) under identical BGSS features yields a"
        r" subgroup mean ARI difference of $V_5 - V_2 = +0.14$ ($95\%$ CI:"
        r" $[+0.065, +0.218]$), with $V_5$ achieving"
        r" $\AblationHighDSubgroupFullIccVTwo$ compared to"
        r" $\AblationHighDSubgroupBgssStdCons$ for $V_2$. Standard dense"
        r" co-association averaging across the noisy base partitions introduces"
        r" spurious dense edges, whereas bipartite anchor distillation"
        r" concentrates consensus weights exclusively on stable manifold"
        r" anchors."
    )
    assert target_ko2 in text, "Target ko2 not found"
    text = text.replace(target_ko2, repl_ko2, 1)

    # 8. Hyperparameter Protocol and Statistics Wording
    target_stat = (
        r"\textbf{Statistical Significance Analysis:}"
        "\n"
        r"Across all 13 benchmarks, Friedman omnibus"
        r" testing~\cite{demsar2006statistical} yields $\chi_F^2 = 9.59$, $p ="
        r" \TableThreeFriedmanPValue$, indicating no statistically significant"
        r" difference across the omnibus collection."
    )
    repl_stat = (
        r"\textbf{Hyperparameter Protocol and Evaluation Unit:}"
        "\n"
        r"All benchmark experiments (Table~\ref{tab:benchmark_ari} and"
        r" Table~\ref{tab:fair_baselines}) were executed with hyperparameters"
        r" fixed \textit{a priori} across all datasets without any post-hoc"
        r" tuning or label supervision. Specifically, base ensemble size was"
        r" fixed to $M=25$, active candidate feature pool fraction to $\alpha ="
        r" 0.15$ ($|\mathcal{F}_{\text{active}}| = \min(D, \max(K, \lfloor 0.15"
        r" D \rfloor))$), anchor budget to $L=40$ ($L = \min(40, N)$), and"
        r" core determinacy threshold to median quantile $\tau_{\text{core}} ="
        r" 0.50$. No dataset-specific hyperparameter grid searches were"
        r" conducted on the benchmark cohorts, preventing optimistic"
        r" overfitting to ground-truth labels. The primary statistical unit of"
        r" analysis is the dataset ($N=13$ omnibus, $n=6$ high-dimensional"
        r" subgroup), with random seeds (30 seeds on $D/N > 20$ cohorts, 10"
        r" seeds on standard benchmarks) treated as repeated measures within"
        r" each dataset."
        "\n\n"
        r"\textbf{Statistical Significance Analysis:}"
        "\n"
        r"Across all 13 benchmarks, Friedman omnibus"
        r" testing~\cite{demsar2006statistical} yields $\chi_F^2 = 9.59$, $p ="
        r" \TableThreeFriedmanPValue$, indicating no statistically significant"
        r" difference across the omnibus collection."
    )
    assert target_stat in text, "Target stat not found"
    text = text.replace(target_stat, repl_stat, 1)

    # 9. Limitations update (20 Newsgroups text sparsity)
    target_lim = (
        r"\item \textbf{Sparse, Zero-Inflated, and Non-Linear Features:} BGSS"
        r" evaluates marginal moments independently. Features with heavy point"
        r" masses at zero (e.g., single-cell RNA counts or sparse TF-IDF text"
        r" features) or non-linear multi-feature interactions (e.g., XOR"
        r" parity structures) can either spuriously inflate Sarle\'s"
        r" Bimodality Coefficient or fail to manifest marginal bimodality,"
        r" requiring multi-dimensional interaction screening in future"
        r" architectures."
    )
    repl_lim = (
        r"\item \textbf{Sparse, Zero-Inflated, and Non-Linear Features:} BGSS"
        r" evaluates marginal moments independently. Features with heavy point"
        r" masses at zero (e.g., single-cell RNA counts) or non-linear"
        r" multi-feature interactions (e.g., XOR parity structures) can either"
        r" spuriously inflate Sarle's Bimodality Coefficient or fail to"
        r" manifest marginal bimodality, requiring multi-dimensional"
        r" interaction screening in future architectures."
        "\n"
        r"    \item \textbf{High-Dimensional Text Sparsity (20 Newsgroups):}"
        r" On 20 Newsgroups ($N=18{,}846, D=10{,}000, K=20$), ICC-v2 yields an"
        r" ARI of $0.000 \pm 0.000$. BGSS is fundamentally mismatched to sparse"
        r" TF-IDF features where extreme vocabulary sparsity and high point"
        r" masses at zero invalidate continuous unimodal/bimodal moment"
        r" screening, whereas classical Ward linkage ($0.099$) and DEC"
        r" ($0.096$) achieve non-zero cluster separation."
    )
    assert target_lim in text, "Target lim not found"
    text = text.replace(target_lim, repl_lim, 1)

    # 10. Replace Section 6 completely
    target_sec6_start = (
        r"\section{Practical Real-World Applications and Domain Case"
        r" Studies}\label{sec:applications}"
    )
    target_sec6_end = (
        r"accelerating consensus grouping while maintaining robust topic"
        r" coherence." + "\n" + r"\end{enumerate}"
    )
    idx_s6_start = text.find(target_sec6_start)
    assert idx_s6_start != -1, "Target sec6 start not found"
    idx_s6_end = text.find(target_sec6_end, idx_s6_start)
    assert idx_s6_end != -1, "Target sec6 end not found"
    full_target_sec6 = text[idx_s6_start : idx_s6_end + len(target_sec6_end)]

    repl_sec6 = (
        r"\section{Illustrative Use Cases and Their Limits}\label{sec:applications}"
        "\n\n"
        r"To examine how the empirical properties and trade-offs of ICC-v2"
        r" manifest in domain-specific workflows, this section presents three"
        r" illustrative use cases spanning translational oncology, large-scale"
        r" single-cell transcriptomics, and point-of-care inductive assignment,"
        r" highlighting their practical utility alongside explicit empirical"
        r" boundaries."
        "\n\n"
        r"\subsection{Translational Oncology}\label{sec:app_oncology}"
        "\n"
        r"In translational cancer genomics, molecular subtyping via microarray"
        r" and RNA-seq profiling routinely operates in small-sample,"
        r" high-dimensional regimes ($N \le 100, D \ge 2{,}000\text{ to"
        r" }20{,}000$) where distance concentration degrades unguided"
        r" consensus clustering~\cite{golub1999molecular,khan2001multiplex}. On"
        r" the Leukemia microarray benchmark ($N=72, D=7{,}129, K=2$), ICC-v2"
        r" attains an ARI of $0.600 \pm 0.367$, with 22 of 30 canonical random"
        r" seeds achieving $\text{ARI} > 0.50$ (median ARI $0.787$). On the"
        r" pediatric SRBCT benchmark ($N=83, D=2{,}308, K=4$), ICC-v2 delivers"
        r" an ARI of $0.546 \pm 0.102$ (median $0.547$, with $70.0\%$ of seeds"
        r" exceeding $0.50$). Furthermore, BGSS captures 27 of the top 50"
        r" known supervised diagnostic marker genes ($54.0\%$ overlap) purely"
        r" unsupervised in $O(N \cdot D)$ time as a descriptive finding."
        "\n\n"
        r"However, outcomes on other high-dimensional cohorts reveal strict"
        r" limitations: across the remaining four high-dimensional cohorts"
        r" (CNS, Colon, Ovarian, and Prostate), ICC-v2 yields near-zero ARI"
        r" ($\le 0.072$), with $0/30$ seeds exceeding $0.50$, and on Prostate"
        r" ($0.012 \pm 0.013$) it underperforms simple ambient baselines"
        r" ($0.049$). These results suggest BGSS-gated ensembling can recover"
        r" coarse subtype structure on some cohorts, but outcomes are highly"
        r" seed-dependent and not clinically actionable without validation."
        "\n\n"
        r"\subsection{Single-Cell Transcriptomics}\label{sec:app_scrna}"
        "\n"
        r"Droplet-based single-cell RNA sequencing (scRNA-seq) profiles tens"
        r" of thousands to millions of individual"
        r" cells~\cite{zheng2017massively}. Storing an $N \times N$ dense"
        r" co-association matrix in double precision for $N=1{,}000{,}000$"
        r" cells requires approximately $8\text{ Terabytes of RAM}$, creating"
        r" a consensus memory wall on standard workstations. By mapping $N$"
        r" cells to $L=60$ representative anchor prototypes, ICC-v2 replaces"
        r" the $N \times N$ matrix with an $N \times L$ bipartite affinity"
        r" matrix $B$ and an $L \times L$ anchor affinity graph"
        r" $W_{\text{anchor}}$. At $N=1{,}000{,}000$ cells, the auxiliary"
        r" consensus graph memory requires only $10^6 \times 60 \times 4\text{"
        r" bytes} = 240.0\text{ MB}$, a $99.6\%$ reduction over the dense"
        r" matrix."
        "\n\n"
        r"However, this scaling feasibility is established primarily under"
        r" synthetic Gaussian mixture benchmarks (Experiment~5,"
        r" Table~\ref{tab:exp5_controlled}, where ICC-v2 scales to"
        r" $N=1{,}000{,}000$ in \ExtremeScaleTime\ with $\text{ARI} \approx"
        r" 0.36$). On real biological single-cell data, such as"
        r" PBMC68k-reduced ($N=68{,}579, D=1{,}000$), ICC-v2 achieves an ARI"
        r" of $0.182 \pm 0.009$ and ranks last among evaluated baselines,"
        r" trailing K-Means ($0.555 \pm 0.008$) and Standard Consensus ($0.540"
        r" \pm 0.004$). Thus, while bipartite graph compression successfully"
        r" solves the memory scaling bottleneck on single-node hardware,"
        r" partition quality on sparse, dropout-dominated single-cell"
        r" distributions requires further algorithmic refinement."
        "\n\n"
        r"\subsection{Point-of-Care Inductive Query"
        r" Assignment}\label{sec:app_conformal}"
        "\n"
        r"Traditional consensus clustering frameworks are strictly"
        r" transductive: when a new patient profile or query sample arrives,"
        r" conventional algorithms cannot assign the query without appending it"
        r" to the historical dataset and re-executing the entire $O((N+1)^2)$"
        r" ensemble consensus optimization from scratch. ICC-v2 addresses this"
        r" latency bottleneck via stability-weighted centroid assignment in the"
        r" active feature subspace (Section~\ref{sec:centroid})."
        "\n\n"
        r"Closed-form centroid assignment costs $O(K \cdot"
        r" |\mathcal{F}_{\text{active}}|)$ per query and agrees with"
        r" unweighted nearest-centroid on 94--99\% of held-out queries"
        r" (Table~\ref{tab:inductive_direct}). However, its test ARI is not"
        r" significantly better than Ambient K-Means, Nystr\"om spectral"
        r" extension, or Random Forest extensions (all bootstrap confidence"
        r" intervals span zero: $\Delta = +0.046$, 95\% CI: $[-0.029, +0.129]$"
        r" vs. Ambient K-Means; $\Delta = -0.023$, 95\% CI: $[-0.081, +0.033]$"
        r" vs. Nystr\"om; $\Delta = -0.006$, 95\% CI: $[-0.053, +0.046]$ vs."
        r" Random Forest). Inductive centroid projection therefore provides an"
        r" efficient, closed-form computational approximation for streaming"
        r" query assignment, but does not achieve superior out-of-sample"
        r" accuracy compared to standard projection alternatives."
    )
    text = text.replace(full_target_sec6, repl_sec6, 1)

    # 11. Conclusion reframing and zero em-dash enforcement
    target_concl = (
        r"This paper presented an empirical examination of consensus"
        r" clustering in high-dimensional noise regimes, systematically"
        r" investigating when feature gating, anchor consensus, and inductive"
        r" projection succeed and where they fail. Through finite-sample"
        r" falsification experiments, we showed that conventional consensus"
        r" stability metrics degrade under high-dimensional isotropic"
        r" distractor noise, converging stably onto arbitrary noise"
        r" partitions. We evaluated Inductive Consensus Clustering (ICC-v2),"
        r" which combines linear Bimodality-Gated Subspace Selection (BGSS),"
        r" bipartite anchor consensus, and stability-weighted centroid"
        r" assignment. Across 13 multi-domain benchmarks (2,750 model fits),"
        r" Standard Consensus achieves the lowest omnibus mean rank"
        r" ($R=\TableThreeStdConsOverallRank$), followed by K-Means"
        r" ($R=\TableThreeKMeansOverallRank$), DEC ($R=\TableThreeDecOverallRank$),"
        r" and ICC-v2 ($R=\TableThreeIccVTwoOverallRank$, Friedman $\chi_F^2 ="
        r" 9.59, p = \TableThreeFriedmanPValue$, $CD = \TrueNemenyiCD$)."
        r" Although ICC-v2 attains the highest Grand Mean ARI (\GrandMeanARI),"
        r" this metric is heavily driven by large gains on two cancer"
        r" microarray benchmarks: Leukemia (\ARIleukemia) and SRBCT (\ARIsrbct,"
        r" $+0.408$ over FastMVC), while averaging"
        r" \OmnibusMeanExcludingLeukemiaSrbct\ on the remaining 11 benchmarks"
        r" (omnibus median ARI: \OmnibusMedianARI). In the exploratory"
        r" high-dimensional subgroup ($D/N > 20$), ICC-v2 achieves Rank \#1"
        r" ($R=\RankBioICCvTwo$), but fails on Prostate ($0.012$ vs. $0.049$)."
        r" Our ablation experiments establish a key null result: determinacy"
        r" anchor certification yields no statistically significant accuracy"
        r" benefit over uniform random anchors ($\Delta = +0.019$,"
        r" dataset-level cluster bootstrap 95\% CI: $[-0.039, +0.082]$),"
        r" indicating that bipartite anchor graph"
        r" dimensionality reduction---reducing graph memory by"
        r" \MemoryScalingTenKGraphReduction\ at $N=10{,}000$ and enabling"
        r" $N=1{,}000{,}000$ scaling in \ExtremeScaleTime\ under"
        r" single-precision batch ensembling ($M=15, L=60$)---is the primary"
        r" operational mechanism rather than anchor certification. Finally, our"
        r" failure analysis demonstrates that marginal moment gating cannot"
        r" resolve non-linear parity structures or sparse zero-inflated counts,"
        r" delineating the exact boundaries of consensus clustering in"
        r" high-dimensional noise."
    )
    repl_concl = (
        r"This paper presented an empirical examination of consensus"
        r" clustering in high-dimensional noise regimes, systematically"
        r" investigating when feature gating, anchor consensus, and inductive"
        r" projection succeed and where they fail. Through finite-sample"
        r" falsification experiments, we showed that conventional consensus"
        r" stability metrics degrade under high-dimensional isotropic"
        r" distractor noise, converging stably onto arbitrary noise"
        r" partitions. We evaluated Inductive Consensus Clustering (ICC-v2),"
        r" which combines linear Bimodality-Gated Subspace Selection (BGSS),"
        r" bipartite anchor consensus, and stability-weighted centroid"
        r" assignment. Across 13 multi-domain benchmarks (2,750 model fits),"
        r" Standard Consensus achieves the lowest omnibus mean rank"
        r" ($R=\TableThreeStdConsOverallRank$), followed by K-Means"
        r" ($R=\TableThreeKMeansOverallRank$), DEC ($R=\TableThreeDecOverallRank$),"
        r" and ICC-v2 ($R=\TableThreeIccVTwoOverallRank$, Friedman $\chi_F^2 ="
        r" 9.59, p = \TableThreeFriedmanPValue$, $CD = \TrueNemenyiCD$)."
        r" Although ICC-v2 attains the highest Grand Mean ARI (\GrandMeanARI),"
        r" this metric is heavily driven by large gains on two cancer"
        r" microarray benchmarks: Leukemia (\ARIleukemia) and SRBCT (\ARIsrbct),"
        r" while averaging \OmnibusMeanExcludingLeukemiaSrbct\ on the"
        r" remaining 11 benchmarks (omnibus median ARI: \OmnibusMedianARI). In"
        r" the exploratory high-dimensional subgroup ($D/N > 20$), ICC-v2"
        r" achieves Rank \#1 ($R=\RankBioICCvTwo$), but fails on Prostate"
        r" ($0.012$ vs. $0.049$). Our ablation experiments establish a key null"
        r" result: determinacy anchor certification yields no statistically"
        r" significant accuracy benefit over uniform random anchors ($\Delta ="
        r" +0.019$, dataset-level cluster bootstrap 95\% CI: $[-0.039,"
        r" +0.082]$), indicating that bipartite anchor graph compression"
        r" (reducing graph memory by \MemoryScalingTenKGraphReduction\ at"
        r" $N=10{,}000$ and enabling $N=1{,}000{,}000$ scaling in"
        r" \ExtremeScaleTime\ under single-precision batch ensembling) is the"
        r" primary operational mechanism rather than anchor certification."
        r" Finally, our failure analysis demonstrates that marginal moment"
        r" gating cannot resolve non-linear parity structures or sparse"
        r" zero-inflated counts, delineating the exact boundaries of consensus"
        r" clustering in high-dimensional noise."
    )
    assert target_concl in text, "Target concl not found"
    text = text.replace(target_concl, repl_concl, 1)

    return text


def main():
    paths = [Path("paper/main.tex"), Path("springer_manuscript/main.tex")]
    for path in paths:
        if path.exists():
            orig = path.read_text(encoding="utf-8")
            revised = revise_content(orig)
            path.write_text(revised, encoding="utf-8")
            print(f"Successfully applied revisions to {path}")


if __name__ == "__main__":
    main()
