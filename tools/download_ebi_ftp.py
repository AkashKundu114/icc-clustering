import ftplib
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw" / "cohort_discovery"

def download_ebi_file(accession, filename, dest_dir):
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / filename
    
    if dest_path.exists() and dest_path.stat().st_size > 0:
        print(f"[=] Already exists: {dest_path} ({dest_path.stat().st_size:,} bytes)")
        return True

    print(f"[*] Connecting to ftp.ebi.ac.uk for {accession}/{filename}...")
    ftp = ftplib.FTP("ftp.ebi.ac.uk", timeout=30)
    ftp.login()
    path = f"/pub/databases/microarray/data/experiment/GEOD/{accession}/"
    ftp.cwd(path)
    
    size = ftp.size(filename)
    print(f"[*] Remote file size: {size:,} bytes ({size / (1024*1024):.1f} MB)")
    ftp.quit()

    part_path = dest_path.with_name(filename + ".part")
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            existing_bytes = part_path.stat().st_size if part_path.exists() else 0
            if size and existing_bytes >= size:
                part_path.rename(dest_path)
                print(f"[+] Download complete: {dest_path.name} ({dest_path.stat().st_size:,} bytes)")
                return True

            print(f"[*] Connecting to ftp.ebi.ac.uk (attempt {attempt}/{max_retries}, offset: {existing_bytes:,})...")
            ftp = ftplib.FTP("ftp.ebi.ac.uk", timeout=60)
            ftp.login()
            path = f"/pub/databases/microarray/data/experiment/GEOD/{accession}/"
            ftp.cwd(path)

            mode = "ab" if existing_bytes > 0 else "wb"
            start_time = time.time()
            last_log = start_time
            downloaded = existing_bytes

            with open(part_path, mode) as f:
                def callback(chunk):
                    nonlocal downloaded, last_log
                    f.write(chunk)
                    downloaded += len(chunk)
                    now = time.time()
                    if now - last_log > 3:
                        elapsed = now - start_time
                        speed = (downloaded - existing_bytes) / elapsed if elapsed > 0 else 0
                        pct = (downloaded / size * 100) if size else 0
                        print(f"    Progress: {downloaded:,} bytes ({pct:.1f}%) at {speed / 1024:.1f} KB/s", flush=True)
                        last_log = now

                ftp.retrbinary(f"RETR {filename}", callback, blocksize=128*1024, rest=existing_bytes if existing_bytes > 0 else None)

            ftp.quit()
            part_path.rename(dest_path)
            print(f"[+] Download complete: {dest_path.name} ({dest_path.stat().st_size:,} bytes)")
            return True
        except Exception as e:
            print(f"[!] Error on attempt {attempt}: {e}")
            time.sleep(3)

    return False

if __name__ == "__main__":
    acc = sys.argv[1] if len(sys.argv) > 1 else "E-GEOD-31210"
    fname = sys.argv[2] if len(sys.argv) > 2 else f"{acc}.processed.1.zip"
    dest = RAW_DIR / acc.replace("E-GEOD-", "GSE")
    download_ebi_file(acc, fname, dest)
