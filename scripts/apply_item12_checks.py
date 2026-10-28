"""
Apply Item 12 updates: tightened abstract (<= 250 words) and notation consistency.
"""

def main():
    with open("paper/main.tex", "r", encoding="utf-8") as f:
        text = f.read()

    # Find and replace abstract
    old_abs_prefix = r"\abstract{Consensus clustering is often assumed to resist high-dimensional noise, and dense $N \times N$ consensus to be unavoidable."
    new_abs = r"""\abstract{Consensus clustering is often assumed to resist high-dimensional noise, and dense $N \times N$ consensus to be unavoidable. We test both assumptions. In finite-sample simulations with isotropic distractors ($D \gg N$), base clusterers (particularly spectral and Ward) converge stably ($\text{stability} > 0.8$) on arbitrary noise partitions while ARI collapses toward zero, indicating that ensemble averaging alone does not remove noise in these simulations. We evaluate ICC-v2, combining linear-time Bimodality-Gated Subspace Selection (BGSS), random-subspace ensembles, bipartite anchor consensus, and closed-form centroid out-of-sample assignment. Across 13 benchmarks (2,750 total fits: 30 seeds on six $D/N > 20$ cohorts, 10 on the remaining seven), we find no statistically significant omnibus difference between methods (Friedman $p = 0.48$); Standard Consensus attains the best mean rank (4.85) and ICC-v2 ranks fourth (5.23). ICC-v2's higher Grand Mean ARI (0.152) is concentrated on two cancer cohorts, Leukemia (0.600) and SRBCT (0.546); it is near zero on most others, and on Prostate underperforms simple baselines (0.012 vs. 0.049). On the six $D/N > 20$ cohorts, ICC-v2 ranks first (exploratory, $n = 6$, not significant after Holm correction). Ablations demonstrate that BGSS and bipartite anchor consensus interact synergistically for accuracy gains ($V_5 - V_2 = +0.140$, 95\% CI [$+0.004, +0.321$]), while anchor certification provides no statistical benefit ($\Delta = +0.019$, 95\% CI [$-0.039, +0.082$]) and bipartite compression cuts consensus-graph memory by 99.6\% at $N = 10{,}000$. Failure modes are characterized under non-linear parity, zero-inflated counts, and large $K$."""

    # Locate start of abstract
    start_pos = text.find(r"\abstract{")
    assert start_pos != -1, "Abstract not found"
    
    # Locate end of abstract (brace matching)
    depth = 0
    end_pos = start_pos
    for idx in range(start_pos + len(r"\abstract"), len(text)):
        if text[idx] == '{':
            depth += 1
        elif text[idx] == '}':
            depth -= 1
            if depth == 0:
                end_pos = idx + 1
                break

    text = text[:start_pos] + new_abs + text[end_pos:]

    with open("paper/main.tex", "w", encoding="utf-8", newline="\r\n") as f:
        f.write(text)

    print("[*] Successfully replaced abstract with tightened version (<= 250 words)")


if __name__ == "__main__":
    main()
