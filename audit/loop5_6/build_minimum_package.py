#!/usr/bin/env python3
"""Build and clean-extract-test a narrow, aggregate-only reproduction package."""
from pathlib import Path
import csv,hashlib,json,shutil,subprocess,sys,tempfile,venv,zipfile
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'audit'/'loop5_6'; PKG=OUT/'minimum_aggregate_package'
INPUT=ROOT/'results/evidence_recovery/recovered/subsample_stability_summary.csv'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 if PKG.exists():shutil.rmtree(PKG)
 (PKG/'inputs').mkdir(parents=True)
 shutil.copy2(INPUT,PKG/'inputs'/'subsample_stability_summary.csv')
 script='''#!/usr/bin/env python3
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
(root/'recomputed.json').write_text(json.dumps(out,indent=2)+'\\n',encoding='utf-8')
print(json.dumps(out,sort_keys=True))
'''
 (PKG/'reproduce_aggregate.py').write_text(script,encoding='utf-8')
 (PKG/'README.md').write_text('''# Minimum aggregate-level reproduction package\n\nThis package reproduces arithmetic summaries from one aggregate CSV (72 dataset-method rows). It does **not** reproduce clustering, resampling, null controls, partition-level pairing, or uncertainty. The CSV is a derived result table; upstream data redistribution is intentionally excluded. Rights to redistribute the aggregate result still require author/source clearance before public release.\n\n## Run\n\nRequires Python 3.9+ and the standard library only:\n\n```bash\npython reproduce_aggregate.py\n```\n\nThe script verifies the input CSV against the dynamically generated SHA-256 in `manifest.csv` and writes `recomputed.json`. A mismatch is fatal.\n\nThe six-cohort experimental protocol, recoverable historically from Git, was 30 class-stratified 80% subsamples per method/cohort, split seeds 5000-5029, fit seed 0, and pairwise ARI over intersections. This package does not reproduce that experiment because its per-fit partitions and records are unavailable.\n''',encoding='utf-8')
 # Hash all package inputs before writing manifest. The manifest excludes itself to avoid self-reference.
 files=sorted(p for p in PKG.rglob('*') if p.is_file() and p.name!='manifest.csv')
 with (PKG/'manifest.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=['path','size_bytes','sha256']);w.writeheader()
  for p in files:w.writerow({'path':p.relative_to(PKG).as_posix(),'size_bytes':p.stat().st_size,'sha256':sha(p)})
 zpath=OUT/'minimum_aggregate_package.zip'
 if zpath.exists():zpath.unlink()
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(PKG.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(PKG.parent))
 log=[]
 with tempfile.TemporaryDirectory(prefix='loop56_clean_') as td:
  clean=Path(td)/'extracted';clean.mkdir()
  with zipfile.ZipFile(zpath) as z:z.extractall(clean)
  extracted=clean/'minimum_aggregate_package'
  env=Path(td)/'venv';venv.EnvBuilder(with_pip=False).create(env)
  py=env/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')
  q=subprocess.run([str(py),'-I',str(extracted/'reproduce_aggregate.py')],cwd=extracted,text=True,capture_output=True)
  log.append({'phase':'zip_extract_and_clean_venv_run','exit_code':q.returncode,'stdout':q.stdout.strip(),'stderr':q.stderr.strip(),'recomputed_json_exists':(extracted/'recomputed.json').exists(),'dependency_install':'not required; standard library only'})
  if q.returncode!=0:raise RuntimeError(q.stderr)
  result=json.loads((extracted/'recomputed.json').read_text())
  assert result['n_aggregate_rows']==72 and abs(result['mean_gap']-0.46427387991007457)<1e-12
 (OUT/'clean_reproduction_test.json').write_text(json.dumps({'package_scope':'aggregate-only; not the six-cohort clustering experiment','package_sha256':sha(zpath),'package_bytes':zpath.stat().st_size,'steps':log,'full_experiment_reproduction':'BLOCKED: no original per-repeat partitions/run records; no clean acquisition+replay tested'},indent=2)+'\n',encoding='utf-8')
 with (OUT/'public_artifact_manifest.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=['artifact','sha256','bytes','scope','redistribution_status','notes']);w.writeheader()
  for p in sorted(PKG.rglob('*')):
   if p.is_file():w.writerow({'artifact':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'bytes':p.stat().st_size,'scope':'minimum aggregate arithmetic package','redistribution_status':'RIGHTS REVIEW REQUIRED before public release' if p.name=='subsample_stability_summary.csv' else 'audit-authored code/docs','notes':'No raw cohort matrix, labels, sample identifiers, per-repeat partitions or run records included'})
  w.writerow({'artifact':'audit/loop5_6/minimum_aggregate_package.zip','sha256':sha(zpath),'bytes':zpath.stat().st_size,'scope':'minimum aggregate arithmetic package','redistribution_status':'draft only; no DOI/release','notes':'Clean extraction and isolated stdlib Python venv tested'})
if __name__=='__main__':main()
