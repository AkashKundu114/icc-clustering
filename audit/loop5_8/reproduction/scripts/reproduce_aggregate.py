"""Recompute aggregate descriptive arithmetic; does not use raw repeated runs.

Expected input: ../inputs/subsample_stability_summary.csv with dataset,
model, subsample_stability, and subsample_accuracy columns.
Output: one JSON object to stdout. No files are written.
"""
from pathlib import Path
import csv
import json
import statistics

HERE = Path(__file__).resolve().parent.parent
INPUT = HERE / "inputs" / "subsample_stability_summary.csv"


def main():
    with INPUT.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit(f"No aggregate rows in {INPUT}")
    needed = {"dataset", "model", "subsample_stability", "subsample_accuracy"}
    if not needed.issubset(rows[0]):
        raise SystemExit(f"Missing columns: {sorted(needed - set(rows[0]))}")
    gaps = []
    stability = []
    ari = []
    for row in rows:
        s, a = float(row["subsample_stability"]), float(row["subsample_accuracy"])
        stability.append(s)
        ari.append(a)
        gaps.append(s - a)
    result = {
        "interpretation": "Aggregate-only arithmetic; not repeat-level reconstruction.",
        "n_rows": len(rows),
        "n_datasets": len({r["dataset"] for r in rows}),
        "n_methods": len({r["model"] for r in rows}),
        "mean_stability": statistics.mean(stability),
        "mean_external_ari": statistics.mean(ari),
        "mean_gap": statistics.mean(gaps),
        "median_gap": statistics.median(gaps),
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
