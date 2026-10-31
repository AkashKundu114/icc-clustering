from pathlib import Path

p = Path("experiments/exp1_generalization/src/plot_exp1_figures.py")
text = p.read_text(encoding="utf-8")

old_o1 = r'ax1.set_title(r"(a) Out-of-Sample Generalization on Held-Out Test Set (20%)", fontsize=13.0, fontweight="bold")'
new_o1 = r'ax1.set_title(r"Out-of-Sample Generalization on Held-Out Test Set (20%)", fontsize=12.0, fontweight="bold")'

old_o2 = r'ax2.set_title(r"(b) Sample Complexity Tradeoff: 50% Core vs 100% Full Training Set", fontsize=13.0, fontweight="bold")'
new_o2 = r'ax2.set_title(r"Sample Complexity Tradeoff (50% Core vs. 100% Full)", fontsize=12.0, fontweight="bold")'

old_p1 = r'ax1.set_title(r"(a) Unsupervised Pseudo-Label Generalization to Test Set", fontsize=13.0, fontweight="bold")'
new_p1 = r'ax1.set_title(r"Unsupervised Pseudo-Label Generalization to Test Set", fontsize=12.0, fontweight="bold")'

old_p2 = r'ax2.set_title(r"(b) Core Filtering Advantage under Corrupted Pseudo-Labels", fontsize=13.0, fontweight="bold")'
new_p2 = r'ax2.set_title(r"Core Filtering Advantage under Corrupted Pseudo-Labels", fontsize=12.0, fontweight="bold")'

for old, new in [(old_o1, new_o1), (old_o2, new_o2), (old_p1, new_p1), (old_p2, new_p2)]:
    assert old in text, f"Target not found: {old}"
    text = text.replace(old, new)

p.write_text(text, encoding="utf-8")
print(f"Successfully updated {p}")
