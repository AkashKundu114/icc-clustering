"""
Apply all scientific and editorial fixes from peer review to manuscript files.
"""

from pathlib import Path

def apply_fixes():
    root = Path(__file__).resolve().parents[1]
    targets = [
        root / "springer_manuscript" / "main.tex",
        root / "paper" / "main.tex"
    ]

    for p in targets:
        if not p.exists():
            continue
        print(f"Processing {p}...")
        content = p.read_text(encoding="utf-8")

        # 1. Abstract
        old_abs_start = r"\abstract{Subsample stability is widely assumed to ensure clustering reliability"
        # We find the abstract block up to \keywords
        abs_end_idx = content.find(r"\keywords{")
        abs_start_idx = content.find(old_abs_start)
        assert abs_start_idx != -1 and abs_end_idx != -1, "Abstract boundaries not found"

        new_abs = (
            r"\abstract{Subsample stability is widely assumed to ensure clustering reliability, "
            r"and consensus clustering to resist high-dimensional noise. We evaluate this premise "
            r"across simulations and six biomedical cohorts ($D/N > 20$) using stratified $80\%$ subsampling "
            r"(30 draws, 435 pairs), column-permuted null controls, and an added post hoc non-degeneracy filter. "
            r"Under isotropic noise ($D \gg N$), base clusterers converge stably onto arbitrary noise partitions "
            r"while the Adjusted Rand Index (ARI) collapses. On real cohorts, three of twelve methods "
            r"(FCAG, FCM, FastMVC) exhibit non-degenerate discordance across $\ge 3$ cohorts; over their nine "
            r"discordant cells, stability reaches $0.684$ while accuracy is $-0.003$ (averaging $0.638$ stability "
            r"and $0.046$ accuracy across all eighteen cells). Paired bootstrap resampling confirms that stability "
            r"substantially exceeds column-permuted nulls while accuracy lingers near chance, demonstrating that "
            r"high reproducibility can reflect noise geometry rather than true clusters."
            "\n\n"
            r"To evaluate what mechanisms recover signal, we analyze Gated Anchor Consensus (GAC)---coupling "
            r"Bimodality-Gated Subspace Selection (BGSS), random-subspace ensembles, and bipartite anchor graphs. "
            r"On the six high-$D$ cohorts, GAC achieves the highest mean ARI ($0.217$ vs. $0.037$ for ambient consensus), "
            r"concentrated in Leukemia ($0.600$) and SRBCT ($0.546$). Random-subspace ensembling provides the primary "
            r"empirical recovery ($0.037 \to 0.155$, $+0.118$), BGSS adds $+0.062$ over matched random gating "
            r"(95\% CI: $[+0.013, +0.142]$), and bipartite compression reduces graph memory by 99.6\% at $N = 10^4$ "
            r"without altering accuracy. Across 13 benchmarks (3,000 fits), omnibus differences are not statistically "
            r"significant (Friedman $p = 0.40$), and GAC fails where marginal bimodality is absent. We conclude "
            r"that stability requires null controls, and that marginal gating succeeds only when informative coordinates "
            r"are detectably multimodal.}"
            "\n\n"
        )
        content = content[:abs_start_idx] + new_abs + content[abs_end_idx:]

        # 2. Intro: post hoc filter
        content = content.replace(
            "using column-permuted null controls and a pre-specified non-degeneracy criterion to exclude trivial partitions.",
            "using column-permuted null controls and a post hoc non-degeneracy filter to exclude trivial partitions."
        )

        # 3. Intro: BGSS Sarle citation
        content = content.replace(
            r"ranks dimensions via finite-sample Sarle's Bimodality Coefficient~\cite{sarle1983sas}, filtering continuous unimodal noise coordinates prior to base clustering.",
            r"ranks dimensions via the finite-sample Bimodality Coefficient (traditionally attributed to Warren Sarle and documented in SAS/STAT~\cite{sas1990stat}; see also Pfister et al.~\cite{pfister2013good}), filtering continuous unimodal noise coordinates prior to base clustering."
        )

        # 4. Intro: Contribution 1
        old_c1 = (
            r"Using a pre-specified non-degeneracy criterion and column-permuted null controls, we show "
            r"that this pattern reflects stable structure in the data rather than permutation artifacts or trivial "
            r"partitions. A paired bootstrap yields a mean gap of $+0.485$ (95\% CI $[+0.379, +0.662]$; "
            r"unconstrained $+0.464$, $[+0.363, +0.607]$), and three of twelve methods (FCAG, FCM, FastMVC) "
            r"meet the criterion on at least three cohorts."
        )
        new_c1 = (
            r"Using an added post hoc non-degeneracy filter and column-permuted null controls, we show that "
            r"this pattern reflects stable structure in the data rather than permutation artifacts or trivial partitions. "
            r"Across the nine discordant method-cohort cells identified under this criterion, stability averages $0.684$ "
            r"while accuracy is $-0.003$ (overall 18-cell average across all six cohorts: $0.638$ stability, $0.046$ accuracy). "
            r"Paired bootstrap resampling across cohorts confirms that excess stability over column-permuted nulls is "
            r"large and positive ($+0.472$, 95\% CI: $[+0.368, +0.645]$), while the stability--accuracy gap averages "
            r"$+0.485$ (95\% CI $[+0.379, +0.662]$; unconstrained $+0.464$, $[+0.363, +0.607]$), confirming that "
            r"reproducibility under resampling does not imply correctness."
        )
        assert old_c1 in content, "Contribution 1 not found"
        content = content.replace(old_c1, new_c1)

        # 5. Intro: Contribution 2
        old_c2 = (
            r"Bipartite random-subspace ensembling accounts for $+0.118$ (65.6\%) of the $+0.180$ gain over ambient "
            r"consensus on the six high-$D$ cohorts, and Bimodality-Gated Subspace Selection (BGSS) adds $+0.062$ over "
            r"matched random gating (95\% CI $[+0.013, +0.142]$)."
        )
        new_c2 = (
            r"Ensembling over random subspaces accounts for $+0.118$ (65.6\%) of the $+0.180$ empirical gain over ambient "
            r"consensus on the six high-$D$ cohorts ($0.037 \to 0.155$), while Bimodality-Gated Subspace Selection (BGSS) "
            r"adds $+0.062$ over matched random gating (95\% CI $[+0.013, +0.142]$). In the absence of subspace gating, "
            r"bipartite graph compression alone yields only $+0.009$ ($0.037 \to 0.046$, Table~\ref{tab:factorial}), "
            r"functioning primarily as a computational compressor ($O(NL)$ memory) rather than a statistical recovery mechanism."
        )
        assert old_c2 in content, "Contribution 2 not found"
        content = content.replace(old_c2, new_c2)

        # 6. Related Work: Citation clump [5-9]
        old_rel_clump = r"Modern extensions examine cluster count selection and stability weighting through iterative sub-matrix extraction and doubly stochastic normalization~\cite{patron2026codac,cai2025spectral,yang2025autoweighted,hu2024multiview,chen2025ccegan}."
        new_rel_clump = r"Modern extensions examine stability weighting through doubly stochastic affinity normalization~\cite{cai2025spectral}, auto-weighted graph reconstruction~\cite{yang2025autoweighted}, hypergraph p-Laplacians with feature selection~\cite{hu2024multiview}, and deep active or generative ensemble formulations~\cite{patron2026codac,chen2025ccegan}."
        assert old_rel_clump in content, "Related work clump not found"
        content = content.replace(old_rel_clump, new_rel_clump)

        # 7. Related Work: Fern & Brodley
        old_wani = r"Random subspace ensembles~\cite{wani2024comprehensive} promote diversity, but under extreme distractor noise they draw mostly uninformative coordinates and base clusterers fit chance structure."
        new_wani = r"Random subspace ensembles, pioneered by Fern and Brodley~\cite{fern2003random} and surveyed by Wani~\cite{wani2024comprehensive}, promote ensemble diversity by projecting data onto random feature subsets; however, under extreme distractor noise ($D \gg N$), random subspaces draw mostly uninformative coordinates, causing base clusterers to fit chance noise structure."
        assert old_wani in content, "Wani citation not found"
        content = content.replace(old_wani, new_wani)

        # 8. Table 1: title
        content = content.replace(
            r"\caption{Methods evaluated and their handling of high-dimensional noise}",
            r"\caption{Clustering methods considered in this study and their handling of high-dimensional noise}"
        )

        # 9. Section 3: Definitions
        old_sec3_def = (
            r"Subsample stability ($\text{Stab}$) is the mean pairwise ARI on overlapping samples across "
            r"all $\binom{30}{2} = 435$ pairs of stratified 80\% subsamples. Accuracy ($\text{Acc}$) is the mean "
            r"ARI of subsample partitions against the reference labels, and the stability--accuracy gap is "
            r"$\Delta = \text{Stab} - \text{Acc}$. Following the pre-specified decision rules, a method-cohort pair "
            r"is discordant under Rule~(i) if $\text{Stab} \ge 0.50$ and $\text{Acc} \le 0.05$. Because a degenerate "
            r"partition (for example, one dominant cluster) attains high stability by construction, Rule~(i') "
            r"additionally requires the smallest cluster to hold at least 5\% of the subsample in at least 90\% of subsamples."
        )
        new_sec3_def = (
            r"Subsample stability ($\text{Stab}$) is the mean pairwise ARI on overlapping samples across all "
            r"$\binom{30}{2} = 435$ pairs of stratified 80\% subsamples. Accuracy ($\text{Acc}$) is the mean ARI "
            r"of subsample partitions against clinical reference labels, and the stability--accuracy gap is "
            r"$\Delta = \text{Stab} - \text{Acc}$. Because $\Delta > 0$ can arise trivially by arithmetic when $\text{Acc} \approx 0$, "
            r"we define excess stability over unstructured noise as $\text{Stab} - \text{Null}$, where $\text{Null}$ "
            r"denotes stability evaluated on column-permuted data. A method-cohort pair is classified as discordant "
            r"under Rule~(i) if $\text{Stab} \ge 0.50$ and $\text{Acc} \le 0.05$, with Rule~(ii) ensuring genuine "
            r"geometric reproducibility by requiring $\text{Stab} - \text{Null} \ge 0.10$. Because degenerate partitions "
            r"(e.g., one dominant cluster) attain high stability by construction, Rule~(i') was added post hoc to "
            r"additionally require the smallest cluster to hold at least 5\% of the subsample in at least 90\% of subsamples."
        )
        assert old_sec3_def in content, "Section 3 Definitions not found"
        content = content.replace(old_sec3_def, new_sec3_def)

        # 10. Section 3: Summary of findings
        old_sec3_sum = (
            r"three of twelve methods (FCAG, FCM, FastMVC) meet Rule~(i') on at least three cohorts, with mean stability 0.638 and mean accuracy 0.046 (Section~\ref{sec:real_data_stability})."
        )
        new_sec3_sum = (
            r"three of twelve methods (FCAG, FCM, FastMVC) meet Rule~(i') on at least three cohorts; across their nine discordant cells, mean stability is $0.684$ while accuracy is $-0.003$ (averaging $0.638$ stability and $0.046$ accuracy across all eighteen cells for these three methods; Section~\ref{sec:real_data_stability})."
        )
        assert old_sec3_sum in content, "Section 3 summary not found"
        content = content.replace(old_sec3_sum, new_sec3_sum)

        # 11. Fig 2 caption
        content = content.replace(
            r"(b) Gap metric indicating positive stability attractors ($\Delta > 0$) for graph-based spectral and Ward clustering.",
            r"(b) Subsample-perturbation stability--accuracy gap ($\Delta = \text{Stab} - \text{ARI}$) under $80\%$ subsampling across 50 independent perturbation draws, demonstrating positive stability attractors ($\Delta > 0$) even when accuracy collapses. Seed stability on unperturbed data is omitted here as it is uninformative ($\text{ARI} \equiv 1.0$) for deterministic Ward and spectral algorithms."
        )

        # 12. Section 3.1 prose
        old_sec31_prose = (
            r"In finite samples, base algorithms capture stochastic noise fluctuations. This produces stability-accuracy discordance: base partitions agree with one another ($\text{Stability} > 0.8$) while partition accuracy collapses ($\text{ARI} \to 0$, Fig.~\ref{fig:ari_stability}). As Fig.~\ref{fig:dist_gap} shows, this gap ($\Delta = \text{Stability} - \text{ARI} > 0$) is especially pronounced in graph-based methods (spectral clustering, Ward linkage), while centroid methods (K-Means, FCM) experience simultaneous loss of stability and accuracy."
        )
        new_sec31_prose = (
            r"In finite samples, base algorithms capture stochastic noise fluctuations. Under subsample perturbation ($80\%$ subsampling matching the real-data protocol), this produces stability-accuracy discordance: perturbed base partitions agree with one another ($\text{Stability} > 0.8$) while partition accuracy collapses ($\text{ARI} \to 0$, Fig.~\ref{fig:ari_stability}). As Fig.~\ref{fig:dist_gap} shows, this gap ($\Delta = \text{Stability} - \text{ARI} > 0$) persists under subsampling in graph-based methods (spectral clustering, Ward linkage), whereas seed stability on unperturbed data is trivial for deterministic solvers, while centroid methods (K-Means, FCM) experience simultaneous loss of stability and accuracy."
        )
        assert old_sec31_prose in content, "Section 3.1 prose not found"
        content = content.replace(old_sec31_prose, new_sec31_prose)

        # 13. Fig 3 caption
        old_fig3_cap = (
            r"The shaded region highlights the pre-specified non-degenerate stability-accuracy discordance zone (Rule~(i'): $\text{Stab} \ge 0.50$, $\text{Acc} \le 0.05$, and smallest cluster holding $\ge 5\%$ of points in $\ge 90\%$ of subsamples)."
        )
        new_fig3_cap = (
            r"The shaded region highlights the non-degenerate stability-accuracy discordance zone (defined post hoc under Rule~(i'): $\text{Stab} \ge 0.50$, $\text{Acc} \le 0.05$, and smallest cluster holding $\ge 5\%$ of points in $\ge 90\%$ of subsamples)."
        )
        assert old_fig3_cap in content, "Fig 3 caption part 1 not found"
        content = content.replace(old_fig3_cap, new_fig3_cap)

        content = content.replace(
            r"whereas GAC ($\Delta = +0.300$) attenuates the gap by feature screening.",
            r"whereas GAC exhibits a reduced average gap ($\Delta = +0.300$), reflecting higher accuracy on signal-rich cohorts (Leukemia, SRBCT) alongside lower stability where features are aggressively filtered (Colon, Leukemia); bootstrap confidence intervals overlap with several baselines."
        )

        # 14. Section 3.2: eliminate redundant definitions
        old_sec32_redundancy = (
            r"Subsample stability ($\text{Stab}$) denotes the average pairwise Adjusted Rand Index (ARI) evaluated on overlapping instances across all $\binom{30}{2} = 435$ subsample pairs. Empirical accuracy ($\text{Acc}$) reflects the mean ARI of subsample assignments referenced to clinical labels, with the stability-accuracy gap quantified as $\Delta = \text{Stab} - \text{Acc}$. Column-permuted null controls ($\text{Null}$) are derived by independently shuffling each feature column across samples, providing a reference baseline for unstructured noise stability. Full-cohort seed stability ($\text{Seed}^*$, mean pairwise ARI across 435 seed pairs on the unperturbed data) is reported as an explicit secondary column for stochastic estimators."
        )
        new_sec32_redundancy = (
            r"Using the subsampling protocol and metrics defined in Section~\ref{sec:falsification} ($\text{Stab}$, $\text{Acc}$, $\text{Null}$, and $\Delta = \text{Stab} - \text{Acc}$), we evaluated all 12 algorithms across the six high-dimensional cohorts. Full-cohort seed stability ($\text{Seed}^*$, mean pairwise ARI across 435 seed pairs on the unperturbed data) is reported as an explicit secondary column for stochastic estimators, noting that deterministic estimators trivially achieve $\text{Seed}^* \equiv 1.000$."
        )
        assert old_sec32_redundancy in content, "Section 3.2 redundancy not found"
        content = content.replace(old_sec32_redundancy, new_sec32_redundancy)

        # 15. Section 3.2: 9 discordant cells breakdown
        old_sec32_disc = (
            r"Across all six high-$D$ cohorts, three methods satisfy the amended non-degenerate stability-accuracy discordance criterion (Decision Rule~(i'): subsample stability $\ge 0.50$, empirical accuracy $\le 0.05$, and minority cluster size $\ge 5\%$ in at least $90\%$ of subsamples) across three distinct cohorts: FCAG (Colon, CNS, Prostate), FCM (Colon, CNS, Ovarian), and FastMVC (Colon, CNS, Prostate)."
        )
        new_sec32_disc = (
            r"Across all six high-$D$ cohorts, three methods satisfy the non-degenerate stability-accuracy discordance criterion (Decision Rule~(i'): subsample stability $\ge 0.50$, empirical accuracy $\le 0.05$, and minority cluster size $\ge 5\%$ in at least $90\%$ of subsamples) across three distinct cohorts: FCAG (Colon, CNS, Prostate), FCM (Colon, CNS, Ovarian), and FastMVC (Colon, CNS, Prostate). Over these nine discordant method-cohort cells, mean stability is $0.684$ while empirical accuracy collapses to chance (mean $\text{Acc} = -0.003$). Averaging across all 18 cells for these three methods (including non-discordant cohorts such as SRBCT and Leukemia) yields an aggregate stability of $0.638$ and accuracy of $0.046$."
        )
        assert old_sec32_disc in content, "Section 3.2 discordant cells not found"
        content = content.replace(old_sec32_disc, new_sec32_disc)

        # 16. Section 3.2: Bootstrap specification
        old_sec32_boot = (
            r"Paired bootstrap resampling across all six cohorts ($B=10{,}000$) reveals an overall mean stability--accuracy gap of $+0.485$ excluding degenerate partitions (95\% CI: $[+0.379, +0.662]$) and $+0.464$ across all partition pairs (95\% CI: $[+0.363, +0.607]$). Both intervals strictly exclude zero, validating pre-specified Decision Rule~(iii)."
        )
        new_sec32_boot = (
            r"To evaluate whether excess stability is statistically robust, we conducted a dataset-clustered bootstrap ($B=10{,}000$ iterations) that resamples cohorts with replacement, pooling paired differences across non-degenerate methods. Excess stability over unstructured noise ($\text{Stab} - \text{Null}$) averages $+0.472$ (95\% CI: $[+0.368, +0.645]$), while permuted-null stability stays near zero ($-0.003$ to $+0.049$). The paired stability--accuracy gap averages $+0.485$ across non-degenerate partitions (95\% CI: $[+0.379, +0.662]$) and $+0.464$ across all partitions (95\% CI: $[+0.363, +0.607]$). Crucially, the excess stability ($\text{Stab} - \text{Null} \ge 0.10$) confirms that base clusterers converge onto genuine, reproducible manifold geometry rather than noise artifacts, even as accuracy remains near zero."
        )
        assert old_sec32_boot in content, "Section 3.2 bootstrap not found"
        content = content.replace(old_sec32_boot, new_sec32_boot)

        # 17. Section 4.2: operational driver -> computational compressor
        content = content.replace(
            r"showing that bipartite graph compression rather than determinacy anchor selection is the primary operational driver.",
            r"showing that bipartite graph compression acts primarily as an efficient computational compressor ($O(NL)$ memory) rather than a selective landmark filter."
        )

        # 18. Section 5.2: Seed schedule
        old_sec52_seeds = (
            r"\item \textbf{Benchmark Replications:} To obtain dependable variance estimates while keeping overall compute tractable, each method was run across 30 independent random seeds ($\mathcal{S}_{\text{high}} = \{42, 43, \dots, 71\}$) on the six high-dimensional ($D/N > 20$) cohorts, and across 10 random seeds ($\mathcal{S}_{\text{other}} = \{42, 43, \dots, 51\}$) on the remaining seven cohorts. This yielded a total of $(6 \times 12 \times 30) + (7 \times 12 \times 10) = 3{,}000$ independent benchmark model executions across the 12 algorithms."
        )
        new_sec52_seeds = (
            r"\item \textbf{Benchmark and Sub-Experiment Replications:} For the omnibus benchmark evaluation (Table~\ref{tab:benchmark_ari}), algorithms were evaluated across 30 independent random seeds ($\mathcal{S}_{\text{high}} = \{42, 43, \dots, 71\}$) on the six high-$D$ cohorts ($D/N > 20$), and across 10 random seeds ($\mathcal{S}_{\text{other}} = \{42, 43, \dots, 51\}$) on the remaining seven cohorts ($3{,}000$ total model fits). For the modular ablation runs, feature gating comparisons, and anchor sensitivity sweeps (Sections~\ref{sec:benchmarks_suite} and \ref{sec:ablation}), a standard secondary sequence of 30 seeds ($\mathcal{S}_{\text{sub}} = \{0, 1, \dots, 29\}$) was used, with both schedules pre-specified to guarantee reproducibility across independent batches."
        )
        assert old_sec52_seeds in content, "Section 5.2 seeds not found"
        content = content.replace(old_sec52_seeds, new_sec52_seeds)

        # 19. Section 5.2: K-Means initialization reconciliation note
        old_init_note = r"Evaluating all algorithms under identical off-the-shelf defaults guarantees a level, leak-free, and directly reproducible comparison."
        new_init_note = (
            r"Evaluating all algorithms under standardized configurations guarantees reproducible comparison. "
            r"Note on K-Means initialization: while Table~\ref{tab:method_parameters} reports the standard scikit-learn "
            r"standalone default ($n_{\text{init}}=10$), the 13-benchmark omnibus evaluation in Table~\ref{tab:benchmark_ari} "
            r"uses single-restart K-Means ($n_{\text{init}}=1$, subgroup mean $0.056$) to provide a direct baseline "
            r"counterpart to individual ensemble base clusterers, whereas the matched-budget sweeps in Table~\ref{tab:fair_baselines} "
            r"use $n_{\text{init}}=5$ ($0.051$) following standard feature selection benchmark conventions."
        )
        assert old_init_note in content, "Init note not found"
        content = content.replace(old_init_note, new_init_note)

        # 20. Table 2: Category label Proposed -> Evaluated Pipeline
        content = content.replace(
            r"\multirow{4}{*}{\textbf{Proposed}} & \multirow{4}{*}{\textbf{GAC}}",
            r"\multirow{4}{*}{\textbf{Evaluated Pipeline}} & \multirow{4}{*}{\textbf{GAC}}"
        )

        # 21. Section 6.1: Inductive agreement range (includes Isolet at 85.0%)
        content = content.replace(
            r"agrees with unweighted nearest-centroid assignments on $94.1\%$--$99.2\%$ (mean $95.3\%$) of test instances.",
            r"agrees with unweighted nearest-centroid assignments on $85.0\%$--$99.2\%$ of test instances across datasets (mean $95.3\%$, with Isolet yielding $85.0\%$ and microarray cohorts spanning $94.1\%$--$99.2\%$; Table~\ref{tab:inductive_direct})."
        )

        # 22. Section 6.1: Scalability timing at N=10,000 (Table 5 Config A says 1.29)
        content = content.replace(
            r"($5.58 \pm 0.63\text{ s}$ at $N=10{,}000$)",
            r"($5.58 \pm 1.29\text{ s}$ at $N=10{,}000$)"
        )

        # 23. Section 6.1: Soften small-scale speedup
        old_speedup = r"Resource profiling across metrics (Fig.~\ref{fig:exp4_quad}) confirms that bipartite anchor consensus accelerates execution across sample scales while maintaining a modest memory footprint."
        new_speedup = r"Resource profiling across metrics (Fig.~\ref{fig:exp4_quad}) shows that bipartite anchor consensus exhibits runtime comparable to dense consensus at small sample scales ($N \le 5{,}000$, speedups $0.92\times\text{--}1.16\times$ due to baseline overheads) and accelerates substantially as sample size expands, reaching a $2.54\times$ speedup at $N = 10{,}000$ (Table~\ref{tab:exp4_timing}) while maintaining a modest memory footprint."
        assert old_speedup in content, "Speedup sentence not found"
        content = content.replace(old_speedup, new_speedup)

        # 24. Fig 6 caption: RAM scaling and beta
        old_fig6 = r"while peak process RAM footprint remains bounded under $4\text{ GB}$."
        new_fig6 = r"while auxiliary bipartite graph memory is strictly bounded ($160\text{ MB}$ for Config A vs. $8\text{ TB}$ for dense consensus) and total process heap memory grows with raw array storage to $3.84\text{ GB}$ at $N=10^6$."
        assert old_fig6 in content, "Fig 6 caption not found"
        content = content.replace(old_fig6, new_fig6)

        # 25. Section 6.2: Soften bipartite attribution
        old_sec62_att = (
            r"Most of the improvement over ambient consensus ($0.037$) comes from combining random subspace selection with bipartite consensus ($0.037 \to 0.155$, gain $+0.118$), with BGSS multimodality gating contributing an added $+0.062$."
        )
        new_sec62_att = (
            r"Most of the improvement over ambient consensus ($0.037$) comes from ensembling over random feature subspaces within the bipartite consensus pipeline ($0.037 \to 0.155$, gain $+0.118$), which dilutes per-clusterer noise exposure, with BGSS multimodality gating contributing an added $+0.062$. By contrast, running bipartite consensus on the full ambient feature space without subspace gating ($V_3$, Table~\ref{tab:factorial}) yields only $0.046$ ($\Delta = +0.009$), confirming that feature subsampling rather than graph bipartite factorization drives this gain."
        )
        assert old_sec62_att in content, "Section 6.2 attribution not found"
        content = content.replace(old_sec62_att, new_sec62_att)

        # 26. Section 7.3: Attenuating co-associations conjecture
        old_coassoc = r"In addition to accelerating computation, bipartite compression helps attenuate spurious off-diagonal noise co-associations."
        new_coassoc = r"Bipartite graph compression provides dramatic computational and memory savings ($O(NL)$ vs. $O(N^2)$), though whether anchor factorization theoretically attenuates spurious off-diagonal noise co-associations remains an open conjecture that is not independently isolated by our factorial cells."
        assert old_coassoc in content, "Coassoc sentence not found"
        content = content.replace(old_coassoc, new_coassoc)

        # 27. Section 7.5: Golub marker baselines
        old_golub = (
            r"When cross-referenced against the top 50 supervised diagnostic marker genes established for the Leukemia cohort (Golub et al., 1999; OpenML ID: 1104), BGSS captures \AblationLeukemiaMarkerFiftyCount\ of the 50 markers (\AblationLeukemiaMarkerFiftyFraction\ overlap, Fig.~\ref{fig:bgss_saliency}) purely unsupervised in $O(N \cdot D)$ time."
        )
        new_golub = (
            r"When cross-referenced against the top 50 supervised diagnostic marker genes established for the Leukemia cohort~\cite{golub1999molecular}, the top 1,069 features selected by BGSS ($\alpha = 0.15$) capture \AblationLeukemiaMarkerFiftyCount\ of the 50 markers (\AblationLeukemiaMarkerFiftyFraction\ overlap, Fig.~\ref{fig:bgss_saliency}) purely unsupervised in $O(N \cdot D)$ time. Under random feature selection, drawing 1,069 of 7,129 genes yields an expected overlap of only $1{,}069 \times (50 / 7{,}129) \approx 7.50$ markers ($15.0\%$), confirming strong statistical enrichment under a hypergeometric test ($k=27, n=1{,}069, K=50, N=7{,}129$; $p = 1.38 \times 10^{-10}$). By comparison, selecting the top 1,069 features by sample variance captures only 8 of the 50 markers ($16.0\%$), performing no better than random expectation because uninformative noise coordinates exhibit substantial variance."
        )
        assert old_golub in content, "Golub text not found"
        content = content.replace(old_golub, new_golub)

        # 28. Fig 10 caption
        old_fig10 = (
            r"\caption{BGSS interpretability audit and diagnostic marker recovery on the Leukemia microarray cohort ($N=72, D=7{,}129$). Demonstrates that BGSS captures 27 of the top 50 supervised markers ($54.0\%$) purely unsupervised in $O(N \cdot D)$ time while filtering uninformative unimodal noise dimensions.}"
        )
        new_fig10 = (
            r"\caption{BGSS interpretability audit and diagnostic marker recovery on the Leukemia microarray cohort ($N=72, D=7{,}129$). Demonstrates that unsupervised BGSS captures 27 of the top 50 supervised markers from Golub et al.~\cite{golub1999molecular} ($54.0\%$ vs. $7.50$ [$15.0\%$] expected under random selection; hypergeometric $p = 1.38 \times 10^{-10}$), whereas standard variance filtering captures only 8 of 50 markers ($16.0\%$).}"
        )
        assert old_fig10 in content, "Fig 10 caption not found"
        content = content.replace(old_fig10, new_fig10)

        # 29. Discussion 8.1
        old_disc81 = (
            r"Bipartite random-subspace ensembling accounts for $+0.118$ ($65.6\%$) of the $+0.180$ gain over ambient consensus. BGSS adds a modest $+0.062$ over matched random gating (95\% CI $[+0.013, +0.142]$, Wilcoxon $p = 0.0625$), while determinacy-based anchor selection yields no measurable benefit ($\Delta = +0.019$, 95\% CI $[-0.039, +0.082]$)."
        )
        new_disc81 = (
            r"Ensembling over random subspaces within the bipartite architecture accounts for $+0.118$ ($65.6\%$) of the $+0.180$ gain over ambient consensus ($0.037 \to 0.155$), while bipartite graph compression alone yields only $+0.009$ ($0.037 \to 0.046$). BGSS adds a modest $+0.062$ over matched random gating (95\% CI $[+0.013, +0.142]$, Wilcoxon $p = 0.0625$), while determinacy-based anchor selection yields no measurable benefit ($\Delta = +0.019$, 95\% CI $[-0.039, +0.082]$)."
        )
        assert old_disc81 in content, "Discussion 8.1 not found"
        content = content.replace(old_disc81, new_disc81)

        # 30. Conclusion 9
        old_conc = (
            r"Bipartite random-subspace ensembling accounts for $+0.118$ ($65.6\%$) of the $+0.180$ gain over ambient consensus on the six high-$D$ cohorts, and Bimodality-Gated Subspace Selection adds a modest $+0.062$ over matched random gating (95\% CI $[+0.013, +0.142]$, Wilcoxon $p = 0.0625$)."
        )
        new_conc = (
            r"Ensembling over random subspaces within the bipartite pipeline accounts for $+0.118$ ($65.6\%$) of the $+0.180$ empirical gain over ambient consensus on the six high-$D$ cohorts ($0.037 \to 0.155$), whereas bipartite graph compression without gating provides $+0.009$ ($0.037 \to 0.046$). Bimodality-Gated Subspace Selection adds $+0.062$ over matched random gating (95\% CI $[+0.013, +0.142]$, Wilcoxon $p = 0.0625$)."
        )
        assert old_conc in content, "Conclusion not found"
        content = content.replace(old_conc, new_conc)

        # 31. Declarations: Competing interests and Author contributions
        old_decl = r"\textbf{Funding}: No external funding was received for this study."
        new_decl = (
            r"\textbf{Funding}: No external funding was received for this study."
            "\n\n"
            r"\textbf{Competing Interests}: The authors declare that they have no competing financial or non-financial interests that could have appeared to influence the work reported in this paper."
            "\n\n"
            r"\textbf{Author Contributions}: All authors contributed to the study conception and design. Kalyan Kumar Das and Akash Kundu developed the experimental codebase, executed the computational simulations and benchmark evaluations, and drafted the initial manuscript. Anirban Mukhopadhyay provided methodological guidance, oversaw the statistical analysis and validation protocols, and critically reviewed and revised the manuscript. All authors read and approved the final manuscript."
        )
        assert old_decl in content, "Funding declaration not found"
        content = content.replace(old_decl, new_decl)

        # Save back
        p.write_text(content, encoding="utf-8")
        print(f"Successfully applied all fixes to {p}!")

if __name__ == "__main__":
    apply_fixes()
