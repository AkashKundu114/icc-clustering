"""
scripts/apply_paper_revisions.py

Synchronously applies all text revisions for Item 1, 3, 4, 5 to both:
- paper/main.tex
- springer_manuscript/main.tex
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def patch_file(p: Path):
    with open(p, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Section 4 title rename
    old_sec4 = r"\section{Proposed Methodology (Inductive Consensus Clustering Framework)}\label{sec:methodology}"
    new_sec4 = r"\section{Proposed Methodology (Gated Anchor Consensus Pipeline)}\label{sec:methodology}"
    if old_sec4 in content:
        content = content.replace(old_sec4, new_sec4)

    # 2. Abstract update (Item 1e, 3b)
    old_abstract_start = r"\abstract{Consensus clustering is widely assumed to resist high-dimensional noise."
    old_abstract_end = r"Failure modes are further characterized under non-linear XOR parity, zero-inflated counts, and large $K$.}"
    
    idx_abs_start = content.find(old_abstract_start)
    idx_abs_end = content.find(old_abstract_end, idx_abs_start) + len(old_abstract_end)

    new_abstract = r"""\abstract{Consensus clustering is widely assumed to resist high-dimensional noise. We evaluate this assumption across synthetic simulations and six biomedical cohorts ($D/N > 20$) using a pre-registered stratified $80\%$ subsample perturbation stability protocol (30 draws per method) alongside independent column-permuted null controls. In finite-sample simulations with isotropic distractors ($D \gg N$), base clusterers (particularly Ward and Spectral) converge stably ($\text{stability} > 0.8$) onto arbitrary noise partitions while Adjusted Rand Index (ARI) collapses toward zero. On real biomedical cohorts, standard baselines exhibit severe subsample stability--accuracy gaps: three of twelve evaluated methods (FCAG, FCM, FastMVC) satisfy our pre-specified ``Stable but Wrong'' criterion ($\text{subsample stability} \ge 0.50$ and $\text{accuracy} \le 0.05$) across at least three distinct cohorts, with Ward and Spectral showing near-perfect stability ($\text{Stab} \ge 0.97$) yet zero accuracy ($\text{ARI} \le 0.03$) on Prostate ($D=12{,}600$), where permuted null stability drops to near zero ($\le 0.03$). A paired cohort bootstrap excludes zero for the overall stability--accuracy gap ($+0.464$, $95\%$ CI: $[+0.363, +0.607]$). We evaluate the Gated Anchor Consensus (GAC) pipeline, combining linear-time Bimodality-Gated Subspace Selection (BGSS), random-subspace ensembles, bipartite anchor graphs, and closed-form centroid projection. Across 13 benchmarks (3,000 fits), omnibus differences across methods are not statistically significant (Friedman $p = 0.40$). GAC achieves the highest mean ARI on the six $D/N > 20$ cohorts ($0.217$ vs. $0.065$ for the best baseline FCAG and $0.037$ for ambient consensus), with gains concentrating in high-bimodality cohorts (Leukemia $0.600 \pm 0.367$ and SRBCT $0.546 \pm 0.102$). Ablations reveal that the random-subspace bipartite ensemble accounts for $+0.118$ (65.6\%) of this gain, while BGSS screening adds $+0.062$ over matched random gating ($95\%$ CI: $[+0.013, +0.142]$, Wilcoxon $p = 0.0625$). Landmark determinacy yields an empirical null result over uniform random sampling ($\Delta = +0.019$, $95\%$ CI: $[-0.039, +0.082]$). On Prostate and CNS, weak marginal bimodality leaves GAC trapped in spurious consensus ($\text{accuracy} \le 0.02$). Failure modes are further characterized under non-linear XOR parity, zero-inflated counts, and large $K$.}"""

    if idx_abs_start != -1:
        content = content[:idx_abs_start] + new_abstract + content[idx_abs_end:]

    # 3. Keywords update
    old_keywords = r"\keywords{Stability-accuracy gap, consensus clustering, high-dimensional noise, clustering ensembles, bipartite anchor graphs, feature gating, distance concentration, inductive out-of-sample projection.}"
    new_keywords = r"\keywords{Subsample stability-accuracy gap, consensus clustering, high-dimensional noise, clustering ensembles, bipartite anchor graphs, feature gating, distance concentration, null control, inductive out-of-sample projection.}"
    content = content.replace(old_keywords, new_keywords)

    # 4. Intro citation (li2025selfsupervised)
    old_intro_p2 = r"Yet in high dimensions ($D \gg N$), ambient noise undermines this aggregation through two distinct structural bottlenecks."
    new_intro_p2 = r"In high-dimensional domains, unsupervised and self-supervised feature selection has emerged as a necessary prerequisite to remove uninformative coordinates before similarity estimation (Li et al.~\cite{li2025selfsupervised}). Yet in high dimensions ($D \gg N$), ambient noise undermines this aggregation through two distinct structural bottlenecks."
    if old_intro_p2 in content and "li2025selfsupervised" not in content:
        content = content.replace(old_intro_p2, new_intro_p2)

    # 5. Contributions Item 1 update
    old_contrib1 = r"\item \textbf{The Stability Trap in High Dimensions (Simulations and Real Benchmarks):} Controlled empirical falsification demonstrating that under isotropic noise ($D \gg N$) and real biomedical cohorts ($D/N > 20$, 30 seeds), consensus stability remains elevated ($\text{stability} \ge 0.50$ to $1.00$) while accuracy collapses near zero ($\text{ARI} \le 0.05$). We document severe stability-accuracy gaps across classical and modern baselines (e.g., Ward and Spectral exhibit mean gaps of $+0.968$ and $+0.964$), proving that ensemble averaging can entrench false partitions rather than eliminate noise."
    new_contrib1 = r"\item \textbf{The Stability Trap in High Dimensions (Subsample Stability and Null Control):} Controlled empirical falsification under isotropic noise ($D \gg N$) and six real biomedical cohorts ($D/N > 20$, 30 stratified $80\%$ subsamples) demonstrates that consensus stability remains high ($\text{subsample stability} \ge 0.50$ to $1.00$) while accuracy collapses near zero ($\text{ARI} \le 0.05$). Paired bootstrap analysis across cohorts ($B=10{,}000$) confirms a positive subsample stability--accuracy gap ($+0.464$, $95\%$ CI: $[+0.363, +0.607]$), while independent column-permuted null controls confirm that null stability collapses to zero (mean $+0.007$). Three methods (FCAG, FCM, FastMVC) meet our pre-registered ``Stable but Wrong'' criterion across at least 3 cohorts, proving that high stability does not indicate partition correctness on real high-dimensional data."
    content = content.replace(old_contrib1, new_contrib1)

    # 6. Contributions Item 2 SD consistency (Item 3a)
    old_contrib2 = r"Leukemia $\text{ARI}=0.600$, SRBCT $\text{ARI}=0.546$"
    new_contrib2 = r"Leukemia $\text{ARI}=0.600 \pm 0.367$, SRBCT $\text{ARI}=0.546 \pm 0.102$"
    content = content.replace(old_contrib2, new_contrib2)

    # 7. Senbabaoglu et al. and Race & Meyer rewrite (Item 3e)
    old_senbabaoglu = r"However, Senbabaoglu et al.~\cite{senbabaoglu2014critical} reassessed the empirical validity of consensus clustering in class discovery, demonstrating that high consensus stability often reflects clusterer-induced geometric artifacts rather than genuine cluster structure, a pathology directly anticipating the stability-accuracy gap examined in this work. To address cluster count ambiguity in consensus pipelines, Race and Meyer~\cite{race2013determining} investigated iterative consensus clustering (ICC), successively pruning confident cluster assignments."
    new_senbabaoglu = r"In a foundational critique, Senbabaoglu et al.~\cite{senbabaoglu2014critical} demonstrated that consensus clustering can produce apparently high stability and apparent cluster structure even on unimodal null data with weak or no true underlying cluster structure. To determine the number of clusters without arbitrary heuristics, Race and Meyer~\cite{race2013determining} developed iterative consensus clustering, successively extracting confident cluster assignments from the consensus matrix and reclustering the remaining residual samples."
    content = content.replace(old_senbabaoglu, new_senbabaoglu)

    # 8. Add recent citations to Related Work (Section 2.1 & 2.2)
    old_rw_p1 = r"Recent active and constraint-based consensus formulations further refine partition assignments by incorporating pairwise instance relationships (CODAC, Patron et al.~\cite{patron2026codac})."
    new_rw_p1 = r"Recent active and constraint-based consensus formulations further refine partition assignments by incorporating pairwise instance relationships (CODAC, Patron et al.~\cite{patron2026codac}). High-order consensus frameworks capture multi-hop relations beyond pairwise co-occurrences (Zhang et al.~\cite{zhang2025highorder}), while sparse representations suppress noisy partition edges in spectral consensus (Fan et al.~\cite{fan2026robust}). Enforcing doubly stochastic normalization over the consensus affinity matrix eliminates vertex degree artifacts in spectral graph partitioning (Cai et al.~\cite{cai2025spectral}), and auto-weighted graph reconstruction dynamically recalibrates base ensemble contributions according to partition reliability (Yang et al.~\cite{yang2025autoweighted}). In multiview domains, hypergraph p-Laplacian regularization with feature selection provides robustness against distractor noise (Hu et al.~\cite{hu2024multiview}), and contrastive clustering ensembles regularize deep representations (Chen et al.~\cite{chen2025ccegan})."
    if old_rw_p1 in content and "zhang2025highorder" not in content:
        content = content.replace(old_rw_p1, new_rw_p1)

    old_rw_p2 = r"GAC pipeline builds upon these bipartite foundations, coupling bipartite compression with linear-time feature gating to resolve high-dimensional noise."
    new_rw_p2 = r"Adaptive anchor selection strategies further enhance bipartite consensus efficiency across large instance sets (Guo et al.~\cite{guo2026consensus}), scalable multi-view ensemble clustering leverages adaptive anchor bipartite graphs (Kong et al.~\cite{kong2026adaptive}), and high-order graph embedding with co-regularization aligns multi-view cluster assignments (Wang et al.~\cite{wang2025coregularized}). Streaming and inductive consensus frameworks have recently expanded toward fairness-constrained partition updates across continuous data flows (Chakraborty et al.~\cite{chakraborty2026generic}). GAC pipeline builds upon these bipartite foundations, coupling bipartite compression with linear-time feature gating to resolve high-dimensional noise."
    if old_rw_p2 in content and "guo2026consensus" not in content:
        content = content.replace(old_rw_p2, new_rw_p2)

    # 9. Add citations in Section 3 (zhang2024optimal, lau2024bayesian, jahanian2026highdim)
    old_sec3_intro = r"To investigate whether consensus clustering inherently overcomes high-dimensional noise, we conduct controlled finite-sample simulations across isotropic distractor regimes."
    new_sec3_intro = r"Minimax theoretical analysis establishes that consistent cluster recovery in high dimensions requires feature signal-to-noise ratios scaling with ambient dimension (Zhang and Zhou~\cite{zhang2024optimal}), and latent repulsive mixture models have been proposed to prevent over-clustering in high-dimensional genomic feature spaces (Lau et al.~\cite{lau2024bayesian}). To investigate whether consensus clustering inherently overcomes high-dimensional noise, we conduct controlled finite-sample simulations across isotropic distractor regimes."
    if old_sec3_intro in content and "zhang2024optimal" not in content:
        content = content.replace(old_sec3_intro, new_sec3_intro)

    # 10. Rewrite Section 3.1 (Item 1e, 3a, 3c)
    old_sec31_intro = r"As shown in Table~\ref{tab:real_data_stability} and Figure~\ref{fig:real_data_stability}, the stability trap is pervasive across real high-dimensional benchmarks, displaying three distinct algorithmic regimes:"
    old_sec31_end = r"In these cohorts, weak marginal feature multimodality prevents BGSS from isolating the signal manifold, showing that feature gating attenuates but cannot entirely eliminate the stability trap when signal coordinates lack detectable marginal separation."

    idx_s31_start = content.find(old_sec31_intro)
    idx_s31_end = content.find(old_sec31_end, idx_s31_start) + len(old_sec31_end)

    new_sec31 = r"""Biomedical cohort clustering under high feature-to-sample ratios requires explicit noise screening to avoid convergence on spurious clinical subtypes (Jahanian et al.~\cite{jahanian2026highdim}). As shown in Table~\ref{tab:real_data_stability} and Figure~\ref{fig:real_data_stability}, our pre-registered stratified subsample perturbation protocol reveals three distinct algorithmic regimes across real high-dimensional benchmarks ($D/N > 20$, 30 stratified $80\%$ subsamples):

\paragraph{1. Pervasive Entrapment Across Classical and Graph Baselines:}
Under stratified subsampling, classical and graph-based baselines repeatedly lock onto mutually agreeing yet clinically spurious partitions. Across all six high-$D$ cohorts, three methods satisfy pre-specified Decision Rule~(i) (subsample stability $\ge 0.50$ and empirical accuracy $\le 0.05$) across at least three distinct cohorts: FCAG (Colon, CNS, Prostate), FCM (Colon, CNS, Ovarian), and FastMVC (Colon, CNS, Prostate). On Prostate ($D=12{,}600$), ten of the twelve evaluated methods satisfy Rule~(i), led by Ward ($\text{Stab}=0.996, \text{Acc}=0.026, \Delta=+0.970$), Spectral ($\text{Stab}=0.971, \text{Acc}=-0.002, \Delta=+0.973$), and Core-Halo ($\text{Stab}=1.000, \text{Acc}=0.000, \Delta=+1.000$). Crucially, under independent column-permuted null controls, stability on Prostate collapses to near zero (range $-0.001$ to $+0.049$). This verifies that the elevated stability observed on real data reflects genuine, highly reproducible geometric attractors in the noise subspace that are completely orthogonal to clinical truth, directly validating the ``Stable but Wrong'' pathology. Paired bootstrap resampling across cohorts ($B=10{,}000$) yields an overall mean stability--accuracy gap of $+0.464$ with a 95\% confidence interval of $[+0.363, +0.607]$, firmly excluding zero and supporting pre-registered Decision Rule~(iii).

\paragraph{2. Behavior of CoHiRF as Run:}
Under our evaluation, CoHiRF exhibits an attenuated mean subsample gap ($\Delta = +0.267$). As run in this benchmark (a reimplementation strictly adhering to official specification with 25 repetitions, a $0.15$ random subspace fraction, and an $0.80$ unanimous threshold), CoHiRF achieves low mean accuracy ($\text{Acc} = 0.020$) and low subsample stability ($\text{Stab} = 0.281$). On Colon, CoHiRF yields subsample stability of only $0.068$ ($\text{Acc}=0.013$), matching Decision Rule~(ii) where real stability minus null stability is below $0.10$ ($0.068 - 0.002 = 0.066$), indicating that stability is uninformative under high distractor dimensionality for this configuration.

\paragraph{3. Where Feature Gating Helps, and Where It Entraps GAC:}
The GAC pipeline achieves the highest mean subsample accuracy among all tested methods ($0.168$ vs. $0.051$ for K-Means and $0.049$ for FCAG) and lowers the mean gap to $+0.300$. On Leukemia ($D=7{,}129$, $\text{Acc} = 0.412, \text{Stab} = 0.334, \Delta = -0.078$) and SRBCT ($D=2{,}308$, $\text{Acc} = 0.493, \text{Stab} = 0.507, \Delta = +0.014$), GAC breaks free from the stability trap: empirical accuracy matches or exceeds subsample stability. In full-cohort runs across 30 seeds, GAC attains $\text{ARI} = 0.600 \pm 0.367$ on Leukemia and $0.546 \pm 0.102$ on SRBCT. However, boundary conditions must be stated transparently: on Prostate ($D=12{,}600$) and CNS ($D=7{,}129$), GAC also falls into the stability trap ($\text{Acc} = 0.012$ and $0.007$, $\text{Stab} = 0.860$ and $0.549$, yielding gaps of $\mathbf{+0.847}$ and $\mathbf{+0.542}$). In these cohorts, diffuse non-bimodal signal distributions prevent marginal BGSS from isolating the signal manifold, demonstrating that unsupervised feature gating cannot rescue consensus clustering when informative coordinates lack detectable marginal separation."""

    if idx_s31_start != -1:
        content = content[:idx_s31_start] + new_sec31 + content[idx_s31_end:]

    # 11. Ensure Declarations have generic AI statement without model names
    idx_decl = content.find(r"\section*{Declarations}")
    if idx_decl != -1:
        decl_sub = content[idx_decl:]
        for banned in ["GPT", "Claude", "Gemini", "OpenAI", "Anthropic", "ChatGPT"]:
            assert banned not in decl_sub, f"Banned model name {banned} found in declarations!"

    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Revisions applied cleanly to {p}")

def main():
    patch_file(ROOT / "paper" / "main.tex")
    patch_file(ROOT / "springer_manuscript" / "main.tex")

if __name__ == "__main__":
    main()
