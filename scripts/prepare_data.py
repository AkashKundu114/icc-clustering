#!/usr/bin/env python3
"""
CLI dataset preparation utility for ICC benchmarks.

Usage:
    python scripts/prepare_data.py --list
    python scripts/prepare_data.py --dataset leukemia
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from icc.data import list_datasets, load_dataset
from icc.utils import configure_logging

logger = configure_logging()


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare benchmark datasets for ICC.")
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all registered benchmark datasets.",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        help="Name of dataset to fetch and verify.",
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default="data/cache",
        help="Local cache directory.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.list:
        datasets = list_datasets()
        print("Registered datasets:")
        for d in datasets:
            print(f"  - {d}")
        return

    if args.dataset:
        logger.info(f"Loading and verifying dataset '{args.dataset}'...")
        X, y, meta = load_dataset(args.dataset)
        logger.info(
            f"Successfully prepared '{args.dataset}': shape={X.shape}, classes={len(set(y))}, meta={meta.get('domain', 'general')}"
        )
    else:
        print("Please specify --dataset <name> or --list. Use --help for options.")


if __name__ == "__main__":
    main()
