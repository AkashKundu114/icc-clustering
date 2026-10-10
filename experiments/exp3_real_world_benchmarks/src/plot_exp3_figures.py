"""
Publication figure generator for Experiment 3 (Real-World High-Dimensional Benchmarks).
Produces Figures 14, 15, 16, and 17 adhering strictly to IEEE Transactions formatting guidelines.
"""

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Add project root to sys.path
root_dir = Path(__file__).resolve().parents[3]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.icc.viz_style import set_academic_style, clean_spines

set_academic_style()

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "exp3_benchmark_results.csv")
FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "figures")
os.makedirs(FIG_DIR, exist_ok=True)

MODEL_PALETTE = {
    "K-Means": "#7f7f7f",            # Gray
    "Ward": "#bcbd22",               # Olive
    "Spectral": "#17becf",           # Cyan
    "FCM": "#e377c2",                # Pink
    "Standard_Consensus": "#1f77b4",  # Blue
    "Li_et_al_2019": "#ff7f0e",       # Orange
    "ICC_v1": "#2ca02c",             # Light Green
    "ICC_v2": "#d62728"              # Crimson Red (Hero)
}

MODEL_LABELS = {
    "K-Means": "K-Means",
    "Ward": "Ward",
    "Spectral": "Spectral",
    "FCM": "FCM",
    "Standard_Consensus": "Std Consensus",
    "Li_et_al_2019": "Li et al. (2019)",
    "ICC_v1": "ICC-v1 (Anchor)",
    "ICC_v2": "ICC-v2 (VSSG+Anchor)"
}


def plot_grouped_metric(df, metric_col, title, ylabel, filename):
    datasets = ["sonar", "madelon", "colon", "leukemia"]
    dataset_titles = [
        "Sonar (D=60)",
        "Madelon (D=500)",
        "Colon (D=2,000)",
        "Leukemia (D=7,129)"
    ]
    models = list(MODEL_PALETTE.keys())
    
    n_datasets = len(datasets)
    n_models = len(models)
    
    fig, ax = plt.subplots(figsize=(10, 4.8))
    
    bar_width = 0.88 / n_models
    x_indices = np.arange(n_datasets)
    
    for m_idx, mname in enumerate(models):
        means = []
        stds = []
        for dname in datasets:
            sub = df[(df["dataset"] == dname) & (df["model"] == mname)]
            means.append(sub[metric_col].mean())
            stds.append(sub[metric_col].std())
            
        offset = (m_idx - n_models / 2.0 + 0.5) * bar_width
        color = MODEL_PALETTE[mname]
        edgecolor = "black" if "ICC" in mname else "none"
        linewidth = 1.0 if "ICC" in mname else 0.5
        
        ax.bar(
            x_indices + offset,
            means,
            yerr=stds,
            width=bar_width,
            label=MODEL_LABELS[mname],
            color=color,
            edgecolor=edgecolor,
            linewidth=linewidth,
            capsize=2,
            error_kw={"elinewidth": 0.8, "alpha": 0.7}
        )
        
    ax.set_xticks(x_indices)
    ax.set_xticklabels(dataset_titles, fontweight="bold")
    ax.set_ylabel(ylabel, fontweight="bold")
    ax.set_title(title, fontweight="bold", pad=12)
    ax.grid(axis="y", alpha=0.4, linestyle=":")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="-")
    ax.legend(ncol=4, loc="upper left", framealpha=0.9, edgecolor="gray")
    clean_spines(ax)
    
    plt.tight_layout()
    save_path = os.path.join(FIG_DIR, filename)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[+] Saved: {save_path}")


def plot_runtime_scalability(df):
    """Figure 16: Consensus Runtime & Linear Scaling Verification."""
    consensus_models = ["Standard_Consensus", "Li_et_al_2019", "ICC_v1", "ICC_v2"]
    
    datasets = ["colon", "leukemia", "sonar", "madelon"]
    # Sort datasets by N: Colon (62), Leukemia (72), Sonar (208), Madelon (500)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))
    
    # Left subplot: Execution time by dataset
    for mname in consensus_models:
        means = []
        sample_sizes = []
        for dname in datasets:
            sub = df[(df["dataset"] == dname) & (df["model"] == mname)]
            means.append(sub["elapsed_sec"].mean() * 1000.0) # convert to ms
            sample_sizes.append(sub["N"].iloc[0])
            
        ax1.plot(sample_sizes, means, marker="o", label=MODEL_LABELS[mname], color=MODEL_PALETTE[mname], linewidth=2.0)
        
    ax1.set_xlabel("Sample Size (N)", fontweight="bold")
    ax1.set_ylabel("Execution Time (milliseconds)", fontweight="bold")
    ax1.set_title("(a) Consensus Runtime Scaling vs N", fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(loc="upper left")
    
    # Right subplot: Number of Core Anchors (Lc) retained
    for mname in ["Li_et_al_2019", "ICC_v1", "ICC_v2"]:
        anchor_means = []
        labels_list = []
        for dname in datasets:
            sub = df[(df["dataset"] == dname) & (df["model"] == mname)]
            anchor_means.append(sub["lc"].mean())
            labels_list.append(f"{dname.capitalize()}\n(N={sub['N'].iloc[0]})")
            
        ax2.plot(range(len(datasets)), anchor_means, marker="s", label=MODEL_LABELS[mname], color=MODEL_PALETTE[mname], linewidth=2.0)
        
    ax2.set_xticks(range(len(datasets)))
    ax2.set_xticklabels(labels_list)
    ax2.set_xlabel("Benchmark Dataset", fontweight="bold")
    ax2.set_ylabel(r"Number of Core Anchors ($L_c$)", fontweight="bold")
    ax2.set_title(r"(b) Effective Anchor Sparsification ($L_c \ll N$)", fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(loc="upper left")
    clean_spines(ax1)
    clean_spines(ax2)
    
    plt.tight_layout()
    save_path = os.path.join(FIG_DIR, "fig16_runtime_scalability.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[+] Saved: {save_path}")


def plot_summary_ranking(df):
    """Figure 17: Average Performance and Rank across All Real-World Benchmarks."""
    models = list(MODEL_PALETTE.keys())
    
    summary = df.groupby(["dataset", "model"])[["ari", "nmi"]].mean().reset_index()
    
    # Compute average rank (1 = best) per dataset
    summary["rank_ari"] = summary.groupby("dataset")["ari"].rank(ascending=False)
    summary["rank_nmi"] = summary.groupby("dataset")["nmi"].rank(ascending=False)
    
    overall = summary.groupby("model").agg({
        "ari": "mean",
        "nmi": "mean",
        "rank_ari": "mean"
    }).loc[models]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))
    
    # Bar chart of Mean Overall ARI across all 4 datasets
    colors = [MODEL_PALETTE[m] for m in models]
    y_pos = np.arange(len(models))
    
    ax1.barh(y_pos, overall["ari"], color=colors, edgecolor="black", alpha=0.85)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([MODEL_LABELS[m] for m in models], fontweight="bold")
    ax1.set_xlabel("Mean Adjusted Rand Index (ARI)", fontweight="bold")
    ax1.set_title("(a) Cross-Dataset Mean ARI Recovery", fontweight="bold")
    ax1.grid(axis="x", linestyle=":", alpha=0.5)
    
    # Bar chart of Average Ranking (lower is better)
    ax2.barh(y_pos, overall["rank_ari"], color=colors, edgecolor="black", alpha=0.85)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([MODEL_LABELS[m] for m in models], fontweight="bold")
    ax2.set_xlabel("Average Rank across Datasets (1 = Best)", fontweight="bold")
    ax2.set_title("(b) Average Performance Ranking", fontweight="bold")
    ax2.invert_xaxis()  # Invert so lower ranks (1st place) extend further right
    ax2.grid(axis="x", linestyle=":", alpha=0.5)
    
    clean_spines(ax1)
    clean_spines(ax2)
    
    plt.tight_layout()
    save_path = os.path.join(FIG_DIR, "fig17_dataset_radar_summary.png")
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"[+] Saved: {save_path}")


def generate_all_figures():
    if not os.path.exists(DATA_PATH):
        print(f"[!] Data file not found: {DATA_PATH}. Run run_benchmark.py first.")
        return
        
    df = pd.read_csv(DATA_PATH)
    print(f"[*] Loaded benchmark data: {len(df)} records")
    
    plot_grouped_metric(
        df,
        metric_col="ari",
        title="Figure 14: Clustering Recovery (ARI) Across Real-World High-Dimensional Benchmarks",
        ylabel="Adjusted Rand Index (ARI)",
        filename="fig14_benchmark_ari_comparison.png"
    )
    
    plot_grouped_metric(
        df,
        metric_col="nmi",
        title="Figure 15: Information-Theoretic Recovery (NMI) Across High-Dimensional Benchmarks",
        ylabel="Normalized Mutual Information (NMI)",
        filename="fig15_benchmark_nmi_comparison.png"
    )
    
    plot_runtime_scalability(df)
    plot_summary_ranking(df)


if __name__ == "__main__":
    generate_all_figures()
