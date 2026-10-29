"""
Plot Anchor Fidelity Quad Comparison (Figure 24 / Figure 18).
Generates the 2x2 multi-panel figure comparing Standard Dense Consensus O(N^2)
vs GAC Pipeline Bipartite Anchor Consensus O(NL).
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

SRC_DIR = Path(__file__).resolve().parent
EXP_DIR = SRC_DIR.parent
DATA_DIR = EXP_DIR / "data"
FIGURES_DIR = EXP_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def plot_fidelity_quad():
    csv_file = DATA_DIR / "exp4_sample_scaling_results.csv"
    if not csv_file.exists():
        print(f"[!] {csv_file} does not exist.")
        return

    df = pd.read_csv(csv_file)
    exact_n = set(df[df["model"] == "Standard_Consensus"]["N"])
    red_n = set(df[df["model"] == "ICC_v2"]["N"])
    n_vals = np.array(sorted(exact_n.intersection(red_n)))

    exact_time_mean, exact_time_std = [], []
    red_time_mean, red_time_std = [], []
    speedup_mean, speedup_std = [], []
    exact_graph_mem, red_graph_mem = [], []
    exact_peak_mem_mean, exact_peak_mem_std = [], []
    red_peak_mem_mean, red_peak_mem_std = [], []

    for n in n_vals:
        sub_exact = df[(df["N"] == n) & (df["model"] == "Standard_Consensus")]
        sub_red = df[(df["N"] == n) & (df["model"] == "ICC_v2")]

        t_ex = sub_exact["runtime_sec"].values[0]
        t_ex_std = sub_exact["time_std"].values[0] if "time_std" in sub_exact.columns else 0.0
        t_red = sub_red["runtime_sec"].values[0]
        t_red_std = sub_red["time_std"].values[0] if "time_std" in sub_red.columns else 0.0

        exact_time_mean.append(t_ex)
        exact_time_std.append(t_ex_std)
        red_time_mean.append(t_red)
        red_time_std.append(t_red_std)

        speedup_mean.append(t_ex / t_red)
        speedup_std.append(0.0)

        exact_graph_mem.append((n * n * 8) / (1024 * 1024))
        red_graph_mem.append((n * 40 * 8) / (1024 * 1024))

        exact_peak_mem_mean.append(sub_exact["peak_memory_mb"].values[0])
        exact_peak_mem_std.append(sub_exact["mem_std"].values[0] if "mem_std" in sub_exact.columns else 0.0)
        red_peak_mem_mean.append(sub_red["peak_memory_mb"].values[0])
        red_peak_mem_std.append(sub_red["mem_std"].values[0] if "mem_std" in sub_red.columns else 0.0)

    exact_time_mean = np.array(exact_time_mean)
    exact_time_std = np.array(exact_time_std)
    red_time_mean = np.array(red_time_mean)
    red_time_std = np.array(red_time_std)
    speedup_mean = np.array(speedup_mean)

    exact_graph_mem = np.array(exact_graph_mem)
    red_graph_mem = np.array(red_graph_mem)
    exact_peak_mem_mean = np.array(exact_peak_mem_mean)
    red_peak_mem_mean = np.array(red_peak_mem_mean)

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, axes = plt.subplots(2, 2, figsize=(14, 11), dpi=300)

    # Panel 1: Time
    ax1 = axes[0, 0]
    ax1.plot(n_vals, exact_time_mean, "s--", color="#1f77b4", linewidth=2.2, markersize=7, label=r"Standard Dense Consensus $\mathcal{O}(N^2)$")
    ax1.fill_between(n_vals, exact_time_mean - exact_time_std, exact_time_mean + exact_time_std, color="#1f77b4", alpha=0.15)
    ax1.plot(n_vals, red_time_mean, "d-", color="#d62728", linewidth=2.2, markersize=7, label=r"GAC Pipeline Bipartite Anchor $\mathcal{O}(NL)$ ($L=40$)")
    ax1.fill_between(n_vals, red_time_mean - red_time_std, red_time_mean + red_time_std, color="#d62728", alpha=0.15)
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel(r"Sample Size $N$", fontsize=12.0, fontweight="bold")
    ax1.set_ylabel(r"Execution Time (seconds, log scale)", fontsize=12.0, fontweight="bold")
    ax1.set_title(r"(a) Wall-Clock Execution Time Scaling", fontsize=13.0, fontweight="bold")
    ax1.grid(True, which="both", linestyle=":", alpha=0.5)
    ax1.legend(loc="upper left", fontsize=10.0, framealpha=0.92)

    # Panel 2: Speedup
    ax2 = axes[0, 1]
    ax2.plot(n_vals, speedup_mean, "o-", color="#2ca02c", linewidth=2.2, markersize=7, label="Empirical Speedup Factor")
    ax2.axhline(1.0, color="gray", linestyle="--", linewidth=1.5, alpha=0.7)
    ax2.set_xscale("log")
    ax2.set_xlabel(r"Sample Size $N$", fontsize=12.0, fontweight="bold")
    ax2.set_ylabel(r"Speedup Ratio ($T_{\text{exact}} / T_{\text{GAC}}$)", fontsize=12.0, fontweight="bold")
    ax2.set_title(r"(b) Empirical Acceleration Factor", fontsize=13.0, fontweight="bold")
    ax2.grid(True, which="both", linestyle=":", alpha=0.5)
    ax2.legend(loc="upper left", fontsize=10.0, framealpha=0.92)

    # Panel 3: Graph Memory
    ax3 = axes[1, 0]
    ax3.plot(n_vals, exact_graph_mem, "s--", color="#1f77b4", linewidth=2.2, markersize=7, label=r"Dense Co-Association Graph $\mathcal{O}(N^2)$")
    ax3.plot(n_vals, red_graph_mem, "d-", color="#d62728", linewidth=2.2, markersize=7, label=r"Bipartite Anchor Graph $\mathcal{O}(NL)$ ($L=40$)")
    ax3.set_xscale("log")
    ax3.set_yscale("log")
    ax3.set_xlabel(r"Sample Size $N$", fontsize=12.0, fontweight="bold")
    ax3.set_ylabel(r"Graph Storage Memory (MB, log scale)", fontsize=12.0, fontweight="bold")
    ax3.set_title(r"(c) Theoretical Graph Memory Consumption", fontsize=13.0, fontweight="bold")
    ax3.grid(True, which="both", linestyle=":", alpha=0.5)
    ax3.legend(loc="upper left", fontsize=10.0, framealpha=0.92)

    # Panel 4: Peak Process Memory
    ax4 = axes[1, 1]
    ax4.plot(n_vals, exact_peak_mem_mean, "s--", color="#1f77b4", linewidth=2.2, markersize=7, label=r"Standard Dense Consensus $\mathcal{O}(N^2)$")
    ax4.plot(n_vals, red_peak_mem_mean, "d-", color="#d62728", linewidth=2.2, markersize=7, label=r"GAC Pipeline Bipartite Anchor $\mathcal{O}(NL)$ ($L=40$)")
    ax4.set_xscale("log")
    ax4.set_xlabel(r"Sample Size $N$", fontsize=12.0, fontweight="bold")
    ax4.set_ylabel(r"Peak Process RAM (MB)", fontsize=12.0, fontweight="bold")
    ax4.set_title(r"(d) Empirical Peak Memory Footprint", fontsize=13.0, fontweight="bold")
    ax4.grid(True, which="both", linestyle=":", alpha=0.5)
    ax4.legend(loc="upper left", fontsize=10.0, framealpha=0.92)

    plt.tight_layout()
    out_file = FIGURES_DIR / "fig24_anchor_fidelity_quad.png"
    plt.savefig(out_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved: {out_file}")


def generate_all_plots():
    plot_fidelity_quad()


if __name__ == "__main__":
    generate_all_plots()
