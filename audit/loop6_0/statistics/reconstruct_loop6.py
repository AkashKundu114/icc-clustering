from pathlib import Path
from collections import defaultdict, Counter
import csv, hashlib, json, re, sys
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

ROOT=Path(r'D:\Final Year Project')
OUT=Path(__file__).resolve().parent
COHORTS=['cns','colon','leukemia','ovarian','prostate','srbct']
PARTS=ROOT/'results/stability/partitions'
RUNS=ROOT/'results/stability/runs'
CACHE=ROOT/'data/cache'
NAME=re.compile(r'(.+?)_(.+)_(real|null)_(\d+)\.npy$')

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1<<20),b''):h.update(block)
 return h.hexdigest()

def main():
 files=sorted(PARTS.glob('*.npy'))
 if len(files)!=4320: raise SystemExit(f'Expected 4320 NPY partitions, found {len(files)}')
 parsed=[]
 for p in files:
  m=NAME.fullmatch(p.name)
  if not m: raise SystemExit(f'Unexpected partition path: {p.name}')
  parsed.append((p,*m.groups()))
 summaries=pd.read_csv(ROOT/'results/stability/subsample_stability_summary.csv')
 saved={(str(r.dataset),str(r.model)):r for r in summaries.itertuples(index=False)}
 records=[]; errors=[]; cache_hashes={}; split_hashes={}
 for cohort in COHORTS:
  with np.load(CACHE/f'{cohort}.npz',allow_pickle=False) as z:
   X,y=z['X'],z['y']
  cache_hashes[cohort]=sha(CACHE/f'{cohort}.npz')
  if len(X)!=len(y): raise SystemExit(f'X/y length mismatch {cohort}')
  methods=sorted({method for _,d,method,mode,rep in parsed if d==cohort})
  if not methods: errors.append(f'no methods:{cohort}')
  for method in methods:
   partitions={'real':[],'null':[]}; repeat_ari=[]; minfracs=[]; real_k=[]
   for mode in ('real','null'):
    for rep in range(30):
     stem=f'{cohort}_{method}_{mode}_{rep}'
     pp=PARTS/f'{stem}.npy'; rp=RUNS/f'{stem}.parquet'
     if not pp.is_file() or not rp.is_file():
      errors.append(f'missing paired partition/record:{stem}');continue
     obj=np.load(pp,allow_pickle=True).item()
     if set(obj.keys()) < {'sub_idx','labels'}:
      errors.append(f'bad keys:{stem}:{list(obj.keys())}');continue
     idx=np.asarray(obj['sub_idx'],dtype=np.int64); pred=np.asarray(obj['labels'])
     if len(idx)!=len(pred) or len(np.unique(idx))!=len(idx) or np.any(idx<0) or np.any(idx>=len(y)):
      errors.append(f'invalid indices/labels:{stem}');continue
     if pred.ndim!=1: errors.append(f'nonvector labels:{stem}');continue
     pq=pd.read_parquet(rp)
     if len(pq)!=1: errors.append(f'parquet row count:{stem}:{len(pq)}')
     else:
      r=pq.iloc[0]
      expected=(str(r.dataset)==cohort and str(r.model)==method and str(r['mode'])==mode and int(r.subsample_id)==rep)
      if not expected: errors.append(f'parquet key mismatch:{stem}')
      if str(r.status)!='success': errors.append(f'non-success:{stem}:{r.status}')
     if mode=='real':
      val=float(adjusted_rand_score(y[idx],pred));repeat_ari.append(val)
      if len(pq)==1 and abs(val-float(pq.iloc[0].accuracy))>1e-12: errors.append(f'Parquet ARI mismatch:{stem}')
      sizes=np.unique(pred,return_counts=True)[1]
      frac=float(sizes.min()/len(pred)) if len(sizes) else float('nan')
      # Preserve the historical audit's degeneracy definition: a repeat is
      # non-degenerate only when every cluster occupies >= threshold and the
      # predicted K is not below the reference-label class count. This is a
      # diagnostic filter, not a label-blind selection rule.
      if len(sizes)<len(np.unique(y)): frac=0.0
      minfracs.append(frac);real_k.append(len(sizes))
     partitions[mode].append((idx,pred,rep))
     if mode=='real': split_hashes[(cohort,rep)]=hashlib.sha256(np.asarray(idx,dtype='<i8').tobytes()).hexdigest()
   def pair_values(parts):
    vals=[]
    for a in range(len(parts)):
     ia,la,_=parts[a]
     ma={int(x):la[j] for j,x in enumerate(ia)}
     for b in range(a+1,len(parts)):
      ib,lb,_=parts[b]
      mb={int(x):lb[j] for j,x in enumerate(ib)}
      common=sorted(set(ma).intersection(mb))
      if not common: errors.append(f'empty intersection:{cohort}/{method}/{a}/{b}');continue
      vals.append(float(adjusted_rand_score([ma[x] for x in common],[mb[x] for x in common])))
    return vals
   rpairs=pair_values(partitions['real']); npairs=pair_values(partitions['null'])
   if len(repeat_ari)!=30 or len(rpairs)!=435 or len(npairs)!=435:
    errors.append(f'count mismatch:{cohort}/{method}: ext={len(repeat_ari)},realpair={len(rpairs)},nullpair={len(npairs)}')
   stab=float(np.mean(rpairs)); ext=float(np.mean(repeat_ari)); null=float(np.mean(npairs)); gap=stab-ext
   sr=saved.get((cohort,method))
   if sr is None: errors.append(f'missing aggregate cell:{cohort}/{method}'); sst=sar=sn=float('nan')
   else: sst=float(sr.subsample_stability); sar=float(sr.subsample_accuracy); sn=float(sr.null_stability)
   records.append({'cohort':cohort,'method':method,'n_real_repeats':len(repeat_ari),'n_null_repeats':len(partitions['null']),'n_external_ari':len(repeat_ari),'n_real_pairwise':len(rpairs),'n_null_pairwise':len(npairs),'mean_stability':stab,'mean_external_ari':ext,'mean_gap':gap,'mean_null_stability':null,'nondegenerate_2pct_repeats':sum(f>=.02 for f in minfracs),'nondegenerate_5pct_repeats':sum(f>=.05 for f in minfracs),'nondegenerate_10pct_repeats':sum(f>=.10 for f in minfracs),'minimum_cluster_fraction':min(minfracs),'k_distribution_real':json.dumps(dict(sorted(Counter(real_k).items()))),'rule_i':stab>=.50 and ext<=.05,'rule_i_prime':stab>=.50 and ext<=.05 and sum(f>=.05 for f in minfracs)>=27,'saved_stability':sst,'saved_external_ari':sar,'saved_null_stability':sn,'abs_diff_stability':abs(stab-sst),'abs_diff_external_ari':abs(ext-sar),'abs_diff_null':abs(null-sn),'cache_sha256':cache_hashes[cohort]})
 # verify same subsample index schedule across methods and modes per cohort/repeat
 split_violations=[]
 for cohort in COHORTS:
  for rep in range(30):
   vals=[]
   for method in sorted({r['method'] for r in records if r['cohort']==cohort}):
    for mode in ('real','null'):
     p=PARTS/f'{cohort}_{method}_{mode}_{rep}.npy'
     if p.exists():
      o=np.load(p,allow_pickle=True).item(); vals.append((method,mode,np.asarray(o['sub_idx'],dtype='<i8').tobytes()))
   if len({v[2] for v in vals})>1: split_violations.append({'cohort':cohort,'repeat':rep,'different_index_vectors':len({v[2] for v in vals})})
 out=OUT/'reconstructed_72_cells.csv';pd.DataFrame(records).to_csv(out,index=False)
 # rederive rules: recurrence count among prime-selected methods; ensure not Boolean flags
 prime=[r for r in records if r['rule_i_prime']]
 recurrence=Counter(r['method'] for r in prime)
 for r in records:r['rule_iii']=bool(r['rule_i_prime'] and recurrence[r['method']]>=3);r['rule_iii_recurrence_count']=recurrence[r['method']]
 pd.DataFrame(records).to_csv(out,index=False)
 subsets=[]
 for rule in ('rule_i','rule_i_prime','rule_iii'):
  sub=[r for r in records if r[rule]]
  subsets.append({'rule':rule,'n_cells':len(sub),'members':';'.join(f"{r['cohort']}:{r['method']}" for r in sub),'mean_stability':float(np.mean([r['mean_stability'] for r in sub])) if sub else None,'mean_external_ari':float(np.mean([r['mean_external_ari'] for r in sub])) if sub else None,'mean_gap':float(np.mean([r['mean_gap'] for r in sub])) if sub else None,'median_gap':float(np.median([r['mean_gap'] for r in sub])) if sub else None})
 pd.DataFrame(subsets).to_csv(OUT/'posthoc_selection_audit.csv',index=False)
 # Per-cohort summaries and leave-one-cohort-out equal-cell/full estimates
 cohorts=[]
 for c in COHORTS:
  sub=[r for r in records if r['cohort']==c]
  cohorts.append({'analysis':'cohort','omitted':'','cohort':c,'n_cells':len(sub),'mean_stability':float(np.mean([r['mean_stability'] for r in sub])),'mean_external_ari':float(np.mean([r['mean_external_ari'] for r in sub])),'mean_gap':float(np.mean([r['mean_gap'] for r in sub])),'median_gap':float(np.median([r['mean_gap'] for r in sub]))})
 for c in COHORTS:
  sub=[r for r in records if r['cohort']!=c]
  cohorts.append({'analysis':'leave_one_cohort_out_cell_weighted','omitted':c,'cohort':'','n_cells':len(sub),'mean_stability':float(np.mean([r['mean_stability'] for r in sub])),'mean_external_ari':float(np.mean([r['mean_external_ari'] for r in sub])),'mean_gap':float(np.mean([r['mean_gap'] for r in sub])),'median_gap':float(np.median([r['mean_gap'] for r in sub]))})
 pd.DataFrame(cohorts).to_csv(OUT/'cohort_sensitivity.csv',index=False)
 # Cohort-cluster bootstrap is included as exploratory sensitivity only; no population probability sample justified.
 nd=[r for r in records if r['nondegenerate_5pct_repeats']>=27]
 cm={c:np.mean([r['mean_gap'] for r in nd if r['cohort']==c]) for c in COHORTS if any(r['cohort']==c for r in nd)}
 cn={c:sum(r['cohort']==c for r in nd) for c in cm}
 if len(cm)==6:
  lines=[]
  for seed in [0,1,7,42,123,2025,99173]:
   ids=np.random.default_rng(seed).integers(0,6,size=(10000,6)); vals=np.array([cm[c] for c in COHORTS]); ns=np.array([cn[c] for c in COHORTS]); w=(vals[ids]*ns[ids]).sum(1)/ns[ids].sum(1); e=vals[ids].mean(1)
   for label,v in [('equal_cell_cluster_bootstrap',w),('equal_cohort_cluster_bootstrap',e)]:lines.append({'estimand':label,'seed':seed,'B':10000,'point':float(np.average(list(cm.values()),weights=list(cn.values()))) if label.startswith('equal_cell') else float(np.mean(list(cm.values()))),'lower_percentile_2_5':float(np.quantile(v,.025)),'upper_percentile_97_5':float(np.quantile(v,.975)),'bootstrap_mean':float(v.mean()),'unit':'resampled cohort; exploratory only'})
  pd.DataFrame(lines).to_csv(OUT/'bootstrap_reanalysis.csv',index=False)
 # Summary validation against saved 72-cell aggregate table
 ds=pd.DataFrame(records); maxdiff={k:float(ds[f'abs_diff_{k}'].max()) for k in ('stability','external_ari','null')}
 summary={'inputs':{'partition_dir':str(PARTS),'run_record_dir':str(RUNS),'cache_dir':str(CACHE),'aggregate_csv':str(ROOT/'results/stability/subsample_stability_summary.csv')},'hashes':{'aggregate_csv':sha(ROOT/'results/stability/subsample_stability_summary.csv'),'cache_npz':cache_hashes},'counts':{'partition_files':len(files),'cells':len(records),'successful_external_ari_records':int(ds.n_external_ari.sum()),'real_pairwise_ari':int(ds.n_real_pairwise.sum()),'null_pairwise_ari':int(ds.n_null_pairwise.sum()),'parquet_validation_errors':len(errors),'split_mismatches':len(split_violations)},'aggregate':{'mean_stability':float(ds.mean_stability.mean()),'mean_external_ari':float(ds.mean_external_ari.mean()),'mean_gap':float(ds.mean_gap.mean()),'median_gap':float(ds.mean_gap.median()),'mean_null_stability':float(ds.mean_null_stability.mean())},'max_abs_difference_saved_summary':maxdiff,'rule_counts':{r:int(ds[r].sum()) for r in ('rule_i','rule_i_prime','rule_iii')},'split_mismatch_examples':split_violations[:20],'errors':errors[:100],'status':'SAVED_OUTPUT_RECONSTRUCTION_ONLY; not historical execution authentication; no fresh clustering fits'}
 (OUT/'reproduction_checks.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
