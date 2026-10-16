"""
Plotting script for Experiment 0.
Reproduces all 8 publication figures directly from CSV data:
- fig1_ari_stability.png
- fig2_gap.png
- fig3_within_between.png
- fig4_noisetype_heatmap.png
- fig5_scaled_ari_stability.png
- fig6_scaled_gap.png
- fig7_regime_comparison.png
- fig8_fcm_phase_transition.png
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Add project root to sys.path
root_dir = Path(__file__).resolve().parents[3]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from icc.viz_style import set_academic_style, clean_spines

# Set academic style at module level
set_academic_style()

# Colors matching the original study
PALETTE = {
    "fcm": "#9467bd",       # purple
    "gmm": "#ff7f0e",       # orange
    "kmeans": "#1f77b4",    # blue
    "spectral": "#d62728",  # red
    "ward": "#2ca02c",      # green
    "ALL_POOLED": "#333333" # dark grey
}


def plot_fig1_and_fig2(agg_csv, out_dir):
    df = pd.read_csv(agg_csv)
    df_algo = df[df["scope"] == "per_algorithm"].copy()
    algos = ["fcm", "gmm", "kmeans", "spectral", "ward"]

    # ---------------- FIGURE 1: ARI & Stability ----------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.4, 5.88), dpi=300)
    for clus in algos:
        sub = df_algo[df_algo["clusterer"] == clus].sort_values("d_noise")
        ax1.plot(sub["d_noise"], sub["mean_ari"], marker="o", label=clus.upper(),
                 color=PALETTE.get(clus, "#000"), linewidth=2.2, markersize=7)
        ax2.plot(sub["d_noise"], sub["stability"], marker="o", label=clus.upper(),
                 color=PALETTE.get(clus, "#000"), linewidth=2.2, markersize=7)

    for ax, title, ylab in [(ax1, r"(a) Clustering Accuracy (ARI vs. Ground Truth)", "Adjusted Rand Index (ARI)"),
                             (ax2, r"(b) Ensemble Stability (Pairwise ARI Across Seeds)", "Consensus Stability")]:
        ax.set_title(title, fontsize=12.5, fontweight="bold")
        ax.set_xlabel(r"Noise Dimensions ($D_{\text{noise}}$)", fontsize=11.5, fontweight="bold")
        if ylab:
            ax.set_ylabel(ylab, fontsize=11.5, fontweight="bold")
        ax.set_xscale("symlog", linthresh=10)
        ax.set_ylim(-0.05, 1.05)
        clean_spines(ax)

    ax2.legend(fontsize=10.5, loc="lower left", framealpha=0.92)
    plt.tight_layout()
    fig1_path = out_dir / "fig1_ari_stability.png"
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"  [Saved] {fig1_path}")

    # ---------------- FIGURE 2: Gap ----------------
    fig, ax = plt.subplots(figsize=(8.0, 5.0), dpi=300)
    for clus in algos:
        sub = df_algo[df_algo["clusterer"] == clus].sort_values("d_noise")
        ax.plot(sub["d_noise"], sub["gap"], marker="o", label=clus.upper(),
                 color=PALETTE.get(clus, "#000"), linewidth=2.2, markersize=7)

    ax.axhline(0, color="black", linestyle="--", linewidth=1.0)
    ax.set_title("Stability$-$Accuracy Gap ($\\Delta = \\text{Stability} - \\text{ARI}$)\n(Positive $\\Delta$ indicates Hallucinated Stability Attractor)", fontsize=12.0, fontweight="bold")
    ax.set_xlabel(r"Noise Dimensions ($D_{\text{noise}}$)", fontsize=11.5, fontweight="bold")
    ax.set_ylabel(r"Gap Metric $\Delta$", fontsize=11.5, fontweight="bold")
    ax.set_xscale("symlog", linthresh=10)
    clean_spines(ax)
    ax.legend(fontsize=10.5, loc="upper left", framealpha=0.92)
    plt.tight_layout()
    fig2_path = out_dir / "fig2_gap.png"
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"  [Saved] {fig2_path}")


def plot_fig1_supp_nmi_stability(agg_csv, out_dir):
    df = pd.read_csv(agg_csv)
    if "mean_nmi" not in df.columns:
        print("  [Notice] mean_nmi not found in exp0_agg.csv, skipping fig1_supp_nmi_stability.")
        return
    df_algo = df[df["scope"] == "per_algorithm"].copy()
    algos = ["fcm", "gmm", "kmeans", "spectral", "ward"]

    # ---------------- SUPPLEMENTARY FIGURE 1: NMI & Stability ----------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.4, 5.88), dpi=300)
    for clus in algos:
        sub = df_algo[df_algo["clusterer"] == clus].sort_values("d_noise")
        ax1.plot(sub["d_noise"], sub["mean_nmi"], marker="o", label=clus,
                 color=PALETTE.get(clus, "#000"), linewidth=1.8, markersize=6)
        ax2.plot(sub["d_noise"], sub["stability"], marker="o", label=clus,
                 color=PALETTE.get(clus, "#000"), linewidth=1.8, markersize=6)

    for ax, title, ylab in [(ax1, "Clustering accuracy (NMI vs ground truth)", "NMI"),
                             (ax2, "Ensemble stability (pairwise ARI across seeds)", "")]:
        ax.set_title(title, fontsize=12)
        ax.set_xlabel("Noise dimensions (D_noise)", fontsize=11)
        if ylab:
            ax.set_ylabel(ylab, fontsize=11)
        ax.set_xscale("symlog", linthresh=10)
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, alpha=0.3)

    ax2.legend(fontsize=9, loc="lower left")
    plt.tight_layout()
    fig1_supp_path = out_dir / "fig1_supp_nmi_stability.png"
    plt.savefig(fig1_supp_path, dpi=300)
    plt.close()
    print(f"  [Saved] {fig1_supp_path}")


def plot_fig3_within_between(agg_csv, out_dir):
    df = pd.read_csv(agg_csv)
    sub = df[df["clusterer"] == "ALL_POOLED"].sort_values("d_noise")

    fig, ax = plt.subplots(figsize=(9.8, 6.3), dpi=300)
    ax.plot(sub["d_noise"], sub["mu_within"], marker="o", color="#2ca02c",
            label="μ_within (same true cluster)", linewidth=2.0, markersize=7)
    ax.plot(sub["d_noise"], sub["mu_between"], marker="o", color="#d62728",
            label="μ_between (different true cluster)", linewidth=2.0, markersize=7)

    ax.set_title(r"Pooled Multi-Clusterer Consensus ($N=300, K=3$)" + "\n" + r"(Between-Cluster Pairs Converging Toward $S_{ij} \to 1.0$ Under Heavy Noise)", fontsize=11.5, fontweight="bold")
    ax.set_xlabel(r"Noise Dimensions ($D_{\text{noise}}$)", fontsize=10.5)
    ax.set_ylabel(r"Mean Pairwise Consensus $S_{ij}$", fontsize=10.5)
    ax.set_xscale("symlog", linthresh=10)
    ax.set_ylim(-0.05, 1.05)
    clean_spines(ax)
    ax.legend(fontsize=9.5, loc="center right", framealpha=0.92)
    plt.tight_layout()
    fig3_path = out_dir / "fig3_within_between.png"
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"  [Saved] {fig3_path}")


def plot_fig4_heatmap(noisetypes_csv, out_dir):
    df = pd.read_csv(noisetypes_csv)
    pivot = df.pivot(index="clusterer", columns="noise_kind", values="gap")
    algos = ["fcm", "gmm", "kmeans", "spectral", "ward"]
    kinds = ["gaussian", "student_t", "correlated", "scaled", "sparse"]
    kinds_labels = ["Gaussian", "Student-$t$", "Correlated", "Scaled", "Sparse"]
    pivot = pivot.reindex(index=algos, columns=kinds)

    fig, ax = plt.subplots(figsize=(8.0, 4.8), dpi=300)
    cax = ax.imshow(pivot.values, cmap="RdBu_r", vmin=-0.5, vmax=1.0, aspect="auto")

    ax.set_xticks(range(len(kinds)))
    ax.set_yticks(range(len(algos)))
    ax.set_xticklabels(kinds_labels, fontsize=11, fontweight="bold")
    ax.set_yticklabels([a.upper() for a in algos], fontsize=11, fontweight="bold")
    ax.set_title(r"Stability$-$ARI Gap Across Diverse Noise Regimes ($D_{\text{noise}}=1{,}000$)", fontsize=12.5, fontweight="bold", pad=10)

    # Annotate numbers
    for i in range(len(algos)):
        for j in range(len(kinds)):
            val = pivot.values[i, j]
            color = "white" if abs(val) > 0.45 else "black"
            ax.text(j, i, f"{val:+.2f}", ha="center", va="center", color=color, fontsize=11, fontweight="bold")

    cbar = fig.colorbar(cax, ax=ax, pad=0.03)
    cbar.set_label(r"Stability$-$Accuracy Gap $\Delta$", fontsize=11, fontweight="bold")
    cbar.ax.tick_params(labelsize=10)
    plt.tight_layout()
    fig4_path = out_dir / "fig4_noisetype_heatmap.png"
    plt.savefig(fig4_path, dpi=300)
    plt.close()
    print(f"  [Saved] {fig4_path}")


def plot_fig5_and_fig6_scaled(scaled_agg_csv, out_dir):
    df = pd.read_csv(scaled_agg_csv)
    df_algo = df[df["scope"] == "per_algorithm"].copy()
    algos = ["fcm", "gmm", "kmeans", "spectral", "ward"]

    # ---------------- FIGURE 5: Scaled ARI & Stability ----------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.2, 6.04), dpi=300)
    for clus in algos:
        sub = df_algo[df_algo["clusterer"] == clus].sort_values("d_noise")
        ax1.plot(sub["d_noise"], sub["mean_ari"], marker="o", label=clus,
                 color=PALETTE.get(clus, "#000"), linewidth=1.8, markersize=6)
        ax2.plot(sub["d_noise"], sub["stability"], marker="o", label=clus,
                 color=PALETTE.get(clus, "#000"), linewidth=1.8, markersize=6)

    fig.suptitle("Genomics-scale regime: N=72 (47/25, ALLAML-like), k=2", fontsize=13, y=0.98)
    for ax, title, ylab in [(ax1, "Clustering accuracy (ARI)", "ARI"),
                             (ax2, "Ensemble stability", "")]:
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("Noise dimensions (D_noise)", fontsize=11)
        if ylab:
            ax.set_ylabel(ylab, fontsize=11)
        ax.set_xscale("symlog", linthresh=10)
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, alpha=0.3)

    ax2.legend(fontsize=10, loc="upper right")
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    fig5_path = out_dir / "fig5_scaled_ari_stability.png"
    plt.savefig(fig5_path, dpi=300)
    plt.close()
    print(f"  [Saved] {fig5_path}")

    # ---------------- FIGURE 6: Scaled Gap ----------------
    fig, ax = plt.subplots(figsize=(9.8, 6.3), dpi=300)
    for clus in algos:
        sub = df_algo[df_algo["clusterer"] == clus].sort_values("d_noise")
        ax.plot(sub["d_noise"], sub["gap"], marker="o", label=clus,
                 color=PALETTE.get(clus, "#000"), linewidth=1.8, markersize=6)

    ax.axhline(0, color="black", linestyle="--", linewidth=1.0)
    ax.set_title("Stability–Accuracy Gap — N=72, D/N up to ~278\n(ALLAML-scale)", fontsize=12)
    ax.set_xlabel("Noise dimensions (D_noise)", fontsize=11)
    ax.set_ylabel("Gap = Stability − ARI", fontsize=11)
    ax.set_xscale("symlog", linthresh=10)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10, loc="upper left")
    plt.tight_layout()
    fig6_path = out_dir / "fig6_scaled_gap.png"
    plt.savefig(fig6_path, dpi=300)
    plt.close()
    print(f"  [Saved] {fig6_path}")


def plot_fig7_regime_comparison(agg_csv, scaled_agg_csv, out_dir):
    df_bal = pd.read_csv(agg_csv)
    df_scale = pd.read_csv(scaled_agg_csv)
    df_bal = df_bal[df_bal["scope"] == "per_algorithm"]
    df_scale = df_scale[df_scale["scope"] == "per_algorithm"]

    fig, axes = plt.subplots(1, 3, figsize=(18.68, 6.1), sharey=True, dpi=300)
    fig.suptitle("The hallucinated-stability signature is regime-dependent, not just algorithm-dependent", fontsize=13, y=0.98)

    for ax, clus in zip(axes, ["fcm", "spectral", "ward"]):
        sub_b = df_bal[df_bal["clusterer"] == clus].sort_values("d_noise")
        sub_s = df_scale[df_scale["clusterer"] == clus].sort_values("d_noise")
        ax.plot(sub_b["d_noise"], sub_b["gap"], marker="o", color="#1f77b4",
                label="N=300 (balanced)", linewidth=1.8, markersize=6)
        ax.plot(sub_s["d_noise"], sub_s["gap"], marker="s", color="#d62728",
                label="N=72 (47/25 imbalanced)", linewidth=1.8, markersize=6)
        ax.axhline(0, color="black", linestyle="--", linewidth=1.0)
        ax.set_title(clus, fontsize=12)
        ax.set_xlabel("Noise dimensions", fontsize=11)
        ax.set_xscale("symlog", linthresh=10)
        ax.grid(True, alpha=0.3)

    axes[0].set_ylabel("Gap = Stability − ARI", fontsize=11)
    axes[0].legend(fontsize=10, loc="upper right")
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    fig7_path = out_dir / "fig7_regime_comparison.png"
    plt.savefig(fig7_path, dpi=300)
    plt.close()
    print(f"  [Saved] {fig7_path}")


def plot_fig8_fcm_phase_transition(fcm_curve_csv, out_dir):
    df = pd.read_csv(fcm_curve_csv)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.9, 10.5), sharex=True, dpi=300)

    # Top panel: ARI vs Dominant Share
    ax1.plot(df["d_noise"], df["mean_ari"], marker="o", color="#9467bd",
             label="Mean ARI (accuracy)", linewidth=2.0, markersize=7)
    ax1.plot(df["d_noise"], df["dominant_share"], marker="s", color="#2ca02c",
             label="Dominant-partition share\n(fraction of 30 seeds landing\non the single most common partition)",
             linewidth=2.0, markersize=7)

    # Shaded regimes
    ax1.axvspan(150, 800, color="red", alpha=0.1)
    ax1.text(350, 0.65, "PURE\nHALLUCINATION\n(100% of seeds\nconverge to same\nwrong answer)",
             color="darkred", ha="center", fontsize=9, fontweight="bold")

    ax1.axvspan(1000, 2250, color="orange", alpha=0.08)
    ax1.text(1500, 0.18, "PARTIAL\n(breaking down)", color="#d95f02", ha="center", fontsize=9)

    ax1.axvspan(2500, 5000, color="blue", alpha=0.08)
    ax1.text(3500, 0.55, "COLLAPSED\n(conventional\ninstability)", color="#386cb0", ha="center", fontsize=9)

    ax1.set_title(r"Fuzzy C-Means Phase Transition: Accuracy vs. Spurious Convergence ($N=300, K=3$)", fontsize=11.5, fontweight="bold")
    ax1.set_ylabel("Metric Value", fontsize=10.5)
    ax1.set_ylim(-0.02, 1.05)
    clean_spines(ax1)
    ax1.legend(loc="center right", fontsize=9, framealpha=0.92)

    # Bottom panel: Distinct partitions
    ax2.plot(df["d_noise"], df["n_distinct"], marker="d", color="#d62728", linewidth=2.0, markersize=7)
    ax2.axvline(150, color="grey", linestyle=":", linewidth=1.0)
    ax2.axvline(200, color="grey", linestyle=":", linewidth=1.0)
    ax2.annotate("Onset window:\n$D_{\\text{noise}} \\in [150, 200]$", xy=(200, 5), xytext=(400, 12),
                 arrowprops=dict(arrowstyle="->", color="black"), fontsize=9, fontweight="bold")

    ax2.set_xlabel(r"Noise Dimensions ($D_{\text{noise}}$)", fontsize=10.5)
    ax2.set_ylabel("Distinct Partitions\n(out of 30 seeds)", fontsize=10.5)
    ax2.set_xscale("log")
    clean_spines(ax2)

    plt.tight_layout()
    fig8_path = out_dir / "fig8_fcm_phase_transition.png"
    plt.savefig(fig8_path, dpi=300)
    plt.close()
    print(f"  [Saved] {fig8_path}")


def generate_all_figures():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    fig_dir = base_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    print("Generating all 8 Experiment 0 publication figures (and supplementary NMI)...")
    plot_fig1_and_fig2(data_dir / "exp0_agg.csv", fig_dir)
    plot_fig1_supp_nmi_stability(data_dir / "exp0_agg.csv", fig_dir)
    plot_fig3_within_between(data_dir / "exp0_agg.csv", fig_dir)
    plot_fig4_heatmap(data_dir / "exp0_noisetypes.csv", fig_dir)
    plot_fig5_and_fig6_scaled(data_dir / "exp0_scaled_agg.csv", fig_dir)
    plot_fig7_regime_comparison(data_dir / "exp0_agg.csv", data_dir / "exp0_scaled_agg.csv", fig_dir)
    plot_fig8_fcm_phase_transition(data_dir / "exp0_fcm_full_curve.csv", fig_dir)
    print("\nAll figures successfully generated and saved to:", fig_dir)


if __name__ == "__main__":
    generate_all_figures()
