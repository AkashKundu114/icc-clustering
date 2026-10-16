"""
Master CLI Runner for Experiment 0 Suite: Consensus Stability Falsification.

Usage:
  python run_exp0.py --reproduce-plots   (re-renders all figures from cached CSVs)
  python run_exp0.py --run-full          (recomputes all sweeps and saves fresh CSVs + figures)
"""

import sys
from pathlib import Path

# Add exp0 directory to path to invoke master pipeline
exp0_dir = Path(__file__).resolve().parent
if str(exp0_dir) not in sys.path:
    sys.path.insert(0, str(exp0_dir))

from run_all import main

if __name__ == "__main__":
    main()
