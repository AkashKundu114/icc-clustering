#!/usr/bin/env python3
"""Metadata-first GEO cohort discovery and checksum-verified download utility.

This tool discovers candidate GEO Series; it does NOT auto-approve cohorts or
infer biological labels. Downloads are opt-in and require a reviewed manifest.
Uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
DEFAULT_QUERY = (
    '("Homo sapiens"[Organism]) AND '
    '("Expression profiling by array"[DataSet Type] OR '
    '"Expression profiling by high throughput sequencing"[DataSet Type]) AND '
    '(cancer OR carcinoma OR tumor OR tumour OR leukemia OR leukaemia OR lymphoma '
    'OR melanoma OR glioma OR sarcoma OR myeloma OR adenocarcinoma)'
)
FIELDS = [
    "geo_accession", "title", "summary", "overall_design", "submission_date",
    "last_update_date", "pubmed_ids", "n_samples", "platforms", "organism",
    "source_query", "source_url", "discovery_timestamp_utc",
    "label_review_status", "eligibility_decision",
]
USER_AGENT = "ICC-biological-cohort-discovery/1.0 (academic research; contact repository maintainer)"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def request_text(url: str, timeout: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def esearch(query: str, retmax: int, email: str | None) -> list[str]:
    params = {"db": "gds", "term": query, "retmax": str(retmax), "retmode": "json"}
    if email:
        params["email"] = email
    url = EUTILS + "/esearch.fcgi?" + urllib.parse.urlencode(params)
    payload = json.loads(request_text(url))
    return payload.get("esearchresult", {}).get("idlist", [])


def esummary(ids: list[str], email: str | None) -> list[dict[str, Any]]:
    if not ids:
        return []
    params = {"db": "gds", "id": ",".join(ids), "retmode": "json"}
    if email:
        params["email"] = email
    url = EUTILS + "/esummary.fcgi?" + urllib.parse.urlencode(params)
    payload = json.loads(request_text(url))
    result = payload.get("result", {})
    rows = []
    for uid in result.get("uids", []):
        item = result.get(uid, {})
        acc = str(item.get("accession", ""))
        if not acc.startswith("GSE"):
            continue
        rows.append({
            "geo_accession": acc,
            "title": clean(item.get("title")),
            "summary": clean(item.get("summary")),
            "overall_design": clean(item.get("gds", {}).get("gse", {}).get("overall_design", "")) if isinstance(item.get("gds"), dict) else "",
            "submission_date": item.get("pdat", ""),
            "last_update_date": item.get("par", ""),
            "pubmed_ids": ";".join(map(str, item.get("pubmedids", []) or [])),
            "n_samples": item.get("n_samples", ""),
            "platforms": ";".join(map(str, item.get("gpl", []) or [])),
            "organism": item.get("taxon", ""),
            "source_url": f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={acc}",
        })
    return rows


def clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(c for v in value if (c := clean(v)))
    return re.sub(r"\s+", " ", str(value)).strip()


def append_jsonl(path: Path, item: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(item, ensure_ascii=False) + "\n")


def discover(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    catalog = out / "candidate_catalog.csv"
    log = out / "search_log.jsonl"
    queries = args.query or [DEFAULT_QUERY]
    known: dict[str, dict[str, Any]] = {}
    if catalog.exists():
        with catalog.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                known[row["geo_accession"]] = row

    for query in queries:
        started = utc_now()
        try:
            ids = esearch(query, args.retmax, args.email)
            append_jsonl(log, {"timestamp_utc": started, "endpoint": "NCBI ESearch db=gds",
                               "query": query, "uid_count": len(ids), "status": "ok"})
            for offset in range(0, len(ids), 200):
                batch = ids[offset:offset + 200]
                rows = esummary(batch, args.email)
                for row in rows:
                    row.update({
                        "source_query": query,
                        "discovery_timestamp_utc": started,
                        "label_review_status": "NOT_REVIEWED",
                        "eligibility_decision": "CANDIDATE_ONLY",
                    })
                    known[row["geo_accession"]] = row
                time.sleep(args.delay)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            append_jsonl(log, {"timestamp_utc": started, "endpoint": "NCBI E-utilities",
                               "query": query, "status": "error", "error": repr(exc)})
            print(f"Discovery error for query: {exc}", file=sys.stderr)
            continue

    rows = sorted(known.values(), key=lambda r: r["geo_accession"])
    with catalog.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} unique GEO Series candidates to {catalog}")
    print("All records remain CANDIDATE_ONLY; review sample-level metadata and original papers.")
    return 0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_manifest(args: argparse.Namespace) -> int:
    """Download only URLs in a human-reviewed CSV manifest.

    Required columns: cohort_id,url,relative_path,expected_sha256,license_reviewed
    license_reviewed must be YES. expected_sha256 may be blank for first acquisition;
    the computed digest is written to the output manifest for subsequent verification.
    """
    manifest = Path(args.manifest)
    root = Path(args.raw_dir).resolve()
    report = Path(args.report)
    with manifest.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"cohort_id", "url", "relative_path", "expected_sha256", "license_reviewed"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"Manifest missing columns: {sorted(missing)}")
        entries = list(reader)

    output = []
    for entry in entries:
        if entry["license_reviewed"].strip().upper() != "YES":
            raise SystemExit(f"Refusing download for {entry['cohort_id']}: license_reviewed is not YES")
        rel = Path(entry["relative_path"])
        if rel.is_absolute() or ".." in rel.parts:
            raise SystemExit(f"Unsafe relative_path: {rel}")
        target = (root / rel).resolve()
        if root not in target.parents:
            raise SystemExit(f"Path escapes raw_dir: {rel}")
        target.parent.mkdir(parents=True, exist_ok=True)

        if target.exists() and target.stat().st_size > 0:
            actual = sha256_file(target)
            expected = entry["expected_sha256"].strip().lower()
            if not expected or actual == expected:
                output.append({**entry, "retrieval_timestamp_utc": utc_now(),
                               "bytes": target.stat().st_size, "sha256": actual,
                               "download_status": "VERIFIED_EXISTING"})
                print(f"Verified existing {entry['cohort_id']} -> {target} ({target.stat().st_size:,} bytes)")
                continue

        tmp = target.with_suffix(target.suffix + ".part")
        try:
            import shutil
            import subprocess
            curl_bin = shutil.which("curl") or shutil.which("curl.exe")
            if curl_bin:
                cmd = [curl_bin, "-sSL", "--fail", "-C", "-", "--connect-timeout", "60", "-m", str(args.timeout), entry["url"], "-o", str(tmp)]
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode != 0:
                    raise RuntimeError(f"curl download failed ({res.returncode}): {res.stderr}")
            else:
                req = urllib.request.Request(entry["url"], headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=args.timeout) as response, tmp.open("wb") as out:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        out.write(chunk)
            actual = sha256_file(tmp)
            expected = entry["expected_sha256"].strip().lower()
            if expected and actual != expected:
                tmp.unlink(missing_ok=True)
                raise SystemExit(f"SHA-256 mismatch for {entry['cohort_id']}: expected {expected}, got {actual}")
            tmp.replace(target)
            output.append({**entry, "retrieval_timestamp_utc": utc_now(),
                           "bytes": target.stat().st_size, "sha256": actual,
                           "download_status": "VERIFIED"})
            print(f"Downloaded {entry['cohort_id']} -> {target} ({target.stat().st_size:,} bytes)")
        except Exception:
            tmp.unlink(missing_ok=True)
            raise

    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(output[0]) if output else list(required))
        writer.writeheader()
        writer.writerows(output)
    print(f"Download manifest written to {report}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p_discover = sub.add_parser("discover", help="Search GEO for candidate human cancer expression series")
    p_discover.add_argument("--query", action="append", help="NCBI GEO/GDS query; repeatable")
    p_discover.add_argument("--retmax", type=int, default=500, help="Maximum results per query (default 500)")
    p_discover.add_argument("--email", help="NCBI contact email (recommended)")
    p_discover.add_argument("--delay", type=float, default=0.35, help="Pause between ESummary batches")
    p_discover.add_argument("--out", default="data/cohort_discovery")
    p_discover.set_defaults(func=discover)

    p_download = sub.add_parser("download", help="Download reviewed files with SHA-256 verification")
    p_download.add_argument("--manifest", required=True)
    p_download.add_argument("--raw-dir", default="data/raw/cohort_discovery")
    p_download.add_argument("--report", default="data/cohort_discovery/download_manifest.csv")
    p_download.add_argument("--timeout", type=int, default=3600)
    p_download.set_defaults(func=download_manifest)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
