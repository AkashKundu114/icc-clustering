from pathlib import Path

p = Path("scripts/make_stability_outputs.py")
text = p.read_text(encoding="utf-8")

old_block = '''    ax1.axvspan(-0.15, 0.05, ymin=0.50, ymax=1.05, color="#ffdddd", alpha=0.35, zorder=1)
    ax1.text(
        -0.03,
        0.82,
        "RULE (i') [ADDED POST HOC]:\\nNON-DEGENERATE ZONE\\n(Subsample Stab $\\\\geq 0.50$, Acc $\\\\leq 0.05$,\\nMin Cluster $\\\\geq 5$%)",
        fontsize=9.0,
        fontweight="bold",
        color="#cc0000",
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff5f5", edgecolor="#cc0000", alpha=0.9),
    )'''

new_block = '''    ax1.axvspan(-0.16, 0.05, ymin=0.50, ymax=1.05, color="#ffdddd", alpha=0.35, zorder=1)
    ax1.text(
        -0.155,
        0.82,
        "Rule (i') Non-Degenerate Zone\\n(Added Post Hoc)\\n"
        r"$\\bullet$ Subsample Stab $\\geq 0.50$" "\\n"
        r"$\\bullet$ Subsample Acc $\\leq 0.05$" "\\n"
        r"$\\bullet$ Min Cluster $\\geq 5\\%$",
        fontsize=8.0,
        fontweight="bold",
        color="#8b0000",
        ha="left",
        va="center",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#cc0000", linewidth=1.2, alpha=0.96),
        zorder=15,
    )'''

assert old_block in text, "old_block not found in text"
text = text.replace(old_block, new_block)

# Also update xlim and diagonal
old_xlim = 'ax1.set_xlim(-0.10, 0.65)'
new_xlim = 'ax1.set_xlim(-0.16, 0.65)'
assert old_xlim in text
text = text.replace(old_xlim, new_xlim)

old_diag = 'ax1.plot([-0.1, 0.7], [-0.1, 0.7]'
new_diag = 'ax1.plot([-0.16, 0.7], [-0.16, 0.7]'
assert old_diag in text
text = text.replace(old_diag, new_diag)

p.write_text(text, encoding="utf-8")
print(f"Successfully patched {p}")
