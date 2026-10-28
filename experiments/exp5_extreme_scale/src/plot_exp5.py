"""
Plotting module for Experiment 5: Extreme Asymptotic Scaling Suite.
Generates 300 DPI publication plots adhering to IEEE TKDE visual standards.

2x2 Panel Architecture:
- Panel (a): Runtime vs N (log-log) across N in [10k, 1M]
- Panel (b): Peak Memory vs N (linear RAM footprint)
- Panel (c): Runtime vs D across D in [1k, 100k]
- Panel (d): Clustering Recovery (ARI) vs N
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


def plot_extreme_scale_quad(save_path=None):
    csv_sample = DATA_DIR / "exp5_sample_scaling_results.csv"
    csv_dim = DATA_DIR / "exp5_dimension_scaling_results.csv"

    if not (csv_sample.exists() and csv_dim.exists()):
        print(f"[!] Missing CSV files in {DATA_DIR}. Run extreme_scale_benchmark.py first.")
        return

    df_s = pd.read_csv(csv_sample)
    df_d = pd.read_csv(csv_dim)

    fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.5), dpi=300)

    # =========================================================================
    # Panel (a): Runtime vs N (log-log)
    # =========================================================================
    ax1 = axes[0, 0]
    sum_s = df_s.groupby("N").agg({
        "time_icc": ["mean", "std"],
        "time_mbk": ["mean", "std"],
        "time_km": ["mean", "std"],
    }).reset_index()

    n_vals = sum_s["N"].values
    t_icc = sum_s["time_icc"]["mean"].values
    std_icc = np.nan_to_num(sum_s["time_icc"]["std"].values)
    t_mbk = sum_s["time_mbk"]["mean"].values
    std_mbk = np.nan_to_num(sum_s["time_mbk"]["std"].values)
    t_km = sum_s["time_km"]["mean"].values

    ax1.errorbar(
        n_vals,
        t_icc,
        yerr=std_icc,
        fmt="o-",
        color="#d62728",
        ecolor="#d62728",
        capsize=3,
        label="ICC-v2 (O(N) Anchor Ensemble)",
        zorder=5,
    )
    ax1.errorbar(
        n_vals,
        t_mbk,
        yerr=std_mbk,
        fmt="s--",
        color="#1f77b4",
        ecolor="#1f77b4",
        capsize=3,
        label="MiniBatchKMeans (Batch=2k)",
        zorder=4,
    )

    valid_km = ~np.isnan(t_km)
    if np.any(valid_km):
        ax1.plot(
            n_vals[valid_km],
            t_km[valid_km],
            "^:",
            color="#7f7f7f",
            label="KMeans (Full Space, N <= 100k)",
            zorder=3,
        )

    # Theoretical O(N) linear reference line anchored at first ICC point
    ref_x = np.array([n_vals[0], n_vals[-1]])
    ref_y = t_icc[0] * (ref_x / ref_x[0])
    ax1.plot(ref_x, ref_y, "k--", alpha=0.5, linewidth=1.2, label=r"Theoretical $\mathcal{O}(N)$ Slope")

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel("Sample Size $N$ (Log Scale, up to $10^6$)", fontsize=12.0, fontweight="bold")
    ax1.set_ylabel("Wall-Clock Time [s] (Log Scale)", fontsize=12.0, fontweight="bold")
    ax1.tick_params(labelsize=11.0)
    ax1.set_title("(a) Massive Sample Complexity Scaling ($D=100, K=5$)", fontsize=13.0, fontweight="bold")
    ax1.grid(True, which="both", linestyle=":", alpha=0.5)
    ax1.legend(loc="upper left", fontsize=10.5)

    # =========================================================================
    # Panel (b): Peak Memory vs N
    # =========================================================================
    ax2 = axes[0, 1]
    m_icc = df_s.groupby("N")["mem_icc_mb"].mean().values
    m_mbk = df_s.groupby("N")["mem_mbk_mb"].mean().values

    ax2.plot(n_vals, m_icc, "o-", color="#d62728", linewidth=2.2, markersize=7, label="ICC-v2 Peak Memory")
    ax2.plot(n_vals, m_mbk, "s--", color="#1f77b4", linewidth=2.2, markersize=7, label="MiniBatchKMeans Peak Memory")

    if "mem_km_mb" in df_s.columns:
        m_km = df_s.groupby("N")["mem_km_mb"].mean().values
        valid_mkm = ~np.isnan(m_km)
        if np.any(valid_mkm):
            ax2.plot(n_vals[valid_mkm], m_km[valid_mkm], "^:", color="#7f7f7f", linewidth=1.8, markersize=6, label="KMeans Peak Memory")

    ax2.set_xlabel("Sample Size $N$ ($10^3$ to $10^6$)", fontsize=12.0, fontweight="bold")
    ax2.set_ylabel("Peak RAM Allocation [MB]", fontsize=12.0, fontweight="bold")
    ax2.tick_params(labelsize=11.0)
    ax2.set_title(r"(b) Memory Footprint Scaling (Linear $\mathcal{O}(N)$)", fontsize=13.0, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(loc="upper left", fontsize=10.5)

    # Format x-axis with comma separators or scientific notation
    ax2.set_xticks(n_vals)
    ax2.set_xticklabels([f"{int(v/1000)}k" if v < 1000000 else "1M" for v in n_vals], fontsize=11.0, fontweight="bold")

    # =========================================================================
    # Panel (c): Runtime vs D (up to D=100,000)
    # =========================================================================
    ax3 = axes[1, 0]
    sum_d = df_d.groupby("D").agg({
        "time_icc": ["mean", "std"],
        "time_km": ["mean", "std"],
        "time_pca": ["mean", "std"],
    }).reset_index()

    d_vals = sum_d["D"].values
    td_icc = sum_d["time_icc"]["mean"].values
    td_km = sum_d["time_km"]["mean"].values
    td_pca = sum_d["time_pca"]["mean"].values

    ax3.plot(d_vals, td_icc, "o-", color="#d62728", linewidth=2.2, markersize=7, label="ICC-v2 (BGSS Gating)")
    ax3.plot(d_vals, td_km, "^:", color="#7f7f7f", linewidth=1.8, markersize=6, label="KMeans (Full Space)")
    ax3.plot(d_vals, td_pca, "d-.", color="#2ca02c", linewidth=2.0, markersize=6, label="PCA + KMeans (d=10)")

    ax3.set_xlabel("Feature Dimension $D$ (up to $100{,}000$, $N=1{,}000$)", fontsize=12.0, fontweight="bold")
    ax3.set_ylabel("Execution Time [s]", fontsize=12.0, fontweight="bold")
    ax3.tick_params(labelsize=11.0)
    ax3.set_title("(c) Ultra-High-Dimension Runtime Scaling ($K=3$)", fontsize=13.0, fontweight="bold")
    ax3.grid(True, linestyle=":", alpha=0.5)
    ax3.legend(loc="upper left", fontsize=10.5)
    ax3.set_xticks(d_vals)
    ax3.set_xticklabels([f"{int(v/1000)}k" for v in d_vals], fontsize=11.0, fontweight="bold")

    # =========================================================================
    # Panel (d): Clustering Recovery (ARI) vs N
    # =========================================================================
    ax4 = axes[1, 1]
    ari_icc = df_s.groupby("N")["ari_icc"].mean().values
    std_ari_icc = np.nan_to_num(df_s.groupby("N")["ari_icc"].std().values)
    ari_mbk = df_s.groupby("N")["ari_mbk"].mean().values
    std_ari_mbk = np.nan_to_num(df_s.groupby("N")["ari_mbk"].std().values)

    ax4.errorbar(
        n_vals,
        ari_icc,
        yerr=std_ari_icc,
        fmt="o-",
        color="#d62728",
        ecolor="#d62728",
        linewidth=2.2,
        markersize=7,
        capsize=4,
        label="ICC-v2 Cluster Recovery",
    )
    ax4.errorbar(
        n_vals,
        ari_mbk,
        yerr=std_ari_mbk,
        fmt="s--",
        color="#1f77b4",
        ecolor="#1f77b4",
        linewidth=2.0,
        markersize=6,
        capsize=4,
        label="MiniBatchKMeans Recovery",
    )

    if "ari_km" in df_s.columns:
        ari_km = df_s.groupby("N")["ari_km"].mean().values
        valid_akm = ~np.isnan(ari_km)
        if np.any(valid_akm):
            ax4.plot(n_vals[valid_akm], ari_km[valid_akm], "^:", color="#7f7f7f", linewidth=1.8, markersize=6, label="KMeans Recovery")

    ax4.set_xlabel("Sample Size $N$ ($10^3$ to $10^6$)", fontsize=12.0, fontweight="bold")
    ax4.set_ylabel("Clustering Quality (ARI)", fontsize=12.0, fontweight="bold")
    ax4.tick_params(labelsize=11.0)
    ax4.set_title("(d) Asymptotic Quality Preservation ($K=5$)", fontsize=13.0, fontweight="bold")
    ax4.set_ylim(-0.05, 1.05)
    ax4.grid(True, linestyle=":", alpha=0.5)
    ax4.legend(loc="center right", fontsize=10.5)
    ax4.set_xticks(n_vals)
    ax4.set_xticklabels([f"{int(v/1000)}k" if v < 1000000 else "1M" for v in n_vals], fontsize=11.0, fontweight="bold")

    clean_spines(ax1)
    clean_spines(ax2)
    clean_spines(ax3)
    clean_spines(ax4)

    fig.tight_layout()
    if save_path is None:
        save_path = FIGURES_DIR / "fig26_extreme_scale_quad.png"
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved 2x2 panel scaling figure to: {save_path}")


def generate_all_plots():
    plot_extreme_scale_quad()


if __name__ == "__main__":
    generate_all_plots()
