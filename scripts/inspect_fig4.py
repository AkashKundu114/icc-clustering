from pathlib import Path

p = Path("experiments/exp1_generalization/src/plot_exp1_figures.py")
text = p.read_text(encoding="utf-8")
lines = text.splitlines()

for i, l in enumerate(lines):
    if "set_title" in l or "suptitle" in l or "savefig" in l or "fig9" in l or "fig10" in l:
        print(f"{i+1}: {l}")
