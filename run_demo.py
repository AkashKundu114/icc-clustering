"""
CICC Web Demo Launcher
======================
Run this script to launch the interactive Conformal Inductive Consensus Clustering
web application on http://127.0.0.1:8000.
"""

import sys
import uvicorn

if __name__ == "__main__":
    print("=" * 70)
    print("Launching CICC Interactive Showcase on http://127.0.0.1:8000")
    print("Features: Conformal Out-of-Sample Coverage, Decoy FDR Gating, Agent Memory")
    print("=" * 70)
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
