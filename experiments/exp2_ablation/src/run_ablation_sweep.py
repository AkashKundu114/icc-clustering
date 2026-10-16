"""
Experiment 2 Sweep Runner: Executes Component-Wise Ablation across Noise Regimes.
Records ARI, NMI, and effective anchor counts for all 6 modular variants across trials.
"""

import time
from pathlib import Path
from typing import List
import numpy as np
import pandas as pd

import sys
curr_dir = Path(__file__).resolve().parent
if str(curr_dir) not in sys.path:
    sys.path.insert(0, str(curr_dir))
root_dir = curr_dir.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from icc.core import build_dataset
from icc.metrics import evaluate_all
from icc.datasets.registry import load_dataset
from ablation_engine import run_icc_variant

VARIANTS = [
    "V0_Standard_Consensus",
    "V1_VSSG_KMeans",
    "V2_VSSG_StdConsensus",
    "V3_Anchors_Only",
    "V4_VSSG_Random_Anchors",
    "V5_Full_ICC_v2",
]


def run_ablation_experiment(
    noise_dims: List[int] = [0, 50, 200, 1000, 3000, 5000],
    n_trials: int = 10,
    n_total: int = 300,
    k_clusters: int = 3,
    noise_kind: str = "scaled",
) -> pd.DataFrame:
    print("=================================================================")
    print(" RUNNING EXPERIMENT 2: COMPONENT-WISE ABLATION STUDY")
    print(f" Noise Regime: {noise_kind.upper()} | N={n_total}, K={k_clusters}")
    print(f" Testing 6 Architectural Variants across {len(noise_dims)} Noise Dimensions")
    print("=================================================================")

    records = []
    t_start = time.time()

    for d_noise in noise_dims:
        t_dim = time.time()
        print(f"\n--> Evaluating D_noise = {d_noise:<5} (Total D = {d_noise + 2})")

        dim_results = {v: {"ari": [], "nmi": [], "ami": [], "v_measure": [], "fm_index": [], "l_c": []} for v in VARIANTS}

        for trial in range(n_trials):
            X, y_true = build_dataset(
                d_noise=d_noise, noise_kind=noise_kind, noise_seed=trial * 37,
                n_per_cluster=n_total // k_clusters, k=k_clusters
            )

            for v_name in VARIANTS:
                preds, l_c = run_icc_variant(
                    X, k=k_clusters,
                    variant_name=v_name,
                    n_base_models=20,
                    n_anchors=40,
                    subspace_rate=0.30,
                    seed=trial,
                )
                metrics = evaluate_all(y_true, preds)
                dim_results[v_name]["ari"].append(metrics["ari"])
                dim_results[v_name]["nmi"].append(metrics["nmi"])
                dim_results[v_name]["ami"].append(metrics["ami"])
                dim_results[v_name]["v_measure"].append(metrics["v_measure"])
                dim_results[v_name]["fm_index"].append(metrics["fm_index"])
                dim_results[v_name]["l_c"].append(l_c)

        for v_name in VARIANTS:
            m_ari = float(np.mean(dim_results[v_name]["ari"]))
            m_nmi = float(np.mean(dim_results[v_name]["nmi"]))
            m_ami = float(np.mean(dim_results[v_name]["ami"]))
            m_v_meas = float(np.mean(dim_results[v_name]["v_measure"]))
            m_fm = float(np.mean(dim_results[v_name]["fm_index"]))
            m_lc = float(np.mean(dim_results[v_name]["l_c"]))
            records.append(dict(
                d_noise=d_noise,
                variant=v_name,
                mean_ari=m_ari,
                mean_nmi=m_nmi,
                mean_ami=m_ami,
                mean_v_measure=m_v_meas,
                mean_fm_index=m_fm,
                mean_lc=m_lc,
                noise_kind=noise_kind,
            ))

        v0_ari = np.mean(dim_results["V0_Standard_Consensus"]["ari"])
        v1_ari = np.mean(dim_results["V1_VSSG_KMeans"]["ari"])
        v5_ari = np.mean(dim_results["V5_Full_ICC_v2"]["ari"])
        print(f"  [D_noise={d_noise:5d}] V0: {v0_ari:.3f} | V1: {v1_ari:.3f} | V5: {v5_ari:.3f} ARI | Lift (V5-V0): {v5_ari - v0_ari:+.3f} ({time.time()-t_dim:.1f}s)")

    df = pd.DataFrame(records)
    out_dir = Path(__file__).resolve().parent.parent / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "exp2_ablation_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nSaved ablation results to {csv_path} in {time.time()-t_start:.1f}s")
    return df


def run_real_world_ablation(
    dataset_names: List[str] = ["leukemia", "srbct"],
    n_trials: int = 5,
) -> pd.DataFrame:
    """
    Executes component-wise ablation across real high-dimensional cancer microarrays.
    Verifies Control 1 (VSSG+KMeans) and Control 2 (VSSG+StdConsensus) against Full ICC-v2.
    """
    print("\n=================================================================")
    print(" RUNNING REAL-WORLD GENOMICS ABLATION AUDIT (CONTROLS 1 & 2)")
    print("=================================================================")
    records = []

    for ds_name in dataset_names:
        X, y_true, meta = load_dataset(ds_name)
        k = meta["K"]
        N, D = X.shape
        print(f"\n--> Benchmark: {ds_name.upper()} (N={N}, D={D}, K={k})")

        ds_results = {v: {"ari": [], "nmi": []} for v in VARIANTS}
        for trial in range(n_trials):
            for v_name in VARIANTS:
                preds, _ = run_icc_variant(
                    X, k=k,
                    variant_name=v_name,
                    n_base_models=25,
                    n_anchors=min(40, N),
                    seed=trial,
                )
                metrics = evaluate_all(y_true, preds)
                ds_results[v_name]["ari"].append(metrics["ari"])
                ds_results[v_name]["nmi"].append(metrics["nmi"])

        for v_name in VARIANTS:
            m_ari = float(np.mean(ds_results[v_name]["ari"]))
            m_nmi = float(np.mean(ds_results[v_name]["nmi"]))
            std_ari = float(np.std(ds_results[v_name]["ari"]))
            records.append(dict(
                dataset=ds_name,
                N=N,
                D=D,
                K=k,
                variant=v_name,
                mean_ari=m_ari,
                std_ari=std_ari,
                mean_nmi=m_nmi,
            ))
            print(f"  {v_name:<25}: ARI = {m_ari:.4f} +/- {std_ari:.4f} | NMI = {m_nmi:.4f}")

    df_real = pd.DataFrame(records)
    out_dir = Path(__file__).resolve().parent.parent / "data"
    csv_path = out_dir / "exp2_real_ablation_results.csv"
    df_real.to_csv(csv_path, index=False)
    print(f"\nSaved real-world ablation audit to {csv_path}")
    return df_real


if __name__ == "__main__":
    run_ablation_experiment()
    run_real_world_ablation()
