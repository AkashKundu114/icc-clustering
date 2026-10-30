"""
Legacy wrapper for scripts/verify_identities.py.

Retained for backward compatibility with existing command-line audits.
Delegates directly to scripts/verify_identities.py.

Usage:
    python scripts/verify_determinacy_identity.py
"""

import sys
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.verify_identities import run_all_checks

if __name__ == "__main__":
    run_all_checks()
