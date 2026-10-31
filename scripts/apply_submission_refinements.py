# -*- coding: utf-8 -*-
from pathlib import Path
import re

def main():
    root = Path(__file__).resolve().parent.parent

    # 1. Update Table 2 / Table 3 caption
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
            "Daggers ($^\\dagger$) mark degenerate partitions failing amended Decision Rule~(i') non-degeneracy condition (smallest cluster holds $< 5\\%$ of the subsample in $> 10\\%$ of subsamples).",
            "Daggers ($^\\dagger$) mark degenerate partitions failing amended Decision Rule~(i') non-degeneracy condition (added post hoc: smallest cluster holds $< 5\\%$ of the subsample in $> 10\\%$ of subsamples)."
        )
        tf.write_text(c, encoding="utf-8")
        print(f"Updated caption in {tf}")

    # 2. Update main.tex targets
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

        # A. ABSTRACT: Soften BGSS & mention multiplicity + per-cohort breakdown
        old_abs_bgss = (
            r"BGSS adds $+0.169$ over matched random gating under bipartite consensus (95\% CI $[+0.036, +0.310]$) "
            r"but only $+0.031$ under dense consensus (CI $[-0.062, +0.149]$), so the gain depends on combining "
            r"multimodality gating with anchor-graph consensus and is driven by two cohorts."
        )
        new_abs_bgss = (
            r"BGSS adds $+0.169$ over matched random gating under bipartite consensus (uncorrected 95\% CI $[+0.036, +0.310]$, "
            r"Wilcoxon $p = 0.031$, $n = 6$) but only $+0.031$ under dense consensus (CI $[-0.062, +0.149]$); "
            r"the observed benefit thus depends on consensus type, and the dense arm is confounded by a degenerate Leukemia result. "
            r"The gain is driven by two cohorts (Leukemia and SRBCT, accounting for $+0.398$ and $+0.447$ of the difference, "
            r"while the other four span $+0.004$ to $+0.078$)."
        )
        if old_abs_bgss in text:
            text = text.replace(old_abs_bgss, new_abs_bgss)

        # B. INTRODUCTION: Tail of paragraph 1
        old_intro_tail = (
            "Our results show that high subsample stability does not imply correctness on these cohorts, "
            "that random feature gating and anchor-graph compression each fail to improve accuracy on their own, "
            "and that marginal bimodality gating helps only in combination with bipartite consensus and only "
            "where informative coordinates are detectably multimodal."
        )
        new_intro_tail = (
            "Our results show that high subsample stability does not imply correctness on these cohorts, "
            "that random feature gating and anchor-graph compression each fail to improve accuracy on their own, "
            "and that the observed benefit of marginal bimodality gating depends on consensus type "
            "(with the dense arm confounded by a degenerate Leukemia result) and requires informative coordinates "
            "to be detectably multimodal."
        )
        if old_intro_tail in text:
            text = text.replace(old_intro_tail, new_intro_tail)

        # C. CONTRIBUTION 2: Soften & caveat
        old_contrib2 = (
            r"\item \textbf{A controlled decomposition of what recovers signal.} Using GAC as an experimental "
            r"vehicle, we cross gating (none, random, BGSS) with consensus type (dense, bipartite). Neither "
            r"bipartite consensus alone ($0.046$ vs. $0.037$) nor random gating ($0.046$ dense, $0.047$ bipartite) "
            r"improves materially on ambient consensus. BGSS raises ARI to $0.217$ under bipartite consensus "
            r"($+0.169$ over matched random gating, 95\% CI $[+0.036, +0.310]$) but only to $0.077$ under dense "
            r"consensus ($+0.031$, CI $[-0.062, +0.149]$). The gain is concentrated in Leukemia and SRBCT, "
            r"and determinacy-based anchors add nothing measurable ($\Delta = +0.019$, 95\% CI $[-0.040, +0.082]$)."
        )
        new_contrib2 = (
            r"\item \textbf{A controlled decomposition of what recovers signal.} Using GAC as an experimental "
            r"vehicle, we cross gating (none, random, BGSS) with consensus type (dense, bipartite). Neither "
            r"bipartite consensus alone ($0.046$ vs. $0.037$) nor random gating ($0.046$ dense, $0.047$ bipartite) "
            r"improves materially on ambient consensus. BGSS raises ARI to $0.217$ under bipartite consensus "
            r"($+0.169$ over matched random gating, uncorrected 95\% CI $[+0.036, +0.310]$, Wilcoxon $p = 0.031$, $n = 6$) "
            r"but only to $0.077$ under dense consensus ($+0.031$, CI $[-0.062, +0.149]$), where performance is dragged down "
            r"by a degenerate Leukemia result. The gain is concentrated in Leukemia ($+0.398$) and SRBCT ($+0.447$), "
            r"and determinacy-based anchors add nothing measurable ($\Delta = +0.019$, 95\% CI $[-0.040, +0.082]$)."
        )
        if old_contrib2 in text:
            text = text.replace(old_contrib2, new_contrib2)

        # D. SECTION 5.2: Seed schedule disclosure
        old_sec52_intro = (
            r"Table~\ref{tab:benchmark_ari} presents the comprehensive empirical ARI results across all 3{,}000 model fits "
            r"(30 seeds on high-$D$ cohorts, 10 seeds on others), with distribution boxplots in Fig.~\ref{fig:benchmark_distributions}."
        )
        new_sec52_intro = (
            r"Table~\ref{tab:benchmark_ari} presents the comprehensive empirical ARI results across all 3{,}000 model fits "
            r"(30 seeds on high-$D$ cohorts, 10 seeds on others), with distribution boxplots in Fig.~\ref{fig:benchmark_distributions}. "
            r"Omnibus benchmark fits evaluate seeds $\{42, \dots, 71\}$ on the high-$D$ cohorts and $\{42, \dots, 51\}$ on other datasets, "
            r"whereas the modular ablation and factorial experiments in Section~\ref{sec:ablation} evaluate seeds $\{0, \dots, 29\}$."
        )
        if old_sec52_intro in text:
            text = text.replace(old_sec52_intro, new_sec52_intro)

        # E. SECTION 6.2: Soften & mention uncorrected test
        old_sec62 = (
            r"Evaluating BGSS directly against matched random subspace gating ($|\mathcal{F}_{\text{active}}| = \lfloor \alpha D \rfloor$ "
            r"across 30 seeds $\{0, \dots, 29\}$ on the six cohorts) shows that random feature gating yields a subgroup "
            r"mean of $0.047$ under bipartite consensus and $0.046$ under dense consensus, performing comparably to ambient "
            r"consensus ($0.046$ bipartite, $0.037$ dense). BGSS multimodality gating raises ARI to $0.217$ under bipartite "
            r"consensus, a paired gain of $+0.169$ over matched random gating (95\% cohort-clustered bootstrap CI $[+0.036, +0.310]$, "
            r"Wilcoxon $W = 0.0, p = 0.0312$). By contrast, under dense consensus BGSS reaches $0.077$, adding only $+0.031$ "
            r"over random dense gating (95\% CI $[-0.062, +0.149]$, Wilcoxon $p = 1.0$), demonstrating that multimodality "
            r"gating and bipartite anchor consensus interact to recover signal."
        )
        new_sec62 = (
            r"Evaluating BGSS directly against matched random subspace gating ($|\mathcal{F}_{\text{active}}| = \lfloor \alpha D \rfloor$ "
            r"across 30 seeds $\{0, \dots, 29\}$ on the six cohorts) shows that random feature gating yields a subgroup "
            r"mean of $0.047$ under bipartite consensus and $0.046$ under dense consensus, performing comparably to ambient "
            r"consensus ($0.046$ bipartite, $0.037$ dense). BGSS multimodality gating raises ARI to $0.217$ under bipartite "
            r"consensus, an uncorrected paired gain of $+0.169$ over matched random gating (95\% cohort-clustered bootstrap CI $[+0.036, +0.310]$, "
            r"uncorrected Wilcoxon $W = 0.0, p = 0.0312, n = 6$), driven by Leukemia ($+0.398$) and SRBCT ($+0.447$). "
            r"By contrast, under dense consensus BGSS reaches $0.077$, adding only $+0.031$ over random dense gating (95\% CI $[-0.062, +0.149]$, "
            r"Wilcoxon $p = 1.0$), where dense consensus is confounded by base-clusterer instability on Leukemia."
        )
        if old_sec62 in text:
            text = text.replace(old_sec62, new_sec62)

        # F. SECTION 7.3: Detailed Leukemia collapse numbers + methods disclosure + cohort breakdown
        old_sec73_body = (
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
        )
        new_sec73_body = (
            r"To separate the effect of multimodality gating from that of feature subsampling, we evaluated matched "
            r"random gating (the same pool size, $\lfloor \alpha D \rfloor$, drawn at random) over the same 30 seeds. "
            r"In an earlier draft of this benchmark, the random-gating baseline mistakenly cascaded BGSS filtering inside "
            r"the randomly drawn feature pool rather than taking the random features unranked; correcting this control arm "
            r"removed spurious signal inflation on Leukemia and SRBCT, lowering the random bipartite baseline from $0.155$ to $0.047$. "
            r"Random gating gives $0.046$ under dense consensus and $0.047$ under bipartite consensus with core anchors "
            r"($0.053$ with uniform anchors), none materially above ambient consensus. Against these controls, BGSS "
            r"adds $+0.169$ under bipartite consensus ($V_5$ vs. random; uncorrected 95\% CI $[+0.036, +0.310]$; positive on all six cohorts, "
            r"Wilcoxon $W = 0.0, p = 0.031, n = 6$) and $+0.145$ with uniform anchors ($V_4$ vs. random; CI $[+0.006, +0.315]$, $p = 0.31$), "
            r"but only $+0.031$ under dense consensus ($V_2$ vs. random; CI $[-0.062, +0.149]$, $p = 1.0$). The dense-consensus "
            r"arm was added post hoc to complete the design. With six cohorts, the smallest attainable two-sided Wilcoxon "
            r"$p$ is $0.031$, and these tests are not corrected for the three comparisons, so we treat the BGSS effect "
            r"as suggestive. Most of the $+0.169$ mean gain is concentrated in two cohorts: Leukemia ($+0.398$) and SRBCT ($+0.447$), "
            r"while the other four cohorts show small differences spanning $+0.004$ to $+0.078$."
            "\n\n"
            r"On Leukemia, BGSS gating actually hurts dense consensus: while ambient dense consensus (V0) achieves a stable "
            r"$+0.162$ ($29/30$ seeds positive), BGSS dense consensus (V2) drops to $0.042$ because in $23$ of $30$ seeds ($76.7\%$), "
            r"base K-Means fits latch onto an uninformative minority cluster ($N = 9\text{--}16$) that cuts across diagnostic classes, "
            r"driving ARI below zero (mean $-0.044$ across those 23 seeds). Only $7$ of $30$ seeds ($23.3\%$) align with diagnostic "
            r"classes (mean ARI $+0.326$, up to $+0.459$). Bipartite anchor consensus with random-subspace ensembling (V5) avoids this "
            r"failure mode and recovers the diagnostic classes reliably, reaching $0.600$ ($22/30$ seeds exceeding $0.50$, up to $1.000$). "
            r"Determinacy-based anchors give no measurable benefit ($V_5 - V_4 = +0.019$, CI $[-0.040, +0.082]$, $p = 0.84$). "
            r"Table~\ref{tab:component_contributions} reports the individual knockout contributions."
        )
        if old_sec73_body in text:
            text = text.replace(old_sec73_body, new_sec73_body)

        # G. SECTION 8.1: Soften & caveat
        old_sec81_gac = (
            r"BGSS multimodality gating raises performance substantially only in combination with bipartite consensus "
            r"($+0.169$ over matched random gating, 95\% CI $[+0.036, +0.310]$, uncorrected Wilcoxon $p = 0.031$), "
            r"while adding only $+0.031$ under dense consensus (CI $[-0.062, +0.149]$). Determinacy-based anchor selection yields "
            r"no measurable benefit ($\Delta = +0.019$, 95\% CI $[-0.040, +0.082]$). Across 13 multi-domain benchmarks, the twelve "
            r"clustering methods are statistically indistinguishable (Friedman $p = 0.40, \text{CD} = 4.62$). The performance "
            r"advantage of GAC is concentrated in Leukemia ($0.600$) and SRBCT ($0.546$), where informative coordinates exhibit "
            r"detectable marginal multimodality, and BGSS recovers 27 of the 50 diagnostic Golub markers ($54.0\%$) without supervision."
        )
        new_sec81_gac = (
            r"BGSS multimodality gating raises performance substantially in combination with bipartite consensus "
            r"($+0.169$ over matched random gating, 95\% CI $[+0.036, +0.310]$, uncorrected Wilcoxon $p = 0.031$, $n = 6$), "
            r"while adding only $+0.031$ under dense consensus (CI $[-0.062, +0.149]$), where the dense arm is confounded "
            r"by a degenerate Leukemia result. The benefit we observe thus depends on consensus type. Determinacy-based anchor "
            r"selection yields no measurable benefit ($\Delta = +0.019$, 95\% CI $[-0.040, +0.082]$). Across 13 multi-domain "
            r"benchmarks, the twelve clustering methods are statistically indistinguishable (Friedman $p = 0.40, \text{CD} = 4.62$). "
            r"The performance advantage of GAC is concentrated in Leukemia ($+0.398$) and SRBCT ($+0.447$), where informative coordinates "
            r"exhibit detectable marginal multimodality, and BGSS recovers 27 of the 50 diagnostic Golub markers ($54.0\%$) without supervision."
        )
        if old_sec81_gac in text:
            text = text.replace(old_sec81_gac, new_sec81_gac)

        # H. SECTION 8.3 (Limitations): Few cohorts
        old_few_cohorts = (
            r"\item \textbf{Few cohorts and uncorrected tests.} High-dimensional inference rests on $n = 6$ biomedical "
            r"cohorts. This sample size restricts statistical power, the BGSS effect rests on two cohorts (Leukemia and "
            r"SRBCT), and pairwise Wilcoxon comparisons are uncorrected across the three gating tests, rendering the "
            r"observed $+0.169$ gain and interaction ($p \approx 0.16$) suggestive rather than definitive."
        )
        new_few_cohorts = (
            r"\item \textbf{Few cohorts and uncorrected tests.} High-dimensional inference rests on $n = 6$ biomedical "
            r"cohorts. This sample size restricts statistical power: the $+0.169$ gain rests primarily on two cohorts "
            r"(Leukemia at $+0.398$ and SRBCT at $+0.447$, versus $+0.004$ to $+0.078$ on the other four), and pairwise "
            r"Wilcoxon comparisons are uncorrected across the three gating tests ($p = 0.031$ uncorrected, $n=6$), "
            r"rendering the observed gain and interaction ($p \approx 0.16$) suggestive rather than definitive."
        )
        if old_few_cohorts in text:
            text = text.replace(old_few_cohorts, new_few_cohorts)

        # I. SECTION 9 (Conclusion): Soften BGSS & mention uncorrected p + cohort breakdown
        old_sec9_bgss = (
            r"Bimodality-Gated Subspace Selection adds $+0.169$ over matched random gating under bipartite consensus "
            r"(95\% CI $[+0.036, +0.310]$, uncorrected Wilcoxon $p = 0.031$), but only $+0.031$ under dense consensus "
            r"(CI $[-0.062, +0.149]$), demonstrating that the gain depends on combining multimodality gating with "
            r"bipartite anchor consensus. Determinacy-based anchor selection gives no measurable benefit "
            r"($\Delta = +0.019$, 95\% CI $[-0.040, +0.082]$). The gains concentrate in Leukemia ($0.600$) and SRBCT ($0.546$), "
            r"where informative coordinates are detectably multimodal."
        )
        new_sec9_bgss = (
            r"Bimodality-Gated Subspace Selection adds $+0.169$ over matched random gating under bipartite consensus "
            r"(uncorrected 95\% CI $[+0.036, +0.310]$, uncorrected Wilcoxon $p = 0.031$, $n = 6$) but only $+0.031$ under "
            r"dense consensus (CI $[-0.062, +0.149]$), where the dense arm is confounded by a degenerate Leukemia result; "
            r"the observed benefit thus depends on consensus type. Determinacy-based anchor selection gives no measurable benefit "
            r"($\Delta = +0.019$, 95\% CI $[-0.040, +0.082]$). The gains concentrate in Leukemia ($+0.398$) and SRBCT ($+0.447$), "
            r"where informative coordinates are detectably multimodal, while the other four cohorts show smaller changes "
            r"($+0.004$ to $+0.078$)."
        )
        if old_sec9_bgss in text:
            text = text.replace(old_sec9_bgss, new_sec9_bgss)

        p.write_text(text, encoding="utf-8")
        print(f"Applied refinements to {p}")

if __name__ == "__main__":
    main()
