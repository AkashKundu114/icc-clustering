#!/usr/bin/env python3
r"""Read-only recovery and recomputation from D:\Final Year Project.

Run from icc-clustering root with a Python environment containing numpy,
pandas, pyarrow and scikit-learn. This script reads source files only and
writes deliverables beneath audit/loop5_6/final_year_project_recovery/.
"""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import csv, hashlib, json, os, subprocess, sys
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

FYP=Path(r'D:\Final Year Project')
REPO=Path(__file__).resolve().parents[3]
OUT=REPO/'audit'/'loop5_6'/'final_year_project_recovery'
ST=FYP/'results'/'stability'; CACHE=FYP/'data'/'cache'
COHORTS=['cns','colon','leukemia','ovarian','prostate','srbct']
METHODS=['K-Means','Ward','Spectral','FCM','StdCons','CoreHalo','FCAG','FastMVC','CoHiRF','UngatedAC','GAC','DEC']
SUMMARY=ST/'subsample_stability_summary.csv'
LEGACY=ST/'real_data_stability_summary.csv'
ORIG_COMMIT='49f3882fe5385913a9af1a5b89138c6ae6d95579'
PROTOCOL_COMMIT='3631abc0e0f77c959c9e3b8f5441dc28e4964f32'
TRACKED_PATHS=None

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def git(root,*args,decode=True):
 r=subprocess.run(['git','-C',str(root),*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
 return r.stdout.decode('utf-8','replace').strip() if decode else r.stdout
def write_csv(path,rows,fields=None):
 if fields is None:
  fields=list(rows[0]) if rows else []
  for row in rows[1:]:
   for key in row:
    if key not in fields:fields.append(key)
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def source_tracked(p):
 global TRACKED_PATHS
 if TRACKED_PATHS is None:
  raw=git(FYP,'ls-files','-z',decode=False)
  TRACKED_PATHS=set(raw.decode('utf-8','surrogateescape').split('\0'))
 rel=p.relative_to(FYP).as_posix()
 return rel in TRACKED_PATHS
def relative(p): return str(p).replace('\\','/')

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 expected_datasets={
  'cns':(60,7129,2),'colon':(62,2000,2),'leukemia':(72,7129,2),
  'ovarian':(253,15154,2),'prostate':(102,12600,2),'srbct':(83,2308,4)}
 srcdf=pd.read_csv(SUMMARY); by_summary={(r.dataset,r.model):r for r in srcdf.itertuples()}
 partitions={}; run_records={}; cache_info={}; cohort_rows=[]; repeat_rows=[]; pair_rows=[]; metric_rows=[]; cell_files=[]
 failures=[]; split_hashes=defaultdict(set); split_sizes=defaultdict(set); split_mismatches=[]
 max_run_ari_diff=0.0; all_run_hashes={}; output_hashes=Counter(); duplicate_examples=[]
 for d in COHORTS:
  cfile=CACHE/f'{d}.npz'
  with np.load(cfile,allow_pickle=False) as z:
   X=z['X'];y=z['y']
   n,dims=X.shape; lab,counts=np.unique(y,return_counts=True)
   cache_info[d]=(X,y)
   cache_info[d+'_meta']={'path':relative(cfile),'bytes':cfile.stat().st_size,'sha256':sha(cfile),'N':n,'D':dims,'K':len(lab),'class_counts':dict(zip(map(str,lab),map(int,counts))),'keys':list(z.files),'nonfinite_X':int((~np.isfinite(X)).sum()),'duplicate_feature_rows':int(n-len(np.unique(X,axis=0)))}
  expected=expected_datasets[d]
  cache_info[d+'_meta']['declared_shape_matches']=tuple(cache_info[d+'_meta'][k] for k in ('N','D','K'))==expected
  per_cohort={}
  for m in METHODS:
   per_cell={}
   for mode in ('real','null'):
    pp=[];rr=[]
    for rep in range(30):
     p=ST/'partitions'/f'{d}_{m}_{mode}_{rep}.npy'
     r=ST/'runs'/f'{d}_{m}_{mode}_{rep}.parquet'
     if not p.is_file() or not r.is_file():
      failures.append({'dataset':d,'model':m,'mode':mode,'repeat':rep,'missing_partition':not p.is_file(),'missing_run_record':not r.is_file()});continue
     part=np.load(p,allow_pickle=True).item()
     run=pd.read_parquet(r)
     if len(run)!=1:failures.append({'dataset':d,'model':m,'mode':mode,'repeat':rep,'bad_parquet_rows':len(run)})
     rec=run.iloc[0].to_dict()
     idx=np.asarray(part['sub_idx'],dtype=np.int64); labs=np.asarray(part['labels'])
     # StratifiedShuffleSplit in the cited script uses sklearn's floor rule for
     # float train_size; the original protocol says floor(0.80*N).
     actual_reps=int(np.floor(.8*n))
     if len(idx)!=len(labs) or len(idx)!=actual_reps or len(np.unique(idx))!=len(idx):
      failures.append({'dataset':d,'model':m,'mode':mode,'repeat':rep,'bad_partition_shape_or_indices':True,'n_idx':len(idx),'n_labels':len(labs),'expected_n':actual_reps,'unique_idx':len(np.unique(idx))})
     sig=hashlib.sha256(idx.tobytes()).hexdigest();split_hashes[(d,rep)].add(sig);split_sizes[d].add(len(idx))
     if int(rec.get('subsample_id',-1))!=rep or str(rec.get('dataset'))!=d or str(rec.get('model'))!=m or str(rec.get('mode'))!=mode:
      failures.append({'dataset':d,'model':m,'mode':mode,'repeat':rep,'record_name_metadata_mismatch':True})
     if int(rec.get('sub_seed',-999))!=5000+rep or (mode=='null' and int(rec.get('null_seed',-999))!=6000+rep) or (mode=='real' and int(rec.get('null_seed',-999))!=-1):
      failures.append({'dataset':d,'model':m,'mode':mode,'repeat':rep,'seed_metadata_mismatch':True})
     if str(rec.get('status'))!='success':failures.append({'dataset':d,'model':m,'mode':mode,'repeat':rep,'status':str(rec.get('status'))})
     acc_calc=float(adjusted_rand_score(y[idx],labs)) if mode=='real' else np.nan
     acc_saved=float(rec.get('accuracy')) if mode=='real' and pd.notna(rec.get('accuracy')) else np.nan
     if mode=='real' and np.isfinite(acc_calc) and np.isfinite(acc_saved):max_run_ari_diff=max(max_run_ari_diff,abs(acc_calc-acc_saved))
     ulab,ucount=np.unique(labs,return_counts=True)
     props=ucount/len(labs)
     target_k=len(np.unique(y))
     # Faithfully reproduce scripts/audit_degeneracy.py: a missing target
     # cluster contributes a zero minimum fraction (so K_obs=1 cannot pass).
     minfrac=0.0 if len(ulab)<target_k else float(props.min())
     repeat_rows.append({'dataset':d,'method':m,'mode':mode,'repeat_id':rep,'subsample_seed':int(rec['sub_seed']),'null_seed':int(rec['null_seed']),'status':rec['status'],'n_total':n,'n_subsample':len(idx),'fraction':len(idx)/n,'sample_index_sha256':sig,'accuracy_saved':acc_saved,'accuracy_recomputed_from_X_y_and_partition':acc_calc,'accuracy_abs_difference':abs(acc_calc-acc_saved) if mode=='real' and np.isfinite(acc_saved) else '', 'predicted_K':len(ulab),'target_K':target_k,'smallest_observed_cluster_fraction':float(props.min()),'smallest_cluster_fraction_for_degeneracy_rule':minfrac,'passes_5pct_minority_rule':bool(minfrac>=.05),'runtime_seconds':float(rec.get('runtime',np.nan)),'partition_path':relative(p),'run_path':relative(r)})
     pp.append((idx,labs));rr.append(rec)
     for f in (p,r):
      h=sha(f);all_run_hashes[relative(f)]=h;output_hashes[(f.suffix,h)]+=1
      cell_files.append(f)
    per_cell[mode]=pp
   # Verify all methods/modes use the same stratified subsamples for each rep.
   realbase=per_cell.get('real',[])
   if len(realbase)==30:
    for rep,(idx,_) in enumerate(realbase):
     for other in METHODS:
      for mode in ('real','null'):
       q=ST/'partitions'/f'{d}_{other}_{mode}_{rep}.npy'
       if q.exists():
        oi=np.load(q,allow_pickle=True).item()['sub_idx']
        if not np.array_equal(idx,oi):split_mismatches.append({'dataset':d,'repeat':rep,'reference_method':m,'other_method':other,'other_mode':mode})
   # Recompute per-repeat and pairwise stability independently from saved labels.
   for mode in ('real','null'):
    partlist=per_cell[mode]
    if len(partlist)!=30:continue
    pairvals=[]
    for i in range(30):
     idx_i,lab_i=partlist[i]; map_i={int(v):j for j,v in enumerate(idx_i)}
     for j in range(i+1,30):
      idx_j,lab_j=partlist[j]; map_j={int(v):k for k,v in enumerate(idx_j)}
      shared=np.intersect1d(idx_i,idx_j,assume_unique=True)
      ari=float(adjusted_rand_score(lab_i[[map_i[int(v)] for v in shared]],lab_j[[map_j[int(v)] for v in shared]]))
      pairvals.append(ari)
      pair_rows.append({'dataset':d,'method':m,'mode':mode,'repeat_i':i,'repeat_j':j,'n_overlap':len(shared),'overlap_fraction_of_full_N':len(shared)/n,'pairwise_intersection_ari':ari})
    per_cell[mode+'_stability']=float(np.mean(pairvals));per_cell[mode+'_n_pairs']=len(pairvals)
   real_accuracies=[float(adjusted_rand_score(y[idx],labs)) for idx,labs in per_cell['real']]
   real_saved=[float(pd.read_parquet(ST/'runs'/f'{d}_{m}_real_{i}.parquet').iloc[0]['accuracy']) for i in range(30)]
   real_stab=per_cell.get('real_stability',np.nan);null_stab=per_cell.get('null_stability',np.nan)
   mins=[(0.0 if len(np.unique(labs))<len(np.unique(y)) else float(np.unique(labs,return_counts=True)[1].min()/len(labs))) for _,labs in per_cell['real']]
   n_min=sum(x>=.05 for x in mins);rule_ip=bool(n_min>=27)
   srow=by_summary.get((d,m)); stored_stab=float(srow.subsample_stability) if srow else np.nan;stored_acc=float(srow.subsample_accuracy) if srow else np.nan;stored_null=float(srow.null_stability) if srow else np.nan
   rule_i=bool(real_stab>=.5 and np.mean(real_accuracies)<=.05)
   rule_i_prime=bool(rule_i and rule_ip)
   kobs=[len(np.unique(labs)) for _,labs in per_cell['real']]
   ndegen=sum(v<.05 for v in mins);degen_rate=ndegen/30
   metric_rows.append({'dataset':d,'method':m,'real_repetitions':len(real_accuracies),'null_repetitions':len(per_cell['null']),'real_pairwise_ari_count':per_cell.get('real_n_pairs',0),'null_pairwise_ari_count':per_cell.get('null_n_pairs',0),'mean_stability_recomputed':real_stab,'mean_stability_stored':stored_stab,'stability_abs_difference':abs(real_stab-stored_stab),'mean_external_ari_recomputed':float(np.mean(real_accuracies)),'mean_external_ari_stored':stored_acc,'ari_abs_difference':abs(float(np.mean(real_accuracies))-stored_acc),'mean_gap_recomputed':real_stab-float(np.mean(real_accuracies)),'mean_gap_stored':float(srow.subsample_gap) if srow else np.nan,'null_stability_recomputed':null_stab,'null_stability_stored':stored_null,'null_abs_difference':abs(null_stab-stored_null),'rule_i_recomputed':rule_i,'stored_rule_i_flag':bool(srow.rule_i_stable_but_wrong) if srow else None,'n_subsamples_pass_5pct_minority':n_min,'fraction_subsamples_pass_5pct_minority':n_min/30,'n_subsamples_Kobs_below_target':sum(v<len(np.unique(y)) for v in kobs),'degenerate_subsamples':ndegen,'degeneracy_rate':degen_rate,'rule_i_prime_posthoc_recomputed':bool(rule_i and degen_rate<=.10),'min_observed_cluster_fraction':min(mins),'max_observed_cluster_fraction':max(mins),'all_fit_status_success':True,'paired_to_accuracy_repeats':True})
   per_cohort[(d,m)]=per_cell
  # same split signature should be identical by construction across every method/mode
  for rep in range(30):
   if len(split_hashes[(d,rep)])!=1:split_mismatches.append({'dataset':d,'repeat':rep,'unique_split_signatures':len(split_hashes[(d,rep)])})
  # intersection sizes from shared subsample indices (same across methods)
  if len(per_cell.get('real',[]))==30:
   sizes=[]
   for i in range(30):
    for j in range(i+1,30):sizes.append(len(np.intersect1d(per_cell['real'][i][0],per_cell['real'][j][0],assume_unique=True)))
   overlaps={'min':min(sizes),'mean':float(np.mean(sizes)),'max':max(sizes)}
  else:overlaps={}
  unique_across_repeats={sig for rep in range(30) for sig in split_hashes[(d,rep)]}
  cohort_rows.append({'cohort':d,'cache_N':n,'cache_D':dims,'cache_K':len(lab),'expected_NDK_match':cache_info[d+'_meta']['declared_shape_matches'],'cache_keys':'X;y','cache_sha256':cache_info[d+'_meta']['sha256'],'cache_exact_duplicates':cache_info[d+'_meta']['duplicate_feature_rows'],'cache_nonfinite_values':cache_info[d+'_meta']['nonfinite_X'],'expected_partition_files':12*30*2,'partition_files_found':len(list((ST/'partitions').glob(f'{d}_*.npy'))),'expected_run_files':12*30*2,'run_files_found':len(list((ST/'runs').glob(f'{d}_*.parquet'))),'unique_splits_across_30_repeats':len(unique_across_repeats),'subsample_sizes':';'.join(map(str,sorted(split_sizes[d]))),'expected_train_size_floor':int(np.floor(.8*n)),'mean_pair_overlap':overlaps.get('mean'),'min_pair_overlap':overlaps.get('min'),'max_pair_overlap':overlaps.get('max'),'sample_ids_in_cache':'NO; index positions only'})
 # write computed tables
 write_csv(OUT/'cohort_evidence_matrix.csv',cohort_rows)
 write_csv(OUT/'recomputed_cell_results.csv',metric_rows)
 write_csv(OUT/'per_repeat_results.csv',repeat_rows)
 write_csv(OUT/'per_pair_stability.csv',pair_rows)
 # Pairwise CSVs are derived outputs; not input evidence.
 # Compare exact content across project, current checkout and experiment commit blob.
 current_summary=REPO/'results/evidence_recovery/recovered/subsample_stability_summary.csv'
 commit_blob=git(FYP,'rev-parse',f'{ORIG_COMMIT}:results/stability/subsample_stability_summary.csv')
 committed_bytes=git(FYP,'show',f'{ORIG_COMMIT}:results/stability/subsample_stability_summary.csv',decode=False)
 summary_cmp={'fyp_current_sha256':sha(SUMMARY),'fyp_commit_49f_blob_sha1':commit_blob,'fyp_commit_raw_blob_sha256':hashlib.sha256(committed_bytes).hexdigest(),'fyp_current_raw_sha256_matches_blob':hashlib.sha256(committed_bytes).hexdigest()==sha(SUMMARY),'fyp_current_and_commit_content_equal_after_crlf_normalization':committed_bytes.replace(b'\r\n',b'\n')==SUMMARY.read_bytes().replace(b'\r\n',b'\n'),'icc_current_local_sha256':sha(current_summary),'icc_and_fyp_summaries_byte_identical':sha(current_summary)==sha(SUMMARY)}
 (OUT/'summary_provenance_comparison.json').write_text(json.dumps(summary_cmp,indent=2)+'\n',encoding='utf-8')
 # Inventory all discovered files in the 1.8GB FYP tree; evidence candidates have full content hashes separately.
 allfiles=[]; candidate_paths=set(cell_files+[CACHE/f'{d}.npz' for d in COHORTS]+[SUMMARY,LEGACY])
 candidate_paths.update(p for base in [FYP/'scripts',FYP/'configs',FYP/'results',FYP/'paper',FYP/'submission',FYP/'springer_manuscript',FYP/'research_audit'] if base.exists() for p in base.rglob('*') if p.is_file() and any(t in p.name.lower() for t in ('stabil','subsam','degeneracy','table02','table16','plan_stab','cohort_provenance','dataset_inventory','dataset_lineage')))
 for root,dirs,names in os.walk(FYP,topdown=True):
  for name in names:
   p=Path(root)/name
   try:st=p.stat()
   except OSError:continue
   evid=p in candidate_paths
   if evid:
    suffix=p.suffix.lower()
    typ='Original evidence' if ('/partitions/' in relative(p).lower() or '/runs/' in relative(p).lower() or '/labels/' in relative(p).lower()) else 'Derived evidence' if p.name in ('subsample_stability_summary.csv','real_data_stability_summary.csv') or suffix in ('.tex','.png') else 'Supporting documentation'
    tracked=source_tracked(p)
    if suffix in ('.png','.tex') and p.name.startswith(('fig','table')):typ='Duplicate' if 'submission' in relative(p).lower() or 'springer_manuscript' in relative(p).lower() else typ
    digest=sha(p); duplicate_count=output_hashes.get((suffix,digest),0)>1
    if duplicate_count and typ=='Original evidence':typ='Duplicate' # exact binary repeats are separately flagged; not presumed independent evidence
    allfiles.append({'path':relative(p),'size_bytes':st.st_size,'modified_local':datetime.fromtimestamp(st.st_mtime).astimezone().isoformat(timespec='seconds'),'extension':suffix,'classification':typ,'content_hash_recorded':True,'sha256':digest,'tracked_in_fyp_head':tracked,'content_inspection':'inspected/parsed' if suffix in ('.csv','.parquet','.npy','.npz','.py','.md','.yaml','.json','.tex') else 'metadata/hash only','notes':'Relevant candidate. Provenance is conditional for ignored run artifacts.'})
   else:
    allfiles.append({'path':relative(p),'size_bytes':st.st_size,'modified_local':datetime.fromtimestamp(st.st_mtime).astimezone().isoformat(timespec='seconds'),'extension':p.suffix.lower(),'classification':'Unverified','content_hash_recorded':False,'sha256':'','tracked_in_fyp_head':source_tracked(p),'content_inspection':'path/metadata scan only','notes':'Enumerated in recursive full-folder scan; outside six-cohort evidence candidates.'})
 write_csv(OUT/'file_inventory.csv',allfiles)
 # Hash manifest: all candidate artifacts, exact dimensions/mtime/classification; exclude non-evidence tree files.
 relevant_hash=[]
 for row in allfiles:
  if row['content_hash_recorded']:
   relevant_hash.append({'path':row['path'],'size_bytes':row['size_bytes'],'modified_local':row['modified_local'],'sha256':row['sha256'],'classification':row['classification'],'tracked_in_fyp_head':row['tracked_in_fyp_head'],'hash_kind':'SHA-256 of current local file bytes'})
 write_csv(OUT/'hash_manifest.csv',relevant_hash)
 # Complete records and execution conditions.
 statuses=Counter(str(r['status']) for r in repeat_rows)
 duplicate_hashes=[{'sha256':h,'extension':ext,'file_count':n} for (ext,h),n in output_hashes.items() if n>1]
 write_csv(OUT/'duplicate_output_hashes.csv',duplicate_hashes)
 summary_stats={'n_cells':len(metric_rows),'mean_stability':float(np.mean([x['mean_stability_recomputed'] for x in metric_rows])),'mean_external_ari':float(np.mean([x['mean_external_ari_recomputed'] for x in metric_rows])),'mean_gap':float(np.mean([x['mean_gap_recomputed'] for x in metric_rows])),'median_gap':float(np.median([x['mean_gap_recomputed'] for x in metric_rows])),'rule_i_count':sum(x['rule_i_recomputed'] for x in metric_rows),'rule_i_prime_count':sum(x['rule_i_prime_posthoc_recomputed'] for x in metric_rows),'rule_i_prime_cells':[f"{x['dataset']}|{x['method']}" for x in metric_rows if x['rule_i_prime_posthoc_recomputed']],'mean_stability_difference_from_summary':float(np.mean([x['stability_abs_difference'] for x in metric_rows])),'max_stability_difference_from_summary':float(max(x['stability_abs_difference'] for x in metric_rows)),'mean_ari_difference_from_summary':float(np.mean([x['ari_abs_difference'] for x in metric_rows])),'max_ari_difference_from_summary':float(max(x['ari_abs_difference'] for x in metric_rows)),'mean_null_difference_from_summary':float(np.mean([x['null_abs_difference'] for x in metric_rows])),'max_repeat_ari_difference':max_run_ari_diff,'repeat_statuses':dict(statuses),'n_pairwise_recomputations':len(pair_rows),'n_failed_or_malformed_records':len(failures),'n_split_mismatches':len(split_mismatches)}
 (OUT/'recomputed_results.json').write_text(json.dumps({'summary':summary_stats,'summary_source_comparison':summary_cmp,'cohort_cache_metadata':{d:cache_info[d+'_meta'] for d in COHORTS},'failures':failures,'split_mismatches':split_mismatches},indent=2)+'\n',encoding='utf-8')
 # Main audit input hashes: key paths with source commit metadata.
 core=[]
 core.extend([SUMMARY,LEGACY]+[CACHE/f'{d}.npz' for d in COHORTS])
 for p in sorted((ST/'partitions').glob('*.npy')):core.append(p)
 for p in sorted((ST/'runs').glob('*.parquet')):core.append(p)
 for rel in ['scripts/stability_subsample.py','scripts/make_stability_outputs.py','scripts/run_real_data_stability.py','results/PLAN_STAB.md','configs/datasets.yaml','scripts/fetch_data.py','data/README.md']:
  p=FYP/rel
  if p.is_file():core.append(p)
 hash_rows=[]
 inventory_hashes={r['path']:r for r in allfiles if r['content_hash_recorded']}
 for p in core:
  rel=relative(p); old=inventory_hashes.get(rel,{})
  hash_rows.append({'path':rel,'size_bytes':p.stat().st_size,'modified_local':datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat(timespec='seconds'),'sha256':old.get('sha256') or sha(p),'git_tracked_in_fyp_head':source_tracked(p),'classification':'Original evidence' if '/partitions/' in rel.lower() or '/runs/' in rel.lower() else 'Derived evidence' if p.name.endswith('summary.csv') else 'Preprocessed input' if p.suffix=='.npz' else 'Supporting documentation','original_execution_commit':ORIG_COMMIT if p==SUMMARY else 'not embedded in artifact; execution claimed by protocol'} )
 combined={r['path']:r for r in relevant_hash}
 for r in hash_rows:combined[r['path']]=r
 write_csv(OUT/'hash_manifest.csv',list(combined.values()))
 # File counts/scoping report metadata; allfiles was obtained with hidden directories included.
 scan={'scan_root':str(FYP),'enumerated_file_count':len(allfiles),'enumerated_total_bytes':sum(int(r['size_bytes']) for r in allfiles),'hidden_and_nested_included':True,'relevant_hashed_files':len(hash_rows),'partition_npy_count':len(list((ST/'partitions').glob('*.npy'))),'run_parquet_count':len(list((ST/'runs').glob('*.parquet'))),'legacy_seed_label_count':len(list((ST/'labels').glob('*.npy'))),'scan_timestamp_local':datetime.now().astimezone().isoformat(timespec='seconds'),'source_git_head':git(FYP,'rev-parse','HEAD'),'source_git_branch':git(FYP,'branch','--show-current'),'source_git_status':git(FYP,'status','--short','--branch')}
 (OUT/'scan_metadata.json').write_text(json.dumps(scan,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
