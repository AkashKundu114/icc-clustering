#!/usr/bin/env python3
"""
Automated Springer Nature Manuscript Compilation & Submission Packaging Script.

1. Verifies/compiles main.pdf via Tectonic if requested/needed.
2. Builds self-contained submission packages:
   - springer_nature_submission_package.zip
   - springer_overleaf.zip
3. Synchronizes packages and PDFs across mirror directories (springer_manuscript, paper).
4. Verifies zip structure and file integrity.
"""

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "springer_manuscript"
PAPER_DIR = REPO_ROOT / "paper"
TECTONIC_BIN = REPO_ROOT / "manuscript" / "scripts" / "bin" / "tectonic.exe"

def compile_pdf():
    print("[1/4] Compiling Springer Nature manuscript via Tectonic...")
    if not TECTONIC_BIN.exists():
        print(f"Error: Tectonic binary not found at {TECTONIC_BIN}")
        sys.exit(1)

    cmd = [
        str(TECTONIC_BIN),
        "-X", "compile",
        str(SRC_DIR / "main.tex"),
        "--outdir", str(SRC_DIR)
    ]
    print(f"  Executing: {' '.join(cmd)}")
    res = subprocess.run(cmd, check=True)
    if res.returncode != 0:
        print("Tectonic compilation failed!")
        sys.exit(res.returncode)

    pdf_path = SRC_DIR / "main.pdf"
    if not pdf_path.exists():
        print(f"Error: {pdf_path} was not generated.")
        sys.exit(1)

    print(f"  [SUCCESS] Compiled {pdf_path} ({pdf_path.stat().st_size / (1024*1024):.2f} MB)")

def create_packages():
    print("\n[2/4] Bundling submission zip packages...")

    core_files = [
        "main.tex",
        "main.pdf",
        "numbers.tex",
        "references.bib",
        "sn-jnl.cls",
        "empty.eps",
        "fig.eps",
    ]

    # Find BST files
    bst_files = list(SRC_DIR.glob("*.bst")) + list((SRC_DIR / "bst").glob("*.bst"))
    # Figures
    fig_files = list((SRC_DIR / "figures").glob("*"))

    zip_targets = [
        SRC_DIR / "springer_nature_submission_package.zip",
        SRC_DIR / "springer_overleaf.zip",
    ]

    for zip_path in zip_targets:
        print(f"  Writing {zip_path.name}...")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for fname in core_files:
                fpath = SRC_DIR / fname
                if fpath.exists():
                    z.write(fpath, arcname=fname)

            # Store BST files at root and under bst/
            seen_bst = set()
            for bst in bst_files:
                if bst.name not in seen_bst:
                    z.write(bst, arcname=bst.name)
                    z.write(bst, arcname=f"bst/{bst.name}")
                    seen_bst.add(bst.name)

            for fig in fig_files:
                if fig.is_file():
                    z.write(fig, arcname=f"figures/{fig.name}")

        print(f"    -> Created {zip_path.name} ({zip_path.stat().st_size / (1024*1024):.2f} MB)")

def sync_mirrors():
    print("\n[3/4] Synchronizing artifacts across mirror locations...")
    mirrors = [PAPER_DIR, REPO_ROOT / "manuscript"]
    sync_items = [
        "main.tex",
        "main.pdf",
        "numbers.tex",
        "springer_nature_submission_package.zip",
        "springer_overleaf.zip",
    ]

    for mirror in mirrors:
        if mirror.exists():
            for item in sync_items:
                src_item = SRC_DIR / item
                dst_item = mirror / item
                if src_item.exists():
                    shutil.copy2(src_item, dst_item)
                    print(f"  Copied {item} to {mirror.name}/")

def verify_package():
    print("\n[4/4] Verifying submission package contents...")
    pkg_path = SRC_DIR / "springer_nature_submission_package.zip"
    with zipfile.ZipFile(pkg_path, "r") as z:
        names = set(z.namelist())
        required = ["main.tex", "main.pdf", "numbers.tex", "references.bib", "sn-jnl.cls"]
        missing = [req for req in required if req not in names]
        if missing:
            print(f"Error: Submission package missing essential files: {missing}")
            sys.exit(1)
        print(f"  [OK] Package verified with {len(names)} files including all required sources.")

if __name__ == "__main__":
    compile_pdf()
    create_packages()
    sync_mirrors()
    verify_package()
    print("\n[COMPLETED] Submission package and PDF build successful!")
