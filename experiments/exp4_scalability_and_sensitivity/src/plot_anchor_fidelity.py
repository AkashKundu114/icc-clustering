"""
Plotting module for Experiment 4.3: Anchor Approximation Fidelity.
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

from icc.viz_style import set_academic_style, clean_spines

set_academic_style()

EXP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = EXP_DIR / "data"
FIGURES_DIR = EXP_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def plot_fidelity_quad():
    csv_file = DATA_DIR / "exp4_3_anchor_fidelity_results.csv"
    if not csv_file.exists():
        print(f"[!] {csv_file} does not exist.")
        return

    df = pd.read_csv(csv_file)
    summary = df.groupby("N").agg({
        "ari_reduced": ["mean", "std"],
        "ari_exact": ["mean", "std"],
        "delta_ari": ["mean", "std"],
        "time_reduced": ["mean", "std"],
        "time_exact": ["mean", "std"],
        "speedup": ["mean", "std"],
        "mem_reduced_mb": ["mean", "std"],
        "mem_exact_mb": ["mean", "std"],
    }).reset_index()

    n_vals = summary["N"].values
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.5), dpi=300)

    # 1. Top-Left: ARI Comparison
    ax1 = axes[0, 0]
    m_red = summary["ari_reduced"]["mean"].values
    s_red = summary["ari_reduced"]["std"].values
    m_ext = summary["ari_exact"]["mean"].values
    s_ext = summary["ari_exact"]["std"].values

    ax1.plot(n_vals, m_red, "o-", color="#d62728", linewidth=2.2, markersize=7, label=r"ICC-v2 Reduced $\mathcal{O}(N)$")
    ax1.fill_between(n_vals, m_red - s_red, m_red + s_red, color="#d62728", alpha=0.15)
    ax1.plot(n_vals, m_ext, "s--", color="#1f77b4", linewidth=2.2, markersize=7, label=r"ICC-v2 Exact $\mathcal{O}(N^2)$")
    ax1.fill_between(n_vals, m_ext - s_ext, m_ext + s_ext, color="#1f77b4", alpha=0.15)
    ax1.set_xlabel("Sample Size $N$", fontsize=12.0, fontweight="bold")
    ax1.set_ylabel("Adjusted Rand Index (ARI)", fontsize=12.0, fontweight="bold")
    ax1.tick_params(labelsize=11.0)
    ax1.set_title("(a) Clustering Quality Fidelity", fontsize=13.0, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(loc="lower right", fontsize=10.5)

    # 2. Top-Right: Delta ARI (Approximation Cost)
    ax2 = axes[0, 1]
    d_m = summary["delta_ari"]["mean"].values
    d_s = summary["delta_ari"]["std"].values
    ax2.plot(n_vals, d_m, "D-", color="#2ca02c", linewidth=2.2, markersize=7, label=r"$\Delta \text{ARI} = \text{Exact} - \text{Reduced}$")
    ax2.fill_between(n_vals, d_m - d_s, d_m + d_s, color="#2ca02c", alpha=0.15)
    ax2.axhline(y=0.0, color="black", linestyle=":", alpha=0.6)
    ax2.axhline(y=0.02, color="gray", linestyle="--", alpha=0.5, label=r"$\pm 0.02$ Bound")
    ax2.axhline(y=-0.02, color="gray", linestyle="--", alpha=0.5)
    ax2.set_xlabel("Sample Size $N$", fontsize=12.0, fontweight="bold")
    ax2.set_ylabel(r"Fidelity Gap $\Delta \text{ARI}$", fontsize=12.0, fontweight="bold")
    ax2.tick_params(labelsize=11.0)
    ax2.set_title("(b) Anchor Approximation Error", fontsize=13.0, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(loc="upper right", fontsize=10.5)

    # 3. Bottom-Left: Runtime Comparison (Log-Log)
    ax3 = axes[1, 0]
    t_red = summary["time_reduced"]["mean"].values
    t_ext = summary["time_exact"]["mean"].values
    ax3.loglog(n_vals, t_red, "o-", color="#d62728", linewidth=2.2, markersize=7, label=r"ICC-v2 Reduced [$\mathcal{O}(N)$]")
    ax3.loglog(n_vals, t_ext, "s--", color="#1f77b4", linewidth=2.2, markersize=7, label=r"ICC-v2 Exact [$\mathcal{O}(N^2)$]")
    ax3.set_xlabel("Sample Size $N$ (log scale)", fontsize=12.0, fontweight="bold")
    ax3.set_ylabel("Execution Time [s] (log scale)", fontsize=12.0, fontweight="bold")
    ax3.tick_params(labelsize=11.0)
    ax3.set_title("(c) Asymptotic Runtime Scalability", fontsize=13.0, fontweight="bold")
    ax3.grid(True, which="both", linestyle=":", alpha=0.5)
    ax3.legend(loc="upper left", fontsize=10.5)

    # 4. Bottom-Right: Memory Footprint
    ax4 = axes[1, 1]
    mem_red = summary["mem_reduced_mb"]["mean"].values
    mem_ext = summary["mem_exact_mb"]["mean"].values
    ax4.plot(n_vals, mem_red, "o-", color="#d62728", linewidth=2.2, markersize=7, label="ICC-v2 Reduced")
    ax4.plot(n_vals, mem_ext, "s--", color="#1f77b4", linewidth=2.2, markersize=7, label=r"ICC-v2 Exact (Dense $N \times N$)")
    ax4.set_xlabel("Sample Size $N$", fontsize=12.0, fontweight="bold")
    ax4.set_ylabel("Peak Memory Allocation [MB]", fontsize=12.0, fontweight="bold")
    ax4.tick_params(labelsize=11.0)
    ax4.set_title("(d) Memory Footprint Scalability", fontsize=13.0, fontweight="bold")
    ax4.grid(True, linestyle=":", alpha=0.5)
    ax4.legend(loc="upper left", fontsize=10.5)

    clean_spines(ax1)
    clean_spines(ax2)
    clean_spines(ax3)
    clean_spines(ax4)

    fig.tight_layout()
    out_file = FIGURES_DIR / "fig24_anchor_fidelity_quad.png"
    out_alias = FIGURES_DIR / "fig_anchor_fidelity_quad.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.savefig(out_alias, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved quad-panel figure to {out_file} and {out_alias}")


def generate_all_plots():
    plot_fidelity_quad()


if __name__ == "__main__":
    generate_all_plots()
