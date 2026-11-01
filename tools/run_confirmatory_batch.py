#!/usr/bin/env python3
"""
tools/run_confirmatory_batch.py
Batch Execution of Preregistered Confirmatory Matrix (E1-E8) across Ingested Cohorts.
Enforces zero label exposure, SHA-256 fingerprinting of predictions, and post-inference unsealing.
"""

import sys
import time
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from icc.confirmatory.runner import execute_confirmatory_cohort, CONFIRMATORY_SEEDS
from icc.confirmatory.statistical_analyzer import run_full_statistical_analysis

UNLABELED_DIR = ROOT / "data" / "confirmatory" / "unlabeled"
VAULT_DIR = ROOT / "data" / "confirmatory" / "vault"
RESULTS_DIR = ROOT / "results" / "confirmatory"


def run_cohorts(cohort_ids):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    completed_cohorts = []
    for c_id in cohort_ids:
        unlabeled_file = UNLABELED_DIR / f"{c_id}_unlabeled.npz"
        if not unlabeled_file.exists():
            print(f"[-] Cohort {c_id} unlabeled matrix not found at {unlabeled_file}. Skipping.")
            continue
        
        print(f"\n{'='*70}")
        print(f"[+] LAUNCHING CONFIRMATORY BENCHMARK: {c_id}")
        print(f"{'='*70}")
        t0 = time.time()
        df_cohort = execute_confirmatory_cohort(
            cohort_id=c_id,
            unlabeled_npz_path=unlabeled_file,
            vault_dir=VAULT_DIR,
            output_dir=RESULTS_DIR,
            seeds=CONFIRMATORY_SEEDS,
        )
        elapsed = time.time() - t0
        print(f"[+] Finished {c_id} in {elapsed:.1f}s. Rows: {len(df_cohort)}")
        completed_cohorts.append(c_id)

    print(f"\n[+] Batch complete. Successfully evaluated {len(completed_cohorts)} cohorts: {completed_cohorts}")
    
    if completed_cohorts:
        print("\n" + "="*70)
        print("[+] RUNNING PRE-REGISTERED STATISTICAL INFERENCE")
        print("="*70)
        stats_out = run_full_statistical_analysis(RESULTS_DIR)
        print("\n=== Family 1: Primary Baseline Comparisons (FWER alpha=0.05) ===")
        print(stats_out.get("family1"))
        print("\n=== Family 2: Architectural Component Attribution (H2a, H2b, H3) ===")
        print(stats_out.get("family2"))

    return completed_cohorts


if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else ["GSE42568", "GSE19188", "GSE21653", "GSE32894"]
    run_cohorts(targets)
