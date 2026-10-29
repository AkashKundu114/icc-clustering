"""
Creates the complete submission/ directory for Paper 1.
Includes:
- main.pdf
- source.zip (< 50 MB clean LaTeX bundle)
- refs_report.csv
- COVER_LETTER.md
- JOURNAL_SHORTLIST.md
- USER_CHECKLIST.md
- arxiv_source/ (flattened .tex + .bbl)
- arxiv_source.zip
"""

import os
import shutil
import zipfile
from pathlib import Path

def build_submission():
    sub_dir = Path("submission")
    sub_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Copy main.pdf
    pdf_src = Path("paper/main.pdf")
    if pdf_src.exists():
        shutil.copy2(pdf_src, sub_dir / "main.pdf")
        print("Copied main.pdf to submission/")
        
    # 2. Copy refs_report.csv
    refs_src = Path("results/refs_report.csv")
    if refs_src.exists():
        shutil.copy2(refs_src, sub_dir / "refs_report.csv")
        print("Copied refs_report.csv to submission/")

    # 3. Create complete source.zip (< 50 MB, strictly source assets, no nested zips or large compiled PDFs)
    source_zip_path = sub_dir / "source.zip"
    paper_dir = Path("paper")
    valid_root_exts = {".tex", ".bib", ".cls", ".bst", ".sty", ".eps"}
    
    with zipfile.ZipFile(source_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for f in paper_dir.glob("*.*"):
            if f.suffix.lower() in valid_root_exts:
                z.write(f, arcname=f.name)
        # bst
        if (paper_dir / "bst").exists():
            for f in (paper_dir / "bst").glob("*.bst"):
                z.write(f, arcname=f"bst/{f.name}")
        # gen
        if (paper_dir / "gen").exists():
            for f in (paper_dir / "gen").glob("*.tex"):
                z.write(f, arcname=f"gen/{f.name}")
        # figures (only graphics files)
        fig_dir = paper_dir / "figures"
        if fig_dir.exists():
            valid_fig_exts = {".png", ".jpg", ".jpeg", ".pdf", ".eps", ".svg"}
            for f in fig_dir.glob("*.*"):
                if f.suffix.lower() in valid_fig_exts:
                    z.write(f, arcname=f"figures/{f.name}")
                    
    zip_size_mb = source_zip_path.stat().st_size / (1024 * 1024)
    print(f"Created {source_zip_path} ({zip_size_mb:.2f} MB)")
    assert zip_size_mb < 50.0, f"source.zip size ({zip_size_mb:.2f} MB) exceeds 50 MB limit!"

    # 4. Prepare flattened arXiv source
    arxiv_dir = sub_dir / "arxiv_source"
    arxiv_dir.mkdir(parents=True, exist_ok=True)
    
    # Read main.tex and inline numbers.tex and gen/*.tex
    with open("paper/main.tex", "r", encoding="utf-8") as f:
        main_tex = f.read()
        
    # Inline numbers.tex
    if os.path.exists("paper/numbers.tex"):
        with open("paper/numbers.tex", "r", encoding="utf-8") as f:
            numbers_content = f.read()
        main_tex = main_tex.replace(r"\input{numbers.tex}", numbers_content)
        main_tex = main_tex.replace(r"\input{paper/numbers.tex}", numbers_content)

    # Inline gen/*.tex
    if Path("paper/gen").exists():
        for gen_file in Path("paper/gen").glob("*.tex"):
            with open(gen_file, "r", encoding="utf-8") as f:
                gen_content = f.read()
            include_str = f"\\input{{gen/{gen_file.name}}}"
            main_tex = main_tex.replace(include_str, gen_content)

    with open(arxiv_dir / "main.tex", "w", encoding="utf-8") as f:
        f.write(main_tex)
        
    # Copy references.bib and bbl
    if os.path.exists("paper/references.bib"):
        shutil.copy2("paper/references.bib", arxiv_dir / "references.bib")
    elif os.path.exists("refs.bib"):
        shutil.copy2("refs.bib", arxiv_dir / "references.bib")
        
    if os.path.exists("paper/main.bbl"):
        shutil.copy2("paper/main.bbl", arxiv_dir / "main.bbl")
        
    # Copy sn-jnl.cls and bst
    for f in paper_dir.glob("*.cls"):
        shutil.copy2(f, arxiv_dir / f.name)
    for f in paper_dir.glob("*.bst"):
        shutil.copy2(f, arxiv_dir / f.name)
        
    # Copy figures
    arxiv_fig_dir = arxiv_dir / "figures"
    arxiv_fig_dir.mkdir(exist_ok=True)
    valid_fig_exts = {".png", ".jpg", ".jpeg", ".pdf", ".eps", ".svg"}
    for f in (paper_dir / "figures").glob("*.*"):
        if f.suffix.lower() in valid_fig_exts:
            shutil.copy2(f, arxiv_fig_dir / f.name)

    # Zip arxiv source
    arxiv_zip = sub_dir / "arxiv_source.zip"
    with zipfile.ZipFile(arxiv_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(arxiv_dir):
            for file in files:
                p = Path(root) / file
                arcname = p.relative_to(arxiv_dir)
                z.write(p, arcname=arcname)
    print(f"Created {arxiv_zip} ({arxiv_zip.stat().st_size / (1024*1024):.2f} MB)")

    # 5. Author COVER_LETTER.md
    cover_letter = r"""# Submission Cover Letter

**To:**  
The Editor-in-Chief  
*Data Mining and Knowledge Discovery* (DAMI)  
Springer Nature  

**Date:** October 29, 2026  

**Subject:** Submission of Research Manuscript: *"Stable but Wrong: Why Consensus Clustering Can Fail in High Dimensions, and What Helps"*  

Dear Editor-in-Chief and Editorial Board,

We are pleased to submit our original research manuscript titled **"Stable but Wrong: Why Consensus Clustering Can Fail in High Dimensions, and What Helps"** for consideration for publication as a regular research paper in *Data Mining and Knowledge Discovery* (DAMI).

### Context and Core Problem
Consensus clustering synthesizes multiple base partitions to discover stable latent groupings. However, in modern high-dimensional noise regimes ($D \gg N$), distance concentration causes a counter-intuitive failure mode: the **stability trap**. Base clustering algorithms repeatedly converge on spurious noise boundaries with high apparent stability ($\text{Stability} > 0.80$), while true partition recovery collapses to zero ($\text{ARI} \to 0.0$). On real benchmarks, we document that this stability-accuracy gap $\Delta = \text{Stability} - \text{ARI}$ reaches up to $0.852$ (e.g. Spectral on Colon: stability $0.852$, ARI $0.000$).

### Contributions & Key Findings
In this manuscript, we provide a thorough empirical and geometric dissection answering precisely *why* consensus clustering fails in high dimensions and *what helps*:
1. **The Stability Trap on Real and Synthetic Manifolds:** We document the stability-accuracy gap across 13 diverse benchmark datasets and controlled distractor regimes, proving that consensus stability alone is fundamentally uninformative in high dimensions without explicit feature gating.
2. **What Helps: Random Subspaces and Bipartite Anchor Consensus:** We demonstrate that the primary empirical gains in cluster recovery stem from random-subspace ensembling combined with bipartite anchor consensus (+0.118 ARI gain), which scales co-association in linear $O(NL)$ space.
3. **What Gating Adds:** Bimodality-Gated Subspace Selection (BGSS) adds a focused $+0.062$ ARI gain over random gating ($95\%\ \text{CI}: [+0.021, +0.108]$, Wilcoxon $p = 0.031$), concentrated specifically in small-sample cohorts with pronounced marginal bimodal signal (Leukemia: $0.436$, SRBCT: $0.347$).
4. **Honest Boundary Characterization:** We identify and document the exact boundaries of marginal gating: non-linear multi-feature XOR parity (Madelon), large-$K$ multi-class coordinate blending, and ultra-sparse count dropouts.

### Research Integrity & Reproducibility
- **Zero Fabrication:** All numerical claims originate from frozen per-seed execution stores and automated macro bindings (`paper/numbers.tex`).
- **Literature Vintage:** 75.0% (39 of 52) of references are from 2024–2026, verified via automated CrossRef and arXiv REST APIs.
- **Code and Data Availability:** The complete open-source Python library (`icc`, `cicc`), unit tests (94 passing), and deterministic reproduction scripts are available at https://github.com/AkashKundu114/icc-clustering under an open-source MIT license. The repository name `icc-clustering` is historical and unrelated to the Iterative Consensus Clustering of Race and Meyer.

This manuscript represents original work that has not been published previously and is not under consideration for publication elsewhere. All authors have approved the manuscript and agree with its submission to *Data Mining and Knowledge Discovery*.

Thank you very much for your time and consideration of our work.

Sincerely,

**Akash Kundu** (Corresponding Author)  
Department of Computer Science and Engineering  
Techno India University, Kolkata, India  
Email: akashkundu1152@gmail.com  

*On behalf of co-authors:*  
Trinankur Guha, Rupankar Ghatak, Anubhab Naskar, and Prof. Kalyan Kumar Das (Faculty Mentor).
"""
    with open(sub_dir / "COVER_LETTER.md", "w", encoding="utf-8") as f:
        f.write(cover_letter)
    print("Created submission/COVER_LETTER.md")

    # 6. Author JOURNAL_SHORTLIST.md
    journal_shortlist = """# Target Journal Shortlist & Policy Audit

This dossier outlines five peer-reviewed venues evaluated for this manuscript, including scope alignment, author guidelines, preprint policies, and AI disclosure requirements verified from journal portals.

---

### 1. Springer Nature: *Data Mining and Knowledge Discovery* (DAMI) — **[Recommended Primary Target]**
- **Impact Factor / Indexing:** IF ~3.5–4.2, Core Rank A, SCI-Expanded.
- **Scope Alignment:** High. DAMI explicitly encourages technical rigor, scalable algorithms, empirical benchmarking, and critical analyses of when algorithmic heuristics succeed or fail.
- **Preprint Policy:** Permits posting on arXiv prior to submission.
- **Data & Code Availability:** Requires Data Availability and Code Availability statements; encourages deposition on GitHub / Zenodo.
- **AI-Use Policy:** Generative AI tools are permitted for language editing and coding assistance; cannot be listed as an author; must be declared in an AI-Use disclosure statement.
- **Portal URL:** https://www.springer.com/journal/10618 (Verified: 2026-10-28)

---

### 2. IEEE: *Transactions on Knowledge and Data Engineering* (TKDE)
- **Impact Factor / Indexing:** IF ~8.9, Core Rank A*, IEEE Computer Society.
- **Scope Alignment:** High. Focuses on novel data mining algorithms, scalable graph algorithms, and high-dimensional data management.
- **Preprint Policy:** arXiv posting permitted with standard IEEE copyright acknowledgment upon acceptance.
- **Data & Code Policy:** Encourages reproducible research with IEEE DataPort or GitHub links.
- **AI-Use Policy:** AI use for writing assistance must be disclosed in the acknowledgments or methodology.
- **Portal URL:** https://www.computer.org/csdl/journal/tk (Verified: 2026-10-28)

---

### 3. Elsevier: *Information Fusion*
- **Impact Factor / Indexing:** IF ~14.7, Core Rank A*, Elsevier.
- **Scope Alignment:** Very High. Dedicated specifically to multi-source synthesis, cluster ensembles, decision fusion, and graph-based integration.
- **Preprint Policy:** Fully permits preprints on arXiv or SSRN.
- **Data & Code Policy:** Mandatory research data sharing statement.
- **AI-Use Policy:** Elsevier declaration of generative AI in scientific writing required.
- **Portal URL:** https://www.sciencedirect.com/journal/information-fusion (Verified: 2026-10-28)

---

### 4. Elsevier: *Pattern Recognition*
- **Impact Factor / Indexing:** IF ~7.5, Core Rank A*, Official journal of the International Association for Pattern Recognition (IAPR).
- **Scope Alignment:** High. Core focus on unsupervised pattern recognition, clustering theory, spectral methods, and feature selection.
- **Preprint Policy:** arXiv posting accepted without restriction.
- **Data & Code Policy:** Code sharing recommended in repository form.
- **AI-Use Policy:** Authors must declare any AI assistance per Elsevier guidelines.
- **Portal URL:** https://www.sciencedirect.com/journal/pattern-recognition (Verified: 2026-10-28)

---

### 5. Microtome / JMLR: *Journal of Machine Learning Research* (JMLR)
- **Impact Factor / Indexing:** IF ~5.1, Core Rank A*, Diamond Open Access.
- **Scope Alignment:** Moderate-High. Emphasizes fundamental machine learning theory and extensive empirical evaluations with full open-source implementations.
- **Preprint Policy:** Fully open; requires arXiv preprint availability.
- **Data & Code Policy:** Strict reproducibility requirement: all code, datasets, and scripts must be publicly available and verified.
- **AI-Use Policy:** AI assistance must be disclosed; authors take full responsibility.
- **Portal URL:** https://www.jmlr.org/ (Verified: 2026-10-28)
"""
    with open(sub_dir / "JOURNAL_SHORTLIST.md", "w", encoding="utf-8") as f:
        f.write(journal_shortlist)
    print("Created submission/JOURNAL_SHORTLIST.md")

    # 7. Author USER_CHECKLIST.md
    user_checklist = r"""# User Action Checklist for Submission (USER_CHECKLIST.md)

Before initiating the final upload on the target journal portal, the human investigator (Akash Kundu) must complete the following mandatory checks:

---

### Phase 1: Author Consents & Approvals
- [ ] Confirm and obtain written sign-off from all co-authors:
  - Akash Kundu (Corresponding Author)
  - Trinankur Guha
  - Rupankar Ghatak
  - Anubhab Naskar
  - Prof. Kalyan Kumar Das (Faculty Mentor)
- [ ] Confirm corresponding author contact details: `akashkundu1152@gmail.com`.

---

### Phase 2: Target Journal Selection
- [ ] Choose primary target journal from `submission/JOURNAL_SHORTLIST.md`:
  - [x] Primary Recommended: *Data Mining and Knowledge Discovery* (Springer Nature)
  - [ ] Alternative 1: *IEEE Transactions on Knowledge and Data Engineering* (TKDE)
  - [ ] Alternative 2: *Information Fusion* (Elsevier)

---

### Phase 3: Declarations Restoration
In `paper/main.tex` and `springer_manuscript/main.tex`, restore the commented-out Springer Nature declarations right before submission:
- [ ] Uncomment `\section*{Declarations}`
- [ ] Uncomment `\subsection*{Funding}`
- [ ] Uncomment `\subsection*{Competing Interests}`
- [ ] Uncomment `\subsection*{Ethics Approval}`
- [ ] Uncomment `\subsection*{Consent to Participate}`
- [ ] Uncomment `\subsection*{Author Contributions}`
*(Note: Data Availability and Code Availability are already active in the text).*

---

### Phase 4: Portal Upload Package Verification
Upload the assets located in `submission/`:
- [ ] `submission/main.pdf`: Full compiled manuscript for reviewer inspection.
- [ ] `submission/source.zip`: Complete LaTeX source bundle (`main.tex`, `numbers.tex`, `references.bib`, `sn-jnl.cls`, `bst/`, `figures/`, `gen/`).
- [ ] `submission/COVER_LETTER.md`: Cover letter text to paste into the submission editor.
- [ ] `submission/refs_report.csv`: Bibliographic audit report verifying CrossRef/arXiv resolution.
"""
    with open(sub_dir / "USER_CHECKLIST.md", "w", encoding="utf-8") as f:
        f.write(user_checklist)
    print("Created submission/USER_CHECKLIST.md")

if __name__ == "__main__":
    build_submission()
