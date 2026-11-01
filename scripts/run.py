#!/usr/bin/env python3
"""
CLI experiment runner for ICC clustering benchmarks.

Usage:
    python scripts/run.py --config configs/default.yaml
    python scripts/run.py --algorithms icc_v2 kmeans --datasets synthetic --seeds 42 43 44
"""

import argparse
import sys
from pathlib import Path

# Ensure src is on python path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from icc.benchmarks import BenchmarkRunner
from icc.utils import configure_logging

logger = configure_logging()


def parse_args():
    parser = argparse.ArgumentParser(description="Run ICC clustering benchmark experiments.")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/default.yaml",
        help="Path to YAML configuration file.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results/experiments",
        help="Directory to save experiment results.",
    )
    parser.add_argument(
        "--algorithms",
        nargs="+",
        help="Override list of algorithms to execute.",
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        help="Override list of datasets to evaluate.",
    )
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        help="Override list of random seeds.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    config_path = Path(args.config)

    override_config = {}
    if config_path.exists():
        runner = BenchmarkRunner(config_path, output_dir=args.output_dir)
    else:
        logger.warning(f"Config '{config_path}' not found, using default settings.")
        runner = BenchmarkRunner(override_config, output_dir=args.output_dir)

    if args.algorithms:
        runner.algorithms = args.algorithms
    if args.datasets:
        runner.datasets = args.datasets
    if args.seeds:
        runner.seeds = args.seeds

    logger.info(f"Running algorithms={runner.algorithms} on datasets={runner.datasets} with seeds={runner.seeds}")
    results = runner.run_all()
    logger.info(f"Completed {len(results)} experiment runs successfully.")


if __name__ == "__main__":
    main()
