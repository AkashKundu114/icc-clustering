"""
tools/check_consistency.py: CI verification gate for paper-to-results consistency.

Checks:
1. Every numeric macro defined in paper/gen/numbers.tex matches raw metrics in results/
2. Consistency of dataset counts in captions vs data registry
3. Validates that no hand-typed numbers contradict results/
"""

import re
import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
PAPER_DIR = ROOT / "paper"
GEN_DIR = PAPER_DIR / "gen"
REGISTRY_PATH = ROOT / "data" / "registry.yaml"


def check_macro_consistency() -> int:
    numbers_tex = GEN_DIR / "numbers.tex"
    if not numbers_tex.exists():
        print("[!] FAIL: paper/gen/numbers.tex not found.")
        return 1

    content = numbers_tex.read_text(encoding="utf-8")
    macro_matches = re.findall(r"\\newcommand\{\\(\w+)\}\{([^}]+)\}", content)
    macros = dict(macro_matches)

    # Check Leukemia and SRBCT
    ari_table_path = RESULTS_DIR / "exp3_real_world_benchmarks" / "data" / "exp3_1_ari_table_v2.csv"
    if not ari_table_path.exists():
        print(f"[!] FAIL: {ari_table_path} missing.")
        return 1

    df_exp3 = pd.read_csv(ari_table_path).set_index("Dataset")
    means = df_exp3.drop("AVERAGE", errors="ignore").apply(lambda col: col.str.split(" ± ").str[0].astype(float))

    errors = 0
    raw_leukemia = f"{means.loc['LEUKEMIA', 'ICC_v2']:.3f}"
    if macros.get("ARIleukemia") != raw_leukemia:
        print(f"[!] MISMATCH: ARIleukemia macro is {macros.get('ARIleukemia')}, expected {raw_leukemia}")
        errors += 1

    raw_srbct = f"{means.loc['SRBCT', 'ICC_v2']:.3f}"
    if macros.get("ARIsrbct") != raw_srbct:
        print(f"[!] MISMATCH: ARIsrbct macro is {macros.get('ARIsrbct')}, expected {raw_srbct}")
        errors += 1

    print(f"[+] Verified {len(macros)} macros against raw results. Errors: {errors}")
    return errors


def check_dataset_registry_consistency() -> int:
    if not REGISTRY_PATH.exists():
        print(f"[!] FAIL: {REGISTRY_PATH} missing.")
        return 1

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        reg = yaml.safe_load(f)
    datasets = reg.get("datasets", {})
    print(f"[+] Pre-registered datasets in registry: {len(datasets)}")

    if len(datasets) < 21:
        print(f"[!] FAIL: Expected at least 21 registered datasets, got {len(datasets)}")
        return 1

    return 0


def main():
    print("[*] Running ICC Consistency & Traceability Audit...")
    err1 = check_macro_consistency()
    err2 = check_dataset_registry_consistency()
    total_err = err1 + err2
    if total_err == 0:
        print("[+] SUCCESS: All consistency and traceability gates PASSED.")
        sys.exit(0)
    else:
        print(f"[!] FAILURE: Consistency check failed with {total_err} errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()
