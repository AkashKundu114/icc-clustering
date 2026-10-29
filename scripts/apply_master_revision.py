"""
scripts/apply_master_revision.py

Applies all master revision items to paper/main.tex and springer_manuscript/main.tex.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def patch_file(tex_path: Path):
    print(f"Patching {tex_path}...")
    with open(tex_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. Title
    old_title = r"\title[When Does Feature Gating Salvage High-D Clustering?]{When Does Feature Gating and Anchor Consensus Salvage High-Dimensional Clustering? An Empirical and Geometric Analysis}"
    new_title = r"\title[When Do Feature Gating and Anchor Consensus Help High-D Clustering?]{When Do Feature Gating and Anchor Consensus Help High-Dimensional Clustering? An Empirical and Geometric Analysis}"
    if old_title in text:
        text = text.replace(old_title, new_title)
        print("  [OK] Title updated.")

    # 2. Abstract
    new_abstract = (
        r"\abstract{Consensus clustering is often assumed to resist high-dimensional noise, and dense $N \times N$ "
        r"consensus to be unavoidable. We test both assumptions. In finite-sample simulations with isotropic distractors "
        r"($D \gg N$), base clusterers (particularly spectral and Ward) converge stably ($\text{stability} > 0.8$) on "
        r"arbitrary noise partitions while ARI collapses toward zero, indicating that ensemble averaging alone does not "
        r"remove noise in these simulations. We evaluate ICC-v2, combining linear-time Bimodality-Gated Subspace Selection "
        r"(BGSS), random-subspace ensembles, bipartite anchor consensus, and closed-form centroid out-of-sample assignment. "
        r"Across 13 benchmarks (3,000 total fits: 30 seeds on six $D/N > 20$ cohorts, 10 on the remaining seven), we find "
        r"no statistically significant omnibus difference between methods (Friedman $p = 0.40$); K-Means attains the best "
        r"mean rank (5.15), followed by Standard Consensus (5.23), DEC (5.23), and ICC-v2 (5.62). ICC-v2's higher Grand Mean "
        r"ARI (0.152) is concentrated on two cancer cohorts, Leukemia (0.600) and SRBCT (0.546); it is near zero on most others, "
        r"and on Prostate underperforms simple baselines (0.012 vs. 0.043--0.049). On the six $D/N > 20$ cohorts, ICC-v2 ranks "
        r"first (exploratory, $n = 6$, subgroup mean $0.217$, not significant after Holm correction). Ablations demonstrate that "
        r"most of the gain over ambient consensus (0.037) stems from the random-subspace ensemble plus bipartite pipeline ($+0.118$), "
        r"while BGSS adds an additional $+0.062$ over matched random gating ($0.217$ vs. $0.155$, 95\% CI [$+0.013, +0.142$], "
        r"Wilcoxon $p = 0.0625$); determinacy anchor selection provides no statistical benefit over uniform random landmarks "
        r"($\Delta = +0.019$, 95\% CI [$-0.039, +0.082$]), and bipartite compression cuts consensus graph memory by 99.6\% "
        r"at $N = 10{,}000$. Failure modes are characterized under non-linear parity, zero-inflated counts, and large $K$.}"
    )
    # Match abstract block
    abs_start = text.find(r"\abstract{")
    if abs_start != -1:
        abs_end = text.find(r"\keywords{")
        if abs_end != -1:
            text = text[:abs_start] + new_abstract + "\n\n" + text[abs_end:]
            print("  [OK] Abstract updated.")

    # 3. Section 3 Paragraph around Eq 2
    old_sec3 = (
        "When uninformative ambient noise dimensions $D_{\\text{noise}}$ expand, Euclidean distance concentration compresses relative distance metrics. "
        "Recent geometric analyses demonstrate that while alternative metrics (Chebyshev and Cosine distances) slow the onset of geometric collapse "
        "relative to Euclidean $L_2$, high-dimensional distractor noise continues to degrade unsupervised distance contrasts across general norms. "
        "Specifically, empirical distance concentration simulations across noise dimensions up to $D_{\\text{noise}}=2{,}000$ (Exp~8d) confirm that while "
        "Chebyshev $L_\\infty$ and Cosine distances slow the onset of geometric collapse (retaining ARIs of $0.597$ and $0.308$ respectively for Spectral "
        "clustering at $D_{\\text{noise}}=2{,}000$, compared to $0.004$ under Euclidean $L_2$), high-dimensional distractor dimensions degrade clustering "
        "accuracy across all distance geometries in unsupervised settings without explicit feature selection. Specifically, the relative spread converges to zero:\n"
        "\\begin{equation}\n"
        " \\lim_{D \\to \\infty} \\frac{d_{\\max} - d_{\\min}}{d_{\\min}} = 0, \\quad \\text{and} \\quad \\lim_{D \\to \\infty} \\frac{\\sqrt{\\mathrm{Var}(\\|\\mathbf{x}_i - \\mathbf{x}_j\\|_2)}}{\\mathbb{E}[\\|\\mathbf{x}_i - \\mathbf{x}_j\\|_2]} = 0.\n"
        "\\end{equation}\n"
        "Consequently, the separation metric $\\rho_{\\text{sep}}(X)$ falls toward or below 1 (Fig.~\\ref{fig:conceptual_overview}(b)), indicating geometric overlap and obliterating distinguishable boundaries between latent classes."
    )

    new_sec3 = (
        "When uninformative ambient noise dimensions $D_{\\text{noise}}$ expand, Euclidean distance concentration "
        "compresses relative distance metrics~\\cite{peng2024interpreting}:\n"
        "\\begin{equation}\\label{eq:dist_concentration}\n"
        " \\lim_{D \\to \\infty} \\frac{d_{\\max} - d_{\\min}}{d_{\\min}} = 0, \\quad \\text{and} \\quad \\lim_{D \\to \\infty} \\frac{\\sqrt{\\mathrm{Var}(\\|\\mathbf{x}_i - \\mathbf{x}_j\\|_2)}}{\\mathbb{E}[\\|\\mathbf{x}_i - \\mathbf{x}_j\\|_2]} = 0.\n"
        "\\end{equation}\n"
        "Consequently, the subspace separation ratio $\\rho_{\\text{sep}}(X)$ falls toward or below 1 (Fig.~\\ref{fig:conceptual_overview}(b)), "
        "indicating severe geometric overlap and obliterating distinguishable boundaries between latent classes. Recent geometric analyses by Peng et al.~\\cite{peng2024interpreting} "
        "show that distance concentration contracts the observable manifold across general Minkowski metrics. In our distance concentration simulations "
        "across noise dimensions up to $D_{\\text{noise}}=2{,}000$ (Exp~8d, Table~\\ref{tab:exp8d_distance}), we find that distance choice slows but does not remove "
        "the collapse for Euclidean-based methods: Chebyshev ($L_\\infty$) with Spectral clustering retains an ARI of $0.597 \\pm 0.091$ at $D_{\\text{noise}}=2{,}000$ "
        "(and Cosine distance retains $0.308 \\pm 0.072$), whereas Euclidean Spectral clustering ($0.004 \\pm 0.005$) and K-Means ($0.019 \\pm 0.018$) collapse completely. "
        "As detailed in Table~\\ref{tab:exp8d_distance}, Chebyshev distance preserves an order-of-magnitude higher relative contrast ($C = 1.341 \\pm 0.190$) and elevated "
        "separation ($\\rho_{\\text{sep}} = 1.039 \\pm 0.005$) compared to Euclidean distance ($C = 0.131 \\pm 0.012, \\rho_{\\text{sep}} = 1.002 \\pm 0.000$); nevertheless, "
        "all unsupervised distance metrics degrade monotonically as noise expands unless informative dimensions are explicitly isolated. This geometric analysis "
        "directly connects to ICC-v2's anchor projection bound: by screening out distractor coordinates via BGSS prior to bipartite consensus, the effective noise "
        "dimension is bounded, preserving $\\rho_{\\text{sep}} \\gg 1$ in the active subspace and bounding spectral projection distortion on the anchor affinity kernel.\n\n"
        "\\input{gen/table_exp8d_distance.tex}"
    )
    if old_sec3 in text:
        text = text.replace(old_sec3, new_sec3)
        print("  [OK] Section 3 Eq 2 & Exp 8d updated.")

    # 4. Section 6.2 CoHiRF text
    old_cohirf = r"CoHiRF attains an average high-$D$ rank of $\TableThreeCohirfHighDRank$ (subgroup mean $0.017$), demonstrating that unguided random feature drawing struggles in extreme noise regimes."
    new_cohirf = (
        r"CoHiRF attains an average high-$D$ rank of $\TableThreeCohirfHighDRank$ (subgroup mean $0.017$). "
        r"This outcome is attributable to the method configuration as run (official implementation evaluated under repetitions $= 25$, "
        r"subspace fraction $= 0.15$, consensus threshold $= 0.80$; Table~\ref{tab:method_parameters}): CoHiRF enforces strict hierarchical consensus "
        r"over unanimous components without bipartite graph spectral projection, which causes extreme cluster fragmentation when features are heavily contaminated "
        r"by ambient noise, whereas random subspace gating within ICC-v2's bipartite pipeline retains a subgroup mean of $0.155$."
    )
    if old_cohirf in text:
        text = text.replace(old_cohirf, new_cohirf)
        print("  [OK] CoHiRF text updated.")

    # 5. Section 6.2 Exp 8e text and table
    old_exp8e = r"This refutes the anchor starvation hypothesis, demonstrating that performance degradation is primarily governed by marginal coordinate blending in BGSS when resolving many overlapping class geometries rather than landmark sparsity."
    new_exp8e = (
        r"This refutes anchor starvation as the main cause; the multi-class coordinate-blending explanation is consistent with but not tested by these data (Table~\ref{tab:exp8e_large_k})."
        r"\n\n\input{gen/table_exp8e_large_k.tex}"
    )
    if old_exp8e in text:
        text = text.replace(old_exp8e, new_exp8e)
        print("  [OK] Exp 8e text and table updated.")

    # 6. Section 6.2 Matched feature gating text (Exp 8c)
    old_exp8c = r"directly comparing BGSS against random feature selection under matched budgets ($|\mathcal{F}_{\text{active}}| = \lfloor \alpha D \rfloor$, Exp~8c) reveals that BGSS achieves a subgroup mean of $0.225$ versus $0.161$ for random gating (a $+0.064$ gain across the six cohorts), verifying that bimodality screening successfully prioritizes informative subspace signal over unguided random projections."
    new_exp8c = (
        r"directly comparing BGSS against matched random subspace gating ($|\mathcal{F}_{\text{active}}| = \lfloor \alpha D \rfloor$, Exp~8c, "
        r"evaluated on the 30 benchmark seeds $\{0, \dots, 29\}$ across the six cohorts) reveals that BGSS attains a subgroup mean of $0.217$ versus $0.155$ "
        r"for random gating (a paired gain of $\Delta = +0.062$, 95\% dataset-clustered bootstrap CI $[+0.013, +0.142]$, Wilcoxon $W = 1.0, p = 0.0625$). "
        r"Most of the overall gain over ambient consensus ($0.037$) comes from the random-subspace ensemble plus bipartite pipeline ($0.037 \to 0.155$, gain $+0.118$), "
        r"while BGSS multimodality screening adds an additional $+0.062$."
    )
    if old_exp8c in text:
        text = text.replace(old_exp8c, new_exp8c)
        print("  [OK] Exp 8c text updated.")

    # 7. Add definition of Exp 8a-8f protocol and seeds
    protocol_text = (
        r"\paragraph{Experimental Protocol and Seed Specifications (Exp 8a--8f):}"
        r"\nTo guarantee complete traceability and protocol adherence, all Phase 3 sub-experiments are pre-registered under deterministic seed sets:"
        r"\n\begin{itemize}"
        r"\n \item \textbf{Exp 8a (CoHiRF Benchmark):} Evaluated across all 13 benchmark datasets using 30 canonical random seeds ($\{0, \dots, 29\}$) on the six high-$D$ cohorts ($D/N > 20$) and 10 seeds ($\{0, \dots, 9\}$) on the remaining seven cohorts (250 model fits)."
        r"\n \item \textbf{Exp 8b (Anchor Selection):} Compares high-determinacy core anchors ($V_5$), uniform random anchors ($V_4$), K-Means centroid anchors, and balanced determinacy anchors across the six high-$D$ cohorts over 30 canonical seeds ($\{0, \dots, 29\}$, 720 fits)."
        r"\n \item \textbf{Exp 8c (Feature Gating):} Benchmarks BGSS multimodality screening against matched random feature subspace gating across the six high-$D$ cohorts over 30 canonical seeds ($\{0, \dots, 29\}$, 360 fits)."
        r"\n \item \textbf{Exp 8d (Distance Metrics and Geometry Simulation):} Evaluates Euclidean, Chebyshev, and Cosine geometries across distractor dimensions $D_{\text{noise}} \in [0, 2000]$ over 5 canonical random seeds ($\{42, 101, 202, 303, 404\}$)."
        r"\n \item \textbf{Exp 8e (Large-$K$ Anchor Budget Scaling):} Evaluates default budget $L=40$ against scaled budget $L=\max(40, 10K)$ on four large-$K$ cohorts (Indian Pines, Isolet, 20 Newsgroups, Extended Yale B) over 10 canonical seeds ($\{42, \dots, 51\}$)."
        r"\n \item \textbf{Exp 8f (Hyperparameter Sensitivity Grid):} Evaluates $M \in \{5, 10, 15, 25, 50\} \times L \in \{20, 40, 60, 80\}$ across the six high-$D$ cohorts over 10 random seeds ($\{42, \dots, 51\}$, 1,200 fits)."
        r"\n\end{itemize}"
    )
    if r"Experimental Protocol and Seed Specifications (Exp 8a--8f):" not in text:
        text = text.replace(r"\input{gen/table8_matched_budget.tex}", r"\input{gen/table8_matched_budget.tex}" + "\n\n" + protocol_text)
        print("  [OK] Exp 8a-8f protocol and seed lists inserted.")

    # 8. Section 6.3 Rank ties & unrounded Friedman
    old_friedman = (
        "Evaluating the 12 clustering algorithms across all 13 benchmarks (3{,}000 independent model fits: 30 seeds on $D/N > 20$ cohorts, 10 on others) via the non-parametric Friedman test (using average ranks for ties, computed directly on unrounded per-seed mean ARIs to eliminate 3-decimal rounding distortion) yields:\n"
        "\\begin{equation}\n"
        " \\chi_F^2 = 11.56, \\quad p = \\TableThreeFriedmanPValue.\n"
        "\\end{equation}"
    )
    new_friedman = (
        "Evaluating the 12 clustering algorithms across all 13 benchmarks (3{,}000 independent model fits: 30 seeds on $D/N > 20$ cohorts, 10 on others) via the non-parametric Friedman test (resolving ties via the average mid-rank convention, \\texttt{scipy.stats.rankdata(..., method='average')}, computed directly on unrounded per-seed mean ARIs) yields:\n"
        "\\begin{equation}\n"
        " \\chi_F^2 = 11.56, \\quad p = \\TableThreeFriedmanPValue,\n"
        "\\end{equation}\n"
        "with an ICC-v2 omnibus rank of $5.62$. When computed directly from the 3-decimal rounded benchmark table, small decimal ties yield $\\chi_F^2 = 11.54, p = 0.40$ with an ICC-v2 rank of $5.58$. Under both evaluations, empirical data fail to reject the null hypothesis of equivalent performance across methods ($p = 0.40 \\gg 0.05$)."
    )
    if old_friedman in text:
        text = text.replace(old_friedman, new_friedman)
        print("  [OK] Friedman rank ties and rounding explanation updated.")

    # 9. Section 6.4 Parameter Sensitivity & Scalability
    old_sec64_timing = (
        r"In our benchmarks, we fixed $L = 40$. Systematic sensitivity testing across $L \in \{20, 40, 60, 80\}$ (Exp~8f) reveals virtually flat response surfaces ($\Delta \le 0.003$ across $L \in [20, 80]$ for $M \ge 15$), demonstrating that $L=40$ comfortably balances structural representation and computational efficiency."
    )
    new_sec64_timing = (
        r"In our benchmarks, we fixed $L = 40$. Systematic sensitivity testing across $L \in \{20, 40, 60, 80\}$ (Exp~8f) across 10 random seeds ($\{42, \dots, 51\}$) reveals virtually flat response surfaces ($\Delta \le 0.003$ across $L \in [20, 80]$ for $M \ge 15$), where the baseline configuration ($M=25, L=40$) attains $0.225 \pm 0.128$; on the full 30 benchmark seeds ($\{0, \dots, 29\}$), $M=25, L=40$ settles at the reported omnibus benchmark mean of $0.217$, confirming that $L=40$ comfortably balances structural representation and computational efficiency."
    )
    if old_sec64_timing in text:
        text = text.replace(old_sec64_timing, new_sec64_timing)
        print("  [OK] Sec 6.4 Exp 8f sensitivity text updated.")

    old_tab4_block = (
        r"We evaluated the computational scaling of ICC-v2 as sample size $N$ increased from $500$ to $10{,}000$ (Table~\ref{tab:exp4_timing}, Fig.~\ref{fig:exp4_n}) across 5 canonical random seeds ($42, 101, 202, 303, 404$). On synthetic benchmarks under isolated execution, ICC-v2 executes in $0.463 \pm 0.095\text{ s}$ at $N=500$ and $10.346 \pm 0.778\text{ s}$ at $N=10{,}000$, demonstrating empirical linear complexity ($\beta \approx 1.0$) consistent with Theorem~\ref{thm:complexity}. At $N=10{,}000$, ICC-v2 achieves a $2.9\times$ speedup over dense consensus ($29.96\text{ s}$) while eliminating $97.4\%$ of peak dynamic RAM ($68.8\text{ MB}$ vs. $2{,}670.6\text{ MB}$)."
    )
    new_tab4_block = (
        r"We evaluated the computational scaling of ICC-v2 as sample size $N$ increased from $500$ to $10{,}000$ (Table~\ref{tab:exp4_timing}, Fig.~\ref{fig:exp4_n}) across 5 canonical random seeds ($42, 101, 202, 303, 404$) on a dedicated idle host. ICC-v2 executes in $0.323 \pm 0.007\text{ s}$ at $N=500$ and $2.302 \pm 0.497\text{ s}$ at $N=10{,}000$ ($0.962 \pm 0.095\text{ s}$ under pure execution without tracing overhead), scaling with an empirical power-law exponent of $\beta = 0.618$ over the tested range. In contrast, Standard Consensus scales with $\beta = 0.917$ (steepening to local exponents $\beta > 1.5$ above $N=5{,}000$), reaching $4.362 \pm 0.501\text{ s}$ at $N=10{,}000$ while requiring $2.67\text{ GB}$ peak memory compared to $68.8\text{ MB}$ for ICC-v2 (a $97.4\%$ reduction). Profiling confirms that the timing jump at $N=8{,}000$ recorded in earlier drafts was an artifact of host CPU throttling and memory swap on a shared testbed, which is completely eliminated under isolated execution on dedicated hardware."
    )
    if old_tab4_block in text:
        text = text.replace(old_tab4_block, new_tab4_block)
        print("  [OK] Table 4 description updated.")

    # 10. Section 7.4 Anchor selection null result and Exp 8b numbers
    old_sec74 = (
        r"To test alternative landmark selection strategies beyond uniform sampling, we evaluated K-Means centroids and balanced K-Means clustering as anchor generators (Exp~8b). Across the six high-$D$ cohorts, K-Means anchors and balanced K-Means anchors achieve subgroup mean ARIs of $0.108 \pm 0.209$ and $0.101 \pm 0.192$ respectively---significantly lower than both uniform random anchors (V4: $0.190 \pm 0.301$) and high-determinacy core anchors (V5: $0.225 \pm 0.318$)."
    )
    new_sec74 = (
        r"To test alternative landmark selection strategies beyond uniform sampling, we evaluated K-Means centroids and balanced determinacy anchors (Exp~8b) across all 30 canonical benchmark seeds ($\{0, \dots, 29\}$). Across the six high-$D$ cohorts, K-Means centroid anchors and balanced determinacy anchors achieve subgroup mean ARIs of $0.124 \pm 0.198$ and $0.119 \pm 0.188$ respectively---substantially lower than both uniform random empirical anchors (V4: $0.198 \pm 0.297$) and high-determinacy core anchors (V5: $0.217 \pm 0.312$)."
    )
    if old_sec74 in text:
        text = text.replace(old_sec74, new_sec74)
        print("  [OK] Section 7.4 Exp 8b numbers reconciled.")

    supp_ref_text = (
        r"\paragraph{Foundational Literature Attribution:}"
        r"\nIn accordance with citation best practices, the original seminal sources for all foundational comparators "
        r"(MacQueen 1967, Arthur \& Vassilvitskii 2007, Ward 1963, Bezdek 1981, von Luxburg 2007, Breiman 2001, Bengio et al. 2013) "
        r"are formally compiled in Supplementary Table~\ref{tab:supp_foundations}."
        r"\n\n\input{gen/tableS1_foundational_refs.tex}"
    )
    if r"Supplementary Table~\ref{tab:supp_foundations}" not in text:
        text = text.replace(r"\subsection{Unsupervised Feature Saliency and Interpretability Audit}", supp_ref_text + "\n\n" + r"\subsection{Unsupervised Feature Saliency and Interpretability Audit}")
        print("  [OK] Supplementary Table S1 inserted.")

    # 11. Conclusion
    old_conc = (
        r"In contrast, determinacy-based anchor certification produced an empirical null result ($\Delta = +0.019$, 95\% CI: $[-0.039, +0.082]$), showing no statistical separation from uniform random anchors."
    )
    new_conc = (
        r"In matched feature gating ablations, comparing BGSS directly against matched random subspace gating reveals a gain of $+0.062$ ($0.217$ vs. $0.155$, 95\% CI $[+0.013, +0.142]$, Wilcoxon $p = 0.0625$), "
        r"establishing that while the random-subspace bipartite ensemble accounts for $+0.118$ of the gain over ambient consensus ($0.037$), BGSS provides an additional $+0.062$ multimodality screening boost. "
        r"In contrast, determinacy-based anchor certification produced an empirical null result ($\Delta = +0.019$, 95\% CI: $[-0.039, +0.082]$), showing no statistical separation from uniform random anchors."
    )
    if old_conc in text:
        text = text.replace(old_conc, new_conc)
        print("  [OK] Conclusion updated.")

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Finished patching {tex_path}.")

def main():
    patch_file(ROOT / "paper" / "main.tex")
    patch_file(ROOT / "springer_manuscript" / "main.tex")

if __name__ == "__main__":
    main()
