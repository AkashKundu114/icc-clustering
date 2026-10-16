import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

def sync_figures():
    """Synchronize all experiment figures to manuscript directories."""
    target_dirs = [
        ROOT_DIR / "manuscript" / "figures",
        ROOT_DIR / "paper" / "figures",
        ROOT_DIR / "springer_manuscript" / "figures"
    ]
    for d in target_dirs:
        d.mkdir(parents=True, exist_ok=True)

    copied = 0
    exp_dir = ROOT_DIR / "experiments"
    for fig_file in exp_dir.rglob("*.png"):
        if "figures" in fig_file.parts and not fig_file.name.startswith("."):
            for d in target_dirs:
                shutil.copy2(fig_file, d / fig_file.name)
            copied += 1

    top_fig_dir = ROOT_DIR / "figures"
    if top_fig_dir.exists():
        for fig_file in top_fig_dir.glob("*.png"):
            for d in target_dirs:
                shutil.copy2(fig_file, d / fig_file.name)
            copied += 1

    print(f"Total figures synced across manuscript directories: {copied}")

if __name__ == "__main__":
    sync_figures()
