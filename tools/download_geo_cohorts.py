#!/usr/bin/env python3
"""
tools/download_geo_cohorts.py
Resilient HTTP chunked downloader for NCBI GEO Series Matrix files.
Supports resuming partial downloads, retries, and integrity checks.
"""

import sys
import time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw" / "cohort_discovery"


def download_file(url: str, dest_path: Path, max_retries: int = 5, chunk_size: int = 128 * 1024) -> bool:
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    part_path = dest_path.with_name(dest_path.name + ".part")

    if dest_path.exists() and dest_path.stat().st_size > 0:
        print(f"[=] Already complete: {dest_path.name} ({dest_path.stat().st_size:,} bytes)")
        return True

    for attempt in range(1, max_retries + 1):
        try:
            existing_bytes = part_path.stat().st_size if part_path.exists() else 0
            headers = {}
            if existing_bytes > 0:
                headers["Range"] = f"bytes={existing_bytes}-"
                print(f"[*] Resuming {dest_path.name} from byte {existing_bytes:,} (attempt {attempt}/{max_retries})...", flush=True)
            else:
                print(f"[*] Starting download {dest_path.name} (attempt {attempt}/{max_retries})...", flush=True)

            with requests.get(url, headers=headers, stream=True, timeout=30) as r:
                if r.status_code not in (200, 206):
                    print(f"[-] Server returned status code {r.status_code}", flush=True)
                    time.sleep(2)
                    continue

                mode = "ab" if existing_bytes > 0 and r.status_code == 206 else "wb"
                if mode == "wb" and existing_bytes > 0:
                    existing_bytes = 0

                content_len = r.headers.get("Content-Length")
                total_expected = existing_bytes + int(content_len) if content_len else None

                with open(part_path, mode) as f:
                    downloaded = existing_bytes
                    start_time = time.time()
                    last_log = start_time
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            now = time.time()
                            if now - last_log > 2:
                                elapsed = now - start_time
                                speed = (downloaded - existing_bytes) / elapsed if elapsed > 0 else 0
                                pct = (downloaded / total_expected * 100) if total_expected else 0
                                print(f"    Progress: {downloaded:,} bytes ({pct:.1f}%) at {speed / 1024:.1f} KB/s", flush=True)
                                last_log = now

            # If reached here without error, verify and finalize
            final_size = part_path.stat().st_size
            if total_expected and final_size != total_expected:
                print(f"[!] Warning: final size {final_size} != expected {total_expected}", flush=True)
                continue

            part_path.rename(dest_path)
            print(f"[+] Download complete: {dest_path.name} ({final_size:,} bytes)", flush=True)
            return True

        except (requests.RequestException, IOError) as e:
            print(f"[!] Error on attempt {attempt}: {e}")
            time.sleep(2)

    print(f"[-] Failed to download {url} after {max_retries} attempts.")
    return False


def get_geo_url(accession: str) -> str:
    num = int(accession.replace("GSE", ""))
    prefix = f"GSE{num // 1000}nnn"
    return f"https://ftp.ncbi.nlm.nih.gov/geo/series/{prefix}/{accession}/matrix/{accession}_series_matrix.txt.gz"


def main():
    targets = sys.argv[1:]
    if not targets:
        targets = ["GSE21653", "GSE32894", "GSE62254", "GSE31210", "GSE10846", "GSE39582", "GSE49710"]

    for acc in targets:
        url = get_geo_url(acc)
        dest = RAW_DIR / acc / f"{acc}_series_matrix.txt.gz"
        success = download_file(url, dest)
        if not success:
            print(f"[!] Failed to acquire {acc}")


if __name__ == "__main__":
    main()
