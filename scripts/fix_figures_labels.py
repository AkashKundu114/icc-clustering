import os
import shutil
from pathlib import Path

# 1. Update plot_exp2_figures.py
p1 = Path("experiments/exp2_ablation/src/plot_exp2_figures.py")
if p1.exists():
    text = p1.read_text(encoding="utf-8")
    text = text.replace("VSSG + K-Means", "BGSS + K-Means")
    text = text.replace("VSSG + Std Consensus", "BGSS + Std Consensus")
    text = text.replace("VSSG + Random Anchors", "BGSS + Random Anchors")
    text = text.replace("VSSG Shielding Lift", "BGSS Shielding Lift")
    p1.write_text(text, encoding="utf-8")
    print("Updated plot_exp2_figures.py")

# 2. Update plot_vssg_figures.py
p2 = Path("experiments/exp2_ablation/src/plot_vssg_figures.py")
if p2.exists():
    text = p2.read_text(encoding="utf-8")
    text = text.replace("VSSG Feature Recovery", "BGSS Feature Recovery")
    text = text.replace("VSSG Signal Recovery", "BGSS Signal Recovery")
    p2.write_text(text, encoding="utf-8")
    print("Updated plot_vssg_figures.py")

# 3. Update plot_anchor_fidelity.py
p3 = Path("experiments/exp4_scalability_and_sensitivity/src/plot_anchor_fidelity.py")
if p3.exists():
    text = p3.read_text(encoding="utf-8")
    text = text.replace("fig.tight_layout()", "fig.tight_layout(pad=2.5)")
    p3.write_text(text, encoding="utf-8")
    print("Updated plot_anchor_fidelity.py")
