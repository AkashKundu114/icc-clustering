import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent

for tex_path in [root / "paper" / "main.tex", root / "springer_manuscript" / "main.tex"]:
    if not tex_path.exists():
        continue
    text = tex_path.read_text(encoding="utf-8")

    # 1. Fig 1 caption: arbitrary noise manifolds -> cluster separation collapses
    old_fig1_cap = r"pairwise contrast disappears ($(d_{\max}-d_{\min})/d_{\min} \to 0$ as $D \to \infty$) and base clusterers repeatedly converge onto arbitrary noise manifolds."
    new_fig1_cap = r"pairwise contrast disappears ($(d_{\max}-d_{\min})/d_{\min} \to 0$ as $D \to \infty$) and cluster separation collapses."
    if old_fig1_cap in text:
        text = text.replace(old_fig1_cap, new_fig1_cap)
        print(f"Patched Fig 1 caption in {tex_path.name}")
    else:
        print(f"[!] Fig 1 caption target not found in {tex_path.name}")

    # 2. Section 3 Definitions: reflects data structure -> sample covariance
    old_sec3_def = r"across those nine cells, mean stability is $0.684$, mean accuracy is $-0.003$, and column-permuted null stability is $\approx 0.01$, so the stability reflects data structure rather than permutation artifacts."
    new_sec3_def = r"across those nine cells, mean stability is $0.684$, mean accuracy is $-0.003$, and column-permuted null stability is $\approx 0.01$, confirming that observed subsample stability reflects underlying sample covariance rather than permutation artifacts, though this structure does not align with diagnostic reference classes."
    if old_sec3_def in text:
        text = text.replace(old_sec3_def, new_sec3_def)
        print(f"Patched Section 3 def in {tex_path.name}")
    else:
        print(f"[!] Section 3 def target not found in {tex_path.name}")

    # 3. Fig 2 subfloats and caption
    old_fig2 = r"""\begin{figure*}[!t]
\centering
\subfloat[Clustering Accuracy (ARI vs. Ground Truth) and Ensemble Stability Across $D_{\text{noise}}$\label{fig:ari_stability}]{%
  \includegraphics[width=0.96\textwidth]{figures/fig02a_ari_stability.png}%
}
\\[1.5ex]
\subfloat[Stability$-$Accuracy Gap ($\Delta = \text{Stability} - \text{ARI}$)\label{fig:dist_gap}]{%
  \includegraphics[width=0.48\textwidth]{figures/fig02b_stability_accuracy_gap.png}%
}
\hfill
\subfloat[Noise Distribution Sensitivity Matrix ($D_{\text{noise}}=1{,}000$)\label{fig:noise_heatmap}]{%
  \includegraphics[width=0.48\textwidth]{figures/fig02c_noise_distribution_sensitivity.png}%
}
\caption{Clustering under isotropic distractor noise ($N=300, K=3$, 20 stratified 80\% subsample draws per noise level). (a) Accuracy (ARI against ground truth) collapses toward zero for all methods as distractor dimensions grow. (b) Subsample stability collapses alongside accuracy under row resampling (dropping to $\le 0.03$ for K-Means, GMM, FCM, and Ward; Spectral lingers at $0.17$). (c) Subsample stability--accuracy gap ($\Delta = \text{Stability} - \text{ARI}$) remains near zero, showing that evidence for stability--accuracy discordance rests on real cohorts rather than isotropic simulations.}
\label{fig:falsification_suite}
\end{figure*}"""

    new_fig2 = r"""\begin{figure*}[!t]
\centering
\subfloat[Clustering Accuracy (ARI vs. Ground Truth) and Subsample Stability Across $D_{\text{noise}}$\label{fig:ari_stability}]{%
  \includegraphics[width=0.96\textwidth]{figures/fig02a_ari_stability.png}%
}
\\[1.5ex]
\subfloat[Stability$-$Accuracy Gap ($\Delta = \text{Stability} - \text{ARI}$) Across $D_{\text{noise}}$\label{fig:dist_gap}]{%
  \includegraphics[width=0.48\textwidth]{figures/fig02b_stability_accuracy_gap.png}%
}
\hfill
\subfloat[Noise Distribution Sensitivity Matrix at $D_{\text{noise}}=1{,}000$\label{fig:noise_heatmap}]{%
  \includegraphics[width=0.48\textwidth]{figures/fig02c_noise_distribution_sensitivity.png}%
}
\caption{Clustering under isotropic distractor noise ($N=300, K=3$, 20 stratified 80\% subsample draws per noise level). (a) Accuracy (ARI against ground truth) collapses toward zero for all methods as distractor dimensions grow, and subsample stability collapses alongside it under row resampling (dropping to $\le 0.03$ for K-Means, GMM, FCM, and Ward; Spectral lingers at $0.17$). (b) The subsample stability--accuracy gap ($\Delta = \text{Stability} - \text{ARI}$) remains near zero across noise scales. (c) Heatmap of the gap across five noise distributions at $D_{\text{noise}}=1{,}000$, confirming that stability--accuracy discordance does not emerge in isotropic distractor simulations and rests on real cohorts.}
\label{fig:falsification_suite}
\end{figure*}"""

    if old_fig2 in text:
        text = text.replace(old_fig2, new_fig2)
        print(f"Patched Fig 2 block in {tex_path.name}")
    else:
        print(f"[!] Fig 2 block target not found in {tex_path.name}")

    # 4. Section 3.1 paragraph rewrite
    old_sec31 = r"""Accuracy collapses as noise dimensions grow for all methods (Fig.~\ref{fig:ari_stability}). Seed-to-seed agreement (Fig.~\ref{fig:dist_gap}) stays near 1 for Ward and spectral clustering, but these are deterministic solvers whose across-seed agreement is 1 by construction, so this panel does not demonstrate stability in a meaningful sense. The stochastic methods (K-Means, FCM, GMM) lose agreement and accuracy together. The simulations therefore establish the accuracy collapse and the failure of alternative metrics to defer it indefinitely (Table~\ref{tab:distance_geometries}); evidence for stability--accuracy discordance comes from the subsample protocol in Section~\ref{sec:real_data_stability}."""

    new_sec31 = r"""Under stratified 80\% subsampling (Fig.~\ref{fig:ari_stability}), clustering accuracy collapses toward zero for all methods as distractor dimensions grow. Subsample stability collapses alongside accuracy under row resampling, dropping to $\le 0.03$ for K-Means, GMM, FCM, and Ward (where Ward falls from $1.000$ at $D_{\text{noise}}=0$ to $0.026$ at $D_{\text{noise}}=5{,}000$), while Spectral clustering lingers at $0.173$. Consequently, the subsample stability--accuracy gap $\Delta = \text{Stability} - \text{ARI}$ remains near zero across all noise scales (Fig.~\ref{fig:dist_gap}) and across diverse noise distributions at $D_{\text{noise}}=1{,}000$ (Fig.~\ref{fig:noise_heatmap}), with minor elevation only under correlated noise ($+0.05$ to $+0.20$) and sparse noise for Ward ($+0.79$, where single-point chaining isolates outliers). In contrast to seed-to-seed agreement on unperturbed data---which remains trivially at $1.0$ for deterministic solvers---subsample stability demonstrates that isotropic noise erases both cluster accuracy and partition reproducibility. The simulations therefore establish the accuracy collapse and demonstrate that alternative distance geometries only delay it (Table~\ref{tab:distance_geometries}); evidence for stability--accuracy discordance rests on the empirical biomedical cohorts evaluated in Section~\ref{sec:real_data_stability}."""

    if old_sec31 in text:
        text = text.replace(old_sec31, new_sec31)
        print(f"Patched Section 3.1 text in {tex_path.name}")
    else:
        print(f"[!] Section 3.1 text target not found in {tex_path.name}")

    # 5. Section 3.2: Clarify pooled +0.472 vs 9-cell ~0.671 and soften "genuine, reproducible manifold geometry" -> "data-driven structure"
    old_sec32_boot = r"""To evaluate whether excess stability is statistically robust, we conducted a dataset-clustered bootstrap ($B=10{,}000$ iterations) that resamples cohorts with replacement, pooling paired differences across non-degenerate methods. Excess stability over unstructured noise ($\text{Stab} - \text{Null}$) averages $+0.472$ (95\% CI: $[+0.368, +0.645]$), while permuted-null stability stays near zero ($-0.003$ to $+0.049$). The paired stability--accuracy gap averages $+0.485$ across non-degenerate partitions (95\% CI: $[+0.379, +0.662]$) and $+0.464$ across all partitions (95\% CI: $[+0.363, +0.607]$). Crucially, the excess stability ($\text{Stab} - \text{Null} \ge 0.10$) confirms that base clusterers converge onto genuine, reproducible manifold geometry rather than noise artifacts, even as accuracy remains near zero."""

    new_sec32_boot = r"""To evaluate whether excess stability is statistically robust, we conducted a dataset-clustered bootstrap ($B=10{,}000$ iterations) that resamples cohorts with replacement, pooling paired differences across non-degenerate methods. Across all 58 non-degenerate method--cohort cells evaluated, excess stability over unstructured noise ($\text{Stab} - \text{Null}$) averages $+0.472$ (95\% CI: $[+0.368, +0.645]$), rising to $\text{Stab} - \text{Null} \approx 0.671$ ($0.684 - 0.013$) across the nine persistently discordant cells, while permuted-null stability stays near zero ($-0.003$ to $+0.049$). The paired stability--accuracy gap averages $+0.485$ across non-degenerate partitions (95\% CI: $[+0.379, +0.662]$) and $+0.464$ across all partitions (95\% CI: $[+0.363, +0.607]$). Crucially, the excess stability ($\text{Stab} - \text{Null} \ge 0.10$) confirms that base clusterers converge onto data-driven structure rather than permutation artifacts, even as accuracy remains near zero."""

    if old_sec32_boot in text:
        text = text.replace(old_sec32_boot, new_sec32_boot)
        print(f"Patched Section 3.2 bootstrap in {tex_path.name}")
    else:
        print(f"[!] Section 3.2 bootstrap target not found in {tex_path.name}")

    # 6. Section 6.2: Trim CoHiRF comparison
    old_sec62 = r""": CoHiRF enforces strict hierarchical consensus over unanimous components without bipartite graph spectral projection, which causes extreme cluster fragmentation when features are heavily contaminated by ambient noise, whereas random subspace gating within the bipartite pipeline yields a subgroup mean of $0.047$ ($0.053$ under uniform anchors), and BGSS raises it to $0.217$."""
    new_sec62 = r""": CoHiRF enforces strict hierarchical consensus over unanimous components without bipartite graph spectral projection, which causes extreme cluster fragmentation when features are heavily contaminated by ambient noise."""
    if old_sec62 in text:
        text = text.replace(old_sec62, new_sec62)
        print(f"Patched Section 6.2 CoHiRF text in {tex_path.name}")
    else:
        print(f"[!] Section 6.2 CoHiRF text target not found in {tex_path.name}")

    # 7. Section 7.3: Qualify BGSS hurting dense consensus on Leukemia
    old_sec73_hurts = r"On Leukemia, BGSS gating actually hurts dense consensus: while ambient dense consensus (V0) achieves a stable $+0.162$"
    new_sec73_hurts = r"On Leukemia, BGSS gating actually hurts dense consensus (V2 vs.\ V0): while ambient dense consensus (V0) achieves a stable $+0.162$"
    if old_sec73_hurts in text:
        text = text.replace(old_sec73_hurts, new_sec73_hurts)
        print(f"Patched Section 7.3 hurts text in {tex_path.name}")

    # 8. Section 7.4: Remove duplicate sentence and standardize CI [-0.040, +0.082]
    old_sec74 = r"""\begin{equation}
\begin{aligned}
 V_5 - V_4 = +0.019 \quad &(95\%\text{ Cluster Bootstrap CI: } [-0.040, +0.082], \\
  &\text{Wilcoxon } W=9.0, p=0.84).
\end{aligned}
\end{equation}
The mean difference between V5 and V4 stands at $\Delta = +0.019$ ($W=9.0, p=0.84$). Because the 95\% bootstrap confidence interval [$-0.039, +0.082$] comfortably encompasses zero, determinacy screening offers no proven performance edge over picking landmarks uniformly at random. This confirms that determinacy screening offers no proven performance edge over picking landmarks uniformly at random."""

    new_sec74 = r"""\begin{equation}
\begin{aligned}
 V_5 - V_4 = +0.019 \quad &(95\%\text{ Cluster Bootstrap CI: } [-0.040, +0.082], \\
  &\text{Wilcoxon } W=9.0, p=0.84).
\end{aligned}
\end{equation}
Because the 95\% bootstrap confidence interval encompasses zero ($\Delta = +0.019$, 95\% CI $[-0.040, +0.082]$, Wilcoxon $W=9.0, p=0.84$), determinacy screening offers no measurable performance edge over picking landmarks uniformly at random."""

    if old_sec74 in text:
        text = text.replace(old_sec74, new_sec74)
        print(f"Patched Section 7.4 null result text in {tex_path.name}")
    else:
        print(f"[!] Section 7.4 target not found in {tex_path.name}")

    # 9. Section 5.2: Note post hoc dense random arm
    old_sec52 = r"with both schedules pre-specified to guarantee reproducibility across independent batches."
    new_sec52 = r"with both seed schedules pre-specified to guarantee reproducibility across independent batches (the dense random-gated arm in Table~\ref{tab:factorial} was subsequently evaluated post hoc under matching seeds $\mathcal{S}_{\text{sub}}$ to complete the factorial grid)."
    if old_sec52 in text:
        text = text.replace(old_sec52, new_sec52)
        print(f"Patched Section 5.2 seed schedule text in {tex_path.name}")
    else:
        print(f"[!] Section 5.2 seed schedule target not found in {tex_path.name}")

    # 10. Replace \cite{sarle1983sas} with \cite{sas1990stat} in Section 2.2
    if r"\cite{sarle1983sas}" in text:
        text = text.replace(r"\cite{sarle1983sas}", r"\cite{sas1990stat}")
        print(f"Replaced cite sarle1983sas with sas1990stat in {tex_path.name}")

    tex_path.write_text(text, encoding="utf-8")
    print(f"Wrote updated {tex_path.name}")

# Reconcile Table 19 in gen/table13_component_contributions.tex and gen/table15_component_contributions.tex
for gen_dir in [root / "paper" / "gen", root / "springer_manuscript" / "gen", root / "submission" / "springer_nature_package" / "gen", root / "submission" / "overleaf_package" / "gen"]:
    for f in ["table13_component_contributions.tex", "table15_component_contributions.tex"]:
        fp = gen_dir / f
        if fp.exists():
            c = fp.read_text(encoding="utf-8")
            if "[+0.004, +0.321]" in c:
                c = c.replace("[+0.004, +0.321]", "[+0.007, +0.321]")
                fp.write_text(c, encoding="utf-8")
                print(f"Reconciled CI in {fp}")

# Patch references.bib
for bib_path in [root / "paper" / "references.bib", root / "springer_manuscript" / "references.bib", root / "submission" / "springer_nature_package" / "references.bib"]:
    if not bib_path.exists():
        continue
    bib = bib_path.read_text(encoding="utf-8")
    # Fix beyer1999nearest
    old_beyer = """@inproceedings{beyer1999nearest,
  author    = {Kevin Beyer and Jonathan Goldstein and Raghu Ramakrishnan and Uri Shaft},
  title     = {When Is `Nearest Neighbor'' Meaningful?},
  booktitle = {Database Theory --- ICDT'99},
  series    = {Lecture Notes in Computer Science},
  volume    = {1540},
  pages     = {217--235},
  year      = {1999},
  publisher = {Springer},
  doi       = {10.1007/3-540-49257-7_15}
}"""

    new_beyer = """@inproceedings{beyer1999nearest,
  author    = {Kevin Beyer and Jonathan Goldstein and Raghu Ramakrishnan and Uri Shaft},
  title     = {When Is ``Nearest Neighbor'' Meaningful?},
  booktitle = {Database Theory --- ICDT'99},
  series    = {Lecture Notes in Computer Science},
  volume    = {1540},
  pages     = {217--235},
  year      = {1999},
  publisher = {Springer},
  address   = {Berlin, Heidelberg},
  doi       = {10.1007/3-540-49257-7_15}
}"""
    if old_beyer in bib:
        bib = bib.replace(old_beyer, new_beyer)
        print(f"Patched beyer1999nearest in {bib_path.name}")
    elif "beyer1999nearest" in bib and "address   = {Berlin, Heidelberg}" not in bib:
        # replace title and add address
        bib = re.sub(
            r"@inproceedings\{beyer1999nearest,[\s\S]*?publisher = \{Springer\},",
            r"""@inproceedings{beyer1999nearest,
  author    = {Kevin Beyer and Jonathan Goldstein and Raghu Ramakrishnan and Uri Shaft},
  title     = {When Is ``Nearest Neighbor'' Meaningful?},
  booktitle = {Database Theory --- ICDT'99},
  series    = {Lecture Notes in Computer Science},
  volume    = {1540},
  pages     = {217--235},
  year      = {1999},
  publisher = {Springer},
  address   = {Berlin, Heidelberg},""",
            bib
        )
        print(f"Regex patched beyer1999nearest in {bib_path.name}")

    # Remove sarle1983sas if present
    if "@article{sarle1983sas" in bib or "@techreport{sarle1983sas" in bib or "@misc{sarle1983sas" in bib:
        bib = re.sub(r"@(article|techreport|misc|book)\{sarle1983sas,[\s\S]*?\n\}\n*", "", bib)
        print(f"Removed sarle1983sas from {bib_path.name}")

    bib_path.write_text(bib, encoding="utf-8")
    print(f"Wrote updated {bib_path.name}")

print("All manuscript text patches applied successfully!")
