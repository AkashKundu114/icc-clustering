#!/usr/bin/env python3
"""Recompute only aggregate descriptive statistics; no experiment rerun."""
import csv,hashlib,json,statistics
from pathlib import Path
root=Path(__file__).resolve().parent
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
manifest=list(csv.DictReader((root/'manifest.csv').open(encoding='utf-8',newline='')))
entry=next(r for r in manifest if r['path']=='inputs/subsample_stability_summary.csv')
src=root/entry['path']; actual=sha(src)
if actual!=entry['sha256']:
 raise SystemExit(f"SHA-256 mismatch: {src}: expected {entry['sha256']}, actual {actual}")
rows=list(csv.DictReader(src.open(encoding='utf-8-sig',newline='')))
stab=[float(r['subsample_stability']) for r in rows]
ari=[float(r['subsample_accuracy']) for r in rows]
gap=[s-a for s,a in zip(stab,ari)]
out={'n_aggregate_rows':len(rows),'n_datasets':len({r['dataset'] for r in rows}),'n_methods':len({r['model'] for r in rows}), 'mean_stability':statistics.mean(stab),'mean_external_ari':statistics.mean(ari),'mean_gap':statistics.mean(gap),'median_gap':statistics.median(gap),'interpretation':'Aggregate-only descriptive recomputation; not repeated-run or raw-partition reproduction.'}
(root/'recomputed.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,sort_keys=True))
