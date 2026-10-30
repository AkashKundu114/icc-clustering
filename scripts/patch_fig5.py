import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

p1 = ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "src" / "plot_exp4_figures.py"
text1 = p1.read_text(encoding="utf-8")

old_anno = 'ax1.annotate("GAC Pipeline: 3.8x speedup at N=10,000\\n(0.835s vs. 3.175s untraced)",\n                 xy=(10000, 0.835), xytext=(1200, 0.35),'
new_anno = 'ax1.annotate("GAC Pipeline: 2.7x speedup at N=10,000\\n(4.35s vs. 11.05s untraced)",\n                 xy=(10000, 4.354), xytext=(1200, 1.2),'

assert old_anno in text1, "old_anno not found in plot_exp4_figures.py"
text1 = text1.replace(old_anno, new_anno)

old_save = '            plt.savefig(tdir / "fig18_sample_complexity_scaling.png", dpi=300, bbox_inches="tight")'
new_save = '            plt.savefig(tdir / "fig18_sample_complexity_scaling.png", dpi=300, bbox_inches="tight")\n            plt.savefig(tdir / "fig05a_sample_complexity_scaling.png", dpi=300, bbox_inches="tight")'

assert old_save in text1, "old_save not found in plot_exp4_figures.py"
text1 = text1.replace(old_save, new_save)
p1.write_text(text1, encoding="utf-8")
print("Patched plot_exp4_figures.py")

p2 = ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "src" / "plot_anchor_fidelity.py"
text2 = p2.read_text(encoding="utf-8")

old_f2_save = '    out_file = FIGURES_DIR / "fig24_anchor_fidelity_quad.png"\n    plt.savefig(out_file, dpi=300, bbox_inches="tight")'
new_f2_save = '''    out_file = FIGURES_DIR / "fig24_anchor_fidelity_quad.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    for tdir in [ROOT / "springer_manuscript" / "figures",
                 ROOT / "paper" / "figures",
                 ROOT / "manuscript" / "figures",
                 ROOT / "figures"]:
        if tdir.exists():
            plt.savefig(tdir / "fig24_anchor_fidelity_quad.png", dpi=300, bbox_inches="tight")
            plt.savefig(tdir / "fig05b_scalability_breakdown.png", dpi=300, bbox_inches="tight")'''

assert old_f2_save in text2, "old_f2_save not found in plot_anchor_fidelity.py"
text2 = text2.replace(old_f2_save, new_f2_save)
p2.write_text(text2, encoding="utf-8")
print("Patched plot_anchor_fidelity.py")
