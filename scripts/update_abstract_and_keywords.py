# -*- coding: utf-8 -*-
from pathlib import Path

def main():
    new_abstract = r"""\abstract{Consensus clustering is widely assumed to resist high-dimensional noise. We evaluate this premise across simulations and six biomedical cohorts ($D/N > 20$) under stratified $80\%$ subsampling (30 draws, 435 pairs) with column-permuted null controls. Under isotropic noise ($D \gg N$), base clusterers converge stably onto arbitrary noise partitions while Adjusted Rand Index (ARI) collapses. On real cohorts, baselines exhibit pronounced stability-accuracy discordance: three of twelve methods (FCAG, FCM, FastMVC) satisfy our non-degenerate discordance criterion on $\ge 3$ cohorts (mean stability $0.638$; mean accuracy $0.046$). A paired bootstrap confirms a positive gap ($+0.485$ non-degenerate, $95\%$ CI: $[+0.379, +0.662]$; unconstrained $+0.464$, $[+0.363, +0.607]$), indicating that high stability does not imply correctness. We evaluate Gated Anchor Consensus (GAC), combining Bimodality-Gated Subspace Selection (BGSS), random-subspace ensembles, bipartite anchor graphs, and projection. Across 13 benchmarks (3,000 fits), omnibus differences across methods are not statistically significant ($p = 0.40$). GAC attains the highest mean ARI on the six $D/N > 20$ cohorts ($0.217$ vs. $0.065$ for FCAG and $0.037$ for ambient consensus), concentrated in Leukemia ($0.600$) and SRBCT ($0.546$). Bipartite ensembling accounts for $+0.118$ (65.6\%) of this gain, while BGSS adds $+0.062$ over matched random gating ($95\%$ CI: $[+0.013, +0.142]$). Landmark determinacy yields an empirical null result over uniform sampling ($\Delta = +0.019$). On Prostate and CNS, diffuse marginal distributions lead to partitions unrelated to reference labels ($\text{accuracy} \le 0.02$).}

\keywords{Cluster stability, Consensus clustering, Ensemble learning, Bipartite anchor graphs, Feature gating}"""

    for rel_path in ['paper/main.tex', 'springer_manuscript/main.tex']:
        p = Path(rel_path)
        text = p.read_text(encoding='utf-8')

        old_abstract = r"""\abstract{Consensus clustering is widely assumed to resist high-dimensional noise. We evaluate this premise across simulations and six biomedical cohorts ($D/N > 20$) under stratified $80\%$ subsampling (30 draws, 435 pairs) with column-permuted null controls. Under isotropic noise ($D \gg N$), base clusterers converge stably onto arbitrary noise partitions while Adjusted Rand Index (ARI) collapses. On real cohorts, baselines exhibit pronounced stability-accuracy discordance: three of twelve methods (FCAG, FCM, FastMVC) satisfy our pre-specified non-degenerate discordance criterion on $\ge 3$ cohorts (mean stability $0.638$, range $0.304$--$0.905$; mean accuracy $0.046$); Ward and Spectral show high subsample stability ($\ge 0.97$) yet near-zero accuracy ($\le 0.03$) on Prostate ($D=12{,}600$, null stability $\le 0.03$). A paired bootstrap excludes zero for the overall gap ($+0.485$ non-degenerate, $95\%$ CI: $[+0.379, +0.662]$; unconstrained $+0.464$, $[+0.363, +0.607]$), indicating that stability does not imply correctness. We evaluate Gated Anchor Consensus (GAC), combining Bimodality-Gated Subspace Selection (BGSS), random-subspace ensembles, bipartite anchor graphs, and projection. Across 13 benchmarks (3,000 fits), omnibus differences across methods are not statistically significant ($p = 0.40$). GAC attains the highest mean ARI on the six $D/N > 20$ cohorts ($0.217$ vs. $0.065$ for FCAG and $0.037$ for ambient consensus), concentrated in Leukemia ($0.600$) and SRBCT ($0.546$). Bipartite ensembling accounts for $+0.118$ (65.6\%) of this gain, while BGSS adds $+0.062$ over matched random gating ($95\%$ CI: $[+0.013, +0.142]$). Landmark determinacy yields an empirical null result over uniform sampling ($\Delta = +0.019$). On Prostate and CNS, diffuse marginal distributions lead to partitions unrelated to reference labels ($\text{accuracy} \le 0.02$).}

\keywords{cluster stability, ensemble learning, consensus clustering, high-dimensional noisy data, bipartite anchor graphs, feature gating, subsample stability, null control.}"""

        assert old_abstract in text, f"old_abstract not found in {rel_path}"
        text = text.replace(old_abstract, new_abstract)
        p.write_text(text, encoding='utf-8')
        print(f"[+] Updated abstract and keywords in {rel_path}")

if __name__ == '__main__':
    main()
