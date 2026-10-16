#!/usr/bin/env python3
"""Convenience root entrypoint forwarding to scripts/demo.py."""

import runpy
from pathlib import Path

if __name__ == "__main__":
    target = Path(__file__).resolve().parent / "scripts" / "demo.py"
    runpy.run_path(str(target), run_name="__main__")
