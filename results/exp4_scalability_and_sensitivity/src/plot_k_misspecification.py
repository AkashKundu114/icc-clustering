"""
Plotting module for Experiment 4.2: K-Misspecification Sensitivity & Robustness.
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
    "Ward": ("#8c564b", "--", "^"),
    "Spectral": ("#9467bd", "-.", "s"),
    "FCM": ("#e377c2", ":", "v"),
    "Standard_Consensus": ("#1f77b4", "--", "p"),
    "Li_et_al_2019": ("#ff7f0e", "-.", "h"),
    "ICC_v1": ("#2ca02c", "-", "D"),
    "ICC_v2": ("#d62728", "-", "*"),
}


def plot_k_robustness(metric="ari"):
    csv_file = DATA_DIR / "exp4_2_k_misspecification_results.csv"
    if not csv_file.exists():
        print(f"[!] {csv_file} does not exist. Run sweep first.")
        return

    df = pd.read_csv(csv_file)
    datasets = ["Synthetic", "Sonar", "SRBCT"]

    fig, axes = plt.subplots(1, 3, figsize=(16, 5), dpi=300, sharey=False)

    for i, dname in enumerate(datasets):
        ax = axes[i]
        df_d = df[df["dataset"] == dname]
        if df_d.empty:
            continue

        k_true = df_d["k_true"].iloc[0]
        k_inputs = sorted(df_d["k_input"].unique())

        for method, (color, style, marker) in METHOD_PALETTE.items():
            df_m = df_d[df_d["method"] == method]
            if df_m.empty:
                continue

            summary = df_m.groupby("k_input")[metric].agg(["mean", "std"]).reindex(k_inputs)
            means = summary["mean"].values
            stds = summary["std"].fillna(0).values

            is_icc2 = (method == "ICC_v2")
            lw = 3.0 if is_icc2 else 1.8
            ms = 9 if is_icc2 else 6
            zorder = 5 if is_icc2 else 2

            ax.plot(
                k_inputs,
                means,
                linestyle=style,
                marker=marker,
                color=color,
                label=method,
                linewidth=lw,
                markersize=ms,
                zorder=zorder,
            )
            ax.fill_between(k_inputs, means - stds, means + stds, color=color, alpha=0.12 if is_icc2 else 0.05, zorder=zorder - 1)

        ax.axvline(x=k_true, color="black", linestyle="--", linewidth=1.5, label=f"True $K={k_true}$", alpha=0.7)
        ax.set_xlabel("Specified Clusters ($K_{\\text{input}}$)")
        ax.set_ylabel(f"Clustering {metric.upper()}")
        ax.set_title(f"({chr(97 + i)}) {dname} ($K_{{\\text{{true}}}} = {k_true}$)")
        ax.grid(True)
        ax.set_xticks(k_inputs)
        clean_spines(ax)

    # Single common legend at top
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=5, frameon=True)

    fig.tight_layout()
    out_file = FIGURES_DIR / f"fig23_k_misspecification_{metric.lower()}.png"
    alt_file = FIGURES_DIR / f"fig_k_misspecification_{metric.lower()}.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.savefig(alt_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved {out_file} and {alt_file}")


def generate_all_plots():
    plot_k_robustness(metric="ari")
    plot_k_robustness(metric="nmi")


if __name__ == "__main__":
    generate_all_plots()
