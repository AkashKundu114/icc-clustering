# -*- coding: utf-8 -*-
from pathlib import Path
import re

def main():
    root = Path(__file__).resolve().parent.parent
    targets = [
        root / "springer_manuscript" / "main.tex",
        root / "paper" / "main.tex",
        root / "submission" / "source" / "main.tex",
        root / "submission" / "springer_nature_package" / "main.tex",
        root / "submission" / "overleaf_package" / "main.tex",
        root / "submission" / "arxiv_package" / "main.tex",
        root / "submission" / "arxiv_source" / "main.tex",
    ]

    for p in targets:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")

        # 1. Line 542 CoHiRF comparison: 0.155 -> 0.047
        old_cohirf = "whereas random subspace gating within GAC pipeline's bipartite pipeline retains a subgroup mean of $0.155$."
        new_cohirf = "whereas random subspace gating within the bipartite pipeline yields a subgroup mean of $0.047$ ($0.053$ under uniform anchors), and BGSS raises it to $0.217$."
        if old_cohirf in text:
            text = text.replace(old_cohirf, new_cohirf)

        # 2. Factorial Subsection clean up
        # Remove redundant sentence before table12 if present
        text = text.replace(
            "\\subsection{Factorial Decomposition}\\label{sec:exp2_knockout}\nTable~\\ref{tab:factorial} summarizes a $2 \\times 2$ factorial breakdown of subgroup mean ARI across the six high-dimensional cohorts.\n\n\\input{gen/table12_factorial_decomposition.tex}",
            "\\subsection{Factorial Decomposition}\\label{sec:exp2_knockout}\n\n\\input{gen/table12_factorial_decomposition.tex}"
        )

        # 3. Anchor null result duplicate sentence and CI [-0.039 -> -0.040]
        text = text.replace("[-0.039, +0.082]", "[-0.040, +0.082]")
        text = text.replace("[-0.039,+0.082]", "[-0.040, +0.082]")
        dup_sentence = "Because the 95% bootstrap confidence interval [$-0.040, +0.082$] comfortably encompasses zero, determinacy screening offers no proven performance edge over picking landmarks uniformly at random. This confirms that determinacy screening offers no proven performance edge over picking landmarks uniformly at random."
        single_sentence = "Because the 95% bootstrap confidence interval [$-0.040, +0.082$] comfortably encompasses zero, determinacy screening offers no proven performance edge over picking landmarks uniformly at random."
        if dup_sentence in text:
            text = text.replace(dup_sentence, single_sentence)

        # 4. If arxiv_source has old Sec 7.3/8.1, copy from springer_manuscript
        if p.name == "main.tex" and "arxiv_source" in str(p):
            src_text = (root / "springer_manuscript" / "main.tex").read_text(encoding="utf-8")
            text = src_text

        p.write_text(text, encoding="utf-8")
        print(f"Patched {p}")

if __name__ == "__main__":
    main()
