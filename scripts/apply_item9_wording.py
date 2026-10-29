"""
Apply Item 9 wording updates to paper/main.tex.
"""

def main():
    with open("paper/main.tex", "r", encoding="utf-8") as f:
        text = f.read()

    # 9a: Sec 6.3 Student's t-test
    s_old_a = "formally proving that parametric Student's $t$-tests are methodologically invalid"
    s_new_a = "indicating that normality assumptions are violated, which motivates the non-parametric tests"
    assert s_old_a in text, "9a text not found"
    text = text.replace(s_old_a, s_new_a)

    # 9b: Abstract ensemble averaging
    s_old_b = "confirming ensemble averaging alone cannot remove noise"
    s_new_b = "indicating that ensemble averaging alone does not remove the noise in these simulations"
    assert s_old_b in text, "9b text not found"
    text = text.replace(s_old_b, s_new_b)

    # 9c: Sec 7.3 hypothesis label
    s_old_c = "by suppressing noisy off-diagonal co-associations through landmark projection"
    s_new_c = "we hypothesize that it operates by suppressing noisy off-diagonal co-associations through landmark projection"
    assert s_old_c in text, "9c text not found"
    text = text.replace(s_old_c, s_new_c)

    # 9d: After Eq. (2) rho_sep
    s_old_d = r"Consequently, the separation metric $\rho_{\text{sep}}(X)$ approaches unity (Fig.~\ref{fig:conceptual_overview}(b)), obliterating the geometric boundaries separating latent classes."
    s_new_d = r"Consequently, the separation metric $\rho_{\text{sep}}(X)$ falls toward or below 1 (Fig.~\ref{fig:conceptual_overview}(b)), indicating geometric overlap and obliterating distinguishable boundaries between latent classes."
    assert s_old_d in text, "9d text not found"
    text = text.replace(s_old_d, s_new_d)

    # 9e: Sec 6.4 Convergence Analysis items 1 & 2
    s_old_e1 = r"\item \textbf{Ensemble Size Convergence ($M$):} Evaluating partition accuracy as a function of base clusterer count demonstrates that consensus accuracy stabilizes as ensemble size reaches $M = 20\text{--}25$. Increasing ensemble size to $M = 50$ or $100$ produces negligible accuracy gains while linearly increasing base clustering runtime ($O(M)$); we adopt $M = 25$ as a practical balance between partition stability and runtime."
    s_new_e1 = r"\item \textbf{Ensemble Size Setting ($M$):} In our main experiments, the base ensemble size is set to $M = 25$ as a practical default matching prior consensus literature~\cite{fred2005combining}. We did not systematically test sensitivity across a broader grid of $M \in \{5, 10, 15, 20, 35, 50, 100\}$ on all real-world cohorts, so whether an earlier plateau exists or larger ensembles yield marginal stability gains remains an open empirical question."
    assert s_old_e1 in text, "9e1 text not found"
    text = text.replace(s_old_e1, s_new_e1)

    s_old_e2 = r"\item \textbf{Anchor Budget Considerations ($L$):} Bipartite anchor consensus constructs an affinity representation against $L$ landmark points. While larger $L$ provides denser anchor coverage, the generalized eigensolve on the anchor affinity matrix incurs cubic spectral complexity ($O(L^3)$). In our benchmarks, setting $L = 40$ provides sufficient landmark representation across diverse sample sizes ($N \in [500, 10{,}000]$) while maintaining negligible eigensolve overhead, keeping overall execution near-linear in $N$ across this range (Fig.~\ref{fig:exp4_quad})."
    s_new_e2 = r"\item \textbf{Anchor Budget Considerations ($L$):} Bipartite anchor consensus constructs an affinity representation against $L$ landmark points. While larger $L$ provides denser anchor coverage, the generalized eigensolve on the anchor affinity matrix incurs cubic spectral complexity ($O(L^3)$). In our benchmarks, we fixed $L = 40$ following scalable ensemble defaults; we did not systematically test alternative anchor budgets $L \in \{10, 20, 60, 80\}$ across all cohorts, leaving the trade-off between anchor density and spectral solve cost as an untested parameter regime."
    assert s_old_e2 in text, "9e2 text not found"
    text = text.replace(s_old_e2, s_new_e2)

    with open("paper/main.tex", "w", encoding="utf-8") as f:
        f.write(text)

    print("[*] Successfully applied all Item 9 edits to paper/main.tex")


if __name__ == "__main__":
    main()
