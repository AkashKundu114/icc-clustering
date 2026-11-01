"""
Single Source of Truth LaTeX Macro Generator Wrapper.

Delegates execution to scripts/make_numbers_passF.py to compile all empirical
macros into numbers.tex across manuscript directories from frozen results.

Usage:
    python scripts/make_numbers.py
"""

import sys
from pathlib import Path

# Ensure repo root and scripts/ are on path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.make_numbers_passF import main  # noqa: E402

if __name__ == "__main__":
    main()

