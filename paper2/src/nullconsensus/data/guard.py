"""
Test Dataset Access Guard (data/guard.py).
Strictly enforces Rule R2: Prevents access to TEST datasets prior to git freeze tag.
"""

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

class DataPeekingViolation(Exception):
    """Raised when an unauthorized attempt is made to load TEST datasets before the freeze tag."""
    pass

def get_git_executable() -> str:
    git_path = shutil.which("git")
    if git_path:
        return git_path
    common_paths = [
        r"C:\Program Files\Git\cmd\git.exe",
        r"C:\Program Files\Git\bin\git.exe"
    ]
    for p in common_paths:
        if os.path.exists(p):
            return p
    return "git"

def verify_test_access_allowed(dataset_name: str) -> bool:
    """
    Verifies whether loading a TEST dataset is legally permitted under protocol R2.
    
    Conditions for access:
    1. FREEZE_TAG environment variable must be set.
    2. FREEZE_TAG must start with 'freeze-'.
    3. Git must recognize FREEZE_TAG as an existing tag.
    4. Working tree must be clean.
    
    Raises:
        DataPeekingViolation if any condition is violated.
    """
    freeze_tag = os.environ.get("FREEZE_TAG", "").strip()
    if not freeze_tag or not freeze_tag.startswith("freeze-"):
        raise DataPeekingViolation(
            f"ACCESS DENIED to TEST dataset '{dataset_name}'. "
            f"Rule R2 Violation: FREEZE_TAG is not set or does not begin with 'freeze-'. "
            f"TEST datasets are strictly sealed until Phase B5 freeze."
        )

    git_exe = get_git_executable()

    # Check git tag exists
    git_cmd = [git_exe, "tag", "-l", freeze_tag]
    try:
        res = subprocess.run(git_cmd, capture_output=True, text=True, check=True)
        if freeze_tag not in res.stdout.split():
            raise DataPeekingViolation(
                f"ACCESS DENIED to TEST dataset '{dataset_name}'. "
                f"Tag '{freeze_tag}' does not exist in git history."
            )
    except DataPeekingViolation:
        raise
    except Exception as e:
        raise DataPeekingViolation(f"Git verification failed for freeze tag '{freeze_tag}': {e}")

    # Check working tree is clean
    try:
        diff_res = subprocess.run([git_exe, "status", "--porcelain"], capture_output=True, text=True, check=True)
        if diff_res.stdout.strip():
            raise DataPeekingViolation(
                f"ACCESS DENIED to TEST dataset '{dataset_name}'. "
                f"Working tree is not clean (uncommitted changes detected)."
            )
    except DataPeekingViolation:
        raise
    except Exception as e:
        raise DataPeekingViolation(f"Git clean status check failed: {e}")

    # Log access
    log_dir = Path("results")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "test_access.log"
    timestamp = datetime.now().isoformat()
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] DATASET={dataset_name} FREEZE_TAG={freeze_tag}\n")

    return True
