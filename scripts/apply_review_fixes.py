"""
scripts/apply_review_fixes.py

Applies all reviewer-mandated revisions to paper/main.tex and synchronizes to springer_manuscript/main.tex.
"""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
MAIN_TEX = ROOT / "paper" / "main.tex"
SPRINGER_TEX = ROOT / "springer_manuscript" / "main.tex"

with open(MAIN_TEX, "r", encoding="utf-8") as f:
    text = f.read()

# -----------------------------------------------------------------------------
# 1. Abstract revisions
# -----------------------------------------------------------------------------
old_abs = (
    r"Ablations demonstrate that BGSS and bipartite anchor consensus interact synergistically for accuracy gains "
    r"($V_5 - V_2 = +0.140$, 95\% CI [$+0.004, +0.321$]), while anchor certification provides no statistical benefit "
    r"($\Delta = +0.019$, 95\% CI [$-0.039, +0.082$]) and bipartite compression cuts consensus-graph memory by 99.6\% at $N = 10{,}000$."
)
new_abs = (
    r"Ablations demonstrate that BGSS and bipartite anchor consensus interact suggestively for accuracy gains "
    r"($V_5 - V_2 = +0.139$, 95\% CI [$+0.004, +0.321$], Wilcoxon $p \approx 0.16$), while anchor certification provides no statistical benefit "
    r"($\Delta = +0.019$, 95\% CI [$-0.039, +0.082$]) and bipartite compression cuts consensus-graph memory by 99.6\% at $N = 10{,}000$."
)
assert old_abs in text, "Abstract target not found"
text = text.replace(old_abs, new_abs)

# Abstract prostate wording
text = text.replace(
    r"and on Prostate underperforms simple baselines (0.012 vs. 0.049).",
    r"and on Prostate underperforms simple baselines (0.012 vs. 0.043--0.049)."
)

# -----------------------------------------------------------------------------
# 2. Section 1 Contributions
# -----------------------------------------------------------------------------
# Contribution 1: change "confirming" to "indicating"
old_contrib1 = r"confirming that consensus aggregation alone does not cancel noise."
new_contrib1 = r"indicating that consensus aggregation alone does not cancel noise in these simulations."
assert old_contrib1 in text, "Contribution 1 target not found"
text = text.replace(old_contrib1, new_contrib1)

# Contribution 3: V5 - V2 = +0.139 and suggestive wording
old_contrib3 = (
    r"Across six biomedical cohorts with $D/N > 20$, $2 \times 2$ factorial and knockout ablations reveal that "
    r"BGSS and bipartite anchor consensus interact synergistically to unlock accuracy gains "
    r"($V_5 - V_2 = +0.140$, 95\% CI: $[+0.004, +0.321]$)"
)
new_contrib3 = (
    r"Across six biomedical cohorts with $D/N > 20$, $2 \times 2$ factorial and knockout ablations reveal that "
    r"BGSS and bipartite anchor consensus interact suggestively to unlock accuracy gains "
    r"($V_5 - V_2 = +0.139$, 95\% CI: $[+0.004, +0.321]$, Wilcoxon $p \approx 0.16$)"
)
assert old_contrib3 in text, "Contribution 3 target not found"
text = text.replace(old_contrib3, new_contrib3)

# -----------------------------------------------------------------------------
# 3. Section 2.2 Typo: "bipartite bipartite transfer cuts"
# -----------------------------------------------------------------------------
old_typo = r"through bipartite bipartite transfer cuts."
new_typo = r"through bipartite transfer cuts."
assert old_typo in text, "Typo target not found"
text = text.replace(old_typo, new_typo)

# -----------------------------------------------------------------------------
# 4. Section 4.2 Anchor sampling clarification (V5 draws uniformly within core set)
# -----------------------------------------------------------------------------
old_sec42 = (
    r"Given sample determinacy $\boldsymbol{\sigma} \in [0, 1]^N$, ICC-v2 extracts an anchor set $\mathcal{A} = \{a_1, \dots, a_L\}$ "
    r"of size $L \ll N$ (default $L=40$) from samples exceeding stability quantile $\tau_{\text{core}}$. We adopt uniform random landmark "
    r"sampling rather than $k$-means prototype anchors (as in FastMVC~\cite{huang2023fast}) or hierarchical $k$-d trees because random subsampling "
    r"executes in strictly $O(L)$ time with zero distance evaluations, avoiding the $O(N \cdot D \cdot L)$ cost of preliminary clustering passes "
    r"in high-dimensional noise regimes."
)
new_sec42 = (
    r"Given sample determinacy $\boldsymbol{\sigma} \in [0, 1]^N$, ICC-v2 extracts an anchor set $\mathcal{A} = \{a_1, \dots, a_L\}$ "
    r"of size $L \ll N$ (default $L=40$) by sampling uniformly at random from within the certified core set $\mathcal{C} = \{i : \sigma_i \ge \tau_{\text{core}}\}$ "
    r"(in contrast to variant V4, which draws anchors uniformly across the full dataset without determinacy screening). We sample uniformly within "
    r"the core set rather than running $k$-means prototype clustering on the core points (as in FastMVC~\cite{huang2023fast}) or constructing "
    r"hierarchical $k$-d trees because random subsampling executes in strictly $O(L)$ time with zero pairwise distance evaluations, avoiding the "
    r"$O(|\mathcal{C}| \cdot D \cdot L)$ cost of preliminary clustering passes in high-dimensional noise regimes."
)
assert old_sec42 in text, "Sec 4.2 target not found"
text = text.replace(old_sec42, new_sec42)

# -----------------------------------------------------------------------------
# 5. Section 6.1 Computational Scalability: Table 4 narrative & Fig 2 caption
# -----------------------------------------------------------------------------
old_sec61 = (
    r"We evaluated the computational scaling of ICC-v2 as sample size $N$ increased from $500$ to $10{,}000$ (Table~\ref{tab:exp4_timing}, Fig.~\ref{fig:exp4_n}). "
    r"On synthetic benchmarks under isolated execution, ICC-v2 executes in $0.463 \pm 0.095\text{ s}$ at $N=500$ and $1.249 \pm 0.063\text{ s}$ at $N=10{,}000$, "
    r"demonstrating empirical near-linear complexity consistent with Theorem~\ref{thm:complexity}."
)
new_sec61 = (
    r"We evaluated the computational scaling of ICC-v2 as sample size $N$ increased from $500$ to $10{,}000$ (Table~\ref{tab:exp4_timing}, Fig.~\ref{fig:exp4_n}) "
    r"across 5 canonical random seeds ($42, 101, 202, 303, 404$). On synthetic benchmarks under isolated execution, ICC-v2 executes in $0.463 \pm 0.095\text{ s}$ "
    r"at $N=500$ and $10.346 \pm 0.778\text{ s}$ at $N=10{,}000$, demonstrating empirical linear complexity ($\beta \approx 1.0$) consistent with Theorem~\ref{thm:complexity}. "
    r"At $N=10{,}000$, ICC-v2 achieves a $2.9\times$ speedup over dense consensus ($29.96\text{ s}$) while eliminating $97.4\%$ of peak dynamic RAM "
    r"($68.8\text{ MB}$ vs. $2{,}670.6\text{ MB}$). Note that Table~\ref{tab:exp4_timing} evaluates benchmark data under $D=200$ and $K=3$, whereas Table~\ref{tab:exp5_controlled} "
    r"Config A evaluates $D=100$ and $K=5$; the doubled feature dimensionality in Table~\ref{tab:exp4_timing} ($D=200$ vs. $D=100$) doubles base clusterer distance computations, "
    r"explaining the runtime difference ($10.35\text{ s}$ vs. $5.58\text{ s}$ at $N=10^4$)."
)
assert old_sec61 in text, "Sec 6.1 target not found"
text = text.replace(old_sec61, new_sec61)

# Fig 2 caption update
old_fig2_cap = r"(a) Execution runtime as sample size $N$ increases from $500$ to $10{,}000$, validating linear $O(N)$ empirical complexity."
new_fig2_cap = r"(a) Execution runtime as sample size $N$ increases from $500$ to $10{,}000$, demonstrating empirical linear $O(N)$ scaling ($\beta \approx 1.04$) and a $2.9\times$ speedup over dense consensus at $N=10{,}000$."
assert old_fig2_cap in text, "Fig 2 caption target not found"
text = text.replace(old_fig2_cap, new_fig2_cap)

# Dtype confirmation in Section 6.1
old_dtype_text = r"Config A ($M=25, L=40$, \texttt{float32}) processes $N=10^6$ samples in $182.64 \pm 51.01\text{ s}$"
assert old_dtype_text in text, "Dtype text not found"
# Dtype is already confirmed as \texttt{float32}

# -----------------------------------------------------------------------------
# 6. Table 6: Restore OpenML IDs and Access URLs
# -----------------------------------------------------------------------------
old_tab6 = r"""\begin{table*}[!t]
\caption{Characteristics of the 13 Multi-Domain Benchmark Datasets}
\label{tab:benchmark_properties}
\centering
\resizebox{\textwidth}{!}{%
\begin{tabular}{@{}llrrrrl@{}}
\toprule
\textbf{Domain} & \textbf{Dataset} & \textbf{Samples ($N$)} & \textbf{Features ($D$)} & \textbf{Classes ($K$)} & \textbf{Ratio ($D/N$)} & \textbf{Evaluation Focus} \\
\midrule
\multirow{6}{*}{\textbf{Microarray}} & CNS & $60$ & $7{,}129$ & $2$ & $118.8$ & High-$D$ Distractor Noise \\
 & Colon & $62$ & $2{,}000$ & $2$ & $32.3$ & Small-$N$ Variance Bias \\
 & Leukemia & $72$ & $7{,}129$ & $2$ & $99.0$ & Extreme High-$D$ Signal \\
 & Ovarian & $253$ & $15{,}154$ & $2$ & $59.9$ & Ultra-High Dimensionality \\
 & Prostate & $102$ & $12{,}600$ & $2$ & $123.5$ & Small-$N$ Dense Noise \\
 & SRBCT & $83$ & $2{,}308$ & $4$ & $27.8$ & Multi-Class Microarray \\
\midrule
\multirow{4}{*}{\textbf{Single-Cell / Tabular}} & Sonar & $208$ & $60$ & $2$ & $0.29$ & Dense Continuous Signals \\
 & Madelon\textsuperscript{*} & $500$ & $500$ & $2$ & $1.00$ & Non-Linear XOR Parity \\
 & Isolet & $7{,}797$ & $617$ & $26$ & $0.08$ & Acoustic Signal Structure \\
 & PBMC68k-red & $700$ & $765$ & $10$ & $1.09$ & Sparse Single-Cell scRNA-seq \\
\midrule
\multirow{3}{*}{\textbf{Text / Image}} & 20 Newsgroups & $18{,}846$ & $10{,}000$ & $20$ & $0.53$ & Ultra-Sparse Document Counts \\
 & Indian Pines & $10{,}249$ & $200$ & $16$ & $0.02$ & Hyperspectral Remote Sensing \\
 & Extended Yale B & $2{,}414$ & $1{,}024$ & $38$ & $0.42$ & Facial Manifold Clustering \\
\bottomrule
\multicolumn{7}{@{}l}{\footnotesize \textsuperscript{*}Madelon is evaluated on a deterministic subsample of 500 of the 2,600 samples from OpenML 1485 ($D/N = 1.00$).} \\
\end{tabular}%
}
\end{table*}"""

new_tab6 = r"""\begin{table*}[!t]
\caption{Characteristics and Upstream Repositories of the 13 Multi-Domain Benchmark Datasets}
\label{tab:benchmark_properties}
\centering
\resizebox{\textwidth}{!}{%
\begin{tabular}{@{}llrrrrlp{5.8cm}@{}}
\toprule
\textbf{Domain} & \textbf{Dataset} & \textbf{Samples ($N$)} & \textbf{Features ($D$)} & \textbf{Classes ($K$)} & \textbf{Ratio ($D/N$)} & \textbf{Evaluation Focus} & \textbf{Upstream Identifier / Access URL} \\
\midrule
\multirow{6}{*}{\textbf{Microarray}} & CNS & $60$ & $7{,}129$ & $2$ & $118.8$ & High-$D$ Distractor Noise & OpenML ID: 45086 (\url{https://www.openml.org/d/45086}) \\
 & Colon & $62$ & $2{,}000$ & $2$ & $32.3$ & Small-$N$ Variance Bias & OpenML ID: 45087 (\url{https://www.openml.org/d/45087}) \\
 & Leukemia & $72$ & $7{,}129$ & $2$ & $99.0$ & Extreme High-$D$ Signal & OpenML ID: 1104 (\url{https://www.openml.org/d/1104}) \\
 & Ovarian & $253$ & $15{,}154$ & $2$ & $59.9$ & Ultra-High Dimensionality & OpenML ID: 45098 (\url{https://www.openml.org/d/45098}) \\
 & Prostate & $102$ & $12{,}600$ & $2$ & $123.5$ & Small-$N$ Dense Noise & OpenML ID: 45099 (\url{https://www.openml.org/d/45099}) \\
 & SRBCT & $83$ & $2{,}308$ & $4$ & $27.8$ & Multi-Class Microarray & OpenML ID: 45101 (\url{https://www.openml.org/d/45101}) \\
\midrule
\multirow{4}{*}{\textbf{Single-Cell / Tabular}} & Sonar & $208$ & $60$ & $2$ & $0.29$ & Dense Continuous Signals & OpenML ID: 40 (\url{https://www.openml.org/d/40}) \\
 & Madelon\textsuperscript{*} & $500$ & $500$ & $2$ & $1.00$ & Non-Linear XOR Parity & OpenML ID: 1485 (\url{https://www.openml.org/d/1485}) \\
 & Isolet & $7{,}797$ & $617$ & $26$ & $0.08$ & Acoustic Signal Structure & OpenML ID: 300 (\url{https://www.openml.org/d/300}) \\
 & PBMC68k-red & $700$ & $765$ & $10$ & $1.09$ & Sparse Single-Cell scRNA-seq & 10x Genomics via Scanpy (\url{https://scanpy.readthedocs.io}) \\
\midrule
\multirow{3}{*}{\textbf{Text / Image}} & 20 Newsgroups & $18{,}846$ & $10{,}000$ & $20$ & $0.53$ & Ultra-Sparse Document Counts & Scikit-learn / CMU (\url{http://qwone.com/~jason/20Newsgroups/}) \\
 & Indian Pines & $10{,}249$ & $200$ & $16$ & $0.02$ & Hyperspectral Remote Sensing & UPV/EHU Hyperspectral (\url{https://www.ehu.eus/ccwintco}) \\
 & Extended Yale B & $2{,}414$ & $1{,}024$ & $38$ & $0.42$ & Facial Manifold Clustering & UCSD Vision Archive (\url{http://vision.ucsd.edu/extyaleb}) \\
\bottomrule
\multicolumn{8}{@{}l}{\footnotesize \textsuperscript{*}Madelon is evaluated on a deterministic subsample of 500 of the 2,600 samples from OpenML 1485 ($D/N = 1.00$).} \\
\end{tabular}%
}
\end{table*}"""

assert old_tab6 in text, "Table 6 target not found"
text = text.replace(old_tab6, new_tab6)

# -----------------------------------------------------------------------------
# 7. Section 6.2 Synthesis of Benchmark Findings
# -----------------------------------------------------------------------------
# Prostate in Subgroup Rank
text = text.replace(
    r"but on Prostate ($0.012$) it underperforms simple baselines ($0.049$).",
    r"but on Prostate ($0.012$) it underperforms simple baselines ($0.043\text{--}0.049$)."
)

# Large-K and High-Dimensional Underperformance paragraph
old_sec62_largek = (
    r"On 20 Newsgroups ($K = 20$), ICC-v2 collapses to $0.000 \pm 0.000$ (versus $0.102$ for DEC and $0.082$ for K-Means). "
    r"On Indian Pines ($K = 16$), ICC-v2 attains $0.136 \pm 0.021$ (versus $0.220$ for Standard Consensus and $0.211$ for K-Means). "
    r"On Yale B ($K = 38$), ICC-v2 yields $0.055 \pm 0.009$ (trailing DEC at $0.130$ and Spectral at $0.098$). "
    r"On PBMC68k-reduced ($K = 10$), it reaches only $0.182 \pm 0.009$ (trailing K-Means at $0.555$ and Standard Consensus at $0.540$)."
)
new_sec62_largek = (
    r"On 20 Newsgroups ($K = 20$), ICC-v2 collapses to $0.000 \pm 0.000$ (versus $0.102 \pm 0.005$ for Standard Consensus, $0.063 \pm 0.055$ for K-Means, and $0.008 \pm 0.003$ for DEC). "
    r"On Indian Pines ($K = 16$), ICC-v2 attains $0.136 \pm 0.030$ (versus $0.220 \pm 0.004$ for Standard Consensus and $0.212 \pm 0.010$ for K-Means). "
    r"On Yale B ($K = 38$), ICC-v2 yields $0.055 \pm 0.007$ (trailing DEC at $0.130 \pm 0.010$ and Spectral at $0.065 \pm 0.002$). "
    r"On PBMC68k-reduced ($K = 10$), it reaches only $0.182 \pm 0.062$ (trailing Standard Consensus at $0.555 \pm 0.037$ and K-Means at $0.494 \pm 0.034$)."
)
assert old_sec62_largek in text, "Sec 6.2 large-K target not found"
text = text.replace(old_sec62_largek, new_sec62_largek)

# Matched-budget feature selection baselines paragraph
old_sec62_matched = (
    r"For each dataset, baselines were allocated exactly $|\mathcal{F}_{\text{active}}| = \lfloor \alpha \cdot D \rfloor$ "
    r"features using Variance Filtering, PCA, Laplacian Score, and Sparse K-Means."
)
new_sec62_matched = (
    r"For each dataset, Variance Filtering, PCA, and Laplacian Score were allocated exactly $|\mathcal{F}_{\text{active}}| = \lfloor \alpha \cdot D \rfloor$ "
    r"features, while Sparse K-Means adaptively estimated its own feature weights under an $L_1$ penalty constraint ($s = 1.1 + 0.5(\sqrt{D} - 1.1)$)."
)
assert old_sec62_matched in text, "Sec 6.2 matched budget target not found"
text = text.replace(old_sec62_matched, new_sec62_matched)

# Clarify ambient K-Means comparison in Sec 6.2
old_sec62_km = r"failing to surpass ambient K-Means ($0.051$)."
new_sec62_km = (
    r"failing to surpass ambient K-Means ($0.051$ under multi-restart $n_{\text{init}}=5$ in Table~\ref{tab:fair_baselines}, "
    r"and $0.056$ under single-restart $n_{\text{init}}=1$ in Table~\ref{tab:benchmark_ari})."
)
assert old_sec62_km in text, "Sec 6.2 KM comparison not found"
text = text.replace(old_sec62_km, new_sec62_km)

# -----------------------------------------------------------------------------
# 8. Section 6.4: Rename "Convergence Analysis"
# -----------------------------------------------------------------------------
old_sec64 = r"\subsection{Convergence Analysis}\label{sec:convergence}"
new_sec64 = r"\subsection{Operational Settings and Scaling Regimes}\label{sec:param_scaling}"
assert old_sec64 in text, "Sec 6.4 title not found"
text = text.replace(old_sec64, new_sec64)

# -----------------------------------------------------------------------------
# 9. Section 7.3: Factorial Decomposition, Synergy Wording & Garbled Sentence
# -----------------------------------------------------------------------------
old_sec73 = (
    r"However, combining BGSS feature gating with bipartite anchor consensus achieves an ARI of $\AblationHighDSubgroupFullIccVTwo$, "
    r"representing a statistically significant synergistic gain of $V_5 - V_2 = +0.140$ (95\% cluster bootstrap CI: $[+0.004, +0.321]$). "
    r"Thus, BGSS gating and bipartite anchor consensus are jointly required to unlock accuracy gains: bipartite graph compression acts not "
    r"merely as a computational accelerator, but acts synergistically with subspace feature screening we hypothesize that it operates by "
    r"suppressing noisy off-diagonal co-associations through landmark projection."
)
new_sec73 = (
    r"However, combining BGSS feature gating with bipartite anchor consensus achieves an ARI of $\AblationHighDSubgroupFullIccVTwo$, "
    r"representing a suggestive gain of $V_5 - V_2 = +0.139$ (bootstrap CI barely excludes zero: 95\% cluster bootstrap CI $[+0.004, +0.321]$; "
    r"exact Wilcoxon $W = 3.0, p \approx 0.16, n = 6$), driven predominantly by Leukemia ($+0.557$ of the $+0.837$ cumulative difference across the six cohorts). "
    r"Thus, while BGSS gating and bipartite anchor consensus show a positive joint interaction, bipartite graph compression acts primarily as a computational "
    r"accelerator and interacts with subspace feature screening; we hypothesize that it operates by suppressing noisy off-diagonal co-associations through landmark projection."
)
assert old_sec73 in text, "Sec 7.3 target not found"
text = text.replace(old_sec73, new_sec73)

# -----------------------------------------------------------------------------
# 10. Section 8.1 Translational Oncology: Prostate K-Means
# -----------------------------------------------------------------------------
old_sec81 = r"underperforms simple ambient K-Means ($0.049$)."
new_sec81 = r"underperforms simple ambient K-Means ($0.043$ under $n_{\text{init}}=1$ in Table~\ref{tab:benchmark_ari}, $0.049$ under $n_{\text{init}}=5$ in Table~\ref{tab:fair_baselines})."
assert old_sec81 in text, "Sec 8.1 target not found"
text = text.replace(old_sec81, new_sec81)

# -----------------------------------------------------------------------------
# 11. Section 8.2 Single-Cell Genomics: PBMC68k Numbers
# -----------------------------------------------------------------------------
old_sec82 = r"ICC-v2 attains an ARI of $0.182 \pm 0.009$, ranking last behind K-Means ($0.555$) and Standard Consensus ($0.540$)."
new_sec82 = r"ICC-v2 attains an ARI of $0.182 \pm 0.062$, ranking last behind Standard Consensus ($0.555 \pm 0.037$) and K-Means ($0.494 \pm 0.034$)."
assert old_sec82 in text, "Sec 8.2 target not found"
text = text.replace(old_sec82, new_sec82)

# -----------------------------------------------------------------------------
# 12. Section 9.1 Limitations: Numbers & Penalty Formula
# -----------------------------------------------------------------------------
old_sec91 = (
    r"on 20 Newsgroups ($K=20$), it collapses to $0.000 \pm 0.000$ (versus $0.102$ for DEC); "
    r"on Indian Pines ($K=16$), it attains $0.136 \pm 0.021$ (versus $0.220$ for Standard Consensus); "
    r"on Yale B ($K=38$), it scores $0.055 \pm 0.009$ (versus $0.130$ for DEC); "
    r"and on PBMC68k-reduced ($K=10$), it achieves $0.182 \pm 0.009$ (versus $0.555$ for K-Means)."
)
new_sec91 = (
    r"on 20 Newsgroups ($K=20$), it collapses to $0.000 \pm 0.000$ (versus $0.102 \pm 0.005$ for Standard Consensus, $0.063 \pm 0.055$ for K-Means, and $0.008 \pm 0.003$ for DEC); "
    r"on Indian Pines ($K=16$), it attains $0.136 \pm 0.030$ (versus $0.220 \pm 0.004$ for Standard Consensus and $0.212 \pm 0.010$ for K-Means); "
    r"on Yale B ($K=38$), it scores $0.055 \pm 0.007$ (versus $0.130 \pm 0.010$ for DEC and $0.065 \pm 0.002$ for Spectral); "
    r"and on PBMC68k-reduced ($K=10$), it achieves $0.182 \pm 0.062$ (versus $0.555 \pm 0.037$ for Standard Consensus and $0.494 \pm 0.034$ for K-Means)."
)
assert old_sec91 in text, "Sec 9.1 target not found"
text = text.replace(old_sec91, new_sec91)

# Sparse K-Means penalty formula in Sec 9.1
old_penalty = r"unsupervised heuristic penalty $s \approx 0.5 \sqrt{D}$ rather than"
new_penalty = r"unsupervised heuristic penalty $s = 1.1 + 0.5(\sqrt{D} - 1.1)$ rather than"
assert old_penalty in text, "Sec 9.1 penalty target not found"
text = text.replace(old_penalty, new_penalty)

# -----------------------------------------------------------------------------
# 13. Section 10 Conclusion: Prostate, Synergy, Anchor Starvation & 1M sample time
# -----------------------------------------------------------------------------
old_conc_prostate = r"underperforming baseline methods on Prostate ($0.012$ vs. $0.049$)."
new_conc_prostate = r"underperforming baseline methods on Prostate ($0.012$ vs. $0.043\text{--}0.049$)."
assert old_conc_prostate in text, "Conclusion prostate target not found"
text = text.replace(old_conc_prostate, new_conc_prostate)

old_conc_synergy = (
    r"Ablation experiments demonstrate that accuracy gains require the joint interaction of marginal multimodality screening (BGSS) "
    r"and bipartite anchor consensus ($V_5 - V_2 = +0.140$, 95\% CI: $[+0.004, +0.321]$), while bipartite graph compression ($O(NL)$) "
    r"simultaneously drives computational efficiency, cutting consensus graph memory by \MemoryScalingTenKGraphReduction\ at $N=10{,}000$ "
    r"and enabling processing $N=1{,}000{,}000$ instances in \ExtremeScaleTime. In contrast, determinacy-based anchor certification produced "
    r"an empirical null result ($\Delta = +0.019$, 95\% CI: $[-0.039, +0.082]$), showing no statistical separation from uniform random anchors. "
    r"Explicit failure modes were characterized under non-linear XOR parity interactions, large cluster counts with anchor starvation ($K \ge 20$), "
    r"ultra-sparse text and single-cell count matrices (20 Newsgroups, PBMC68k-reduced), and weak-signal genomic cohorts."
)
new_conc_synergy = (
    r"Ablation experiments demonstrate that accuracy gains show a suggestive joint interaction between marginal multimodality screening (BGSS) "
    r"and bipartite anchor consensus ($V_5 - V_2 = +0.139$, 95\% CI: $[+0.004, +0.321]$, Wilcoxon $p \approx 0.16$), while bipartite graph compression ($O(NL)$) "
    r"simultaneously drives computational efficiency, cutting consensus graph memory by \MemoryScalingTenKGraphReduction\ at $N=10{,}000$ "
    r"and enabling processing $N=1{,}000{,}000$ instances in $141\text{--}183\text{ s}$. In contrast, determinacy-based anchor certification produced "
    r"an empirical null result ($\Delta = +0.019$, 95\% CI: $[-0.039, +0.082]$), showing no statistical separation from uniform random anchors. "
    r"Explicit failure modes were characterized under non-linear XOR parity interactions, large cluster counts (with anchor starvation remaining an untested hypothesis for $K \ge 20$), "
    r"ultra-sparse text and single-cell count matrices (20 Newsgroups, PBMC68k-reduced), and weak-signal genomic cohorts."
)
assert old_conc_synergy in text, "Conclusion synergy target not found"
text = text.replace(old_conc_synergy, new_conc_synergy)

# -----------------------------------------------------------------------------
# 14. Declarations: AI Use Disclosure and Full OpenML IDs / URLs
# -----------------------------------------------------------------------------
old_decl = r"""\section*{Declarations}

\textbf{Funding}: No specific external grant funding was received for this study.

\textbf{Conflict of interest}: The authors declare that they have no competing financial or non-financial interests directly or indirectly related to the work submitted for publication.

\textbf{Ethics approval and consent to participate}: Not applicable. This study analyzes publicly available benchmark datasets and synthetic benchmark simulations involving no human subjects or animal experiments.

\textbf{Consent for publication}: All authors have read and approved the final manuscript and consent to its publication.

\textbf{Data availability}: Upstream repository identifiers and access URLs for all 13 benchmark datasets are documented in Table~\ref{tab:benchmark_properties}. Preprocessing scripts to fetch and cache all raw data directly from original repositories are provided in the code repository via \texttt{scripts/fetch\_data.py}.

\textbf{Code availability}: All benchmark datasets, raw pre-processed matrices, baseline reproduction harnesses, and experimental figure generators are released under the open-source MIT License at \url{https://github.com/AkashKundu114/icc-clustering} (release tag \texttt{v2.0.0}).

\textbf{Authors' contributions}: A.~Kundu conceived the study, derived the theoretical framework, implemented the algorithms, conducted experiments, and wrote the manuscript. T.~Guha, R.~Ghatak, and A.~Naskar contributed to experimental benchmarking, baseline implementations, and code verification. K.~K.~Das supervised the research, reviewed statistical methodology, and edited the manuscript. Correspondence and material requests should be addressed to A.~Kundu (\href{mailto:akashkundu1152@gmail.com}{\texttt{akashkundu1152@gmail.com}})."""

new_decl = r"""\section*{Declarations}

\textbf{Funding}: No specific external grant funding was received for this study.

\textbf{Conflict of interest}: The authors declare that they have no competing financial or non-financial interests directly or indirectly related to the work submitted for publication.

\textbf{Ethics approval and consent to participate}: Not applicable. This study analyzes publicly available benchmark datasets and synthetic benchmark simulations involving no human subjects or animal experiments.

\textbf{Consent for publication}: All authors have read and approved the final manuscript and consent to its publication.

\textbf{Data availability}: All 13 benchmark datasets analyzed in this study are publicly accessible from their original upstream open-access repositories:
\begin{itemize}
    \item \textbf{Biomedical and Tabular Microarrays:} CNS (OpenML ID: 45086, \url{https://www.openml.org/d/45086}), Colon (OpenML ID: 45087, \url{https://www.openml.org/d/45087}), Leukemia (OpenML ID: 1104, \url{https://www.openml.org/d/1104}), Ovarian (OpenML ID: 45098, \url{https://www.openml.org/d/45098}), Prostate (OpenML ID: 45099, \url{https://www.openml.org/d/45099}), SRBCT (OpenML ID: 45101, \url{https://www.openml.org/d/45101}), Sonar (OpenML ID: 40, \url{https://www.openml.org/d/40}), Madelon (OpenML ID: 1485, \url{https://www.openml.org/d/1485}), and Isolet (OpenML ID: 300, \url{https://www.openml.org/d/300}; UCI ID: 54, \url{https://archive.ics.uci.edu/dataset/54/isolet}).
    \item \textbf{Text Benchmark:} 20 Newsgroups (CMU 20 Newsgroups corpus: \url{http://qwone.com/~jason/20Newsgroups/}; accessible via \texttt{sklearn.datasets.fetch\_20newsgroups}).
    \item \textbf{Hyperspectral Benchmark:} Indian Pines (Purdue University LARS / UPV/EHU repository: \url{https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes}).
    \item \textbf{Facial Image Benchmark:} Extended Yale B (UCSD Computer Vision archive: \url{http://vision.ucsd.edu/extyaleb/CroppedYaleB.zip}; Academic Torrents persistent archive: \url{https://academictorrents.com/details/aad8bf8e6ee5d8a3bf46c7ab5adfacdd8ad36247}).
    \item \textbf{Single-Cell Genomics Benchmark:} PBMC68k-reduced (10x Genomics 68k PBMCs primary repository: \url{https://www.10xgenomics.com/datasets/fresh-68-k-pbm-cs-donor-a-1-standard-1-1-0}; distributed in Scanpy: \url{https://scanpy.readthedocs.io/en/stable/generated/scanpy.datasets.pbmc68k_reduced.html}).
\end{itemize}
Automated download and caching routines for all 13 cohorts are provided via \texttt{scripts/fetch\_data.py}.

\textbf{Code availability}: All benchmark datasets, raw pre-processed matrices, baseline reproduction harnesses, and experimental figure generators are released under the open-source MIT License at \url{https://github.com/AkashKundu114/icc-clustering} (release tag \texttt{v2.0.0}).

\textbf{Use of artificial intelligence tools}: During the preparation of this work, the authors used AI coding and editorial assistance tools (Google Antigravity, utilizing Gemini models) for writing automated reproducibility and verification scripts, formatting LaTeX tables, querying CrossRef bibliographic APIs, checking numerical consistency across result registries, and proofreading text. The human authors reviewed and edited all outputs, accept full responsibility for the contents of the publication, and confirm that all mathematical derivations, empirical analyses, and scientific conclusions originate from the authors.

\textbf{Authors' contributions}: A.~Kundu conceived the study, derived the theoretical framework, implemented the algorithms, conducted experiments, and wrote the manuscript. T.~Guha, R.~Ghatak, and A.~Naskar contributed to experimental benchmarking, baseline implementations, and code verification. K.~K.~Das supervised the research, reviewed statistical methodology, and edited the manuscript. Correspondence and material requests should be addressed to A.~Kundu (\href{mailto:akashkundu1152@gmail.com}{\texttt{akashkundu1152@gmail.com}})."""

assert old_decl in text, "Declarations target not found"
text = text.replace(old_decl, new_decl)

# Save to paper/main.tex
with open(MAIN_TEX, "w", encoding="utf-8") as f:
    f.write(text)

# Sync to springer_manuscript/main.tex
shutil.copy2(MAIN_TEX, SPRINGER_TEX)
print("Successfully applied all revisions and synchronized to springer_manuscript/main.tex.")
