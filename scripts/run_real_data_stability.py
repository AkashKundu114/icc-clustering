"""
Legacy wrapper for scripts/reproduce_stability.py.

Retained for backward compatibility with existing command-line workflows.
Delegates directly to scripts/reproduce_stability.py.

Usage:
    python scripts/run_real_data_stability.py
"""

import sys
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.reproduce_stability import main

if __name__ == "__main__":
    main()
