"""
Central Reproduction CLI for ICC-v2.

Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes.

Provides unified, deterministic reproduction workflows across synthetic regimes, real-world
benchmarks, theoretical propositions, table generation, figure synchronization, and numerical
integrity verifications.

Usage:
    python scripts/reproduce.py --scope smoke     # Fast smoke test (~5s)
    python scripts/reproduce.py --scope verify    # Numerical & theoretical proofs verification (~5s)
    python scripts/reproduce.py --scope tables    # Recompile all 21 paper LaTeX tables (~5s)
    python scripts/reproduce.py --scope figures   # Sync and generate manuscript figures (~15s)
    python scripts/reproduce.py --scope full      # Run all reproduction suites end-to-end
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent


def run_smoke():
    print("=" * 70)
    print("ICC-v2 Reproduction Suite: Smoke Scope (Synthetic + Real Benchmarks)")
    print("=" * 70)
    t0 = time.perf_counter()

    from icc import ICC
    from icc.datasets.registry import load_dataset
    from icc.metrics import evaluate_all

    # 1. Synthetic high-dimensional noise benchmark
    rng = np.random.default_rng(42)
    X_syn = rng.standard_normal((100, 20))
    model_syn = ICC(n_clusters=3, random_state=42)
    pred_syn = model_syn.fit_predict(X_syn)
    print(f"[*] [1/3] Synthetic: N=100, D=20, recovered_clusters={len(np.unique(pred_syn))}, sum={pred_syn.sum()}")

    # 2. Leukemia benchmark (D=7129)
    X_leu, y_leu, _ = load_dataset("leukemia")
    model_leu = ICC(n_clusters=2, random_state=0)
    pred_leu = model_leu.fit_predict(X_leu)
    ari_leu = evaluate_all(y_leu, pred_leu)["ari"]
    print(f"[*] [2/3] Leukemia (Seed 0): N=72, D=7129, ARI={ari_leu:.4f}")

    # 3. SRBCT benchmark (D=2308)
    X_srb, y_srb, _ = load_dataset("srbct")
    model_srb = ICC(n_clusters=4, random_state=0)
    pred_srb = model_srb.fit_predict(X_srb)
    ari_srb = evaluate_all(y_srb, pred_srb)["ari"]
    print(f"[*] [3/3] SRBCT (Seed 0):    N=83, D=2308, ARI={ari_srb:.4f}")

    elapsed = time.perf_counter() - t0
    print("-" * 70)
    print(f"Smoke reproduction passed successfully in {elapsed:.2f} seconds.")
    print("=" * 70)


def run_verify():
    print("=" * 70)
    print("ICC-v2 Reproduction Suite: Verification Scope")
    print("=" * 70)

    # 1. Numerical checks
    print("\n[Step 1/4] Running 19-point numerical claim verifier (check_numbers.py)...")
    res = subprocess.run([sys.executable, "scripts/check_numbers.py"], cwd=ROOT)
    if res.returncode != 0:
        print("ERROR: Numerical check failed.")
        sys.exit(res.returncode)

    # 2. Proposition 1 theoretical determinacy
    print("\n[Step 2/4] Verifying Proposition 1 transfer cut determinacy (verify_prop1.py)...")
    res = subprocess.run([sys.executable, "scripts/verify_prop1.py"], cwd=ROOT)
    if res.returncode != 0:
        print("ERROR: Proposition 1 verification failed.")
        sys.exit(res.returncode)

    # 3. Proposition 2 Contingency Tensor Identity
    print("\n[Step 3/4] Verifying Proposition 2 contingency tensor identity (verify_determinacy_identity.py)...")
    res = subprocess.run([sys.executable, "scripts/verify_determinacy_identity.py"], cwd=ROOT)
    if res.returncode != 0:
        print("ERROR: Proposition 2 verification failed.")
        sys.exit(res.returncode)

    # 4. Sarle's Bimodality Coefficient Analytical Verification
    print("\n[Step 4/4] Verifying Sarle's Bimodality Coefficient thresholds (verify_bc.py)...")
    res = subprocess.run([sys.executable, "scripts/verify_bc.py"], cwd=ROOT)
    if res.returncode != 0:
        print("ERROR: BC verification failed.")
        sys.exit(res.returncode)

    print("\nAll mathematical and numerical verification suites passed successfully.")
    print("=" * 70)


def run_tables():
    print("=" * 70)
    print("ICC-v2 Reproduction Suite: LaTeX Table Generation Scope")
    print("=" * 70)
    res = subprocess.run([sys.executable, "scripts/make_tables.py"], cwd=ROOT)
    if res.returncode != 0:
        print("ERROR: Table generation failed.")
        sys.exit(res.returncode)
    print("=" * 70)


def run_figures():
    print("=" * 70)
    print("ICC-v2 Reproduction Suite: Figure Generation & Synchronization Scope")
    print("=" * 70)
    print("\n[*] Synchronizing figures...")
    subprocess.run([sys.executable, "scripts/sync_figures.py"], cwd=ROOT, check=True)
    print("\n[*] Rendering conceptual framework figure...")
    subprocess.run([sys.executable, "scripts/plot_conceptual_framework.py"], cwd=ROOT, check=True)
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="ICC-v2 Central Reproduction CLI")
    parser.add_argument(
        "--scope",
        choices=["smoke", "verify", "tables", "figures", "full"],
        default="smoke",
        help="Reproduction execution scope (smoke, verify, tables, figures, full)",
    )
    args = parser.parse_args()

    # Enforce BLAS thread determinism
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"

    if args.scope == "smoke":
        run_smoke()
    elif args.scope == "verify":
        run_verify()
    elif args.scope == "tables":
        run_tables()
    elif args.scope == "figures":
        run_figures()
    elif args.scope == "full":
        run_smoke()
        run_verify()
        run_tables()
        run_figures()
        print("\nFull reproduction suite finished successfully.")


if __name__ == "__main__":
    main()
