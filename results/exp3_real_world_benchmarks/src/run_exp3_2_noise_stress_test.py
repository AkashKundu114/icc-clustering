"""
Experiment 3.2: Real-World Noise Corruption Stress-Test.
Evaluates the graceful degradation of consensus algorithms as controlled Gaussian
feature noise is injected directly into real high-dimensional cancer microarrays:
- Leukemia (N=72, D=7,129)
- Colon (N=62, D=2,000)
- Prostate (N=102, D=12,600)
"""

import os
import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from experiments.exp3_real_world_benchmarks.src.dataset_loader import load_benchmark_dataset
from experiments.exp3_real_world_benchmarks.src.benchmark_models import (
    run_standard_consensus,
    run_li_et_al_2019,
    run_icc_v1,
    run_icc_v2
)
from src.icc.core import adjusted_rand_score, normalized_mutual_info_score

OUTPUT_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "exp3_2_noise_stress_test.csv")
FIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "figures", "fig15_noise_corruption_degradation.png")

NOISE_LEVELS = [0.0, 0.2, 0.5, 1.0, 2.0]
TARGET_DATASETS = ["leukemia", "colon", "prostate"]
MODELS = {
    "Standard_Consensus": run_standard_consensus,
    "Li_et_al_2019": run_li_et_al_2019,
    "ICC_v1": run_icc_v1,
    "ICC_v2": run_icc_v2
}


def run_sub_exp3_2(n_trials=5):
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    os.makedirs(os.path.dirname(FIG_PATH), exist_ok=True)
    
    print("=" * 80)
    print("RUNNING SUB-EXPERIMENT 3.2: REAL-WORLD NOISE CORRUPTION STRESS-TEST")
    print(f"Target Datasets: {TARGET_DATASETS}")
    print(f"Noise Variances: {NOISE_LEVELS}")
    print("=" * 80)
    
    records = []
    
    for dname in TARGET_DATASETS:
        print(f"\n---> Dataset: {dname.upper()}")
        X_clean, y, meta = load_benchmark_dataset(dname)
        N, D, K = meta["N"], meta["D"], meta["K"]
        
        for sigma in NOISE_LEVELS:
            for t_idx in range(n_trials):
                seed = 42 + t_idx * 17
                rng = np.random.default_rng(seed)
                
                # Inject controlled noise
                if sigma > 0:
                    noise = rng.normal(0.0, sigma, size=X_clean.shape)
                    X_noisy = X_clean + noise
                else:
                    X_noisy = X_clean.copy()
                    
                for mname, mfn in MODELS.items():
                    pred, elapsed, lc = mfn(X_noisy, K, seed=seed)
                    ari = adjusted_rand_score(y, pred)
                    nmi = normalized_mutual_info_score(y, pred)
                    
                    records.append({
                        "dataset": dname,
                        "noise_sigma": sigma,
                        "trial": t_idx,
                        "model": mname,
                        "ari": ari,
                        "nmi": nmi,
                        "elapsed_sec": elapsed,
                        "lc": lc
                    })
                    
            # Print intermediate summary
            sub = [r for r in records if r["dataset"] == dname and r["noise_sigma"] == sigma]
            df_sub = pd.DataFrame(sub)
            summary = df_sub.groupby("model")["ari"].mean().to_dict()
            print(f"     sigma={sigma:.1f}: " + " | ".join([f"{m}={summary[m]:.3f}" for m in summary]))
            
    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n[+] Results saved to: {OUTPUT_CSV}")
    
    plot_fig15_noise_degradation(df)
    return df


def plot_fig15_noise_degradation(df):
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 10.5,
        "axes.titlesize": 11.0,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 8.5,
        "figure.dpi": 300
    })
    
    model_styles = {
        "ICC_v2": {"color": "#d62728", "marker": "d", "ls": "-", "lw": 2.2, "label": "ICC-v2 (VSSG+Anchor) [Ours]"},
        "ICC_v1": {"color": "#2ca02c", "marker": "o", "ls": "-", "lw": 1.8, "label": "ICC-v1 (Calibrated Core)"},
        "Li_et_al_2019": {"color": "#ff7f0e", "marker": "^", "ls": "--", "lw": 1.8, "label": "Li et al. (2019)"},
        "Standard_Consensus": {"color": "#1f77b4", "marker": "s", "ls": ":", "lw": 1.8, "label": "Standard Consensus"}
    }
    
    dataset_meta_labels = {
        "leukemia": r"(a) Leukemia ($N=72, D=7,129, K=2$)",
        "colon": r"(b) Colon ($N=62, D=2,000, K=2$)",
        "prostate": r"(c) Prostate ($N=102, D=12,600, K=2$)"
    }
    
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.3), sharey=True)
    
    for ax_idx, dname in enumerate(TARGET_DATASETS):
        ax = axes[ax_idx]
        df_d = df[df["dataset"] == dname]
        
        # Plot in order of baselines first, then our models on top
        for mname in ["Standard_Consensus", "Li_et_al_2019", "ICC_v1", "ICC_v2"]:
            sub = df_d[df_d["model"] == mname]
            means = sub.groupby("noise_sigma")["ari"].mean()
            stds = sub.groupby("noise_sigma")["ari"].std()
            
            style = model_styles[mname]
            ax.plot(
                means.index, means.values,
                marker=style["marker"],
                label=style["label"],
                color=style["color"],
                linestyle=style["ls"],
                linewidth=style["lw"],
                markersize=6
            )
            ax.fill_between(
                means.index,
                means.values - stds.values,
                means.values + stds.values,
                color=style["color"],
                alpha=0.12
            )
            
        ax.set_xlabel(r"Injected Noise Variance ($\sigma_{\text{noise}}$)", fontweight="bold")
        if ax_idx == 0:
            ax.set_ylabel("Clustering Recovery (ARI)", fontweight="bold")
        ax.set_title(dataset_meta_labels[dname], fontweight="bold")
        ax.grid(True, linestyle=":", alpha=0.5)
        ax.axhline(0, color="black", linestyle="-", linewidth=0.7, alpha=0.7)
        ax.set_ylim(-0.25, 0.95)
        
        if ax_idx == 0:
            ax.legend(loc="upper right", framealpha=0.92, facecolor="white", edgecolor="#cccccc")
            
    plt.suptitle("Empirical Degradation Under Additive Noise Corruption on Cancer Microarrays",
                 fontweight="bold", fontsize=12.0, y=1.00)
    plt.tight_layout()
    plt.savefig(FIG_PATH, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved: {FIG_PATH}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--replot", action="store_true", help="Only replot from existing CSV")
    parser.add_argument("--trials", type=int, default=5, help="Number of trials per level")
    args = parser.parse_args()
    
    if args.replot and os.path.exists(OUTPUT_CSV):
        print(f"[*] Re-generating Figure 15 directly from {OUTPUT_CSV}...")
        df_existing = pd.read_csv(OUTPUT_CSV)
        plot_fig15_noise_degradation(df_existing)
    else:
        run_sub_exp3_2(n_trials=args.trials)
