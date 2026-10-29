import shutil

def add_table16():
    with open("paper/main.tex", "r", encoding="utf-8") as f:
        text = f.read()

    target = r"\section{Real-World Applications}\label{sec:applications}"
    replacement = r"""\section{Real-World Applications}\label{sec:applications}

To evaluate the translational utility and practical boundaries of the ICC-v2 framework, we examined three representative application domains: translational oncology microarray subtyping, large-scale single-cell transcriptomics, and high-throughput point-of-care inductive query projection. Table~\ref{tab:case_studies_synthesis} summarizes the evaluation cohorts, data regimes, primary metrics, operational advantages, and empirical failure boundaries across all three case studies.

\input{gen/table16_case_studies.tex}"""

    if target in text:
        text = text.replace(target, replacement, 1)
        print("Inserted Table 16 into Section 8.")
    else:
        print("Target not found!")
        return

    with open("paper/main.tex", "w", encoding="utf-8") as f:
        f.write(text)

    # Sync to springer_manuscript
    shutil.copy2("paper/main.tex", "springer_manuscript/main.tex")
    print("Synced paper/main.tex to springer_manuscript/main.tex")

if __name__ == "__main__":
    add_table16()
