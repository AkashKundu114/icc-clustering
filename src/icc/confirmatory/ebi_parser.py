"""
src/icc/confirmatory/ebi_parser.py
Parser for EBI BioStudies / ArrayExpress Processed Cohort Archives.

Processes zip archives containing probe-level sample tables and SDRF metadata,
assembles high-dimensional expression matrices, and enforces strict label quarantine.
"""

import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
import zipfile

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

from icc.confirmatory.vault import LabelQuarantineVault


def parse_ebi_gse31210(
    zip_path: Path,
    sdrf_path: Path,
    output_dir: Path,
    vault_dir: Path,
    max_genes: int = 10000,
) -> Tuple[np.ndarray, str, Dict[str, Any]]:
    """
    Parses Okayama GSE31210 Lung Adenocarcinoma cohort from EBI BioStudies.
    Restricts to N=226 primary lung tumor specimens, excluding 20 normal lung controls.
    Ground truth: Oncogenic mutational driver status (EGFR_mut, KRAS_mut, Other_driver_neg).
    """
    zip_path = Path(zip_path)
    sdrf_path = Path(sdrf_path)
    cohort_id = "GSE31210"

    print(f"[EBI_PARSER] Parsing SDRF metadata from {sdrf_path.name}...")
    sdrf_text = sdrf_path.read_text(encoding="utf-8", errors="ignore")
    reader = csv.reader(sdrf_text.splitlines(), delimiter="\t")
    header = next(reader)

    source_idx = header.index("Comment [Sample_source_name]")
    # Gene alteration status column
    status_idx = 29
    sample_col = 0

    valid_samples = []
    labels = []
    sample_table_map = {}

    with zipfile.ZipFile(zip_path, "r") as z:
        available_files = set(z.namelist())
        for row in reader:
            if len(row) <= status_idx:
                continue
            src = row[source_idx].strip()
            # Retain only primary tumor resections, exclude normal lung controls
            if "primary lung tumor" not in src.lower():
                continue

            # Extract GSM accession from Source Name (e.g., 'GSM773785 1' -> 'GSM773785')
            gsm = row[sample_col].strip().split()[0]
            table_name = f"{gsm}_sample_table.txt"
            if table_name not in available_files:
                continue

            status_val = row[status_idx].strip()
            if "EGFR" in status_val:
                label = "EGFR_mut"
            elif "KRAS" in status_val:
                label = "KRAS_mut"
            else:
                label = "Triple_Neg"

            valid_samples.append(gsm)
            labels.append(label)
            sample_table_map[gsm] = table_name

    N = len(valid_samples)
    print(f"[EBI_PARSER] Filtered to {N} valid primary lung tumors. Classes: {set(labels)}")

    # Read probe tables from zip archive
    probe_ids = None
    expression_columns = []
    with zipfile.ZipFile(zip_path, "r") as z:
        for idx, gsm in enumerate(valid_samples):
            fname = sample_table_map[gsm]
            with z.open(fname) as f:
                df = pd.read_csv(f, sep="\t", header=0)
                if probe_ids is None:
                    probe_ids = df["ID_REF"].values
                vals = df["VALUE"].values.astype(np.float32)
                expression_columns.append(vals)

    raw_mat = np.column_stack(expression_columns)  # (D, N)
    print(f"[EBI_PARSER] Assembled raw matrix: {raw_mat.shape[0]} probes x {raw_mat.shape[1]} samples.")

    # Transpose to (N, D)
    X = raw_mat.T.astype(np.float64)

    # Impute missing values label-blind
    if np.isnan(X).any():
        col_means = np.nanmean(X, axis=0)
        col_means = np.nan_to_num(col_means, nan=0.0)
        inds = np.where(np.isnan(X))
        X[inds] = np.take(col_means, inds[1])

    # Log2 transform if values appear to be raw intensities
    if np.nanmax(X) > 100.0:
        X = np.log2(np.maximum(X, 0.0) + 1.0)

    # Unsupervised feature selection by variance
    if max_genes and X.shape[1] > max_genes:
        variances = np.var(X, axis=0)
        top_idx = np.argsort(variances)[-max_genes:]
        top_idx.sort()
        X = X[:, top_idx]
        print(f"[EBI_PARSER] Selected top {X.shape[1]} features by unsupervised variance.")

    # Standardize features label-blind
    scaler = StandardScaler()
    X_standardized = scaler.fit_transform(X)

    # Encode integer labels for vault sealing
    le = LabelEncoder()
    encoded_labels = le.fit_transform(labels)

    # Seal labels in quarantine vault
    vault = LabelQuarantineVault(cohort_id, vault_dir)
    vault_fingerprint = vault.seal_labels(
        sample_accessions=valid_samples,
        labels=encoded_labels,
        label_names=list(le.classes_),
        label_category="B1_MUTATIONAL_DRIVER",
    )

    # Save UNLABELED feature matrix to disk
    output_dir.mkdir(parents=True, exist_ok=True)
    unlabeled_path = output_dir / f"{cohort_id}_unlabeled.npz"
    np.savez_compressed(
        unlabeled_path,
        X=X_standardized,
        sample_accessions=np.array(valid_samples),
        n_clusters=len(le.classes_),
    )
    print(f"[EBI_PARSER] Saved quarantined unlabeled matrix to {unlabeled_path} (Shape: {X_standardized.shape}).")

    meta = {
        "cohort_id": cohort_id,
        "N": int(N),
        "D": int(X_standardized.shape[1]),
        "K": int(len(le.classes_)),
        "classes": list(le.classes_),
        "vault_fingerprint": vault_fingerprint,
        "unlabeled_path": str(unlabeled_path),
        "matrix_sha256": hashlib.sha256(X_standardized.tobytes()).hexdigest(),
    }
    return X_standardized, vault_fingerprint, meta
