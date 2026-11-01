# -*- coding: utf-8 -*-
"""
tests/test_benchmark_expansion_audit.py

Automated test suite verifying the completeness, schema conformity, and scientific
integrity of the multi-agent benchmark audit deliverables prepared for DMKD.
"""

import json
from pathlib import Path
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
AUDIT_DIR = ROOT / "research_audit" / "dami_revision"


def test_audit_deliverables_exist():
    """Verify that all 22 required audit deliverables exist and are non-empty."""
    required_files = [
        "ALGORITHM_IMPLEMENTATION_MATRIX.csv",
        "HYPERPARAMETER_REGISTRY.csv",
        "TRAINING_PIPELINE_AUDIT.md",
        "LEAKAGE_AND_FAILURE_AUDIT.md",
        "PREPROCESSING_PROVENANCE.csv",
        "LEAKAGE_CHECKLIST.md",
        "DATA_PIPELINE_AUDIT.md",
        "METRIC_DEFINITIONS.md",
        "EVALUATION_FRAMEWORK.md",
        "ROBUSTNESS_EXPERIMENT_MATRIX.csv",
        "COMPUTATIONAL_BENCHMARK_PLAN.md",
        "STATISTICAL_EVALUATION_PROTOCOL.md",
        "MULTIPLICITY_MAP.csv",
        "EFFECT_SIZE_AND_CI_REPORT.md",
        "COHORT_CANDIDATE_REGISTRY.csv",
        "COHORT_PROVENANCE_REPORT.md",
        "COHORT_OVERLAP_MATRIX.csv",
        "COHORT_EXPANSION_REPORT.md",
        "EXPERIMENT_RUNNER_AUDIT.md",
        "REPRODUCIBILITY_AND_EXECUTION_REPORT.md",
        "EXPERIMENT_MANIFEST_SCHEMA.json",
        "EXPERIMENTAL_RED_TEAM_REPORT.md",
    ]

    for fname in required_files:
        fpath = AUDIT_DIR / fname
        assert fpath.exists(), f"Missing required audit deliverable: {fname}"
        assert fpath.stat().st_size > 0, f"Audit deliverable is empty: {fname}"


def test_algorithm_matrix_integrity():
    """Verify ALGORITHM_IMPLEMENTATION_MATRIX.csv structure and content."""
    matrix_path = AUDIT_DIR / "ALGORITHM_IMPLEMENTATION_MATRIX.csv"
    df = pd.read_csv(matrix_path)
    assert len(df) >= 15, f"Expected at least 15 algorithm rows, got {len(df)}"
    required_cols = [
        "algorithm_name", "category", "target_paper_reference",
        "fitted_vs_calculated", "feature_selection_strategy", "seed_handling", "published_fidelity"
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing column {col} in algorithm matrix"


def test_cohort_registry_integrity():
    """Verify COHORT_CANDIDATE_REGISTRY.csv contains 29 entries with valid lifecycle statuses."""
    reg_path = AUDIT_DIR / "COHORT_CANDIDATE_REGISTRY.csv"
    df = pd.read_csv(reg_path)
    assert len(df) == 29, f"Expected exactly 29 cohorts in candidate registry, got {len(df)}"
    valid_statuses = {
        "CONFIRMATORY_ELIGIBLE",
        "ELIGIBILITY_REVIEWED",
        "DOWNLOADED",
        "EXCLUDED",
        "EXPLORATORY_LOCKED"
    }
    for status in df["lifecycle_status"]:
        assert status in valid_statuses, f"Invalid lifecycle status: {status}"


def test_manifest_schema_valid_json():
    """Verify EXPERIMENT_MANIFEST_SCHEMA.json is valid JSON Schema."""
    schema_path = AUDIT_DIR / "EXPERIMENT_MANIFEST_SCHEMA.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    assert schema.get("title") == "DMKDExperimentExecutionManifest"
    assert "properties" in schema
    assert "git_provenance" in schema["required"]
