"""Validate prospective run manifests without fitting models.
Expected input: JSON object containing a records array; successful records
reference .npy partitions with sub_idx and labels and dynamic SHA-256 values.
"""
import argparse, hashlib, json, sys
from pathlib import Path
import numpy as np

HASH_FIELDS=(('source','config_sha256'),('source','environment_sha256'),('data','raw_sha256'),('data','feature_sha256'),('data','ordered_sample_ids_sha256'),('data','labels_sha256'),('sampling','indices_sha256'),('output','partition_sha256'),('output','assignment_sha256'))
def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for block in iter(lambda:f.read(1<<20),b''): h.update(block)
 return h.hexdigest()
def validate(manifest_path):
 mf=Path(manifest_path).resolve(); doc=json.loads(mf.read_text(encoding='utf-8-sig')); errors=[]; records=doc.get('records')
 if not isinstance(records,list): return {'ok':False,'errors':['manifest.records must be a list'],'n_records':0}
 ids=set()
 for i,r in enumerate(records):
  tag=f'record[{i}]'; rid=r.get('run_id')
  if not rid or rid in ids: errors.append(f'{tag}: missing or duplicate run_id {rid!r}')
  ids.add(rid)
  for group,key in HASH_FIELDS:
   value=(r.get(group) or {}).get(key)
   if not isinstance(value,str) or len(value)!=64 or any(c not in '0123456789abcdef' for c in value): errors.append(f'{tag}: invalid {group}.{key}')
  status=(r.get('execution') or {}).get('status')
  if status not in ('success','failed'): errors.append(f'{tag}: invalid execution.status')
  out=r.get('output') or {}; rel=out.get('partition_path')
  if status=='success':
   if not rel: errors.append(f'{tag}: successful record lacks output.partition_path'); continue
   p=(mf.parent/rel).resolve()
   if mf.parent not in p.parents: errors.append(f'{tag}: output path escapes run root'); continue
   if not p.is_file(): errors.append(f'{tag}: missing partition {rel}'); continue
   if sha(p)!=out.get('partition_sha256'): errors.append(f'{tag}: partition SHA-256 mismatch'); continue
   try:
    arr=np.load(p,allow_pickle=True); z=arr.item() if arr.shape==() else None
    if not isinstance(z,dict) or 'sub_idx' not in z or 'labels' not in z: errors.append(f'{tag}: partition must be scalar object with sub_idx and labels'); continue
    ix=np.asarray(z['sub_idx']); y=np.asarray(z['labels'])
    if ix.ndim!=1 or y.ndim!=1 or len(ix)!=len(y) or len(ix)!=out.get('n_samples'): errors.append(f'{tag}: index/label length mismatch')
    if ix.dtype.kind not in 'iu' or len(np.unique(ix))!=len(ix) or (ix<0).any(): errors.append(f'{tag}: invalid sample indices')
    if len(np.unique(y))!=out.get('observed_k'): errors.append(f'{tag}: observed K mismatch')
    sizes=sorted(np.bincount(y.astype(int)).tolist())
    if sizes!=out.get('cluster_sizes'): errors.append(f'{tag}: cluster size mismatch')
    if hashlib.sha256(np.ascontiguousarray(y).tobytes()).hexdigest()!=out.get('assignment_sha256'): errors.append(f'{tag}: assignment hash mismatch')
    if hashlib.sha256(np.ascontiguousarray(ix).tobytes()).hexdigest()!=(r.get('sampling') or {}).get('indices_sha256'): errors.append(f'{tag}: indices hash mismatch')
   except Exception as e: errors.append(f'{tag}: cannot load partition: {type(e).__name__}: {e}')
 return {'ok':not errors,'n_records':len(records),'unique_run_ids':len(ids),'errors':errors}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('manifest'); a=ap.parse_args()
 result=validate(a.manifest); print(json.dumps(result,indent=2)); return 0 if result['ok'] else 1
if __name__=='__main__':sys.exit(main())
