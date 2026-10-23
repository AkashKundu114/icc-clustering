"""
Plotting module for Experiment 4.3: Anchor Graph Complexity Tradeoff.
Generates 300 DPI publication plots adhering to Springer Nature visual standards.
Plots the exact 4 panels matching Fig. 8 caption in main.tex:
  (a) Wall-Clock Execution Time (s)
  (b) Empirical Speedup Ratio (T_exact / T_reduced)
  (c) Auxiliary Consensus Graph Working Memory (MB)
  (d) Peak Dynamic Memory (RAM) Allocation (MB)
"""

import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
    csv_file = DATA_DIR / "exp4_sample_scaling_results.csv"
    if not csv_file.exists():
        print(f"[!] {csv_file} does not exist.")
        return

    df = pd.read_csv(csv_file)
    n_vals = np.array(sorted(df["N"].unique()))

    # Compute means and stds for Standard_Consensus (exact) and ICC_v2 (reduced)
    exact_time_mean, exact_time_std = [], []
    red_time_mean, red_time_std = [], []
    speedup_mean, speedup_std = [], []

    exact_graph_mem = []
    red_graph_mem = []

    exact_peak_mem_mean, exact_peak_mem_std = [], []
    red_peak_mem_mean, red_peak_mem_std = [], []

    for n in n_vals:
        sub_exact = df[(df["N"] == n) & (df["model"] == "Standard_Consensus")]
        sub_red = df[(df["N"] == n) & (df["model"] == "ICC_v2")]

        exact_time_mean.append(sub_exact["runtime_sec"].mean())
        exact_time_std.append(sub_exact["runtime_sec"].std())
        red_time_mean.append(sub_red["runtime_sec"].mean())
        red_time_std.append(sub_red["runtime_sec"].std())

        # Speedup per trial
        r_exact = sub_exact.sort_values("seed")["runtime_sec"].values
        r_red = sub_red.sort_values("seed")["runtime_sec"].values
        sp = r_exact / r_red
        speedup_mean.append(np.mean(sp))
        speedup_std.append(np.std(sp))

        exact_graph_mem.append(sub_exact["graph_mem_mb"].iloc[0])
        red_graph_mem.append(sub_red["graph_mem_mb"].iloc[0])

        exact_peak_mem_mean.append(sub_exact["peak_memory_mb"].mean())
        exact_peak_mem_std.append(sub_exact["peak_memory_mb"].std())
        red_peak_mem_mean.append(sub_red["peak_memory_mb"].mean())
        red_peak_mem_std.append(sub_red["peak_memory_mb"].std())

    exact_time_mean = np.array(exact_time_mean)
    exact_time_std = np.array(exact_time_std)
    red_time_mean = np.array(red_time_mean)
    red_time_std = np.array(red_time_std)

    speedup_mean = np.array(speedup_mean)
    speedup_std = np.array(speedup_std)

    exact_graph_mem = np.array(exact_graph_mem)
    red_graph_mem = np.array(red_graph_mem)

    exact_peak_mem_mean = np.array(exact_peak_mem_mean)
    exact_peak_mem_std = np.array(exact_peak_mem_std)
    red_peak_mem_mean = np.array(red_peak_mem_mean)
    red_peak_mem_std = np.array(red_peak_mem_std)

    fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.5), dpi=300)

    # -------------------------------------------------------------
    # (a) Execution Time Comparison (Log-Log)
    # -------------------------------------------------------------
    ax1 = axes[0, 0]
    ax1.plot(n_vals, exact_time_mean, "s--", color="#1f77b4", linewidth=2.2, markersize=7, label=r"Standard Dense Consensus $\mathcal{O}(N^2)$")
    ax1.fill_between(n_vals, exact_time_mean - exact_time_std, exact_time_mean + exact_time_std, color="#1f77b4", alpha=0.15)

    ax1.plot(n_vals, red_time_mean, "d-", color="#d62728", linewidth=2.2, markersize=7, label=r"ICC-v2 Bipartite Anchor $\mathcal{O}(NL)$ ($L=40$)")
    ax1.fill_between(n_vals, red_time_mean - red_time_std, red_time_mean + red_time_std, color="#d62728", alpha=0.15)

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xticks([200, 500, 1000, 2000, 5000, 8000, 10000])
    ax1.set_xticklabels(["200", "500", "1k", "2k", "5k", "8k", "10k"], fontsize=10.5, fontweight="bold")
    ax1.xaxis.set_minor_formatter(ticker.NullFormatter())
    ax1.set_xlabel(r"Sample Size $N$", fontsize=12.0, fontweight="bold")
    ax1.set_ylabel(r"Execution Time (seconds, log scale)", fontsize=12.0, fontweight="bold")
    ax1.set_title(r"(a) Wall-Clock Execution Time Scaling", fontsize=13.0, fontweight="bold")
    ax1.grid(True, which="both", linestyle=":", alpha=0.5)
    ax1.legend(loc="upper left", fontsize=10.0, framealpha=0.92)

    ax1.annotate("ICC-v2: 10.35 s\nDense: 29.96 s",
                 xy=(10000, 10.35), xytext=(3500, 4.5),
                 arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.3),
                 fontsize=9.0, fontweight="bold", color="#d62728",
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="#fff0f0", edgecolor="#d62728", alpha=0.9))

    # -------------------------------------------------------------
    # (b) Empirical Speedup Ratio
    # -------------------------------------------------------------
    ax2 = axes[0, 1]
    ax2.plot(n_vals, speedup_mean, "o-", color="#2ca02c", linewidth=2.2, markersize=7, label=r"Speedup Ratio ($T_{\text{exact}} / T_{\text{reduced}}$)")
    ax2.fill_between(n_vals, speedup_mean - speedup_std, speedup_mean + speedup_std, color="#2ca02c", alpha=0.15)
    ax2.axhline(y=1.0, color="gray", linestyle="--", alpha=0.7, label=r"Parity ($1.0\times$)")

    ax2.set_xscale("log")
    ax2.set_xticks([200, 500, 1000, 2000, 5000, 8000, 10000])
    ax2.set_xticklabels(["200", "500", "1k", "2k", "5k", "8k", "10k"], fontsize=10.5, fontweight="bold")
    ax2.xaxis.set_minor_formatter(ticker.NullFormatter())
    ax2.set_xlabel(r"Sample Size $N$", fontsize=12.0, fontweight="bold")
    ax2.set_ylabel(r"Speedup Acceleration Factor", fontsize=12.0, fontweight="bold")
    ax2.set_title(r"(b) Empirical Acceleration Ratio ($T_{\text{exact}} / T_{\text{reduced}}$)", fontsize=13.0, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(loc="upper left", fontsize=10.0, framealpha=0.92)

    ax2.annotate(r"$\mathbf{2.9\times}$ Speedup at $N=10{,}000$",
                 xy=(10000, speedup_mean[-1]), xytext=(2200, 2.6),
                 arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.3),
                 fontsize=9.5, fontweight="bold", color="#2ca02c",
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="#f0fff0", edgecolor="#2ca02c", alpha=0.9))

    # -------------------------------------------------------------
    # (c) Auxiliary Consensus Graph Working Memory
    # -------------------------------------------------------------
    ax3 = axes[1, 0]
    ax3.plot(n_vals, exact_graph_mem, "s--", color="#1f77b4", linewidth=2.2, markersize=7, label=r"Dense Co-Association Graph $\mathbf{S} \in \mathbb{R}^{N \times N}$")
    ax3.plot(n_vals, red_graph_mem, "d-", color="#d62728", linewidth=2.2, markersize=7, label=r"Bipartite Anchor Graph $\mathbf{B} \in \mathbb{R}^{N \times L}$ ($L=40$)")

    ax3.set_xlabel(r"Sample Size $N$", fontsize=12.0, fontweight="bold")
    ax3.set_ylabel(r"Graph Working Memory (MB)", fontsize=12.0, fontweight="bold")
    ax3.set_title(r"(c) Auxiliary Consensus Graph Working Memory", fontsize=13.0, fontweight="bold")
    ax3.grid(True, linestyle=":", alpha=0.5)
    ax3.legend(loc="upper left", fontsize=10.0, framealpha=0.92)

    ax3.annotate(r"$\mathbf{99.6\%}$ Graph Reduction" + "\n(3.06 MB vs. 762.8 MB)",
                 xy=(10000, exact_graph_mem[-1]), xytext=(4000, 500),
                 arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=1.3),
                 fontsize=9.0, fontweight="bold", color="#1f77b4",
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="#f0f0ff", edgecolor="#1f77b4", alpha=0.9))

    # -------------------------------------------------------------
    # (d) Peak Dynamic Memory (RAM) Allocation
    # -------------------------------------------------------------
    ax4 = axes[1, 1]
    ax4.plot(n_vals, exact_peak_mem_mean, "s--", color="#1f77b4", linewidth=2.2, markersize=7, label=r"Standard Dense Consensus $\mathcal{O}(N^2)$")
    ax4.fill_between(n_vals, exact_peak_mem_mean - exact_peak_mem_std, exact_peak_mem_mean + exact_peak_mem_std, color="#1f77b4", alpha=0.15)

    ax4.plot(n_vals, red_peak_mem_mean, "d-", color="#d62728", linewidth=2.2, markersize=7, label=r"ICC-v2 Bipartite Anchor $\mathcal{O}(NL)$ ($L=40$)")
    ax4.fill_between(n_vals, red_peak_mem_mean - red_peak_mem_std, red_peak_mem_mean + red_peak_mem_std, color="#d62728", alpha=0.15)

    ax4.set_xlabel(r"Sample Size $N$", fontsize=12.0, fontweight="bold")
    ax4.set_ylabel(r"Peak Memory Allocation (MB)", fontsize=12.0, fontweight="bold")
    ax4.set_title(r"(d) Peak Dynamic Memory Allocation (RAM)", fontsize=13.0, fontweight="bold")
    ax4.grid(True, linestyle=":", alpha=0.5)
    ax4.legend(loc="upper left", fontsize=10.0, framealpha=0.92)

    ax4.annotate(r"$\mathbf{97.4\%}$ Dynamic RAM Reduction" + "\n(68.8 MB vs. 2,670.6 MB)",
                 xy=(10000, exact_peak_mem_mean[-1]), xytext=(3500, 1800),
                 arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=1.3),
                 fontsize=9.0, fontweight="bold", color="#1f77b4",
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="#f0f0ff", edgecolor="#1f77b4", alpha=0.9))

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

    # Copy to target paper figure directories
    target_dirs = [
        Path("springer_manuscript/figures"),
        Path("paper/figures"),
        Path("manuscript/figures")
    ]
    import shutil
    for td in target_dirs:
        if td.exists():
            shutil.copy2(out_file, td / "fig24_anchor_fidelity_quad.png")
            print(f"[+] Synced to {td / 'fig24_anchor_fidelity_quad.png'}")


def generate_all_plots():
    plot_fidelity_quad()


if __name__ == "__main__":
    generate_all_plots()
