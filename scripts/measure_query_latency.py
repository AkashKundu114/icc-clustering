"""
Legacy wrapper for scripts/benchmark_latency.py.

Retained for backward compatibility with existing latency benchmark commands.
Delegates directly to scripts/benchmark_latency.py.

Usage:
    python scripts/measure_query_latency.py
"""

import sys
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.benchmark_latency import main

if __name__ == "__main__":
    main()
