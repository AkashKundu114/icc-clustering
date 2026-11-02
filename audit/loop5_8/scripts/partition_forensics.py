from pathlib import Path
import hashlib,re,csv,json
from collections import defaultdict,Counter
import numpy as np,pandas as pd
ROOT=Path(r'D:\Final Year Project')
PART=ROOT/'results/stability/partitions'; RUN=ROOT/'results/stability/runs'
OUT=Path('audit/loop5_8')

def sha(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def parsed(p):
 m=re.match(r'(.+?)_(.+)_(real|null)_(\d+)\.npy$',p.name)
 return m.groups() if m else ('','','',-1)
files=sorted(PART.glob('*.npy')); groups=defaultdict(list)
for p in files: groups[sha(p)].append(p)
dup={h:ps for h,ps in groups.items() if len(ps)>1}
rows=[]
for gid,(h,ps) in enumerate(sorted(dup.items(),key=lambda z:z[1][0].name),1):
 metas=[parsed(p) for p in ps]
 dset={x[0] for x in metas}; models={x[1] for x in metas}; modes={x[2] for x in metas}; reps={x[3] for x in metas}
 type_='within_same_cell_repeats' if len(dset)==len(models)==len(modes)==1 and len(reps)>1 else ('cross_mode' if len(modes)>1 else ('cross_method' if len(models)>1 else 'other'))
 for p,meta in zip(ps,metas):
  ds,model,mode,rep=meta
  obj=np.load(p,allow_pickle=True).item(); idx=np.asarray(obj['sub_idx']); lab=np.asarray(obj['labels'])
  run=RUN/f'{ds}_{model}_{mode}_{rep}.parquet'
  rr={}; runsha=''
  if run.exists():
   runsha=sha(run); rdf=pd.read_parquet(run)
   hit=rdf[(rdf.dataset.astype(str)==ds)&(rdf.model.astype(str)==model)&(rdf['mode'].astype(str)==mode)&(rdf.subsample_id.astype(int)==int(rep))]
   if len(hit)==1: rr=hit.iloc[0].to_dict()
  rows.append(dict(duplicate_group=f'G{gid:03d}',sha256=h,group_size=len(ps),group_type=type_,file=p.name,dataset=ds,method=model,mode=mode,repeat=rep,bytes=p.stat().st_size,mtime=p.stat().st_mtime,run_record_path=str(run),run_record_sha256=runsha,run_record_found=bool(rr),fit_status=rr.get('status',''),sub_seed=rr.get('sub_seed',''),null_seed=rr.get('null_seed',''),fit_accuracy=rr.get('accuracy',''),subsample_n=len(idx),sample_indices_sha256=hashlib.sha256(idx.tobytes()).hexdigest(),labels_sha256=hashlib.sha256(lab.tobytes()).hexdigest(),n_clusters=len(np.unique(lab)),cluster_sizes=';'.join(map(str,sorted(np.unique(lab,return_counts=True)[1],reverse=True)))))
with (OUT/'duplicate_partition_inventory.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
# Exact named comparisons
named=[('cns_CoHiRF_null_17.npy','cns_CoHiRF_real_17.npy'),('prostate_CoHiRF_null_5.npy','prostate_CoreHalo_real_5.npy'),('prostate_StdCons_null_16.npy','prostate_UngatedAC_real_16.npy')]
comp=[]
for a,b in named:
 oa=np.load(PART/a,allow_pickle=True).item(); ob=np.load(PART/b,allow_pickle=True).item()
 da,ma,moa,ra=parsed(PART/a); db,mb,mob,rb=parsed(PART/b)
 ra_df=pd.read_parquet(RUN/f'{da}_{ma}_{moa}_{ra}.parquet'); rb_df=pd.read_parquet(RUN/f'{db}_{mb}_{mob}_{rb}.parquet')
 def rec(df,ds,m,mode,r):
  x=df[(df.dataset==ds)&(df.model==m)&(df['mode']==mode)&(df.subsample_id==int(r))]
  return x.iloc[0].to_dict() if len(x)==1 else {'match_count':len(x)}
 xa,xb=np.asarray(oa['sub_idx']),np.asarray(ob['sub_idx']); ya,yb=np.asarray(oa['labels']),np.asarray(ob['labels'])
 comp.append(dict(file_a=a,file_b=b,hash_a=sha(PART/a),hash_b=sha(PART/b),indices_equal=np.array_equal(xa,xb),labels_equal=np.array_equal(ya,yb),n_samples_a=len(xa),n_samples_b=len(xb),indices_order_equal=np.array_equal(xa,xb),labels_equal_after_index_sort=np.array_equal(ya[np.argsort(xa)],yb[np.argsort(xb)]) if np.array_equal(np.sort(xa),np.sort(xb)) else False,cluster_counts_a=len(np.unique(ya)),cluster_counts_b=len(np.unique(yb)),cluster_sizes_a=';'.join(map(str,sorted(np.unique(ya,return_counts=True)[1],reverse=True))),cluster_sizes_b=';'.join(map(str,sorted(np.unique(yb,return_counts=True)[1],reverse=True))),record_a=json.dumps(rec(ra_df,da,ma,moa,ra),default=str),record_b=json.dumps(rec(rb_df,db,mb,mob,rb),default=str)))
(OUT/'named_duplicate_comparisons.json').write_text(json.dumps(comp,indent=2),encoding='utf-8')
print('partitions',len(files),'dup groups',len(dup),'dup files',sum(len(p) for p in dup.values()),'inventory rows',len(rows))
print('types',Counter(r['group_type'] for r in rows))
for c in comp: print(c['file_a'],c['file_b'],'idx',c['indices_equal'],'lab',c['labels_equal'],'K',c['cluster_counts_a'],c['cluster_counts_b'],'sizes',c['cluster_sizes_a'],c['cluster_sizes_b'])
