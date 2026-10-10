"""
Plotting script for Experiment 2 Suite: Component-Wise Ablation.
Generates:
- fig11_ablation_curves.png (ARI across noise dimensions for all 6 variants)
- fig12_ablation_waterfall.png (Component contribution decomposition)
- fig13_nmi_ablation.png (NMI comparison)
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Add project root to sys.path
root_dir = Path(__file__).resolve().parents[3]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.icc.viz_style import set_academic_style, clean_spines

set_academic_style()

VARIANT_COLORS = {
    "V0_Standard_Consensus": "#7f7f7f",       # grey
    "V1_Subspaces_Only": "#1f77b4",           # blue
    "V2_Anchors_Only": "#9467bd",             # purple
    "V3_Subspaces_Plus_Anchors": "#ff7f0e",   # orange
    "V4_Subspaces_Plus_Calibration": "#e377c2", # pink
    "V5_Full_ICC_v1": "#2ca02c"               # bold green
}

VARIANT_LABELS = {
    "V0_Standard_Consensus": "V0: Standard Consensus (Baseline)",
    "V1_Subspaces_Only": "V1: Subspace Gating Only",
    "V2_Anchors_Only": "V2: Core Anchors Only",
    "V3_Subspaces_Plus_Anchors": "V3: Subspaces + Core Anchors",
    "V4_Subspaces_Plus_Calibration": "V4: Subspaces + Noise Calibration",
    "V5_Full_ICC_v1": "V5: Full ICC-v1 (Gating + Calib + Anchors) [Ours]"
}


def plot_exp2_figures():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    fig_dir = base_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    csv_path = data_dir / "exp2_ablation_results.csv"
    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    set_academic_style()

    # -------------------------------------------------------------------------
    # 1. Figure 11: ARI Recovery Curves across 6 Variants
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10.0, 5.2), dpi=300)

    for v_name, label in VARIANT_LABELS.items():
        sub = df[df["variant"] == v_name].sort_values("d_noise")
        lw = 2.6 if v_name == "V5_Full_ICC_v1" else (2.0 if v_name == "V0_Standard_Consensus" else 1.8)
        ls = "-" if "Full" in v_name or "Baseline" in label else "--"
        marker = "d" if "Full" in v_name else ("s" if "Baseline" in label else "o")
        ax.plot(sub["d_noise"], sub["mean_ari"], marker=marker, label=label,
                color=VARIANT_COLORS.get(v_name, "#000"), linewidth=lw, linestyle=ls, markersize=7)

    ax.set_title("Figure 11: Component-Wise Ablation: Dissecting Invariant Core Consensus (ICC)", fontsize=13.0, fontweight="bold")
    ax.set_xlabel(r"Nuisance Distractor Dimensions ($D_{\text{noise}}$)", fontsize=12.0, fontweight="bold")
    ax.set_ylabel("Clustering Recovery (ARI)", fontsize=12.0, fontweight="bold")
    ax.tick_params(labelsize=11.0)
    ax.set_xscale("symlog", linthresh=10)
    ax.set_ylim(-0.05, 0.85)
    clean_spines(ax)
    ax.legend(loc="lower left", fontsize=10.5, framealpha=0.92, facecolor="white", edgecolor="#cccccc")

    plt.tight_layout()
    fig11_path = fig_dir / "fig11_ablation_curves.png"
    plt.savefig(fig11_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  [Saved] {fig11_path}")

    # -------------------------------------------------------------------------
    # 2. Figure 12: Stepwise Component Contribution (Dual Panel: D_noise=0 and D_noise=50)
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.8), dpi=300)
    v_keys = list(VARIANT_LABELS.keys())
    labels = [k.split("_")[0] for k in v_keys]
    colors = [VARIANT_COLORS[k] for k in v_keys]
    hatches = ["//", "", "xx", "xx", "", "xx"]

    # Panel (a): D_noise = 0
    sub0 = df[df["d_noise"] == 0].set_index("variant")
    aris0 = [sub0.loc[k]["mean_ari"] for k in v_keys]
    b1 = ax1.bar(labels, aris0, color=colors, edgecolor="black", linewidth=0.8, alpha=0.88, hatch=hatches, width=0.55)
    ax1.set_title(r"(a) Zero Noise Baseline ($D_{\text{noise}}=0$)", fontsize=13.0, fontweight="bold")
    ax1.set_ylabel("Adjusted Rand Index (ARI)", fontsize=12.0, fontweight="bold")
    ax1.tick_params(axis="x", labelsize=11.0)
    ax1.tick_params(axis="y", labelsize=11.0)
    ax1.set_ylim(0, 0.96)
    clean_spines(ax1)

    for rect in b1:
        h = rect.get_height()
        ax1.annotate(f"{h:.3f}", xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points",
                     ha="center", va="bottom", fontsize=10.5, fontweight="bold")

    ax1.annotate("Anchor Boost: +34.0%\n(V2, V3, V5 vs V0)",
                 xy=(2, 0.75), xytext=(0.7, 0.82),
                 arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.3),
                 fontsize=10.0, fontweight="bold", color="#2ca02c",
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="#f0fff0", edgecolor="#2ca02c", alpha=0.9))

    # Panel (b): D_noise = 50
    sub50 = df[df["d_noise"] == 50].set_index("variant")
    aris50 = [sub50.loc[k]["mean_ari"] for k in v_keys]
    b2 = ax2.bar(labels, aris50, color=colors, edgecolor="black", linewidth=0.8, alpha=0.88, hatch=hatches, width=0.55)
    ax2.set_title(r"(b) Intermediate Distractor Regime ($D_{\text{noise}}=50$)", fontsize=13.0, fontweight="bold")
    ax2.set_ylabel("Adjusted Rand Index (ARI)", fontsize=12.0, fontweight="bold")
    ax2.tick_params(axis="x", labelsize=11.0)
    ax2.tick_params(axis="y", labelsize=11.0)
    ax2.set_ylim(0, 0.48)
    clean_spines(ax2)
    ax2.grid(True, linestyle=":", alpha=0.5, axis="y")

    for rect in b2:
        h = rect.get_height()
        ax2.annotate(f"{h:.3f}", xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points",
                     ha="center", va="bottom", fontsize=10.5, fontweight="bold")

    plt.suptitle("Figure 12: Stepwise Component Impact Under Low and Moderate Distractor Dimensions",
                 fontweight="bold", fontsize=14.0, y=0.995)
    plt.tight_layout()
    fig12_path = fig_dir / "fig12_ablation_waterfall.png"
    plt.savefig(fig12_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  [Saved] {fig12_path}")

    # -------------------------------------------------------------------------
    # 3. Figure 13: NMI Recovery Curves
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10.0, 5.2), dpi=300)
    for v_name, label in VARIANT_LABELS.items():
        sub = df[df["variant"] == v_name].sort_values("d_noise")
        lw = 2.4 if v_name == "V5_Full_ICC_v1" else (1.8 if v_name == "V0_Standard_Consensus" else 1.5)
        ls = "-" if "Full" in v_name or "Baseline" in label else "--"
        marker = "d" if "Full" in v_name else ("s" if "Baseline" in label else "o")
        ax.plot(sub["d_noise"], sub["mean_nmi"], marker=marker, label=label,
                color=VARIANT_COLORS.get(v_name, "#000"), linewidth=lw, linestyle=ls, markersize=6)

    ax.set_title("Figure 13: Normalized Mutual Information (NMI) Across Ablation Variants", fontweight="bold")
    ax.set_xlabel(r"Nuisance Distractor Dimensions ($D_{\text{noise}}$)", fontweight="bold")
    ax.set_ylabel("Normalized Mutual Information (NMI)", fontweight="bold")
    ax.set_xscale("symlog", linthresh=10)
    ax.set_ylim(-0.05, 0.90)
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.legend(loc="lower left", framealpha=0.92, facecolor="white", edgecolor="#cccccc")

    plt.tight_layout()
    fig13_path = fig_dir / "fig13_nmi_ablation.png"
    plt.savefig(fig13_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  [Saved] {fig13_path}")

    # -------------------------------------------------------------------------
    # 4. Supplementary Figure 13: AMI Recovery Curves
    # -------------------------------------------------------------------------
    if "mean_ami" in df.columns:
        fig, ax = plt.subplots(figsize=(10.0, 5.2), dpi=300)
        for v_name, label in VARIANT_LABELS.items():
            sub = df[df["variant"] == v_name].sort_values("d_noise")
            lw = 2.4 if v_name == "V5_Full_ICC_v1" else (1.8 if v_name == "V0_Standard_Consensus" else 1.5)
            ls = "-" if "Full" in v_name or "Baseline" in label else "--"
            marker = "d" if "Full" in v_name else ("s" if "Baseline" in label else "o")
            ax.plot(sub["d_noise"], sub["mean_ami"], marker=marker, label=label,
                    color=VARIANT_COLORS.get(v_name, "#000"), linewidth=lw, linestyle=ls, markersize=6)

        ax.set_title("Supplementary Figure 13: Adjusted Mutual Information (AMI) Across Ablation Variants", fontweight="bold")
        ax.set_xlabel(r"Nuisance Distractor Dimensions ($D_{\text{noise}}$)", fontweight="bold")
        ax.set_ylabel("Adjusted Mutual Information (AMI)", fontweight="bold")
        ax.set_xscale("symlog", linthresh=10)
        ax.set_ylim(-0.05, 0.90)
        ax.grid(True, linestyle=":", alpha=0.5)
        ax.legend(loc="lower left", framealpha=0.92, facecolor="white", edgecolor="#cccccc")

        plt.tight_layout()
        fig13_supp_path = fig_dir / "fig13_supp_ami_ablation.png"
        plt.savefig(fig13_supp_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"  [Saved] {fig13_supp_path}")


if __name__ == "__main__":
    plot_exp2_figures()
