# -*- coding: utf-8 -*-
r"""
Applies final submission polish items:
1. Footnote on Prostate page 11 listing the 7 non-degenerate algorithms meeting Rule (i').
2. Retitle Table 13 to 'Statistical Testing Parameters and Configurations' and clarify pre-specified family in Section 6.3.
3. Replace 'Supplementary Table' references with plain 'Table' for Tables 4 and 20.
4. Fig. 2b caption: change 'remains near zero across noise scales' to 'stays below 0.2 across noise scales'.
5. Add \clearpage before Section 6.4 to keep heading and numbered list together.
"""

from pathlib import Path

def apply_fixes(file_path: Path):
    text = file_path.read_text(encoding="utf-8")

    # 1. Footnote on Prostate
    target1 = r"On Prostate ($D=12{,}600$), seven non-degenerate algorithms meet Rule~(i'), headed by Ward"
    repl1 = r"On Prostate ($D=12{,}600$), seven non-degenerate algorithms meet Rule~(i')\footnote{The seven algorithms meeting Rule~(i') on Prostate are DEC, FCAG, FastMVC, GAC, K-Means, Spectral Clustering, and Ward.}, headed by Ward"
    assert target1 in text, "Target 1 not found"
    text = text.replace(target1, repl1)

    # 2. Table 13 Title & Section 6.3
    target2a = r"Table~\ref{tab:statistical_params} reports the pre-specified parameters governing all statistical hypothesis tests, family-wise error adjustments, and bootstrap resamplings."
    repl2a = r"Table~\ref{tab:statistical_params} reports the statistical testing parameters governing hypothesis tests, family-wise error adjustments, and bootstrap resamplings."
    assert target2a in text, "Target 2a not found"
    text = text.replace(target2a, repl2a)

    target2b = r"\caption{Pre-Specified Statistical Testing Parameters and Configurations}"
    repl2b = r"\caption{Statistical Testing Parameters and Configurations}"
    assert target2b in text, "Target 2b not found"
    text = text.replace(target2b, repl2b)

    target2c = r"Holm-Bonferroni step-down correction is applied to the family of 11 pairwise benchmark comparisons between GAC and baseline algorithms in the high-dimensional subgroup evaluation above;"
    repl2c = r"Holm-Bonferroni step-down correction is applied to the pre-specified family of 11 pairwise benchmark comparisons between GAC and baseline algorithms in the high-dimensional subgroup evaluation above;"
    assert target2c in text, "Target 2c not found"
    text = text.replace(target2c, repl2c)

    # 3. Supplementary references -> plain Table references
    target3a = r"supported by the detailed subsample degeneracy audit in Supplementary Table~\ref{tab:degeneracy_audit}."
    repl3a = r"supported by the detailed subsample degeneracy audit in Table~\ref{tab:degeneracy_audit}."
    assert target3a in text, "Target 3a not found"
    text = text.replace(target3a, repl3a)

    target3b = r"As documented in Supplementary Table~\ref{tab:degeneracy_audit}, CoHiRF also encounters high subsample degeneracy"
    repl3b = r"As documented in Table~\ref{tab:degeneracy_audit}, CoHiRF also encounters high subsample degeneracy"
    assert target3b in text, "Target 3b not found"
    text = text.replace(target3b, repl3b)

    target3c = r"formally compiled in Supplementary Table~\ref{tab:supp_foundations}."
    repl3c = r"formally compiled in Table~\ref{tab:supp_foundations}."
    assert target3c in text, "Target 3c not found"
    text = text.replace(target3c, repl3c)

    # 4. Fig. 2b caption
    target4 = r"(b) The subsample stability--accuracy gap ($\Delta = \text{Stability} - \text{ARI}$) remains near zero across noise scales."
    repl4 = r"(b) The subsample stability--accuracy gap ($\Delta = \text{Stability} - \text{ARI}$) stays below 0.2 across noise scales."
    assert target4 in text, "Target 4 not found"
    text = text.replace(target4, repl4)

    # 5. Section 6.4 numbering layout
    target5 = "surpasses $0.50$.\n\n\\subsection{Operational Parameter Analysis}\\label{sec:param_scaling}"
    repl5 = "surpasses $0.50$.\n\n\\clearpage\n\\subsection{Operational Parameter Analysis}\\label{sec:param_scaling}"
    assert target5 in text, "Target 5 not found"
    text = text.replace(target5, repl5)

    file_path.write_text(text, encoding="utf-8")
    print(f"Successfully updated {file_path}")

if __name__ == "__main__":
    apply_fixes(Path("springer_manuscript/main.tex"))
    apply_fixes(Path("paper/main.tex"))
