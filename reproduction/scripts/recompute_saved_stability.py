#!/usr/bin/env python3
"""Recompute six-cohort summaries from a user-supplied saved-output bundle.

This is a saved-partition verifier, not a clustering-run producer. It expects
the directory structure documented in reproduction/README.md. Inputs are not
included in this repository. NPY files use NumPy object serialization; only
run this script on an archive whose origin you trust and whose SHA-256 manifest
you have checked.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import pickle
import re
import sys
from collections import defaultdict
from importlib import import_module
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import adjusted_rand_score

COHORTS = ("cns", "colon", "leukemia", "ovarian", "prostate", "srbct")
METHODS = (
    "K-Means", "Ward", "Spectral", "FCM", "StdCons", "CoreHalo",
    "FCAG", "FastMVC", "CoHiRF", "UngatedAC", "GAC", "DEC",
)
MODES = ("real", "null")
REPEATS = tuple(range(30))
FILENAME = re.compile(r"(?P<dataset>[^_]+)_(?P<method>.+)_(?P<mode>real|null)_(?P<repeat>\d+)\.npy$")
try:
    _numpy_reconstruct = import_module("numpy._core.multiarray")._reconstruct
except (ImportError, AttributeError):  # NumPy 1.x compatibility
    _numpy_reconstruct = import_module("numpy.core.multiarray")._reconstruct


class NumpyOnlyUnpickler(pickle.Unpickler):
    """Restrict legacy object-NPY payloads to NumPy array reconstruction."""

    def find_class(self, module: str, name: str) -> Any:
        if module in {"numpy.core.multiarray", "numpy._core.multiarray"} and name == "_reconstruct":
            return _numpy_reconstruct
        if module == "numpy" and name == "ndarray":
            return np.ndarray
        if module == "numpy" and name == "dtype":
            return np.dtype
        raise pickle.UnpicklingError(f"blocked pickle global {module}.{name}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_partition(path: Path) -> tuple[np.ndarray, np.ndarray]:
    with path.open("rb") as handle:
        if handle.read(6) != b"\x93NUMPY":
            raise ValueError(f"not a NumPy NPY file: {path.name}")
        version = handle.read(2)
        major = version[0]
        header_length = int.from_bytes(handle.read(2 if major == 1 else 4), "little")
        handle.read(header_length)
        value = NumpyOnlyUnpickler(handle).load()
    if isinstance(value, np.ndarray) and value.shape == ():
        value = value.item()
    if not isinstance(value, dict) or not {"sub_idx", "labels"}.issubset(value):
        raise ValueError(f"unexpected partition schema: {path.name}")
    indices = np.asarray(value["sub_idx"], dtype=np.int64)
    labels = np.asarray(value["labels"])
    if indices.ndim != 1 or labels.ndim != 1 or len(indices) != len(labels) or len(indices) == 0:
        raise ValueError(f"invalid partition vectors: {path.name}")
    if len(np.unique(indices)) != len(indices):
        raise ValueError(f"duplicate sample index in {path.name}")
    return indices, labels


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True, help="Root of the evidence bundle")
    parser.add_argument("--output-dir", type=Path, required=True, help="New or empty output directory")
    parser.add_argument("--expected-hashes", type=Path,
                        help="Optional JSON object mapping input-relative paths to expected SHA-256 values")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.data_root.resolve()
    out = args.output_dir.resolve()
    parts_dir = root / "results/stability/partitions"
    runs_dir = root / "results/stability/runs"
    cache_dir = root / "data/cache"
    aggregate_path = root / "results/stability/subsample_stability_summary.csv"
    required = [parts_dir, runs_dir, cache_dir, aggregate_path]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit("Required evidence inputs missing:\n" + "\n".join(missing))
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        raise SystemExit(f"Output directory must be empty: {out}")

    expected = {
        f"{cohort}_{method}_{mode}_{repeat}.npy"
        for cohort in COHORTS for method in METHODS for mode in MODES for repeat in REPEATS
    }
    partition_paths = sorted(parts_dir.glob("*.npy"))
    actual_names = {path.name for path in partition_paths}
    if actual_names != expected:
        raise SystemExit(
            f"Partition key set mismatch: missing={len(expected-actual_names)}, "
            f"unexpected={len(actual_names-expected)}"
        )
    parquet_paths = sorted(runs_dir.glob("*.parquet"))
    if {path.stem for path in parquet_paths} != {path.stem for path in partition_paths}:
        raise SystemExit("Partition and Parquet key sets differ")

    caches: dict[str, dict[str, Any]] = {}
    labels_by_cohort: dict[str, np.ndarray] = {}
    input_manifest: list[dict[str, Any]] = []
    for cohort in COHORTS:
        path = cache_dir / f"{cohort}.npz"
        if not path.is_file():
            raise SystemExit(f"Missing cohort cache: {path.name}")
        with np.load(path, allow_pickle=False) as archive:
            X, y = np.asarray(archive["X"]), np.asarray(archive["y"])
        if X.ndim != 2 or y.ndim != 1 or len(X) != len(y):
            raise SystemExit(f"Invalid cache shapes for {cohort}: X={X.shape}, y={y.shape}")
        labels_by_cohort[cohort] = y
        caches[cohort] = {"path": f"data/cache/{path.name}", "bytes": path.stat().st_size,
                          "sha256": sha256(path), "X_shape": list(X.shape), "y_shape": list(y.shape),
                          "n_classes": int(np.unique(y).size)}
        input_manifest.append({"path": f"data/cache/{path.name}", "bytes": path.stat().st_size,
                               "sha256": caches[cohort]["sha256"], "type": "feature_label_cache"})

    by_cell: dict[tuple[str, str, str], list[tuple[int, np.ndarray, np.ndarray]]] = defaultdict(list)
    duplicate_hashes: dict[str, list[str]] = defaultdict(list)
    split_by_cohort_repeat: dict[tuple[str, int], set[bytes]] = defaultdict(set)
    errors: list[str] = []
    for path in partition_paths:
        match = FILENAME.fullmatch(path.name)
        if match is None:
            errors.append(f"bad filename: {path.name}")
            continue
        cohort, method, mode, repeat_s = match.group("dataset", "method", "mode", "repeat")
        repeat = int(repeat_s)
        idx, labels = load_partition(path)
        if cohort not in labels_by_cohort or np.any(idx < 0) or np.any(idx >= len(labels_by_cohort[cohort])):
            errors.append(f"sample index out of bounds: {path.name}")
            continue
        key = (cohort, method, mode)
        by_cell[key].append((repeat, idx, labels))
        if mode == "real":
            split_by_cohort_repeat[(cohort, repeat)].add(idx.astype("<i8", copy=False).tobytes())
        duplicate_hashes[sha256(path)].append(path.name)
        input_manifest.append({"path": f"results/stability/partitions/{path.name}",
                               "bytes": path.stat().st_size, "sha256": sha256(path), "type": "partition"})

    records_by_key: dict[str, pd.DataFrame] = {}
    seeds_by_cohort_repeat_mode: dict[tuple[str, int, str], set[tuple[int, int]]] = defaultdict(set)
    for path in parquet_paths:
        frame = pd.read_parquet(path)
        if len(frame) != 1:
            errors.append(f"Parquet row count is not 1: {path.name}")
        records_by_key[path.stem] = frame
        match = FILENAME.fullmatch(path.stem + ".npy")
        if match and len(frame) == 1:
            cohort, _, mode, repeat_s = match.group("dataset", "method", "mode", "repeat")
            row = frame.iloc[0]
            try:
                seeds_by_cohort_repeat_mode[(cohort, int(repeat_s), mode)].add(
                    (int(row["sub_seed"]), int(row["null_seed"])))
            except (KeyError, TypeError, ValueError):
                errors.append(f"missing or malformed seed metadata: {path.name}")
        input_manifest.append({"path": f"results/stability/runs/{path.name}",
                               "bytes": path.stat().st_size, "sha256": sha256(path), "type": "per_fit_record"})
    aggregate = pd.read_csv(aggregate_path)
    if not {"dataset", "model", "subsample_stability", "subsample_accuracy", "null_stability"}.issubset(aggregate):
        raise SystemExit("Aggregate summary lacks expected columns")
    saved = {(str(r.dataset), str(r.model)): r for r in aggregate.itertuples(index=False)}
    input_manifest.append({"path": "results/stability/subsample_stability_summary.csv",
                           "bytes": aggregate_path.stat().st_size, "sha256": sha256(aggregate_path),
                           "type": "historical_aggregate_for_comparison_only"})
    expected_hashes: dict[str, str] = {}
    if args.expected_hashes:
        loaded = json.loads(args.expected_hashes.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict) or not all(isinstance(k, str) and isinstance(v, str)
                                                   for k, v in loaded.items()):
            raise SystemExit("Expected-hashes file must be a JSON object of relative path to SHA-256")
        expected_hashes = {key.replace("\\", "/"): value.lower() for key, value in loaded.items()}
        observed_paths = {entry["path"] for entry in input_manifest}
        for entry in input_manifest:
            expected_hash = expected_hashes.get(entry["path"])
            if expected_hash is None:
                errors.append(f"expected SHA-256 not supplied: {entry['path']}")
            elif expected_hash != entry["sha256"].lower():
                errors.append(f"SHA-256 mismatch: {entry['path']}")
        for expected_path in sorted(set(expected_hashes) - observed_paths):
            errors.append(f"expected-hash path not found in evidence bundle: {expected_path}")

    cell_rows: list[dict[str, Any]] = []
    for cohort in COHORTS:
        y = labels_by_cohort[cohort]
        for method in METHODS:
            mode_rows: dict[str, list[tuple[int, np.ndarray, np.ndarray]]] = {}
            for mode in MODES:
                rows = sorted(by_cell[(cohort, method, mode)], key=lambda row: row[0])
                if [row[0] for row in rows] != list(REPEATS):
                    errors.append(f"repeat indices incomplete: {cohort}/{method}/{mode}")
                mode_rows[mode] = rows
                if len(rows) != 30:
                    errors.append(f"repeat count mismatch: {cohort}/{method}/{mode}")
            for real, null in zip(mode_rows["real"], mode_rows["null"]):
                if real[0] != null[0] or not np.array_equal(real[1], null[1]):
                    errors.append(f"real/null split mismatch: {cohort}/{method}/{real[0]}")

            real_aris: list[float] = []
            qualifying_repeat_counts = {0.02: 0, 0.05: 0, 0.10: 0}
            for mode in MODES:
                for repeat, idx, labels in mode_rows[mode]:
                    record = records_by_key[f"{cohort}_{method}_{mode}_{repeat}"]
                    if len(record) != 1:
                        continue
                    row = record.iloc[0]
                    if (str(row.get("dataset")) != cohort or str(row.get("model")) != method
                        or str(row.get("mode")) != mode or int(row.get("subsample_id")) != repeat
                        or str(row.get("status")) != "success" or int(row.get("n_samples")) != len(idx)):
                        errors.append(f"Parquet metadata mismatch: {cohort}/{method}/{mode}/{repeat}")
                    if mode == "real":
                        aria = float(adjusted_rand_score(y[idx], labels))
                        real_aris.append(aria)
                        cluster_sizes = np.unique(labels, return_counts=True)[1]
                        min_cluster_fraction = (float(cluster_sizes.min() / len(labels))
                                                if len(cluster_sizes) and len(labels) else 0.0)
                        # Historical post-hoc screen: a repeat is eligible only
                        # if its smallest cluster meets the fraction threshold
                        # and predicted K is not below reference-label K.
                        if len(cluster_sizes) < np.unique(y).size:
                            min_cluster_fraction = 0.0
                        for threshold in qualifying_repeat_counts:
                            if min_cluster_fraction >= threshold:
                                qualifying_repeat_counts[threshold] += 1
                        stored = row.get("accuracy")
                        if pd.isna(stored) or abs(float(stored) - aria) > 1e-12:
                            errors.append(f"Parquet ARI mismatch: {cohort}/{method}/real/{repeat}")
                    elif not pd.isna(row.get("accuracy")):
                        errors.append(f"Null-mode record has nonempty accuracy: {cohort}/{method}/{repeat}")

            def mean_pairwise(rows: list[tuple[int, np.ndarray, np.ndarray]]) -> tuple[float, int]:
                values = []
                for i in range(len(rows)):
                    for j in range(i + 1, len(rows)):
                        _, idx_a, labels_a = rows[i]
                        _, idx_b, labels_b = rows[j]
                        shared = np.intersect1d(idx_a, idx_b, assume_unique=True)
                        if len(shared) < 2:
                            errors.append(f"intersection smaller than 2: {cohort}/{method}")
                            continue
                        pos_a = {int(sample): pos for pos, sample in enumerate(idx_a)}
                        pos_b = {int(sample): pos for pos, sample in enumerate(idx_b)}
                        values.append(float(adjusted_rand_score(
                            [labels_a[pos_a[int(s)]] for s in shared],
                            [labels_b[pos_b[int(s)]] for s in shared])))
                return (float(np.mean(values)) if values else float("nan"), len(values))

            stability, n_real_pairs = mean_pairwise(mode_rows["real"])
            null_stability, n_null_pairs = mean_pairwise(mode_rows["null"])
            if n_real_pairs != 435 or n_null_pairs != 435:
                errors.append(f"pair count mismatch: {cohort}/{method}")
            saved_row = saved.get((cohort, method))
            cell_rows.append({
                "dataset": cohort, "method": method, "n_repeats": len(real_aris),
                "n_real_pairwise": n_real_pairs, "n_null_pairwise": n_null_pairs,
                "mean_stability": stability, "mean_external_ari": float(np.mean(real_aris)),
                "mean_gap": stability - float(np.mean(real_aris)), "mean_null_stability": null_stability,
                "nondegenerate_repeats_2pct": qualifying_repeat_counts[0.02],
                "nondegenerate_repeats_5pct": qualifying_repeat_counts[0.05],
                "nondegenerate_repeats_10pct": qualifying_repeat_counts[0.10],
                "passes_5pct_27of30": qualifying_repeat_counts[0.05] >= 27,
                "saved_mean_stability": float(saved_row.subsample_stability) if saved_row is not None else np.nan,
                "saved_mean_external_ari": float(saved_row.subsample_accuracy) if saved_row is not None else np.nan,
                "saved_mean_null_stability": float(saved_row.null_stability) if saved_row is not None else np.nan,
            })

    split_mismatches = [{"dataset": cohort, "repeat": repeat, "n_distinct_index_vectors": len(vectors)}
                        for (cohort, repeat), vectors in split_by_cohort_repeat.items() if len(vectors) != 1]
    if split_mismatches:
        errors.append(f"cross-method split mismatches: {len(split_mismatches)}")
    seed_mismatches = [{"dataset": cohort, "repeat": repeat, "mode": mode,
                        "distinct_seed_pairs": len(seed_pairs)}
                       for (cohort, repeat, mode), seed_pairs in seeds_by_cohort_repeat_mode.items()
                       if len(seed_pairs) != 1]
    if seed_mismatches:
        errors.append(f"cross-method seed mismatches: {len(seed_mismatches)}")
    cells = pd.DataFrame(cell_rows).sort_values(["dataset", "method"])
    cells["passes_original_numeric_rule"] = (cells.mean_stability >= 0.50) & (cells.mean_external_ari <= 0.05)
    cells["passes_rule_i_prime_intersection"] = cells.passes_original_numeric_rule & cells.passes_5pct_27of30
    cells.to_csv(out / "recomputed_cells.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    comparison = {
        "max_abs_stability_difference": float((cells.mean_stability - cells.saved_mean_stability).abs().max()),
        "max_abs_external_ari_difference": float((cells.mean_external_ari - cells.saved_mean_external_ari).abs().max()),
        "max_abs_null_stability_difference": float((cells.mean_null_stability - cells.saved_mean_null_stability).abs().max()),
    }
    for metric, difference in comparison.items():
        if not np.isfinite(difference) or difference > 1e-12:
            errors.append(f"recomputed aggregate does not match saved summary ({metric}={difference})")
    summary = {
        "classification": "recomputed from user-supplied saved outputs; not a fresh clustering run",
        "counts": {"partition_files": len(partition_paths), "per_fit_records": len(parquet_paths),
                   "cells": len(cells), "external_ari_observations": int(cells.n_repeats.sum()),
                   "real_pairwise_ari": int(cells.n_real_pairwise.sum()),
                   "null_pairwise_ari": int(cells.n_null_pairwise.sum()),
                   "partition_duplicate_hash_groups": sum(len(names) > 1 for names in duplicate_hashes.values()),
                   "split_mismatches": len(split_mismatches), "seed_mismatches": len(seed_mismatches),
                   "validation_errors": len(errors)},
        "descriptive_cell_weighted": {"mean_stability": float(cells.mean_stability.mean()),
                                       "mean_external_ari": float(cells.mean_external_ari.mean()),
                                       "mean_gap": float(cells.mean_gap.mean()),
                                       "median_gap": float(cells.mean_gap.median()),
                                       "mean_null_stability": float(cells.mean_null_stability.mean())},
        "posthoc_selection_counts": {
            "cells_passing_5pct_minimum_cluster_fraction_in_at_least_27_of_30_repeats": int(cells.passes_5pct_27of30.sum()),
            "cells_passing_original_mean_stability_ari_rule": int(cells.passes_original_numeric_rule.sum()),
            "cells_passing_both_screens_rule_i_prime_intersection": int(cells.passes_rule_i_prime_intersection.sum()),
            "reference_label_informed_k_floor": True,
            "posthoc_and_exploratory": True,
        },
        "aggregate_comparison": comparison, "cache_metadata": caches,
        "inputs": input_manifest, "errors": errors,
        "software": {"python": sys.version, "numpy": np.__version__, "pandas": pd.__version__,
                     "scikit_learn": sklearn.__version__},
        "limitations": ["Input sample IDs and source row order are not authenticated by this calculation.",
                        "Stored status and metrics do not authenticate original fit execution.",
                        "Pairwise ARIs are dependent summaries, not independent observations."],
    }
    summary_path = out / "recomputation_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    outputs = []
    for path in sorted(out.iterdir()):
        if path.is_file():
            outputs.append({"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)})
    (out / "output_manifest.json").write_text(json.dumps(outputs, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"counts": summary["counts"], "summary": summary["descriptive_cell_weighted"],
                      "aggregate_comparison": comparison}, indent=2))
    if errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
