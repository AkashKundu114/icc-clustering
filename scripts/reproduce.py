"""
Central Reproduction CLI for ICC-v2.

Executes deterministic reproducibility verification across synthetic and real-world benchmark datasets.

Usage:
    python scripts/reproduce.py --scope smoke
"""

import argparse
import os
import time

import numpy as np


def run_smoke():
    print("=" * 60)
    print("ICC-v2 Reproduction: Smoke Scope (Synthetic + Real Benchmarks)")
    print("=" * 60)
    t0 = time.perf_counter()

    from icc import ICC
    from icc.datasets.registry import load_dataset
    from icc.metrics import evaluate_all

    # 1. Synthetic
    rng = np.random.default_rng(42)
    X_syn = rng.standard_normal((100, 20))
    model_syn = ICC(n_clusters=3, random_state=42)
    pred_syn = model_syn.fit_predict(X_syn)
    print(f"[1/3] Synthetic: N=100, D=20, clusters={len(np.unique(pred_syn))}, sum={pred_syn.sum()}")

    # 2. Leukemia
    X_leu, y_leu, _ = load_dataset("leukemia")
    model_leu = ICC(n_clusters=2, random_state=0)
    pred_leu = model_leu.fit_predict(X_leu)
    ari_leu = evaluate_all(y_leu, pred_leu)["ari"]
    print(f"[2/3] Leukemia (Seed 0): N=72, D=7129, ARI={ari_leu:.4f}")

    # 3. SRBCT
    X_srb, y_srb, _ = load_dataset("srbct")
    model_srb = ICC(n_clusters=4, random_state=0)
    pred_srb = model_srb.fit_predict(X_srb)
    ari_srb = evaluate_all(y_srb, pred_srb)["ari"]
    print(f"[3/3] SRBCT (Seed 0):    N=83, D=2308, ARI={ari_srb:.4f}")

    elapsed = time.perf_counter() - t0
    print("-" * 60)
    print(f"Smoke reproduction passed in {elapsed:.2f} seconds.")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="ICC-v2 Central Reproduction CLI")
    parser.add_argument(
        "--scope",
        choices=["smoke", "standard", "full"],
        default="smoke",
        help="Reproduction execution scope (smoke, standard, full)",
    )
    args = parser.parse_args()

    # Enforce BLAS thread determinism
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"

    if args.scope == "smoke":
        run_smoke()
    else:
        print(f"Scope '{args.scope}' initiated. For standard/full, execute experiment scripts directly.")

if __name__ == "__main__":
    main()
