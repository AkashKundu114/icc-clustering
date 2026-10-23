"""
Forwarding wrapper to maintain single source of truth from Pass F results store.
See scripts/make_numbers_passF.py for full details.
"""
import sys
from pathlib import Path

# Ensure repo root and scripts/ are on path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.make_numbers_passF import main

if __name__ == "__main__":
    main()
