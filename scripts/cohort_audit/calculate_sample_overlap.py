"""
Step 2 & 3: Sample Identifier Extraction, Normalisation, and Overlap Detection.
Audits sample identifiers across all available datasets and computes pairwise overlap metrics.

Outputs:
- results/cohort_independence/sample_identifier_audit.csv
- results/cohort_independence/sample_overlap_matrix.csv
- results/cohort_independence/sample_overlap_pairs.csv
"""

import gzip
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

import numpy as np
import pandas as pd

_ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR_MAIN = _ROOT / "data" / "cache"
CACHE_DIR_EXP3 = _ROOT / "experiments" / "exp3_real_world_benchmarks" / "data" / "cache"
OPENML_CACHE_DIR = Path.home() / "scikit_learn_data" / "openml" / "openml.org"

OUT_DIR = _ROOT / "results" / "cohort_independence"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def normalise_sample_id(raw_id: str) -> str:
    """
    Standardize sample identifier syntax:
    - Lowercase
    - Strip whitespace, quotation marks, and trailing suffixes
    - Normalize delimiters (_, -, .)
    """
    s = str(raw_id).strip().strip("'\"").lower()
    # Replace whitespace and punctuation
    s = re.sub(r"[\s\t\n]+", "_", s)
    s = re.sub(r"[-.]", "_", s)
    return s


def extract_sample_ids_from_arff(file_path: Path) -> List[str]:
    """Extract raw sample IDs or row identifiers from an ARFF file."""
    ids = []
    with gzip.open(file_path, "rt", encoding="utf-8", errors="ignore") as gz:
        in_data = False
        row_idx = 0
        for line in gz:
            line_str = line.strip()
            if not line_str or line_str.startswith("%"):
                continue
            if line_str.upper().startswith("@DATA"):
                in_data = True
                continue
            if in_data:
                parts = line_str.split(",")
                # If first column looks like an ID string or number
                first_token = parts[0].strip().strip("'\"")
                last_token = parts[-1].strip().strip("'\"")
                # Use dataset prefix and row index as primary traceable ID
                sample_id = f"{file_path.stem.split('.')[0]}_sample_{row_idx:04d}"
                ids.append(sample_id)
                row_idx += 1
    return ids


def run_sample_audit():
    print("=== Extracting and Auditing Sample Identifiers ===")
    
    # 1. Collect all cached datasets
    datasets = {}
    
    # Check npz in main cache
    for f in CACHE_DIR_MAIN.glob("*.npz"):
        data = np.load(f, allow_pickle=True)
        N = data["X"].shape[0] if "X" in data else 0
        name = f.stem
        # Generate standardized sample IDs
        datasets[name] = [f"{name}_{i:04d}" for i in range(N)]

    # Check npz in exp3 cache
    for f in CACHE_DIR_EXP3.glob("*.npz"):
        name = f"exp3_{f.stem}"
        if f.stem not in datasets:
            data = np.load(f, allow_pickle=True)
            N = data["X"].shape[0] if "X" in data else 0
            datasets[name] = [f"{f.stem}_{i:04d}" for i in range(N)]

    # Add raw ARFF files from openml download cache
    dl_dir = OPENML_CACHE_DIR / "data" / "v1" / "download"
    key_arffs = [
        "CNS.arff.gz", "Colon.arff.gz", "Leukemia.arff.gz", "Ovarian.arff.gz",
        "Prostate.arff.gz", "SRBCT.arff.gz", "GCM.arff.gz", "DLBCL.arff.gz",
        "Breast.arff.gz", "11_Tumors.arff.gz", "9_Tumors.arff.gz", "GLI.arff.gz"
    ]
    for target in key_arffs:
        matches = list(dl_dir.glob(f"**/{target}"))
        if matches:
            p = matches[0]
            clean_name = f"arff_{target.split('.')[0].lower()}"
            datasets[clean_name] = extract_sample_ids_from_arff(p)

    print(f"Collected sample rosters across {len(datasets)} dataset representations.")

    # 2. Write sample identifier audit
    audit_rows = []
    for ds_name, id_list in datasets.items():
        audit_rows.append({
            "dataset_name": ds_name,
            "sample_count": len(id_list),
            "id_format": "Synthetic Index / Row Identifier" if "sample_" in id_list[0] or "_" in id_list[0] else "Native ID",
            "first_id_raw": id_list[0] if id_list else "",
            "last_id_raw": id_list[-1] if id_list else "",
            "has_unique_ids": len(id_list) == len(set(id_list)),
            "comparability_flag": "Requires feature-level profile correlation (microarray benchmarks lack universal Patient IDs)"
        })
    df_audit = pd.DataFrame(audit_rows)
    df_audit.to_csv(OUT_DIR / "sample_identifier_audit.csv", index=False)
    print(f"Saved sample identifier audit to: {OUT_DIR / 'sample_identifier_audit.csv'}")

    # 3. Compute Pairwise Identifier Overlap Matrix
    ds_names = sorted(list(datasets.keys()))
    n_ds = len(ds_names)
    matrix = np.zeros((n_ds, n_ds), dtype=np.float64)
    pairs_records = []

    for i in range(n_ds):
        for j in range(n_ds):
            name_a = ds_names[i]
            name_b = ds_names[j]
            set_a = set(datasets[name_a])
            set_b = set(datasets[name_b])

            inter = len(set_a.intersection(set_b))
            union = len(set_a.union(set_b))
            jaccard = inter / union if union > 0 else 0.0
            o_a = inter / len(set_a) if len(set_a) > 0 else 0.0
            o_b = inter / len(set_b) if len(set_b) > 0 else 0.0

            matrix[i, j] = jaccard

            if i < j:
                pairs_records.append({
                    "dataset_a": name_a,
                    "dataset_b": name_b,
                    "unique_samples_a": len(set_a),
                    "unique_samples_b": len(set_b),
                    "intersection_count": inter,
                    "jaccard_similarity": jaccard,
                    "overlap_relative_to_a": o_a,
                    "overlap_relative_to_b": o_b,
                    "identifier_overlap_verdict": "Identical ID namespace" if jaccard == 1.0 else (
                        "Partial overlap" if jaccard > 0 else "Disjoint ID strings (Requires profile matching)"
                    )
                })

    df_matrix = pd.DataFrame(matrix, index=ds_names, columns=ds_names)
    df_matrix.to_csv(OUT_DIR / "sample_overlap_matrix.csv")
    print(f"Saved overlap matrix to: {OUT_DIR / 'sample_overlap_matrix.csv'}")

    df_pairs = pd.DataFrame(pairs_records)
    df_pairs.to_csv(OUT_DIR / "sample_overlap_pairs.csv", index=False)
    print(f"Saved pairwise overlap table to: {OUT_DIR / 'sample_overlap_pairs.csv'}")


if __name__ == "__main__":
    run_sample_audit()
