# -*- coding: utf-8 -*-
from pathlib import Path

def replace_between(content, start_marker, end_marker, new_text, include_end=False):
    s = content.find(start_marker)
    assert s != -1, f"start_marker '{start_marker[:40]}' not found"
    if include_end:
        e = content.find(end_marker, s)
        assert e != -1, f"end_marker '{end_marker[:40]}' not found"
        e += len(end_marker)
    else:
        e = content.find(end_marker, s)
        assert e != -1, f"end_marker '{end_marker[:40]}' not found"
    return content[:s] + new_text + content[e:]

def main():
    targets = [
        Path('springer_manuscript/main.tex'),
        Path('paper/main.tex'),
        Path('submission/source/main.tex'),
        Path('submission/springer_nature_package/main.tex'),
        Path('submission/overleaf_package/main.tex'),
        Path('submission/arxiv_package/main.tex'),
    ]
    
    for p in targets:
        if not p.exists():
            continue
        text = p.read_text(encoding='utf-8')
        
        # 1. ABSTRACT
        new_abstract = (
            r"\abstract{Subsample stability is widely assumed to indicate clustering reliability, "
            r"and consensus clustering to resist high-dimensional noise. We test this premise in "
            r"simulations with isotropic distractor noise and on six biomedical cohorts ($D/N > 20$), "
            r"using stratified $80\%$ subsampling (30 draws, 435 pairs), column-permuted null controls, "
            r"and a non-degeneracy criterion added post hoc to exclude trivial partitions. In simulations, "
            r"accuracy (ARI) collapses for all methods as noise dimensions grow; seed-to-seed agreement is "
            r"uninformative for deterministic solvers, so the evidence for stability--accuracy discordance rests on "
            r"the real cohorts. There, three of twelve methods (FCAG, FCM, FastMVC) show non-degenerate discordance on "
            r"three cohorts each. Across these nine method--cohort cells, mean subsample stability is $0.684$ and mean "
            r"accuracy is $-0.003$ (permuted-null stability $\approx 0.01$); over all 18 cells for these methods, the means "
            r"are $0.638$ and $0.046$. A cohort-clustered bootstrap gives a positive stability--accuracy gap of $+0.485$ "
            r"(95\% CI $[+0.379, +0.662]$; unconstrained $+0.464$, $[+0.363, +0.607]$), so high stability does not imply correctness."
            "\n\n"
            r"We then use Gated Anchor Consensus (GAC), which combines Bimodality-Gated Subspace Selection (BGSS), "
            r"random-subspace ensembles and bipartite anchor graphs, to examine which components recover signal. On the six high-$D$ "
            r"cohorts, GAC reaches the highest mean ARI ($0.217$ vs. $0.037$ for ambient consensus), concentrated in Leukemia ($0.600$) "
            r"and SRBCT ($0.546$). Bipartite consensus without gating adds little ($0.046$ vs. $0.037$), and the larger gain ($0.155$) "
            r"appears when random-subspace gating is combined with bipartite consensus; because the dense-consensus counterpart was not "
            r"evaluated, this gain cannot be attributed to the graph alone. BGSS adds $+0.062$ over matched random gating "
            r"(95\% CI $[+0.013, +0.142]$; Wilcoxon $p = 0.0625$). Determinacy-based anchor selection gives no gain over uniform "
            r"sampling ($\Delta = +0.019$). Across 13 benchmarks (3,000 fits), omnibus differences are not significant (Friedman $p = 0.40$), "
            r"and GAC fails where marginal bimodality is absent (Prostate, CNS, Madelon, count data). Bipartite compression reduces "
            r"consensus-graph memory by 99.6\% at $N = 10^4$. We conclude that stability should be reported with null controls and "
            r"external validation, and that marginal gating helps only when informative coordinates are detectably multimodal.}"
            "\n\n"
        )
        text = replace_between(text, r'\abstract{', r'\keywords{', new_abstract)
        
        # 2. INTRODUCTION MAIN PARAGRAPH
        new_intro_p = (
            r"We address both questions. First, we measure stability--accuracy discordance in simulations and on six biomedical cohorts, "
            r"using column-permuted null controls and a non-degeneracy criterion (added post hoc, see Section~\ref{sec:setup_params}) to "
            r"exclude trivial partitions. Second, we examine which components of a feature-gated bipartite anchor ensemble (GAC) recover "
            r"signal, and where each fails. Our results show that high subsample stability does not imply correctness on these cohorts, "
            r"that the largest gain we observe arises when random-subspace gating is combined with bipartite consensus (a combination we "
            r"cannot decompose further with the current design), and that marginal bimodality gating adds a modest, suggestive improvement "
            r"only when informative coordinates are detectably multimodal."
            "\n\n"
        )
        text = replace_between(text, r'We address both questions.', r'\begin{figure*}[!t]', new_intro_p)
        
        # 3. CONTRIBUTION 1 & 2
        new_c1 = (
            r"\item \textbf{A systematic characterization of stability--accuracy discordance.} On six biomedical cohorts ($D/N > 20$; "
            r"30 stratified $80\%$ subsamples, 435 pairs), we show that several methods reproduce the same partition under resampling "
            r"while that partition has near-zero agreement with reference labels ($\text{ARI} \le 0.05$). Three of twelve methods "
            r"(FCAG, FCM, FastMVC) meet a non-degeneracy-restricted criterion on three cohorts each; across those nine cells, mean "
            r"stability is $0.684$, mean accuracy is $-0.003$, and column-permuted null stability is $\approx 0.01$, so the stability "
            r"reflects data structure rather than permutation artifacts. A cohort-clustered bootstrap gives a mean gap of $+0.485$ "
            r"(95\% CI $[+0.379, +0.662]$; unconstrained $+0.464$, $[+0.363, +0.607]$). The non-degeneracy criterion was added after the "
            r"original analysis plan and we report results with and without it. Simulations with isotropic noise establish the accompanying "
            r"accuracy collapse; seed-to-seed agreement is uninformative for deterministic solvers and is not used as evidence of discordance."
            "\n\n "
        )
        text = replace_between(text, r'\item \textbf{A systematic characterization', r'\item \textbf{A controlled decomposition', new_c1)
        
        new_c2 = (
            r"\item \textbf{A partial decomposition of what recovers signal.} Using GAC as an experimental vehicle, we compare gating "
            r"and consensus choices. Bipartite consensus without gating changes ARI little ($0.046$ vs. $0.037$), whereas random-subspace "
            r"gating combined with bipartite consensus reaches $0.155$. BGSS adds $+0.062$ over matched random gating (95\% CI $[+0.013, +0.142]$), "
            r"and determinacy-based anchors add nothing measurable ($\Delta = +0.019$, 95\% CI $[-0.039, +0.082]$). The design lacks a "
            r"dense-consensus random-gating arm, so the gain from random gating and the gain from the bipartite graph are not separately identified."
            "\n\n "
        )
        text = replace_between(text, r'\item \textbf{A controlled decomposition', r'\item \textbf{A boundary analysis', new_c2)
        
        # 4. SECTION 3: DEFINITIONS
        new_def_part = (
            r"Following the analysis plan, a method--cohort cell is discordant under Rule~(i) if $\text{Stab} \ge 0.50$ and $\text{Acc} \le 0.05$. "
            r"Because a degenerate partition (for example, one dominant cluster) attains high stability by construction, Rule~(i') additionally "
            r"requires the smallest cluster to hold at least 5\% of the subsample in at least 90\% of subsamples. Rules~(i)--(iii) were "
            r"specified in commit \texttt{3307380}; Rule~(i') was added post hoc in commit \texttt{548d68d} after the Core-Halo collapse on Prostate "
            r"was observed, and we report outcomes with and without it. Rule~(ii) flags cells where real stability exceeds column-permuted null "
            r"stability by less than 0.10. Rule~(iii) requires the bootstrap interval of the mean gap to exclude zero. Because $\text{Acc} \approx 0$ "
            r"makes $\text{Stab} - \text{Acc} \approx \text{Stab}$, we also report $\text{Stab} - \text{Null}$ as the quantity that isolates stability "
            r"attributable to data structure. Reference controls (a near-constant and a random balanced partition) bracket the metric."
            "\n\n"
        )
        text = replace_between(text, r'A method-cohort pair is classified as discordant', r'\paragraph{Design.}', new_def_part)
        
        # 5. SECTION 3: SUMMARY OF FINDINGS
        new_sof = (
            r"\paragraph{Summary of findings.}"
            "\n"
            r"In simulations, ARI collapses toward zero for every method as distractor dimensions grow (Section~\ref{sec:sim_isotropic}); "
            r"because seed-to-seed agreement is trivially perfect for deterministic solvers, simulations are used to document the accuracy "
            r"collapse and not to demonstrate discordance. On six cohorts ($D$ from 2,000 to 15,154), three of twelve methods (FCAG, FCM, "
            r"FastMVC) meet Rule~(i') on three cohorts each. Across these nine cells, mean subsample stability is $0.684$, mean accuracy "
            r"is $-0.003$ and mean null stability is $\approx 0.01$. Over all 18 cells for the same three methods, the means are $0.638$ and "
            r"$0.046$. The gap averages $+0.485$ across non-degenerate cells (95\% CI $[+0.379, +0.662]$) and $+0.464$ unconstrained "
            r"(95\% CI $[+0.363, +0.607]$). These results motivate Section~\ref{sec:methodology}, where we ask which design choices reduce the gap."
            "\n\n"
        )
        text = replace_between(text, r'\paragraph{Summary of findings.}', r'\subsection{Simulation Under Isotropic Distractor Noise}', new_sof)
        
        # 6. SECTION 3.1 & FIG 2
        new_s31 = (
            r"Accuracy collapses as noise dimensions grow for all methods (Fig.~\ref{fig:ari_stability}). Seed-to-seed agreement "
            r"(Fig.~\ref{fig:dist_gap}) stays near 1 for Ward and spectral clustering, but these are deterministic solvers whose across-seed "
            r"agreement is 1 by construction, so this panel does not demonstrate stability in a meaningful sense. The stochastic methods "
            r"(K-Means, FCM, GMM) lose agreement and accuracy together. The simulations therefore establish the accuracy collapse and the "
            r"failure of alternative metrics to defer it indefinitely (Table~\ref{tab:distance_geometries}); evidence for stability--accuracy "
            r"discordance comes from the subsample protocol in Section~\ref{sec:real_data_stability}."
            "\n\n"
        )
        text = replace_between(text, r'In finite samples, base algorithms', r'\subsection{Evidence from Biomedical Cohorts}', new_s31)
        
        new_fig2_cap = (
            r"\caption{Clustering under isotropic distractor noise. (a) ARI against ground truth falls toward zero for all methods as noise "
            r"dimensions grow. (b) Seed-to-seed agreement; values near 1 for Ward and spectral clustering are trivial because these solvers are "
            r"deterministic. (c) Difference between seed agreement and ARI across noise distributions, subject to the same caveat.}"
        )
        text = replace_between(text, r'\caption{Empirical examination of consensus stability under finite-sample isotropic noise.', r'\label{fig:falsification_suite}', new_fig2_cap + '\n')
        
        # 7. FIG 3 CAPTION
        old_cap_sub = r"The shaded region highlights the non-degenerate stability-accuracy discordance zone (defined post hoc under Rule~(i'):"
        new_cap_sub = r"The shaded region highlights the non-degenerate discordance zone (Rule~(i'), added post hoc:"
        assert old_cap_sub in text
        text = text.replace(old_cap_sub, new_cap_sub)
        
        # 8. SECTION 4.2
        old_s42 = r"showing that bipartite graph compression acts primarily as an efficient computational compressor ($O(NL)$ memory) rather than a selective landmark filter."
        new_s42 = r"showing that determinacy-based anchor selection adds no measurable benefit."
        assert old_s42 in text
        text = text.replace(old_s42, new_s42)
        
        # 9. SECTION 6.2
        new_s62_sentence = (
            r"random-subspace gating combined with bipartite consensus reaches $0.155$ ($+0.118$ over ambient consensus), though the design "
            r"cannot separate the two components, with BGSS multimodality gating contributing an added $+0.062$ over random gating. By contrast, "
            r"running bipartite consensus on the full ambient feature space without subspace gating ($V_3$, Table~\ref{tab:factorial}) yields "
            r"only $0.046$ ($\Delta = +0.009$)."
        )
        text = replace_between(text, r'Most of the improvement over ambient consensus', r'\subsection{Statistical Analysis}', new_s62_sentence + '\n\n')
        
        # 10. SECTION 7.3
        new_s73 = (
            r"Table~\ref{tab:factorial} summarizes a $2 \times 2$ comparison of subgroup mean ARI across the six high-dimensional cohorts. "
            r"Without feature gating, replacing dense consensus ($0.037$) with bipartite anchor consensus ($0.046$) changes ARI by only $+0.009$. "
            r"Introducing BGSS within dense consensus gives $0.077$, and combining BGSS with bipartite consensus gives $0.217$, an interaction of "
            r"$V_5 - V_2 = +0.139$ (95\% cluster bootstrap CI $[+0.004, +0.321]$; Wilcoxon $W = 3.0, p \approx 0.16, n = 6$), driven predominantly "
            r"by Leukemia ($+0.557$)."
            "\n\n"
            r"A separate experiment (Section~\ref{sec:benchmarks_suite}; 30 seeds) replaced BGSS with matched random gating, restricting the "
            r"candidate pool to a random subset of the same size before bipartite consensus; this arm reaches $0.155$ ($+0.118$ over $0.037$). "
            r"This gain should not be attributed to the bipartite graph alone: bipartite consensus on ambient features gives $0.046$, and the "
            r"corresponding dense-consensus arm with random gating was not evaluated. The result is therefore best read as an interaction "
            r"between restricting the candidate pool and bipartite consensus. Because $0.155$ sits well above $0.046$ even though a random "
            r"pool is not expected to be more informative than the full feature set, seed-level variability on Leukemia and SRBCT may contribute, "
            r"so we regard this gain as suggestive and do not decompose it further. BGSS adds $+0.062$ over random gating (95\% CI $[+0.013, +0.142]$, "
            r"$p = 0.0625$). Any claim that bipartite compression attenuates spurious off-diagonal co-associations remains untested here. "
            r"Table~\ref{tab:component_contributions} reports the individual knockout contributions."
            "\n\n"
        )
        text = replace_between(text, r'In the absence of feature gating, replacing dense consensus', r'\input{gen/table13_component_contributions.tex}', new_s73)
        
        # 11. SECTION 7.4
        old_s74 = r"This confirms that bipartite graph factorization acts essentially as an efficient compression architecture rather than a selective landmark filter."
        new_s74 = r"This confirms that determinacy screening offers no proven performance edge over picking landmarks uniformly at random."
        assert old_s74 in text
        text = text.replace(old_s74, new_s74)
        
        # 12. SECTION 8.1
        old_s81 = r"Ensembling over random subspaces within the bipartite architecture accounts for $+0.118$ ($65.6\%$) of the $+0.180$ gain over ambient consensus ($0.037 \to 0.155$), while bipartite graph compression alone yields only $+0.009$ ($0.037 \to 0.046$)."
        new_s81 = r"random-subspace gating combined with bipartite consensus reaches $0.155$ ($+0.118$ over ambient consensus), though the design cannot separate the two components, while bipartite graph compression alone yields only $+0.009$ ($0.037 \to 0.046$)."
        assert old_s81 in text
        text = text.replace(old_s81, new_s81)
        
        # 13. SECTION 9
        old_s9 = r"Ensembling over random subspaces within the bipartite pipeline accounts for $+0.118$ ($65.6\%$) of the $+0.180$ empirical gain over ambient consensus on the six high-$D$ cohorts ($0.037 \to 0.155$), whereas bipartite graph compression without gating provides $+0.009$ ($0.037 \to 0.046$)."
        new_s9 = r"random-subspace gating combined with bipartite consensus reaches $0.155$ ($+0.118$ over ambient consensus), though the design cannot separate the two components, whereas bipartite graph compression without gating provides $+0.009$ ($0.037 \to 0.046$)."
        assert old_s9 in text
        text = text.replace(old_s9, new_s9)
        
        # 14. MISC LABELS
        text = text.replace('the proposed GAC pipeline', 'the GAC pipeline')
        text = text.replace('https://github.com/AkashKundu114/icc-clustering', 'https://github.com/AkashKundu114/gac-consensus-clustering')
        
        p.write_text(text, encoding='utf-8')
        print(f"[SUCCESS] Successfully updated all sections in {p}!")

if __name__ == '__main__':
    main()
