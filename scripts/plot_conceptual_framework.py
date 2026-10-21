"""
Generates Figure 0: Motivational Conceptual Illustration for Manuscript.

Visualizes:
(a) Ground-Truth Signal Subspace (d=2): 3 well-separated clusters with certified anchor cores.
(b) High-Dimensional Noise Drowning (D=2,000): Complete overlap in random noise projections,
    plus distance concentration inset (pairwise distance variance collapse).
(c) Bimodality-Gated Subspace Selection (BGSS): Bimodality spectrum separating signal from noise.
(d) Geometry-Calibrated Inductive Projection: Projecting unseen out-of-sample query instances.

Outputs:
    springer_manuscript/figures/fig0_conceptual_framework.png (300 DPI)
    paper/figures/fig0_conceptual_framework.png
    manuscript/figures/fig0_conceptual_framework.png
    experiments/figures/fig0_conceptual_framework.png
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from scipy.spatial.distance import pdist

ROOT_DIR = Path(__file__).resolve().parents[1]

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
})


def generate_conceptual_figure():
    fig, axes = plt.subplots(2, 2, figsize=(12, 9.2), dpi=300)
    rng = np.random.default_rng(42)

    # -------------------------------------------------------------------------
    # Panel (a): True Signal Subspace (d=2)
    # -------------------------------------------------------------------------
    ax_a = axes[0, 0]
    n_per = 60
    c1 = rng.normal(loc=[-2.5, -1.0], scale=0.55, size=(n_per, 2))
    c2 = rng.normal(loc=[2.5, -1.0], scale=0.55, size=(n_per, 2))
    c3 = rng.normal(loc=[0.0, 2.8], scale=0.55, size=(n_per, 2))

    colors = ["#1f77b4", "#2ca02c", "#ff7f0e"]
    clusters = [c1, c2, c3]
    labels = ["Cluster 1", "Cluster 2", "Cluster 3"]

    for i, (pts, col, lab) in enumerate(zip(clusters, colors, labels)):
        ax_a.scatter(pts[:, 0], pts[:, 1], c=col, s=36, alpha=0.7, edgecolors="none", label=lab)
        center = np.mean(pts, axis=0)
        dists = np.linalg.norm(pts - center, axis=1)
        core_idx = np.argsort(dists)[:8]
        ax_a.scatter(pts[core_idx, 0], pts[core_idx, 1], c=col, marker="*", s=130,
                     edgecolors="black", linewidths=0.9, zorder=5)

    ax_a.set_title("(a) Informative Signal Subspace ($d=2$)\nLatent clusters & certified invariant anchors (stars)", fontweight="bold", pad=8)
    ax_a.set_xlabel("Signal Dimension $X_1$")
    ax_a.set_ylabel("Signal Dimension $X_2$")
    ax_a.legend(loc="upper right", framealpha=0.9)
    ax_a.grid(True, linestyle="--", alpha=0.4)

    # -------------------------------------------------------------------------
    # Panel (b): Noise Drowning & Distance Concentration
    # -------------------------------------------------------------------------
    ax_b = axes[0, 1]
    noise1 = rng.normal(loc=0.0, scale=1.0, size=(n_per * 3,))
    noise2 = rng.normal(loc=0.0, scale=1.0, size=(n_per * 3,))

    for i, col in enumerate(colors):
        sub_n1 = noise1[i * n_per:(i + 1) * n_per]
        sub_n2 = noise2[i * n_per:(i + 1) * n_per]
        ax_b.scatter(sub_n1, sub_n2, c=col, s=36, alpha=0.55, edgecolors="none")

    ax_b.set_title("(b) Uninformative Distractor Space ($D=2{,}000$)\nStructure collapses into noise attractor", fontweight="bold", pad=8)
    ax_b.set_xlabel("Nuisance Dimension $X_{742}$")
    ax_b.set_ylabel("Nuisance Dimension $X_{1895}$")
    ax_b.set_ylim(-3.5, 3.8)
    ax_b.grid(True, linestyle="--", alpha=0.4)

    # Inset: Distance Concentration Curve
    ax_inset = ax_b.inset_axes([0.52, 0.44, 0.44, 0.38])
    d_vals = [2, 10, 50, 200, 1000, 5000]
    rel_spread = []
    for D in d_vals:
        pts_high = rng.normal(size=(100, D))
        pw = pdist(pts_high)
        spread = (np.max(pw) - np.min(pw)) / np.min(pw)
        rel_spread.append(spread)

    ax_inset.plot(d_vals, rel_spread, "d-", color="#d62728", linewidth=2.0, markersize=5.5)
    ax_inset.set_xscale("log")
    ax_inset.set_title("Distance Concentration\n$(d_{\\max}-d_{\\min})/d_{\\min} \\to 0$", fontsize=8.0, pad=3)
    ax_inset.set_xlabel("Dimension $D$", fontsize=7.5)
    ax_inset.set_ylabel("Relative Spread", fontsize=7.5)
    ax_inset.tick_params(labelsize=7.0)
    ax_inset.grid(True, linestyle=":", alpha=0.5)

    # -------------------------------------------------------------------------
    # Panel (c): Bimodality-Gated Subspace Selection (BGSS)
    # -------------------------------------------------------------------------
    ax_c = axes[1, 0]
    total_dims = 100
    bimodality = rng.normal(loc=0.18, scale=0.04, size=total_dims)
    bimodality[0] = 0.88
    bimodality[1] = 0.82
    bimodality[5] = 0.32

    dim_indices = np.arange(total_dims)
    bar_cols = ["#d62728" if i in [0, 1] else "#aec7e8" for i in dim_indices]

    ax_c.bar(dim_indices, bimodality, color=bar_cols, width=0.8, edgecolor="none")
    threshold = 0.28
    ax_c.axhline(threshold, color="#2ca02c", linestyle="--", linewidth=2.0,
                 label=r"BGSS Candidate Pool Cutoff ($\rho_{\text{pool}}$)")

    ax_c.annotate("True Signal $X_1$\n(Recovered)", xy=(0, 0.88), xytext=(8, 0.80),
                 arrowprops=dict(facecolor="black", arrowstyle="->", lw=1.2),
                 fontsize=9.5, fontweight="bold")
    ax_c.annotate("True Signal $X_2$\n(Recovered)", xy=(1, 0.82), xytext=(12, 0.63),
                 arrowprops=dict(facecolor="black", arrowstyle="->", lw=1.2),
                 fontsize=9.5, fontweight="bold")
    ax_c.annotate("Uninformative Noise Ocean\n(Penalized & Gated Out)", xy=(50, 0.20), xytext=(40, 0.40),
                 arrowprops=dict(facecolor="gray", arrowstyle="->", lw=1.2),
                 fontsize=9.0)

    ax_c.set_title("(c) BGSS Feature Saliency Spectrum\nBimodality coefficient separates signal from distractor noise", fontweight="bold", pad=8)
    ax_c.set_xlabel("Feature Index $d \\in \\{1, \\dots, D\\}$")
    ax_c.set_ylabel(r"Bimodality Saliency Score $\hat{b}_d$")
    ax_c.set_ylim(0, 1.0)
    ax_c.legend(loc="upper right", framealpha=0.9)
    ax_c.grid(True, linestyle="--", alpha=0.4)

    # -------------------------------------------------------------------------
    # Panel (d): Geometry-Calibrated Inductive Projection
    # -------------------------------------------------------------------------
    ax_d = axes[1, 1]
    centroids = np.array([[-2.5, -1.0], [2.5, -1.0], [0.0, 2.8]])
    for i, (cnt, col, lab) in enumerate(zip(centroids, colors, labels)):
        ellipse = patches.Ellipse(cnt, width=1.8, height=1.4, angle=0,
                                  edgecolor=col, facecolor=col, alpha=0.15, linestyle="--", linewidth=1.5)
        ax_d.add_patch(ellipse)
        ax_d.scatter(cnt[0], cnt[1], c=col, marker="P", s=200, edgecolors="black",
                     linewidths=1.2, label=f"Anchor Centroid $\\mu_{i+1}$", zorder=6)

    x_query = np.array([1.6, -0.4])
    ax_d.scatter(x_query[0], x_query[1], c="red", marker="o", s=130, edgecolors="black",
                 linewidths=1.5, label=r"Unseen Query $\mathbf{x}_{\text{new}}$", zorder=7)

    for i, cnt in enumerate(centroids):
        dist = np.linalg.norm(x_query - cnt)
        lw = 2.4 if i == 1 else 1.0
        ls = "-" if i == 1 else ":"
        alp = 0.9 if i == 1 else 0.4
        ax_d.plot([x_query[0], cnt[0]], [x_query[1], cnt[1]], color="black" if i == 1 else "gray",
                  linestyle=ls, linewidth=lw, alpha=alp)

    ax_d.annotate("Inductive Assignment:\n"
                  r"$\arg\min_c \|\mathbf{x}_{\text{new}} - \boldsymbol{\mu}_c\|_{\text{BGSS}}$" "\n"
                  r"$P(C_2 \mid \mathbf{x}) = 0.89$",
                  xy=x_query, xytext=(0.3, 0.7),
                  arrowprops=dict(facecolor="red", arrowstyle="->", lw=1.2),
                  fontsize=9.0, fontweight="bold",
                  bbox=dict(boxstyle="round,pad=0.4", fc="#fff2f2", ec="red", lw=1.0))

    ax_d.set_title("(d) Closed-Form Inductive Projection\nSubspace distance to anchor centroids assigns query $\\mathbf{x}_{\\text{new}}$", fontweight="bold", pad=8)
    ax_d.set_xlabel("Projected Feature $X_1$")
    ax_d.set_ylabel("Projected Feature $X_2$")
    ax_d.set_xlim(-4, 4)
    ax_d.set_ylim(-2.5, 4.0)
    ax_d.legend(loc="upper left", framealpha=0.9, fontsize=9)
    ax_d.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()

    out_dirs = [
        ROOT_DIR / "springer_manuscript" / "figures",
        ROOT_DIR / "paper" / "figures",
        ROOT_DIR / "manuscript" / "figures",
        ROOT_DIR / "experiments" / "figures",
    ]
    for od in out_dirs:
        od.mkdir(parents=True, exist_ok=True)
        out_p = od / "fig0_conceptual_framework.png"
        plt.savefig(out_p, dpi=300, bbox_inches="tight")
        print(f"[SUCCESS] Saved figure to: {out_p}")

    plt.close()


if __name__ == "__main__":
    generate_conceptual_figure()
