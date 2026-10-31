import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Palette matching the paper
PALETTE = {
    "fcm": "#9467bd",       # purple
    "gmm": "#ff7f0e",       # orange
    "kmeans": "#1f77b4",    # blue
    "spectral": "#d62728",  # red
    "ward": "#2ca02c",      # green
}

# Subsample evaluation data (20 stratified 80% subsample draws, N=300, K=3)
data = [
    {"d_noise": 0, "clusterer": "kmeans", "stab": 0.693262, "acc": 0.806162, "gap": -0.112900},
    {"d_noise": 0, "clusterer": "gmm", "stab": 1.000000, "acc": 1.000000, "gap": 0.000000},
    {"d_noise": 0, "clusterer": "ward", "stab": 1.000000, "acc": 1.000000, "gap": 0.000000},
    {"d_noise": 0, "clusterer": "spectral", "stab": 1.000000, "acc": 1.000000, "gap": 0.000000},
    {"d_noise": 0, "clusterer": "fcm", "stab": 1.000000, "acc": 1.000000, "gap": 0.000000},
    {"d_noise": 50, "clusterer": "kmeans", "stab": 0.090475, "acc": 0.131895, "gap": -0.041420},
    {"d_noise": 50, "clusterer": "gmm", "stab": 0.518397, "acc": 0.538264, "gap": -0.019867},
    {"d_noise": 50, "clusterer": "ward", "stab": 0.065909, "acc": 0.108527, "gap": -0.042617},
    {"d_noise": 50, "clusterer": "spectral", "stab": 0.215720, "acc": 0.180357, "gap": 0.035363},
    {"d_noise": 50, "clusterer": "fcm", "stab": 0.185984, "acc": 0.229097, "gap": -0.043112},
    {"d_noise": 500, "clusterer": "kmeans", "stab": 0.003449, "acc": 0.003550, "gap": -0.000101},
    {"d_noise": 500, "clusterer": "gmm", "stab": 0.005084, "acc": 0.003465, "gap": 0.001619},
    {"d_noise": 500, "clusterer": "ward", "stab": 0.028775, "acc": 0.008697, "gap": 0.020078},
    {"d_noise": 500, "clusterer": "spectral", "stab": 0.080324, "acc": -0.001584, "gap": 0.081908},
    {"d_noise": 500, "clusterer": "fcm", "stab": 0.022044, "acc": 0.014308, "gap": 0.007736},
    {"d_noise": 2000, "clusterer": "kmeans", "stab": 0.003421, "acc": 0.000583, "gap": 0.002838},
    {"d_noise": 2000, "clusterer": "gmm", "stab": 0.003995, "acc": -0.000517, "gap": 0.004511},
    {"d_noise": 2000, "clusterer": "ward", "stab": 0.021942, "acc": 0.003048, "gap": 0.018894},
    {"d_noise": 2000, "clusterer": "spectral", "stab": 0.109097, "acc": 0.001473, "gap": 0.107624},
    {"d_noise": 2000, "clusterer": "fcm", "stab": 0.009651, "acc": 0.004032, "gap": 0.005619},
    {"d_noise": 5000, "clusterer": "kmeans", "stab": 0.000245, "acc": 0.000853, "gap": -0.000607},
    {"d_noise": 5000, "clusterer": "gmm", "stab": 0.005195, "acc": -0.001181, "gap": 0.006376},
    {"d_noise": 5000, "clusterer": "ward", "stab": 0.026216, "acc": -0.000385, "gap": 0.026601},
    {"d_noise": 5000, "clusterer": "spectral", "stab": 0.172939, "acc": 0.001728, "gap": 0.171212},
    {"d_noise": 5000, "clusterer": "fcm", "stab": 0.003637, "acc": 0.002038, "gap": 0.001599},
]

df = pd.DataFrame(data)
algos = ["fcm", "gmm", "kmeans", "spectral", "ward"]

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 11

def clean_spines(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#444444")
    ax.spines["bottom"].set_color("#444444")

# ---------------- FIGURE 2A: ARI & Subsample Stability ----------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 5.2), dpi=300)
for clus in algos:
    sub = df[df["clusterer"] == clus].sort_values("d_noise")
    ax1.plot(sub["d_noise"], sub["acc"], marker="o", label=clus.upper(),
             color=PALETTE.get(clus, "#000"), linewidth=2.0, markersize=6)
    ax2.plot(sub["d_noise"], sub["stab"], marker="o", label=clus.upper(),
             color=PALETTE.get(clus, "#000"), linewidth=2.0, markersize=6)

for ax, title, ylab in [
    (ax1, r"Clustering Accuracy (ARI vs. Ground Truth)", "Adjusted Rand Index (ARI)"),
    (ax2, r"Subsample Stability (Stratified 80% Resampling)", "Subsample Stability (ARI)"),
]:
    ax.set_title(title, fontsize=12.0, fontweight="bold", pad=10)
    ax.set_xlabel(r"Noise Dimensions ($D_{\text{noise}}$)", fontsize=11.0, fontweight="bold")
    ax.set_ylabel(ylab, fontsize=11.0, fontweight="bold")
    ax.set_xscale("symlog", linthresh=10)
    ax.set_ylim(-0.15, 1.05)
    clean_spines(ax)

ax2.legend(fontsize=10.0, loc="upper right", framealpha=0.92)
plt.tight_layout()

# ---------------- FIGURE 2B: Gap ----------------
fig_gap, ax_gap = plt.subplots(figsize=(7.5, 4.8), dpi=300)
for clus in algos:
    sub = df[df["clusterer"] == clus].sort_values("d_noise")
    ax_gap.plot(sub["d_noise"], sub["gap"], marker="o", label=clus.upper(),
                color=PALETTE.get(clus, "#000"), linewidth=2.0, markersize=6)

ax_gap.axhline(0, color="black", linestyle="--", linewidth=1.0)
ax_gap.set_title(r"Subsample Stability$-$Accuracy Gap ($\Delta = \text{Stability} - \text{ARI}$)", fontsize=11.5, fontweight="bold", pad=10)
ax_gap.set_xlabel(r"Noise Dimensions ($D_{\text{noise}}$)", fontsize=11.0, fontweight="bold")
ax_gap.set_ylabel(r"Gap Metric $\Delta$", fontsize=11.0, fontweight="bold")
ax_gap.set_xscale("symlog", linthresh=10)
ax_gap.set_ylim(-0.20, 0.30)
clean_spines(ax_gap)
ax_gap.legend(fontsize=10.0, loc="lower right", framealpha=0.92)
plt.tight_layout()

# Save destinations
dest_dirs = [
    Path("experiments/exp0_falsification/figures"),
    Path("paper/figures"),
    Path("springer_manuscript/figures"),
    Path("submission/springer_nature_package/figures"),
    Path("submission/overleaf_package/figures"),
    Path("submission/arxiv_package/figures"),
]

for d in dest_dirs:
    if d.exists():
        f1 = d / "fig02a_ari_stability.png"
        f2 = d / "fig02b_stability_accuracy_gap.png"
        # Also old names if in exp0
        fig.savefig(f1, dpi=300)
        fig_gap.savefig(f2, dpi=300)
        if "exp0_falsification" in str(d):
            fig.savefig(d / "fig1_ari_stability.png", dpi=300)
            fig_gap.savefig(d / "fig2_gap.png", dpi=300)
        print(f"Saved {f1} and {f2}")

plt.close(fig)
plt.close(fig_gap)
print("Fig 2 replot complete.")
