"""
src/icc/confirmatory/parser.py
Series Matrix Parser and Label-Quarantined Feature Matrix Extractor.

Parses NCBI GEO Series Matrix files (.txt.gz), extracts high-dimensional
expression matrices (N samples x D features), and seals biological subtype
labels into the quarantine vault without exposing labels to models.
"""

import gzip
import hashlib
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

from icc.confirmatory.vault import LabelQuarantineVault


def parse_geo_series_matrix(
    matrix_path: Path,
    cohort_id: str,
    label_extractor_fn,
    output_dir: Path,
    vault_dir: Path,
    max_genes: Optional[int] = 10000,
) -> Tuple[np.ndarray, str, Dict[str, Any]]:
    """
    Parses a series matrix file, extracts unlabeled X, and seals labels in vault.

    Parameters
    ----------
    matrix_path : Path
        Path to series_matrix.txt.gz.
    cohort_id : str
        Cohort identifier (e.g., 'GSE42568', 'GSE19188').
    label_extractor_fn : callable
        Function taking (metadata_dict, sample_accessions) and returning
        (valid_sample_mask, label_strings, class_names, label_category).
    output_dir : Path
        Directory to save unlabeled matrix.
    vault_dir : Path
        Directory to store the sealed label vault.
    max_genes : int, optional
        If D > max_genes, retain top max_genes by unsupervised variance.

    Returns
    -------
    X : np.ndarray of shape (N, D)
        Unlabeled, standardized feature matrix.
    vault_fingerprint : str
        SHA-256 fingerprint of the sealed label vault.
    meta : dict
        Provenance and dimensionality metadata.
    """
    matrix_path = Path(matrix_path)
    if not matrix_path.exists():
        raise FileNotFoundError(f"Missing matrix file at {matrix_path}")

    sample_accessions: List[str] = []
    metadata_headers: Dict[str, List[str]] = {}
    expression_data: List[List[float]] = []
    gene_ids: List[str] = []

    print(f"[PARSER] Ingesting {matrix_path.name} for cohort {cohort_id}...")
    with gzip.open(matrix_path, "rt", encoding="utf-8", errors="replace") as f:
        in_matrix = False
        for line in f:
            if not in_matrix:
                if line.startswith("!Sample_geo_accession"):
                    sample_accessions = [s.strip().strip('"') for s in line.strip().split("\t")[1:]]
                elif line.startswith("!Sample_"):
                    parts = line.strip().split("\t")
                    key = parts[0].strip()
                    vals = [v.strip().strip('"') for v in parts[1:]]
                    if key not in metadata_headers:
                        metadata_headers[key] = vals
                    else:
                        # Append characteristics rows
                        metadata_headers[f"{key}__row_{len(metadata_headers)}"] = vals
                elif line.startswith("!series_matrix_table_begin"):
                    in_matrix = True
                    continue
            else:
                if line.startswith("!series_matrix_table_end"):
                    break
                if line.startswith('"ID_REF"') or line.startswith("ID_REF"):
                    continue
                parts = line.strip().split("\t")
                if len(parts) < len(sample_accessions) + 1:
                    continue
                gene_id = parts[0].strip().strip('"')
                try:
                    vals = [float(v) if v not in ("", "null", "NA", "NaN") else np.nan for v in parts[1:]]
                    if len(vals) == len(sample_accessions):
                        expression_data.append(vals)
                        gene_ids.append(gene_id)
                except ValueError:
                    continue

    raw_mat = np.array(expression_data, dtype=np.float32)  # (D, N)
    print(f"[PARSER] Read raw expression matrix: {raw_mat.shape[0]} probes x {raw_mat.shape[1]} samples.")

    # Transpose to (N, D)
    raw_X = raw_mat.T  # (N, D)

    # Extract labels using cohort-specific metadata extractor
    mask, raw_labels, class_names, label_category = label_extractor_fn(metadata_headers, sample_accessions)
    
    # Filter valid samples
    X_filtered = raw_X[mask]
    valid_accessions = [sample_accessions[i] for i in range(len(sample_accessions)) if mask[i]]
    valid_labels = [raw_labels[i] for i in range(len(raw_labels)) if mask[i]]

    N, D = X_filtered.shape
    print(f"[PARSER] Filtered to {N} valid biological samples with verified labels.")

    # Handle missing values label-blind
    if np.isnan(X_filtered).any():
        col_means = np.nanmean(X_filtered, axis=0)
        col_means = np.nan_to_num(col_means, nan=0.0)
        inds = np.where(np.isnan(X_filtered))
        X_filtered[inds] = np.take(col_means, inds[1])

    # Unsupervised log2 transform if values appear to be raw intensities (> 100)
    if np.nanmax(X_filtered) > 100.0:
        X_filtered = np.log2(np.maximum(X_filtered, 0.0) + 1.0)

    # Unsupervised feature selection by variance if D > max_genes
    if max_genes and D > max_genes:
        variances = np.var(X_filtered, axis=0)
        top_idx = np.argsort(variances)[-max_genes:]
        top_idx.sort()
        X_filtered = X_filtered[:, top_idx]
        D = X_filtered.shape[1]
        print(f"[PARSER] Selected top {D} features by unsupervised variance.")

    # Standardize features label-blind
    scaler = StandardScaler()
    X_standardized = scaler.fit_transform(X_filtered)

    # Encode integer labels for vault sealing
    le = LabelEncoder()
    encoded_labels = le.fit_transform(valid_labels)

    # Seal labels in quarantine vault
    vault = LabelQuarantineVault(cohort_id, vault_dir)
    vault_fingerprint = vault.seal_labels(
        sample_accessions=valid_accessions,
        labels=encoded_labels,
        label_names=list(le.classes_),
        label_category=label_category,
    )

    # Save UNLABELED feature matrix to disk
    output_dir.mkdir(parents=True, exist_ok=True)
    unlabeled_path = output_dir / f"{cohort_id}_unlabeled.npz"
    np.savez_compressed(
        unlabeled_path,
        X=X_standardized,
        sample_accessions=np.array(valid_accessions),
        n_clusters=len(le.classes_),
    )
    print(f"[PARSER] Saved quarantined unlabeled matrix to {unlabeled_path} (Shape: {X_standardized.shape}).")

    meta = {
        "cohort_id": cohort_id,
        "N": int(N),
        "D": int(D),
        "K": int(len(le.classes_)),
        "classes": list(le.classes_),
        "vault_fingerprint": vault_fingerprint,
        "unlabeled_path": str(unlabeled_path),
        "matrix_sha256": hashlib.sha256(X_standardized.tobytes()).hexdigest(),
    }
    return X_standardized, vault_fingerprint, meta
