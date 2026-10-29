"""
Apply Item 10 updates to paper/main.tex.
"""

def main():
    with open("paper/main.tex", "r", encoding="utf-8") as f:
        text = f.read()

    # 10a: Madelon subsample in Table 3 (formerly Table 6)
    s_old_madelon = r" & Madelon & $500$ & $500$ & $2$ & $1.00$ & Non-Linear XOR Parity \\"
    s_new_madelon = r" & Madelon\textsuperscript{*} & $500$ & $500$ & $2$ & $1.00$ & Non-Linear XOR Parity \\"
    assert s_old_madelon in text, "Madelon row not found"
    text = text.replace(s_old_madelon, s_new_madelon)

    s_old_table_bottom = r"""\bottomrule
\end{tabular}%
}
\end{table*}"""
    s_new_table_bottom = r"""\bottomrule
\multicolumn{7}{@{}l}{\footnotesize \textsuperscript{*}Madelon is evaluated on a deterministic subsample of 500 of the 2,600 samples from OpenML 1485 ($D/N = 1.00$).} \\
\end{tabular}%
}
\end{table*}"""
    assert s_old_table_bottom in text, "Table bottom not found"
    text = text.replace(s_old_table_bottom, s_new_table_bottom, 1)

    # 10b: Sec 5.1 CPU model, clock speed, and package versions
    s_old_env = r"""\subsection{Computational Environment}\label{sec:setup_env}
We executed benchmark fits using Python 3.14 on an AMD Ryzen 9 8940HX host paired with an NVIDIA RTX 5060 GPU."""
    s_new_env = r"""\subsection{Computational Environment}\label{sec:setup_env}
All experimental benchmarks, scaling evaluations, and ablations were executed on a dedicated host equipped with an AMD Ryzen 9 8940HX processor (16 physical cores, 32 logical threads, 2.40~GHz base clock, up to 5.20~GHz boost), 16~GB DDR5 RAM, and an NVIDIA GeForce RTX 5060 Laptop GPU running 64-bit Windows 11. Experiments were conducted using Python 3.14.6 with core numerical libraries: NumPy 2.4.6, SciPy 1.18.0, scikit-learn 1.9.1, and PyTorch 2.16.0."""
    assert s_old_env in text, "Environment section not found"
    text = text.replace(s_old_env, s_new_env)

    # 10c: Tie-handling convention and unrounded per-seed means for Friedman test
    s_old_friedman = r"""\textbf{Non-Parametric Omnibus Hypothesis Testing:}
Evaluating the 11 clustering algorithms across all 13 benchmarks (2,750 independent model fits: 30 seeds on $D/N > 20$ cohorts, 10 on others) via the non-parametric Friedman test yields:
\begin{equation}
    \chi_F^2 = 9.59, \quad p = 0.48.
\end{equation}"""
    s_new_friedman = r"""\textbf{Non-Parametric Omnibus Hypothesis Testing:}
Evaluating the 11 clustering algorithms across all 13 benchmarks (2,750 independent model fits: 30 seeds on $D/N > 20$ cohorts, 10 on others) via the non-parametric Friedman test (using average ranks for ties, computed directly on unrounded per-seed mean ARIs to eliminate 3-decimal rounding distortion) yields:
\begin{equation}
    \chi_F^2 = 9.59, \quad p = 0.48.
\end{equation}"""
    assert s_old_friedman in text, "Friedman section not found"
    text = text.replace(s_old_friedman, s_new_friedman)

    # In Table 9, make sure Friedman test lists average ranks for ties
    s_old_tab9 = r"""Post-Hoc Critical Difference & Nemenyi test ($CD = 4.19$) & Omnibus rank comparison~\cite{demsar2006statistical} \\"""
    s_new_tab9 = r"""Omnibus Rank Test & Friedman test (average ranks for ties) & Global equivalence test~\cite{friedman1937use} \\
Post-Hoc Critical Difference & Nemenyi test ($CD = 4.19$) & Omnibus rank comparison~\cite{demsar2006statistical} \\"""
    assert s_old_tab9 in text, "Table 9 row not found"
    text = text.replace(s_old_tab9, s_new_tab9)

    with open("paper/main.tex", "w", encoding="utf-8") as f:
        f.write(text)

    print("[*] Successfully applied Item 10 updates to paper/main.tex")


if __name__ == "__main__":
    main()
