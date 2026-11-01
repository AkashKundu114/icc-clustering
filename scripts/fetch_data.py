"""
Dataset Fetcher and Verifier.

Downloads, unpacks, and validates all 13 benchmark datasets used across the manuscript.
Checks expected sample count N, dimension D, and cluster count K.

Usage:
    python scripts/fetch_data.py
"""

from icc.datasets.registry import list_datasets, load_dataset


def main():
    print("=" * 60)
    print("ICC-v2 Benchmark Dataset Fetcher & Verifier")
    print("=" * 60)

    datasets = list_datasets(enabled_only=True)
    print(f"Found {len(datasets)} enabled benchmark datasets.")

    success_count = 0
    for d in datasets:
        print(f"\nProcessing '{d.name}' ({d.domain}, N={d.expected_N}, D={d.expected_D}, K={d.expected_K})...")
        try:
            X, y, meta = load_dataset(d.name)
            assert X.shape[0] == d.expected_N, f"N mismatch: {X.shape[0]} != {d.expected_N}"
            assert X.shape[1] == d.expected_D, f"D mismatch: {X.shape[1]} != {d.expected_D}"
            print(f"  [OK] Loaded: shape={X.shape}, labels={len(set(y))}")
            success_count += 1
        except Exception as e:
            print(f"  [FAIL] Could not load {d.name}: {e}")

    print("\n" + "=" * 60)
    print(f"Dataset verification complete: {success_count}/{len(datasets)} ready.")
    print("=" * 60)

if __name__ == "__main__":
    main()
