r"""
IEEE Manuscript Compliance & Quality Analyzer
Target Venue: IEEE Transactions on Knowledge and Data Engineering (TKDE) / IEEE TNNLS / IEEE TPAMI

Validates:
1. Document class and Computer Society layout compliance
2. Mandatory frontmatter (Abstract word count <= 200 words, IEEE Keywords)
3. Figure presence, formats, and native image resolution (>= 300 DPI)
4. Cross-reference integrity (dangling \ref, missing \label)
5. Citation completeness against BibTeX database (missing \cite, syntax)
6. Table styling (booktabs compliance, caption positioning)
7. Page budget and density estimation
"""

import sys
import re
import os
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def analyze_manuscript(base_dir: Path):
    tex_path = base_dir / "main.tex"
    bib_path = base_dir / "references.bib"
    cls_path = base_dir / "IEEEtran.cls"
    bst_path = base_dir / "IEEEtran.bst"

    print("=" * 80)
    print("           IEEE TRANSACTIONS MANUSCRIPT COMPLIANCE ANALYZER           ")
    print("=" * 80)
    print(f"Base Directory: {base_dir.resolve()}")
    print(f"Target Venue:   IEEE Transactions on Knowledge and Data Engineering (TKDE)")
    print("-" * 80)

    issues = []
    warnings = []
    passes = []

    # 1. File Presence Checks
    for f, name in [(cls_path, "IEEEtran.cls class file"),
                    (bst_path, "IEEEtran.bst BibTeX style"),
                    (tex_path, "main.tex manuscript"),
                    (bib_path, "references.bib bibliography")]:
        if f.exists() and f.stat().st_size > 0:
            passes.append(f"Found {name} ({f.stat().st_size:,} bytes)")
        else:
            issues.append(f"Missing or empty {name}: {f}")

    if not tex_path.exists():
        print("\nFATAL: main.tex not found. Aborting analysis.")
        return False

    with open(tex_path, "r", encoding="utf-8") as fp:
        tex_content = fp.read()

    # 2. Documentclass Checks
    doc_match = re.search(r"\\documentclass\[(.*?)\]\{IEEEtran\}", tex_content)
    if doc_match:
        options = [opt.strip() for opt in doc_match.group(1).split(",")]
        passes.append(f"Valid \\documentclass[IEEEtran] detected with options: {options}")
        if "journal" in options:
            passes.append("Document mode correctly set to 'journal'")
        else:
            warnings.append("Document mode not explicitly set to 'journal'")
        if "compsoc" in options:
            passes.append("Computer Society format ('compsoc') enabled for IEEE TKDE")
        else:
            warnings.append("IEEE TKDE recommends 'compsoc' option in \\documentclass")
    else:
        issues.append("No valid \\documentclass[...]{IEEEtran} declaration found.")

    # 2b. IEEEtran Package Compatibility (subfig vs caption/subcaption)
    if re.search(r"\\usepackage(?:\[.*?\])?\{subcaption\}", tex_content):
        issues.append("Package 'subcaption' overrides IEEEtran native caption engine. Use 'subfig' with [caption=false] instead.")
    elif re.search(r"\\usepackage(?:\[.*?\])?\{caption\}", tex_content) and "caption=false" not in tex_content:
        issues.append("Package 'caption' overrides IEEEtran native caption engine. Use 'subfig' with [caption=false] instead.")
    elif "subfig" in tex_content and "caption=false" in tex_content:
        passes.append("IEEEtran caption compliance verified: subfig used with caption=false (prevents caption.sty collision)")

    # 3. Frontmatter & Abstract Word Count
    abstract_match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex_content, re.DOTALL)
    if abstract_match:
        abstract_text = abstract_match.group(1).strip()
        words = len(re.findall(r"\b\w+\b", abstract_text))
        if words <= 200:
            passes.append(f"Abstract length compliant: {words} words (IEEE limit <= 200 words)")
        elif words <= 250:
            warnings.append(f"Abstract slightly long: {words} words (IEEE recommended <= 200 words)")
        else:
            issues.append(f"Abstract exceeds IEEE limits: {words} words (maximum 200-250 words)")
    else:
        issues.append("Missing \\begin{abstract} ... \\end{abstract} environment.")

    keywords_match = re.search(r"\\begin\{IEEEkeywords\}(.*?)\\end\{IEEEkeywords\}", tex_content, re.DOTALL)
    if keywords_match:
        kw_text = keywords_match.group(1).strip()
        kw_list = [k.strip() for k in re.split(r",|;", kw_text) if k.strip()]
        if 4 <= len(kw_list) <= 10:
            passes.append(f"IEEE Keywords compliant: {len(kw_list)} keywords detected")
        else:
            warnings.append(f"IEEE Keywords count ({len(kw_list)}) should ideally be between 4 and 8")
    else:
        issues.append("Missing \\begin{IEEEkeywords} ... \\end{IEEEkeywords} environment.")

    # 4. Mandatory Section Headers
    expected_sections = [
        ("Introduction", r"\\section\{Introduction\}"),
        ("Related Work", r"\\section\{Related Work\}"),
        ("Theoretical / Motivation", r"\\section\{.*?(Motivation|Falsification).*?\}"),
        ("Methodology / Framework", r"\\section\{.*?(Framework|Algorithm|Method).*?\}"),
        ("Experiments / Evaluation", r"\\section\{.*?(Experiment|Evaluation).*?\}"),
        ("Conclusion", r"\\section\{Conclusion\}")
    ]
    for sec_name, pattern in expected_sections:
        if re.search(pattern, tex_content, re.IGNORECASE):
            passes.append(f"Section detected: {sec_name}")
        else:
            warnings.append(f"Recommended section header not found: {sec_name}")

    # 5. Cross-Reference Integrity
    labels = set(re.findall(r"\\label\{([^}]+)\}", tex_content))
    refs = set(re.findall(r"\\(?:ref|eqref|autoref)\{([^}]+)\}", tex_content))

    missing_labels = refs - labels
    if missing_labels:
        issues.append(f"Dangling references with missing \\label: {sorted(list(missing_labels))}")
    else:
        passes.append(f"All {len(refs)} cross-references have valid matching \\label declarations")

    unused_labels = labels - refs
    if unused_labels:
        warnings.append(f"Declared \\label items never referenced: {sorted(list(unused_labels))}")

    # 6. BibTeX Citation Completeness
    citations = set()
    for cite_match in re.findall(r"\\cite\{([^}]+)\}", tex_content):
        for key in cite_match.split(","):
            citations.add(key.strip())

    bib_keys = set()
    if bib_path.exists():
        with open(bib_path, "r", encoding="utf-8") as fp:
            bib_content = fp.read()
        bib_keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib_content))

    missing_cites = citations - bib_keys
    if missing_cites:
        issues.append(f"Citations in text missing from references.bib: {sorted(list(missing_cites))}")
    else:
        passes.append(f"All {len(citations)} citations present in references.bib")

    # 7. Figure Asset and Resolution Verification
    fig_matches = re.findall(r"\\includegraphics(?:\[.*?\])?\{([^}]+)\}", tex_content)
    passes.append(f"Detected {len(fig_matches)} figure inclusions via \\includegraphics")
    
    for fig_rel in set(fig_matches):
        fig_file = base_dir / fig_rel
        if not fig_file.exists():
            # Check without extension or with .png
            if (base_dir / f"{fig_rel}.png").exists():
                fig_file = base_dir / f"{fig_rel}.png"
            elif (base_dir / f"{fig_rel}.pdf").exists():
                fig_file = base_dir / f"{fig_rel}.pdf"
            else:
                issues.append(f"Referenced figure file does not exist: {fig_rel}")
                continue

        if HAS_PIL and fig_file.suffix.lower() in [".png", ".jpg", ".jpeg"]:
            try:
                with Image.open(fig_file) as im:
                    w, h = im.size
                    dpi = im.info.get("dpi", (72, 72))
                    dpi_x = int(dpi[0]) if isinstance(dpi, tuple) else int(dpi)
                    # IEEE requires at least 300 DPI, or high pixel resolution for column width (3.5 in -> >= 1050 px)
                    if dpi_x >= 300 or w >= 1000:
                        passes.append(f"Figure {fig_file.name}: {w}x{h} px, {dpi_x} DPI (Meets IEEE Print Specs)")
                    else:
                        warnings.append(f"Figure {fig_file.name}: {w}x{h} px, {dpi_x} DPI (Below recommended 300 DPI)")
            except Exception as e:
                warnings.append(f"Could not inspect image metadata for {fig_file.name}: {e}")
        else:
            passes.append(f"Figure file verified on disk: {fig_file.name}")

    # 8. Table Standards
    tables = re.findall(r"\\begin\{table\*?\}(.*?)\\end\{table\*?\}", tex_content, re.DOTALL)
    for i, tbl in enumerate(tables):
        if "\\toprule" in tbl and "\\midrule" in tbl and "\\bottomrule" in tbl:
            passes.append(f"Table {i+1} adheres to publication-grade \\booktabs conventions")
        else:
            warnings.append(f"Table {i+1} does not use standard \\booktabs (\\toprule, \\midrule, \\bottomrule)")
        
        caption_pos = tbl.find("\\caption")
        tabular_pos = tbl.find("\\begin{tabular")
        if caption_pos != -1 and tabular_pos != -1 and caption_pos < tabular_pos:
            passes.append(f"Table {i+1} caption is correctly positioned ABOVE the table")
        else:
            warnings.append(f"Table {i+1} caption should be placed ABOVE the tabular environment in IEEE format")

    # 9. IEEE Biographies
    bio_matches = re.findall(r"\\begin\{IEEEbiography.*?\}", tex_content)
    if bio_matches:
        passes.append(f"IEEE Biography block verified ({len(bio_matches)} author biographies)")
    else:
        warnings.append("IEEE Transactions standard requires author biographies at the end of the manuscript")

    # 10. Page Budget / Word Count Estimation
    total_words = len(re.findall(r"\b\w+\b", tex_content))
    # IEEEtran 2-column density is approximately 900-1000 words per page (text-heavy), or ~600 words with figures
    estimated_pages = max(1, round(total_words / 650 + len(fig_matches) * 0.4 + len(tables) * 0.3))
    passes.append(f"Estimated page budget: ~{estimated_pages} pages ({total_words:,} words total, including code/figures)")

    # Print Summary Report
    print("\n[+] PASSES:")
    for p in passes:
        print(f"  [PASS] {p}")

    if warnings:
        print("\n[!] WARNINGS (Non-blocking recommendations):")
        for w in warnings:
            print(f"  [WARN] {w}")

    if issues:
        print("\n[-] CRITICAL COMPLIANCE ISSUES (Must resolve for IEEE submission):")
        for iss in issues:
            print(f"  [FAIL] {iss}")
        print("\n" + "=" * 80)
        print("OVERALL STATUS: FAILED (Resolve critical issues above)")
        print("=" * 80)
        return False
    else:
        print("\n" + "=" * 80)
        print("OVERALL STATUS: IEEE TRANSACTIONS COMPLIANT (Grade: A+)")
        print("Ready for IEEE ScholarOne Submission / Overleaf / IEEE PDF-eXpress")
        print("=" * 80)
        return True

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent
    success = analyze_manuscript(base_dir)
    sys.exit(0 if success else 1)
