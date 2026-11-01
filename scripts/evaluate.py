#!/usr/bin/env python3
"""
CLI evaluation and summary generator for ICC experiment results.

Usage:
    python scripts/evaluate.py --results results/experiments/run_*.json
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from icc.utils import configure_logging

logger = configure_logging()


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate and summarize benchmark results.")
    parser.add_argument(
        "--results",
        type=str,
        required=True,
        help="Path to JSON results file.",
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        help="Optional path to export summary CSV table.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    results_path = Path(args.results)
    if not results_path.exists():
        logger.error(f"Results file '{results_path}' does not exist.")
        sys.exit(1)

    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for item in data:
        metrics = item.get("metrics", {})
        rows.append({
            "dataset": item.get("dataset"),
            "algorithm": item.get("algorithm"),
            "seed": item.get("seed"),
            "ari": metrics.get("ari", np.nan),
            "nmi": metrics.get("nmi", np.nan),
            "ami": metrics.get("ami", np.nan),
            "runtime_sec": item.get("runtime_seconds", 0.0),
            "status": item.get("status"),
        })

    df = pd.DataFrame(rows)
    print("\n=== Experiment Results Summary ===")
    summary = df.groupby(["dataset", "algorithm"]).agg({
        "ari": ["mean", "std"],
        "nmi": ["mean", "std"],
        "runtime_sec": "mean",
    }).round(4)
    print(summary)

    if args.output_csv:
        summary.to_csv(args.output_csv)
        logger.info(f"Summary exported to {args.output_csv}")


if __name__ == "__main__":
    main()
