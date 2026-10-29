import re

def main():
    tex_path = "paper/main.tex"
    with open(tex_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update line 89 / roadmap sentence
    old_roadmap = "Section~\\ref{sec:conclusion} concludes the paper. Source code and data availability follow."
    new_roadmap = "Section~\\ref{sec:conclusion} concludes the paper. Declarations follow."
    if old_roadmap in content:
        content = content.replace(old_roadmap, new_roadmap)
        print("Updated roadmap sentence.")
    else:
        print("Roadmap sentence not found or already updated.")

    declarations_block = r"""\section*{Declarations}

\begin{itemize}
\item \textbf{Funding:} No specific external grant funding was received for this study.
\item \textbf{Conflict of interest/Competing interests:} The authors declare that they have no competing financial or non-financial interests directly or indirectly related to the work submitted for publication.
\item \textbf{Ethics approval and consent to participate:} Not applicable. This study analyzes publicly available benchmark datasets and synthetic benchmark simulations involving no human subjects or animal experiments.
\item \textbf{Consent for publication:} All co-authors have been provided the complete pre-submission manuscript bundle. Formal submission sign-off is confirmed by the corresponding author.
\item \textbf{Data availability:} All benchmark datasets analyzed in this study are publicly accessible from their original upstream open-access repositories:
\begin{itemize}
    \item \textbf{Biomedical and Tabular Microarrays:} CNS (OpenML ID: 1128, \url{https://www.openml.org/d/1128}), Colon (OpenML ID: 1111, \url{https://www.openml.org/d/1111}), Leukemia (OpenML ID: 1104, \url{https://www.openml.org/d/1104}), Ovarian (OpenML ID: 1142, \url{https://www.openml.org/d/1142}), Prostate (OpenML ID: 1159, \url{https://www.openml.org/d/1159}), SRBCT (OpenML ID: 1158, \url{https://www.openml.org/d/1158}), Sonar (OpenML ID: 40, \url{https://www.openml.org/d/40}), Madelon (OpenML ID: 1485, \url{https://www.openml.org/d/1485}), and Isolet (UCI Machine Learning Repository: \url{https://archive.ics.uci.edu/dataset/54/isolet}; OpenML ID: 300, \url{https://www.openml.org/d/300}).
    \item \textbf{Text Benchmark:} 20 Newsgroups (original corpus: \url{http://qwone.com/~jason/20Newsgroups/}).
    \item \textbf{Hyperspectral Benchmark:} Indian Pines (UPV/EHU Hyperspectral Imagery Repository: \url{https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes}).
    \item \textbf{Facial Image Benchmark:} Extended Yale B (Academic Torrents persistent archive: \url{https://academictorrents.com/details/aad8bf8e6ee5d8a3bf46c7ab5adfacdd8ad36247}).
    \item \textbf{Single-Cell Genomics Benchmark:} PBMC68k-reduced (10x Genomics 68k PBMCs primary repository: \url{https://www.10xgenomics.com/datasets/fresh-68-k-pbm-cs-donor-a-1-standard-1-1-0}; distributed in Scanpy: \url{https://scanpy.readthedocs.io/en/stable/generated/scanpy.datasets.pbmc68k_reduced.html}).
\end{itemize}
\item \textbf{Materials availability:} Not applicable.
\item \textbf{Code availability:} The complete, fully reproducible Python implementation of ICC-v2, benchmark harnesses, validation scripts, and figure generation routines are released under the MIT License at: \url{https://github.com/AkashKundu114/icc-clustering} (release tag \texttt{v2.0.0}).
\item \textbf{Author contribution:} A. Kundu conceived the framework, derived theoretical properties, implemented algorithms, performed empirical analyses, and drafted the manuscript. T. Guha, R. Ghatak, and A. Naskar designed baseline pipelines, contributed to computational scaling experiments, and validated code integrity. K. K. Das supervised the research, reviewed statistical methodologies, and edited the manuscript.
\item \textbf{Use of Artificial Intelligence Disclosure:} During the preparation of this manuscript and software repository, the authors utilized an agentic AI coding assistant solely for assistive technical tasks, specifically code quality audits, static analysis, unit test suite verification, bibliographic cross-checking against CrossRef APIs, figure plotting, LaTeX table and manuscript formatting, and typographical proofreading. No artificial intelligence tools were used for scientific ideation, research conceptualization, empirical design, theoretical derivations, or the formulation of substantive claims. All conceptual formulations, empirical designs, and mathematical derivations were conceived and directed exclusively by the human authors. The authors conducted independent cross-checks of all generated code, tables, figures, and formatting, and assume full responsibility for the scientific integrity, accuracy, and reproducibility of all reported findings.
\end{itemize}

"""

    # Replace \section*{Source Code and Data Availability}... with declarations_block
    pattern = r"\\section\*\{Source Code and Data Availability\}.*?(?=\\bibliography\{references\})"
    if re.search(pattern, content, flags=re.DOTALL):
        content = re.sub(pattern, lambda m: declarations_block, content, flags=re.DOTALL)
        print("Replaced Source Code and Data Availability with Declarations section.")
    else:
        print("Source Code and Data Availability pattern not matched!")
        return

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully wrote updated paper/main.tex")

if __name__ == "__main__":
    main()
