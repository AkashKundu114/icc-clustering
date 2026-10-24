"""
Packages the Springer Nature submission bundle and Overleaf bundle.
"""
import zipfile
from pathlib import Path


def create_bundle(source_dir: Path, output_zip: Path):
    source_dir = Path(source_dir)
    output_zip = Path(output_zip)
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    
    files_to_include = [
        "ICCv2_Consensus_Clustering.tex",
        "ICCv2_Consensus_Clustering.pdf",
        "main.tex",
        "main.pdf",
        "numbers.tex",
        "references.bib",
        "sn-jnl.cls",
        "empty.eps",
        "fig.eps",
        "sn-apacite.bst",
        "sn-aps.bst",
        "sn-basic.bst",
        "sn-chicago.bst",
        "sn-mathphys-ay.bst",
        "sn-mathphys-num.bst",
        "sn-nature.bst",
        "sn-vancouver-ay.bst",
        "sn-vancouver-num.bst",
    ]
    
    with zipfile.ZipFile(output_zip, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for fname in files_to_include:
            fpath = source_dir / fname
            if fpath.exists():
                z.write(fpath, arcname=fname)
            else:
                # check if in paper/
                fpath_alt = Path("paper") / fname
                if fpath_alt.exists():
                    z.write(fpath_alt, arcname=fname)
        
        # Add bst directory
        bst_dir = source_dir / "bst"
        if not bst_dir.exists():
            bst_dir = Path("paper/bst")
        if bst_dir.exists():
            for f in bst_dir.glob("*.bst"):
                z.write(f, arcname=f"bst/{f.name}")
        
        # Add figures directory
        fig_dir = source_dir / "figures"
        if not fig_dir.exists():
            fig_dir = Path("paper/figures")
        if fig_dir.exists():
            for f in fig_dir.glob("*.*"):
                z.write(f, arcname=f"figures/{f.name}")
                
    print(f"Created {output_zip} ({output_zip.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    # Paper bundles
    create_bundle(Path("paper"), Path("paper/springer_nature_submission_package.zip"))
    create_bundle(Path("paper"), Path("paper/springer_overleaf.zip"))
    
    # Springer manuscript bundles
    create_bundle(Path("springer_manuscript"), Path("springer_manuscript/springer_nature_submission_package.zip"))
    create_bundle(Path("springer_manuscript"), Path("springer_manuscript/springer_overleaf.zip"))
