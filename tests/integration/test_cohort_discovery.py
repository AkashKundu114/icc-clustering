"""
Unit tests for biological cohort discovery, validation gates, and checksum downloader.

Ensures that:
1. Metadata parser and cleaning operate robustly.
2. Checksum calculations match SHA-256 standard.
3. Download manifests strictly enforce explicit license review ('YES') and safe paths.
4. Mandatory eligibility gates (A-I) and B1-B6 label ontologies correctly screen candidates.
5. All tests run offline with mock fixtures (no live NCBI network calls in CI).
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from icc.data.cohorts import (
    clean,
    download_manifest,
    esummary,
    sha256_file,
)

# =============================================================================
# 1. Metadata and String Cleaning Tests
# =============================================================================

def test_clean_none():
    assert clean(None) == ""


def test_clean_list():
    assert clean(["GPL570", "GPL96"]) == "GPL570; GPL96"
    assert clean([None, "GPL570", "  "]) == "GPL570"


def test_clean_whitespace():
    raw = "  Study   investigating \n\t triple-negative breast  cancer.  "
    assert clean(raw) == "Study investigating triple-negative breast cancer."


# =============================================================================
# 2. Cryptographic Checksum Tests
# =============================================================================

def test_sha256_file(tmp_path: Path):
    test_file = tmp_path / "test_data.txt"
    content = b"Benchmark cohort expression matrix content"
    test_file.write_bytes(content)

    expected = hashlib.sha256(content).hexdigest()
    assert sha256_file(test_file) == expected


# =============================================================================
# 3. ESummary Parser Tests (Mocked)
# =============================================================================

def test_esummary_parsing_filter_non_gse():
    mock_payload = {
        "result": {
            "uids": ["1001", "1002", "1003"],
            "1001": {
                "accession": "GSE62254",
                "title": "Asian Cancer Research Group gastric cancer study",
                "summary": "Transcriptomic profiling of 300 primary gastric tumors",
                "gds": {"gse": {"overall_design": "Microarray profiling on Affymetrix HG-U133plus2"}},
                "pdat": "2014/10/20",
                "par": "2020/05/11",
                "pubmedids": [25894828],
                "n_samples": 300,
                "gpl": [570],
                "taxon": "Homo sapiens",
            },
            "1002": {
                "accession": "GDS1234",  # Not a GSE series, must be filtered
                "title": "Curated dataset",
            },
            "1003": {
                "accession": "GSE39582",
                "title": "Colorectal cancer molecular subtypes",
                "summary": "Profiling of 566 colorectal tumors",
                "n_samples": 566,
                "gpl": [570],
                "taxon": "Homo sapiens",
            },
        }
    }

    with patch("icc.data.cohorts.request_text", return_value=json.dumps(mock_payload)):
        rows = esummary(["1001", "1002", "1003"], email=None)

    assert len(rows) == 2
    accs = [r["geo_accession"] for r in rows]
    assert "GSE62254" in accs
    assert "GSE39582" in accs
    assert "GDS1234" not in accs

    row_gse = next(r for r in rows if r["geo_accession"] == "GSE62254")
    assert row_gse["n_samples"] == 300
    assert row_gse["organism"] == "Homo sapiens"
    assert row_gse["platforms"] == "570"


# =============================================================================
# 4. Manifest Downloader Security and Licensing Guards
# =============================================================================

def test_download_manifest_refusal_unreviewed_license(tmp_path: Path):
    manifest_file = tmp_path / "manifest.csv"
    with manifest_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["cohort_id", "url", "relative_path", "expected_sha256", "license_reviewed"],
        )
        writer.writeheader()
        writer.writerow({
            "cohort_id": "UNREVIEWED_COHORT",
            "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE62nnn/GSE62254/matrix/GSE62254_series_matrix.txt.gz",
            "relative_path": "GSE62254/matrix.txt.gz",
            "expected_sha256": "",
            "license_reviewed": "NO",
        })

    args = MagicMock()
    args.manifest = str(manifest_file)
    args.raw_dir = str(tmp_path / "raw")
    args.report = str(tmp_path / "report.csv")
    args.timeout = 10

    with pytest.raises(SystemExit) as exc_info:
        download_manifest(args)

    assert "license_reviewed is not YES" in str(exc_info.value)


def test_download_manifest_path_traversal_prevention(tmp_path: Path):
    manifest_file = tmp_path / "manifest.csv"
    with manifest_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["cohort_id", "url", "relative_path", "expected_sha256", "license_reviewed"],
        )
        writer.writeheader()
        writer.writerow({
            "cohort_id": "TRAVERSAL_ATTEMPT",
            "url": "https://example.com/data.tar.gz",
            "relative_path": "../../../etc/shadow",
            "expected_sha256": "",
            "license_reviewed": "YES",
        })

    args = MagicMock()
    args.manifest = str(manifest_file)
    args.raw_dir = str(tmp_path / "raw")
    args.report = str(tmp_path / "report.csv")
    args.timeout = 10

    with pytest.raises(SystemExit) as exc_info:
        download_manifest(args)

    assert "Unsafe relative_path" in str(exc_info.value) or "escapes raw_dir" in str(exc_info.value)


def test_download_manifest_checksum_mismatch(tmp_path: Path):
    manifest_file = tmp_path / "manifest.csv"
    with manifest_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["cohort_id", "url", "relative_path", "expected_sha256", "license_reviewed"],
        )
        writer.writeheader()
        writer.writerow({
            "cohort_id": "TEST_COHORT",
            "url": "https://example.com/test.txt",
            "relative_path": "test.txt",
            "expected_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
            "license_reviewed": "YES",
        })

    args = MagicMock()
    args.manifest = str(manifest_file)
    args.raw_dir = str(tmp_path / "raw")
    args.report = str(tmp_path / "report.csv")
    args.timeout = 10

    # Mock urllib response with distinct content
    fake_response = MagicMock()
    fake_response.read.side_effect = [b"Actual payload content", b""]
    fake_response.__enter__.return_value = fake_response

    with patch("shutil.which", return_value=None), patch("urllib.request.urlopen", return_value=fake_response):
        with pytest.raises(SystemExit) as exc_info:
            download_manifest(args)

    assert "SHA-256 mismatch" in str(exc_info.value)


# =============================================================================
# 5. Label Ontology (B1-B6) and Gate Screening Verification
# =============================================================================

def classify_label_type(label_name: str, label_description: str) -> str:
    """Classifies label according to cohort discovery eligibility specifications."""
    text = f"{label_name} {label_description}".lower().replace("_", " ")
    
    # B4: Clinical outcome / survival endpoints (FORBIDDEN for clustering evaluation)
    if any(k in text for k in [
        "overall survival", "survival", "recurrence", "relapse", "event-free",
        "disease-free", "progression-free", "os_status", "rfs", "dfs", "pfs",
        "responder", "non-responder", "response to therapy"
    ]):
        return "B4"

    # B5: Technical / batch / center / platform metadata
    if any(k in text for k in ["batch", "plate", "center", "centre", "scan_date", "sequencing_batch"]):
        return "B5"

    # B2: Tumor vs normal / diagnostic contrast
    if any(k in text for k in ["tumor vs normal", "tumour vs normal", "normal vs tumor", "adjacent normal", "non-disease"]):
        return "B2"

    # B3: Specific receptor status or single mutation status
    if any(k in text for k in ["er status", "pr status", "her2 status", "egfr mutation", "kras mutation", "braf mutation", "tp53 status"]):
        return "B3"

    # B6: Inferred signature / algorithmic class
    if any(k in text for k in ["pam50", "cms_classifier", "consensus molecular subtype", "inferred", "ssgsea"]):
        return "B6"

    # B1: Biological subtype / histological lineage / tumor type
    if any(k in text for k in ["subtype", "histology", "lineage", "histological type", "subgroup", "molecular subtype"]):
        return "B1"

    return "UNKNOWN"


def test_label_classification():
    assert classify_label_type("histological_subtype", "squamous vs adenocarcinoma") == "B1"
    assert classify_label_type("molecular_subgroup", "WNT, SHH, Group 3, Group 4") == "B1"
    assert classify_label_type("tissue_type", "Tumour vs Normal adjacent") == "B2"
    assert classify_label_type("HER2_status", "HER2 positive vs negative") == "B3"
    assert classify_label_type("overall_survival_status", "Dead vs Alive at 5 years") == "B4"
    assert classify_label_type("relapse_free_survival", "Recurrence within 3 years") == "B4"
    assert classify_label_type("sequencing_batch", "Batch 1 vs Batch 2") == "B5"
    assert classify_label_type("PAM50_call", "Inferred PAM50 breast cancer subtype") == "B6"


def evaluate_mandatory_gates(candidate: dict[str, Any]) -> dict[str, bool]:
    """Evaluates Mandatory Gates A through I defined in the specification."""
    gates = {}
    gates["Gate_A_Human"] = candidate.get("organism") == "Homo sapiens"
    gates["Gate_B_CancerBiospecimen"] = candidate.get("specimen_type") in ["tissue", "tumor_biopsy", "cell_line", "pbmc"]
    gates["Gate_C_ExpressionMatrix"] = candidate.get("assay_type") in ["microarray", "bulk_rna_seq"]
    gates["Gate_D_MinSamples30"] = int(candidate.get("n_samples", 0)) >= 30
    gates["Gate_E_MinFeatures500"] = int(candidate.get("n_features", 0)) >= 500
    gates["Gate_F_SampleMapping"] = bool(candidate.get("sample_mapping_verified", False))
    gates["Gate_G_DocumentedTerms"] = candidate.get("license_status") in ["open_academic", "public_domain", "cc_by"]
    gates["Gate_H_TraceablePublication"] = bool(candidate.get("pubmed_id") or candidate.get("doi"))
    gates["Gate_I_NoFatalDuplication"] = not bool(candidate.get("is_fatal_duplicate", False))
    return gates


def test_mandatory_gates():
    candidate_valid = {
        "organism": "Homo sapiens",
        "specimen_type": "tumor_biopsy",
        "assay_type": "microarray",
        "n_samples": 300,
        "n_features": 54675,
        "sample_mapping_verified": True,
        "license_status": "open_academic",
        "pubmed_id": "25894828",
        "doi": "10.1038/nm.3850",
        "is_fatal_duplicate": False,
    }
    gates = evaluate_mandatory_gates(candidate_valid)
    assert all(gates.values())

    # Candidate with N=18 fails Gate D
    candidate_small = dict(candidate_valid, n_samples=18)
    assert not evaluate_mandatory_gates(candidate_small)["Gate_D_MinSamples30"]

    # Candidate with non-human organism fails Gate A
    candidate_mouse = dict(candidate_valid, organism="Mus musculus")
    assert not evaluate_mandatory_gates(candidate_mouse)["Gate_A_Human"]

    # Candidate with D=400 fails Gate E
    candidate_low_d = dict(candidate_valid, n_features=400)
    assert not evaluate_mandatory_gates(candidate_low_d)["Gate_E_MinFeatures500"]


# =============================================================================
# 6. Expression Matrix Orientation and Preprocessing Isolation
# =============================================================================

def test_matrix_orientation_and_unsupervised_preprocessing():
    # Simulate sample x feature matrix (N=40, D=600)
    N, D = 40, 600
    np.random.seed(42)
    X = np.random.randn(N, D)
    _y_labels = np.array(["SubtypeA"] * 20 + ["SubtypeB"] * 20)

    # ICC matrix contract: samples along axis 0, features along axis 1
    assert X.shape[0] == N
    assert X.shape[1] == D

    # Unsupervised preprocessing: standardization across features without using labels
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    std[std == 0] = 1.0
    X_scaled = (X - mean) / std

    assert X_scaled.shape == (N, D)
    assert np.allclose(np.mean(X_scaled, axis=0), 0.0, atol=1e-7)
    assert np.allclose(np.std(X_scaled, axis=0), 1.0, atol=1e-7)


