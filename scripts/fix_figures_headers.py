"""
Fix overlapping titles and headers in figures.
"""

def fix_exp1():
    p = "experiments/exp1_generalization/src/plot_exp1_figures.py"
    with open(p, "r", encoding="utf-8") as f:
        text = f.read()

    # In fig9 and fig10, do tight_layout then suptitle with bbox
    text = text.replace(
        'plt.suptitle("Downstream Classifier Generalization from Oracle True Labels",\n                     fontweight="bold", fontsize=14.0, y=0.995)\n        plt.tight_layout()',
        'plt.tight_layout()\n        plt.subplots_adjust(top=0.90)\n        plt.suptitle("Downstream Classifier Generalization from Oracle True Labels",\n                     fontweight="bold", fontsize=13.0, y=0.98)'
    )
    text = text.replace(
        'plt.suptitle("Downstream Generalization from Unsupervised Pseudo-Labels",\n                     fontweight="bold", fontsize=14.0, y=0.995)\n        plt.tight_layout()',
        'plt.tight_layout()\n        plt.subplots_adjust(top=0.90)\n        plt.suptitle("Downstream Generalization from Unsupervised Pseudo-Labels",\n                     fontweight="bold", fontsize=13.0, y=0.98)'
    )

    with open(p, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(text)
    print("[*] Fixed exp1 plot titles")


def fix_vssg_legends():
    # 1. plot_exp3_figures.py
    p3 = "experiments/exp3_real_world_benchmarks/src/plot_exp3_figures.py"
    with open(p3, "r", encoding="utf-8") as f:
        t3 = f.read()
    t3 = t3.replace('"ICC_v2": "ICC-v2 (VSSG+Anchor)"', '"ICC_v2": "ICC-v2 (BGSS+Anchor)"')
    with open(p3, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(t3)
    print("[*] Fixed VSSG in plot_exp3_figures.py")

    # 2. plot_exp4_figures.py
    p4 = "experiments/exp4_scalability_and_sensitivity/src/plot_exp4_figures.py"
    with open(p4, "r", encoding="utf-8") as f:
        t4 = f.read()
    t4 = t4.replace('"ICC_v2": "ICC-v2 (VSSG+Anchor) O(N)"', '"ICC_v2": "ICC-v2 (BGSS+Anchor) O(N)"')
    t4 = t4.replace('VSSG Feature Gating:', 'BGSS Feature Gating:')
    with open(p4, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(t4)
    print("[*] Fixed VSSG in plot_exp4_figures.py")

    # 3. plot_exp5.py
    p5 = "experiments/exp5_extreme_scale/src/plot_exp5.py"
    with open(p5, "r", encoding="utf-8") as f:
        t5 = f.read()
    t5 = t5.replace('label="ICC-v2 (VSSG Gating)"', 'label="ICC-v2 (BGSS Gating)"')
    with open(p5, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(t5)
    print("[*] Fixed VSSG in plot_exp5.py")

    # 4. plot_missing_data.py
    pm = "experiments/exp3_real_world_benchmarks/src/plot_missing_data.py"
    with open(pm, "r", encoding="utf-8") as f:
        tm = f.read()
    tm = tm.replace('"ICC_v2": ("#d62728", "-", "*", "ICC-v2 (VSSG+Anchor, Ours)")', '"ICC_v2": ("#d62728", "-", "*", "ICC-v2 (BGSS+Anchor, Ours)")')
    with open(pm, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(tm)
    print("[*] Fixed VSSG in plot_missing_data.py")


if __name__ == "__main__":
    fix_exp1()
    fix_vssg_legends()
