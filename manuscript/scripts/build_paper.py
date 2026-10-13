#!/usr/bin/env python3
"""
Automated IEEE Paper Compilation and Packaging Pipeline.
- Compiles LaTeX via pdflatex/latexmk if installed.
- Otherwise, packages a 100% self-contained Overleaf / IEEE ScholarOne submission zip.
"""

import subprocess
import shutil
import zipfile
import sys
from pathlib import Path

def build():
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent
    dist_dir = base_dir / "dist"
    dist_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("           IEEE TRANSACTIONS BUILD & EXPORT PIPELINE           ")
    print("=" * 70)

    # 1. Check for tectonic, pdflatex, or latexmk
    tectonic_bin = base_dir / "scripts" / "bin" / "tectonic.exe"
    has_tectonic = tectonic_bin.exists() or (shutil.which("tectonic") is not None)
    has_latexmk = shutil.which("latexmk") is not None
    has_pdflatex = shutil.which("pdflatex") is not None

    if has_tectonic:
        tectonic_cmd = str(tectonic_bin) if tectonic_bin.exists() else "tectonic"
        print(f"[+] Found Tectonic engine ({tectonic_cmd}). Compiling all publication targets...")
        targets = [
            ("icde_main.tex", "icde_main.pdf"),
            ("main.tex", "main.pdf"),
            ("technical_report.tex", "technical_report.pdf"),
        ]
        for src, out_name in targets:
            print(f"  -> Compiling {src} via Tectonic...")
            try:
                subprocess.run([tectonic_cmd, "-X", "compile", str(base_dir / src), "--outdir", str(dist_dir)],
                               cwd=base_dir, check=True)
                print(f"     [SUCCESS] Built {dist_dir / out_name}")
            except Exception as e:
                print(f"     [!] Failed to compile {src}: {e}")
    elif has_latexmk or has_pdflatex:
        print("[+] Found local LaTeX compiler. Commencing PDF generation...")
        try:
            if has_latexmk:
                cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "main.tex"]
                subprocess.run(cmd, cwd=base_dir, check=True)
            else:
                for step, cmd in [
                    ("1/4: pdflatex", ["pdflatex", "-interaction=nonstopmode", "main.tex"]),
                    ("2/4: bibtex",   ["bibtex", "main"]),
                    ("3/4: pdflatex", ["pdflatex", "-interaction=nonstopmode", "main.tex"]),
                    ("4/4: pdflatex", ["pdflatex", "-interaction=nonstopmode", "main.tex"]),
                ]:
                    print(f"  -> Running {step}...")
                    subprocess.run(cmd, cwd=base_dir, check=True, stdout=subprocess.DEVNULL)
            
            pdf_path = base_dir / "main.pdf"
            if pdf_path.exists():
                dest_pdf = dist_dir / "IEEE_TKDE_Inductive_Consensus_Clustering.pdf"
                shutil.copy2(pdf_path, dest_pdf)
                print(f"[SUCCESS] Generated publication PDF: {dest_pdf}")
        except Exception as e:
            print(f"[!] Compilation failed: {e}")
    else:
        print("[*] No local LaTeX engine detected on PATH.")
        print("    Packaging complete Overleaf / IEEE ScholarOne bundle instead...")

    # 2. Package standalone submission ZIPs
    # 2a. Package TKDE Journal Submission ZIP
    tkde_zip = dist_dir / "IEEE_TKDE_Manuscript_Submission_Package.zip"
    print(f"\n[+] Bundling TKDE journal submission package: {tkde_zip.name}...")

    tkde_files = [
        "main.tex",
        "references.bib",
        "IEEEtran.cls",
        "IEEEtran.bst",
        "IEEEtrantools.sty",
        "IEEEabrv.bib",
        "supplementary_tables.tex",
        "IEEE_VENUE_TARGET.md",
        "README.md",
    ]

    with zipfile.ZipFile(tkde_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in tkde_files:
            p = base_dir / f
            if p.exists():
                z.write(p, arcname=f)
                print(f"  Packed root file: {f}")

        fig_dir = base_dir / "figures"
        if fig_dir.exists():
            for fig in fig_dir.glob("*.png"):
                z.write(fig, arcname=f"figures/{fig.name}")
            print(f"  Packed figures directory ({len(list(fig_dir.glob('*.png')))} assets)")

        for sc in (base_dir / "scripts").glob("*.py"):
            z.write(sc, arcname=f"scripts/{sc.name}")
        print("  Packed verification scripts")

    # 2b. Package ICDE 2027 Double-Blind Conference Package
    icde_zip = dist_dir / "IEEE_ICDE_2027_Submission_Package.zip"
    print(f"\n[+] Bundling ICDE 2027 double-blind conference package: {icde_zip.name}...")

    icde_files = [
        ("icde_main.tex", "main.tex"),
        ("references.bib", "references.bib"),
        ("IEEEtran.cls", "IEEEtran.cls"),
        ("IEEEtran.bst", "IEEEtran.bst"),
        ("IEEEtrantools.sty", "IEEEtrantools.sty"),
        ("IEEEabrv.bib", "IEEEabrv.bib"),
        ("technical_report.tex", "technical_report.tex"),
        ("supplementary_tables.tex", "supplementary_tables.tex"),
    ]

    with zipfile.ZipFile(icde_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for src_name, arc_name in icde_files:
            p = base_dir / src_name
            if p.exists():
                z.write(p, arcname=arc_name)
                print(f"  Packed ICDE file: {src_name} -> {arc_name}")

        fig_dir = base_dir / "figures"
        if fig_dir.exists():
            for fig in fig_dir.glob("*.png"):
                z.write(fig, arcname=f"figures/{fig.name}")
            print(f"  Packed figures directory ({len(list(fig_dir.glob('*.png')))} assets)")

        for sc in (base_dir / "scripts").glob("*.py"):
            z.write(sc, arcname=f"scripts/{sc.name}")
        print("  Packed verification scripts")

    print("\n" + "=" * 70)
    print(f"TKDE Package: {tkde_zip} ({tkde_zip.stat().st_size / (1024*1024):.2f} MB)")
    print(f"ICDE Package: {icde_zip} ({icde_zip.stat().st_size / (1024*1024):.2f} MB)")
    print("Upload either zip directly to Overleaf (New Project -> Upload Project)")
    print("=" * 70)

if __name__ == "__main__":
    build()
