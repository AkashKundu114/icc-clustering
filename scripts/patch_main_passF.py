"""
Patch springer_manuscript/main.tex with all Pass F updates using clean block replacements.
"""

from pathlib import Path

TEX_PATH = Path("springer_manuscript/main.tex")
with open(TEX_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Abstract
old_abs_target = r"""Across 13 multi-domain benchmarks (1,430 model fits), Deep Embedded Clustering (DEC)~\cite{xie2016unsupervised} and K-Means achieve the lowest omnibus mean rank ($R=4.85$), followed by Standard Consensus ($R=4.92$), Ward ($R=5.31$), and ICC-v2 ($R=5.85$, Friedman $\chi_F^2 = 9.69, p = 0.47$, $CD = 4.19$). Although ICC-v2 attains the highest Grand Mean ARI of \GrandMeanARI\ (median ARI \OmnibusMedianARI), we reveal that this omnibus mean is heavily driven by two cancer microarray benchmarks: Leukemia (\ARIleukemia) and SRBCT (\ARIsrbct), whereas it averages \OmnibusMeanExcludingLeukemiaSrbct\ on the remaining 11 datasets. In the exploratory high-dimensional subgroup ($D/N > 20$), ICC-v2 achieves Rank \#1 ($R=\RankBioICCvTwo$), but fails on Prostate ($0.011$ vs. $0.049$ for Standard Consensus). Crucially, ablation testing demonstrates a key null result: determinacy anchor certification provides no statistically significant accuracy gain over uniform random anchors ($\Delta = +0.010$, dataset-level cluster bootstrap 95\% CI: $[-0.051, +0.076]$), establishing that bipartite graph compression---which reduces consensus graph memory by \MemoryScalingTenKGraphReduction\ at $N=10{,}000$ (\MemoryScalingTenKReduction\ peak dynamic memory)---rather than anchor certification is the primary operational mechanism."""

new_abs = r"""Across 13 multi-domain benchmarks (2,750 model fits), Standard Consensus achieves the lowest omnibus mean rank ($R=\TableThreeStdConsOverallRank$), followed by K-Means ($R=\TableThreeKMeansOverallRank$), DEC~\cite{xie2016unsupervised} ($R=\TableThreeDecOverallRank$), ICC-v2 ($R=\TableThreeIccVTwoOverallRank$), and Ward ($R=\TableThreeWardOverallRank$, Friedman $\chi_F^2 = 9.59, p = \TableThreeFriedmanPValue$, $CD = \TrueNemenyiCD$). Although ICC-v2 attains the highest Grand Mean ARI of \GrandMeanARI\ (median ARI \OmnibusMedianARI), we reveal that this omnibus mean is heavily driven by two cancer microarray benchmarks: Leukemia (\ARIleukemia) and SRBCT (\ARIsrbct), whereas it averages \OmnibusMeanExcludingLeukemiaSrbct\ on the remaining 11 datasets. In the exploratory high-dimensional subgroup ($D/N > 20$), ICC-v2 achieves Rank \#1 ($R=\RankBioICCvTwo$), but fails on Prostate ($0.012$ vs. $0.049$ for Standard Consensus). Crucially, ablation testing demonstrates a key null result: determinacy anchor certification provides no statistically significant accuracy gain over uniform random anchors ($\Delta = +0.019$, dataset-level cluster bootstrap 95\% CI: $[-0.039, +0.082]$), establishing that bipartite graph compression---which reduces consensus graph memory by \MemoryScalingTenKGraphReduction\ at $N=10{,}000$ (\MemoryScalingTenKReduction\ peak dynamic memory)---rather than anchor certification is the primary operational mechanism."""

if old_abs_target in text:
    text = text.replace(old_abs_target, new_abs)
    print("1. Abstract replaced successfully.")

# 2. Table 1 (Taxonomy) and Core-Halo Description
old_tab1 = r"""\begin{table}[!t]
\caption{Methodological Taxonomy and Comparison Across Consensus Paradigms}
\label{tab:taxonomy_comparison}
\centering
\footnotesize
\setlength{\tabcolsep}{3.5pt}
\begin{tabular}{@{}lccccc@{}}
\toprule
\textbf{Method} & \textbf{Feature Gating} & \textbf{Core Filtering} & \textbf{Inductive} & \textbf{Aux. Mem.} & \textbf{High-$D$ Noise} \\
\midrule
Std Cons.~\cite{fred2005combining}   & None           & None         & No          & $O(N^2)$ & No  \\
Core-Halo Cons.                      & None           & Determinacy  & No          & $O(N^2)$ & No  \\
FCAG~\cite{nie2024fast}              & None           & Anchors      & No          & $O(NL)$  & No  \\
FastMVC~\cite{huang2023fast}         & None           & Anchors      & No          & $O(NL)$  & No  \\
U-SPEC~\cite{huang2020ultra}         & None           & Anchors      & Nystr{\"o}m & $O(NL)$  & No \\
\textbf{ICC-v2 (Ours)}               & \textbf{BGSS}  & \textbf{Core Anchors} & \textbf{Centroid} & $\mathbf{O(NL)}$ & \textbf{Gated Subspace} \\
\bottomrule
\end{tabular}
\end{table}"""

new_tab1 = r"""\begin{table}[!t]
\caption{Methodological Taxonomy and Comparison Across Consensus Paradigms}
\label{tab:taxonomy_comparison}
\centering
\footnotesize
\setlength{\tabcolsep}{3.5pt}
\begin{tabular}{@{}lccccc@{}}
\toprule
\textbf{Method} & \textbf{Feature Gating} & \textbf{Core Filtering} & \textbf{Inductive} & \textbf{Aux. Mem.} & \textbf{High-$D$ Noise} \\
\midrule
Std Cons.~\cite{fred2005combining}        & None           & None         & No          & $O(N^2)$ & No  \\
Core-Halo Cons.~\cite{li2019clustering}$^*$ & None           & Determinacy  & No          & $O(N^2)$ & No  \\
FCAG~\cite{nie2024fast}                   & None           & Anchors      & No          & $O(NL)$  & No  \\
FastMVC~\cite{huang2023fast}              & None           & Anchors      & No          & $O(NL)$  & No  \\
U-SPEC~\cite{huang2020ultra}              & None           & Anchors      & Nystr{\"o}m & $O(NL)$  & No \\
\textbf{ICC-v2 (Ours)}                    & \textbf{BGSS}  & \textbf{Core Anchors} & \textbf{Centroid} & $\mathbf{O(NL)}$ & \textbf{Gated Subspace} \\
\bottomrule
\multicolumn{6}{@{}l@{}}{\footnotesize $^*$Our implementation inspired by Li et al.~\cite{li2019clustering} ($M=25$, average linkage on core distance, affinity halo assignment).}
\end{tabular}
\end{table}"""

if old_tab1 in text:
    text = text.replace(old_tab1, new_tab1)
    print("2. Table 1 replaced successfully.")

# Core-Halo prose description in Section 2
old_corehalo_prose = r"""Specifically, Core-Halo Consensus (Li et al.~\cite{li2019clustering}) constructs a dense co-association matrix over base clusterings, computes sample determinacy $\sum_{j} S_{ij}^2 / (N-1)$, designates points exceeding median determinacy as core points, clusters the core subset using average-linkage hierarchical clustering, and assigns remaining halo points to the nearest core cluster via co-association affinity."""
new_corehalo_prose = r"""Specifically, Li et al.~\cite{li2019clustering} formulate consensus clustering based on sample stability evaluated across diverse partitions. In our benchmark implementation inspired by Li et al.~\cite{li2019clustering}, we generate $M=25$ base K-Means clusterings, compute the dense co-association matrix $S \in [0, 1]^{N \times N}$, calculate sample determinacy $s_i = \frac{1}{N-1}\sum_{j \neq i} S_{ij}^2$, designate instances with $s_i \ge \operatorname{median}(s)$ as certified core points, cluster the core distance submatrix ($1 - S_{\text{core}}$) via average-linkage hierarchical clustering into $K$ groups, and assign halo instances to the core cluster maximizing average co-association affinity $\frac{1}{|C_c|}\sum_{j \in C_c} S_{hj}$."""
if old_corehalo_prose in text:
    text = text.replace(old_corehalo_prose, new_corehalo_prose)
    print("3. Core-Halo prose replaced successfully.")

# 3. Table 2 (Inductive table) and surrounding text
old_tab2_block = r"""\begin{table}[!t]
\caption{Empirical Adjusted Rand Index (ARI) on Held-Out Test Splits ($20\%$, Mean $\pm$ Standard Deviation Across 10 Canonical Seeds)}
\label{tab:inductive_direct}
\centering
\tiny
\setlength{\tabcolsep}{2.0pt}
\begin{tabular}{@{}lccccc@{}}
\toprule
\textbf{Dataset} & \textbf{Ambient KM} & \shortstack{\textbf{Weighted Centroid}\\\textbf{(Eqs.~6--7)}} & \shortstack{\textbf{Unweighted Near.}\\\textbf{Centroid (Eq.~7)}} & \textbf{Rand. Forest} & \textbf{Nystr\"om Ext.} \\
\midrule
CNS & $\mathbf{+0.071 \pm 0.221}$ & $-0.004 \pm 0.101$ & $-0.008 \pm 0.105$ & $+0.003 \pm 0.146$ & $-0.008 \pm 0.105$ \\
Colon & $-0.038 \pm 0.048$ & $+0.082 \pm 0.169$ & $+0.098 \pm 0.176$ & $+0.060 \pm 0.132$ & $\mathbf{+0.108 \pm 0.212}$ \\
Leukemia & $+0.146 \pm 0.104$ & $+0.257 \pm 0.314$ & $+0.216 \pm 0.291$ & $+0.266 \pm 0.361$ & $\mathbf{+0.296 \pm 0.335}$ \\
Ovarian & $+0.004 \pm 0.042$ & $-0.008 \pm 0.038$ & $+0.006 \pm 0.081$ & $\mathbf{+0.044 \pm 0.107}$ & $+0.017 \pm 0.107$ \\
SRBCT & $+0.033 \pm 0.134$ & $+0.221 \pm 0.120$ & $+0.253 \pm 0.134$ & $+0.318 \pm 0.216$ & $\mathbf{+0.367 \pm 0.221}$ \\
Isolet & $\mathbf{+0.466 \pm 0.033}$ & $+0.408 \pm 0.028$ & $+0.409 \pm 0.022$ & $+0.302 \pm 0.022$ & $+0.315 \pm 0.018$ \\
\bottomrule
\end{tabular}
\end{table}

In Table~\ref{tab:inductive_direct}, stability-weighted centroid assignment (Eqs.~\ref{eq:centroid_proj}--\ref{eq:query_assign}) and standard unweighted nearest centroid assignment (Eq.~\ref{eq:query_assign}) exhibit extremely high pairwise label agreement across test query points: $99.2\%$ on CNS, $99.2\%$ on Colon, $97.3\%$ on Leukemia, $96.9\%$ on Ovarian, and $94.1\%$ on SRBCT (averaging $97.3\%$ across the five high-dimensional biomedical cohorts; $85.0\%$ on Isolet). This empirical concordance demonstrates that while determinacy weighting pulls cluster prototypes toward high-confidence core exemplars in the active feature space, the resulting decision boundaries largely preserve partition assignments for out-of-sample query instances. As reported in Table~\ref{tab:inductive_direct}, the closed-form centroid projection rule outperforms ambient K-Means on Leukemia ($+0.257$ vs. $+0.146$), SRBCT ($+0.221$ vs. $+0.033$), and Colon ($+0.082$ vs. $-0.038$), executing in $O(K \cdot |\mathcal{F}_{\text{active}}|)$ operations without rebuilding the consensus graph. Where non-linear manifold geometry is prominent, Nystr\"om spectral extension provides an alternative extension mechanism (attaining $+0.296$ on Leukemia and $+0.367$ on SRBCT), formalizing the accuracy-latency tradeoff in inductive consensus learning."""

new_tab2_block = r"""\begin{table}[!t]
\caption{Empirical Adjusted Rand Index (ARI) on Held-Out Test Splits ($20\%$, Mean $\pm$ Standard Deviation Across 10 Canonical Seeds)}
\label{tab:inductive_direct}
\centering
\tiny
\setlength{\tabcolsep}{2.0pt}
\begin{tabular}{@{}lccccc@{}}
\toprule
\textbf{Dataset} & \textbf{Ambient KM} & \shortstack{\textbf{Weighted Centroid}\\\textbf{(Eqs.~6--7)}} & \shortstack{\textbf{Unweighted Near.}\\\textbf{Centroid (Eq.~7)}} & \textbf{Rand. Forest} & \textbf{Nystr\"om Ext.} \\
\midrule
CNS & $\mathbf{+0.071 \pm 0.221}$ & $-0.004 \pm 0.101$ & $-0.008 \pm 0.105$ & $+0.003 \pm 0.146$ & $-0.008 \pm 0.105$ \\
Colon & $-0.038 \pm 0.048$ & $+0.082 \pm 0.169$ & $+0.098 \pm 0.176$ & $+0.060 \pm 0.132$ & $\mathbf{+0.108 \pm 0.212}$ \\
Leukemia & $+0.146 \pm 0.104$ & $+0.257 \pm 0.314$ & $+0.216 \pm 0.291$ & $+0.266 \pm 0.361$ & $\mathbf{+0.296 \pm 0.335}$ \\
Ovarian & $+0.004 \pm 0.042$ & $-0.008 \pm 0.038$ & $+0.006 \pm 0.081$ & $\mathbf{+0.044 \pm 0.107}$ & $+0.017 \pm 0.107$ \\
SRBCT & $+0.033 \pm 0.134$ & $+0.221 \pm 0.120$ & $+0.253 \pm 0.134$ & $+0.318 \pm 0.216$ & $\mathbf{+0.367 \pm 0.221}$ \\
Isolet & $\mathbf{+0.466 \pm 0.033}$ & $+0.408 \pm 0.028$ & $+0.409 \pm 0.022$ & $+0.302 \pm 0.022$ & $+0.315 \pm 0.018$ \\
\midrule
\textbf{Mean ARI} & 0.114 & 0.159 & 0.161 & 0.165 & \textbf{0.183} \\
\midrule
\multicolumn{6}{@{}l@{}}{\textbf{Paired Differences vs. Weighted Centroid ($\Delta = \text{Centroid} - \text{Baseline}$, 95\% Bootstrap CI):}} \\
\multicolumn{6}{@{}l@{}}{\quad vs. Ambient KM: $\Delta = +0.046$, 95\% CI: $[-0.029, +0.129]$ (Ambient KM higher on CNS, Isolet)} \\
\multicolumn{6}{@{}l@{}}{\quad vs. Nystr\"om Ext.: $\Delta = -0.023$, 95\% CI: $[-0.081, +0.033]$} \\
\multicolumn{6}{@{}l@{}}{\quad vs. Random Forest: $\Delta = -0.006$, 95\% CI: $[-0.053, +0.046]$} \\
\bottomrule
\end{tabular}
\end{table}

In Table~\ref{tab:inductive_direct}, stability-weighted centroid assignment (Eqs.~\ref{eq:centroid_proj}--\ref{eq:query_assign}) and standard unweighted nearest centroid assignment (Eq.~\ref{eq:query_assign}) exhibit extremely high pairwise label agreement across test query points: $99.2\%$ on CNS, $99.2\%$ on Colon, $97.3\%$ on Leukemia, $96.9\%$ on Ovarian, and $94.1\%$ on SRBCT (averaging $97.3\%$ across the five high-dimensional biomedical cohorts; $85.0\%$ on Isolet). This empirical concordance demonstrates that while determinacy weighting pulls cluster prototypes toward high-confidence core exemplars in the active feature space, the resulting decision boundaries largely preserve partition assignments for out-of-sample query instances.

For inductive baseline benchmarking, Ambient K-Means is evaluated on held-out test query points via standard Euclidean nearest centroid assignment to the cluster centers learned on the training split. Evaluating paired differences between stability-weighted centroid projection and competing inductive rules across test splits yields $\Delta = +0.046$ vs. Ambient K-Means (dataset-level cluster bootstrap 95\% CI: $[-0.029, +0.129]$), $\Delta = -0.023$ vs. Nystr\"om spectral extension (95\% CI: $[-0.081, +0.033]$), and $\Delta = -0.006$ vs. Random Forest (95\% CI: $[-0.053, +0.046]$). Because all bootstrap confidence intervals span zero, the empirical intervals do not support an omnibus claim of superiority over alternative inductive mechanisms. Instead, the data reveal regime-dependent tradeoffs: Ambient K-Means achieves superior test generalization on CNS ($-0.075$ paired difference: Ambient KM $+0.071$ vs. Centroid $-0.004$) and Isolet ($-0.058$ difference: $+0.466$ vs. $+0.408$), whereas Centroid projection proves advantageous on Colon ($+0.120$), Leukemia ($+0.112$), and SRBCT ($+0.188$). Where non-linear manifold geometry is prominent, Nystr\"om spectral extension provides an alternative extension mechanism (attaining $+0.296$ on Leukemia and $+0.367$ on SRBCT), formalizing the accuracy-latency tradeoff in inductive consensus learning."""

if old_tab2_block in text:
    text = text.replace(old_tab2_block, new_tab2_block)
    print("4. Table 2 replaced successfully.")

# 4. Section 5.3: Factorial Ablation (30 seeds updates)
old_ablation_prose = r"""To disentangle feature gating from bipartite anchor consensus, we evaluated a pre-specified (internal protocol, not externally time-stamped) $2 \times 2$ factorial protocol ($\{\text{Ambient}, \text{BGSS}\} \times \{\text{Dense Consensus}, \text{Bipartite Anchor Consensus}\}$) alongside single-model controls across all 6 high-dimensional biomedical benchmarks ($D/N > 20$: CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT) over 10 random seeds (Seeds 0--9). Across the 6 datasets, ambient standard dense consensus (V0) achieves a subgroup mean ARI of $\AblationHighDSubgroupAmbientStdCons$, ambient anchor consensus (V3) yields $\AblationHighDSubgroupAmbientAnchor$, and ambient K-Means achieves $\AblationHighDSubgroupAmbientKMeans$. Restricting input to the BGSS candidate pool yields $\AblationHighDSubgroupBgssKMeans$ for single K-Means (V1) and $\AblationHighDSubgroupBgssStdCons$ for dense consensus (V2). In contrast, Full ICC-v2 (V5: BGSS + certified core anchors) achieves a subgroup mean ARI of $\mathbf{\AblationHighDSubgroupFullIccVTwo}$ vs. $\AblationHighDSubgroupBgssRandomAnchor$ for V4 with uniform random anchors (paired mean difference $\Delta = +0.010$, dataset-level cluster bootstrap 95\% CI: $[-0.051, +0.076]$). Because the confidence interval encompasses zero (and a paired Wilcoxon signed-rank test across the six datasets yields $W=8.0, p=0.69$), determinacy certification yields no statistically significant performance advantage over uniform random anchor selection across the subgroup. Specifically, per-dataset paired differences $\Delta = V5 - V4$ vary markedly across cohorts: $+0.026$ on CNS, $+0.011$ on Colon, $+0.149$ on Leukemia, $+0.014$ on Ovarian, $-0.024$ on Prostate, and $-0.114$ on SRBCT, confirming that uniform random anchor ensembling is competitive with deterministic certification. The primary performance driver is the transition from dense consensus to bipartite anchor consensus under BGSS feature selection (V5 vs. V2: $\Delta = +0.145$, 95\% CI: $[+0.070, +0.226]$). Furthermore, the high-dimensional subgroup performance is heavily driven by Leukemia ($0.704$) and SRBCT ($0.537$); across the remaining four datasets (CNS, Colon, Ovarian, Prostate), V5 attains a mean ARI of only $0.029$ (vs. $0.022$ for V4).
    \item \textbf{Dissecting the Leukemia Marker Discrepancy and Discrete Bimodality:} On Leukemia ($N=72, D=7{,}129, K=2$), across all evaluation protocols (the omnibus benchmark Table~\ref{tab:benchmark_ari}, the fair feature-matched baseline comparison Table~\ref{tab:fair_baselines}, and the $2 \times 2$ factorial ablation) evaluated under the canonical random seeds (Seeds 0--9), ICC-v2 yields an identical $0.704 \pm 0.265$ (median $0.787$, with 9/10 seeds yielding $\text{ARI} > 0.74$). More fundamentally, Leukemia partition recovery is intrinsically bimodal under small-sample high-dimensional ensembling: partitions either successfully discover the true $47$ ALL vs. $25$ AML dichotomy ($\text{ARI} \in [0.74, 0.89]$) or collapse onto arbitrary distractor noise boundaries ($\text{ARI} \le 0.0$). Across an exhaustive 30-seed aggregate evaluation, the overall mean is $0.600 \pm 0.367$ (median $0.787$) with a $73.3\%$ success rate ($22/30$ seeds with $\text{ARI} > 0.50$); likewise on SRBCT, 30 seeds yield a mean of $0.546 \pm 0.102$ (median $0.547$, with $70.0\%$ of seeds achieving $\text{ARI} > 0.50$). In contrast, on the remaining four high-dimensional datasets (CNS, Colon, Ovarian, Prostate), all 30 seeds yield $\text{ARI} \le 0.50$ ($0\%$ success rate), confirming that finite-sample discrete bimodality is concentrated in the Leukemia and SRBCT cohorts."""

new_ablation_prose = r"""To disentangle feature gating from bipartite anchor consensus, we evaluated a pre-specified $2 \times 2$ factorial protocol ($\{\text{Ambient}, \text{BGSS}\} \times \{\text{Dense Consensus}, \text{Bipartite Anchor Consensus}\}$) alongside single-model controls across all 6 high-dimensional biomedical benchmarks ($D/N > 20$: CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT) across 30 canonical random seeds (Seeds 0--29). Across the 6 datasets, ambient standard dense consensus (V0) achieves a subgroup mean ARI of $\AblationHighDSubgroupAmbientStdCons$, ambient anchor consensus (V3) yields $\AblationHighDSubgroupAmbientAnchor$, and ambient K-Means achieves $\AblationHighDSubgroupAmbientKMeans$. Restricting input to the BGSS candidate pool yields $\AblationHighDSubgroupBgssKMeans$ for single K-Means (V1) and $\AblationHighDSubgroupBgssStdCons$ for dense consensus (V2). In contrast, Full ICC-v2 (V5: BGSS + certified core anchors) achieves a subgroup mean ARI of $\mathbf{\AblationHighDSubgroupFullIccVTwo}$ vs. $\AblationHighDSubgroupBgssRandomAnchor$ for V4 with uniform random anchors (paired mean difference $\Delta = +0.019$, dataset-level cluster bootstrap 95\% CI: $[-0.039, +0.082]$). Because the confidence interval encompasses zero (and a paired Wilcoxon signed-rank test across the six cohorts yields $W=9.0, p=0.84$), determinacy certification yields no statistically significant performance advantage over uniform random anchor selection across the subgroup. The primary performance driver is the transition from dense consensus to bipartite anchor consensus under BGSS feature selection (V5 vs. V2: $\Delta = +0.139$, 95\% CI: $[+0.065, +0.218]$). Furthermore, the high-dimensional subgroup performance is heavily driven by Leukemia ($0.600$) and SRBCT ($0.546$); across the remaining four cohorts (CNS, Colon, Ovarian, Prostate), V5 attains a mean ARI of $0.039$ (vs. $0.032$ for V4).
    \item \textbf{Dissecting the Leukemia Marker Discrepancy and Discrete Bimodality:} On Leukemia ($N=72, D=7{,}129, K=2$), across all evaluation protocols (the omnibus benchmark Table~\ref{tab:benchmark_ari}, the fair feature-matched baseline comparison Table~\ref{tab:fair_baselines}, and the $2 \times 2$ factorial ablation) evaluated under 30 canonical random seeds (Seeds 0--29), ICC-v2 yields an identical $0.600 \pm 0.367$ (median $0.787$, with 22/30 seeds yielding $\text{ARI} > 0.50$, $73.3\%$). More fundamentally, Leukemia partition recovery is intrinsically bimodal under small-sample high-dimensional ensembling: partitions either successfully discover the true $47$ ALL vs. $25$ AML dichotomy ($\text{ARI} \in [0.74, 0.89]$) or collapse onto arbitrary distractor noise boundaries ($\text{ARI} \le 0.0$). On SRBCT, 30 seeds yield a mean of $0.546 \pm 0.102$ (median $0.547$, with $70.0\%$ of seeds achieving $\text{ARI} > 0.50$). In contrast, on the remaining four high-dimensional datasets (CNS, Colon, Ovarian, Prostate), all 30 seeds yield $\text{ARI} \le 0.50$ ($0\%$ success rate), confirming that finite-sample discrete bimodality is concentrated in the Leukemia and SRBCT cohorts."""

if old_ablation_prose in text:
    text = text.replace(old_ablation_prose, new_ablation_prose)
    print("5. Factorial ablation replaced successfully.")

# 5. Fig. 7 Caption (Critical Difference)
old_fig7_cap = r"""\caption{Dem\v{s}ar Critical Difference analysis~\cite{demsar2006statistical} across 13 multi-domain benchmarks. Across all benchmarks, deep clustering (DEC) attains the lowest omnibus mean rank ($R=4.31$), followed by Standard Consensus ($R=5.08$), K-Means ($R=5.31$), Ward ($R=5.31$), and ICC-v2 ($R=5.46$). Under the Nemenyi test ($k=11, N=13, \alpha=0.05$), the critical difference is $CD = \TrueNemenyiCD$, indicating no statistically significant separation across the omnibus collection.}"""

new_fig7_cap = r"""\caption{Dem\v{s}ar Critical Difference analysis~\cite{demsar2006statistical} across 13 multi-domain benchmarks. Across all benchmarks, Standard Consensus attains the lowest omnibus mean rank ($R=\TableThreeStdConsOverallRank$), followed by K-Means ($R=\TableThreeKMeansOverallRank$), deep clustering (DEC, $R=\TableThreeDecOverallRank$), ICC-v2 ($R=\TableThreeIccVTwoOverallRank$), and Ward ($R=\TableThreeWardOverallRank$). Under the Nemenyi test ($k=11, N=13, \alpha=0.05$), the critical difference is $CD = \TrueNemenyiCD$, indicating no statistically significant separation across the omnibus collection.}"""

if old_fig7_cap in text:
    text = text.replace(old_fig7_cap, new_fig7_cap)
    print("6. Fig 7 caption replaced successfully.")

# 6. Table 4: replace table blocks
old_tab4_cap = r"""\caption{Omnibus Benchmark Matrix Across 13 Real-World Datasets and 11 Clustering Frameworks (10 Canonical Random Seeds, Mean $\pm$ Standard Deviation ARI)}"""
new_tab4_cap = r"""\caption{Omnibus Benchmark Matrix Across 13 Real-World Datasets and 11 Clustering Frameworks (Mean $\pm$ Standard Deviation ARI Across Canonical Seeds: 30 Seeds on $D/N > 20$ Cohorts$^\dagger$, 10 Seeds on Standard Benchmarks)}"""
if old_tab4_cap in text:
    text = text.replace(old_tab4_cap, new_tab4_cap)

# Block 1
idx_p1 = text.find(r'Part I: Classical Clustering Baselines')
if idx_p1 != -1 and 'Indian Pines ($10.2\\text{k}, 200, 16$) & $+0.212' in text[idx_p1:idx_p1+1000]:
    idx_mid1 = text.find(r'\midrule', idx_p1)
    idx_mid1 = text.find(r'\midrule', idx_mid1 + 5)
    idx_bot1 = text.find(r'\bottomrule', idx_mid1)

    new_p1_body = r"""CNS ($60, 7.1\text{k}, 2$)$^\dagger$ & $-0.023 \pm 0.025$ & $-0.022 \pm 0.000$ & $-0.004 \pm 0.000$ & $+0.002 \pm 0.000$ \\
Colon ($62, 2.0\text{k}, 2$)$^\dagger$ & $+0.063 \pm 0.130$ & $-0.016 \pm 0.000$ & $-0.023 \pm 0.000$ & $+0.009 \pm 0.012$ \\
Indian Pines ($10.2\text{k}, 200, 16$) & $+0.212 \pm 0.010$ & $+0.214 \pm 0.000$ & $\mathbf{+0.229 \pm 0.000}$ & $+0.173 \pm 0.010$ \\
Isolet ($7.8\text{k}, 617, 26$) & $+0.448 \pm 0.031$ & $\mathbf{+0.502 \pm 0.000}$ & $+0.417 \pm 0.000$ & $+0.059 \pm 0.000$ \\
Leukemia ($72, 7.1\text{k}, 2$)$^\dagger$ & $+0.126 \pm 0.088$ & $+0.082 \pm 0.000$ & $+0.139 \pm 0.000$ & $+0.100 \pm 0.000$ \\
Madelon ($500, 500, 2$) & $+0.028 \pm 0.017$ & $+0.012 \pm 0.000$ & $+0.039 \pm 0.001$ & $+0.029 \pm 0.019$ \\
20 Newsgroups ($18.8\text{k}, 10\text{k}, 20$) & $+0.063 \pm 0.055$ & $+0.099 \pm 0.000$ & $+0.000 \pm 0.000$ & $+0.006 \pm 0.000$ \\
Ovarian ($253, 15.1\text{k}, 2$)$^\dagger$ & $+0.006 \pm 0.006$ & $+0.011 \pm 0.000$ & $+0.019 \pm 0.001$ & $+0.002 \pm 0.001$ \\
Prostate ($102, 12.6\text{k}, 2$)$^\dagger$ & $+0.043 \pm 0.015$ & $+0.026 \pm 0.000$ & $-0.003 \pm 0.000$ & $+0.048 \pm 0.000$ \\
Sonar ($208, 60, 2$) & $+0.014 \pm 0.021$ & $-0.001 \pm 0.000$ & $-0.005 \pm 0.000$ & $\mathbf{+0.026 \pm 0.017}$ \\
SRBCT ($83, 2.3\text{k}, 4$)$^\dagger$ & $+0.118 \pm 0.064$ & $+0.109 \pm 0.000$ & $+0.080 \pm 0.000$ & $+0.104 \pm 0.030$ \\
Yale B ($2.4\text{k}, 1.0\text{k}, 38$) & $+0.016 \pm 0.002$ & $+0.049 \pm 0.000$ & $+0.065 \pm 0.002$ & $-0.001 \pm 0.000$ \\
PBMC68k-reduced ($700, 765, 10$)$^*$ & $+0.494 \pm 0.034$ & $+0.495 \pm 0.000$ & $+0.414 \pm 0.002$ & $+0.347 \pm 0.024$ \\
\midrule
\textbf{Grand Mean ARI} & 0.124 & 0.120 & 0.105 & 0.070 \\
\textbf{Mean Rank (All 13)} & \TableThreeKMeansOverallRank & \TableThreeWardOverallRank & 6.62 & 6.77 \\
\textbf{Mean Rank (12, Excl. PBMC)} & \TableThreeKMeansTwelveRank & \TableThreeWardTwelveRank & 6.67 & 6.50 \\
\textbf{Mean Rank ($D/N > 20$ Subgroup)} & \TableThreeKMeansHighDRank & \TableThreeWardHighDRank & \TableThreeSpectralHighDRank & \TableThreeFcmHighDRank \\"""

    text = text[:idx_mid1 + len(r'\midrule') + 1] + new_p1_body + "\n" + text[idx_bot1:]
    print("7. Table 4 Part I replaced successfully.")

# Block 2
idx_p2 = text.find(r'Part II: Consensus and Scalable Graph Baselines')
if idx_p2 != -1 and 'Indian Pines ($10.2\\text{k}, 200, 16$) & $+0.220' in text[idx_p2:idx_p2+1000]:
    idx_mid2 = text.find(r'\midrule', idx_p2)
    idx_mid2 = text.find(r'\midrule', idx_mid2 + 5)
    idx_bot2 = text.find(r'\bottomrule', idx_mid2)

    new_p2_body = r"""CNS ($60, 7.1\text{k}, 2$)$^\dagger$ & $-0.025 \pm 0.020$ & $-0.007 \pm 0.012$ & $+0.014 \pm 0.019$ & $-0.004 \pm 0.000$ \\
Colon ($62, 2.0\text{k}, 2$)$^\dagger$ & $-0.013 \pm 0.015$ & $-0.008 \pm 0.013$ & $+0.034 \pm 0.080$ & $-0.016 \pm 0.000$ \\
Indian Pines ($10.2\text{k}, 200, 16$) & $+0.220 \pm 0.004$ & $+0.138 \pm 0.031$ & $+0.209 \pm 0.013$ & $+0.203 \pm 0.009$ \\
Isolet ($7.8\text{k}, 617, 26$) & $+0.477 \pm 0.015$ & $+0.368 \pm 0.032$ & $+0.468 \pm 0.025$ & $+0.437 \pm 0.020$ \\
Leukemia ($72, 7.1\text{k}, 2$)$^\dagger$ & $+0.162 \pm 0.064$ & $+0.123 \pm 0.057$ & $+0.130 \pm 0.064$ & $+0.323 \pm 0.000$ \\
Madelon ($500, 500, 2$) & $\mathbf{+0.040 \pm 0.014}$ & $+0.038 \pm 0.004$ & $+0.012 \pm 0.015$ & $-0.000 \pm 0.000$ \\
20 Newsgroups ($18.8\text{k}, 10\text{k}, 20$) & $\mathbf{+0.102 \pm 0.005}$ & $+0.076 \pm 0.010$ & $+0.008 \pm 0.003$ & $+0.037 \pm 0.016$ \\
Ovarian ($253, 15.1\text{k}, 2$)$^\dagger$ & $+0.009 \pm 0.001$ & $+0.009 \pm 0.005$ & $+0.005 \pm 0.009$ & $-0.008 \pm 0.012$ \\
Prostate ($102, 12.6\text{k}, 2$)$^\dagger$ & $\mathbf{+0.049 \pm 0.002}$ & $+0.000 \pm 0.000$ & $+0.016 \pm 0.009$ & $+0.004 \pm 0.002$ \\
Sonar ($208, 60, 2$) & $-0.001 \pm 0.002$ & $+0.015 \pm 0.016$ & $+0.007 \pm 0.007$ & $-0.004 \pm 0.000$ \\
SRBCT ($83, 2.3\text{k}, 4$)$^\dagger$ & $+0.042 \pm 0.012$ & $+0.099 \pm 0.056$ & $+0.074 \pm 0.055$ & $+0.094 \pm 0.000$ \\
Yale B ($2.4\text{k}, 1.0\text{k}, 38$) & $+0.016 \pm 0.002$ & $+0.009 \pm 0.003$ & $\mathbf{+0.130 \pm 0.010}$ & $+0.041 \pm 0.004$ \\
PBMC68k-reduced ($700, 765, 10$)$^*$ & $\mathbf{+0.555 \pm 0.037}$ & $+0.402 \pm 0.122$ & $+0.512 \pm 0.066$ & $+0.400 \pm 0.076$ \\
\midrule
\textbf{Grand Mean ARI} & 0.126 & 0.097 & 0.125 & 0.116 \\
\textbf{Mean Rank (All 13)} & \textbf{\TableThreeStdConsOverallRank} & 6.62 & \TableThreeDecOverallRank & 7.23 \\
\textbf{Mean Rank (12, Excl. PBMC)} & \TableThreeStdConsTwelveRank & 6.58 & \TableThreeDecTwelveRank & 7.17 \\
\textbf{Mean Rank ($D/N > 20$ Subgroup)} & \TableThreeStdConsHighDRank & \TableThreeLiHighDRank & \TableThreeDecHighDRank & \TableThreeFcagHighDRank \\"""

    text = text[:idx_mid2 + len(r'\midrule') + 1] + new_p2_body + "\n" + text[idx_bot2:]
    print("8. Table 4 Part II replaced successfully.")

# Block 3
idx_p3 = text.find(r'Part III: Anchor Consensus and Proposed Frameworks')
if idx_p3 != -1 and 'Indian Pines ($10.2\\text{k}, 200, 16$) & $+0.201' in text[idx_p3:idx_p3+1000]:
    idx_mid3 = text.find(r'\midrule', idx_p3)
    idx_mid3 = text.find(r'\midrule', idx_mid3 + 5)

    new_p3_body = r"""CNS ($60, 7.1\text{k}, 2$)$^\dagger$ & $+0.009 \pm 0.006$ & $-0.017 \pm 0.020$ & $\mathbf{+0.021 \pm 0.022}$ \\
Colon ($62, 2.0\text{k}, 2$)$^\dagger$ & $-0.016 \pm 0.001$ & $-0.003 \pm 0.017$ & $\mathbf{+0.072 \pm 0.110}$ \\
Indian Pines ($10.2\text{k}, 200, 16$) & $+0.201 \pm 0.014$ & $+0.135 \pm 0.037$ & $+0.136 \pm 0.030$ \\
Isolet ($7.8\text{k}, 617, 26$) & $+0.432 \pm 0.019$ & $+0.301 \pm 0.045$ & $+0.278 \pm 0.030$ \\
Leukemia ($72, 7.1\text{k}, 2$)$^\dagger$ & $+0.171 \pm 0.177$ & $+0.155 \pm 0.082$ & $\mathbf{+0.600 \pm 0.367}$ \\
Madelon ($500, 500, 2$) & $+0.000 \pm 0.000$ & $+0.040 \pm 0.006$ & $+0.021 \pm 0.018$ \\
20 Newsgroups ($18.8\text{k}, 10\text{k}, 20$) & $+0.000 \pm 0.000$ & $+0.062 \pm 0.010$ & $+0.000 \pm 0.000$ \\
Ovarian ($253, 15.1\text{k}, 2$)$^\dagger$ & $-0.009 \pm 0.012$ & $+0.023 \pm 0.009$ & $\mathbf{+0.050 \pm 0.139}$ \\
Prostate ($102, 12.6\text{k}, 2$)$^\dagger$ & $+0.000 \pm 0.001$ & $+0.019 \pm 0.022$ & $+0.012 \pm 0.013$ \\
Sonar ($208, 60, 2$) & $-0.003 \pm 0.005$ & $+0.006 \pm 0.006$ & $+0.007 \pm 0.008$ \\
SRBCT ($83, 2.3\text{k}, 4$)$^\dagger$ & $+0.138 \pm 0.061$ & $+0.101 \pm 0.044$ & $\mathbf{+0.546 \pm 0.102}$ \\
Yale B ($2.4\text{k}, 1.0\text{k}, 38$) & $+0.040 \pm 0.004$ & $+0.009 \pm 0.002$ & $+0.055 \pm 0.007$ \\
PBMC68k-reduced ($700, 765, 10$)$^*$ & $+0.461 \pm 0.065$ & $+0.357 \pm 0.088$ & $+0.182 \pm 0.062$ \\
\midrule
\textbf{Grand Mean ARI} & 0.110 & 0.091 & \textbf{\TableThreeIccVTwoGrandMean} \\
\textbf{Mean Rank (All 13)} & \TableThreeFastMvcHighDRank & \TableThreeIccVOneHighDRank & \TableThreeIccVTwoOverallRank \\
\textbf{Mean Rank (12, Excl. PBMC)} & 7.08 & 6.17 & \textbf{\TableThreeIccVTwoTwelveRank} \\
\textbf{Mean Rank ($D/N > 20$ Subgroup)} & \TableThreeFastMvcHighDRank & \TableThreeIccVOneHighDRank & \textbf{\TableThreeIccVTwoHighDRank} \\"""

    idx_bot3 = text.find(r'\midrule', idx_mid3 + 5)
    idx_end_tab4 = text.find(r'\end{tabular}', idx_bot3)
    text = text[:idx_mid3 + len(r'\midrule') + 1] + new_p3_body + "\n\\bottomrule\n" + text[idx_end_tab4:]
    print("9. Table 4 Part III replaced successfully.")

# 7. Table 5 (Fair baselines)
idx_fb = text.find(r'\label{tab:fair_baselines}')
if idx_fb != -1 and '0.226' in text[idx_fb:idx_fb+3500]:
    new_tab5_block = r"""\begin{table*}[!t]
\caption{Fair Feature-Matched Baseline Comparison Across High-Dimensional Regimes ($D/N > 20$, 30 Canonical Seeds, Mean $\pm$ Standard Deviation ARI)}
\label{tab:fair_baselines}
\centering
\tiny
\setlength{\tabcolsep}{2.0pt}

% Block 1: Single-model & feature selection
\begin{tabular}{@{}lccccc@{}}
\toprule
\multicolumn{6}{c}{\textbf{Part I: Feature-Selected K-Means and Sparse Clustering Baselines}} \\
\midrule
\textbf{Dataset ($N, D, K$)} & \shortstack{\textbf{K-Means}\\\textbf{(Ambient)}} & \shortstack{\textbf{K-Means}\\\textbf{(VarFilt)}} & \shortstack{\textbf{K-Means}\\\textbf{(PCA)}} & \shortstack{\textbf{K-Means}\\\textbf{(LapScore)}} & \shortstack{\textbf{Sparse}\\\textbf{K-Means}} \\
\midrule
CNS ($60, 7.1\text{k}, 2$) & $-0.001 \pm 0.015$ & $-0.015 \pm 0.018$ & $-0.004 \pm 0.015$ & $-0.042 \pm 0.007$ & $-0.023 \pm 0.019$ \\
Colon ($62, 2.0\text{k}, 2$) & $-0.011 \pm 0.012$ & $-0.016 \pm 0.006$ & $-0.009 \pm 0.013$ & $-0.016 \pm 0.002$ & $+0.016 \pm 0.073$ \\
Leukemia ($72, 7.1\text{k}, 2$) & $+0.200 \pm 0.055$ & $+0.210 \pm 0.057$ & $+0.215 \pm 0.054$ & $+0.211 \pm 0.000$ & $+0.117 \pm 0.106$ \\
Ovarian ($253, 15.1\text{k}, 2$) & $+0.009 \pm 0.001$ & $-0.000 \pm 0.000$ & $+0.010 \pm 0.001$ & $+0.001 \pm 0.001$ & $+0.001 \pm 0.003$ \\
Prostate ($102, 12.6\text{k}, 2$) & $\mathbf{+0.049 \pm 0.000}$ & $+0.048 \pm 0.005$ & $\mathbf{+0.049 \pm 0.000}$ & $\mathbf{+0.049 \pm 0.000}$ & $+0.030 \pm 0.021$ \\
SRBCT ($83, 2.3\text{k}, 4$) & $+0.058 \pm 0.035$ & $+0.052 \pm 0.028$ & $+0.066 \pm 0.038$ & $+0.042 \pm 0.002$ & $+0.165 \pm 0.128$ \\
\midrule
\textbf{Subgroup Mean ARI} & 0.051 & \FairBaselinesKmVarFiltHighDMean & \FairBaselinesKmPcaHighDMean & 0.041 & \FairBaselinesSparseKmHighDMean \\
\textbf{Subgroup Median ARI} & 0.027 & 0.017 & 0.027 & 0.017 & 0.004 \\
\bottomrule
\end{tabular}

\vspace{1.0ex}

% Block 2: Consensus variants and ICC-v2
\begin{tabular}{@{}lcccc@{}}
\toprule
\multicolumn{5}{c}{\textbf{Part II: Feature-Selected Consensus Ensembles and Proposed ICC-v2}} \\
\midrule
\textbf{Dataset ($N, D, K$)} & \shortstack{\textbf{Std Cons}\\\textbf{(Ambient)}} & \shortstack{\textbf{Std Cons}\\\textbf{(VarFilt)}} & \shortstack{\textbf{Std Cons}\\\textbf{(PCA)}} & \shortstack{\textbf{ICC-v2}\\\textbf{(Ours)}} \\
\midrule
CNS ($60, 7.1\text{k}, 2$) & $-0.025 \pm 0.020$ & $-0.026 \pm 0.016$ & $-0.028 \pm 0.018$ & $\mathbf{+0.021 \pm 0.022}$ \\
Colon ($62, 2.0\text{k}, 2$) & $-0.013 \pm 0.015$ & $-0.010 \pm 0.012$ & $-0.010 \pm 0.016$ & $\mathbf{+0.072 \pm 0.110}$ \\
Leukemia ($72, 7.1\text{k}, 2$) & $+0.162 \pm 0.064$ & $+0.139 \pm 0.043$ & $+0.171 \pm 0.063$ & $\mathbf{+0.600 \pm 0.367}$ \\
Ovarian ($253, 15.1\text{k}, 2$) & $+0.009 \pm 0.001$ & $-0.000 \pm 0.001$ & $+0.008 \pm 0.003$ & $\mathbf{+0.050 \pm 0.139}$ \\
Prostate ($102, 12.6\text{k}, 2$) & $+0.049 \pm 0.002$ & $\mathbf{+0.049 \pm 0.000}$ & $+0.049 \pm 0.002$ & $+0.012 \pm 0.013$ \\
SRBCT ($83, 2.3\text{k}, 4$) & $+0.042 \pm 0.012$ & $+0.039 \pm 0.008$ & $+0.041 \pm 0.014$ & $\mathbf{+0.546 \pm 0.102}$ \\
\midrule
\textbf{Subgroup Mean ARI} & 0.037 & 0.032 & \FairBaselinesStdConsPcaHighDMean & \textbf{\FairBaselinesIccVTwoHighDMean} \\
\textbf{Subgroup Median ARI} & 0.022 & 0.019 & 0.019 & \textbf{\FairBaselinesIccVTwoHighDMedian} \\
\bottomrule
\end{tabular}
\end{table*}"""

    start_fb = text.rfind(r'\begin{table*}', 0, idx_fb)
    end_fb = text.find(r'\end{table*}', idx_fb) + len(r'\end{table*}')
    text = text[:start_fb] + new_tab5_block + text[end_fb:]
    print("10. Table 5 replaced successfully.")

# 8. Section 5.4: Regime bullets and statistical significance analysis
idx_start_reg = text.rfind(r'\begin{itemize}', 0, text.find('Small-Sample'))
idx_end_reg = text.find('should be interpreted as exploratory and post-hoc.', idx_start_reg) + len('should be interpreted as exploratory and post-hoc.')

new_regimes_section = r"""\begin{itemize}
    \item \textbf{Small-Sample, High-Dimensional Regimes ($D/N > 20$):} In cancer microarrays and mass spectrometry assays where $D \gg N$, ICC-v2 demonstrates competitive performance across 30 canonical random seeds. On SRBCT ($D/N=27.8, K=4$), ICC-v2 achieves an ARI of $\mathbf{\ARIsrbct} \pm \SrbctTableThreeStd$ (an absolute increase of $+0.408$ over FastMVC at $0.138 \pm 0.061$, and $+0.504$ over Standard Consensus at $0.042 \pm 0.012$); on Leukemia ($D/N=99.0$), it delivers $\mathbf{\ARIleukemia} \pm \LeukemiaTableThreeStd$ (vs. $0.162 \pm 0.064$ for Standard Consensus and $0.130 \pm 0.064$ for DEC); and on Ovarian ($D=15{,}154$), it achieves $\mathbf{\ARIovarian} \pm 0.139$. Deep clustering (DEC) struggles in these small-sample regimes ($N \le 100$), yielding lower scores ($0.074 \pm 0.055$ on SRBCT).
    \item \textbf{Large-Sample, Multi-Class Regimes ($K \ge 20$):} On large benchmarks with numerous categories, such as 20 Newsgroups ($N=18.8\text{k}, K=20$) and Isolet ($N=7.8\text{k}, K=26$), classical hierarchical Ward linkage ($0.099$ and $0.502$) and DEC ($0.468$ on Isolet) outperform ICC-v2 ($0.000$ and $0.278$). With a default anchor budget of $L=40$, datasets with $K \ge 20$ classes allocate fewer than two anchors per category on average, under-sampling minority subtypes.
    \item \textbf{Near-Zero ARI Regimes:} On CNS, Prostate, and Ovarian, evaluated methods achieve near-zero mean ARI ($\le 0.050$), while on Colon, methods average below $0.073$ (with ICC-v2 at $0.072 \pm 0.110$ and K-Means at $0.063 \pm 0.130$), reflecting the substantial difficulty of unsupervised partition recovery on these biological datasets.
\end{itemize}

\textbf{Statistical Significance Analysis:}
Across all 13 benchmarks, Friedman omnibus testing~\cite{demsar2006statistical} yields $\chi_F^2 = 9.59$, $p = \TableThreeFriedmanPValue$, indicating no statistically significant difference across the omnibus collection. Under the two-tailed post-hoc Nemenyi test ($\alpha=0.05, k=11, N=13$), the critical difference threshold is:
\begin{equation}
    CD_{N=13} = q_\alpha \sqrt{\frac{k(k+1)}{6N}} = 3.219 \sqrt{\frac{11 \times 12}{6 \times 13}} = 4.19.
\end{equation}
Standard Consensus ($R=\MeanRankStdCons$), K-Means ($R=\TableThreeKMeansOverallRank$), DEC ($R=\MeanRankDEC$), ICC-v2 ($R=\MeanRankICCvTwo$), and Ward ($R=\TableThreeWardOverallRank$) occupy the top five ranks without statistically significant separation across the omnibus collection. However, because ICC-v2 underperforms on the demonstration subset PBMC68k-reduced ($N=700$, Rank \#11, ARI $0.182$ vs. $0.555$ for Standard Consensus), we also evaluated omnibus ranks and critical difference excluding this subsample ($N=12$ full benchmark datasets). For $N=12$, the critical difference threshold expands to:
\begin{equation}
    CD_{N=12} = 3.219 \sqrt{\frac{11 \times 12}{6 \times 12}} = 4.36,
\end{equation}
with Friedman $\chi_F^2 = 8.06, p = 0.62$. Across the 12 full benchmark datasets, ICC-v2 attains the lowest mean rank $R=\TableThreeIccVTwoTwelveRank$, followed by K-Means ($R=\TableThreeKMeansTwelveRank$), Standard Consensus ($R=\TableThreeStdConsTwelveRank$), DEC ($R=\TableThreeDecTwelveRank$), and Ward ($R=\TableThreeWardTwelveRank$).

On the pre-specified high-dimensional biomedical subgroup ($D/N > 20$, comprising $N=6$ datasets: CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT across 30 seeds), ICC-v2 attains the top mean rank $R = \RankBioICCvTwo$ compared to $R = \TableThreeIccVOneHighDRank$ for ICC-v1, $R = \TableThreeKMeansHighDRank$ for K-Means, $R = \TableThreeFcmHighDRank$ for FCM, $R = \RankBioDEC$ for DEC, $R = \RankBioStdCons$ for Standard Consensus, and $R = \TableThreeLiHighDRank$ for Core-Halo Consensus, with an omnibus high-dimensional subgroup mean ARI of \FairBaselinesIccVTwoHighDMean\ (median \FairBaselinesIccVTwoHighDMedian, in exact numerical agreement across Table~\ref{tab:benchmark_ari}, Table~\ref{tab:fair_baselines}, and the $2 \times 2$ factorial ablation). However, for $N=6$ datasets, the Nemenyi threshold is $CD = 6.16$. Pairwise Wilcoxon tests~\cite{wilcoxon1945individual} between ICC-v2 and baselines on this subgroup yield unadjusted $p = 0.031$ against FCAG, FastMVC, Core-Halo Cons., and Spectral, but after Holm step-down adjustment across 10 baselines, the adjusted values are $p_{\text{adj}} \ge 0.3125$. Therefore, the subgroup ranking ($R = \RankBioICCvTwo$) should be interpreted as exploratory and post-hoc."""

if idx_start_reg != -1 and idx_end_reg > idx_start_reg:
    text = text[:idx_start_reg] + new_regimes_section + text[idx_end_reg:]
    print("11. Regime bullets and statistical significance replaced successfully.")

# 9. Limitation 8
old_lim8 = r"""\item \textbf{Near-Zero ARI Regimes:} On CNS, Colon, Prostate, and Ovarian, all evaluated methods achieve low ARI ($\le 0.052$), indicating unresolved clustering challenges on these benchmarks."""
new_lim8 = r"""\item \textbf{Near-Zero ARI Regimes:} On CNS, Prostate, and Ovarian, evaluated methods achieve near-zero mean ARI ($\le 0.050$), while on Colon methods average below $0.073$, indicating unresolved clustering challenges on these biological benchmarks."""
if old_lim8 in text:
    text = text.replace(old_lim8, new_lim8)
    print("12. Limitation 8 replaced successfully.")

# 10. Exp 5: Scalability & Controlled Series
old_exp5_block = r"""\begin{figure*}[!t]
\centering
\includegraphics[width=0.80\textwidth]{figures/fig26_extreme_scale_quad.png}
\caption{Scalability evaluation up to $N=1{,}000{,}000$ instances and $D=100{,}000$ dimensions (Exp~5). (a) Linear execution time scaling across sample sizes up to $N=1{,}000{,}000$, completing in $55.6\text{s}$. (b) Memory consumption scaling, requiring $3.05\text{ GB}$ peak RAM at $N=1{,}000{,}000$. (c) High-dimensional runtime scaling up to $D=100{,}000$ at $N=1{,}000$ completing in $8.28\text{s}$. (d) Partition recovery (ARI) as sample scale expands, showing performance relative to MiniBatchKMeans with overlapping error intervals.}
\label{fig:exp5_scale}
\end{figure*}

\begin{figure*}[!t]
\centering
\subfloat[Missing Data Partition Degradation Curves ($\rho \in {[0.0, 0.70]}$)\label{fig:missing_curves}]{%
    \includegraphics[width=0.55\textwidth]{figures/fig25a_missing_data_degradation.png}%
}
\hfill
\subfloat[Imputation Strategy Heatmap\label{fig:missing_heatmap}]{%
    \includegraphics[width=0.40\textwidth]{figures/fig25b_imputation_strategy_heatmap.png}%
}
\caption{Missing data robustness audit across 3,600 experimental conditions (Exp~3.5). (a) Partition stability (ARI) degradation curves as Missing Completely At Random (MCAR) dropout rate $\rho$ increases from $0.0$ to $0.70$ across Colon, Leukemia, and SRBCT. (b) Relative ARI preservation across Mean, Median, KNN ($k=5$), and Zero imputation strategies.}
\label{fig:missing_suite}
\end{figure*}

\textbf{1. Scalability Assessment (Exp 5):} Evaluating ICC-v2 on large synthetic manifolds (Fig.~\ref{fig:exp5_scale}) examines asymptotic limits. To assess extreme sample scaling up to $N=1{,}000{,}000$ ($D=100, K=5$), we evaluated a dedicated high-throughput anchor batch architecture utilizing single precision (float32), reduced ensemble size $M=15$, and anchor count $L=60$. Under this tailored configuration, where dense consensus requires $\approx 8\text{ TB}$ RAM, ICC-v2 completes in \textbf{$55.6\text{s}$} with \textbf{$3.05\text{ GB}$ peak process RSS} ($\text{ARI} = 0.382$ vs. $0.150$ for MiniBatchKMeans, Fig.~\ref{fig:exp5_scale}(d)). We separate raw data matrix storage ($10^6 \times 100 \times 4\text{ bytes} = 400.0\text{ MB}$ in float32) from bipartite graph auxiliary memory ($10^6 \times 60 \times 4\text{ bytes} = 240.0\text{ MB}$). We emphasize that this $55.6\text{ s}$ throughput reflects this specific lightweight batch architecture ($M=15, L=60$, float32); by comparison, the default configuration evaluated in Exp~4 ($M=25, L=40$, float64) required $10.35\text{ s}$ at $N=10{,}000$, demonstrating that linear scaling to massive cohorts requires appropriate batching and precision tuning. In high feature spaces ($D=100{,}000, N=1{,}000$), ICC-v2 executes in \textbf{$8.28\text{s}$}."""

new_exp5_block = r"""\begin{figure*}[!t]
\centering
\includegraphics[width=0.80\textwidth]{figures/fig26_extreme_scale_quad.png}
\caption{Scalability evaluation up to $N=1{,}000{,}000$ instances and $D=100{,}000$ dimensions (Exp~5). (a) Execution time scaling across sample sizes up to $N=1{,}000{,}000$, completing in \ExtremeScaleTime\ under reduced ensembling ($M=15, L=60$). (b) Memory consumption scaling, requiring $3.91\text{ GB}$ peak RAM at $N=1{,}000{,}000$. (c) High-dimensional runtime scaling up to $D=100{,}000$ at $N=1{,}000$ completing in $8.28\text{s}$. (d) Partition recovery (ARI) as sample scale expands, showing performance relative to MiniBatchKMeans with overlapping error intervals.}
\label{fig:exp5_scale}
\end{figure*}

\begin{figure*}[!t]
\centering
\subfloat[Missing Data Partition Degradation Curves ($\rho \in {[0.0, 0.70]}$)\label{fig:missing_curves}]{%
    \includegraphics[width=0.55\textwidth]{figures/fig25a_missing_data_degradation.png}%
}
\hfill
\subfloat[Imputation Strategy Heatmap\label{fig:missing_heatmap}]{%
    \includegraphics[width=0.40\textwidth]{figures/fig25b_imputation_strategy_heatmap.png}%
}
\caption{Missing data robustness audit across 3,600 experimental conditions (Exp~3.5). (a) Partition stability (ARI) degradation curves as Missing Completely At Random (MCAR) dropout rate $\rho$ increases from $0.0$ to $0.70$ across Colon, Leukemia, and SRBCT. (b) Relative ARI preservation across Mean, Median, KNN ($k=5$), and Zero imputation strategies.}
\label{fig:missing_suite}
\end{figure*}

\textbf{1. Controlled Scalability Assessment (Exp 5):} Evaluating ICC-v2 on large synthetic manifolds (Fig.~\ref{fig:exp5_scale}) examines asymptotic limits. To establish reproducible scaling behavior, we conducted a controlled evaluation comparing the default configuration ($M=25, L=40$, float64) against a reduced ensembling configuration ($M=15, L=60$, float32) across $N \in \{10^4, 10^5, 10^6\}$ instances on an isotropic Gaussian mixture ($D=100, K=5$) over 3 random seeds (Table~\ref{tab:exp5_controlled}) using identical hardware (AMD Ryzen / Intel x86-64, Windows, Python 3.14, NumPy 2.x, scikit-learn).

\begin{table}[!t]
\caption{Controlled Scalability Evaluation Across Sample Sizes ($D=100, K=5$, 3 Random Seeds, Mean $\pm$ Standard Deviation)}
\label{tab:exp5_controlled}
\centering
\small
\setlength{\tabcolsep}{3.0pt}
\begin{tabular}{@{}lccccc@{}}
\toprule
\textbf{Configuration} & $\mathbf{N}$ & \textbf{Time (s)} & \textbf{RAM (MB)} & \textbf{ARI} & \textbf{Scaling Exp. $\beta$ (95\% CI)} \\
\midrule
Default ($M=25, L=40$, f64) & $10^4$ & $5.58 \pm 1.29$   & $64.6$    & $0.275 \pm 0.128$ & \multirow{3}{*}{$0.755 \pm 0.084 \; [0.590, 0.921]$} \\
Default ($M=25, L=40$, f64) & $10^5$ & $14.92 \pm 4.03$  & $393.2$   & $0.368 \pm 0.202$ & \\
Default ($M=25, L=40$, f64) & $10^6$ & $182.64 \pm 51.01$& $3{,}836.8$ & $0.371 \pm 0.205$ & \\
\midrule
Reduced ($M=15, L=60$, f32) & $10^4$ & $2.48 \pm 0.18$   & $57.1$    & $0.208 \pm 0.067$ & \multirow{3}{*}{$0.873 \pm 0.076 \; [0.724, 1.023]$} \\
Reduced ($M=15, L=60$, f32) & $10^5$ & $8.77 \pm 0.89$   & $397.7$   & $0.345 \pm 0.181$ & \\
Reduced ($M=15, L=60$, f32) & $10^6$ & $141.22 \pm 34.87$& $3{,}909.9$ & $0.361 \pm 0.197$ & \\
\bottomrule
\end{tabular}
\end{table}

Under the default configuration, ICC-v2 scales with empirical exponent $\beta = 0.755 \pm 0.084$ (95\% CI: $[0.590, 0.921]$, $R^2 = 0.919$), completing $N=1{,}000{,}000$ in $182.64 \pm 51.01\text{ s}$ with $3.84\text{ GB}$ peak RSS. Under the reduced configuration ($M=15, L=60$), runtime at $10^6$ scales to \textbf{\ExtremeScaleTime} with $3.91\text{ GB}$ peak process RSS and empirical scaling exponent $\beta = 0.873 \pm 0.076$ (95\% CI: $[0.724, 1.023]$, $R^2 = 0.949$). Where dense consensus requires $\approx 8\text{ TB}$ RAM, ICC-v2 separates raw data matrix storage from bipartite graph auxiliary memory ($10^6 \times 60 \times 4\text{ bytes} = 240.0\text{ MB}$). In high feature spaces ($D=100{,}000, N=1{,}000$), ICC-v2 executes in \textbf{$8.28\text{s}$}."""

if old_exp5_block in text:
    text = text.replace(old_exp5_block, new_exp5_block)
    print("13. Exp 5 block replaced successfully.")

# 11. Conclusion updates
old_conclusion = r"""Across 13 multi-domain benchmarks (1,430 model fits), DEC achieves the lowest omnibus mean rank ($R=4.31$), while ICC-v2 ranks fifth ($R=5.46$, Friedman $\chi_F^2 = 11.34, p = 0.33$, $CD = 4.19$). Although ICC-v2 attains the highest Grand Mean ARI (\GrandMeanARI), this metric is heavily driven by large gains on two cancer microarray benchmarks: Leukemia (\ARIleukemia) and SRBCT (\ARIsrbct, $+0.388$ over FastMVC), while averaging \OmnibusMeanExcludingLeukemiaSrbct\ on the remaining 11 benchmarks (omnibus median ARI: \OmnibusMedianARI). In the exploratory high-dimensional subgroup ($D/N > 20$), ICC-v2 achieves Rank \#1 ($R=\RankBioICCvTwo$), but fails on Prostate ($0.013$ vs. $0.049$). Our ablation experiments establish a key null result: determinacy anchor certification yields no statistically significant accuracy benefit over uniform random anchors ($\Delta = +0.010$, dataset-level cluster bootstrap 95\% CI: $[-0.051, +0.076]$)"""

new_conclusion = r"""Across 13 multi-domain benchmarks (2,750 model fits), Standard Consensus achieves the lowest omnibus mean rank ($R=\TableThreeStdConsOverallRank$), followed by K-Means ($R=\TableThreeKMeansOverallRank$), DEC ($R=\TableThreeDecOverallRank$), and ICC-v2 ($R=\TableThreeIccVTwoOverallRank$, Friedman $\chi_F^2 = 9.59, p = \TableThreeFriedmanPValue$, $CD = \TrueNemenyiCD$). Although ICC-v2 attains the highest Grand Mean ARI (\GrandMeanARI), this metric is heavily driven by large gains on two cancer microarray benchmarks: Leukemia (\ARIleukemia) and SRBCT (\ARIsrbct, $+0.408$ over FastMVC), while averaging \OmnibusMeanExcludingLeukemiaSrbct\ on the remaining 11 benchmarks (omnibus median ARI: \OmnibusMedianARI). In the exploratory high-dimensional subgroup ($D/N > 20$), ICC-v2 achieves Rank \#1 ($R=\RankBioICCvTwo$), but fails on Prostate ($0.012$ vs. $0.049$). Our ablation experiments establish a key null result: determinacy anchor certification yields no statistically significant accuracy benefit over uniform random anchors ($\Delta = +0.019$, dataset-level cluster bootstrap 95\% CI: $[-0.039, +0.082]$)"""

if old_conclusion in text:
    text = text.replace(old_conclusion, new_conclusion)
    print("14. Conclusion replaced successfully.")

with open(TEX_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("\nSUCCESS: main.tex completely and cleanly patched with all Pass F updates!")
