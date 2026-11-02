from pathlib import Path
import hashlib, csv, re, json, subprocess, os
from collections import defaultdict, Counter
from datetime import datetime, timezone
import numpy as np
import pandas as pd
ROOT=Path(r'D:\Final Year Project'); PART=ROOT/'results/stability/partitions'; RUN=ROOT/'results/stability/runs'; OUT=Path('audit/loop5_9/provenance')
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def parse(p):
 m=re.fullmatch(r'(.+?)_(.+)_(real|null)_(\d+)\.npy',p.name)
 if not m: return ('','','',-1)
 return m.group(1),m.group(2),m.group(3),int(m.group(4))
files=sorted(PART.glob('*.npy')); byhash=defaultdict(list); malformed=[]; records=[]
for p in files:
 h=sha(p); byhash[h].append(p)
 d,m,mode,r=parse(p)
 try:
  obj=np.load(p,allow_pickle=True).item(); ix=np.asarray(obj['sub_idx']); y=np.asarray(obj['labels'])
  if ix.ndim!=1 or y.ndim!=1 or len(ix)!=len(y) or len(np.unique(ix))!=len(ix): malformed.append(str(p))
  sizes=sorted(np.unique(y,return_counts=True)[1].astype(int).tolist(),reverse=True); k=len(sizes)
 except Exception as e:
  malformed.append(str(p)); ix=np.array([]);y=np.array([]);sizes=[];k=-1
 rp=RUN/f'{d}_{m}_{mode}_{r}.parquet'; rec={}; parq_rows=-1
 if rp.exists():
  df=pd.read_parquet(rp); parq_rows=len(df)
  hit=df[(df.dataset.astype(str)==d)&(df.model.astype(str)==m)&(df['mode'].astype(str)==mode)&(df.subsample_id.astype(int)==r)]
  if len(hit)==1:rec=hit.iloc[0].to_dict()
 records.append({'path':str(p),'sha256':h,'dataset':d,'method':m,'mode':mode,'repeat':r,'bytes':p.stat().st_size,'mtime_epoch':p.stat().st_mtime,'mtime_utc':datetime.fromtimestamp(p.stat().st_mtime,timezone.utc).isoformat(),'indices_sha256':hashlib.sha256(ix.tobytes()).hexdigest() if len(ix) else '', 'labels_sha256':hashlib.sha256(y.tobytes()).hexdigest() if len(y) else '', 'n':len(ix),'K':k,'sizes':';'.join(map(str,sizes)),'parquet':str(rp),'parquet_sha256':sha(rp) if rp.exists() else '', 'parquet_exists':rp.exists(),'parquet_rows':parq_rows,'status':rec.get('status',''),'sub_seed':rec.get('sub_seed',''),'null_seed':rec.get('null_seed',''),'saved_ari':rec.get('accuracy','')})
dup={h:ps for h,ps in byhash.items() if len(ps)>1}; out=[]
for g,(h,ps) in enumerate(sorted(dup.items(),key=lambda z:z[1][0].name),1):
 ms=[parse(p) for p in ps]; ds={x[0] for x in ms}; methods={x[1] for x in ms}; modes={x[2] for x in ms}; reps={x[3] for x in ms}
 label='within_same_cell_repeats' if len(ds)==len(methods)==len(modes)==1 and len(reps)>1 else ('cross_mode' if len(modes)>1 else ('cross_method' if len(methods)>1 else 'other'))
 for p in ps:
  q=next(x for x in records if x['path']==str(p))
  out.append({'duplicate_group':f'G{g:03d}','group_sha256':h,'group_size':len(ps),'group_relation':label,'forensic_classification':'CANNOT CLASSIFY','classification_reason':'No original partition producer, input hashes, or output-write trace; byte equality cannot distinguish independent equal outputs from reuse/overwrite.',**q})
with (OUT/'duplicate_reaudit.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=out[0].keys());w.writeheader();w.writerows(out)
# Census assertions, exact named payload comparisons
named=[('cns_CoHiRF_null_17.npy','cns_CoHiRF_real_17.npy'),('prostate_CoHiRF_null_5.npy','prostate_CoreHalo_real_5.npy'),('prostate_StdCons_null_16.npy','prostate_UngatedAC_real_16.npy')]; comps=[]
for a,b in named:
 pa,pb=PART/a,PART/b; xa=np.load(pa,allow_pickle=True).item(); xb=np.load(pb,allow_pickle=True).item(); ia,ib=np.asarray(xa['sub_idx']),np.asarray(xb['sub_idx']); ya,yb=np.asarray(xa['labels']),np.asarray(xb['labels']); da,ma,moa,ra=parse(pa); db,mb,mob,rb=parse(pb)
 def get(path,d,m,mode,r):
  df=pd.read_parquet(path); x=df[(df.dataset.astype(str)==d)&(df.model.astype(str)==m)&(df['mode'].astype(str)==mode)&(df.subsample_id.astype(int)==r)]
  return x.iloc[0].to_dict() if len(x)==1 else {'matching_rows':len(x)}
 _,cb=np.unique(ya,return_counts=True); _,cd=np.unique(yb,return_counts=True)
 comps.append({'file_a':a,'file_b':b,'sha_a':sha(pa),'sha_b':sha(pb),'indices_order_equal':bool(np.array_equal(ia,ib)),'labels_array_equal':bool(np.array_equal(ya,yb)),'sample_order_length_a':len(ia),'sample_order_length_b':len(ib),'cluster_sizes_a':sorted(cb.astype(int).tolist(),reverse=True),'cluster_sizes_b':sorted(cd.astype(int).tolist(),reverse=True),'record_a':{k:str(v) for k,v in get(RUN/f'{da}_{ma}_{moa}_{ra}.parquet',da,ma,moa,ra).items()},'record_b':{k:str(v) for k,v in get(RUN/f'{db}_{mb}_{mob}_{rb}.parquet',db,mb,mob,rb).items()}})
# Search source tree for partition producer tokens excluding binaries/data payloads
needles=('sub_idx','null_seed','sub_seed','results/stability/partitions','results/stability/runs','subsample_stability_summary')
found=[]
for p in ROOT.rglob('*'):
 if not p.is_file() or '.git' in p.parts or any(x in p.parts for x in ('.venv','data/cache','results/stability/partitions','results/stability/runs')): continue
 if p.suffix.lower() not in {'.py','.ipynb','.md','.yaml','.yml','.json','.toml','.csv'}:continue
 try: txt=p.read_text(encoding='utf-8',errors='ignore')
 except:continue
 hits=[x for x in needles if x in txt]
 if hits: found.append({'path':str(p),'hits':'|'.join(hits),'writes_partition_path':bool(re.search(r'(np\.save|to_parquet|write_parquet).*partitions|partitions.*(np\.save|to_parquet|write_parquet)',txt,re.S))})
summary={'partitions':len(files),'partition_names_unique':len({p.name for p in files}),'sha_groups':len(byhash),'unique_sha':len(byhash),'duplicate_groups':len(dup),'duplicate_files':sum(len(v) for v in dup.values()),'excess_duplicate_files':sum(len(v)-1 for v in dup.values()),'group_size_distribution':dict(Counter(len(v) for v in dup.values())),'malformed_partitions':malformed,'missing_parquet':sum(not r['parquet_exists'] for r in records),'parquet_rows_not_one':sum(r['parquet_rows']!=1 for r in records),'non_success_status':sum(r['status']!='success' for r in records),'duplicate_relation_groups':dict(Counter(next(x['group_relation'] for x in out if x['duplicate_group']==g) for g in {x['duplicate_group'] for x in out})),'named_cases':comps,'producer_search_hits':found}
(OUT/'duplicate_census_independent.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:summary[k] for k in ['partitions','unique_sha','duplicate_groups','duplicate_files','excess_duplicate_files','group_size_distribution','malformed_partitions','missing_parquet','parquet_rows_not_one','non_success_status','duplicate_relation_groups']},indent=2))
