# -*- coding: utf-8 -*-
from pathlib import Path
import re

def main():
    root = Path(__file__).resolve().parent.parent

    # 1. Update Table 2 / Table 3 caption across all occurrences
    tab2_files = [
        root / "paper" / "gen" / "table02_real_data_stability.tex",
        root / "springer_manuscript" / "gen" / "table02_real_data_stability.tex",
        root / "submission" / "springer_nature_package" / "gen" / "table02_real_data_stability.tex",
        root / "submission" / "overleaf_package" / "gen" / "table02_real_data_stability.tex",
    ]
    for tf in tab2_files:
        if not tf.exists():
            continue
        c = tf.read_text(encoding="utf-8")
        c = c.replace(
            "satisfy pre-specified Decision Rule~(i)",
            "satisfy pre-specified Decision Rules~(i)--(iii)"
        )
        tf.write_text(c, encoding="utf-8")
        print(f"Updated caption in {tf}")

    # 2. Update all main.tex targets
    targets = [
        root / "springer_manuscript" / "main.tex",
        root / "paper" / "main.tex",
        root / "submission" / "source" / "main.tex",
        root / "submission" / "springer_nature_package" / "main.tex",
        root / "submission" / "overleaf_package" / "main.tex",
        root / "submission" / "arxiv_package" / "main.tex",
        root / "submission" / "arxiv_source" / "main.tex",
    ]

    for p in targets:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")

        # A. ABSTRACT: Tighten to ~250 words per DAMI guidelines and user suggestion
        s_abs = text.find(r"\abstract{")
        e_abs = text.find(r"\keywords{", s_abs)
        if s_abs != -1 and e_abs != -1:
            close_brace = text.rfind("}", s_abs, e_abs)
            new_abstract = (
                r"\abstract{Subsample stability is widely assumed to indicate clustering reliability, "
                r"and consensus clustering to resist high-dimensional noise. We test this premise in isotropic "
                r"simulations and on six biomedical cohorts ($D/N > 20$), using stratified $80\%$ subsampling "
                r"($30$ draws, $435$ pairs), column-permuted null controls, and a non-degeneracy criterion added "
                r"post hoc to exclude trivial partitions. In simulations, accuracy collapses with noise dimensions "
                r"and subsample stability collapses alongside it, so evidence for stability--accuracy discordance "
                r"rests on the real cohorts. There, three of twelve methods (FCAG, FCM, FastMVC) show non-degenerate "
                r"discordance on three cohorts each. Across these nine cells, mean stability is $0.684$ and mean "
                r"accuracy is $-0.003$ (permuted null $\approx 0.01$); across all 18 cells, the means are $0.638$ "
                r"and $0.046$. A cohort-clustered bootstrap confirms a positive gap of $+0.485$ (95\% CI $[+0.379, +0.662]$; "
                r"unconstrained $+0.464$), showing that reproducibility does not imply correctness."
                "\n\n"
                r"Using Gated Anchor Consensus (GAC), we test which components recover signal. Bipartite consensus "
                r"alone ($0.046$) and random feature gating ($0.046$ dense, $0.047$ bipartite) match ambient consensus "
                r"($0.037$). Bimodality-Gated Subspace Selection (BGSS) raises ARI to $0.217$ under bipartite consensus "
                r"($+0.169$ over matched random gating, 95\% CI $[+0.036, +0.310]$), driven by Leukemia and SRBCT, "
                r"but only to $0.077$ under dense consensus ($+0.031$), where performance is confounded by a degenerate "
                r"Leukemia result. Determinacy-based anchors add no benefit ($\Delta = +0.019$). Across 13 benchmarks "
                r"($3{,}000$ fits), omnibus differences are not significant (Friedman $p = 0.40$). Bipartite compression "
                r"reduces consensus-graph memory by $99.6\%$ at $N = 10^4$. Stability should be reported with null controls "
                r"and degeneracy audits, and marginal gating helps only when informative coordinates show detectable multimodality.}"
            )
            text = text[:s_abs] + new_abstract + text[close_brace+1:]

        # B. CONTRIBUTION 2: Proper CI wording (not "uncorrected 95% CI")
        old_c2 = (
            r"\item \textbf{A controlled decomposition of what recovers signal.} Using GAC as an experimental "
            r"vehicle, we cross gating (none, random, BGSS) with consensus type (dense, bipartite). Neither "
            r"bipartite consensus alone ($0.046$ vs. $0.037$) nor random gating ($0.046$ dense, $0.047$ bipartite) "
            r"improves materially on ambient consensus. BGSS raises ARI to $0.217$ under bipartite consensus "
            r"($+0.169$ over matched random gating, uncorrected 95\% CI $[+0.036, +0.310]$, Wilcoxon $p = 0.031$, $n = 6$) "
            r"but only to $0.077$ under dense consensus ($+0.031$, CI $[-0.062, +0.149]$), where performance is dragged down "
            r"by a degenerate Leukemia result. The gain is concentrated in Leukemia ($+0.398$) and SRBCT ($+0.447$), "
            r"and determinacy-based anchors add nothing measurable ($\Delta = +0.019$, 95\% CI $[-0.040, +0.082]$)."
        )
        new_c2 = (
            r"\item \textbf{A controlled decomposition of what recovers signal.} Using GAC as an experimental "
            r"vehicle, we cross gating (none, random, BGSS) with consensus type (dense, bipartite). Neither "
            r"bipartite consensus alone ($0.046$ vs. $0.037$) nor random gating ($0.046$ dense, $0.047$ bipartite) "
            r"improves materially on ambient consensus. BGSS raises ARI to $0.217$ under bipartite consensus "
            r"($+0.169$ over matched random gating, 95\% CI $[+0.036, +0.310]$, Wilcoxon $p = 0.031$ uncorrected for the three comparisons, $n = 6$) "
            r"but only to $0.077$ under dense consensus ($+0.031$, CI $[-0.062, +0.149]$), where performance is dragged down "
            r"by a degenerate Leukemia result. The gain is concentrated in Leukemia ($+0.398$) and SRBCT ($+0.447$), "
            r"and determinacy-based anchors add nothing measurable ($\Delta = +0.019$, 95\% CI $[-0.040, +0.082]$)."
        )
        if old_c2 in text:
            text = text.replace(old_c2, new_c2)

        # C. SECTION 6.2: Proper CI wording and Leukemia/Colon/SRBCT distinction
        old_s62 = (
            r"BGSS multimodality gating raises ARI to $0.217$ under bipartite consensus, an uncorrected paired gain of $+0.169$ over matched random gating (95\% cohort-clustered bootstrap CI $[+0.036, +0.310]$, "
            r"uncorrected Wilcoxon $W = 0.0, p = 0.0312, n = 6$), driven by Leukemia ($+0.398$) and SRBCT ($+0.447$). "
            r"By contrast, under dense consensus BGSS reaches $0.077$, adding only $+0.031$ over random dense gating (95\% CI $[-0.062, +0.149]$, "
            r"Wilcoxon $p = 1.0$), where dense consensus is confounded by base-clusterer instability on Leukemia."
        )
        new_s62 = (
            r"BGSS multimodality gating raises ARI to $0.217$ under bipartite consensus, a paired gain of $+0.169$ over matched random gating (95\% cohort-clustered bootstrap CI $[+0.036, +0.310]$, "
            r"Wilcoxon $W = 0.0, p = 0.0312$ uncorrected for the three comparisons, $n = 6$), driven by Leukemia ($+0.398$) and SRBCT ($+0.447$). "
            r"By contrast, under dense consensus BGSS reaches $0.077$, adding only $+0.031$ over random dense gating (95\% CI $[-0.062, +0.149]$, "
            r"Wilcoxon $p = 1.0$), where dense consensus is confounded by base-clusterer instability on Leukemia."
        )
        if old_s62 in text:
            text = text.replace(old_s62, new_s62)

        # D. SECTION 7.3: Issues 1, 2, 3, 4
        # Replace the entire Sec 7.3 paragraph
        s_73 = text.find(r"\input{gen/table12_factorial_decomposition.tex}")
        if s_73 != -1:
            e_73 = text.find(r"\input{gen/table13_component_contributions.tex}", s_73)
            assert e_73 != -1
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
                r"In an earlier draft of this benchmark, the random-gating baseline mistakenly cascaded BGSS filtering inside "
                r"the randomly drawn feature pool rather than taking the random features unranked; correcting this control arm "
                r"removed spurious signal inflation on Leukemia and SRBCT, lowering the random bipartite baseline from $0.155$ to $0.047$. "
                r"Random gating gives $0.046$ under dense consensus and $0.047$ under bipartite consensus with core anchors "
                r"($0.053$ with uniform anchors), none materially above ambient consensus. Against these controls, BGSS "
                r"adds $+0.169$ under bipartite consensus ($V_5$ vs. random; 95\% CI $[+0.036, +0.310]$; positive on all six cohorts, "
                r"Wilcoxon $W = 0.0, p = 0.031$ uncorrected for the three comparisons, $n = 6$) and $+0.145$ with uniform anchors "
                r"($V_4$ vs. random; CI $[+0.006, +0.315]$, $p = 0.31$), but only $+0.031$ under dense consensus "
                r"($V_2$ vs. random; CI $[-0.062, +0.149]$, $p = 1.0$). The dense-consensus arm was added post hoc to complete "
                r"the design. With six cohorts, the smallest attainable two-sided Wilcoxon $p$ is $0.031$, and these tests are not "
                r"corrected for the three comparisons, so we treat the BGSS effect as suggestive. Most of the $+0.169$ mean gain "
                r"is concentrated in two cohorts: Leukemia ($+0.398$) and SRBCT ($+0.447$), while the other four cohorts show small "
                r"differences spanning $+0.004$ to $+0.078$."
                "\n\n"
                r"On Leukemia, BGSS gating actually hurts dense consensus: while ambient dense consensus (V0) achieves a stable "
                r"$+0.162$ ($29/30$ seeds positive), BGSS dense consensus (V2) drops to $0.042$ because in $23$ of $30$ seeds ($76.7\%$), "
                r"base K-Means fits latch onto a small cluster ($N = 9\text{--}16$) unrelated to the diagnostic classes, "
                r"driving ARI below zero (mean $-0.044$ across those 23 seeds). Only $7$ of $30$ seeds ($23.3\%$) align with diagnostic "
                r"classes (mean ARI $+0.326$, up to $+0.459$). Bipartite anchor consensus with random-subspace ensembling (V5) reduces "
                r"this collapse rate from $23/30$ ($76.7\%$) to $8/30$ ($26.7\%$), with $22$ of $30$ seeds exceeding $\text{ARI} > 0.50$ "
                r"(up to $1.000$) and reaching a subgroup mean of $0.600$. Conversely, on Colon and SRBCT, BGSS dense consensus ($V_2$) "
                r"is competitive or superior against the matched \emph{dense} random arm ($+0.084$ vs. $-0.006$ on Colon, and $+0.333$ "
                r"vs. $+0.055$ on SRBCT), confirming that the weak overall $V_2$ mean ($0.077$) is driven by the Leukemia collapse rather "
                r"than a failure of BGSS across all cohorts. Determinacy-based anchors give no measurable benefit ($V_5 - V_4 = +0.019$, "
                r"CI $[-0.040, +0.082]$, $p = 0.84$). Table~\ref{tab:component_contributions} reports the individual knockout contributions."
                "\n\n"
            )
            end_input_12 = s_73 + len(r"\input{gen/table12_factorial_decomposition.tex}")
            text = text[:end_input_12] + new_sec73_body + text[e_73:]

        # E. SECTION 8.1: Issue 3 & 4
        old_s81 = (
            r"BGSS multimodality gating raises performance substantially in combination with bipartite consensus "
            r"($+0.169$ over matched random gating, 95\% CI $[+0.036, +0.310]$, uncorrected Wilcoxon $p = 0.031$, $n = 6$), "
            r"while adding only $+0.031$ under dense consensus (CI $[-0.062, +0.149]$), where the dense arm is confounded "
            r"by a degenerate Leukemia result."
        )
        new_s81 = (
            r"BGSS multimodality gating raises performance substantially in combination with bipartite consensus "
            r"($+0.169$ over matched random gating, 95\% CI $[+0.036, +0.310]$, Wilcoxon $p = 0.031$ uncorrected for the three comparisons, $n = 6$), "
            r"while adding only $+0.031$ under dense consensus (CI $[-0.062, +0.149]$), where the dense arm is confounded "
            r"by a degenerate Leukemia result (though $V_2$ outperforms the dense random arm on Colon and SRBCT)."
        )
        if old_s81 in text:
            text = text.replace(old_s81, new_s81)

        # F. SECTION 9 (Conclusion): Issue 4
        old_s9 = (
            r"Bimodality-Gated Subspace Selection adds $+0.169$ over matched random gating under bipartite consensus "
            r"(uncorrected 95\% CI $[+0.036, +0.310]$, uncorrected Wilcoxon $p = 0.031$, $n = 6$) but only $+0.031$ under "
            r"dense consensus (CI $[-0.062, +0.149]$)"
        )
        new_s9 = (
            r"Bimodality-Gated Subspace Selection adds $+0.169$ over matched random gating under bipartite consensus "
            r"(95\% CI $[+0.036, +0.310]$, Wilcoxon $p = 0.031$ uncorrected for the three comparisons, $n = 6$) but only $+0.031$ under "
            r"dense consensus (CI $[-0.062, +0.149]$)"
        )
        if old_s9 in text:
            text = text.replace(old_s9, new_s9)

        p.write_text(text, encoding="utf-8")
        print(f"Applied final submission polish to {p}")

if __name__ == "__main__":
    main()
