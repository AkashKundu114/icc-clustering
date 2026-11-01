from pathlib import Path
import numpy as np
from icc.confirmatory.runner import execute_confirmatory_cohort

def main():
    root = Path(__file__).resolve().parent.parent
    unlabeled = root / "data" / "confirmatory" / "unlabeled" / "GSE42568_unlabeled.npz"
    vault_dir = root / "data" / "confirmatory" / "vault"
    output_dir = root / "results" / "confirmatory_test"
    
    print("[*] Running 1-seed smoke test on GSE42568...")
    df = execute_confirmatory_cohort(
        cohort_id="GSE42568",
        unlabeled_npz_path=unlabeled,
        vault_dir=vault_dir,
        output_dir=output_dir,
        seeds=[42],
    )
    print("[+] Test completed:")
    print(df[["model_name", "ari", "nmi", "runtime_sec", "status"]])

if __name__ == "__main__":
    main()
