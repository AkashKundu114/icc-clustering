import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 5))
ax.axvspan(-0.14, 0.05, ymin=0.50, ymax=1.05, color="#ffdddd", alpha=0.35)
ax.set_xlim(-0.14, 0.65)
ax.set_ylim(-0.05, 1.05)

# Place text on the left in the empty corridor
ax.text(
    -0.135,
    0.80,
    "Rule (i') Non-Degenerate Zone\n(Added Post Hoc)\n"
    r"$\bullet\ \text{Subsample Stab} \geq 0.50$" "\n"
    r"$\bullet\ \text{Empirical Acc} \leq 0.05$" "\n"
    r"$\bullet\ \text{Min Cluster} \geq 5\%$",
    fontsize=8.5,
    fontweight="bold",
    color="#990000",
    ha="left",
    va="center",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#cc0000", linewidth=1.2, alpha=0.95),
)

plt.savefig("scripts/test_banner.png", bbox_inches="tight", dpi=200)
print("Saved test_banner.png")
