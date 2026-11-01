"""CLI entry point for the ``icc-demo`` console script."""

import sys
from pathlib import Path

# Ensure root directory is in sys.path to find demo.py
_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from demo import main  # noqa: E402

if __name__ == "__main__":
    main()
