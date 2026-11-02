"""Generate dynamic Loop 5.9 deliverable manifest and SHA256SUMS.

Reads every file under audit/loop5_9. Writes loop5_9_manifest.csv and
SHA256SUMS. Self-reference is impossible, so each lists all other files and
README.md documents the self-exclusion convention.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv, hashlib

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'audit'/'loop5_9'
MANIFEST=OUT/'loop5_9_manifest.csv'
SUMS=OUT/'SHA256SUMS'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def main():
    excluded={MANIFEST.resolve(),SUMS.resolve()}
    files=sorted(p for p in OUT.rglob('*') if p.is_file() and p.resolve() not in excluded)
    rows=[]
    for p in files:
        rel=p.relative_to(OUT).as_posix()
        if p.suffix.lower()=='.py': kind='audit script'
        elif p.suffix.lower() in {'.csv','.json','.txt'}:kind='machine-readable audit output or manifest'
        elif 'pre_remediation' in rel:kind='frozen manuscript package copy/static QA artifact'
        else:kind='audit report or supporting artifact'
        rows.append({'relative_path':rel,'bytes':p.stat().st_size,'sha256':sha(p),'artifact_class':kind})
    with MANIFEST.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    files_for_sums=sorted(p for p in OUT.rglob('*') if p.is_file() and p.resolve()!=SUMS.resolve())
    SUMS.write_text(''.join(f'{sha(p)}  {p.relative_to(OUT).as_posix()}\n' for p in files_for_sums),encoding='utf-8')
    print(f'manifest_rows={len(rows)} checksum_entries={len(files_for_sums)}')

if __name__=='__main__':main()
