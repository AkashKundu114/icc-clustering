"""
Plotting module for Experiment 2.1: VSSG Interpretability and Feature Selection Audit.
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


def plot_madelon_pr():
    csv_file = DATA_DIR / "exp2_1_madelon_pr.csv"
    if not csv_file.exists():
        print(f"[!] {csv_file} not found. Run simulation first.")
        return

    df = pd.read_csv(csv_file)
    summary = df.groupby("K_cutoff").agg({
        "precision": ["mean", "std"],
        "recall": ["mean", "std"],
    }).reset_index()

    k_vals = summary["K_cutoff"].values
    prec_mean = summary["precision"]["mean"].values
    prec_std = summary["precision"]["std"].values
    rec_mean = summary["recall"]["mean"].values
    rec_std = summary["recall"]["std"].values

    fig, ax1 = plt.subplots(figsize=(6.5, 4.5), dpi=300)

    color_prec = "#1f77b4"
    color_rec = "#d62728"

    ax1.set_xlabel("Feature Selection Cutoff $K$ (Candidate Pool Size)")
    ax1.set_ylabel("Precision@K", color=color_prec)
    line1 = ax1.plot(k_vals, prec_mean, marker="o", color=color_prec, label="Precision@K")
    ax1.fill_between(k_vals, prec_mean - prec_std, prec_mean + prec_std, color=color_prec, alpha=0.15)
    ax1.tick_params(axis="y", labelcolor=color_prec)
    ax1.set_ylim(-0.05, 1.05)
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Recall@K (Fraction of 20 Informative)", color=color_rec)
    line2 = ax2.plot(k_vals, rec_mean, marker="s", color=color_rec, linestyle="--", label="Recall@K")
    ax2.fill_between(k_vals, rec_mean - rec_std, rec_mean + rec_std, color=color_rec, alpha=0.15)
    ax2.tick_params(axis="y", labelcolor=color_rec)
    ax2.set_ylim(-0.05, 1.05)

    # Informative marker
    ax1.axvline(x=20, color="gray", linestyle=":", label="True $K=20$ Cutoff")

    lines = line1 + line2 + [plt.Line2D([0], [0], color="gray", linestyle=":", label="True $K=20$")]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="center right")

    plt.title("VSSG Feature Recovery on Madelon ($D=500, K_{\\text{true}}=20$)")
    fig.tight_layout()
    out_path = FIGURES_DIR / "fig22a_vssg_madelon_pr.png"
    plt.savefig(out_path, dpi=300)
    plt.savefig(FIGURES_DIR / "figA_vssg_madelon_pr.png", dpi=300)
    plt.close()
    print(f"[+] Saved {out_path} and figA_vssg_madelon_pr.png")


def plot_synthetic_pr():
    csv_file = DATA_DIR / "exp2_1_synthetic_10kd_pr.csv"
    if not csv_file.exists():
        print(f"[!] {csv_file} not found.")
        return

    df = pd.read_csv(csv_file)
    summary = df.groupby("K_cutoff").agg({
        "precision": ["mean", "std"],
        "recall": ["mean", "std"],
    }).reset_index()

    k_vals = summary["K_cutoff"].values
    prec_mean = summary["precision"]["mean"].values
    prec_std = summary["precision"]["std"].values
    rec_mean = summary["recall"]["mean"].values
    rec_std = summary["recall"]["std"].values

    fig, ax1 = plt.subplots(figsize=(6.5, 4.5), dpi=300)

    color_prec = "#2ca02c"
    color_rec = "#ff7f0e"

    ax1.set_xlabel("Feature Selection Cutoff $K$ (Candidate Pool Size)")
    ax1.set_ylabel("Precision@K", color=color_prec)
    line1 = ax1.plot(k_vals, prec_mean, marker="^", color=color_prec, label="Precision@K")
    ax1.fill_between(k_vals, prec_mean - prec_std, prec_mean + prec_std, color=color_prec, alpha=0.15)
    ax1.tick_params(axis="y", labelcolor=color_prec)
    ax1.set_ylim(-0.05, 1.05)
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Recall@K (Fraction of 50 Signal)", color=color_rec)
    line2 = ax2.plot(k_vals, rec_mean, marker="D", color=color_rec, linestyle="--", label="Recall@K")
    ax2.fill_between(k_vals, rec_mean - rec_std, rec_mean + rec_std, color=color_rec, alpha=0.15)
    ax2.tick_params(axis="y", labelcolor=color_rec)
    ax2.set_ylim(-0.05, 1.05)

    ax1.axvline(x=50, color="gray", linestyle=":", label="True Signal $D=50$")

    lines = line1 + line2 + [plt.Line2D([0], [0], color="gray", linestyle=":", label="True Signal $D=50$")]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="center right")

    plt.title("VSSG Feature Recovery in Ultra-High-D ($D=10,000, D_{\\text{signal}}=50$)")
    fig.tight_layout()
    out_path = FIGURES_DIR / "fig22b_vssg_synthetic_pr.png"
    plt.savefig(out_path, dpi=300)
    plt.savefig(FIGURES_DIR / "figB_vssg_synthetic_pr.png", dpi=300)
    plt.close()
    print(f"[+] Saved {out_path} and figB_vssg_synthetic_pr.png")


def plot_noise_sweep():
    csv_file = DATA_DIR / "exp2_1_noise_sweep_pr.csv"
    if not csv_file.exists():
        print(f"[!] {csv_file} not found.")
        return

    df = pd.read_csv(csv_file)
    # Check column names (support recall_at_50 or recall_at_k)
    k_col = "recall_at_50" if "recall_at_50" in df.columns else "recall_at_k"
    k2_col = "recall_at_2k" if "recall_at_2k" in df.columns else k_col

    summary = df.groupby("d_noise").agg({
        k_col: ["mean", "std"],
        k2_col: ["mean", "std"],
    }).reset_index()

    d_noise = summary["d_noise"].values
    rec_k_mean = summary[k_col]["mean"].values
    rec_k_std = summary[k_col]["std"].values
    rec_2k_mean = summary[k2_col]["mean"].values
    rec_2k_std = summary[k2_col]["std"].values

    fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)

    ax.plot(d_noise, rec_k_mean, marker="o", color="#1f77b4", label="Recall@50 ($K = D_{\\text{signal}}$)")
    ax.fill_between(d_noise, rec_k_mean - rec_k_std, rec_k_mean + rec_k_std, color="#1f77b4", alpha=0.15)

    ax.plot(d_noise, rec_2k_mean, marker="s", color="#2ca02c", linestyle="--", label="Recall@100 ($K = 2 \\times D_{\\text{signal}}$)")
    ax.fill_between(d_noise, rec_2k_mean - rec_2k_std, rec_2k_mean + rec_2k_std, color="#2ca02c", alpha=0.15)

    ax.set_xlabel("Noise Feature Dimension $D_{\\text{noise}}$")
    ax.set_ylabel("Signal Feature Recall")
    ax.set_title("VSSG Signal Recovery vs Noise Dimension ($D_{\\text{signal}}=50$)")
    ax.set_ylim(0.0, 1.05)
    ax.grid(True)
    ax.legend(loc="lower left")

    fig.tight_layout()
    out_path = FIGURES_DIR / "fig22c_vssg_noise_degradation.png"
    plt.savefig(out_path, dpi=300)
    plt.savefig(FIGURES_DIR / "figC_vssg_noise_degradation.png", dpi=300)
    plt.close()
    print(f"[+] Saved {out_path} and figC_vssg_noise_degradation.png")


def plot_trinity():
    """Generates a 3-panel consolidated IEEE figure."""
    m_csv = DATA_DIR / "exp2_1_madelon_pr.csv"
    s_csv = DATA_DIR / "exp2_1_synthetic_10kd_pr.csv"
    w_csv = DATA_DIR / "exp2_1_noise_sweep_pr.csv"

    if not (m_csv.exists() and s_csv.exists() and w_csv.exists()):
        print("[!] Cannot create trinity plot: Missing intermediate CSVs.")
        return

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8), dpi=300)

    # Panel A: Madelon
    df_m = pd.read_csv(m_csv)
    sum_m = df_m.groupby("K_cutoff").agg({"precision": ["mean", "std"], "recall": ["mean", "std"]}).reset_index()
    k_m = sum_m["K_cutoff"].values
    ax1 = axes[0]
    ax1.plot(k_m, sum_m["precision"]["mean"], "o-", color="#1f77b4", linewidth=2.2, markersize=7, label="Precision@K")
    ax1.fill_between(k_m, sum_m["precision"]["mean"] - sum_m["precision"]["std"], sum_m["precision"]["mean"] + sum_m["precision"]["std"], color="#1f77b4", alpha=0.15)
    ax1_r = ax1.twinx()
    ax1_r.plot(k_m, sum_m["recall"]["mean"], "s--", color="#d62728", linewidth=2.2, markersize=7, label="Recall@K")
    ax1_r.fill_between(k_m, sum_m["recall"]["mean"] - sum_m["recall"]["std"], sum_m["recall"]["mean"] + sum_m["recall"]["std"], color="#d62728", alpha=0.15)
    ax1.set_xlabel("Cutoff $K$", fontsize=12.0, fontweight="bold")
    ax1.set_ylabel("Precision@K", color="#1f77b4", fontsize=12.0, fontweight="bold")
    ax1_r.set_ylabel("Recall@K", color="#d62728", fontsize=12.0, fontweight="bold")
    ax1.tick_params(labelsize=11.0)
    ax1_r.tick_params(labelsize=11.0)
    ax1.set_title("(a) Madelon Benchmark ($D=500$)", fontsize=13.0, fontweight="bold")
    ax1.set_ylim(-0.05, 1.05)
    ax1_r.set_ylim(-0.05, 1.05)
    ax1.grid(True, linestyle=":", alpha=0.5)

    # Panel B: Synthetic 10kD
    df_s = pd.read_csv(s_csv)
    sum_s = df_s.groupby("K_cutoff").agg({"precision": ["mean", "std"], "recall": ["mean", "std"]}).reset_index()
    k_s = sum_s["K_cutoff"].values
    ax2 = axes[1]
    ax2.plot(k_s, sum_s["precision"]["mean"], "^-", color="#2ca02c", linewidth=2.2, markersize=7, label="Precision@K")
    ax2.fill_between(k_s, sum_s["precision"]["mean"] - sum_s["precision"]["std"], sum_s["precision"]["mean"] + sum_s["precision"]["std"], color="#2ca02c", alpha=0.15)
    ax2_r = ax2.twinx()
    ax2_r.plot(k_s, sum_s["recall"]["mean"], "D--", color="#ff7f0e", linewidth=2.2, markersize=7, label="Recall@K")
    ax2_r.fill_between(k_s, sum_s["recall"]["mean"] - sum_s["recall"]["std"], sum_s["recall"]["mean"] + sum_s["recall"]["std"], color="#ff7f0e", alpha=0.15)
    ax2.set_xlabel("Cutoff $K$", fontsize=12.0, fontweight="bold")
    ax2.set_ylabel("Precision@K", color="#2ca02c", fontsize=12.0, fontweight="bold")
    ax2_r.set_ylabel("Recall@K", color="#ff7f0e", fontsize=12.0, fontweight="bold")
    ax2.tick_params(labelsize=11.0)
    ax2_r.tick_params(labelsize=11.0)
    ax2.set_title("(b) Synthetic Manifold ($D=10{,}000$)", fontsize=13.0, fontweight="bold")
    ax2.set_ylim(-0.05, 1.05)
    ax2_r.set_ylim(-0.05, 1.05)
    ax2.grid(True, linestyle=":", alpha=0.5)

    # Panel C: Noise sweep
    df_w = pd.read_csv(w_csv)
    sum_w = df_w.groupby("d_noise").agg({"recall_at_k": ["mean", "std"], "recall_at_2k": ["mean", "std"]}).reset_index()
    d_n = sum_w["d_noise"].values
    ax3 = axes[2]
    ax3.plot(d_n, sum_w["recall_at_k"]["mean"], "o-", color="#1f77b4", linewidth=2.2, markersize=7, label="Recall@50 ($K=D_{\\text{sig}}$)")
    ax3.fill_between(d_n, sum_w["recall_at_k"]["mean"] - sum_w["recall_at_k"]["std"], sum_w["recall_at_k"]["mean"] + sum_w["recall_at_k"]["std"], color="#1f77b4", alpha=0.15)
    ax3.plot(d_n, sum_w["recall_at_2k"]["mean"], "s--", color="#2ca02c", linewidth=2.2, markersize=7, label="Recall@100 ($K=2D_{\\text{sig}}$)")
    ax3.fill_between(d_n, sum_w["recall_at_2k"]["mean"] - sum_w["recall_at_2k"]["std"], sum_w["recall_at_2k"]["mean"] + sum_w["recall_at_2k"]["std"], color="#2ca02c", alpha=0.15)
    ax3.set_xlabel("Noise Dimension $D_{\\text{noise}}$", fontsize=12.0, fontweight="bold")
    ax3.set_ylabel("Signal Recall", fontsize=12.0, fontweight="bold")
    ax3.tick_params(labelsize=11.0)
    ax3.set_title("(c) Noise Stress Degradation", fontsize=13.0, fontweight="bold")
    ax3.set_ylim(0.0, 1.05)
    ax3.legend(loc="lower left", fontsize=10.5)
    ax3.grid(True, linestyle=":", alpha=0.5)

    fig.tight_layout()
    out_path = FIGURES_DIR / "fig22_vssg_interpretability_trinity.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved consolidated {out_path}")


def generate_all_plots():
    plot_madelon_pr()
    plot_synthetic_pr()
    plot_noise_sweep()
    plot_trinity()


if __name__ == "__main__":
    generate_all_plots()
