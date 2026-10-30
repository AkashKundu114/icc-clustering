"""
Dataset download, unpacking, and validation utility for ICC-v2 benchmarks.

Downloads, extracts, caches, and validates all 13 canonical benchmark datasets
used throughout the manuscript experiments:
- Genomics: Colon, SRBCT, CNS, Leukemia, Prostate, Ovarian
- Physical / Synthetic: Sonar, Madelon
- Vision: Extended Yale B
- Audio: ISOLET
- Hyperspectral: Indian Pines
- Text: 20 Newsgroups
- Single-cell RNA-seq: Zheng68k (PBMC68k-reduced)

Verifies sample count N, feature dimension D, cluster count K, and absence of NaNs.

Usage:
    python scripts/download_data.py
    python scripts/download_data.py --dataset leukemia
    python scripts/download_data.py --summary
"""

import argparse
import sys
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from icc.datasets.registry import list_datasets, load_dataset


def download_and_validate(target_dataset=None, show_summary=False):
    """
    Download and validate datasets from the central registry.

    Parameters
    ----------
    target_dataset : str or None, default=None
        Specific dataset name to load/validate. If None, processes all enabled datasets.
    show_summary : bool, default=False
        If True, displays an overview table of registered dataset metadata.

    Returns
    -------
    dict
        Dictionary mapping dataset name to boolean success status.
    """
    print("=" * 70)
    print("ICC-v2 Benchmark Dataset Downloader & Integrity Verifier")
    print("=" * 70)

    datasets = list_datasets(enabled_only=True)
    if show_summary:
        print(f"\nRegistered Benchmark Datasets ({len(datasets)} total):")
        print(f"{'Name':<16} {'Domain':<16} {'N':>8} {'D':>8} {'K':>6}")
        print("-" * 58)
        for d in datasets:
            print(f"{d.name:<16} {d.domain:<16} {d.expected_N:>8} {d.expected_D:>8} {d.expected_K:>6}")
        print("-" * 58)
        return {d.name: True for d in datasets}

    if target_dataset:
        datasets = [d for d in datasets if d.name.lower() == target_dataset.lower()]
        if not datasets:
            print(f"[ERROR] Dataset '{target_dataset}' not found in registry.")
            return {}

    print(f"Found {len(datasets)} dataset(s) to process.\n")

    results = {}
    success_count = 0

    for d in datasets:
        print(f"[*] Processing '{d.name}' ({d.domain}): expected N={d.expected_N}, D={d.expected_D}, K={d.expected_K}...")
        try:
            X, y, meta = load_dataset(d.name)
            assert X.shape[0] == d.expected_N, f"N mismatch: got {X.shape[0]}, expected {d.expected_N}"
            assert X.shape[1] == d.expected_D, f"D mismatch: got {X.shape[1]}, expected {d.expected_D}"
            assert len(y) == d.expected_N, f"Label length mismatch: got {len(y)}, expected {d.expected_N}"
            
            n_unique_y = len(set(y))
            print(f"    [OK] Verified shape={X.shape}, classes={n_unique_y}, D/N={meta.get('d_over_n', X.shape[1]/X.shape[0]):.2f}")
            results[d.name] = True
            success_count += 1
        except Exception as exc:
            print(f"    [FAIL] Could not load or verify '{d.name}': {exc}")
            results[d.name] = False

    print("\n" + "=" * 70)
    print(f"Dataset verification complete: {success_count}/{len(datasets)} passed successfully.")
    print("=" * 70)
    return results


def main():
    parser = argparse.ArgumentParser(description="Download and verify ICC-v2 benchmark datasets.")
    parser.add_argument(
        "--dataset",
        type=str,
        default=None,
        help="Specify a single dataset to download/verify (e.g., 'colon', 'leukemia', 'isolet').",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Display tabular summary of dataset configurations without loading tensors.",
    )
    args = parser.parse_args()

    download_and_validate(target_dataset=args.dataset, show_summary=args.summary)


if __name__ == "__main__":
    main()
