"""
Legacy wrapper for scripts/benchmark_scaling.py.

Retained for backward compatibility with existing replication workflows.
Delegates directly to scripts/benchmark_scaling.py.

Usage:
    python scripts/rerun_table4_timing.py
"""

import sys
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.benchmark_scaling import main

if __name__ == "__main__":
    main()
