"""
Apply ORCID updates across:
- paper/main.tex & springer_manuscript/main.tex
- CITATION.cff
- submission/COVER_LETTER.md
- submission/USER_CHECKLIST.md
"""

from pathlib import Path

def update_all():
    # Remove temporary test files
    for p in ["paper/main_test.tex", "paper/main_test.pdf"]:
        Path(p).unlink(missing_ok=True)

    # 1. Update paper/main.tex and springer_manuscript/main.tex
    preamble_add = r"\gdef\orcidlogo{\textcolor[HTML]{A6CE39}{\fontsize{7}{8}\selectfont\textbf{iD}}}"
    
    author_block_new = (
        r"\author*[1]{\fnm{Kalyan Kumar} \sur{Das}\orcid{https://orcid.org/0009-0004-8333-8900}}\email{kalyan.biltu@gmail.com}" + "\n\n" +
        r"\author[1]{\fnm{Akash} \sur{Kundu}\orcid{https://orcid.org/0009-0003-8246-7316}}\email{akashkundu1152@gmail.com}" + "\n\n" +
        r"\author[2]{\fnm{Anirban} \sur{Mukhopadhyay}\orcid{https://orcid.org/0000-0001-8128-3521}}\email{anirban@klyuniv.ac.in}"
    )

    old_contrib = (
        r"\textbf{Authors' contributions}: K.~K.~Das conceived and supervised the research, formulated the research problem, reviewed statistical methodology, and edited the manuscript. "
        r"A.~Kundu formulated the theoretical framework and proofs, implemented the core algorithms and test suites, conducted the benchmark experiments, and wrote the manuscript. "
        r"A.~Mukhopadhyay contributed to theoretical analysis, methodological refinement, and critical review of the manuscript. "
        r"All authors reviewed and approved the final manuscript. General correspondence should be addressed to K.~K.~Das (\href{mailto:kalyan.biltu@gmail.com}{\texttt{kalyan.biltu@gmail.com}}). "
        r"Requests for code, data artifacts, and experimental reproduction materials should be addressed to A.~Kundu (\href{mailto:akashkundu1152@gmail.com}{\texttt{akashkundu1152@gmail.com}})."
    )

    new_contrib = (
        r"\textbf{Authors' contributions}: K.~K.~Das (ORCID: \href{https://orcid.org/0009-0004-8333-8900}{0009-0004-8333-8900}) conceived and supervised the research, formulated the research problem, reviewed statistical methodology, and edited the manuscript. "
        r"A.~Kundu (ORCID: \href{https://orcid.org/0009-0003-8246-7316}{0009-0003-8246-7316}) formulated the theoretical framework and proofs, implemented the core algorithms and test suites, conducted the benchmark experiments, and wrote the manuscript. "
        r"A.~Mukhopadhyay (ORCID: \href{https://orcid.org/0000-0001-8128-3521}{0000-0001-8128-3521}) contributed to theoretical analysis, methodological refinement, and critical review of the manuscript. "
        r"All authors reviewed and approved the final manuscript. General correspondence should be addressed to K.~K.~Das (\href{mailto:kalyan.biltu@gmail.com}{\texttt{kalyan.biltu@gmail.com}}). "
        r"Requests for code, data artifacts, and experimental reproduction materials should be addressed to A.~Kundu (\href{mailto:akashkundu1152@gmail.com}{\texttt{akashkundu1152@gmail.com}})."
    )

    for p in ["paper/main.tex", "springer_manuscript/main.tex"]:
        path = Path(p)
        text = path.read_text(encoding="utf-8")
        
        # Preamble addition
        if preamble_add not in text:
            assert r"\begin{document}" in text
            text = text.replace(r"\begin{document}", preamble_add + "\n\n" + r"\begin{document}")

        # Replace author block
        auth_start = text.find(r"\author")
        affil_start = text.find(r"\affil")
        old_authors = text[auth_start:affil_start]
        text = text[:auth_start] + author_block_new + "\n\n" + text[affil_start:]

        # Replace contributions block
        if old_contrib in text:
            text = text.replace(old_contrib, new_contrib)

        path.write_text(text, encoding="utf-8")
        print(f"Updated {p}")

    p1 = Path("paper/main.tex").read_bytes()
    p2 = Path("springer_manuscript/main.tex").read_bytes()
    print("Manuscripts identical:", p1 == p2)

    # 2. Update CITATION.cff
    cff_content = """cff-version: 1.2.0
message: "If you use this software or benchmark suite in your research, please cite as follows."
title: "Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes"
version: 2.2.0
date-released: "2026-10-30"
authors:
  - family-names: "Das"
    given-names: "Kalyan Kumar"
    orcid: "https://orcid.org/0009-0004-8333-8900"
    email: "kalyan.biltu@gmail.com"
    affiliation: "Department of Computer Science and Engineering, Techno India University"
  - family-names: "Kundu"
    given-names: "Akash"
    orcid: "https://orcid.org/0009-0003-8246-7316"
    email: "akashkundu1152@gmail.com"
    affiliation: "Department of Computer Science and Engineering, Techno India University"
  - family-names: "Mukhopadhyay"
    given-names: "Anirban"
    orcid: "https://orcid.org/0000-0001-8128-3521"
    email: "anirban@klyuniv.ac.in"
    affiliation: "Department of Computer Science and Engineering, University of Kalyani"
repository-code: "https://github.com/AkashKundu114/icc-clustering"
license: "MIT"
keywords:
  - "cluster ensemble"
  - "consensus clustering"
  - "inductive learning"
  - "out-of-sample extension"
  - "high-dimensional data"
  - "bipartite anchor graph"
  - "feature gating"
  - "subsample stability"
"""
    Path("CITATION.cff").write_text(cff_content, encoding="utf-8")
    print("Updated CITATION.cff")

    # 3. Update submission/COVER_LETTER.md
    cl_path = Path("submission/COVER_LETTER.md")
    cl_text = cl_path.read_text(encoding="utf-8")
    old_signoff = """**Prof. Kalyan Kumar Das** (Corresponding Author, Research Supervisor)  
Department of Computer Science and Engineering  
Techno India University, Kolkata, India  
Email: kalyan.biltu@gmail.com  

*On behalf of co-authors:*  
**Akash Kundu** (Lead Developer & Author for Code/Reproduction Materials Requests: akashkundu1152@gmail.com, Techno India University) and **Prof. Anirban Mukhopadhyay** (Senior Collaborator: anirban@klyuniv.ac.in, University of Kalyani)."""

    new_signoff = """**Prof. Kalyan Kumar Das** (Corresponding Author, Research Supervisor)  
Department of Computer Science and Engineering  
Techno India University, Kolkata, India  
Email: kalyan.biltu@gmail.com  
ORCID: https://orcid.org/0009-0004-8333-8900  

*On behalf of co-authors:*  
- **Akash Kundu** (Lead Developer & Author for Code/Reproduction Materials Requests: akashkundu1152@gmail.com, Techno India University; ORCID: https://orcid.org/0009-0003-8246-7316)  
- **Prof. Anirban Mukhopadhyay** (Senior Collaborator: anirban@klyuniv.ac.in, University of Kalyani; ORCID: https://orcid.org/0000-0001-8128-3521)"""

    if old_signoff in cl_text:
        cl_text = cl_text.replace(old_signoff, new_signoff)
        cl_path.write_text(cl_text, encoding="utf-8")
        print("Updated submission/COVER_LETTER.md")

    # 4. Update submission/USER_CHECKLIST.md
    chk_path = Path("submission/USER_CHECKLIST.md")
    chk_lines = chk_path.read_text(encoding="utf-8").splitlines()
    new_chk_lines = []
    for l in chk_lines:
        new_chk_lines.append(l)
        if "Confirm code/data/materials request contact details" in l:
            new_chk_lines.append("- [x] Author ORCID iDs verified:")
            new_chk_lines.append("  - Prof. Kalyan Kumar Das: `0009-0004-8333-8900`")
            new_chk_lines.append("  - Akash Kundu: `0009-0003-8246-7316`")
            new_chk_lines.append("  - Prof. Anirban Mukhopadhyay: `0000-0001-8128-3521`")
    chk_path.write_text("\n".join(new_chk_lines) + "\n", encoding="utf-8")
    print("Updated submission/USER_CHECKLIST.md")

if __name__ == "__main__":
    update_all()
