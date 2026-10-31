# -*- coding: utf-8 -*-
from pathlib import Path
import re

def main():
    root = Path(__file__).resolve().parent.parent
    targets = [
        root / "springer_manuscript" / "main.tex",
        root / "paper" / "main.tex",
        root / "submission" / "source" / "main.tex",
        root / "submission" / "springer_nature_package" / "main.tex",
        root / "submission" / "overleaf_package" / "main.tex",
        root / "submission" / "arxiv_package" / "main.tex",
    ]

    for p in targets:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")

        # 1. ABSTRACT
        # Find \abstract{...}
        s_abs = text.find(r"\abstract{")
        e_abs = text.find(r"\keywords{", s_abs)
        assert s_abs != -1 and e_abs != -1, f"Abstract boundaries not found in {p}"
        
        # We need to find the matching closing brace before \keywords
        # It ends at the last '}' before \keywords
        close_brace = text.rfind("}", s_abs, e_abs)
        assert close_brace != -1, "Closing brace of abstract not found"

        new_abstract = (
            r"\abstract{Subsample stability is widely taken as evidence that a clustering is reliable, "
            r"and consensus clustering is widely assumed to resist high-dimensional noise. We test this premise "
            r"in simulations with isotropic distractor noise and on six biomedical cohorts ($D/N > 20$), "
            r"using stratified $80\%$ subsampling (30 draws, 435 pairs), column-permuted null controls, "
            r"and a non-degeneracy criterion added post hoc to exclude trivial partitions. In simulations, "
            r"accuracy (ARI) collapses for all methods as noise dimensions grow, and stability collapses with it "
            r"under subsampling, so the evidence for stability--accuracy discordance rests on the real cohorts. "
            r"There, three of twelve methods (FCAG, FCM, FastMVC) show non-degenerate discordance on three cohorts each. "
            r"Across these nine method--cohort cells, mean subsample stability is $0.684$, mean accuracy is $-0.003$ "
            r"and permuted-null stability is $\approx 0.01$; over all 18 cells for these methods, the means are "
            r"$0.638$ and $0.046$. A cohort-clustered bootstrap gives a positive stability--accuracy gap of $+0.485$ "
            r"(95\% CI $[+0.379, +0.662]$; unconstrained $+0.464$, $[+0.363, +0.607]$), so high reproducibility "
            r"does not imply correctness."
            "\n\n"
            r"We then use Gated Anchor Consensus (GAC), which combines Bimodality-Gated Subspace Selection (BGSS), "
            r"random-subspace ensembles and bipartite anchor graphs, to ask which components recover signal. "
            r"On the six high-$D$ cohorts, GAC reaches the highest mean ARI ($0.217$ vs. $0.037$ for ambient consensus), "
            r"concentrated in Leukemia ($0.600$) and SRBCT ($0.546$). Bipartite consensus alone ($0.046$) and random "
            r"feature gating with dense ($0.046$) or bipartite ($0.047$) consensus do not improve materially on ambient "
            r"consensus. BGSS adds $+0.169$ over matched random gating under bipartite consensus (95\% CI $[+0.036, +0.310]$) "
            r"but only $+0.031$ under dense consensus (CI $[-0.062, +0.149]$), so the gain depends on combining "
            r"multimodality gating with anchor-graph consensus and is driven by two cohorts. Determinacy-based anchors "
            r"give no gain over uniform sampling ($\Delta = +0.019$). Across 13 benchmarks (3,000 fits), omnibus "
            r"differences are not significant (Friedman $p = 0.40$), and GAC fails where marginal bimodality is absent "
            r"(Prostate, CNS, Madelon, count data). Bipartite compression reduces consensus-graph memory by 99.6\% at "
            r"$N = 10^4$. We conclude that stability should be reported with null controls and external validation, "
            r"and that marginal gating helps only when informative coordinates are detectably multimodal.}"
        )
        text = text[:s_abs] + new_abstract + text[close_brace+1:]

        # 2. INTRODUCTION: Main paragraph last sentences
        old_intro_tail = re.search(r"Our results show.*?are detectably multimodal\.", text, re.DOTALL)
        if old_intro_tail:
            new_intro_tail = (
                "Our results show that high subsample stability does not imply correctness on these cohorts, "
                "that random feature gating and anchor-graph compression each fail to improve accuracy on their own, "
                "and that marginal bimodality gating helps only in combination with bipartite consensus and only "
                "where informative coordinates are detectably multimodal."
            )
            text = text[:old_intro_tail.start()] + new_intro_tail + text[old_intro_tail.end():]

        # 3. CONTRIBUTION 2
        old_contrib2 = re.search(r"\\item \\textbf\{A (?:controlled|partial) decomposition of what recovers signal\.\}.*?(?=\\item \\textbf\{A boundary analysis)", text, re.DOTALL)
        if old_contrib2:
            new_contrib2 = (
                r"\item \textbf{A controlled decomposition of what recovers signal.} Using GAC as an experimental "
                r"vehicle, we cross gating (none, random, BGSS) with consensus type (dense, bipartite). Neither "
                r"bipartite consensus alone ($0.046$ vs. $0.037$) nor random gating ($0.046$ dense, $0.047$ bipartite) "
                r"improves materially on ambient consensus. BGSS raises ARI to $0.217$ under bipartite consensus "
                r"($+0.169$ over matched random gating, 95\% CI $[+0.036, +0.310]$) but only to $0.077$ under dense "
                r"consensus ($+0.031$, CI $[-0.062, +0.149]$). The gain is concentrated in Leukemia and SRBCT, "
                r"and determinacy-based anchors add nothing measurable ($\Delta = +0.019$, 95\% CI $[-0.040, +0.082]$)."
                "\n\n"
            )
            text = text[:old_contrib2.start()] + new_contrib2 + text[old_contrib2.end():]

        # 4. SECTION 6.2 (around line 564)
        old_sec62 = re.search(r"Evaluating BGSS directly against matched random subspace gating.*?Table~\\ref\{tab:factorial\}\) yields only \$0\.046\$ \(\$\\Delta = \+0\.009\$\)\.", text, re.DOTALL)
        if old_sec62:
            new_sec62 = (
                r"Evaluating BGSS directly against matched random subspace gating ($|\mathcal{F}_{\text{active}}| = \lfloor \alpha D \rfloor$ "
                r"across 30 seeds $\{0, \dots, 29\}$ on the six cohorts) shows that random feature gating yields a subgroup "
                r"mean of $0.047$ under bipartite consensus and $0.046$ under dense consensus, performing comparably to ambient "
                r"consensus ($0.046$ bipartite, $0.037$ dense). BGSS multimodality gating raises ARI to $0.217$ under bipartite "
                r"consensus, a paired gain of $+0.169$ over matched random gating (95\% cohort-clustered bootstrap CI $[+0.036, +0.310]$, "
                r"Wilcoxon $W = 0.0, p = 0.0312$). By contrast, under dense consensus BGSS reaches $0.077$, adding only $+0.031$ "
                r"over random dense gating (95\% CI $[-0.062, +0.149]$, Wilcoxon $p = 1.0$), demonstrating that multimodality "
                r"gating and bipartite anchor consensus interact to recover signal."
            )
            text = text[:old_sec62.start()] + new_sec62 + text[old_sec62.end():]

        # 5. SECTION 7.3
        # Look for Table~\ref{tab:factorial} ... Table~\ref{tab:component_contributions}
        s_73 = text.find(r"\input{gen/table12_factorial_decomposition.tex}")
        if s_73 != -1:
            e_73 = text.find(r"\input{gen/table13_component_contributions.tex}", s_73)
            assert e_73 != -1, "table13_component_contributions.tex not found after table12"
            
            new_sec73_body = (
                "\n\n"
                r"Table~\ref{tab:factorial} summarizes a $2 \times 2$ comparison of subgroup mean ARI across the six "
                r"high-dimensional cohorts. Without feature gating, replacing dense consensus ($0.037$) with bipartite "
                r"consensus ($0.046$) changes ARI by only $+0.009$. With BGSS gating, dense consensus reaches $0.077$ "
                r"and bipartite consensus $0.217$, an interaction of $V_5 - V_2 = +0.139$ (95\% cohort-clustered bootstrap "
                r"CI $[+0.007, +0.321]$; Wilcoxon $W = 3.0, p = 0.16, n = 6$), driven by Leukemia ($+0.558$) and SRBCT ($+0.213$)."
                "\n\n"
                r"To separate the effect of multimodality gating from that of feature subsampling, we evaluated matched "
                r"random gating (the same pool size, $\lfloor \alpha D \rfloor$, drawn at random) over the same 30 seeds. "
                r"Random gating gives $0.046$ under dense consensus and $0.047$ under bipartite consensus with core anchors "
                r"($0.053$ with uniform anchors), none materially above ambient consensus. Against these controls, BGSS "
                r"adds $+0.169$ under bipartite consensus ($V_5$ vs. random; CI $[+0.036, +0.310]$; positive on all six cohorts, "
                r"Wilcoxon $p = 0.031$) and $+0.145$ with uniform anchors ($V_4$ vs. random; CI $[+0.006, +0.315]$, $p = 0.31$), "
                r"but only $+0.031$ under dense consensus ($V_2$ vs. random; CI $[-0.062, +0.149]$, $p = 1.0$). The dense-consensus "
                r"arm was added post hoc to complete the design. With six cohorts, the smallest attainable two-sided Wilcoxon "
                r"$p$ is $0.031$, and these tests are not corrected for the three comparisons, so we treat the BGSS effect "
                r"as suggestive. In Leukemia, dense consensus on the 1,069-feature BGSS space suffers from base-clusterer "
                r"degeneracy (frequent 1-cluster collapse in unperturbed dense consensus, pulling mean ARI down to $0.042$), "
                r"whereas bipartite anchor consensus with random-subspace ensembling avoids this collapse and reaches $0.600$. "
                r"Determinacy-based anchors give no measurable benefit ($V_5 - V_4 = +0.019$, CI $[-0.040, +0.082]$, $p = 0.84$). "
                r"Table~\ref{tab:component_contributions} reports the individual knockout contributions."
                "\n\n"
            )
            # Find the start of the paragraph following \input{gen/table12_factorial_decomposition.tex}
            end_input_12 = s_73 + len(r"\input{gen/table12_factorial_decomposition.tex}")
            text = text[:end_input_12] + new_sec73_body + text[e_73:]

        # 6. SECTION 8.1
        old_sec81 = re.search(r"\\subsection\{What the Results Show\}\\label\{sec:disc_results\}.*?(?=\\subsection\{Recommendations for Practice\})", text, re.DOTALL)
        if old_sec81:
            new_sec81 = (
                r"\subsection{What the Results Show}\label{sec:disc_results}" "\n"
                r"The primary empirical finding of this work is that reproducibility under resampling does not guarantee "
                r"correctness when $D \gg N$. While controlled simulations with isotropic distractor noise establish that "
                r"accuracy collapses toward zero under high dimensions (accompanied by a collapse in subsample stability), "
                r"evidence for stability--accuracy discordance rests on the real biomedical cohorts. There, three of the twelve "
                r"evaluated methods (FCAG, FCM, FastMVC) exhibit non-degenerate discordance on at least three cohorts. The overall "
                r"stability--accuracy gap averages $+0.485$ (95\% CI $[+0.379, +0.662]$), whereas column-permuted null stability "
                r"remains near zero. The geometric diagnostic on Prostate helps explain this breakdown: Ward linkage and K-Means "
                r"isolate a small group of PCA-space outliers ($N \approx 11$ to $14$), whereas spectral and anchor methods yield "
                r"balanced partitions aligned with the leading principal component ($r = 0.77\text{--}0.86$) and with total "
                r"per-sample expression ($r = -0.52\text{--}-0.59$). These partitions achieve high subsample stability because "
                r"they track a dominant axis of variation in the sample space; however, that axis does not correspond to clinical "
                r"tumor status." "\n\n"
                r"The GAC case study provides a second, more measured insight into what algorithmic mechanisms recover signal. "
                r"Bipartite graph compression alone yields only $+0.009$ ($0.037 \to 0.046$), and random feature gating alone "
                r"achieves comparable baseline performance whether paired with dense consensus ($0.046$) or bipartite consensus "
                r"($0.047$). BGSS multimodality gating raises performance substantially only in combination with bipartite "
                r"consensus ($+0.169$ over matched random gating, 95\% CI $[+0.036, +0.310]$, uncorrected Wilcoxon $p = 0.031$), "
                r"while adding only $+0.031$ under dense consensus (CI $[-0.062, +0.149]$). Determinacy-based anchor selection yields "
                r"no measurable benefit ($\Delta = +0.019$, 95\% CI $[-0.040, +0.082]$). Across 13 multi-domain benchmarks, the twelve "
                r"clustering methods are statistically indistinguishable (Friedman $p = 0.40, \text{CD} = 4.62$). The performance "
                r"advantage of GAC is concentrated in Leukemia ($0.600$) and SRBCT ($0.546$), where informative coordinates exhibit "
                r"detectable marginal multimodality, and BGSS recovers 27 of the 50 diagnostic Golub markers ($54.0\%$) without supervision. "
                r"Where marginal multimodality is absent, as in Prostate and CNS, GAC exhibits the same stability--accuracy discordance "
                r"as the baseline methods." "\n\n"
            )
            text = text[:old_sec81.start()] + new_sec81 + text[old_sec81.end():]

        # 7. SECTION 8.3 (Limitations)
        old_few_cohorts = re.search(r"\\item \\textbf\{Few cohorts\.\}.*?(?=\\item \\textbf\{Reference labels)", text, re.DOTALL)
        if old_few_cohorts:
            new_few_cohorts = (
                r"\item \textbf{Few cohorts and uncorrected tests.} High-dimensional inference rests on $n = 6$ biomedical "
                r"cohorts. This sample size restricts statistical power, the BGSS effect rests on two cohorts (Leukemia and "
                r"SRBCT), and pairwise Wilcoxon comparisons are uncorrected across the three gating tests, rendering the "
                r"observed $+0.169$ gain and interaction ($p \approx 0.16$) suggestive rather than definitive." "\n"
            )
            text = text[:old_few_cohorts.start()] + new_few_cohorts + text[old_few_cohorts.end():]

        # 8. SECTION 9 (Conclusion)
        old_sec9 = re.search(r"This paper asked whether reproducibility under resampling can be trusted.*?Future work should test", text, re.DOTALL)
        if old_sec9:
            new_sec9 = (
                r"This paper asked whether reproducibility under resampling can be trusted as evidence that a clustering "
                r"is correct when the number of features far exceeds the number of samples. While simulations demonstrate accuracy "
                r"collapse under high-dimensional isotropic noise, evidence for stability--accuracy discordance rests on the real "
                r"biomedical cohorts. On six biomedical cohorts ($D/N > 20$), several methods repeatedly converge onto the same "
                r"partitions under resampling while agreement with reference labels stays near chance. Across non-degenerate "
                r"partitions the stability--accuracy gap averages $+0.485$ (95\% CI $[+0.379, +0.662]$; unconstrained $+0.464$, "
                r"$[+0.363, +0.607]$), while column-permuted null stability remains near zero. Three of twelve methods "
                r"(FCAG, FCM, FastMVC) meet our non-degenerate discordance criterion on at least three cohorts. On Prostate, "
                r"the diagnostic analysis shows that these partitions follow a dominant axis of variation in the data "
                r"(outliers, the first principal component, total expression) rather than tumor status." "\n\n"
                r"The Gated Anchor Consensus (GAC) case study shows which design choices help and which do not. Neither "
                r"bipartite graph compression alone ($0.037 \to 0.046$) nor random feature gating ($0.046$ dense, $0.047$ bipartite) "
                r"improves materially over ambient consensus. Bimodality-Gated Subspace Selection adds $+0.169$ over matched random "
                r"gating under bipartite consensus (95\% CI $[+0.036, +0.310]$, uncorrected Wilcoxon $p = 0.031$), but only $+0.031$ "
                r"under dense consensus (CI $[-0.062, +0.149]$), demonstrating that the gain depends on combining multimodality "
                r"gating with bipartite anchor consensus. Determinacy-based anchor selection gives no measurable benefit "
                r"($\Delta = +0.019$, 95\% CI $[-0.040, +0.082]$). The gains concentrate in Leukemia ($0.600$) and SRBCT ($0.546$), "
                r"where informative coordinates are detectably multimodal. Across 13 benchmarks ($3{,}000$ model fits), the twelve "
                r"methods are statistically indistinguishable (Friedman $p = 0.40$), and GAC fails where marginal multimodality is "
                r"absent (Prostate, CNS), where structure is non-linear (Madelon), or where data are sparse or have many classes. "
                r"Bipartite compression reduces consensus-graph memory by $99.6\%$ at $N = 10^4$, but we do not claim linear "
                r"runtime scaling." "\n\n"
                r"Three practical implications follow. Stability should be reported together with null-control stability "
                r"and a degeneracy audit. Partitions should be validated externally and inspected for technical drivers "
                r"before biological interpretation. Univariate feature gating should be used only after checking that the "
                r"data show multimodal marginals. Limitations include the small number of high-dimensional cohorts, partial "
                r"reference labels, default hyperparameters with known $K$, and the absence of batch or clinical annotations. "
                r"Future work should test"
            )
            text = text[:old_sec9.start()] + new_sec9 + text[old_sec9.end():]

        # 9. FIGURE 2 CAPTION
        old_fig2_cap = re.search(r"\\caption\{Clustering under isotropic distractor noise\..*?\\label\{fig:falsification_suite\}", text, re.DOTALL)
        if old_fig2_cap:
            new_fig2_cap = (
                r"\caption{Clustering under isotropic distractor noise ($N=300, K=3$, 20 stratified 80\% subsample draws per noise level). "
                r"(a) Accuracy (ARI against ground truth) collapses toward zero for all methods as distractor dimensions grow. "
                r"(b) Subsample stability collapses alongside accuracy under row resampling (dropping to $\le 0.03$ for K-Means, "
                r"GMM, FCM, and Ward; Spectral lingers at $0.17$). (c) Subsample stability--accuracy gap ($\Delta = \text{Stability} - \text{ARI}$) "
                r"remains near zero, showing that evidence for stability--accuracy discordance rests on real cohorts rather than isotropic simulations.}" "\n"
                r"\label{fig:falsification_suite}"
            )
            text = text[:old_fig2_cap.start()] + new_fig2_cap + text[old_fig2_cap.end():]

        p.write_text(text, encoding="utf-8")
        print(f"Successfully updated {p}")

if __name__ == "__main__":
    main()
