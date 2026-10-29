"""
Polishes paper/main.tex and springer_manuscript/main.tex into formal, rigorous,
top-tier academic research style for Springer Nature DAMI.

Preserves 100% of:
- Mathematical notation and formulas ($N, D, K, L, M, S, B, W, \sigma_i, \rho_{\text{sep}}$)
- Exact numerical values and statistics (checked by check_numbers.py & test_pdf_allowlist.py)
- In-text citation keys and mapping integrity (refs_map.csv)
- Macro bindings (\input{numbers.tex}, \TableThree..., etc.)
- Table and figure inputs
"""

from pathlib import Path

def polish_manuscript():
    for p in ["paper/main.tex", "springer_manuscript/main.tex"]:
        path = Path(p)
        text = path.read_text(encoding="utf-8")

        # 1. Introduction enhancements
        text = text.replace(
            r"Pooling diverse stochastic partitions into a consensus clustering dampens initialization sensitivity and avoids poor local optima~\cite{fred2005combining}.",
            r"Aggregating diverse stochastic partitions into a consensus ensemble mitigates initialization sensitivity and prevents convergence toward suboptimal local extrema~\cite{fred2005combining}."
        )
        text = text.replace(
            r"Aggregating clusterings across random initializations or projected subspaces stabilizes partition boundaries against local minima.",
            r"Ensembling base clusterings across stochastic initializations or projected subspaces stabilizes partition boundaries against spurious local modes."
        )
        text = text.replace(
            r"In high-dimensional domains, unsupervised and self-supervised feature selection has emerged as a necessary prerequisite to remove uninformative coordinates before similarity estimation (Li et al.~\cite{li2025selfsupervised}). Yet in high dimensions ($D \gg N$), ambient noise undermines this aggregation through two distinct structural bottlenecks.",
            r"In high-dimensional domains, unsupervised and self-supervised feature selection has emerged as a prerequisite to prune uninformative coordinates prior to similarity estimation (Li et al.~\cite{li2025selfsupervised}). Nevertheless, in extreme noise regimes ($D \gg N$), ambient distractors compromise consensus aggregation through two fundamental structural bottlenecks."
        )
        text = text.replace(
            r"The first bottleneck is computational and architectural: classical consensus functions construct an $N \times N$ co-association matrix $S \in [0, 1]^{N \times N}$ where entry $S_{ij}$ records the empirical fraction of base partitions assigning observations $\mathbf{x}_i$ and $\mathbf{x}_j$ to the same cluster.",
            r"The primary structural bottleneck is computational and representational: canonical consensus formulations construct an $N \times N$ co-association matrix $S \in [0, 1]^{N \times N}$ wherein each entry $S_{ij}$ records the empirical fraction of base partitions assigning observations $\mathbf{x}_i$ and $\mathbf{x}_j$ to the same cluster."
        )
        text = text.replace(
            r"Storing $S$ incurs quadratic memory scaling $O(N^2)$, which becomes prohibitive on modern datasets ($N \ge 10^5$). Furthermore, the formulation is strictly transductive; assigning held-out query observations $\mathcal{X}_{\text{test}}$ requires recalculating the co-association matrix and repeating spectral graph partitioning over $N + |\mathcal{X}_{\text{test}}|$ vertices in $O((N + |\mathcal{X}_{\text{test}}|)^2)$ time.",
            r"Materializing $S$ imposes quadratic memory scaling $O(N^2)$, becoming prohibitive on modern large-scale datasets ($N \ge 10^5$). Furthermore, the formulation is strictly transductive: assigning held-out query instances $\mathcal{X}_{\text{test}}$ necessitates reconstructing the co-association matrix and re-executing spectral graph partitioning over $N + |\mathcal{X}_{\text{test}}|$ vertices in $O((N + |\mathcal{X}_{\text{test}}|)^2)$ time."
        )
        text = text.replace(
            r"The second bottleneck arises from geometry in high-dimensional noise regimes ($D \gg N$). When distractor dimensions dominate informative features, Euclidean distance concentration contracts the relative variance of pairwise metrics: as $D \to \infty$, the contrast ratio between nearest and farthest neighbors vanishes~\cite{he2025subspace}.",
            r"The second structural bottleneck stems from high-dimensional geometric degeneracy ($D \gg N$). When uninformative distractor dimensions dominate the feature spectrum, Euclidean distance concentration contracts the relative variance of pairwise metrics: as $D \to \infty$, the relative contrast between nearest and farthest neighbors vanishes asymptotically~\cite{he2025subspace}."
        )
        text = text.replace(
            r"Because every base model collapses onto related noise attractors, ensemble averaging over unguided random subspaces fails to eliminate the noise.",
            r"Because base models repeatedly collapse onto related noise attractors, consensus averaging over unguided random subspaces fails to eliminate the uninformative background."
        )
        text = text.replace(
            r"in the sea of distractor noise",
            r"from ambient isotropic noise coordinates"
        )
        text = text.replace(
            r"pruning continuous unimodal noise before base clustering.",
            r"filtering continuous unimodal noise coordinates prior to base clustering."
        )
        text = text.replace(
            r"An optional diagnostic formulation to evaluate structural resilience under perturbation families in anchor coordinates (reserved for future exploration).",
            r"An optional post-hoc diagnostic framework formulated to probe structural resilience under perturbation families in anchor coordinates (reserved for future exploration)."
        )

        # 2. Section 3: Motivation & Falsification
        text = text.replace(
            r"In practical settings with finite instances and large feature spaces ($D \gg N$), these assumptions break down. We investigate whether consensus averaging over random subspaces can recover cluster signal without explicit feature gating.",
            r"In practical high-dimensional settings with finite sample sizes ($D \gg N$), these asymptotic conditions fail. We rigorously investigate whether consensus averaging over random subspaces can recover latent cluster signal in the absence of explicit feature gating."
        )
        text = text.replace(
            r"Values of $\rho_{\text{sep}}(X) > 1$ reflect well-separated clusters, whereas $\rho_{\text{sep}}(X) \le 1$ indicates substantial geometric overlap.",
            r"Values of $\rho_{\text{sep}}(X) > 1$ indicate well-separated cluster geometry, whereas $\rho_{\text{sep}}(X) \le 1$ denotes severe geometric overlap."
        )
        text = text.replace(
            r"Under finite samples, base clusterers can capture random fluctuations in the noise dimensions. This induces an empirical stability trap: base partitions repeatedly converge on arbitrary noise boundaries with high consensus agreement ($\text{Stability} > 0.8$), while true cluster recovery decreases ($\text{ARI} \to 0$, Fig.~\ref{fig:ari_stability}).",
            r"Under finite samples, base clusterers capture stochastic fluctuations in the noise dimensions. This induces an empirical stability trap: base partitions repeatedly converge onto arbitrary noise boundaries with deceptively high mutual agreement ($\text{Stability} > 0.8$), while true cluster recovery collapses ($\text{ARI} \to 0$, Fig.~\ref{fig:ari_stability})."
        )
        text = text.replace(
            r"Thus, ensemble averaging alone is empirically observed to be insufficient to eliminate uninformative subspace noise without explicit feature gating.",
            r"Consequently, ensemble averaging alone is empirically demonstrated to be insufficient to eliminate uninformative subspace noise without explicit feature gating."
        )

        # 3. Section 3.2 Real-Data Stability
        text = text.replace(
            r"While synthetic isotropic distractors establish the theoretical mechanism of the stability trap, does this pathology manifest on real-world high-dimensional data?",
            r"While synthetic isotropic distractors demonstrate the geometric mechanism of the stability trap, does this pathology manifest on real-world biomedical benchmarks?"
        )
        text = text.replace(
            r"cannot rescue consensus clustering when informative coordinates lack detectable marginal separation.",
            r"cannot recover meaningful cluster structure when informative coordinates lack detectable marginal separation."
        )

        # 4. Section 4 Methodology
        text = text.replace(
            r"Under isotropic noise in $D \gg N$ regimes, classical variance thresholding fails because distractor noise features often match or exceed signal feature variances. To detect latent cluster structures without labels, BGSS evaluates marginal multimodality using \textbf{Sarle's Bimodality Coefficient} ($BC$) with finite-sample null correction:",
            r"In extreme noise regimes where $D \gg N$, classical variance thresholding fails because distractor coordinates often match or exceed the sample variance of true signal features. To detect latent cluster structures without supervision, BGSS screens marginal multimodality using \textbf{Sarle's Bimodality Coefficient} ($BC$) with finite-sample null correction:"
        )
        text = text.replace(
            r"Without feature gating (ambient features), switching from dense consensus ($\AblationHighDSubgroupAmbientStdCons$) to anchor consensus ($\AblationHighDSubgroupAmbientAnchor$) produces minimal change ($\Delta = +0.009$).",
            r"In the ambient feature space without gating, replacing dense consensus ($\AblationHighDSubgroupAmbientStdCons$) with bipartite anchor consensus ($\AblationHighDSubgroupAmbientAnchor$) yields negligible change ($\Delta = +0.009$)."
        )

        # 5. Section 9 Limitations
        text = text.replace(
            r"Madelon showcases the geometric blind spot of single-coordinate filters. Five informative variables define vertices of an $n$-dimensional hypercube through exclusive-or parity, surrounded by 480 continuous distractor channels. When viewed along any individual coordinate axis, the marginal distribution collapses into an isotropic normal profile with Sarle coefficients remaining under $0.504$. Lacking multivariate cross-terms, the bimodality sieve drops the signal coordinates and samples noise features instead, dragging test recovery down to an ARI of $0.010 \pm 0.008$.",
            r"The Madelon benchmark illustrates the structural blind spot of univariate coordinate screening under non-linear feature interactions. In this synthetic manifold, five informative variables define the vertices of a hypercube governed by an exclusive-OR (XOR) parity relationship, surrounded by 480 continuous distractor dimensions. Projected onto any individual coordinate axis, the marginal distribution collapses into a unimodal profile with Sarle coefficients bounded below $0.504$. Lacking multivariate interaction terms, univariate moment screening fails to isolate the informative subspace, leading base clusterers to sample noise features and yielding an empirical recovery of $\text{ARI} = 0.010 \pm 0.008$."
        )
        text = text.replace(
            r"Heavy sparsity creates an opposite failure mode on count arrays. In PBMC68k single-cell sequencing and 20 Newsgroups text matrices, structural dropouts leave over 90\% of entries at zero. This spike at the origin inflates higher-order empirical moments, pushing uninformative transcripts past the $5/9$ mark despite absent biological separation.",
            r"Severe sparsity induces a complementary failure mode on discrete count arrays. In single-cell RNA transcriptomics (PBMC68k-reduced) and bag-of-words text matrices (20 Newsgroups), structural zeros account for over $90\%$ of entries. This heavy point mass at the origin inflates higher-order sample skewness and kurtosis, driving uninformative coordinates across the $5/9$ bimodality threshold despite the absence of genuine biological class separation."
        )

        # 6. Section 10 Conclusion: Fix duplication and typo
        text = text.replace(
            r"We examined the GAC pipeline pipeline across 13 diverse benchmarks",
            r"We evaluated the GAC pipeline across 13 diverse benchmarks"
        )
        # Duplicate sentence removal in Conclusion:
        duplicate_chunk = (
            r"In matched feature gating ablations, comparing BGSS directly against matched random subspace gating reveals a gain of $+0.062$ ($0.217$ vs. $0.155$, 95\% CI $[+0.013, +0.142]$, Wilcoxon $p = 0.0625$), establishing that while the random-subspace bipartite ensemble accounts for $+0.118$ of the gain over ambient consensus ($0.037$), BGSS provides an additional $+0.062$ multimodality screening boost. In matched feature gating ablations, comparing BGSS directly against matched random subspace gating reveals a gain of $+0.062$ ($0.217$ vs. $0.155$, 95\% CI $[+0.013, +0.142]$, Wilcoxon $p = 0.0625$), establishing that while the random-subspace bipartite ensemble accounts for $+0.118$ of the gain over ambient consensus ($0.037$), BGSS provides an additional $+0.062$ multimodality screening boost."
        )
        single_chunk = (
            r"In matched feature gating ablations, comparing BGSS directly against matched random subspace gating reveals an empirical gain of $+0.062$ ($0.217$ vs. $0.155$, 95\% CI: $[+0.013, +0.142]$, Wilcoxon $p = 0.0625$), establishing that while the random-subspace bipartite ensemble accounts for $+0.118$ of the gain over ambient consensus ($0.037$), BGSS provides a targeted $+0.062$ multimodality screening enhancement."
        )
        if duplicate_chunk in text:
            text = text.replace(duplicate_chunk, single_chunk)
            print(f"  [OK] Removed duplicated sentence in Conclusion of {p}")

        path.write_text(text, encoding="utf-8")
        print(f"Successfully polished {p} to academic/research style.")

if __name__ == "__main__":
    polish_manuscript()
