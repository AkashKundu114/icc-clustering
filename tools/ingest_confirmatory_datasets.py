#!/usr/bin/env python3
"""
tools/ingest_confirmatory_datasets.py
Ingestion, Label Quarantine Sealing, and Feature Matrix Generation for Confirmatory Cohorts.
"""

from pathlib import Path
import numpy as np
import json
import re
from icc.confirmatory.parser import parse_geo_series_matrix

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw" / "cohort_discovery"
UNLABELED_DIR = ROOT / "data" / "confirmatory" / "unlabeled"
VAULT_DIR = ROOT / "data" / "confirmatory" / "vault"


def extract_gse42568_labels(headers, accessions):
    """
    Extracts biological intrinsic classes for Clarke GSE42568 breast cohort.
    Restricts to the N=104 primary breast cancer specimens, excluding healthy normal controls.
    Ground truth: ER receptor status (ER+ vs ER-) and Grade (1, 2, 3).
    """
    tissue_row = None
    er_row = None
    grade_row = None
    
    for k, v in headers.items():
        if not tissue_row and any("tissue:" in str(x) for x in v):
            tissue_row = v
        if not er_row and any("er_status:" in str(x) for x in v):
            er_row = v
        if not grade_row and any("grade:" in str(x) for x in v):
            grade_row = v

    mask = []
    labels = []
    for i in range(len(accessions)):
        tissue = tissue_row[i].lower() if tissue_row else ""
        if "normal" in tissue:
            mask.append(False)
            labels.append("NORMAL_EXCLUDED")
        else:
            mask.append(True)
            er_val = er_row[i].strip() if er_row else "NA"
            if "1" in er_val:
                mask.append(True)
                labels.append("ER_Positive")
            elif "0" in er_val:
                mask.append(True)
                labels.append("ER_Negative")
            else:
                mask.append(False)
                labels.append("ER_UNKNOWN_EXCLUDED")

    class_names = sorted(list(set(l for i, l in enumerate(labels) if mask[i])))
    return mask, labels, class_names, "B3_RECEPTOR_STATUS"


def extract_gse19188_labels(headers, accessions):
    """
    Extracts histological tumor types for Hou GSE19188 NSCLC cohort.
    Ground truth: N=91 tumor specimens across 3 distinct histologies (ADC, SCC, LCC),
    excluding healthy adjacent controls.
    """
    cell_row = None
    for k, v in headers.items():
        if any("cell type:" in str(x) for x in v):
            cell_row = v
            break

    mask = []
    labels = []
    for i in range(len(accessions)):
        c_val = cell_row[i].strip() if cell_row else ""
        if "healthy" in c_val.lower():
            mask.append(False)
            labels.append("HEALTHY_EXCLUDED")
        elif "scc" in c_val.lower():
            mask.append(True)
            labels.append("SCC_Squamous")
        elif "lcc" in c_val.lower():
            mask.append(True)
            labels.append("LCC_LargeCell")
        elif "adc" in c_val.lower():
            mask.append(True)
            labels.append("ADC_Adeno")
        else:
            mask.append(False)
            labels.append("OTHER")

    class_names = sorted(list(set(l for i, l in enumerate(labels) if mask[i])))
    return mask, labels, class_names, "B1_HISTOLOGICAL_SUBTYPE"


def extract_gse21653_labels(headers, accessions):
    """
    Extracts Perou-Sorlie PAM50 intrinsic subtypes for Sabatier GSE21653 breast cohort.
    Ground truth: N=266 tumor biopsies across 5 intrinsic subtypes:
    LuminalA, LuminalB, Basal, Normal, ERBB2.
    """
    mask = []
    labels = []
    for i in range(len(accessions)):
        sub = None
        for k, v in headers.items():
            if "characteristics" in k and i < len(v) and "molecular subtype:" in v[i]:
                sub = v[i].split("molecular subtype:")[1].strip().strip('"')
                break
        if sub:
            mask.append(True)
            labels.append(sub)
        else:
            mask.append(False)
            labels.append("UNKNOWN")

    class_names = sorted(list(set(l for i, l in enumerate(labels) if mask[i])))
    return mask, labels, class_names, "B1_INTRINSIC_SUBTYPE"


def extract_gse32894_labels(headers, accessions):
    """
    Extracts Sjodahl Lund molecular subtypes for GSE32894 urothelial bladder carcinoma.
    Ground truth: N=308 tumor resections across 7 discrete Lund taxonomy subtypes:
    MS1a, MS1b, MS2a.1, MS2a.2, MS2b.1, MS2b2.1, MS2b2.2.
    """
    mask = []
    labels = []
    for i in range(len(accessions)):
        sub = None
        for k, v in headers.items():
            if "characteristics" in k and i < len(v) and "molecular_subtype:" in v[i]:
                sub = v[i].split("molecular_subtype:")[1].strip().strip('"')
                break
        if sub:
            mask.append(True)
            labels.append(sub)
        else:
            mask.append(False)
            labels.append("UNKNOWN")

    class_names = sorted(list(set(l for i, l in enumerate(labels) if mask[i])))
    return mask, labels, class_names, "B1_LUND_MOLECULAR_TAXONOMY"


def main():
    UNLABELED_DIR.mkdir(parents=True, exist_ok=True)
    VAULT_DIR.mkdir(parents=True, exist_ok=True)

    ingested = []

    # 1. GSE42568
    gse42568_raw = RAW_DIR / "GSE42568" / "GSE42568_series_matrix.txt.gz"
    if gse42568_raw.exists():
        X, fp, meta = parse_geo_series_matrix(
            gse42568_raw, "GSE42568", extract_gse42568_labels, UNLABELED_DIR, VAULT_DIR, max_genes=10000
        )
        ingested.append(meta)

    # 2. GSE19188
    gse19188_raw = RAW_DIR / "GSE19188" / "GSE19188_series_matrix.txt.gz"
    if gse19188_raw.exists():
        X, fp, meta = parse_geo_series_matrix(
            gse19188_raw, "GSE19188", extract_gse19188_labels, UNLABELED_DIR, VAULT_DIR, max_genes=10000
        )
        ingested.append(meta)

    # 3. GSE21653
    gse21653_raw = RAW_DIR / "GSE21653" / "GSE21653_series_matrix.txt.gz"
    if gse21653_raw.exists():
        X, fp, meta = parse_geo_series_matrix(
            gse21653_raw, "GSE21653", extract_gse21653_labels, UNLABELED_DIR, VAULT_DIR, max_genes=10000
        )
        ingested.append(meta)

    # 4. GSE32894
    gse32894_raw = RAW_DIR / "GSE32894" / "GSE32894_series_matrix.txt.gz"
    if gse32894_raw.exists():
        X, fp, meta = parse_geo_series_matrix(
            gse32894_raw, "GSE32894", extract_gse32894_labels, UNLABELED_DIR, VAULT_DIR, max_genes=10000
        )
        ingested.append(meta)

    manifest_file = UNLABELED_DIR / "ingested_cohorts_manifest.json"
    manifest_file.write_text(json.dumps(ingested, indent=2), encoding="utf-8")
    print(f"\n[+] Completed ingestion for {len(ingested)} confirmatory cohorts.")
    print(f"[+] Saved manifest to {manifest_file}")


if __name__ == "__main__":
    main()
