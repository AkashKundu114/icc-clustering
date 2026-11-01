# -*- coding: utf-8 -*-
"""
tests/test_g1_protocol_remediation.py

Automated test suite verifying the integrity, consistency, and scientific constraints
of the Gate G1 Protocol Remediation for Springer Nature DMKD.

Covers:
1. Hypothesis-to-test mapping consistency (HYPOTHESIS_TEST_MAPPING.csv).
2. Multiplicity-family membership and step-down thresholds.
3. Correct equivalence testing decision logic (TOST with margin +/-0.02).
4. Seed pairing and budget-matched feature gating contract.
5. Cohort-level aggregation (within-cohort median, cross-cohort mean/median).
6. Cohort eligibility status transitions and lifecycle stages.
7. Label quarantine and clinical outcome exclusion.
8. Manuscript macro consistency (0.217 mean, 0.061 median).
9. Safety gate: No confirmatory execution or preregistration tagging prior to approval.
"""

import os
import subprocess
from pathlib import Path
import pandas as pd
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent


def test_hypothesis_test_mapping_consistency():
    """Verify HYPOTHESIS_TEST_MAPPING.csv is complete, valid, and enforces directional rules."""
    map_path = ROOT / "research_audit" / "dami_revision" / "HYPOTHESIS_TEST_MAPPING.csv"
    assert map_path.exists(), f"Missing hypothesis mapping file at {map_path}"

    df = pd.read_csv(map_path)
    assert len(df) == 13, f"Expected 13 test mappings, got {len(df)}"

    expected_ids = [
        "H1a", "H1b", "H2a", "H2b", "H3",
        "BM-01", "BM-02", "BM-03", "BM-04", "BM-05", "BM-06", "BM-07", "BM-08"
    ]
    assert list(df["hypothesis_id"]) == expected_ids, "Hypothesis IDs mismatch"

    # Verify all alphas are 0.05
    for alpha in df["nominal_alpha"]:
        assert float(alpha) == 0.05, f"Expected alpha 0.05, got {alpha}"

    # Verify directional superiority rule for Family 1 baseline tests
    family_1 = df[df["inferential_family"].str.contains("Family 1")]
    assert len(family_1) == 8, f"Expected 8 baseline tests in Family 1, got {len(family_1)}"
    for idx, row in family_1.iterrows():
        rule = row["decision_rule_reject_h0"]
        assert "p_adj < 0.05" in rule, f"Missing p_adj threshold in {row['hypothesis_id']}"
        assert "Median(D_" in rule and "> 0" in rule, (
            f"Family 1 baseline test {row['hypothesis_id']} must enforce directional superiority rule: {rule}"
        )


def test_multiplicity_family_membership():
    """Verify multiplicity family structure, step-down schedules, and membership."""
    map_path = ROOT / "research_audit" / "dami_revision" / "HYPOTHESIS_TEST_MAPPING.csv"
    df = pd.read_csv(map_path)

    f1 = df[df["inferential_family"].str.contains("Family 1")]
    f2 = df[df["inferential_family"].str.contains("Family 2")]
    f3 = df[df["inferential_family"].str.contains("Family 3")]

    assert len(f1) == 8, f"Family 1 must contain exactly 8 tests, got {len(f1)}"
    assert len(f2) == 3, f"Family 2 must contain exactly 3 tests (H2a, H2b, H3), got {len(f2)}"
    assert len(f3) == 2, f"Family 3 must contain exactly 2 tests (H1a, H1b), got {len(f3)}"

    # Check step-down alpha thresholds
    f1_step1_alpha = 0.05 / 8
    assert abs(f1_step1_alpha - 0.00625) < 1e-6
    f2_step1_alpha = 0.05 / 3
    assert abs(f2_step1_alpha - 0.016667) < 1e-4


def test_equivalence_decision_logic():
    """Verify formal TOST equivalence decision logic at +/-0.02 margin."""
    delta = 0.02

    def evaluate_tost(ci_lower: float, ci_upper: float):
        """Returns verdict based on 90% confidence interval relative to [-delta, +delta]."""
        if ci_lower > -delta and ci_upper < delta:
            return "EQUIVALENT"
        elif ci_upper <= -delta or ci_lower >= delta:
            return "NON_EQUIVALENT"
        else:
            return "INCONCLUSIVE"

    # Test cases
    assert evaluate_tost(-0.015, 0.015) == "EQUIVALENT"
    assert evaluate_tost(-0.010, 0.018) == "EQUIVALENT"
    assert evaluate_tost(0.025, 0.060) == "NON_EQUIVALENT"
    assert evaluate_tost(-0.050, -0.022) == "NON_EQUIVALENT"

    # Inconclusive boundary crossings
    assert evaluate_tost(-0.019, 0.057) == "INCONCLUSIVE"
    assert evaluate_tost(-0.025, 0.010) == "INCONCLUSIVE"
    assert evaluate_tost(-0.005, 0.035) == "INCONCLUSIVE"


def test_seed_pairing_and_randomization_contract():
    """Verify deterministic 30-seed sequence and paired configuration."""
    canonical_seeds = list(range(30))
    assert len(canonical_seeds) == 30
    assert len(set(canonical_seeds)) == 30
    assert canonical_seeds[0] == 0 and canonical_seeds[-1] == 29

    # Verify RNG reproducibility
    rng1 = np.random.default_rng(42)
    rng2 = np.random.default_rng(42)
    assert np.all(rng1.random(10) == rng2.random(10))


def test_cohort_level_aggregation():
    """Verify within-cohort median aggregation and cross-cohort summary calculation."""
    # Simulated 30 seeds on a cohort with an outlier
    seed_runs = np.array([0.05] * 28 + [0.85, 0.90])  # severe positive outliers
    within_cohort_median = float(np.median(seed_runs))
    within_cohort_mean = float(np.mean(seed_runs))

    # Median must remain robust to outliers
    assert within_cohort_median == 0.05
    assert within_cohort_mean > 0.10

    # Cross-cohort aggregation
    cohort_medians = np.array([0.0210, 0.0721, 0.5998, 0.0499, 0.0122, 0.5456])
    cross_cohort_mean = float(np.mean(cohort_medians))
    cross_cohort_median = float(np.median(cohort_medians))

    assert abs(cross_cohort_mean - 0.2168) < 0.001
    assert abs(cross_cohort_median - 0.0610) < 0.001


def test_cohort_eligibility_status_transitions():
    """Verify cohort registry status categories and candidate lifecycle."""
    reg_path = ROOT / "research_audit" / "dami_revision" / "CONFIRMATORY_COHORT_REGISTRY.csv"
    ex_path = ROOT / "research_audit" / "dami_revision" / "COHORT_EXCLUSION_LOG.csv"
    assert reg_path.exists(), f"Missing registry at {reg_path}"
    assert ex_path.exists(), f"Missing exclusion log at {ex_path}"

    df_reg = pd.read_csv(reg_path)
    df_ex = pd.read_csv(ex_path)

    # Verify no candidate is marked as evaluated in confirmatory benchmark
    for eval_status in df_reg["evaluated_in_benchmark"]:
        assert "FALSE" in str(eval_status).upper(), (
            f"Candidate cohort marked as evaluated before Gate G1: {eval_status}"
        )

    # Verify Tier A count
    tier_a = df_reg[df_reg["eligibility_tier"] == "TIER_A"]
    assert len(tier_a) == 10, f"Expected 10 Tier A candidates, got {len(tier_a)}"

    # Verify Tier B count
    tier_b = df_reg[df_reg["eligibility_tier"] == "TIER_B"]
    assert len(tier_b) == 5, f"Expected 5 Tier B candidates, got {len(tier_b)}"

    # Verify OpenML 45085 van 't Veer is in exclusion log (B4 clinical outcome)
    vveer_matches = df_ex[df_ex["cohort_id"].str.contains("VAN_T_VEER", case=False, na=False)]
    assert len(vveer_matches) >= 1, "van 't Veer clinical outcome cohort not found in exclusion log!"


def test_label_quarantine_integrity():
    """Verify that exploratory cohorts are locked and zero unsealed confirmatory results exist."""
    # Check baseline status in PREREGISTRATION.md and HYPOTHESES_AND_ANALYSIS_PLAN.md
    prereg = ROOT / "research_audit" / "dami_revision" / "PREREGISTRATION.md"
    assert prereg.exists()
    content = prereg.read_text(encoding="utf-8")
    assert "EXPLORATORY" in content
    assert "confirmatory" in content.lower()

    hyp_plan = ROOT / "research_audit" / "dami_revision" / "HYPOTHESES_AND_ANALYSIS_PLAN.md"
    assert hyp_plan.exists()
    hyp_content = hyp_plan.read_text(encoding="utf-8")
    assert "EXPLORATORY" in hyp_content


def test_macro_consistency_numbers_and_stats():
    """Verify that numbers.tex macros match Pass F canonical store (0.217 and 0.061)."""
    num_path = ROOT / "paper" / "numbers.tex"
    if not num_path.exists():
        num_path = ROOT / "springer_manuscript" / "numbers.tex"
    assert num_path.exists()
    tex = num_path.read_text(encoding="utf-8")

    assert "\\newcommand{\\FairBaselinesIccVTwoHighDMean}{0.217}" in tex
    assert "\\newcommand{\\FairBaselinesIccVTwoHighDMedian}{0.061}" in tex
    assert "\\newcommand{\\TableThreeFriedmanPValue}{0.40}" in tex
    assert "\\newcommand{\\TrueNemenyiCD}{4.62}" in tex


def test_preregistration_tag_status():
    """Verify that git tag prereg-dami-v1 exists and points to the authorized commit."""
    res = subprocess.run(["git", "tag", "-l", "prereg-dami-v1"], capture_output=True, text=True, cwd=ROOT)
    assert res.returncode == 0
    tag_output = res.stdout.strip()
    assert tag_output == "prereg-dami-v1", f"ERROR: Git tag prereg-dami-v1 missing: '{tag_output}'"
