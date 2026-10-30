"""
CICC Web Demo Launcher
======================
Run this script to launch the interactive Conformal Inductive Consensus Clustering
web application on http://127.0.0.1:8000.
"""

import sys
from pathlib import Path

# Ensure demo directory is in python path
cur_dir = Path(__file__).resolve().parent
if str(cur_dir) not in sys.path:
    sys.path.insert(0, str(cur_dir))

# Ensure repo root is in python path
repo_root = cur_dir.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

try:
    import uvicorn
except ImportError:
    print("Error: uvicorn is not installed. Run: pip install fastapi uvicorn")
    sys.exit(1)

if __name__ == "__main__":
    print("=" * 70)
    print("Launching CICC Interactive Showcase on http://127.0.0.1:8000")
    print("Features: Conformal Out-of-Sample Coverage, Decoy FDR Gating, Streaming Memory")
    print("=" * 70)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
