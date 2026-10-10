"""
Experiment 3.1: Expanded Multi-Domain Benchmark Matrix (13 Datasets x 11 Models x 10 Trials).

Datasets (13 enabled):
1. Sonar (N=208, D=60, K=2) - Acoustic
2. Madelon (N=500, D=500, K=2) - Synthetic XOR + Distractor Noise
3. Colon (N=62, D=2,000, K=2) - Genomics
4. SRBCT (N=83, D=2,308, K=4) - Genomics
5. CNS (N=60, D=7,129, K=2) - Genomics
6. Leukemia (N=72, D=7,129, K=2) - Genomics
7. Prostate (N=102, D=12,600, K=2) - Genomics
8. Ovarian (N=253, D=15,154, K=2) - Mass Spectrometry
9. Newsgroups20 (N=18,846, D=10,000, K=20) - TF-IDF Text
10. Isolet (N=7,797, D=617, K=26) - Spoken Letter Audio
11. Indian Pines (N=10,249, D=200, K=16) - Hyperspectral Imaging
12. Yale B (N=2,414, D=1,024, K=38) - Face Biometrics
13. Zheng68k (N=700, D=765, K=10) - scRNA-seq Profiling

Models (11 enabled):
- Classical Single: K-Means, Ward, Spectral, FCM
- Consensus/Ensemble: Standard_Consensus, Li_et_al_2019, ICC_v1, ICC_v2
- Deep Clustering: DEC
- Scalable Anchor-based: FCAG, FastMVC
"""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.icc.viz_style import set_academic_style, clean_spines

from experiments.exp3_real_world_benchmarks.src.benchmark_models import MODELS
from src.icc.datasets.registry import list_datasets, load_dataset
from src.icc.metrics import evaluate_all

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "figures")

ORIGINAL_CSV = os.path.join(DATA_DIR, "exp3_1_benchmark_matrix.csv")
OUTPUT_CSV_V2 = os.path.join(DATA_DIR, "exp3_1_benchmark_matrix_v2.csv")

FIG14_PATH_13DS = os.path.join(FIG_DIR, "fig14_benchmark_matrix_13datasets.png")
FIG14B_PATH_13DS_NMI = os.path.join(FIG_DIR, "fig14b_benchmark_matrix_13datasets_nmi.png")

# Backwards compatible paths
FIG_PATH_8DS = os.path.join(FIG_DIR, "fig14_benchmark_matrix_8datasets.png")
FIG_PATH_8DS_NMI = os.path.join(FIG_DIR, "fig14b_benchmark_matrix_nmi.png")

SEEDS = [42, 101, 202, 303, 404, 505, 606, 707, 808, 909]

MODEL_ORDER = [
    "K-Means",
    "Ward",
    "Spectral",
    "FCM",
    "Standard_Consensus",
    "Li_et_al_2019",
    "DEC",
    "FCAG",
    "FastMVC",
    "ICC_v1",
    "ICC_v2",
]

MODEL_COLORS = [
    "#7f7f7f",  # K-Means (Gray)
    "#bcbd22",  # Ward (Olive)
    "#17becf",  # Spectral (Cyan)
    "#e377c2",  # FCM (Pink)
    "#1f77b4",  # Standard Consensus (Blue)
    "#ff7f0e",  # Li et al. (Orange)
    "#9467bd",  # DEC (Purple)
    "#8c564b",  # FCAG (Brown)
    "#393b79",  # FastMVC (Dark Navy)
    "#2ca02c",  # ICC-v1 (Green)
    "#d62728",  # ICC-v2 (Crimson Hero)
]

MODEL_LABELS = [
    "K-Means",
    "Ward",
    "Spectral",
    "FCM",
    "Std Consensus",
    "Li et al. (2019)",
    "DEC (ICML 2016)",
    "FCAG (TPAMI 2024)",
    "FastMVC (TKDE 2023)",
    "ICC-v1 (Anchor)",
    "ICC-v2 (VSSG+Anchor)",
]

CSV_COLUMNS = [
    "dataset",
    "N",
    "D",
    "K",
    "model",
    "trial",
    "seed",
    "ari",
    "nmi",
    "ami",
    "v_measure",
    "fm_index",
    "elapsed_sec",
    "lc",
]


def seed_v2_from_original_if_needed(output_path: str, orig_path: str) -> pd.DataFrame:
    """Pre-seed v2 CSV with existing runs from original 8-dataset CSV if available."""
    if os.path.exists(output_path):
        try:
            df = pd.read_csv(output_path)
            if not df.empty:
                return df
        except Exception:
            pass

    if os.path.exists(orig_path):
        try:
            orig_df = pd.read_csv(orig_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            orig_df.to_csv(output_path, index=False)
            print(f"[+] Pre-seeded {output_path} with {len(orig_df)} completed runs from {orig_path}")
            return orig_df
        except Exception as e:
            print(f"[!] Warning: failed to pre-seed from {orig_path}: {e}")

    # Create empty dataframe with required schema
    df = pd.DataFrame(columns=CSV_COLUMNS)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


def generate_benchmark_tables(df: pd.DataFrame, output_dir: Optional[str] = None, suffix: str = "_v2"):
    """
    Generates summary tables formatted with mean ± std and cross-dataset average
    for all 5 clustering evaluation metrics: ARI, NMI, AMI, V-Measure, FM-Index.
    """
    if output_dir is None:
        output_dir = DATA_DIR
    os.makedirs(output_dir, exist_ok=True)

    datasets = sorted(df["dataset"].unique().tolist())
    models = [m for m in MODEL_ORDER if m in df["model"].unique()]

    metrics = ["ari", "nmi", "ami", "v_measure", "fm_index"]

    for metric in metrics:
        rows = []
        for dname in datasets:
            row = {"Dataset": dname.upper()}
            for m in models:
                sub = df[(df["dataset"] == dname) & (df["model"] == m)]
                if not sub.empty:
                    m_val = sub[metric].mean()
                    s_val = sub[metric].std()
                    row[m] = f"{m_val:.4f} ± {s_val:.4f}"
                else:
                    row[m] = "N/A"
            rows.append(row)

        # Cross-dataset average row
        avg_row = {"Dataset": "AVERAGE"}
        for m in models:
            sub = df[df["model"] == m]
            if not sub.empty:
                avg_row[m] = f"{sub[metric].mean():.4f}"
            else:
                avg_row[m] = "N/A"
        rows.append(avg_row)

        table_df = pd.DataFrame(rows)
        csv_file = os.path.join(output_dir, f"exp3_1_{metric}_table{suffix}.csv")
        table_df.to_csv(csv_file, index=False)

        tex_file = os.path.join(output_dir, f"exp3_1_{metric}_table{suffix}.tex")
        try:
            with open(tex_file, "w", encoding="utf-8") as f:
                f.write(table_df.to_latex(index=False))
        except Exception:
            pass
        print(f"[+] Saved {metric.upper()} table to: {csv_file}")


def plot_fig14_13datasets(df: pd.DataFrame, metric: str = "ari", save_path: Optional[str] = None):
    """
    Renders publication-ready 4x4 panel figure comparing all 11 clustering methods
    across all 13 multi-domain benchmark datasets plus cross-dataset summary.
    """
    if save_path is None:
        save_path = FIG14_PATH_13DS if metric == "ari" else FIG14B_PATH_13DS_NMI
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    set_academic_style()
    plt.rcParams.update({
        "font.size": 10.5,
        "axes.labelsize": 12.0,
        "axes.titlesize": 12.5,
        "xtick.labelsize": 10.0,
        "ytick.labelsize": 10.5,
        "figure.titlesize": 16.0,
    })

    # Available models ordered according to MODEL_ORDER
    available_models = [m for m in MODEL_ORDER if m in df["model"].unique()]
    palette = [MODEL_COLORS[MODEL_ORDER.index(m)] for m in available_models]
    labels = [MODEL_LABELS[MODEL_ORDER.index(m)] for m in available_models]

    datasets = sorted(df["dataset"].unique().tolist())
    n_datasets = len(datasets)

    fig, axes = plt.subplots(4, 4, figsize=(18, 14), sharey=True)
    axes_flat = axes.flatten()

    y_pos = np.arange(len(available_models))

    for i in range(16):
        ax = axes_flat[i]

        if i < n_datasets:
            dname = datasets[i]
            df_d = df[df["dataset"] == dname]

            # Extract dataset metadata from first row
            meta_n = int(df_d["N"].iloc[0]) if not df_d.empty else 0
            meta_d = int(df_d["D"].iloc[0]) if not df_d.empty else 0
            meta_k = int(df_d["K"].iloc[0]) if not df_d.empty else 0

            means = []
            stds = []
            for m in available_models:
                sub = df_d[df_d["model"] == m]
                means.append(sub[metric].mean() if not sub.empty else 0.0)
                stds.append(sub[metric].std() if not sub.empty else 0.0)

            means = np.nan_to_num(np.array(means))
            stds = np.nan_to_num(np.array(stds))

            bars = ax.barh(
                y_pos,
                means,
                xerr=stds,
                color=palette,
                edgecolor=["black" if "ICC" in m else "none" for m in available_models],
                linewidth=[1.0 if "ICC" in m else 0.5 for m in available_models],
                height=0.68,
                capsize=2,
                error_kw={"elinewidth": 0.7, "alpha": 0.7},
            )

            # Annotate values
            for j, val in enumerate(means):
                offset = 0.015 if val >= 0 else -0.015
                ha = "left" if val >= 0 else "right"
                ax.text(
                    val + offset,
                    j,
                    f"{val:.3f}",
                    va="center",
                    ha=ha,
                    fontsize=8.5,
                    fontweight="bold" if "ICC_v2" in available_models[j] else "normal",
                    color="#a00000" if "ICC_v2" in available_models[j] else "#222222",
                )

            d_title = f"({chr(97 + i)}) {dname.upper()} (N={meta_n}, D={meta_d}, K={meta_k})"
            ax.set_title(d_title, fontweight="bold", pad=4)
            ax.axvline(0, color="black", linestyle="-", linewidth=0.8, alpha=0.8)
            ax.grid(axis="x", linestyle=":", alpha=0.5)

            x_min = min(-0.06, np.min(means - stds) - 0.08)
            x_max = max(0.15, np.max(means + stds) + 0.12)
            ax.set_xlim(x_min, x_max)
            clean_spines(ax)

        elif i == n_datasets:
            # Cross-Dataset Grand Mean Panel
            ax.set_title("(n) Cross-Dataset Grand Mean", fontweight="bold", pad=4)
            avg_means = []
            for m in available_models:
                sub = df[df["model"] == m]
                avg_means.append(sub[metric].mean() if not sub.empty else 0.0)
            avg_means = np.nan_to_num(np.array(avg_means))

            ax.barh(
                y_pos,
                avg_means,
                color=palette,
                edgecolor=["black" if "ICC" in m else "none" for m in available_models],
                linewidth=[1.2 if "ICC" in m else 0.5 for m in available_models],
                height=0.68,
            )

            for j, val in enumerate(avg_means):
                offset = 0.015 if val >= 0 else -0.015
                ha = "left" if val >= 0 else "right"
                ax.text(
                    val + offset,
                    j,
                    f"{val:.3f}",
                    va="center",
                    ha=ha,
                    fontsize=9.0,
                    fontweight="bold" if "ICC_v2" in available_models[j] else "normal",
                    color="#a00000" if "ICC_v2" in available_models[j] else "black",
                )

            ax.axvline(0, color="black", linestyle="-", linewidth=0.8, alpha=0.8)
            ax.grid(axis="x", linestyle=":", alpha=0.5)
            ax.set_xlim(min(-0.05, np.min(avg_means) - 0.05), max(0.15, np.max(avg_means) + 0.10))
            clean_spines(ax)

        else:
            # Unused axes
            ax.axis("off")

        # Y-axis ticks on first column
        if i % 4 == 0:
            ax.set_yticks(y_pos)
            ax.set_yticklabels(labels, fontweight="bold")
            ax.set_ylabel("Clustering Method", fontweight="bold")

        # X-axis label on bottom row
        if i >= 12 and i <= n_datasets:
            ax.set_xlabel(f"Quality ({metric.upper()})", fontweight="bold")

    fig_title = (
        f"Figure 14: Comprehensive Clustering Recovery ({metric.upper()}) "
        f"Across {n_datasets} Multi-Domain Real-World Benchmarks"
    )
    plt.suptitle(fig_title, fontweight="bold", y=0.995)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved 13-dataset figure to: {save_path}")


def run_sub_exp3_1(
    n_trials: int = 10,
    resume: bool = True,
    output_csv: str = OUTPUT_CSV_V2,
) -> pd.DataFrame:
    """
    Executes Experiment 3.1: Expanded Multi-Domain Benchmark Matrix.

    Parameters
    ----------
    n_trials : int, default=10
        Number of stochastic trials per (dataset, model) combination.
    resume : bool, default=True
        Whether to resume existing progress from output_csv / original CSV.
    output_csv : str, default=OUTPUT_CSV_V2
        Path to target output CSV file.
    """
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)

    # 1. Discover all enabled datasets from registry
    dataset_infos = list_datasets(enabled_only=True)
    dataset_names = [d.name for d in dataset_infos]
    model_names = list(MODELS.keys())

    print("=" * 80)
    print("RUNNING SUB-EXPERIMENT 3.1: EXPANDED MULTI-DOMAIN BENCHMARK MATRIX (V2)")
    print(f"Datasets ({len(dataset_names)}): {dataset_names}")
    print(f"Models ({len(model_names)}): {model_names}")
    print(f"Trials per model: {n_trials}")
    print(f"Target Output CSV: {output_csv}")
    print("=" * 80)

    # 2. Initialize or load existing records for resume capability
    if resume:
        df = seed_v2_from_original_if_needed(output_csv, ORIGINAL_CSV)
        completed_set: Set[Tuple[str, str, int]] = set()
        if not df.empty and "dataset" in df.columns and "model" in df.columns and "trial" in df.columns:
            for _, r in df.iterrows():
                completed_set.add((str(r["dataset"]), str(r["model"]), int(r["trial"])))
        print(f"[+] Found {len(completed_set)} pre-existing trial runs in cache/resume set.")
    else:
        completed_set = set()
        df = pd.DataFrame(columns=CSV_COLUMNS)
        df.to_csv(output_csv, index=False)

    total_conditions = len(dataset_names) * len(model_names) * n_trials
    pbar = tqdm(total=total_conditions, desc="Benchmarking Matrix", unit="run")
    pbar.update(len(completed_set))

    # 3. Main execution loop
    for dname in dataset_names:
        # Load dataset
        X, y, meta = load_dataset(dname)
        N, D = X.shape
        K = meta.get("K", len(np.unique(y)))

        for mname, model_fn in MODELS.items():
            for t_idx in range(n_trials):
                key = (dname, mname, t_idx)
                if key in completed_set:
                    continue

                seed = SEEDS[t_idx % len(SEEDS)]
                try:
                    pred, elapsed_sec, lc = model_fn(X, K, seed=seed)
                    scores = evaluate_all(y, pred)
                except Exception as e:
                    print(f"\n[!] Error running {mname} on {dname} (trial {t_idx}): {e}")
                    # In case of algorithm failure, record null predictions
                    pred = np.zeros(N, dtype=int)
                    elapsed_sec = 0.0
                    lc = 0
                    scores = {"ari": 0.0, "nmi": 0.0, "ami": 0.0, "v_measure": 0.0, "fm_index": 0.0}

                row_dict = {
                    "dataset": dname,
                    "N": N,
                    "D": D,
                    "K": K,
                    "model": mname,
                    "trial": t_idx,
                    "seed": seed,
                    "ari": scores["ari"],
                    "nmi": scores["nmi"],
                    "ami": scores["ami"],
                    "v_measure": scores["v_measure"],
                    "fm_index": scores["fm_index"],
                    "elapsed_sec": elapsed_sec,
                    "lc": lc,
                }

                # Real-time incremental append to disk
                row_df = pd.DataFrame([row_dict])
                row_df.to_csv(output_csv, mode="a", header=not os.path.exists(output_csv), index=False)
                completed_set.add(key)

                pbar.set_postfix({"dataset": dname, "model": mname, "ari": f"{scores['ari']:.3f}"})
                pbar.update(1)

    pbar.close()

    # 4. Final summary and plots
    final_df = pd.read_csv(output_csv)
    print(f"\n[+] All {len(final_df)} model fits complete. Saved to: {output_csv}")

    generate_benchmark_tables(final_df, suffix="_v2")

    # Generate publication figures for all 13 datasets
    plot_fig14_13datasets(final_df, metric="ari", save_path=FIG14_PATH_13DS)
    plot_fig14_13datasets(final_df, metric="nmi", save_path=FIG14B_PATH_13DS_NMI)

    return final_df


def main():
    parser = argparse.ArgumentParser(description="Run Experiment 3.1 Benchmark Matrix")
    parser.add_argument("--trials", type=int, default=10, help="Number of trials per condition")
    parser.add_argument("--no-resume", action="store_true", help="Do not resume; restart from scratch")
    parser.add_argument("--output", type=str, default=OUTPUT_CSV_V2, help="Output CSV path")
    parser.add_argument("--reproduce-plots", action="store_true", help="Re-generate figures from output CSV")
    args = parser.parse_args()

    if args.reproduce_plots:
        csv_to_use = args.output if os.path.exists(args.output) else ORIGINAL_CSV
        print(f"[*] Re-generating 13-dataset figures from: {csv_to_use}")
        df = pd.read_csv(csv_to_use)
        plot_fig14_13datasets(df, metric="ari", save_path=FIG14_PATH_13DS)
        plot_fig14_13datasets(df, metric="nmi", save_path=FIG14B_PATH_13DS_NMI)
        print("[+] Done regenerating 13-dataset figures!")
        return

    run_sub_exp3_1(
        n_trials=args.trials,
        resume=not args.no_resume,
        output_csv=args.output,
    )


if __name__ == "__main__":
    main()
