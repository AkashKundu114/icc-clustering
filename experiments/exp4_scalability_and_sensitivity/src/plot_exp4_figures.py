"""
Publication figure generator for Experiment 4: Scalability & Sensitivity Analysis.
Generates Figures 18, 19, 20, and 21 following strict IEEE Transactions typography standards.
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

from icc.viz_style import set_academic_style, clean_spines

set_academic_style()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FIG_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

MODEL_PALETTE = {
    "Standard_Consensus": "#1f77b4",  # Blue
    "Li_et_al_2019": "#ff7f0e",       # Orange
    "ICC_v1": "#2ca02c",             # Green
    "ICC_v2": "#d62728"              # Crimson Red
}

MODEL_LABELS = {
    "Standard_Consensus": "Std Consensus O(N²)",
    "Li_et_al_2019": "Li et al. (2019) O(N²)",
    "ICC_v1": "Ungated AC (Anchor) O(N)",
    "ICC_v2": "GAC Pipeline (BGSS+Anchor) O(N)"
}


def plot_figure_18():
    """Sample Complexity Scaling: Runtime and Memory Footprint vs N."""
    csv_path = os.path.join(DATA_DIR, "exp4_sample_scaling_results.csv")
    if not os.path.exists(csv_path):
        print(f"[!] File not found: {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    summary = df.groupby(["N", "model"])[["runtime_sec", "peak_memory_mb"]].mean().reset_index()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.8), dpi=300)
    
    model_order = ["Standard_Consensus", "Li_et_al_2019", "ICC_v1", "ICC_v2"]
    styles = {
        "Standard_Consensus": {"color": "#1f77b4", "marker": "s", "ls": ":", "lw": 2.0},
        "Li_et_al_2019": {"color": "#ff7f0e", "marker": "^", "ls": "--", "lw": 2.0},
        "ICC_v1": {"color": "#2ca02c", "marker": "o", "ls": "-", "lw": 2.0},
        "ICC_v2": {"color": "#d62728", "marker": "d", "ls": "-", "lw": 2.6}
    }
    
    # Subplot (a): Log-log Runtime vs N
    for mname in model_order:
        sub = summary[summary["model"] == mname]
        ax1.plot(
            sub["N"],
            sub["runtime_sec"],
            marker=styles[mname]["marker"],
            label=MODEL_LABELS[mname],
            color=styles[mname]["color"],
            linestyle=styles[mname]["ls"],
            linewidth=styles[mname]["lw"],
            markersize=7
        )
        
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xticks([200, 500, 1000, 2000, 5000, 8000, 10000])
    ax1.set_xticklabels(["200", "500", "1k", "2k", "5k", "8k", "10k"], fontsize=10.5, fontweight="bold")
    ax1.xaxis.set_minor_formatter(ticker.NullFormatter())
    ax1.tick_params(axis="y", labelsize=11.0)
    ax1.set_xlabel("Sample Size (N)", fontsize=12.0, fontweight="bold")
    ax1.set_ylabel("Execution Time (seconds, log scale)", fontsize=12.0, fontweight="bold")
    ax1.set_title(r"(a) Consensus Execution Runtime Scaling", fontsize=13.0, fontweight="bold")
    ax1.grid(True, which="both", linestyle=":", alpha=0.5)
    ax1.legend(loc="upper left", fontsize=10.5, framealpha=0.92, facecolor="white", edgecolor="#cccccc")
    
    # Annotation on runtime
    ax1.annotate("GAC Pipeline: 1.9x speedup at N=10,000\n(2.3s vs. 4.4s, 0.96s pure)",
                 xy=(10000, 2.30), xytext=(1200, 0.5),
                 arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.3),
                 fontsize=9.0, fontweight="bold", color="#d62728",
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="#fff0f0", edgecolor="#d62728", alpha=0.9))
    
    # Subplot (b): Log-log Peak Memory vs N
    for mname in model_order:
        sub = summary[summary["model"] == mname]
        ax2.plot(
            sub["N"],
            sub["peak_memory_mb"],
            marker=styles[mname]["marker"],
            label=MODEL_LABELS[mname],
            color=styles[mname]["color"],
            linestyle=styles[mname]["ls"],
            linewidth=styles[mname]["lw"],
            markersize=7
        )
        
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xticks([200, 500, 1000, 2000, 5000, 8000, 10000])
    ax2.set_xticklabels(["200", "500", "1k", "2k", "5k", "8k", "10k"], fontsize=10.5, fontweight="bold")
    ax2.xaxis.set_minor_formatter(ticker.NullFormatter())
    ax2.tick_params(axis="y", labelsize=11.0)
    ax2.set_xlabel("Sample Size (N)", fontsize=12.0, fontweight="bold")
    ax2.set_ylabel("Peak Memory Footprint (MB, log scale)", fontsize=12.0, fontweight="bold")
    ax2.set_title(r"(b) Memory Footprint Scaling $\mathcal{O}(N L_c)$ vs $\mathcal{O}(N^2)$", fontsize=13.0, fontweight="bold")
    ax2.grid(True, which="both", linestyle=":", alpha=0.5)
    # Annotation on memory savings
    ax2.annotate("-97.4% Peak Memory at N=10,000\n(68.8 MB vs. 2,671 MB)",
                 xy=(10000, 68.83), xytext=(1100, 8.0),
                 arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.3),
                 fontsize=9.0, fontweight="bold", color="#d62728",
                 bbox=dict(boxstyle="round,pad=0.25", facecolor="#fff0f0", edgecolor="#d62728", alpha=0.9))
    
    clean_spines(ax1)
    clean_spines(ax2)
    
    plt.tight_layout()
    save_path = os.path.join(FIG_DIR, "fig18_sample_complexity_scaling.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    for tdir in [root_dir / "springer_manuscript" / "figures",
                 root_dir / "paper" / "figures",
                 root_dir / "manuscript" / "figures"]:
        if tdir.exists():
            plt.savefig(tdir / "fig18_sample_complexity_scaling.png", dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved: {save_path}")


def plot_figure_19():
    """Dimension Scaling vs D in [100, 20000]."""
    csv_path = os.path.join(DATA_DIR, "exp4_dim_scaling_results.csv")
    if not os.path.exists(csv_path):
        print(f"[!] File not found: {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    summary = df.groupby(["D", "model"])[["runtime_sec"]].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(7.5, 4.6), dpi=300)
    
    model_order = ["Standard_Consensus", "Li_et_al_2019", "ICC_v1", "ICC_v2"]
    styles = {
        "Standard_Consensus": {"color": "#1f77b4", "marker": "s", "ls": ":", "lw": 2.0},
        "Li_et_al_2019": {"color": "#ff7f0e", "marker": "^", "ls": "--", "lw": 2.0},
        "ICC_v1": {"color": "#2ca02c", "marker": "o", "ls": "-", "lw": 2.0},
        "ICC_v2": {"color": "#d62728", "marker": "d", "ls": "-", "lw": 2.6}
    }
    
    for mname in model_order:
        sub = summary[summary["model"] == mname]
        ax.plot(
            sub["D"],
            sub["runtime_sec"],
            marker=styles[mname]["marker"],
            label=MODEL_LABELS[mname],
            color=styles[mname]["color"],
            linestyle=styles[mname]["ls"],
            linewidth=styles[mname]["lw"],
            markersize=7
        )
        
    ax.set_xscale("log")
    ax.set_xticks([100, 500, 2000, 5000, 10000, 20000])
    ax.set_xticklabels(["100", "500", "2k", "5k", "10k", "20k"], fontsize=11.0, fontweight="bold")
    ax.tick_params(axis="y", labelsize=11.0)
    ax.set_xlabel("Feature Dimensionality (D, log scale)", fontsize=12.0, fontweight="bold")
    ax.set_ylabel("Execution Time (seconds)", fontsize=12.0, fontweight="bold")
    ax.set_title("Execution Runtime vs Feature Dimension D (N=500)", fontsize=13.0, fontweight="bold")
    ax.grid(True, which="both", linestyle=":", alpha=0.5)
    ax.legend(loc="upper left", fontsize=10.5, framealpha=0.92, facecolor="white", edgecolor="#cccccc")
    
    # Callout annotation at D=20,000 (placed in top center to avoid crossing curves)
    ax.annotate("BGSS Feature Gating:\n36.7% faster runtime at D=20,000\n(0.96s vs 1.52s)",
                xy=(20000, 0.964), xytext=(700, 1.15),
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.3),
                fontsize=9.5, fontweight="bold", color="#d62728",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#fff0f0", edgecolor="#d62728", alpha=0.9))
    
    clean_spines(ax)
    plt.tight_layout()
    save_path = os.path.join(FIG_DIR, "fig19_dimension_scaling.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved: {save_path}")


def plot_figure_20():
    """Ensemble Size Convergence Plateau."""
    csv_path = os.path.join(DATA_DIR, "exp4_sensitivity_results.csv")
    if not os.path.exists(csv_path):
        print(f"[!] File not found: {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    sub = df[df["sweep_type"] == "ensemble_size_M"]
    summary = sub.groupby("param_value").agg({
        "ari": ["mean", "std"],
        "nmi": ["mean", "std"]
    }).reset_index()
    
    M_vals = summary["param_value"].values
    ari_mean = summary["ari"]["mean"].values
    ari_std = summary["ari"]["std"].values
    nmi_mean = summary["nmi"]["mean"].values
    nmi_std = summary["nmi"]["std"].values
    
    fig, ax = plt.subplots(figsize=(7.5, 4.6), dpi=300)
    
    # Optimal regime shaded band
    ax.axvspan(25, 50, color="#2ca02c", alpha=0.12, label=r"Optimal Operating Regime ($M \in [25, 50]$)")
    
    ax.plot(M_vals, ari_mean, marker="o", color="#d62728", label="Mean ARI", linewidth=2.4, markersize=7)
    ax.fill_between(M_vals, np.clip(ari_mean - ari_std, 0.0, 1.0), np.clip(ari_mean + ari_std, 0.0, 1.0), color="#d62728", alpha=0.12)
    
    ax.plot(M_vals, nmi_mean, marker="s", color="#1f77b4", label="Mean NMI", linewidth=2.0, linestyle="--", markersize=6)
    ax.fill_between(M_vals, np.clip(nmi_mean - nmi_std, 0.0, 1.0), np.clip(nmi_mean + nmi_std, 0.0, 1.0), color="#1f77b4", alpha=0.12)
    
    ax.axvline(25, color="black", linestyle=":", linewidth=1.2)
    
    ax.annotate("Plateau Onset (M=25):\nReaches 95% of peak ARI",
                xy=(25, ari_mean[np.where(M_vals == 25)[0][0]]), xytext=(35, 0.55),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
                fontsize=9.5, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#f8f9fa", edgecolor="#6c757d", alpha=0.9))
    
    ax.set_xlabel("Ensemble Size M (Number of Subspace Base Clusterings)", fontsize=12.0, fontweight="bold")
    ax.set_ylabel("Clustering Recovery Score", fontsize=12.0, fontweight="bold")
    ax.tick_params(labelsize=11.0)
    ax.set_title("GAC Pipeline Performance Plateau vs Ensemble Size M", fontsize=13.0, fontweight="bold")
    ax.grid(True, linestyle=":", alpha=0.5)
    ax.set_ylim(0.25, 1.05)
    ax.legend(loc="lower right", fontsize=10.5, framealpha=0.92, facecolor="white", edgecolor="#cccccc")
    
    clean_spines(ax)
    plt.tight_layout()
    save_path = os.path.join(FIG_DIR, "fig20_ensemble_size_plateau.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved: {save_path}")


def plot_figure_21():
    """2D Hyperparameter Sensitivity Landscape Heatmaps."""
    csv_path = os.path.join(DATA_DIR, "exp4_sensitivity_results.csv")
    if not os.path.exists(csv_path):
        print(f"[!] File not found: {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.8, 4.8), dpi=300)
    
    # -------------------------------------------------------------------------
    # Panel (a): Candidate Anchors L vs Core Quantile tau
    # -------------------------------------------------------------------------
    sub_grid1 = df[df["sweep_type"] == "grid_L_vs_tau"]
    piv1 = sub_grid1.groupby(["param_value", "secondary_val"])["ari"].mean().unstack()
    
    cax1 = ax1.imshow(piv1.values, cmap="YlGnBu", aspect="auto", origin="lower", vmin=0.3, vmax=1.0)
    
    # Add contour isolines overlay
    try:
        X_grid, Y_grid = np.meshgrid(range(len(piv1.columns)), range(len(piv1.index)))
        ax1.contour(X_grid, Y_grid, piv1.values, levels=[0.80, 0.85], colors="#d62728", linewidths=1.5, linestyles="--")
    except Exception:
        pass
        
    ax1.set_xticks(range(len(piv1.columns)))
    ax1.set_xticklabels([f"{v:.2f}" for v in piv1.columns], fontsize=11.0, fontweight="bold")
    ax1.set_yticks(range(len(piv1.index)))
    ax1.set_yticklabels([str(int(v)) for v in piv1.index], fontsize=11.0, fontweight="bold")
    ax1.set_xlabel(r"Core Stability Threshold Quantile ($\tau_{\text{core}}$)", fontsize=12.0, fontweight="bold")
    ax1.set_ylabel(r"Candidate Anchors ($L$)", fontsize=12.0, fontweight="bold")
    ax1.set_title(r"(a) Robustness Plateau over $(L, \tau_{\text{core}})$", fontsize=13.0, fontweight="bold")
    
    for i in range(len(piv1.index)):
        for j in range(len(piv1.columns)):
            val = piv1.values[i, j]
            color = "white" if val > 0.75 else "black"
            ax1.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=9.5, fontweight="bold")
            
    cbar1 = fig.colorbar(cax1, ax=ax1)
    cbar1.set_label("Mean ARI", fontsize=11.0, fontweight="bold")
    cbar1.ax.tick_params(labelsize=10.0)
    
    # -------------------------------------------------------------------------
    # Panel (b): Ensemble Size M vs Beta
    # -------------------------------------------------------------------------
    sub_grid2 = df[df["sweep_type"] == "grid_M_vs_beta"]
    piv2 = sub_grid2.groupby(["param_value", "secondary_val"])["ari"].mean().unstack()
    
    cax2 = ax2.imshow(piv2.values, cmap="YlGnBu", aspect="auto", origin="lower", vmin=0.3, vmax=1.0)
    
    try:
        X_grid2, Y_grid2 = np.meshgrid(range(len(piv2.columns)), range(len(piv2.index)))
        ax2.contour(X_grid2, Y_grid2, piv2.values, levels=[0.80, 0.85], colors="#d62728", linewidths=1.5, linestyles="--")
    except Exception:
        pass
        
    ax2.set_xticks(range(len(piv2.columns)))
    ax2.set_xticklabels([f"{v:.1f}" for v in piv2.columns], fontsize=11.0, fontweight="bold")
    ax2.set_yticks(range(len(piv2.index)))
    ax2.set_yticklabels([str(int(v)) for v in piv2.index], fontsize=11.0, fontweight="bold")
    ax2.set_xlabel(r"Noise Decay Exponent ($\beta$)", fontsize=12.0, fontweight="bold")
    ax2.set_ylabel(r"Ensemble Size ($M$)", fontsize=12.0, fontweight="bold")
    ax2.set_title(r"(b) Robustness Plateau over $(M, \beta)$", fontsize=13.0, fontweight="bold")
    
    for i in range(len(piv2.index)):
        for j in range(len(piv2.columns)):
            val = piv2.values[i, j]
            color = "white" if val > 0.75 else "black"
            ax2.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=9.5, fontweight="bold")
            
    cbar2 = fig.colorbar(cax2, ax=ax2)
    cbar2.set_label("Mean ARI", fontsize=11.0, fontweight="bold")
    cbar2.ax.tick_params(labelsize=10.0)
    
    plt.suptitle("Hyperparameter Robustness Landscape Heatmaps (Red dashed = ARI 0.80/0.85 contour)",
                 fontweight="bold", fontsize=13.5, y=0.995)
    plt.tight_layout()
    save_path = os.path.join(FIG_DIR, "fig21_hyperparameter_sensitivity_map.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved: {save_path}")


def plot_figure_21_supp_nmi():
    """Supplementary 2D Hyperparameter Sensitivity Landscape Heatmaps for NMI."""
    csv_path = os.path.join(DATA_DIR, "exp4_sensitivity_results.csv")
    if not os.path.exists(csv_path):
        print(f"[!] File not found: {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    if "nmi" not in df.columns:
        print("[!] NMI column not found in sensitivity results.")
        return
        
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.6), dpi=300)
    
    # Panel (a): Candidate Anchors L vs Core Quantile tau (NMI)
    sub_grid1 = df[df["sweep_type"] == "grid_L_vs_tau"]
    piv1 = sub_grid1.groupby(["param_value", "secondary_val"])["nmi"].mean().unstack()
    
    cax1 = ax1.imshow(piv1.values, cmap="YlGnBu", aspect="auto", origin="lower", vmin=0.3, vmax=1.0)
    
    try:
        X_grid, Y_grid = np.meshgrid(range(len(piv1.columns)), range(len(piv1.index)))
        ax1.contour(X_grid, Y_grid, piv1.values, levels=[0.80, 0.85], colors="#d62728", linewidths=1.5, linestyles="--")
    except Exception:
        pass
        
    ax1.set_xticks(range(len(piv1.columns)))
    ax1.set_xticklabels([f"{v:.2f}" for v in piv1.columns])
    ax1.set_yticks(range(len(piv1.index)))
    ax1.set_yticklabels([str(int(v)) for v in piv1.index])
    ax1.set_xlabel(r"Core Stability Threshold Quantile ($\tau_{\text{core}}$)", fontweight="bold")
    ax1.set_ylabel(r"Candidate Anchors ($L$)", fontweight="bold")
    ax1.set_title(r"(a) NMI Plateau over $(L, \tau_{\text{core}})$", fontweight="bold")
    
    for i in range(len(piv1.index)):
        for j in range(len(piv1.columns)):
            val = piv1.values[i, j]
            color = "white" if val > 0.75 else "black"
            ax1.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=8.5, fontweight="bold")
            
    fig.colorbar(cax1, ax=ax1, label="Mean NMI")
    
    # Panel (b): Ensemble Size M vs Beta (NMI)
    sub_grid2 = df[df["sweep_type"] == "grid_M_vs_beta"]
    piv2 = sub_grid2.groupby(["param_value", "secondary_val"])["nmi"].mean().unstack()
    
    cax2 = ax2.imshow(piv2.values, cmap="YlGnBu", aspect="auto", origin="lower", vmin=0.3, vmax=1.0)
    
    try:
        X_grid2, Y_grid2 = np.meshgrid(range(len(piv2.columns)), range(len(piv2.index)))
        ax2.contour(X_grid2, Y_grid2, piv2.values, levels=[0.80, 0.85], colors="#d62728", linewidths=1.5, linestyles="--")
    except Exception:
        pass
        
    ax2.set_xticks(range(len(piv2.columns)))
    ax2.set_xticklabels([f"{v:.1f}" for v in piv2.columns])
    ax2.set_yticks(range(len(piv2.index)))
    ax2.set_yticklabels([str(int(v)) for v in piv2.index])
    ax2.set_xlabel(r"Noise Decay Exponent ($\beta$)", fontweight="bold")
    ax2.set_ylabel(r"Ensemble Size ($M$)", fontweight="bold")
    ax2.set_title(r"(b) NMI Plateau over $(M, \beta)$", fontweight="bold")
    
    for i in range(len(piv2.index)):
        for j in range(len(piv2.columns)):
            val = piv2.values[i, j]
            color = "white" if val > 0.75 else "black"
            ax2.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=8.5, fontweight="bold")
            
    fig.colorbar(cax2, ax=ax2, label="Mean NMI")
    
    plt.suptitle("Supplementary NMI Hyperparameter Robustness Landscape Heatmaps",
                 fontweight="bold", fontsize=11.5, y=0.99)
    plt.tight_layout()
    save_path = os.path.join(FIG_DIR, "fig21_supp_nmi_sensitivity_heatmaps.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved: {save_path}")


def generate_all_exp4_figures():
    print("[*] Generating Figure 18 (Sample Complexity Scaling)...")
    plot_figure_18()
    print("[*] Generating Figure 19 (Dimension Scaling)...")
    plot_figure_19()
    print("[*] Generating Figure 20 (Ensemble Plateau)...")
    plot_figure_20()
    print("[*] Generating Figure 21 (Sensitivity Maps)...")
    plot_figure_21()
    print("[*] Generating Supplementary Figure 21 (NMI Sensitivity Maps)...")
    plot_figure_21_supp_nmi()


if __name__ == "__main__":
    generate_all_exp4_figures()
