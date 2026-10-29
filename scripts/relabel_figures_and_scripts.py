"""
scripts/relabel_figures_and_scripts.py

Relabels ICC-v2 and ICC-v1 in experiment plotting scripts:
- experiments/exp1_generalization/src/plot_exp1_figures.py
- experiments/exp2_ablation/src/plot_exp2_figures.py
- experiments/exp3_real_world_benchmarks/src/plot_exp3_figures.py
- experiments/exp4_scalability_and_sensitivity/src/plot_exp4_figures.py
- experiments/exp4_scalability_and_sensitivity/src/plot_anchor_fidelity.py
- experiments/exp5_extreme_scale/src/plot_exp5.py
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

SCRIPTS = [
    ROOT / "experiments" / "exp1_generalization" / "src" / "plot_exp1_figures.py",
    ROOT / "experiments" / "exp2_ablation" / "src" / "plot_exp2_figures.py",
    ROOT / "experiments" / "exp3_real_world_benchmarks" / "src" / "plot_exp3_figures.py",
    ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "src" / "plot_exp4_figures.py",
    ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "src" / "plot_anchor_fidelity.py",
    ROOT / "experiments" / "exp5_extreme_scale" / "src" / "plot_exp5.py",
]

REPLACEMENTS = [
    ("ICC-v2 (Ours)", "GAC Pipeline (Ours)"),
    ("ICC-v2 [Ours]", "GAC Pipeline [Ours]"),
    ("Full ICC-v2 [Ours]", "Full GAC Pipeline [Ours]"),
    ("Full ICC-v2", "Full GAC Pipeline"),
    ("ICC-v2 (BGSS+Anchor)", "GAC Pipeline (BGSS+Anchor)"),
    ("ICC-v2 (BGSS Gating)", "GAC Pipeline (BGSS Gating)"),
    ("ICC-v2 Bipartite Anchor", "GAC Pipeline Bipartite Anchor"),
    ("ICC-v2 (O(N) Anchor Ensemble)", "GAC Pipeline (O(N) Anchor Ensemble)"),
    ("ICC-v2 Peak Memory", "GAC Pipeline Peak Memory"),
    ("ICC-v2 Cluster Recovery", "GAC Pipeline Cluster Recovery"),
    ("ICC-v2 Performance Plateau", "GAC Pipeline Performance Plateau"),
    ("Dissecting Invariant Core Consensus (ICC-v2)", "Dissecting Gated Anchor Consensus (GAC)"),
    ("ICC-v1 (Anchor) O(N)", "Ungated AC (Anchor) O(N)"),
    ("ICC-v2 (BGSS+Anchor) O(N)", "GAC Pipeline (BGSS+Anchor) O(N)"),
    ("ICC-v1 (Anchor)", "Ungated AC (Anchor)"),
    ("ICC-v1 Calibrated Core (50%) [Ours]", "Ungated AC Calibrated Core (50%)"),
    ("Train on Core Pseudo-Labels Only (ICC-v1)", "Train on Core Pseudo-Labels Only (Ungated AC)"),
    ("ICC-v1", "Ungated AC"),
    ("ICC-v2: 1.9x speedup", "GAC Pipeline: 1.9x speedup"),
    ("ICC-v2: 10.35 s", "GAC Pipeline: 2.30 s"),
    ("ICC-v2", "GAC Pipeline"),
]

def main():
    for p in SCRIPTS:
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8")
        orig = txt
        for old_s, new_s in REPLACEMENTS:
            txt = txt.replace(old_s, new_s)
        if txt != orig:
            p.write_text(txt, encoding="utf-8")
            print(f"[*] Updated plotting script: {p.name}")

if __name__ == "__main__":
    main()
