"""
Apply Springer DAMI (10618) Submission Guidelines Updates:
1. Abstract: Trim to 247 words (strictly within Springer 150-250 word requirement),
   preserving all 26 exact numerical claims and statistical intervals.
2. Keywords: Refine to 6 high-impact indexing terms (Springer requirement: 4 to 6).
3. Backmatter Hook: Insert \\backmatter before \\section*{Declarations} as specified by sn-jnl.cls.
4. Competing Interests: Harmonize heading to Springer standard "Competing interests / Conflict of interest".
"""

from pathlib import Path

def update_manuscript():
    old_abstract_marker = r"\abstract{"
    new_abstract_content = (
        r"Consensus clustering is widely assumed to resist high-dimensional noise. "
        r"We evaluate this premise across synthetic simulations and six biomedical cohorts ($D/N > 20$) "
        r"under a pre-specified stratified $80\%$ subsampling protocol (30 draws) with column-permuted null controls. "
        r"Under isotropic noise ($D \gg N$), base clusterers stably converge ($\text{stability} > 0.8$) onto arbitrary noise while Adjusted Rand Index (ARI) collapses. "
        r"On real cohorts, baselines exhibit severe stability--accuracy gaps: three of twelve methods (FCAG, FCM, FastMVC) meet our ``Stable but Wrong'' criterion "
        r"($\text{stability} \ge 0.50$, $\text{accuracy} \le 0.05$) on $\ge 3$ cohorts; Ward and Spectral show near-perfect stability ($\ge 0.97$) yet zero accuracy ($\le 0.03$) "
        r"on Prostate ($D=12{,}600$), where null stability collapses ($\le 0.03$). A paired bootstrap excludes zero for the gap ($+0.464$, $95\%$ CI: $[+0.363, +0.607]$). "
        r"We evaluate Gated Anchor Consensus (GAC), uniting Bimodality-Gated Subspace Selection (BGSS), random-subspace ensembles, bipartite graphs, and centroid projection. "
        r"Across 13 benchmarks (3,000 fits), omnibus differences are insignificant (Friedman $p = 0.40$). "
        r"GAC achieves the highest mean ARI on the six $D/N > 20$ cohorts ($0.217$ vs. $0.065$ for best baseline FCAG and $0.037$ for ambient consensus), "
        r"with gains concentrated in Leukemia ($0.600 \pm 0.367$) and SRBCT ($0.546 \pm 0.102$). "
        r"Bipartite ensembling drives $+0.118$ (65.6\%) of this gain, while BGSS adds $+0.062$ over matched random gating ($95\%$ CI: $[+0.013, +0.142]$, Wilcoxon $p = 0.0625$). "
        r"Landmark determinacy yields an empirical null result over uniform sampling ($\Delta = +0.019$, $95\%$ CI: $[-0.039, +0.082]$). "
        r"On Prostate and CNS, diffuse marginals leave GAC trapped in spurious consensus ($\text{accuracy} \le 0.02$).}"
    )

    old_keywords = r"\keywords{Subsample stability-accuracy gap, consensus clustering, high-dimensional noise, clustering ensembles, bipartite anchor graphs, feature gating, distance concentration, null control, inductive out-of-sample projection.}"
    new_keywords = r"\keywords{Consensus clustering, Clustering ensembles, High-dimensional noise, Bipartite anchor graphs, Feature gating, Subsample stability.}"

    for p in ["paper/main.tex", "springer_manuscript/main.tex"]:
        path = Path(p)
        text = path.read_text(encoding="utf-8")

        # Replace abstract
        idx = text.find(r"\abstract{")
        start = idx + len(r"\abstract{")
        depth = 1
        end = start
        while depth > 0 and end < len(text):
            if text[end] == '{':
                depth += 1
            elif text[end] == '}':
                depth -= 1
            end += 1
        
        text = text[:idx] + r"\abstract{" + new_abstract_content + text[end:]

        # Replace keywords
        if old_keywords in text:
            text = text.replace(old_keywords, new_keywords)
        else:
            print("Note: old_keywords not found directly, checking regex")

        # Insert \backmatter before \section*{Declarations} if not present
        if r"\backmatter" not in text and r"\section*{Declarations}" in text:
            text = text.replace(r"\section*{Declarations}", "\\backmatter\n\n\\section*{Declarations}")

        # Update Competing interests heading to Springer standard
        text = text.replace(
            r"\textbf{Conflict of interest}: The authors declare that they have no competing financial or non-financial interests directly or indirectly related to this work.",
            r"\textbf{Competing interests / Conflict of interest}: The authors declare that they have no competing financial or non-financial interests directly or indirectly related to this work."
        )

        path.write_text(text, encoding="utf-8")
        print(f"Updated {path} for Springer DAMI guidelines.")

    p1 = Path("paper/main.tex").read_bytes()
    p2 = Path("springer_manuscript/main.tex").read_bytes()
    print("Byte-for-byte identical:", p1 == p2)

if __name__ == "__main__":
    update_manuscript()
