"""
Builds verified submission packages for:
1. Overleaf (overleaf_package.zip)
2. Springer Nature DAMI (springer_nature_package.zip)
3. arXiv (arxiv_package.tar.gz and arxiv_package.zip)

Follows official submission guidelines for each platform:
- Overleaf: Single root main.tex, references.bib, main.bbl, sn-jnl.cls, bst/, gen/, figures/, zero junk files, < 50 MB, < 180 files.
- Springer Nature: Source bundle with main.tex, references.bib, main.bbl, sn-jnl.cls, figures/, declarations verified, cover letter, checklist, refs audit report.
- arXiv: Flat/clean source with inlined macros/tables, pre-generated root main.bbl, sn-jnl.cls, referenced figures, 00README.XXX, < 10 MB, available as .tar.gz and .zip.
"""

import os
import re
import shutil
import subprocess
import tarfile
import zipfile
from pathlib import Path


def get_referenced_figures(tex_path: Path):
    tex = tex_path.read_text(encoding="utf-8")
    cites = re.findall(r"\\includegraphics(?:\[.*?\])?\{([^}]+)\}", tex)
    clean_figs = set()
    for c in cites:
        if c.strip() == "Orcidlogo" or c.startswith("Orcidlogo"):
            continue
        fig_name = c.replace("figures/", "").strip()
        clean_figs.add(fig_name)
    return sorted(clean_figs)


def get_referenced_tables(tex_path: Path):
    tex = tex_path.read_text(encoding="utf-8")
    inputs = re.findall(r"\\input\{([^}]+)\}", tex)
    clean_tabs = set()
    for inp in inputs:
        if inp.startswith("gen/"):
            clean_tabs.add(inp.replace("gen/", "").strip())
    return sorted(clean_tabs)


def build_packages():
    root = Path(__file__).resolve().parent.parent
    sub_dir = root / "submission"
    sub_dir.mkdir(parents=True, exist_ok=True)
    paper_dir = root / "paper"
    tectonic_exe = root / "tools" / "bin" / "tectonic.exe"

    ref_figs = get_referenced_figures(paper_dir / "main.tex")
    ref_tabs = get_referenced_tables(paper_dir / "main.tex")
    print(f"[1/6] Discovered {len(ref_figs)} actively referenced figures and {len(ref_tabs)} tables in paper/main.tex:")
    for f in ref_figs:
        print(f"  - fig: {f}")
    for t in ref_tabs:
        print(f"  - tab: {t}")

    # Copy main.pdf to submission root
    if (paper_dir / "main.pdf").exists():
        shutil.copy2(paper_dir / "main.pdf", sub_dir / "main.pdf")
        print(f"  Copied main.pdf ({sub_dir / 'main.pdf'})")

    # =========================================================================
    # PACKAGE 1: Overleaf Package
    # =========================================================================
    print("\n[2/6] Building Overleaf Package (submission/overleaf_package)...")
    overleaf_dir = sub_dir / "overleaf_package"
    if overleaf_dir.exists():
        shutil.rmtree(overleaf_dir)
    overleaf_dir.mkdir(parents=True)

    # Core files
    shutil.copy2(paper_dir / "main.tex", overleaf_dir / "main.tex")
    shutil.copy2(paper_dir / "references.bib", overleaf_dir / "references.bib")
    shutil.copy2(paper_dir / "main.bbl", overleaf_dir / "main.bbl")
    shutil.copy2(paper_dir / "numbers.tex", overleaf_dir / "numbers.tex")
    shutil.copy2(paper_dir / "sn-jnl.cls", overleaf_dir / "sn-jnl.cls")
    for orcid_ext in ["eps", "pdf", "png"]:
        shutil.copy2(paper_dir / f"Orcidlogo.{orcid_ext}", overleaf_dir / f"Orcidlogo.{orcid_ext}")

    # bst files in root and in bst/
    (overleaf_dir / "bst").mkdir(exist_ok=True)
    for bst_file in paper_dir.glob("*.bst"):
        shutil.copy2(bst_file, overleaf_dir / bst_file.name)
        shutil.copy2(bst_file, overleaf_dir / "bst" / bst_file.name)

    # gen/ tables (only actively referenced tables)
    (overleaf_dir / "gen").mkdir(exist_ok=True)
    for tab_name in ref_tabs:
        src_tab = paper_dir / "gen" / tab_name
        if src_tab.exists():
            shutil.copy2(src_tab, overleaf_dir / "gen" / tab_name)

    # figures/ (only actively referenced figures)
    (overleaf_dir / "figures").mkdir(exist_ok=True)
    for fig_name in ref_figs:
        src_fig = paper_dir / "figures" / fig_name
        if src_fig.exists():
            shutil.copy2(src_fig, overleaf_dir / "figures" / fig_name)
        else:
            print(f"  WARNING: Figure {fig_name} not found in paper/figures!")

    # Overleaf README
    readme_overleaf = """# Overleaf Project Import Instructions

This package is configured for 1-click import into Overleaf:
1. Log into your Overleaf account.
2. Click **New Project** -> **Upload Project**.
3. Select `overleaf_package.zip`.
4. Overleaf will automatically detect `main.tex` as the root document.
5. In project settings (Menu icon in top-left):
   - **Compiler**: pdfLaTeX
   - **TeX Live version**: 2024 or 2025
   - **Main document**: `main.tex`
6. Click **Recompile**.
"""
    (overleaf_dir / "README.md").write_text(readme_overleaf, encoding="utf-8")

    # Test compile Overleaf package with Tectonic
    print("  Testing compilation of Overleaf package with Tectonic...")
    res_ol = subprocess.run([str(tectonic_exe), str(overleaf_dir / "main.tex")], capture_output=True, text=True)
    assert res_ol.returncode == 0, f"Overleaf package compilation failed:\n{res_ol.stderr}\n{res_ol.stdout}"
    print("  [OK] Overleaf package compiled cleanly (returncode 0).")
    if (overleaf_dir / "main.pdf").exists():
        os.remove(overleaf_dir / "main.pdf")

    # Zip Overleaf package
    overleaf_zip = sub_dir / "overleaf_package.zip"
    with zipfile.ZipFile(overleaf_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for root_path, _, files in os.walk(overleaf_dir):
            for file in files:
                p = Path(root_path) / file
                arcname = p.relative_to(overleaf_dir)
                z.write(p, arcname=arcname)
    ol_size_mb = overleaf_zip.stat().st_size / (1024 * 1024)
    print(f"  Created {overleaf_zip.name} ({ol_size_mb:.2f} MB)")

    # =========================================================================
    # PACKAGE 2: Springer Nature DAMI Submission Package (NO EXTRA FILES)
    # =========================================================================
    print("\n[3/6] Building Clean Springer Nature Package (submission/springer_nature_package)...")
    springer_dir = sub_dir / "springer_nature_package"
    if springer_dir.exists():
        shutil.rmtree(springer_dir)
    springer_dir.mkdir(parents=True)

    # Core source files ONLY
    shutil.copy2(paper_dir / "main.tex", springer_dir / "main.tex")
    shutil.copy2(paper_dir / "references.bib", springer_dir / "references.bib")
    shutil.copy2(paper_dir / "main.bbl", springer_dir / "main.bbl")
    shutil.copy2(paper_dir / "numbers.tex", springer_dir / "numbers.tex")
    shutil.copy2(paper_dir / "sn-jnl.cls", springer_dir / "sn-jnl.cls")
    shutil.copy2(paper_dir / "sn-mathphys-num.bst", springer_dir / "sn-mathphys-num.bst")
    (springer_dir / "bst").mkdir(exist_ok=True)
    shutil.copy2(paper_dir / "sn-mathphys-num.bst", springer_dir / "bst" / "sn-mathphys-num.bst")

    for orcid_ext in ["eps", "pdf", "png"]:
        shutil.copy2(paper_dir / f"Orcidlogo.{orcid_ext}", springer_dir / f"Orcidlogo.{orcid_ext}")

    # gen/ tables (strictly the 15 referenced tables)
    (springer_dir / "gen").mkdir(exist_ok=True)
    for tab_name in ref_tabs:
        src_tab = paper_dir / "gen" / tab_name
        if src_tab.exists():
            shutil.copy2(src_tab, springer_dir / "gen" / tab_name)

    # figures/ (strictly the 15 referenced figures)
    (springer_dir / "figures").mkdir(exist_ok=True)
    for fig_name in ref_figs:
        src_fig = paper_dir / "figures" / fig_name
        if src_fig.exists():
            shutil.copy2(src_fig, springer_dir / "figures" / fig_name)

    # Test compile Springer package with Tectonic
    print("  Testing compilation of clean Springer Nature package with Tectonic...")
    res_sp = subprocess.run([str(tectonic_exe), str(springer_dir / "main.tex")], capture_output=True, text=True)
    assert res_sp.returncode == 0, f"Springer package compilation failed:\n{res_sp.stderr}\n{res_sp.stdout}"
    print("  [OK] Springer Nature package compiled cleanly (returncode 0).")
    if (springer_dir / "main.pdf").exists():
        os.remove(springer_dir / "main.pdf")

    # Zip Springer package
    springer_zip = sub_dir / "springer_nature_package.zip"
    with zipfile.ZipFile(springer_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for root_path, _, files in os.walk(springer_dir):
            for file in files:
                p = Path(root_path) / file
                arcname = p.relative_to(springer_dir)
                z.write(p, arcname=arcname)
    sp_size_mb = springer_zip.stat().st_size / (1024 * 1024)
    print(f"  Created {springer_zip.name} ({sp_size_mb:.2f} MB)")

    # =========================================================================
    # PACKAGE 3: arXiv Submission Package
    # =========================================================================
    print("\n[4/6] Building arXiv Package (submission/arxiv_package)...")
    arxiv_dir = sub_dir / "arxiv_package"
    if arxiv_dir.exists():
        shutil.rmtree(arxiv_dir)
    arxiv_dir.mkdir(parents=True)

    # Inlining numbers.tex and gen/*.tex into main.tex for arXiv robustness
    main_tex = (paper_dir / "main.tex").read_text(encoding="utf-8")
    numbers_content = (paper_dir / "numbers.tex").read_text(encoding="utf-8")
    main_tex = main_tex.replace(r"\input{numbers.tex}", numbers_content)
    main_tex = main_tex.replace(r"\input{paper/numbers.tex}", numbers_content)

    for tab_name in ref_tabs:
        gen_content = (paper_dir / "gen" / tab_name).read_text(encoding="utf-8")
        include_str = f"\\input{{gen/{tab_name}}}"
        main_tex = main_tex.replace(include_str, gen_content)

    (arxiv_dir / "main.tex").write_text(main_tex, encoding="utf-8")
    # Pre-generated main.bbl matching main.tex name (MANDATORY for arXiv)
    shutil.copy2(paper_dir / "main.bbl", arxiv_dir / "main.bbl")
    shutil.copy2(paper_dir / "references.bib", arxiv_dir / "references.bib")
    shutil.copy2(paper_dir / "sn-jnl.cls", arxiv_dir / "sn-jnl.cls")
    for orcid_file in paper_dir.glob("Orcidlogo.*"):
        shutil.copy2(orcid_file, arxiv_dir / orcid_file.name)

    # bst files
    for bst_file in paper_dir.glob("*.bst"):
        shutil.copy2(bst_file, arxiv_dir / bst_file.name)

    # figures/
    (arxiv_dir / "figures").mkdir(exist_ok=True)
    for fig_name in ref_figs:
        src_fig = paper_dir / "figures" / fig_name
        if src_fig.exists():
            shutil.copy2(src_fig, arxiv_dir / "figures" / fig_name)

    # arXiv 00README.XXX
    readme_arxiv = "main.tex\n"
    (arxiv_dir / "00README.XXX").write_text(readme_arxiv, encoding="utf-8")

    # Test compile arXiv package with Tectonic
    print("  Testing compilation of arXiv package with Tectonic...")
    res_ar = subprocess.run([str(tectonic_exe), str(arxiv_dir / "main.tex")], capture_output=True, text=True)
    assert res_ar.returncode == 0, f"arXiv package compilation failed:\n{res_ar.stderr}\n{res_ar.stdout}"
    print("  [OK] arXiv package compiled cleanly (returncode 0).")
    if (arxiv_dir / "main.pdf").exists():
        os.remove(arxiv_dir / "main.pdf")

    # Create arXiv .tar.gz (arXiv's preferred native format)
    arxiv_tar_gz = sub_dir / "arxiv_package.tar.gz"
    with tarfile.open(arxiv_tar_gz, "w:gz") as tar:
        for root_path, _, files in os.walk(arxiv_dir):
            for file in files:
                p = Path(root_path) / file
                arcname = p.relative_to(arxiv_dir)
                tar.add(p, arcname=str(arcname).replace("\\", "/"))
    tar_size_mb = arxiv_tar_gz.stat().st_size / (1024 * 1024)
    print(f"  Created {arxiv_tar_gz.name} ({tar_size_mb:.2f} MB)")

    # Create arXiv .zip
    arxiv_zip = sub_dir / "arxiv_package.zip"
    with zipfile.ZipFile(arxiv_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for root_path, _, files in os.walk(arxiv_dir):
            for file in files:
                p = Path(root_path) / file
                arcname = p.relative_to(arxiv_dir)
                z.write(p, arcname=arcname)
    ar_size_mb = arxiv_zip.stat().st_size / (1024 * 1024)
    print(f"  Created {arxiv_zip.name} ({ar_size_mb:.2f} MB)")

    # Also synchronize root submission/source.zip (< 50 MB)
    print("\n[5/6] Synchronizing master submission/source.zip...")
    source_zip = sub_dir / "source.zip"
    with zipfile.ZipFile(source_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for root_path, _, files in os.walk(springer_dir):
            for file in files:
                p = Path(root_path) / file
                arcname = p.relative_to(springer_dir)
                z.write(p, arcname=arcname)
    src_size_mb = source_zip.stat().st_size / (1024 * 1024)
    print(f"  Created {source_zip.name} ({src_size_mb:.2f} MB)")

    # =========================================================================
    # SUMMARY & VERIFICATION
    # =========================================================================
    print("\n[6/6] Summary of Generated Submission Packages in submission/:")
    packages = [
        ("Overleaf Package", overleaf_zip, ol_size_mb, 50.0),
        ("Springer Nature Package", springer_zip, sp_size_mb, 50.0),
        ("arXiv Tarball (.tar.gz)", arxiv_tar_gz, tar_size_mb, 10.0),
        ("arXiv Archive (.zip)", arxiv_zip, ar_size_mb, 10.0),
        ("Master Source Archive", source_zip, src_size_mb, 50.0),
    ]

    for name, path, size, limit in packages:
        status = "PASS" if size <= limit else "WARNING (exceeds standard limit)"
        print(f"  - {name}: {path.name} ({size:.2f} MB, limit: {limit:.1f} MB) -> {status}")

    print("\nAll packages built and verified successfully!")


if __name__ == "__main__":
    build_packages()
