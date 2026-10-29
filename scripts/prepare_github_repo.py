"""
Prepares D:\icc-clustering for GitHub upload:
1. Removes all useless, obsolete, duplicate, and temporary files from D:\icc-clustering.
2. Synchronizes verified manuscript, figures, tables, stats, tests, and scripts from D:\Final Year Project.
3. Cleans all __pycache__ and temp build files.
"""
import os
import shutil
from pathlib import Path

SRC = Path(r"D:\Final Year Project")
DST = Path(r"D:\icc-clustering")

def main():
    print(f"Source (Local): {SRC}")
    print(f"Destination (GitHub Ready): {DST}")
    
    # 1. Removals of useless / obsolete folders and files from DST
    items_to_remove = [
        DST / "ieee_manuscript",
        DST / "manuscript",
        DST / "springer_manuscript" / "springer_manuscript",
        DST / ".coverage",
        DST / ".pytest_cache",
        DST / ".ruff_cache",
        DST / "paper" / "main_fixed.pdf",
        DST / "paper" / "main_fixed.tex",
        DST / "paper" / "technical_report.pdf",
        DST / "paper" / "technical_report.tex",
        DST / "paper" / "ICCv2_Consensus_Clustering.pdf",
        DST / "paper" / "ICCv2_Consensus_Clustering.tex",
        DST / "paper" / "sn-article.pdf",
        DST / "paper" / "sn-article.tex",
        DST / "paper" / "user-manual.pdf",
        DST / "paper" / "springer_nature_submission_package.zip",
        DST / "paper" / "springer_overleaf.zip",
        DST / "paper" / "empty.eps",
        DST / "paper" / "fig.eps",
        DST / "springer_manuscript" / "ICCv2_Consensus_Clustering.pdf",
        DST / "springer_manuscript" / "ICCv2_Consensus_Clustering.tex",
        DST / "springer_manuscript" / "sn-article.pdf",
        DST / "springer_manuscript" / "sn-article.tex",
        DST / "springer_manuscript" / "user-manual.pdf",
        DST / "springer_manuscript" / "springer_nature_submission_package.zip",
        DST / "springer_manuscript" / "springer_overleaf.zip",
        DST / "springer_manuscript" / "empty.eps",
        DST / "springer_manuscript" / "fig.eps",
        DST / "springer_manuscript" / "main.aux",
        DST / "springer_manuscript" / "main.bbl",
        DST / "springer_manuscript" / "main.out",
    ]
    
    freed_bytes = 0
    for p in items_to_remove:
        if p.exists():
            if p.is_dir():
                sz = sum(f.stat().st_size for f in p.glob("**/*") if f.is_file())
                shutil.rmtree(p)
            else:
                sz = p.stat().st_size
                p.unlink()
            freed_bytes += sz
            print(f"Removed: {p.relative_to(DST)} ({sz / (1024*1024):.2f} MB)")
            
    # Clean all __pycache__ in DST
    for pycache in DST.glob("**/__pycache__"):
        if pycache.exists():
            shutil.rmtree(pycache)
            print(f"Cleaned pycache: {pycache.relative_to(DST)}")
            
    print(f"Total space freed in {DST.name}: {freed_bytes / (1024*1024):.2f} MB\n")
    
    # 2. Synchronization of core assets from SRC to DST
    
    # Root files
    shutil.copy2(SRC / "REVISION_LOG.md", DST / "REVISION_LOG.md")
    print("Synced: REVISION_LOG.md")
    
    # Results
    for rf in ["stats.json", "refs_report.csv", "query_latency.json"]:
        src_f = SRC / "results" / rf
        if src_f.exists():
            shutil.copy2(src_f, DST / "results" / rf)
            print(f"Synced: results/{rf}")
            
    # Governance
    gov_conf = SRC / "governance" / "preregistration" / "AUTHOR_CONFIRMATION.md"
    if gov_conf.exists():
        (DST / "governance" / "preregistration").mkdir(parents=True, exist_ok=True)
        shutil.copy2(gov_conf, DST / "governance" / "preregistration" / "AUTHOR_CONFIRMATION.md")
        print("Synced: governance/preregistration/AUTHOR_CONFIRMATION.md")
        
    # Tests
    shutil.copy2(SRC / "tests" / "test_pdf_allowlist.py", DST / "tests" / "test_pdf_allowlist.py")
    print("Synced: tests/test_pdf_allowlist.py")
    
    # Scripts (key reproducibility scripts)
    key_scripts = [
        "check_numbers.py",
        "make_stats.py",
        "verify_refs.py",
        "measure_query_latency.py",
        "rerun_table4_timing.py",
        "package_submission.py",
        "plot_conceptual_framework.py"
    ]
    for s in key_scripts:
        src_s = SRC / "scripts" / s
        if src_s.exists():
            shutil.copy2(src_s, DST / "scripts" / s)
            print(f"Synced: scripts/{s}")
            
    # Paper assets
    paper_files = [
        "main.tex",
        "main.pdf",
        "numbers.tex",
        "references.bib",
        "sn-jnl.cls"
    ]
    for pf in paper_files:
        src_pf = SRC / "paper" / pf
        if src_pf.exists():
            shutil.copy2(src_pf, DST / "paper" / pf)
            print(f"Synced: paper/{pf}")
            
    # Gen tables in paper
    src_gen = SRC / "paper" / "gen"
    dst_gen = DST / "paper" / "gen"
    if src_gen.exists():
        dst_gen.mkdir(parents=True, exist_ok=True)
        for gf in src_gen.glob("*.tex"):
            shutil.copy2(gf, dst_gen / gf.name)
        print("Synced: paper/gen/ tables")
        
    # Figures in paper
    src_figs = SRC / "paper" / "figures"
    dst_figs = DST / "paper" / "figures"
    if src_figs.exists():
        dst_figs.mkdir(parents=True, exist_ok=True)
        for ff in src_figs.glob("*.png"):
            shutil.copy2(ff, dst_figs / ff.name)
        for ff in src_figs.glob("*.jpg"):
            shutil.copy2(ff, dst_figs / ff.name)
        print("Synced: paper/figures/")
        
    # Keep springer_manuscript in sync with paper numbers.tex & main.tex
    if (DST / "springer_manuscript").exists():
        shutil.copy2(SRC / "paper" / "numbers.tex", DST / "springer_manuscript" / "numbers.tex")
        shutil.copy2(SRC / "paper" / "main.tex", DST / "springer_manuscript" / "main.tex")
        shutil.copy2(SRC / "paper" / "main.pdf", DST / "springer_manuscript" / "main.pdf")
        print("Synced: springer_manuscript/ numbers and main.tex/pdf")
        
    # Experiments plotting scripts and figures
    for exp_dir in ["exp1_generalization", "exp2_ablation", "exp3_real_world_benchmarks", 
                    "exp4_scalability_and_sensitivity", "exp5_extreme_scale"]:
        s_exp = SRC / "experiments" / exp_dir
        d_exp = DST / "experiments" / exp_dir
        if s_exp.exists() and d_exp.exists():
            # Sync src python files
            if (s_exp / "src").exists():
                for py in (s_exp / "src").glob("*.py"):
                    shutil.copy2(py, d_exp / "src" / py.name)
            # Sync figures
            if (s_exp / "figures").exists():
                for fig in (s_exp / "figures").glob("*.png"):
                    shutil.copy2(fig, d_exp / "figures" / fig.name)
            # Sync data if updated
            if (s_exp / "data").exists():
                for dat in (s_exp / "data").glob("*.csv"):
                    shutil.copy2(dat, d_exp / "data" / dat.name)
            print(f"Synced experiments: {exp_dir}")

    print("\nSynchronization and cleanup complete!")

if __name__ == "__main__":
    main()
