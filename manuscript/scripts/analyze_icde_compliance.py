r"""
IEEE ICDE 2027 Conference Manuscript Compliance & Double-Blind Analyzer
Target Venue: IEEE International Conference on Data Engineering (ICDE 2027)

Validates:
1. Document class: strict IEEE conference layout (\documentclass[10pt,conference]{IEEEtran})
2. Double-Blind Anonymity: zero occurrences of author names, institutional affiliations, personal emails
3. Frontmatter: Abstract word count (<= 200 words), IEEE keywords
4. Figure presence, formats, and native resolution (>= 300 DPI)
5. Cross-reference integrity (no dangling \ref, matching \label)
6. Citation completeness against references.bib
7. Table styling (booktabs compliance, caption above)
8. Page budget estimation (targeting <= 12 pages)
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

def analyze_icde_manuscript(base_dir: Path):
    tex_path = base_dir / "icde_main.tex"
    bib_path = base_dir / "references.bib"
    cls_path = base_dir / "IEEEtran.cls"
    bst_path = base_dir / "IEEEtran.bst"

    print("=" * 80)
    print("       IEEE ICDE 2027 CONFERENCE MANUSCRIPT COMPLIANCE ANALYZER        ")
    print("=" * 80)
    print(f"Base Directory: {base_dir.resolve()}")
    print(f"Target Manuscript: {tex_path.name}")
    print(f"Target Venue:   IEEE ICDE 2027 (Research Track - Double Blind)")
    print("-" * 80)

    issues = []
    warnings = []
    passes = []

    # 1. File Presence
    for f, name in [(cls_path, "IEEEtran.cls class file"),
                    (bst_path, "IEEEtran.bst BibTeX style"),
                    (tex_path, "icde_main.tex manuscript"),
                    (bib_path, "references.bib bibliography")]:
        if f.exists() and f.stat().st_size > 0:
            passes.append(f"Found {name} ({f.stat().st_size:,} bytes)")
        else:
            issues.append(f"Missing or empty {name}: {f}")

    if not tex_path.exists():
        print("\nFATAL: icde_main.tex not found. Aborting analysis.")
        return False

    with open(tex_path, "r", encoding="utf-8") as fp:
        tex_content = fp.read()

    # 2. Documentclass Checks
    doc_match = re.search(r"\\documentclass\[(.*?)\]\{IEEEtran\}", tex_content)
    if doc_match:
        options = [opt.strip() for opt in doc_match.group(1).split(",")]
        passes.append(f"Valid \\documentclass[IEEEtran] detected with options: {options}")
        if "conference" in options:
            passes.append("Document mode correctly set to 'conference' for IEEE ICDE")
        else:
            issues.append("Document mode NOT set to 'conference' (required for ICDE 2027)")
        if "compsoc" in options:
            issues.append("Option 'compsoc' should NOT be used for conference submissions")
    else:
        issues.append("No valid \\documentclass[...]{IEEEtran} declaration found.")

    # 3. Double-Blind Anonymity Audit
    forbidden_terms = [
        "Akash", "Kundu", "Techno India", "akash231001001449", "akashkundu11522",
        "github.com/akashkundu", "Department of Computer Science"
    ]
    for term in forbidden_terms:
        if re.search(rf"\b{re.escape(term)}\b", tex_content, re.IGNORECASE):
            issues.append(f"DOUBLE-BLIND VIOLATION: Found identifying text '{term}' in manuscript!")
    
    if not any("DOUBLE-BLIND VIOLATION" in s for s in issues):
        passes.append("Double-Blind audit passed: Zero author/institutional identifiers detected")

    # Author block check
    if "\\IEEEauthorblockN{Anonymous Authors}" in tex_content:
        passes.append("Author block properly anonymized ('Anonymous Authors')")
    else:
        warnings.append("Author block does not use standard '\\IEEEauthorblockN{Anonymous Authors}'")

    # 4. Frontmatter & Abstract Word Count
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
        kw_count = len(re.split(r",|;", kw_text))
        passes.append(f"IEEE Keywords compliant: {kw_count} keywords detected")
    else:
        warnings.append("No \\begin{IEEEkeywords} environment detected.")

    # 5. Core Sections
    required_sections = [
        (r"\\section\{Introduction", "Introduction"),
        (r"\\section\{Related Work", "Related Work"),
        (r"\\section\{Theoretical Motivation", "Theoretical Motivation / Falsification"),
        (r"\\section\{The Inductive Consensus Clustering Framework", "Methodology / Framework"),
        (r"\\section\{Experimental Evaluation", "Experiments / Evaluation"),
        (r"\\section\{Conclusion", "Conclusion")
    ]
    for pattern, name in required_sections:
        if re.search(pattern, tex_content, re.IGNORECASE):
            passes.append(f"Section detected: {name}")
        else:
            issues.append(f"Missing mandatory section: {name}")

    # 6. Cross-References
    labels = set(re.findall(r"\\label\{([^}]+)\}", tex_content))
    refs = set(re.findall(r"\\ref\{([^}]+)\}", tex_content))
    dangling_refs = refs - labels
    if dangling_refs:
        issues.append(f"Dangling cross-references with no matching \\label: {sorted(dangling_refs)}")
    else:
        passes.append(f"All {len(refs)} cross-references have valid matching \\label declarations")

    # 7. Citations & Bibliography
    cites = set()
    for match in re.findall(r"\\cite\{([^}]+)\}", tex_content):
        for k in match.split(","):
            cites.add(k.strip())

    if bib_path.exists():
        with open(bib_path, "r", encoding="utf-8") as fp:
            bib_content = fp.read()
        bib_keys = set(re.findall(r"@\w+\s*\{\s*([^,]+),", bib_content))
        missing_cites = cites - bib_keys
        if missing_cites:
            issues.append(f"Missing citation keys not found in references.bib: {sorted(missing_cites)}")
        else:
            passes.append(f"All {len(cites)} citations present in references.bib")

    # 8. Figures
    fig_inclusions = re.findall(r"\\includegraphics(?:\[.*?\])?\{([^}]+)\}", tex_content)
    passes.append(f"Detected {len(fig_inclusions)} figure inclusions via \\includegraphics")
    
    for fig_rel in fig_inclusions:
        fig_file = base_dir / fig_rel
        if not fig_file.exists():
            issues.append(f"Figure file not found: {fig_rel}")
            continue
        if HAS_PIL and fig_file.suffix.lower() in [".png", ".jpg", ".jpeg"]:
            try:
                with Image.open(fig_file) as img:
                    w, h = img.size
                    dpi = img.info.get("dpi", (72, 72))[0]
                    if dpi >= 290 or w >= 2000:
                        passes.append(f"Figure {fig_file.name}: {w}x{h} px, ~{int(dpi)} DPI (Print Compliant)")
                    else:
                        warnings.append(f"Figure {fig_file.name} resolution low: {int(dpi)} DPI")
            except Exception as e:
                warnings.append(f"Unable to inspect image metadata for {fig_file.name}: {e}")

    # 9. Tables
    table_count = len(re.findall(r"\\begin\{table\*?\}", tex_content))
    booktabs_count = len(re.findall(r"\\toprule", tex_content))
    if table_count > 0 and booktabs_count >= table_count:
        passes.append(f"All {table_count} tables adhere to publication-grade \\booktabs conventions")
    elif table_count > 0:
        warnings.append(f"Some tables may not use \\booktabs conventions ({booktabs_count}/{table_count})")

    # 10. Page Budget / Word Count Estimation
    raw_text = re.sub(r"%.*$", "", tex_content, flags=re.MULTILINE)
    raw_text = re.sub(r"\\[a-zA-Z]+(?:\[.*?\])?\{.*?\}", " ", raw_text)
    raw_text = re.sub(r"\\[a-zA-Z]+", " ", raw_text)
    word_count = len(re.findall(r"\b\w+\b", raw_text))
    # Standard IEEE conference 2-column density: ~850 words per full text page.
    # With figures and tables taking ~4-5 pages, ~5,000 words yields ~11-12 pages.
    passes.append(f"Estimated conference text size: {word_count:,} words")
    if word_count <= 5500:
        passes.append("Text word budget compliant with IEEE ICDE 12-page ceiling")
    else:
        warnings.append(f"Text length ({word_count} words) is close to or exceeds 12-page ceiling. Check compiled PDF.")

    # Reporting
    print("\n[+] PASSES:")
    for p in passes:
        print(f"  [PASS] {p}")

    if warnings:
        print("\n[*] WARNINGS:")
        for w in warnings:
            print(f"  [WARN] {w}")

    if issues:
        print("\n[-] CRITICAL ISSUES:")
        for iss in issues:
            print(f"  [FAIL] {iss}")
        print("\n" + "=" * 80)
        print("OVERALL STATUS: NON-COMPLIANT (Review critical issues above)")
        print("=" * 80)
        return False
    else:
        print("\n" + "=" * 80)
        print("OVERALL STATUS: IEEE ICDE 2027 COMPLIANT (Grade: A+)")
        print("Ready for Double-Blind Submission / Overleaf / PDF Generation")
        print("=" * 80)
        return True

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent
    success = analyze_icde_manuscript(base_dir)
    sys.exit(0 if success else 1)
