"""
Legacy wrapper for scripts/download_data.py.

Retained for backward compatibility with existing command-line invocations
and automated test harnesses. Delegates directly to scripts/download_data.py.

Usage:
    python scripts/fetch_data.py
"""

import sys
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.download_data import main

if __name__ == "__main__":
    main()
