"""
Tests for Test Dataset Access Guard (data/guard.py).
"""

import os
import pytest
from nullconsensus.data.guard import verify_test_access_allowed, DataPeekingViolation

def test_guard_blocks_without_freeze_tag(monkeypatch):
    monkeypatch.delenv("FREEZE_TAG", raising=False)
    with pytest.raises(DataPeekingViolation, match="Rule R2 Violation: FREEZE_TAG is not set"):
        verify_test_access_allowed("unseen_test_dataset")

def test_guard_blocks_with_invalid_tag_prefix(monkeypatch):
    monkeypatch.setenv("FREEZE_TAG", "v1.0.0")
    with pytest.raises(DataPeekingViolation, match="does not begin with 'freeze-'"):
        verify_test_access_allowed("unseen_test_dataset")

def test_guard_blocks_with_nonexistent_tag(monkeypatch):
    monkeypatch.setenv("FREEZE_TAG", "freeze-nonexistent-tag-12345")
    with pytest.raises(DataPeekingViolation, match="does not exist in git history"):
        verify_test_access_allowed("unseen_test_dataset")
