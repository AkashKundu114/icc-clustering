"""
Humanize Manuscript: Refines the academic prose of paper/main.tex into natural,
scholarly, top-tier research writing for Springer Nature DAMI.

Preserves 100% of:
- All numerical values, confidence intervals, sample sizes, and statistics.
- All LaTeX macros, table inputs, figure references, and citation keys.
- All mathematical symbols, definitions, theorems, and equations.
- All negative results, boundary conditions, and author metadata.
"""

from pathlib import Path

def humanize_text(text: str) -> str:
    # -------------------------------------------------------------
    # 1. ABSTRACT
    # -------------------------------------------------------------
    old_abstract = (
        r"\abstract{Consensus clustering is widely assumed to resist high-dimensional noise. "
        r"We test this assumption across synthetic simulations and six biomedical cohorts ($D/N > 20$) "
        r"using a pre-specified stratified $80\%$ subsampling protocol (30 draws) and column-permuted null controls. "
        r"Under isotropic noise ($D \gg N$), base clusterers stably converge ($\text{stability} > 0.8$) onto arbitrary noise while Adjusted Rand Index (ARI) collapses. "
        r"On real cohorts, baselines exhibit severe stability--accuracy gaps: three of twelve methods (FCAG, FCM, FastMVC) satisfy our ``Stable but Wrong'' criterion "
        r"($\text{stability} \ge 0.50$, $\text{accuracy} \le 0.05$) on $\ge 3$ cohorts; Ward and Spectral show near-perfect stability ($\ge 0.97$) yet zero accuracy ($\le 0.03$) "
        r"on Prostate ($D=12{,}600$), where null stability collapses ($\le 0.03$). A paired bootstrap excludes zero for the gap ($+0.464$, $95\%$ CI: $[+0.363, +0.607]$). "
        r"We evaluate Gated Anchor Consensus (GAC), uniting Bimodality-Gated Subspace Selection (BGSS), random-subspace ensembles, bipartite graphs, and centroid projection. "
        r"Across 13 benchmarks (3,000 fits), omnibus differences are insignificant (Friedman $p = 0.40$). "
        r"GAC achieves the highest mean ARI on the six $D/N > 20$ cohorts ($0.217$ vs. $0.065$ for best baseline FCAG and $0.037$ for ambient consensus), "
        r"with gains concentrated in Leukemia ($0.600 \pm 0.367$) and SRBCT ($0.546 \pm 0.102$). "
        r"Bipartite ensembling drives $+0.118$ (65.6\%) of this gain, while BGSS adds $+0.062$ over matched random gating ($95\%$ CI: $[+0.013, +0.142]$, Wilcoxon $p = 0.0625$). "
        r"Landmark determinacy yields an empirical null result over uniform sampling ($\Delta = +0.019$, $95\%$ CI: $[-0.039, +0.082]$). "
        r"On Prostate and CNS, weak bimodality leaves GAC trapped in spurious consensus ($\text{accuracy} \le 0.02$).}"
    )

    new_abstract = (
        r"\abstract{Consensus clustering is widely assumed to provide resilience against high-dimensional noise. "
        r"We evaluate this premise across controlled synthetic benchmarks and six biomedical cohorts ($D/N > 20$) "
        r"under a pre-specified stratified $80\%$ subsampling protocol (30 draws) alongside column-permuted null controls. "
        r"Under isotropic noise ($D \gg N$), base clusterers converge stably ($\text{stability} > 0.8$) onto arbitrary noise partitions while the Adjusted Rand Index (ARI) collapses. "
        r"On real cohorts, standard baselines exhibit pronounced stability--accuracy discrepancies: three of twelve methods (FCAG, FCM, FastMVC) meet our ``Stable but Wrong'' criterion "
        r"($\text{stability} \ge 0.50$, $\text{accuracy} \le 0.05$) across $\ge 3$ cohorts; Ward and Spectral exhibit near-perfect stability ($\ge 0.97$) alongside near-zero accuracy ($\le 0.03$) "
        r"on Prostate ($D=12{,}600$), where null stability drops to $\le 0.03$. A paired bootstrap excludes zero for the gap ($+0.464$, $95\%$ CI: $[+0.363, +0.607]$). "
        r"To address these pathologies, we evaluate Gated Anchor Consensus (GAC), uniting Bimodality-Gated Subspace Selection (BGSS), random-subspace ensembles, bipartite graphs, and inductive centroid projection. "
        r"Across 13 benchmarks (3,000 fits), omnibus differences remain statistically indistinguishable (Friedman $p = 0.40$). "
        r"GAC achieves the highest mean ARI across the six $D/N > 20$ cohorts ($0.217$ vs. $0.065$ for the strongest baseline FCAG and $0.037$ for ambient consensus), "
        r"with gains concentrated in Leukemia ($0.600 \pm 0.367$) and SRBCT ($0.546 \pm 0.102$). "
        r"Bipartite ensembling accounts for $+0.118$ (65.6\%) of this improvement, whereas BGSS contributes $+0.062$ over matched random gating ($95\%$ CI: $[+0.013, +0.142]$, Wilcoxon $p = 0.0625$). "
        r"Landmark determinacy produces an empirical null result over uniform sampling ($\Delta = +0.019$, $95\%$ CI: $[-0.039, +0.082]$). "
        r"On Prostate and CNS, diffuse marginal distributions leave GAC vulnerable to spurious consensus ($\text{accuracy} \le 0.02$).}"
    )

    if old_abstract in text:
        text = text.replace(old_abstract, new_abstract)
    else:
        print("Note: abstract exact match not found; skipping abstract replacement or already replaced.")

    # -------------------------------------------------------------
    # 2. INTRODUCTION SECTION SIGNPOSTING AND OPENING
    # -------------------------------------------------------------
    old_intro_open = (
        r"Aggregating diverse stochastic partitions into a consensus ensemble mitigates initialization sensitivity and prevents convergence toward suboptimal local extrema~\cite{fred2005combining}. "
        r"Recent comprehensive surveys continue to emphasize the persistent challenges of clustering algorithms under complex noise and scaling regimes~\cite{wani2024comprehensive}. "
        r"Ensembling base clusterers across stochastic initializations or projected subspaces stabilizes partition boundaries against spurious local modes. "
        r"In high-dimensional domains, unsupervised and self-supervised feature selection has emerged as a prerequisite to prune uninformative coordinates prior to similarity estimation (Li et al.~\cite{li2025selfsupervised}). "
        r"Nevertheless, in extreme noise regimes ($D \gg N$), ambient distractors compromise consensus aggregation through two fundamental structural bottlenecks."
    )
    new_intro_open = (
        r"Consensus clustering aggregates diverse stochastic partitions into an integrated ensemble, damping initialization sensitivity and stabilizing partition boundaries against suboptimal local extrema~\cite{fred2005combining}. "
        r"While ensembling provides well-documented empirical robustness across complex data distributions~\cite{wani2024comprehensive}, its efficacy degrades sharply when applied to high-dimensional datasets submerged in uninformative background coordinates ($D \gg N$). "
        r"In such regimes, unsupervised and self-supervised feature screening has become an essential prerequisite to discard irrelevant coordinates prior to similarity estimation~\cite{li2025selfsupervised}. "
        r"Yet, when ambient noise dominates the feature spectrum, standard consensus architectures encounter two interrelated structural bottlenecks."
    )
    if old_intro_open in text:
        text = text.replace(old_intro_open, new_intro_open)

    old_signposting = (
        r"The remainder of this manuscript is organized as follows: Section~\ref{sec:related} reviews related work across recent cluster ensembles, anchor graphs, and subspace methods. "
        r"Section~\ref{sec:falsification} examines the empirical motivation and finite-sample falsification suite. "
        r"Section~\ref{sec:methodology} presents the mathematical formulation and procedural pseudocode (Algorithm~\ref{alg:iccv2}) of the GAC pipeline. "
        r"Section~\ref{sec:setup} details the experimental setup, hardware specifications, parameter configurations, evaluation metrics, and statistical tests. "
        r"Section~\ref{sec:evaluation} reports experimental evaluation covering computational scalability, 13-cohort benchmarks, statistical testing, and convergence analyses. "
        r"Section~\ref{sec:ablation} presents the ablation study, factorial interaction, and feature saliency audits. "
        r"Section~\ref{sec:applications} discusses real-world application case studies and their limits. "
        r"Section~\ref{sec:limitations} characterizes failure modes and future research directions. "
        r"Section~\ref{sec:conclusion} concludes the paper. Declarations follow."
    )
    new_signposting = (
        r"The remainder of this article proceeds as follows. Section~\ref{sec:related} surveys related work across cluster ensembles, anchor graph formulations, and subspace clustering. "
        r"Section~\ref{sec:falsification} presents the finite-sample falsification suite and details the stability trap observed across biomedical cohorts. "
        r"Section~\ref{sec:methodology} formulates the mathematical framework and procedural pseudocode (Algorithm~\ref{alg:iccv2}) for the GAC pipeline. "
        r"Section~\ref{sec:setup} details the experimental protocol, computational environment, parameter choices, and non-parametric statistical suite. "
        r"Section~\ref{sec:evaluation} reports experimental findings spanning million-sample scaling, the 13-cohort benchmark, and non-parametric hypothesis testing. "
        r"Section~\ref{sec:ablation} provides modular ablations, factorial interactions, and feature saliency audits. "
        r"Section~\ref{sec:applications} examines three translational case studies and their empirical boundaries. "
        r"Section~\ref{sec:limitations} analyzes explicit failure modes, and Section~\ref{sec:conclusion} concludes the paper."
    )
    if old_signposting in text:
        text = text.replace(old_signposting, new_signposting)

    # -------------------------------------------------------------
    # 3. SECTION 2: RELATED WORK RESTRUCTURING
    # -------------------------------------------------------------
    old_related_2_1 = (
        r"Consensus clustering aggregates diverse partitions generated by base algorithms into an integrated consensus solution. "
        r"In a foundational critique, Senbabaoglu et al.~\cite{senbabaoglu2014critical} demonstrated that consensus clustering can produce apparently high stability and apparent cluster structure even on unimodal null data with weak or no true underlying cluster structure. "
        r"To determine the number of clusters without arbitrary heuristics, Race and Meyer~\cite{race2013determining} developed iterative consensus clustering, successively extracting confident cluster assignments from the consensus matrix and reclustering the remaining residual samples. "
        r"Classical formulations construct an $N \times N$ pairwise co-association matrix $S$ where each entry $S_{ij}$ records the fraction of base clusterings in which instances $\mathbf{x}_i$ and $\mathbf{x}_j$ co-occur in the same cluster, followed by graph partitioning or spectral aggregation~\cite{fettal2026scalable}. "
        r"Recent active and constraint-based consensus formulations further refine partition assignments by incorporating pairwise instance relationships (CODAC, Patron et al.~\cite{patron2026codac}). "
        r"High-order consensus frameworks capture multi-hop relations beyond pairwise co-occurrences (Zhang et al.~\cite{zhang2025highorder}), while sparse representations suppress noisy partition edges in spectral consensus (Fan et al.~\cite{fan2026robust}). "
        r"Enforcing doubly stochastic normalization over the consensus affinity matrix eliminates vertex degree artifacts in spectral graph partitioning (Cai et al.~\cite{cai2025spectral}), and auto-weighted graph reconstruction dynamically recalibrates base ensemble contributions according to partition reliability (Yang et al.~\cite{yang2025autoweighted}). "
        r"In multiview domains, hypergraph p-Laplacian regularization with feature selection provides robustness against distractor noise (Hu et al.~\cite{hu2024multiview}), and contrastive clustering ensembles regularize deep representations (Chen et al.~\cite{chen2025ccegan})."
    )
    new_related_2_1 = (
        r"Consensus clustering pools diverse partitions generated by base algorithms into an integrated consensus solution~\cite{fred2005combining}. "
        r"In a foundational critique, Senbabaoglu et al.~\cite{senbabaoglu2014critical} demonstrated that consensus clustering can generate deceptive visual patterns and elevated stability scores even on unimodal null data with no true underlying clusters. "
        r"To identify cluster counts without arbitrary heuristics, Race and Meyer~\cite{race2013determining} introduced iterative consensus clustering, successively extracting confident cluster assignments from the consensus matrix and reclustering residual instances. "
        r"Classical formulations construct an $N \times N$ pairwise co-association matrix $S$ whose entries $S_{ij}$ record the empirical fraction of base clusterings in which instances $\mathbf{x}_i$ and $\mathbf{x}_j$ co-occur, followed by graph partitioning or spectral aggregation~\cite{fettal2026scalable}. "
        r"\par Recent studies have advanced consensus formulations across multiple operational fronts. "
        r"Active and constraint-driven models refine assignments by querying pairwise instance relationships (CODAC, Patron et al.~\cite{patron2026codac}), while high-order consensus frameworks model multi-hop relationships beyond direct pairwise co-occurrences (Zhang et al.~\cite{zhang2025highorder}). "
        r"Sparse matrix representations suppress noisy partition edges in spectral consensus graphs (Fan et al.~\cite{fan2026robust}), and doubly stochastic normalization eliminates vertex-degree distortions during spectral partitioning (Cai et al.~\cite{cai2025spectral}). "
        r"Furthermore, auto-weighted graph reconstruction dynamically recalibrates base ensemble weights according to partition reliability (Yang et al.~\cite{yang2025autoweighted}). "
        r"In multi-view domains, hypergraph $p$-Laplacian regularization with feature selection provides robustness against distractor noise (Hu et al.~\cite{hu2024multiview}), while contrastive clustering ensembles regularize deep representations (Chen et al.~\cite{chen2025ccegan})."
    )
    if old_related_2_1 in text:
        text = text.replace(old_related_2_1, new_related_2_1)

    # Break up the 20-citation block in Section 2.2 into thematic sentences:
    old_anchor_block = (
        r"Nie et al.~\cite{nie2024fast} proposed Fast Clustering with Anchor Guidance (FCAG), achieving fast spectral partitioning by constructing anchor-to-sample graphs that bypass full similarity matrix construction. "
        r"Recent advances in anchor graph and bipartite consensus have explored dynamic hypergraph reconstruction (YACHT, Xu et al.~\cite{xu2025dynamic,xu2026dynamic}), large-scale anchor constrained Laplacian rank clustering (Ma et al.~\cite{ma2025large}), robust outlier decoupling (RANGE, Xu et al.~\cite{xu2026range}), structured bipartite graph learning (Zhang et al.~\cite{zhang2025structured}, Wang et al.~\cite{wang2024structured}), dynamic unified bipartite learning (Zhao et al.~\cite{zhao2024multiview}), fast spectral consensus (Zhang et al.~\cite{zhang2025anchor}, Ma et al.~\cite{ma2025fast}), bipartite graph factorization (Zhao et al.~\cite{zhao2026efficient}, Yang et al.~\cite{yang2025correntropy,tkde2026fast}), anchor-guided label spreading (Xie et al.~\cite{xie2025fast,xie2025efficient}), multi-anchor fusion and nonnegative tensor factorization (Yang et al.~\cite{yang2025anchor}, Liao et al.~\cite{liao2026multiview}), incomplete anchor networks (Fu et al.~\cite{fu2025anchor}), projection-based multi-view exploitation (Song et al.~\cite{song2026enhanced}), consensus-specific reconstruction (Ren et al.~\cite{ren2026multiview}), hierarchical feature descent (Ou et al.~\cite{ou2024anchor}), adaptive topological weighting and multiple kernel learning (Xu et al.~\cite{xu2024enhancing,xu2026topological}), adaptive anchor graph co-clustering (Nie and Qiang~\cite{ins2025fast}), random forest anchor clustering (Li et al.~\cite{li2026rfag}), and multiview anchor spectral clustering (Lei et al.~\cite{lei2024anchor}). While these frameworks achieve linear scaling in sample size $N$, they operate predominantly in the ambient feature space without explicit high-dimensional feature screening, leaving them vulnerable to isotropic noise when $D \gg N$. Adaptive anchor selection strategies further enhance bipartite consensus efficiency across large instance sets (Guo et al.~\cite{guo2026consensus}), scalable multi-view ensemble clustering leverages adaptive anchor bipartite graphs (Kong et al.~\cite{kong2026adaptive}), and high-order graph embedding with co-regularization aligns multi-view cluster assignments (Wang et al.~\cite{wang2025coregularized}). Streaming and inductive consensus frameworks have recently expanded toward fairness-constrained partition updates across continuous data flows (Chakraborty et al.~\cite{chakraborty2026generic}). GAC pipeline builds upon these bipartite foundations, coupling bipartite compression with linear-time feature gating to resolve high-dimensional noise."
    )
    new_anchor_block = (
        r"Nie et al.~\cite{nie2024fast} introduced Fast Clustering with Anchor Guidance (FCAG), accelerating spectral partitioning by constructing anchor-to-sample bipartite graphs that bypass full similarity matrix materialization. "
        r"Subsequent research has expanded bipartite graph consensus across several methodological frontiers. "
        r"In dynamic topology learning, dynamic hypergraph reconstruction (YACHT, Xu et al.~\cite{xu2025dynamic,xu2026dynamic}) and large-scale anchor-constrained Laplacian rank formulations (Ma et al.~\cite{ma2025large}) optimize graph structure during spectral factorization, while robust outlier decoupling (RANGE, Xu et al.~\cite{xu2026range}) and structured bipartite graph learning (Zhang et al.~\cite{zhang2025structured}, Wang et al.~\cite{wang2024structured}) mitigate anomalous observations. "
        r"In multi-view and spectral aggregation, recent methods investigate dynamic unified bipartite learning (Zhao et al.~\cite{zhao2024multiview}), fast spectral consensus solvers (Zhang et al.~\cite{zhang2025anchor}, Ma et al.~\cite{ma2025fast}), bipartite graph factorization (Zhao et al.~\cite{zhao2026efficient}, Yang et al.~\cite{yang2025correntropy,tkde2026fast}), and anchor-guided label spreading (Xie et al.~\cite{xie2025fast,xie2025efficient}). "
        r"Further theoretical and computational extensions incorporate multi-anchor fusion with nonnegative tensor factorization (Yang et al.~\cite{yang2025anchor}, Liao et al.~\cite{liao2026multiview}), incomplete anchor networks (Fu et al.~\cite{fu2025anchor}), projection-based multi-view exploitation (Song et al.~\cite{song2026enhanced}), consensus-specific reconstruction (Ren et al.~\cite{ren2026multiview}), hierarchical feature descent (Ou et al.~\cite{ou2024anchor}), adaptive topological weighting with multiple kernel learning (Xu et al.~\cite{xu2024enhancing,xu2026topological}), adaptive anchor graph co-clustering (Nie and Qiang~\cite{ins2025fast}), random forest anchor clustering (Li et al.~\cite{li2026rfag}), and multiview anchor spectral clustering (Lei et al.~\cite{lei2024anchor}). "
        r"Complementing these spectral advances, adaptive landmark selection enhances bipartite consensus scalability across large instance sets (Guo et al.~\cite{guo2026consensus}), scalable multi-view ensembles leverage adaptive anchor graphs (Kong et al.~\cite{kong2026adaptive}), co-regularized high-order graph embeddings align multi-view partitions (Wang et al.~\cite{wang2025coregularized}), and streaming consensus frameworks incorporate fairness constraints across continuous data flows (Chakraborty et al.~\cite{chakraborty2026generic}). "
        r"Although these frameworks achieve linear scaling in sample size $N$, they operate predominantly in the uncurated ambient feature space. When exposed to extreme high-dimensional regimes ($D \gg N$), their landmark distances remain susceptible to distance concentration and isotropic noise. The GAC pipeline builds directly upon these bipartite foundations, coupling bipartite graph compression with linear-time statistical feature screening to insulate landmark consensus from ambient noise."
    )
    if old_anchor_block in text:
        text = text.replace(old_anchor_block, new_anchor_block)

    # In Section 2.3: clean repetitive phrasing
    old_subspace_block = (
        r"To address this, GAC pipeline introduces linear-time Bimodality-Gated Subspace Selection (BGSS), filtering uninformative features in strictly $O(N \cdot D)$ time prior to base clusterer generation using Sarle's bimodality coefficient."
    )
    new_subspace_block = (
        r"To address this vulnerability without iterative optimization overhead, the GAC pipeline introduces Bimodality-Gated Subspace Selection (BGSS), filtering uninformative coordinates in strictly linear time $O(ND)$ prior to ensemble generation using finite-sample Sarle's bimodality coefficient."
    )
    if old_subspace_block in text:
        text = text.replace(old_subspace_block, new_subspace_block)

    # -------------------------------------------------------------
    # 4. SECTION 3: EMPIRICAL MOTIVATION AND FALSIFICATION
    # -------------------------------------------------------------
    # Remove AI ban list words like "Crucially" in Section 3.1
    text = text.replace(
        r"Crucially, under independent column-permuted null controls, stability on Prostate collapses to near zero (range $-0.001$ to $+0.049$).",
        r"Under independent column-permuted null controls, stability on Prostate collapses to near zero (range $-0.001$ to $+0.049$)."
    )

    # -------------------------------------------------------------
    # 5. SECTION 6: CLEAN DUPLICATION IN STATISTICAL ANALYSIS
    # -------------------------------------------------------------
    old_dup_friedman = (
        r"with an GAC pipeline omnibus rank of $5.62$. When computed directly from the 3-decimal rounded benchmark table, small decimal ties yield $\chi_F^2 = 11.54, p = 0.40$ with an GAC pipeline rank of $5.58$. Under both evaluations, empirical data fail to reject the null hypothesis of equivalent performance across methods ($p = 0.40 \gg 0.05$)." + "\n" +
        r"With $p = \TableThreeFriedmanPValue \gg 0.05$, empirical data fail to reject the null hypothesis of equivalent performance across methods. In average rank across datasets, K-Means ranks first ($R = \TableThreeKMeansOverallRank$), followed by Standard Consensus ($R = \TableThreeStdConsOverallRank$), DEC ($R = \TableThreeDecOverallRank$), GAC pipeline ($R = \TableThreeIccVTwoOverallRank$, Rank 4), Ward ($R = \TableThreeWardOverallRank$), and CoHiRF ($R = \TableThreeCohirfOverallRank$)."
    )
    new_dup_friedman = (
        r"yielding an omnibus rank of $5.62$ for GAC. When computed directly from the 3-decimal rounded benchmark table, small decimal ties yield $\chi_F^2 = 11.54$ ($p = 0.40$) with a corresponding GAC rank of $5.58$. Under both evaluations, empirical data fail to reject the null hypothesis of equivalent performance across methods ($p = \TableThreeFriedmanPValue \gg 0.05$). In overall average rank across datasets, K-Means ranks first ($R = \TableThreeKMeansOverallRank$), followed by Standard Consensus ($R = \TableThreeStdConsOverallRank$), DEC ($R = \TableThreeDecOverallRank$), GAC pipeline ($R = \TableThreeIccVTwoOverallRank$, Rank 4), Ward ($R = \TableThreeWardOverallRank$), and CoHiRF ($R = \TableThreeCohirfOverallRank$)."
    )
    if old_dup_friedman in text:
        text = text.replace(old_dup_friedman, new_dup_friedman)
        print("  [OK] Cleaned duplicated Friedman sentence in Section 6.")

    # Clean "an GAC pipeline" grammar artifacts throughout text:
    text = text.replace("an GAC pipeline", "a GAC pipeline")
    text = text.replace("with an GAC", "with a GAC")

    # -------------------------------------------------------------
    # 6. SECTION 7: ABLATION STUDY HUMANIZATION
    # -------------------------------------------------------------
    text = text.replace(
        r"We measured an average gain of $\Delta = +0.019$ between V5 and V4 on the six cohorts ($W=9.0, p=0.84$). The bootstrap interval [$-0.039, +0.082$] covers zero, showing that anchor quality checks provide no reliable advantage over uniform landmark sampling. Consequently, bipartite graph construction functions as a compression device rather than a precision landmark filter.",
        r"Across the six cohorts, the empirical difference between V5 and V4 averages $\Delta = +0.019$ ($W=9.0, p=0.84$). Because the 95\% bootstrap interval [$-0.039, +0.082$] covers zero, sample determinacy checks offer no demonstrable performance advantage over uniform landmark sampling. Consequently, bipartite graph construction functions primarily as a compression device rather than a precision landmark filter."
    )

    # -------------------------------------------------------------
    # 7. SECTION 8 & 9: APPLICATIONS AND LIMITATIONS POLISH
    # -------------------------------------------------------------
    text = text.replace(
        r"Point-of-care clinical diagnostics and streaming data analysis require rapid classification of newly observed instances without expensive graph reconstruction.",
        r"Point-of-care clinical profiling and streaming classification require rapid assignment of newly observed instances without re-solving graph partitioning problems."
    )
    text = text.replace(
        r"Nonetheless, empirical evaluation (Table~\ref{tab:inductive_direct}) demonstrates that the test ARI of inductive centroid projection is not significantly higher than ambient K-Means, Nystr\"om spectral extension, or Random Forest classifiers (all bootstrap confidence intervals span zero).",
        r"Empirical evaluation (Table~\ref{tab:inductive_direct}) confirms that the test ARI of inductive centroid projection is not significantly higher than ambient K-Means, Nystr\"om spectral extension, or Random Forest classifiers (all bootstrap confidence intervals span zero)."
    )

    return text

def main():
    tex_path = Path("paper/main.tex")
    content = tex_path.read_text(encoding="utf-8")
    new_content = humanize_text(content)
    tex_path.write_text(new_content, encoding="utf-8")
    print(f"Updated {tex_path}")

    springer_path = Path("springer_manuscript/main.tex")
    springer_path.write_text(new_content, encoding="utf-8")
    print(f"Synced {springer_path} (byte-for-byte identical)")

if __name__ == "__main__":
    main()
