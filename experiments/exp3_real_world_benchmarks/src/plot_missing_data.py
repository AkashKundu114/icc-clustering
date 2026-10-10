"""
Plotting module for Experiment 3.5: Missing Data Robustness & Imputation Resilience.
Generates 300 DPI publication plots adhering to IEEE TKDE visual standards.
"""

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Add project root to sys.path
root_dir = Path(__file__).resolve().parents[3]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.icc.viz_style import set_academic_style, clean_spines

set_academic_style()

EXP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = EXP_DIR / "data"
FIGURES_DIR = EXP_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

METHOD_PALETTE = {
    "K-Means": ("#7f7f7f", ":", "o"),
    "Standard_Consensus": ("#1f77b4", "--", "p"),
    "Li_et_al_2019": ("#ff7f0e", "-.", "h"),
    "ICC_v1": ("#2ca02c", "-", "D"),
    "ICC_v2": ("#d62728", "-", "*"),
}


def plot_missing_data_curves():
    csv_file = DATA_DIR / "exp3_5_missing_data_results.csv"
    if not csv_file.exists():
        print(f"[!] {csv_file} not found.")
        return

    df = pd.read_csv(csv_file)
    datasets = ["colon", "leukemia", "srbct"]
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), dpi=300)

    for idx, dname in enumerate(datasets):
        ax = axes[idx]
        df_d = df[(df["dataset"] == dname) & (df["strategy"] == "mean")]
        if df_d.empty:
            df_d = df[df["dataset"] == dname]

        rho_vals = sorted(df_d["rho"].unique())

        for mname, (color, style, marker) in METHOD_PALETTE.items():
            df_m = df_d[df_d["method"] == mname]
            if df_m.empty:
                continue

            summary = df_m.groupby("rho")["ari"].agg(["mean", "std"]).reindex(rho_vals)
            means = summary["mean"].values
            stds = summary["std"].fillna(0).values

            is_icc2 = (mname == "ICC_v2")
            lw = 3.0 if is_icc2 else 1.8
            ms = 8 if is_icc2 else 5
            zorder = 5 if is_icc2 else 2

            ax.plot(
                rho_vals,
                means,
                linestyle=style,
                marker=marker,
                color=color,
                label=mname,
                linewidth=lw,
                markersize=ms,
                zorder=zorder,
            )
            ax.fill_between(rho_vals, means - stds, means + stds, color=color, alpha=0.12 if is_icc2 else 0.05)

        ax.set_xlabel(r"Missingness Fraction ($\rho_{\text{MCAR}}$)", fontsize=12.0, fontweight="bold")
        ax.set_ylabel("Mean ARI on Imputed Data", fontsize=12.0, fontweight="bold")
        ax.tick_params(labelsize=11.0)
        ax.set_title(f"({chr(97 + idx)}) {dname.upper()} Cohort", fontsize=13.0, fontweight="bold")
        ax.set_ylim(-0.05, 1.0)
        clean_spines(ax)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=5, fontsize=11.0, frameon=True)
    fig.tight_layout()

    out_file = FIGURES_DIR / "fig25a_missing_data_degradation.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved {out_file}")


def plot_imputation_strategy_heatmap():
    csv_file = DATA_DIR / "exp3_5_missing_data_results.csv"
    if not csv_file.exists():
        return

    df = pd.read_csv(csv_file)
    df_icc2 = df[df["method"] == "ICC_v2"]
    if df_icc2.empty:
        return

    pivot = df_icc2.groupby(["strategy", "rho"])["ari"].mean().unstack()
    strategies = list(pivot.index)
    rhos = list(pivot.columns)

    fig, ax = plt.subplots(figsize=(8.0, 4.8), dpi=300)
    im = ax.imshow(pivot.values, cmap="YlGnBu", aspect="auto")
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("ICC-v2 Mean ARI", fontsize=11.0, fontweight="bold")
    cbar.ax.tick_params(labelsize=10.0)

    ax.set_xticks(range(len(rhos)))
    ax.set_xticklabels([f"{r:.1f}" for r in rhos], fontsize=11.0, fontweight="bold")
    ax.set_yticks(range(len(strategies)))
    ax.set_yticklabels([s.upper() for s in strategies], fontsize=11.0, fontweight="bold")
    ax.set_xlabel(r"Missing Data Fraction $\rho$", fontsize=12.0, fontweight="bold")
    ax.set_ylabel("Imputation Strategy", fontsize=12.0, fontweight="bold")
    ax.set_title("Figure 25b: ICC-v2 Performance across Imputation Paradigms", fontsize=13.0, fontweight="bold")

    for r in range(len(strategies)):
        for c in range(len(rhos)):
            val = pivot.values[r, c]
            ax.text(c, r, f"{val:.3f}", ha="center", va="center", color="white" if val > 0.3 else "black", fontsize=10.0, fontweight="bold")

    fig.tight_layout()
    out_file = FIGURES_DIR / "fig25b_imputation_strategy_heatmap.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved {out_file}")


def generate_all_plots():
    plot_missing_data_curves()
    plot_imputation_strategy_heatmap()


if __name__ == "__main__":
    generate_all_plots()
