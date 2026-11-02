"""Tests for the supported public reproduction command scopes."""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_help_lists_only_supported_scopes():
    result = subprocess.run(
        [sys.executable, "scripts/reproduce.py", "--help"],
        cwd=ROOT, capture_output=True, text=True, check=False
    )
    assert result.returncode == 0
    assert "smoke" in result.stdout and "verify" in result.stdout
    assert "tables" not in result.stdout and "figures" not in result.stdout


@pytest.mark.parametrize("scope", ["tables", "figures", "full"])
def test_unsupported_reproduction_scopes_fail(scope):
    result = subprocess.run(
        [sys.executable, "scripts/reproduce.py", "--scope", scope],
        cwd=ROOT, capture_output=True, text=True, check=False
    )
    assert result.returncode != 0
    assert "executed" not in result.stdout.lower()
