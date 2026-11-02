#!/usr/bin/env python3
"""Reaggregate the two saved 13-dataset score tables supplied by the user.

This script verifies arithmetic and row structure only. It does not authenticate
that each row came from a fresh or comparable clustering fit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import scipy
from scipy.stats import friedmanchisquare, rankdata


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scores", nargs=2, required=True, type=Path,
                        metavar=("PASS_F_CSV", "COHIRF_CSV"),
                        help="The two historical CSV score sources")
    parser.add_argument("--output-dir", required=True, type=Path,
                        help="New or empty output directory")
    parser.add_argument("--expected-hashes", type=Path,
                        help="Optional JSON object mapping score CSV basenames to expected SHA-256 values")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        raise SystemExit(f"Output directory must be empty: {out}")

    frames = []
    inputs: list[dict[str, Any]] = []
    for path in args.scores:
        path = path.resolve()
        if not path.is_file():
            raise SystemExit(f"Missing score input: {path}")
        frame = pd.read_csv(path)
        required = {"dataset", "model", "seed", "ari"}
        if not required.issubset(frame.columns):
            raise SystemExit(f"{path.name} lacks columns {sorted(required - set(frame.columns))}")
        frames.append(frame[["dataset", "model", "seed", "ari"]].copy())
        inputs.append({"name": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)})
    hash_errors: list[str] = []
    if args.expected_hashes:
        expected_hashes = json.loads(args.expected_hashes.read_text(encoding="utf-8"))
        if not isinstance(expected_hashes, dict):
            raise SystemExit("Expected-hashes file must be a JSON object")
        actual_names = {item["name"] for item in inputs}
        for item in inputs:
            expected_hash = expected_hashes.get(item["name"])
            if expected_hash is None:
                hash_errors.append(f"expected SHA-256 not supplied: {item['name']}")
            elif str(expected_hash).lower() != item["sha256"].lower():
                hash_errors.append(f"SHA-256 mismatch: {item['name']}")
        for name in set(expected_hashes) - actual_names:
            hash_errors.append(f"expected-hash file not supplied: {name}")

    rows = pd.concat(frames, ignore_index=True)
    rows["dataset"] = rows.dataset.astype(str)
    rows["model"] = rows.model.astype(str)
    rows["seed"] = rows.seed.astype(str)
    rows["ari"] = pd.to_numeric(rows.ari, errors="coerce")
    datasets = sorted(rows.dataset.unique())
    methods = sorted(rows.model.unique())
    key_counts = rows.groupby(["dataset", "model", "seed"], dropna=False).size()
    cells = rows.groupby(["dataset", "model"], dropna=False).agg(
        n=("ari", "size"), mean_ari=("ari", "mean"), median_ari=("ari", "median"),
        sd_ari=("ari", "std"), zero_count=("ari", lambda values: int((values == 0).sum())),
        nonfinite=("ari", lambda values: int((~np.isfinite(values)).sum())),
    ).reset_index()
    complete_grid = len(cells) == len(datasets) * len(methods)
    expected = {dataset: (30 if dataset in {"cns", "colon", "leukemia", "ovarian", "prostate", "srbct"} else 10)
                for dataset in datasets}
    cells["expected_n_by_historical_schedule"] = cells.dataset.map(expected)
    cells["schedule_complete"] = cells.n == cells.expected_n_by_historical_schedule
    pivot = cells.pivot(index="dataset", columns="model", values="mean_ari").reindex(index=datasets, columns=methods)
    if pivot.isna().any().any():
        raise SystemExit("Friedman matrix has missing dataset-method cell means")
    ranks = np.vstack([rankdata(-pivot.loc[dataset].to_numpy(), method="average") for dataset in datasets])
    scipy_stat = p_value = formula_stat = None
    average_ranks: dict[str, float] = {}
    ranking: list[str] = []
    if len(datasets) >= 2 and len(methods) >= 2:
        scipy_stat, p_value = friedmanchisquare(*[pivot[method].to_numpy() for method in methods])
        n_datasets, n_methods = ranks.shape
        rank_sums = ranks.sum(axis=0)
        raw_q = 12 / (n_datasets * n_methods * (n_methods + 1)) * np.sum(rank_sums**2) - 3 * n_datasets * (n_methods + 1)
        tie_total = 0
        for _, row in pivot.iterrows():
            tie_total += sum(count**3 - count for count in Counter(row.tolist()).values() if count > 1)
        correction = 1 - tie_total / (n_datasets * (n_methods**3 - n_methods))
        formula_stat = raw_q / correction if correction else float("nan")
        average_ranks = dict(zip(methods, map(float, ranks.mean(axis=0))))
        ranking = [methods[index] for index in np.argsort(ranks.mean(axis=0))]
    cells.to_csv(out / "benchmark_cell_summary.csv", index=False)
    result = {
        "classification": "arithmetic recomputation from supplied score rows; no fits rerun or fit-event authentication",
        "inputs": inputs,
        "n_rows": len(rows), "n_datasets": len(datasets), "datasets": datasets,
        "n_methods": len(methods), "methods": methods, "n_dataset_method_cells": len(cells),
        "complete_grid": complete_grid,
        "incomplete_schedule_cells": cells.loc[~cells.schedule_complete,
                                                ["dataset", "model", "n", "expected_n_by_historical_schedule"]].to_dict("records"),
        "duplicate_dataset_method_seed_keys": int((key_counts > 1).sum()),
        "nonfinite_ari_rows": int((~np.isfinite(rows.ari)).sum()),
        "zero_ari_rows": int((rows.ari == 0).sum()),
        "hash_verification_errors": hash_errors,
        "friedman": {"chi_square_scipy": float(scipy_stat) if scipy_stat is not None else None,
                     "chi_square_tie_corrected_formula": float(formula_stat) if formula_stat is not None else None,
                     "df": len(methods) - 1 if methods else None,
                     "p_value": float(p_value) if p_value is not None else None,
                     "average_ranks": average_ranks, "best_to_worst": ranking},
        "software": {"python": __import__("sys").version, "numpy": np.__version__,
                     "pandas": pd.__version__, "scipy": scipy.__version__},
        "limitations": ["The historical score rows can include imported/copied values and ambiguous failures.",
                        "A complete score matrix does not establish fair or independent model executions.",
                        "Friedman results are a separate external-ARI benchmark, not stability evidence."],
    }
    (out / "benchmark_recalculation.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"n_rows": result["n_rows"], "n_dataset_method_cells": result["n_dataset_method_cells"],
                      "friedman": result["friedman"]}, indent=2))
    return 0 if (
        complete_grid
        and not result["incomplete_schedule_cells"]
        and result["duplicate_dataset_method_seed_keys"] == 0
        and result["nonfinite_ari_rows"] == 0
        and not hash_errors
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
