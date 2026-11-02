from pathlib import Path
import csv, hashlib, json, statistics
from collections import Counter, defaultdict
from scipy.stats import friedmanchisquare, rankdata
ROOT=Path.cwd(); OUT=ROOT/'audit/loop6_0/benchmark'; FYP=Path(r'D:\Final Year Project')
passf=FYP/'results/passF/benchmark_matrix_passF.csv'; co=FYP/'results/exp3_cohirf_benchmark.csv'; passe=FYP/'results/passE/benchmark_matrix_seeds0_9.csv'
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def load(p):
 with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
pf=load(passf); ch=load(co); pe=load(passe)
# Verify row counts, cells, duplicate keys, complete source schedule.
allrows=[]
for r in pf:
 d=r['dataset'].lower(); m=r['model']; seed=int(r['seed']); D=int(r['D'])
 high=D>20 and d in {'cns','colon','leukemia','ovarian','prostate','srbct'}
 origin='PassF saved matrix; fit event not authenticated'
 if high and m=='Ward' and seed>=10: origin='Copied score: high-D Ward seed 10-29 values repeat seed-0 metrics per Loop5.9 merge/source audit'
 if high and m=='ICC_v2' and seed>=10: origin='Imported ARI-only values from PassE according to Loop5.9 merge/source audit'
 allrows.append({'dataset':d,'method':m,'seed':seed,'ari':float(r['ari']),'nmi':float(r['nmi']),'source_file':str(passf),'source_sha256':digest(passf),'row_provenance_assessment':origin,'fit_execution_authenticated':'NO'})
for r in ch:
 allrows.append({'dataset':r['dataset'].lower(),'method':'CoHiRF','seed':int(r['seed']),'ari':float(r['ari']),'nmi':float(r['nmi']),'source_file':str(co),'source_sha256':digest(co),'row_provenance_assessment':'CoHiRF saved result CSV; script schedule matches 0-29 high-D and 0-9 other datasets, but fit execution not authenticated','fit_execution_authenticated':'NO'})
with (OUT/'row_provenance.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(allrows[0]));w.writeheader();w.writerows(allrows)
keys=Counter((r['dataset'],r['method'],r['seed']) for r in allrows)
datasets=sorted({r['dataset'] for r in allrows}); methods=sorted({r['method'] for r in allrows})
by=defaultdict(list)
for r in allrows: by[(r['dataset'],r['method'])].append(r)
# Output actual seed schedules per dataset/method, grouped cohort class.
with (OUT/'seed_schedule_audit.csv').open('w',newline='',encoding='utf-8') as f:
 fields=['dataset','dimension_class','method','n_rows','seeds','seed_min','seed_max','schedule_matches_documented_runner','source_file','assessment'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for (d,m),rs in sorted(by.items()):
  ss=sorted(r['seed'] for r in rs); high=d in {'cns','colon','leukemia','ovarian','prostate','srbct'}; expected=list(range(30)) if high else list(range(10)); isco=m=='CoHiRF'; match=ss==expected
  w.writerow({'dataset':d,'dimension_class':'high-D biomedical' if high else 'other benchmark','method':m,'n_rows':len(rs),'seeds':';'.join(map(str,ss)),'seed_min':min(ss),'seed_max':max(ss),'schedule_matches_documented_runner':'YES' if (isco and match) else ('NO/DIFFERENT SEED FAMILY' if not isco else 'NO'),'source_file':str(co if isco else passf),'assessment':'CoHiRF phase3 script explicitly uses 0-29/0-9; PassF matrix uses same visible seed values but CSV alone does not authenticate generator; separate generic exp3 runner uses [42,101,202,...]'})
# Method matrix from inspected 5.9 review, with citation to concrete implementation paths.
impl={
'K-Means':('experiments/exp3_real_world_benchmarks/src/benchmark_models.py; src/icc/baselines/classical.py','single KMeans call; one initialization','single fit','n_init=1; not compute-matched to ensembles'),
'Ward':('src/icc/baselines/classical.py','Ward path adds seeded Gaussian jitter before deterministic agglomeration','single fit','High-D seeds 10-29 copied from seed 0; not independent repeats'),
'Spectral':('src/icc/baselines/classical.py','nearest-neighbor spectral clustering','single fit','Different affinity/compute profile'),
'FCM':('src/icc/baselines/classical.py','custom fuzzy c-means implementation','single fit','Implementation-specific; parity not verified'),
'Standard_Consensus':('src/icc/baselines/consensus.py','25 KMeans base partitions then dense coassociation','25 base fits + consensus','Unequal compute vs single-fit methods'),
'Core_Halo_Consensus':('src/icc/baselines/consensus.py','local core/halo implementation','25 base fits + postprocess','42 exact zero ARI/NMI records lack status/error metadata'),
'ICC_v1':('src/icc/baselines/consensus.py','local anchor consensus implementation','25 base fits + anchor consensus','Implementation parity not independently checked'),
'ICC_v2':('src/icc/baselines/consensus.py; src/icc/consensus_v2.py','25 base models, 40 anchors, pool fraction .15; auto engine varies with N','25 base fits + consensus','High-D seed 10-29 imported; engine differs for small N'),
'DEC':('src/icc/baselines/deep.py','auto-backend deep embedded clustering; exception handling returns zero metrics in benchmark helper','training + fine tune','Backend/compute variation; failures may be encoded as zero'),
'FCAG':('src/icc/baselines/anchor.py','local anchor-guided spectral method','anchor graph/eigensolve','No independent parity check against cited implementation'),
'FastMVC':('src/icc/baselines/anchor.py','explicit internal surrogate, not canonical published baseline','multi-view graph + eigensolve','Must be labeled proxy; not evidence about named published method'),
'CoHiRF':('src/icc/baselines/cohirf.py; scripts/run_phase3_experiments.py','25 repetitions, 15% feature subspace, threshold .80','ensemble repetitions','Different seed range from PassF/general runner; no execution log')}
with (OUT/'method_fidelity_matrix.csv').open('w',newline='',encoding='utf-8') as f:
 fields=['method','implementation_path','implementation_summary','nominal_budget','fidelity_or_comparability_limitation','evidence_status'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for m,v in impl.items(): w.writerow({'method':m,'implementation_path':v[0],'implementation_summary':v[1],'nominal_budget':v[2],'fidelity_or_comparability_limitation':v[3],'evidence_status':'Source inspected; no fit rerun or reference-parity test'})
# Failure audit.
with (OUT/'failure_status_audit.csv').open('w',newline='',encoding='utf-8') as f:
 fields=['method','rows','zero_ari_count','zero_nmi_count','explicit_status_column','interpretation'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for m in methods:
  rs=[r for r in allrows if r['method']==m]; zA=sum(r['ari']==0 for r in rs);zN=sum(r['nmi']==0 for r in rs)
  w.writerow({'method':m,'rows':len(rs),'zero_ari_count':zA,'zero_nmi_count':zN,'explicit_status_column':'NO','interpretation':'Zero scores are ambiguous between genuine outcome and failed fit; exception-to-zero behavior is documented for DEC path' if zA or zN else 'No zero-valued ARI/NMI rows; no explicit fit status is present'})
# summarize 156 cells and Friedman across per-cell means
cellmeans={k:statistics.mean(r['ari'] for r in v) for k,v in by.items()}
if len(datasets)!=13 or len(methods)!=12 or len(cellmeans)!=156: raise RuntimeError(f'wrong matrix: {len(datasets)} datasets, {len(methods)} methods, {len(cellmeans)} cells')
mat=[[cellmeans[(d,m)] for d in datasets] for m in methods]
stat,p=friedmanchisquare(*mat); ranks=[rankdata([-cellmeans[(d,m)] for m in methods],method='average') for d in datasets] # ranks 1 best
avg={m:statistics.mean(r[i] for r in ranks) for i,m in enumerate(methods)}
with (OUT/'recalculated_benchmark.csv').open('w',newline='',encoding='utf-8') as f:
 fields=['dataset','method','n_saved_score_rows','mean_ari','sd_ari','avg_rank_within_dataset','source_provenance_caveat'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for d in datasets:
  order=sorted(methods,key=lambda m:cellmeans[(d,m)],reverse=True)
  for rk,m in enumerate(order,1):
   rs=by[(d,m)]; w.writerow({'dataset':d,'method':m,'n_saved_score_rows':len(rs),'mean_ari':cellmeans[(d,m)],'sd_ari':statistics.stdev(r['ari'] for r in rs) if len(rs)>1 else 0,'avg_rank_within_dataset':rk,'source_provenance_caveat':'Saved score rows; copied/imported rows and no fit event authentication'})
(OUT/'recalculation.json').write_text(json.dumps({'input_paths':[str(passf),str(co)],'input_sha256':{str(passf):digest(passf),str(co):digest(co)},'rows':len(allrows),'datasets':len(datasets),'methods':len(methods),'dataset_method_cells':len(cellmeans),'duplicate_dataset_method_seed_keys':sum(v>1 for v in keys.values()),'incomplete_cells':[str(k) for k,v in by.items() if len(v)!=(30 if k[0] in {'cns','colon','leukemia','ovarian','prostate','srbct'} else 10)],'friedman_chi2':float(stat),'df':len(methods)-1,'p_value':float(p),'average_ranks':avg,'interpretation':'Saved-score-row recalculation only; not 3000 authenticated fit events; descriptive exploratory Friedman across a convenience set of heterogeneous datasets.'},indent=2)+'\n')
print('rows',len(allrows),'datasets',len(datasets),'methods',len(methods),'cells',len(cellmeans),'duplicate keys',sum(v>1 for v in keys.values()),'Friedman',stat,p,'ICC_v2',avg.get('ICC_v2'))
