"""
Plotting module for Experiment 3.5: Missing Data Robustness & Imputation Resilience.
Generates publication-quality 300 DPI figures following IEEE TKDE standards:
- Figure 25a / 18a: 3-panel curve (Colon, Leukemia, SRBCT) of ARI vs rho across methods.
- Figure 25b / 18b: Imputation strategy vs rho heatmap for ICC-v2.
"""

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

EXP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = EXP_DIR / "data"
FIGURES_DIR = EXP_DIR / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CSV = DATA_DIR / "exp3_5_missing_data_results.csv"

# IEEE TKDE publication typography & style
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10.0,
    "axes.labelsize": 11.0,
    "axes.titlesize": 11.5,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9.0,
    "figure.titlesize": 13.0,
    "lines.linewidth": 2.0,
    "grid.alpha": 0.35,
    "grid.linestyle": ":",
})

METHOD_PALETTE = {
    "K-Means": ("#7f7f7f", ":", "o", "K-Means (Baseline)"),
    "Standard_Consensus": ("#1f77b4", "--", "s", "Standard Consensus"),
    "Li_et_al_2019": ("#ff7f0e", "-.", "^", "Li et al. (2019)"),
    "ICC_v1": ("#2ca02c", "-", "D", "ICC-v1 (Anchor Only)"),
    "ICC_v2": ("#d62728", "-", "*", "ICC-v2 (VSSG+Anchor, Ours)"),
}


def plot_missing_data_curves(
    csv_path: Optional[Path] = None,
    save_path: Optional[Path] = None,
):
    """
    Figure 25a (and Figure 18a): 3-panel comparative performance curves (ARI vs missingness fraction rho)
    for Colon, Leukemia, and SRBCT across clustering algorithms.
    """
    if csv_path is None:
        csv_path = DEFAULT_CSV
    if save_path is None:
        save_path = FIGURES_DIR / "fig25a_missing_data_degradation.png"

    if not Path(csv_path).exists():
        print(f"[!] File not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    datasets = ["colon", "leukemia", "srbct"]
    dataset_titles = [
        "Colon (N=62, D=2,000, K=2)",
        "Leukemia (N=72, D=7,129, K=2)",
        "SRBCT (N=83, D=2,308, K=4)",
    ]

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.0), dpi=300, sharey=True)

    for idx, dname in enumerate(datasets):
        ax = axes[idx]
        df_d = df[df["dataset"].str.lower() == dname.lower()]
        if df_d.empty:
            continue

        rho_vals = sorted(df_d["rho"].unique())

        for mname, (color, style, marker, label) in METHOD_PALETTE.items():
            df_m = df_d[df_d["method"] == mname]
            if df_m.empty:
                continue

            # Group across trials and imputation strategies
            summary = df_m.groupby("rho")["ari"].agg(["mean", "std"]).reindex(rho_vals)
            means = summary["mean"].values
            stds = summary["std"].fillna(0).values

            is_icc2 = (mname == "ICC_v2")
            lw = 2.8 if is_icc2 else 1.6
            ms = 8.0 if is_icc2 else 5.5
            zorder = 5 if is_icc2 else 3

            ax.plot(
                rho_vals,
                means,
                linestyle=style,
                marker=marker,
                color=color,
                label=label,
                linewidth=lw,
                markersize=ms,
                zorder=zorder,
            )
            ax.fill_between(
                rho_vals,
                means - stds,
                means + stds,
                color=color,
                alpha=0.15 if is_icc2 else 0.05,
                zorder=zorder - 1,
            )

        ax.set_xlabel(r"Missingness Fraction ($\rho_{\mathrm{MCAR}}$)")
        if idx == 0:
            ax.set_ylabel("Clustering Recovery (ARI)", fontweight="bold")
        ax.set_title(f"({chr(97 + idx)}) {dataset_titles[idx]}", fontweight="bold", pad=8)
        ax.set_xlim(-0.02, 0.72)
        ax.set_ylim(-0.08, 0.85)
        ax.grid(True)

    # Common unified legend above panels
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.05),
        ncol=5,
        frameon=True,
        facecolor="white",
        edgecolor="#cccccc",
        fontsize=9.5,
    )

    fig.suptitle("Cluster Recovery Robustness under Increasing Missingness Rates", fontweight="bold", y=1.11, fontsize=12.5)
    fig.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    # Also save fig18a alias
    fig18a_path = FIGURES_DIR / "fig18a_missing_data_curves.png"
    plt.savefig(fig18a_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved Figure 25a to: {save_path} and {fig18a_path}")


def plot_imputation_strategy_heatmap(
    csv_path: Optional[Path] = None,
    save_path: Optional[Path] = None,
):
    """
    Figure 25b (and Figure 18b): Imputation Strategy vs Missingness Fraction rho Heatmap for ICC-v2.
    Displays cross-dataset mean ARI recovery across Mean, Median, KNN, and Zero schemes.
    """
    if csv_path is None:
        csv_path = DEFAULT_CSV
    if save_path is None:
        save_path = FIGURES_DIR / "fig25b_imputation_strategy_heatmap.png"

    if not Path(csv_path).exists():
        return

    df = pd.read_csv(csv_path)
    df_icc2 = df[df["method"] == "ICC_v2"]
    if df_icc2.empty:
        return

    # Standardize imputation strategy capitalization
    df_icc2 = df_icc2.copy()
    col_strat = "imputation" if "imputation" in df_icc2.columns else "strategy"
    df_icc2["imputation_std"] = df_icc2[col_strat].astype(str).str.capitalize()

    datasets = ["colon", "leukemia", "srbct"]
    rhos = sorted(df_icc2["rho"].unique())
    strategies = ["Mean", "Median", "KNN", "Zero"]

    # 4-panel layout: 3 cohorts + Overall Cross-Cohort Average
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.2), dpi=300)

    for i, dname in enumerate(datasets):
        ax = axes[i]
        sub = df_icc2[df_icc2["dataset"].str.lower() == dname.lower()]
        pivot = sub.groupby(["imputation_std", "rho"])["ari"].mean().unstack().reindex(index=strategies, columns=rhos)

        im = ax.imshow(pivot.values, cmap="YlGnBu", vmin=-0.05, vmax=0.80, aspect="auto")

        ax.set_xticks(range(len(rhos)))
        ax.set_xticklabels([f"{r:.2f}" for r in rhos])
        ax.set_yticks(range(len(strategies)))
        ax.set_yticklabels(strategies if i == 0 else [])
        ax.set_xlabel(r"Missing Rate $\rho$")
        if i == 0:
            ax.set_ylabel("Imputation Strategy", fontweight="bold")
        ax.set_title(f"({chr(97 + i)}) {dname.upper()}", fontweight="bold", pad=6)

        for r_idx in range(len(strategies)):
            for c_idx in range(len(rhos)):
                val = pivot.values[r_idx, c_idx]
                if not np.isnan(val):
                    ax.text(
                        c_idx,
                        r_idx,
                        f"{val:.3f}",
                        ha="center",
                        va="center",
                        color="white" if val > 0.40 else "black",
                        fontsize=8.5,
                        fontweight="bold",
                    )

    # Panel (d): Cross-Cohort Grand Mean
    ax_avg = axes[3]
    pivot_avg = df_icc2.groupby(["imputation_std", "rho"])["ari"].mean().unstack().reindex(index=strategies, columns=rhos)
    im_avg = ax_avg.imshow(pivot_avg.values, cmap="YlGnBu", vmin=-0.05, vmax=0.80, aspect="auto")

    ax_avg.set_xticks(range(len(rhos)))
    ax_avg.set_xticklabels([f"{r:.2f}" for r in rhos])
    ax_avg.set_yticks(range(len(strategies)))
    ax_avg.set_yticklabels([])
    ax_avg.set_xlabel(r"Missing Rate $\rho$")
    ax_avg.set_title("(d) Cross-Cohort Mean", fontweight="bold", pad=6)

    for r_idx in range(len(strategies)):
        for c_idx in range(len(rhos)):
            val = pivot_avg.values[r_idx, c_idx]
            if not np.isnan(val):
                ax_avg.text(
                    c_idx,
                    r_idx,
                    f"{val:.3f}",
                    ha="center",
                    va="center",
                    color="white" if val > 0.40 else "black",
                    fontsize=8.5,
                    fontweight="bold",
                )

    cbar_ax = fig.add_axes([0.92, 0.18, 0.015, 0.68])
    cbar = fig.colorbar(im_avg, cax=cbar_ax)
    cbar.set_label("ICC-v2 Clustering Recovery (ARI)", fontweight="bold")

    fig.suptitle(
        r"ICC-v2 Performance Heatmap Across Imputation Strategies and Missingness Rates $\rho$",
        fontweight="bold",
        y=1.03,
        fontsize=12.5,
    )
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    # Also save fig18b alias
    fig18b_path = FIGURES_DIR / "fig18b_imputation_heatmap.png"
    plt.savefig(fig18b_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved Figure 25b to: {save_path} and {fig18b_path}")


def generate_all_plots():
    plot_missing_data_curves()
    plot_imputation_strategy_heatmap()


if __name__ == "__main__":
    generate_all_plots()
