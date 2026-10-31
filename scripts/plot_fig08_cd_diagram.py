"""
Plots the Demšar Critical Difference (CD) Diagram for the 12 evaluated methods
across 13 benchmarks, matching results/stats.json and Table 10 / Table 6.
"""

from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent

# Load ranks from results/stats.json
stats_path = ROOT / "results" / "stats.json"
stats_data = json.loads(stats_path.read_text(encoding="utf-8"))
n13 = stats_data["N13"]
ranks_dict = n13["ranks"]
cd = float(n13["nemenyi_cd"]) # 4.62
n_datasets = 13
k_models = len(ranks_dict) # 12

# Order models by rank ascending (1 = best)
sorted_raw = sorted(ranks_dict.items(), key=lambda x: x[1])

MODEL_DISPLAY = {
    "K-Means": "K-Means",
    "Standard_Consensus": "Standard Consensus",
    "DEC": "DEC (ICML 2016)",
    "ICC_v2": "GAC Pipeline",
    "Ward": "Ward",
    "ICC_v1": "Anchor Consensus (Ungated)",
    "Spectral": "Spectral",
    "FCM": "FCM",
    "Core_Halo_Consensus": "Core-Halo Cons.",
    "FastMVC": "FastMVC (TKDE 2023)",
    "CoHiRF": "CoHiRF (2024)",
    "FCAG": "FCAG (TPAMI 2024)",
}

sorted_models = [MODEL_DISPLAY.get(m, m) for m, _ in sorted_raw]
sorted_r = [r for _, r in sorted_raw]

print("12-Model Ranks for CD Diagram:")
for m, r in zip(sorted_models, sorted_r):
    print(f"  {m:30s}: {r:.2f}")

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9.5,
    "axes.labelsize": 10.0,
    "axes.titlesize": 11.0,
    "xtick.labelsize": 9.0,
    "ytick.labelsize": 9.0,
    "figure.dpi": 300,
})

fig = plt.figure(figsize=(15.0, 5.8), dpi=300)
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.45], wspace=0.32)
ax_bar = fig.add_subplot(gs[0])
ax_cd = fig.add_subplot(gs[1])

# -------------------------------------------------------------------------
# Panel (a): Non-Parametric Rank Order Bar Chart
# -------------------------------------------------------------------------
y_pos = np.arange(k_models)
colors = []
for m in sorted_models:
    if "GAC" in m:
        colors.append("#d62728")
    elif "Ungated" in m:
        colors.append("#2ca02c")
    elif "FCAG" in m or "FastMVC" in m:
        colors.append("#8c564b")
    elif "DEC" in m:
        colors.append("#9467bd")
    elif "Consensus" in m or "Core-Halo" in m:
        colors.append("#1f77b4")
    elif "CoHiRF" in m:
        colors.append("#e377c2")
    else:
        colors.append("#6c757d")

bars = ax_bar.barh(
    y_pos,
    sorted_r,
    color=colors,
    edgecolor="black",
    linewidth=0.8,
    alpha=0.85,
    height=0.65,
)
ax_bar.set_yticks(y_pos)
ax_bar.set_yticklabels(sorted_models, fontweight="bold")
ax_bar.set_xlabel(f"Average Rank Across {n_datasets} Datasets (1 = Best)", fontweight="bold")
ax_bar.set_title(f"(a) Average Empirical Rank Distribution across {n_datasets} Benchmarks", fontweight="bold")
ax_bar.set_xlim(0, max(k_models + 0.5, np.max(sorted_r) + 1.2))
ax_bar.invert_yaxis()
ax_bar.grid(axis="x", linestyle=":", alpha=0.5)

for i, r in enumerate(sorted_r):
    ax_bar.text(r + 0.15, i, f"{r:.2f}", va="center", ha="left", fontweight="bold", fontsize=9.0)

# -------------------------------------------------------------------------
# Panel (b): Demšar Critical Difference (CD) Diagram
# -------------------------------------------------------------------------
ax_cd.set_xlim(-0.5, k_models + 1.5)
ax_cd.set_ylim(-7.2, 2.6)
ax_cd.axis("off")

axis_y = 0.5
ax_cd.plot([1, k_models], [axis_y, axis_y], color="black", linewidth=1.5)
for t in range(1, k_models + 1):
    ax_cd.plot([t, t], [axis_y, axis_y + 0.12], color="black", linewidth=1.2)
    ax_cd.text(t, axis_y + 0.22, str(t), ha="center", va="bottom", fontweight="bold", fontsize=9.5)
ax_cd.text((1 + k_models) / 2.0, axis_y + 0.70, "Average Rank", ha="center", va="bottom", fontweight="bold", fontsize=11)

# CD interval bar
cd_start = 1.0
cd_end = min(k_models, cd_start + cd)
cd_y = axis_y + 1.45
ax_cd.plot([cd_start, cd_end], [cd_y, cd_y], color="#d62728", linewidth=2.5)
ax_cd.plot([cd_start, cd_start], [cd_y - 0.1, cd_y + 0.1], color="#d62728", linewidth=2.0)
ax_cd.plot([cd_end, cd_end], [cd_y - 0.1, cd_y + 0.1], color="#d62728", linewidth=2.0)
ax_cd.text(
    (cd_start + cd_end) / 2.0,
    cd_y + 0.15,
    rf"$CD = {cd:.2f}$ (Nemenyi $\alpha=0.05$, $N={n_datasets}$, $k={k_models}$)",
    ha="center",
    va="bottom",
    fontweight="bold",
    color="#d62728",
    fontsize=9.0,
)

# Partition models: left side (ranks <= mid), right side (ranks > mid)
mid_rank = (1 + k_models) / 2.0
left_models = [(sorted_models[i], sorted_r[i]) for i in range(k_models) if sorted_r[i] <= mid_rank]
right_models = [(sorted_models[i], sorted_r[i]) for i in range(k_models) if sorted_r[i] > mid_rank]

# Left side labels
step_y_left = 5.2 / max(1, len(left_models))
for idx, (m, r) in enumerate(left_models):
    y_line = axis_y - 0.60 - idx * step_y_left
    c = "#d62728" if "GAC" in m else "#2ca02c" if "Ungated" in m else "#495057"
    ax_cd.plot([r, r], [axis_y, y_line], color=c, linewidth=1.2)
    ax_cd.plot([r, 0.30], [y_line, y_line], color=c, linewidth=1.2)
    ax_cd.text(0.20, y_line, f"{m} ({r:.2f})", ha="right", va="center", fontweight="bold", fontsize=9.0, color=c)
    ax_cd.plot(r, axis_y, marker="o", color=c, markersize=5.0)

# Right side labels
step_y_right = 5.2 / max(1, len(right_models))
for idx, (m, r) in enumerate(right_models):
    y_line = axis_y - 0.60 - idx * step_y_right
    c = "#1f77b4" if "Consensus" in m or "Core-Halo" in m else "#495057"
    ax_cd.plot([r, r], [axis_y, y_line], color=c, linewidth=1.2)
    ax_cd.plot([r, k_models + 0.70], [y_line, y_line], color=c, linewidth=1.2)
    ax_cd.text(k_models + 0.80, y_line, f"({r:.2f}) {m}", ha="left", va="center", fontweight="bold", fontsize=9.0, color=c)
    ax_cd.plot(r, axis_y, marker="o", color=c, markersize=5.0)

# Equivalence clique bar connecting all 12 methods (spread = 7.77 - 5.15 = 2.62 <= CD = 4.62)
clique_y = axis_y - 6.0
best_rank = sorted_r[0]    # 5.15 (K-Means)
worst_rank = sorted_r[-1]  # 7.77 (FCAG)
ax_cd.plot([best_rank, worst_rank], [clique_y, clique_y], color="#343a40", linewidth=4.0, solid_capstyle="round")
ax_cd.plot([best_rank, best_rank], [clique_y - 0.18, clique_y + 0.18], color="#343a40", linewidth=2.0)
ax_cd.plot([worst_rank, worst_rank], [clique_y - 0.18, clique_y + 0.18], color="#343a40", linewidth=2.0)
ax_cd.text(
    (best_rank + worst_rank) / 2.0,
    clique_y - 0.38,
    rf"Single Equivalence Group: all 12 methods ($\Delta R = {worst_rank - best_rank:.2f} \leq CD = {cd:.2f}$)",
    ha="center",
    va="top",
    fontsize=9.0,
    fontweight="bold",
    color="#212529",
)

ax_cd.set_title(rf"(b) Demšar Critical Difference Diagram ($\alpha=0.05$, $k={k_models}$)", fontweight="bold", fontsize=11.0, pad=10)

plt.suptitle(
    f"Non-Parametric Model Rankings & Statistical Separation Across {n_datasets} Real-World Benchmarks",
    fontweight="bold",
    fontsize=12.0,
    y=0.99,
)
plt.subplots_adjust(top=0.88)

save_paths = [
    ROOT / "paper" / "figures" / "fig08_critical_difference_diagram.png",
    ROOT / "paper" / "figures" / "fig17_critical_difference_diagram_v2.png",
    ROOT / "springer_manuscript" / "figures" / "fig08_critical_difference_diagram.png",
    ROOT / "springer_manuscript" / "figures" / "fig17_critical_difference_diagram_v2.png",
    ROOT / "experiments" / "exp3_real_world_benchmarks" / "figures" / "fig17_critical_difference_diagram_v2.png",
]

for p in save_paths:
    p.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(p, dpi=300, bbox_inches="tight")
    print(f"[+] Saved CD diagram to: {p}")

plt.close()
print("All CD diagrams successfully generated and saved.")
