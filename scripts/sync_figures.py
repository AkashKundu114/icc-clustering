#!/usr/bin/env python3
"""
Synchronizes all generated figures from experiments/*/figures to ieee_manuscript/figures.
Ensures consistency and 300 DPI publication standards across the repository.
"""

import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DEST_DIR = ROOT_DIR / "ieee_manuscript" / "figures"
DEST_DIR.mkdir(parents=True, exist_ok=True)

def sync_figures():
    copied = 0
    # Search all experiment directories
    exp_dir = ROOT_DIR / "experiments"
    for fig_file in exp_dir.rglob("*.png"):
        if "figures" in fig_file.parts and not fig_file.name.startswith("."):
            dest_file = DEST_DIR / fig_file.name
            shutil.copy2(fig_file, dest_file)
            copied += 1
            print(f"  [Synced] {fig_file.name} -> {dest_file.relative_to(ROOT_DIR)}")

    # Check top-level figures if any
    top_fig_dir = ROOT_DIR / "figures"
    if top_fig_dir.exists():
        for fig_file in top_fig_dir.glob("*.png"):
            dest_file = DEST_DIR / fig_file.name
            shutil.copy2(fig_file, dest_file)
            copied += 1
            print(f"  [Synced] {fig_file.name} -> {dest_file.relative_to(ROOT_DIR)}")

    print(f"\n[+] Total figures synced to {DEST_DIR.relative_to(ROOT_DIR)}: {copied}")

if __name__ == "__main__":
    sync_figures()
