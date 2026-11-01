# -*- coding: utf-8 -*-
r"""
Synchronizes verified codebase, paper artifacts, results, figures, tables,
and documentation from D:\Final Year Project to D:\icc-clustering.
"""
import shutil
from pathlib import Path

SRC = Path(r"D:\Final Year Project")
DST = Path(r"D:\icc-clustering")

def sync_dir(src_d: Path, dst_d: Path, ext_filter=None):
    if not src_d.exists():
        return
    dst_d.mkdir(parents=True, exist_ok=True)
    count = 0
    for f in src_d.glob("*"):
        if f.is_file():
            if ext_filter and f.suffix not in ext_filter:
                continue
            shutil.copy2(f, dst_d / f.name)
            count += 1
    print(f"Synced {count} files from {src_d.relative_to(SRC)} to {dst_d.relative_to(DST)}")

def main():
    print(f"Syncing from {SRC} to {DST}...")

    # 1. Source code (src/)
    shutil.copytree(SRC / "src", DST / "src", dirs_exist_ok=True)
    print("Synced: src/")

    # 2. Results (stats.json, passF, stability)
    if (SRC / "results" / "stats.json").exists():
        shutil.copy2(SRC / "results" / "stats.json", DST / "results" / "stats.json")
        print("Synced: results/stats.json")
    sync_dir(SRC / "results" / "passF", DST / "results" / "passF")
    sync_dir(SRC / "results" / "stability", DST / "results" / "stability")

    # 3. Figures (paper/figures, experiments/exp0_falsification/figures)
    sync_dir(SRC / "paper" / "figures", DST / "paper" / "figures", ext_filter=[".png", ".jpg", ".pdf"])
    sync_dir(SRC / "springer_manuscript" / "figures", DST / "springer_manuscript" / "figures", ext_filter=[".png", ".jpg", ".pdf"])
    sync_dir(SRC / "experiments" / "exp0_falsification" / "figures", DST / "experiments" / "exp0_falsification" / "figures", ext_filter=[".png", ".jpg", ".pdf"])

    # 4. LaTeX tables (paper/gen, springer_manuscript/gen)
    sync_dir(SRC / "paper" / "gen", DST / "paper" / "gen", ext_filter=[".tex"])
    sync_dir(SRC / "springer_manuscript" / "gen", DST / "springer_manuscript" / "gen", ext_filter=[".tex"])

    # 5. Paper and Manuscript core files
    for fname in ["main.tex", "main.pdf", "numbers.tex", "references.bib", "sn-jnl.cls"]:
        if (SRC / "paper" / fname).exists():
            shutil.copy2(SRC / "paper" / fname, DST / "paper" / fname)
        if (SRC / "springer_manuscript" / fname).exists():
            shutil.copy2(SRC / "springer_manuscript" / fname, DST / "springer_manuscript" / fname)
    print("Synced: paper/ and springer_manuscript/ main.tex, main.pdf, numbers.tex, references.bib")

    # 6. Submission zip packages
    for zname in ["springer_nature_submission_package.zip", "springer_overleaf.zip"]:
        if (SRC / "paper" / zname).exists():
            shutil.copy2(SRC / "paper" / zname, DST / "paper" / zname)
        if (SRC / "springer_manuscript" / zname).exists():
            shutil.copy2(SRC / "springer_manuscript" / zname, DST / "springer_manuscript" / zname)
    print("Synced: submission packages (.zip)")

    # 7. Key scripts
    scripts_to_sync = [
        "replot_fig2_subsample.py",
        "make_tables.py",
        "make_stability_outputs.py",
        "package_submission.py",
        "apply_final_submission_polish.py",
        "apply_checklist_fixes.py",
        "apply_final_reviewer_fixes.py",
        "plot_fig08_cd_diagram.py",
        "run_reconciliation_stats.py",
        "bootstrap_utils.py",
        "apply_latest_batch_fixes.py",
        "patch_fig4_titles.py",
        "verify_pdf_changes.py",
        "copy_fresh_figures.py",
    ]
    for s in scripts_to_sync:
        if (SRC / "scripts" / s).exists():
            shutil.copy2(SRC / "scripts" / s, DST / "scripts" / s)
        elif (SRC / s).exists():
            shutil.copy2(SRC / s, DST / "scripts" / s)
    print("Synced: key scripts")

    # 7b. Tests
    if (SRC / "tests" / "test_pdf_allowlist.py").exists():
        (DST / "tests").mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC / "tests" / "test_pdf_allowlist.py", DST / "tests" / "test_pdf_allowlist.py")
        print("Synced: tests/test_pdf_allowlist.py")

    # 8. Clean pycache in DST
    for p in DST.glob("**/__pycache__"):
        shutil.rmtree(p, ignore_errors=True)
    print("Cleaned __pycache__ in destination.")

if __name__ == "__main__":
    main()
