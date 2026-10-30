"""
Central Reproduction CLI for ICC-v2.

Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes.

Provides push-button verification of all tables, figures, benchmarks, and theoretical invariants
reported in the paper.

Scopes:
    --scope smoke       Fast verification of synthetic and real datasets (< 3s)
    --scope verify      Verify mathematical proofs, determinacy identities, and statistical invariants (< 3s)
    --scope tables      Extract and format all Paper Tables (Table 1 through Table 15) to results/tables/
    --scope figures     Verify presence, provenance, and checksums of all paper figures
    --scope benchmarks  Execute real-data evaluations on Leukemia, SRBCT, Colon, Lymphoma datasets
    --scope all         Execute all reproduction scopes end-to-end

Usage:
    python scripts/reproduce.py --scope smoke
    python scripts/reproduce.py --scope verify
    python scripts/reproduce.py --scope tables
    python scripts/reproduce.py --scope figures
    python scripts/reproduce.py --scope benchmarks
    python scripts/reproduce.py --scope all
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent


def set_deterministic_threads():
    """Enforce BLAS and OpenMP single-threaded execution for determinism."""
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
    os.environ["NUMEXPR_NUM_THREADS"] = "1"


def run_smoke():
    """Execute fast smoke verification on synthetic and real datasets (< 3s)."""
    print("\n" + "=" * 70)
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
    n_c_syn = len(np.unique(pred_syn))
    print(f"[*] [1/3] Synthetic: N=100, D=20, recovered_clusters={n_c_syn}, sum={pred_syn.sum()}")

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
    print("=" * 70 + "\n")


def run_verify():
    """Execute mathematical proofs, determinacy identities, and theoretical invariant verifications (< 3s)."""
    print("\n" + "=" * 70)
    print("ICC-v2 Reproduction Suite: Identity & Invariant Verification Scope")
    print("=" * 70)
    t0 = time.perf_counter()

    # 1. Proposition 2: Exact Sample Determinacy Identity
    print("[*] [1/3] Verifying Proposition 2 Contingency Matrix Determinacy Identity...")
    cmd_id = [sys.executable, str(ROOT / "scripts" / "verify_identities.py")]
    res_id = subprocess.run(cmd_id, cwd=ROOT)
    if res_id.returncode != 0:
        print("[!] Error: verify_identities.py exited with failure.")
        sys.exit(res_id.returncode)

    # 2. Proposition 1: Bimodality Coefficient Separation Bound
    print("[*] [2/3] Verifying Proposition 1 Bimodality Separation Bound...")
    cmd_prop1 = [sys.executable, str(ROOT / "scripts" / "verify_prop1.py")]
    res_prop1 = subprocess.run(cmd_prop1, cwd=ROOT)
    if res_prop1.returncode != 0:
        print("[!] Error: verify_prop1.py exited with failure.")
        sys.exit(res_prop1.returncode)

    # 3. Statistical Invariants & Consistency Checker
    print("[*] [3/3] Verifying Scientific Consistency & Stats Invariants...")
    cmd_check = [sys.executable, str(ROOT / "tools" / "check_consistency.py")]
    res_check = subprocess.run(cmd_check, cwd=ROOT)
    if res_check.returncode != 0:
        print("[!] Error: check_consistency.py exited with failure.")
        sys.exit(res_check.returncode)

    elapsed = time.perf_counter() - t0
    print("-" * 70)
    print(f"Identity and invariant verification passed successfully in {elapsed:.2f} seconds.")
    print("=" * 70 + "\n")


def run_tables(table_arg: str = "all"):
    """Execute paper table reproduction (scripts/reproduce_tables.py)."""
    print("\n" + "=" * 70)
    print("ICC-v2 Reproduction Suite: Tables Scope")
    print("=" * 70)
    t0 = time.perf_counter()

    script_path = ROOT / "scripts" / "reproduce_tables.py"
    cmd = [sys.executable, str(script_path), "--table", table_arg]
    res = subprocess.run(cmd, cwd=ROOT)
    if res.returncode != 0:
        print("[!] Error: reproduce_tables.py exited with failure.")
        sys.exit(res.returncode)

    elapsed = time.perf_counter() - t0
    print(f"Table reproduction completed in {elapsed:.2f} seconds.")
    print("=" * 70 + "\n")


def run_figures(generate: bool = False):
    """Execute figure verification and synchronization (scripts/reproduce_figures.py)."""
    print("\n" + "=" * 70)
    print("ICC-v2 Reproduction Suite: Figures Scope")
    print("=" * 70)
    t0 = time.perf_counter()

    script_path = ROOT / "scripts" / "reproduce_figures.py"
    cmd = [sys.executable, str(script_path)]
    if generate:
        cmd.append("--generate")
    res = subprocess.run(cmd, cwd=ROOT)
    if res.returncode != 0:
        print("[!] Error: reproduce_figures.py exited with failure.")
        sys.exit(res.returncode)

    elapsed = time.perf_counter() - t0
    print(f"Figure verification completed in {elapsed:.2f} seconds.")
    print("=" * 70 + "\n")


def run_benchmarks(datasets: list = None, seeds: list = None):
    """Execute real-data evaluations (scripts/reproduce_benchmarks.py)."""
    print("\n" + "=" * 70)
    print("ICC-v2 Reproduction Suite: Benchmarks Scope")
    print("=" * 70)
    t0 = time.perf_counter()

    script_path = ROOT / "scripts" / "reproduce_benchmarks.py"
    cmd = [sys.executable, str(script_path)]
    if datasets:
        cmd.extend(["--datasets"] + datasets)
    if seeds:
        cmd.extend(["--seeds"] + [str(s) for s in seeds])
    res = subprocess.run(cmd, cwd=ROOT)
    if res.returncode != 0:
        print("[!] Error: reproduce_benchmarks.py exited with failure.")
        sys.exit(res.returncode)

    elapsed = time.perf_counter() - t0
    print(f"Benchmark reproduction completed in {elapsed:.2f} seconds.")
    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="ICC-v2 Central Reproduction Engine")
    parser.add_argument(
        "--scope",
        choices=["smoke", "verify", "tables", "figures", "benchmarks", "all"],
        default="smoke",
        help="Reproduction execution scope (smoke, verify, tables, figures, benchmarks, all)",
    )
    parser.add_argument(
        "--table",
        type=str,
        default="all",
        help="Specific table to reproduce for tables scope ('all', '1', '6', etc.)",
    )
    parser.add_argument(
        "--generate-figures",
        action="store_true",
        help="Re-render figures during figures scope",
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        default=["leukemia", "srbct", "colon", "lymphoma"],
        help="Datasets for benchmarks scope",
    )
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=[0, 1, 2],
        help="Random seeds for benchmarks scope",
    )
    args = parser.parse_args()

    set_deterministic_threads()

    t_start = time.perf_counter()

    if args.scope == "smoke":
        run_smoke()
    elif args.scope == "verify":
        run_verify()
    elif args.scope == "tables":
        run_tables(table_arg=args.table)
    elif args.scope == "figures":
        run_figures(generate=args.generate_figures)
    elif args.scope == "benchmarks":
        run_benchmarks(datasets=args.datasets, seeds=args.seeds)
    elif args.scope == "all":
        print("\n" + "#" * 70)
        print("  Executing Complete ICC-v2 Reproduction Pipeline End-to-End")
        print("#" * 70)
        run_smoke()
        run_verify()
        run_tables(table_arg="all")
        run_figures(generate=args.generate_figures)
        run_benchmarks(datasets=args.datasets, seeds=args.seeds)
        t_total = time.perf_counter() - t_start
        print("#" * 70)
        print(f"  Complete Reproduction Pipeline Succeeded in {t_total:.2f} seconds.")
        print("#" * 70 + "\n")


if __name__ == "__main__":
    main()
