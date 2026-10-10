"""
Experiment 2 Sweep Runner: Executes Component-Wise Ablation across Noise Regimes.
Records ARI, NMI, and effective anchor counts for all 6 variants across 10 trials.
"""

import time
from pathlib import Path
import numpy as np
import pandas as pd

import sys
curr_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(curr_dir))
root_dir = curr_dir.parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.icc.core import build_dataset
from src.icc.metrics import evaluate_all
from ablation_engine import run_icc_variant

VARIANTS = {
    "V0_Standard_Consensus": dict(use_subspaces=False, use_noise_calibration=False, use_core_anchors=False),
    "V1_Subspaces_Only": dict(use_subspaces=True, use_noise_calibration=False, use_core_anchors=False),
    "V2_Anchors_Only": dict(use_subspaces=False, use_noise_calibration=False, use_core_anchors=True),
    "V3_Subspaces_Plus_Anchors": dict(use_subspaces=True, use_noise_calibration=False, use_core_anchors=True),
    "V4_Subspaces_Plus_Calibration": dict(use_subspaces=True, use_noise_calibration=True, use_core_anchors=False),
    "V5_Full_ICC_v1": dict(use_subspaces=True, use_noise_calibration=True, use_core_anchors=True)
}


def run_ablation_experiment(
    noise_dims=[0, 50, 200, 1000, 3000, 5000],
    n_trials=10,
    n_total=300,
    k_clusters=3,
    noise_kind="scaled"
):
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

            for v_name, config in VARIANTS.items():
                preds, l_c = run_icc_variant(
                    X, k=k_clusters,
                    use_subspaces=config["use_subspaces"],
                    use_noise_calibration=config["use_noise_calibration"],
                    use_core_anchors=config["use_core_anchors"],
                    n_base_models=20,
                    n_anchors=60,
                    subspace_rate=0.25,
                    beta=2.0,
                    seed=trial
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
                noise_kind=noise_kind
            ))

        v0_ari = np.mean(dim_results["V0_Standard_Consensus"]["ari"])
        v5_ari = np.mean(dim_results["V5_Full_ICC_v1"]["ari"])
        v5_ami = np.mean(dim_results["V5_Full_ICC_v1"]["ami"])
        print(f"  [D_noise={d_noise:5d}] V0: {v0_ari:.3f} ARI | V5: {v5_ari:.3f} ARI (AMI: {v5_ami:.3f}) | Lift: {v5_ari - v0_ari:+.3f} ARI ({time.time()-t_dim:.1f}s)")

    df = pd.DataFrame(records)
    out_dir = Path(__file__).resolve().parent.parent / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "exp2_ablation_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nSaved ablation results to {csv_path} in {time.time()-t_start:.1f}s")
    return df


if __name__ == "__main__":
    run_ablation_experiment()
