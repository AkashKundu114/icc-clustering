"""Build dynamic source/artifact manifests and SHA256SUMS for Loop 5.8.

Expected: target repo at audit baseline, local D:\\Final Year Project, and all
Loop 5.8 reports/scripts complete. Reads source bytes and Git metadata only.
Writes only audit/loop5_8/audit_source_of_truth_manifest.csv,
execution_manifest.json, and SHA256SUMS.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib, json, subprocess

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "audit" / "loop5_8"
FYP = Path(r"D:\Final Year Project")


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def git(root, *args):
    try:
        return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "UNAVAILABLE"


def tracked_set(root):
    raw = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"])
    return set(x.decode("utf-8", "replace").replace("\\", "/") for x in raw.split(b"\0") if x)


def main():
    if not FYP.is_dir():
        raise SystemExit(f"Required local FYP directory is absent: {FYP}")
    files = {}

    def add(path, kind, role):
        path = Path(path)
        if path.is_file():
            files[str(path.resolve())] = (path, kind, role)

    # Full local stability evidence and six exact cached inputs.
    for subdir, kind, role in [
        (FYP / "results/stability/partitions", "saved_partition", "original experiment output; execution provenance unresolved"),
        (FYP / "results/stability/runs", "per_fit_record", "saved per-fit output; execution provenance unresolved"),
        (FYP / "data/cache", "cached_input", "preprocessed input; run linkage not embedded in fit records"),
    ]:
        for p in sorted(subdir.glob("*")):
            if p.is_file():
                add(p, kind, role)
    fyp_sources = [
        FYP / "results/stability/subsample_stability_summary.csv",
        FYP / "results/stability/real_data_stability_summary.csv",
        FYP / "results/passF/benchmark_matrix_passF.csv",
        FYP / "results/passF/benchmark_matrix_summary_passF.csv",
        FYP / "results/exp3_cohirf_benchmark.csv",
        FYP / "scripts/run_phase3_experiments.py",
        FYP / "experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py",
        FYP / "paper/main.tex",
        FYP / "scripts/audit_degeneracy.py",
        FYP / "scripts/make_stability_outputs.py",
    ]
    for p in fyp_sources:
        add(p, "source_or_summary", "source/configuration or comparison target; see report for role")
    # Audit source files and all deliverables except self-referential manifests.
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name not in {"audit_source_of_truth_manifest.csv", "audit_execution_manifest.json", "execution_manifest.json", "SHA256SUMS"}:
            add(p, "audit_artifact", "Loop 5.8 script or deliverable")

    target_commit = git(ROOT, "rev-parse", "HEAD")
    fyp_commit = git(FYP, "rev-parse", "HEAD")
    target_tracked = tracked_set(ROOT)
    fyp_tracked = tracked_set(FYP)
    rows = []
    for key in sorted(files):
        p, kind, role = files[key]
        if p.resolve().is_relative_to(ROOT.resolve()):
            rel = p.resolve().relative_to(ROOT.resolve()).as_posix()
            tr = rel in target_tracked
            fr = False
            commit = target_commit if tr else "UNTRACKED/IGNORED at target baseline"
        elif p.resolve().is_relative_to(FYP.resolve()):
            rel = p.resolve().relative_to(FYP.resolve()).as_posix()
            tr = False
            fr = rel in fyp_tracked
            commit = fyp_commit if fr else "UNTRACKED/IGNORED in local FYP worktree"
        else:
            rel = str(p)
            tr = fr = False
            commit = "EXTERNAL"
        stat = p.stat()
        rows.append({
            "path": str(p.resolve()), "relative_path": rel, "bytes": stat.st_size,
            "sha256": sha(p), "artifact_type": kind, "role_or_provenance_note": role,
            "tracked_in_target": tr, "tracked_in_fyp": fr, "source_commit_or_status": commit,
        })
    manifest = OUT / "audit_source_of_truth_manifest.csv"
    with manifest.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    execution = {
        "audit": "Loop 5.8",
        "baseline_target_commit": target_commit,
        "fetched_origin_main": git(ROOT, "rev-parse", "origin/main"),
        "target_branch": git(ROOT, "branch", "--show-current"),
        "fyp_worktree_commit": fyp_commit,
        "original_experiment_execution_commit": "UNVERIFIABLE",
        "protocol_or_artifact_commits_are_not_execution_attestations": True,
        "final_manuscript_commit": "UNAVAILABLE; target paper/manuscript/main.tex is absent/untracked",
        "loop5_8_deliverables_commit": "NOT COMMITTED",
        "public_release_commit": "NONE",
        "executed_scripts": [
            "audit/loop5_8/scripts/partition_forensics.py (subagent; direct read-only scan)",
            "audit/loop5_8/scripts/bootstrap_estimand.py (lead; rerun after report correction)",
            "audit/loop5_8/scripts/benchmark_provenance_inventory.py (subagent; local source/row inventory)",
            "audit/loop5_8/scripts/build_manuscript_claims.py (subagent; FYP candidate claim matrix; no manuscript edit)",
            "audit/loop5_8/reproduction/scripts/reproduce_aggregate.py (lead; repeated local execution)",
            "audit/loop5_6/minimum_aggregate_package/reproduce_aggregate.py (fresh clone; exit 0)",
        ],
        "fresh_clone_commit": "29bcc279589d4a6c1e6747885cc857085ac8d6d0",
        "fresh_clone_tiers": {"tier1_aggregate": "PASS", "tier2_partition": "FAIL_INPUTS_ABSENT", "tier3_full_fit": "NOT_RUN"},
        "local_saved_counts": {"partitions": 4320, "per_fit_records": 4320, "pairwise_stability_values": 62640, "reconstructed_cells": 72},
        "loop5_8_manifest_rows": len(rows),
        "environment": {"python": "3.14.6 for lead's Tier 1 clone check; specialist environment details are recorded where available", "os": "Windows local environment"},
        "executed_at_local": datetime.now().astimezone().isoformat(timespec="seconds"),
        "limitations": ["Saved fit execution/input linkage not authenticated", "No complete public package or raw evidence release", "No model fits rerun", "FYP evidence is local-only"],
    }
    (OUT / "audit_execution_manifest.json").write_text(json.dumps(execution, indent=2) + "\n", encoding="utf-8")

    sum_paths = [p for p in sorted(OUT.rglob("*")) if p.is_file() and p.name != "SHA256SUMS"]
    (OUT / "SHA256SUMS").write_text("".join(f"{sha(p)}  {p.relative_to(OUT).as_posix()}\n" for p in sum_paths), encoding="utf-8")
    print(f"manifest_rows={len(rows)} checksum_entries={len(sum_paths)}")


if __name__ == "__main__":
    main()
