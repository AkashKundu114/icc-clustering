"""Independent, read-only Loop 5.7 reconstruction and reconciliation.

Run from the repository root. Reads the local Final Year Project worktree and
the manuscript; writes only beneath audit/loop5_7. No model fits are rerun.
"""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import csv, hashlib, json, subprocess
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score
from scipy.stats import friedmanchisquare, rankdata

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'audit'/'loop5_7'
FYP=Path(r'D:\Final Year Project')
COHORTS=['cns','colon','leukemia','ovarian','prostate','srbct']
METHODS=['K-Means','Ward','Spectral','FCM','StdCons','CoreHalo','FCAG','FastMVC','CoHiRF','UngatedAC','GAC','DEC']
HASH_CACHE={}
def digest(path):
    path=Path(path)
    if path in HASH_CACHE: return HASH_CACHE[path]
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    HASH_CACHE[path]=h.hexdigest()
    return HASH_CACHE[path]
def writecsv(path,rows):
    cols=[]
    for r in rows:
        for k in r:
            if k not in cols: cols.append(k)
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
def git(cwd,*args):
    return subprocess.check_output(['git','-C',str(cwd),*args],text=True,stderr=subprocess.DEVNULL).strip()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    stability_dir=FYP/'results'/'stability'
    summary=pd.read_csv(stability_dir/'subsample_stability_summary.csv')
    saved={(str(r.dataset),str(r.model)):r for r in summary.itertuples(index=False)}
    raw=[]; cells=[]; errors=[]; split_sets=defaultdict(set); part_hashes=Counter(); parquet_hashes=Counter()
    cross_mode_same=[]; expected_paths=set()
    for d in COHORTS:
        cache=FYP/'data'/'cache'/f'{d}.npz'
        with np.load(cache,allow_pickle=False) as z:
            X=z['X']; y=z['y']
        target_k=len(np.unique(y)); n=len(y)
        for m in METHODS:
            runs={}
            for mode in ('real','null'):
                parts=[]; accuracies=[]; kobs=[]; minfrac=[]; statuses=[]
                for rep in range(30):
                    stem=f'{d}_{m}_{mode}_{rep}'
                    pp=stability_dir/'partitions'/f'{stem}.npy'; rp=stability_dir/'runs'/f'{stem}.parquet'
                    expected_paths.update((pp,rp))
                    if not pp.is_file() or not rp.is_file():
                        errors.append({'dataset':d,'method':m,'mode':mode,'repeat':rep,'error':'missing partition or run'}); continue
                    part=np.load(pp,allow_pickle=True).item()
                    idx=np.asarray(part['sub_idx'],dtype=np.int64); labels=np.asarray(part['labels'])
                    frame=pd.read_parquet(rp)
                    if len(frame)!=1: errors.append({'dataset':d,'method':m,'mode':mode,'repeat':rep,'error':f'parquet row count={len(frame)}'})
                    if len(frame)==0: continue
                    rec=frame.iloc[0].to_dict()
                    # Access by key (Series.mode is a pandas method).
                    meta_checks={'dataset':str(rec.get('dataset'))==d,'model':str(rec.get('model'))==m,'mode':str(rec.get('mode'))==mode,'subsample_id':int(rec.get('subsample_id',-1))==rep,'sub_seed':int(rec.get('sub_seed',-1))==5000+rep,'status':str(rec.get('status'))=='success'}
                    if not all(meta_checks.values()): errors.append({'dataset':d,'method':m,'mode':mode,'repeat':rep,'error':'metadata/status mismatch: '+str([k for k,v in meta_checks.items() if not v])})
                    if mode=='null' and int(rec.get('null_seed',-1))!=6000+rep: errors.append({'dataset':d,'method':m,'mode':mode,'repeat':rep,'error':'null seed mismatch'})
                    if mode=='real' and int(rec.get('null_seed',-1))!=-1: errors.append({'dataset':d,'method':m,'mode':mode,'repeat':rep,'error':'real null_seed not -1'})
                    if len(idx)!=len(labels) or len(idx)!=int(np.floor(.8*n)) or len(np.unique(idx))!=len(idx) or np.any(idx<0) or np.any(idx>=n):
                        errors.append({'dataset':d,'method':m,'mode':mode,'repeat':rep,'error':'partition dimensions, size, or indices invalid'})
                    signature=hashlib.sha256(idx.tobytes()).hexdigest(); split_sets[(d,rep)].add(signature)
                    part_hashes[digest(pp)]+=1; parquet_hashes[digest(rp)]+=1
                    ari=float(adjusted_rand_score(y[idx],labels)) if mode=='real' else np.nan
                    saved_ari=float(rec.get('accuracy',np.nan)) if mode=='real' else np.nan
                    if mode=='real' and (not np.isfinite(saved_ari) or abs(ari-saved_ari)>1e-12): errors.append({'dataset':d,'method':m,'mode':mode,'repeat':rep,'error':'repeat ARI differs from Parquet accuracy'})
                    u,c=np.unique(labels,return_counts=True); min_f=0.0 if len(u)<target_k else float(c.min()/len(labels))
                    parts.append((idx,labels)); statuses.append(str(rec.get('status')))
                    if mode=='real': accuracies.append(ari)
                    kobs.append(len(u)); minfrac.append(min_f)
                    raw.append({'dataset':d,'method':m,'mode':mode,'repeat':rep,'status':rec.get('status'),'n_samples':len(idx),'predicted_K':len(u),'minimum_cluster_fraction':min_f,'ari_vs_reference':ari if mode=='real' else '', 'saved_accuracy':saved_ari if mode=='real' else '', 'partition_sha256':digest(pp),'run_sha256':digest(rp)})
                runs[mode]=(parts,accuracies,kobs,minfrac,statuses)
            real_parts=runs['real'][0]; null_parts=runs['null'][0]
            def pair_aris(parts):
                vals=[]
                for i in range(len(parts)):
                    ix,ly=parts[i]; map_i={int(v):j for j,v in enumerate(ix)}
                    for j in range(i+1,len(parts)):
                        jx,ry=parts[j]; map_j={int(v):k for k,v in enumerate(jx)}
                        shared=np.intersect1d(ix,jx,assume_unique=True)
                        vals.append(float(adjusted_rand_score(ly[[map_i[int(v)] for v in shared]],ry[[map_j[int(v)] for v in shared]])))
                return vals
            stabs=pair_aris(real_parts); nulls=pair_aris(null_parts)
            accs=runs['real'][1]; mf=runs['real'][3]; ks=runs['real'][2]
            nondeg=sum(x>=.05 for x in mf)
            q=saved.get((d,m))
            s_stab=float(q.subsample_stability) if q else np.nan
            s_ari=float(q.subsample_accuracy) if q else np.nan
            s_null=float(q.null_stability) if q else np.nan
            stab=float(np.mean(stabs)); ari=float(np.mean(accs)); gap=stab-ari; rule_i=stab>=.5 and ari<=.05; rule_ip=rule_i and nondeg>=27
            cells.append({'dataset':d,'method':m,'row_id':d+'|'+m,'n_successful_real_repeats':len(accs),'n_successful_null_repeats':len(null_parts),'n_pairwise_real_aris':len(stabs),'n_pairwise_null_aris':len(nulls),'mean_stability':stab,'saved_stability':s_stab,'stability_abs_error':abs(stab-s_stab),'mean_external_ari':ari,'saved_external_ari':s_ari,'ari_abs_error':abs(ari-s_ari),'mean_gap':gap,'saved_gap':float(q.subsample_gap) if q else np.nan,'mean_null_stability':float(np.mean(nulls)),'saved_null_stability':s_null,'null_abs_error':abs(float(np.mean(nulls))-s_null),'minimum_cluster_fraction':min(mf) if mf else np.nan,'nondegenerate_repeats_5pct':nondeg,'degenerate_repeats_5pct':len(mf)-nondeg,'observed_K_distribution':json.dumps(dict(sorted(Counter(ks).items()))),'rule_i':rule_i,'rule_i_prime':rule_ip,'paired_same_protocol':len(accs)==30 and len(stabs)==435,'all_status_success':all(x=='success' for x in runs['real'][4]+runs['null'][4])})
    for d in COHORTS:
        if any(len(split_sets[(d,r)])!=1 for r in range(30)): errors.append({'dataset':d,'error':'cross-method/mode split mismatch'})
        if len({next(iter(split_sets[(d,r)])) for r in range(30) if split_sets[(d,r)]})!=30: errors.append({'dataset':d,'error':'repeated split is not unique across 30 repetitions'})
    writecsv(OUT/'independent_repeat_checks.csv',raw)
    # Method recurrence is derived from cell metrics, not stored Boolean flags.
    recurrence=Counter(c['method'] for c in cells if c['rule_i_prime'])
    for c in cells: c['rule_iii_method_recurrence']=recurrence[c['method']]>=3 and c['rule_i_prime']
    selected=[c for c in cells if c['rule_iii_method_recurrence']]
    nondeg_cells=[c for c in cells if c['degenerate_repeats_5pct']<=3]
    def cohort_bootstrap(frame, rng, nboot=10000):
        cohorts=np.array(['colon','srbct','cns','leukemia','prostate','ovarian'])
        means={d:float(np.mean([x['mean_gap'] for x in frame if x['dataset']==d])) for d in cohorts if any(x['dataset']==d for x in frame)}
        vals=[]
        for _ in range(nboot):
            draw=rng.choice(cohorts,size=6,replace=True)
            cvals=[means[d] for d in draw if d in means]
            if cvals: vals.append(float(np.mean(cvals)))
        return {'point_cell_weighted':float(np.mean([x['mean_gap'] for x in frame])),'point_equal_cohort':float(np.mean(list(means.values()))),'cohort_mean_gaps':means,'percentile_95_ci':list(map(float,np.percentile(vals,[2.5,97.5]))),'n_cells':len(frame),'bootstrap_resamples':nboot}
    rng_seq=np.random.default_rng(42)
    ci_all_seq=cohort_bootstrap(cells,rng_seq)
    ci_nondeg_seq=cohort_bootstrap(nondeg_cells,rng_seq)
    ci_nondeg_fresh=cohort_bootstrap(nondeg_cells,np.random.default_rng(42))
    boot={'purpose':'exploratory sensitivity reproduction; cohort exchangeability assumed','same_rng_sequential_as_audit_degeneracy.py':{'all_cells':ci_all_seq,'nondegenerate_cells':ci_nondeg_seq},'fresh_seed_on_nondegenerate_only':ci_nondeg_fresh,'warning':'The manuscript reports the cell-weighted nondegenerate point estimate with a cohort-resampled CI whose bootstrap center is the equal-cohort mean; these are different estimands.'}
    (OUT/'bootstrap_reassessment.json').write_text(json.dumps(boot,indent=2)+'\n',encoding='utf-8')
    writecsv(OUT/'recomputed_cell_results.csv',cells)
    metrics=['mean_stability','mean_external_ari','mean_gap','mean_null_stability']
    summary_rows=[]
    for k in metrics:
        vals=[c[k] for c in cells]; summary_rows.append({'metric':k,'independent_value':float(np.mean(vals)) if k!='mean_gap' else float(np.mean(vals)),'median_cells':float(np.median(vals)),'max_abs_cell_error_vs_saved':max(c[{'mean_stability':'stability_abs_error','mean_external_ari':'ari_abs_error','mean_gap':'stability_abs_error','mean_null_stability':'null_abs_error'}[k]] for c in cells) if k!='mean_gap' else max(abs(c['mean_gap']-c['saved_gap']) for c in cells),'n_cells':len(cells)})
    # Benchmark reconstruction: Pass F plus the separately generated CoHiRF table.
    passf=FYP/'results'/'passF'/'benchmark_matrix_passF.csv'; cohirf=FYP/'results'/'exp3_cohirf_benchmark.csv'
    a=pd.read_csv(passf); b=pd.read_csv(cohirf)
    bench=pd.concat([a[['dataset','model','seed','ari']],b[['dataset','model','seed','ari']]],ignore_index=True)
    keydup=int(bench.duplicated(['dataset','model','seed']).sum()); bmeans=bench.groupby(['dataset','model']).ari.mean().unstack()
    counts=bench.groupby(['dataset','model']).size()
    fstat,fp=friedmanchisquare(*[bmeans[m] for m in bmeans.columns])
    ranks=bmeans.apply(lambda row:pd.Series(rankdata(-row.to_numpy(),method='average'),index=row.index),axis=1)
    benchmark={'rows':len(bench),'datasets':int(bench.dataset.nunique()),'methods':int(bench.model.nunique()),'complete_cells':int(bmeans.size),'missing_cell_means':int(bmeans.isna().sum().sum()),'duplicate_dataset_method_seed_keys':keydup,'cell_observation_counts':dict(Counter(map(int,counts.values))),'minimum_cell_n':int(counts.min()),'maximum_cell_n':int(counts.max()),'friedman_chi_square':float(fstat),'degrees_freedom':int(len(bmeans.columns)-1),'p_value':float(fp),'ICC_v2_mean_rank':float(ranks['ICC_v2'].mean()),'ICC_v2_rank_position':int((ranks.mean()<ranks['ICC_v2'].mean()).sum()+1),'row_inputs':[str(passf),str(cohirf)]}
    (OUT/'benchmark_recalculation.json').write_text(json.dumps(benchmark,indent=2)+'\n',encoding='utf-8')
    # Machine-readable sensitivity grid over the recovered per-repeat partitions.
    sens=[]
    for threshold in (.02,.05,.10):
        for required in (25,27,29,30):
            active=[]
            for c in cells:
                rpts=[r for r in raw if r['dataset']==c['dataset'] and r['method']==c['method'] and r['mode']=='real']
                n_pass=sum(float(r['minimum_cluster_fraction'])>=threshold for r in rpts)
                passed=c['rule_i'] and n_pass>=required
                if passed: active.append(c)
            counts2=Counter(c['method'] for c in active); recur=sorted(m for m,nx in counts2.items() if nx>=3)
            selected_ids=sorted(c['row_id'] for c in active if c['method'] in recur)
            sens.append({'minimum_cluster_fraction_threshold':threshold,'minimum_nondegenerate_repeats':required,'rule_i_candidates':sum(c['rule_i'] for c in cells),'rule_i_prime_cells':len(active),'recurring_methods':';'.join(recur),'rule_iii_cells':len(selected_ids),'rule_iii_cell_ids':';'.join(selected_ids)})
    writecsv(OUT/'nine_cell_sensitivity_analysis.csv',sens)
    writecsv(OUT/'nine_cell_final_verification.csv',[c for c in cells])
    # Protocol status and actual artifact counts.
    n_part=len(list((stability_dir/'partitions').glob('*.npy'))); n_run=len(list((stability_dir/'runs').glob('*.parquet')))
    part_groups=Counter(); part_digest_map=defaultdict(list)
    for p in (stability_dir/'partitions').glob('*.npy'):
        h=digest(p); part_digest_map[h].append(p.name)
    duplicate_groups=[v for v in part_digest_map.values() if len(v)>1]
    cross_mode=[]; same_method_cross_mode=[]
    for group in duplicate_groups:
        if any('_real_' in s for s in group) and any('_null_' in s for s in group):
            cross_mode.append(sorted(group))
    for d in COHORTS:
        for m in METHODS:
            for r in range(30):
                x=f'{d}_{m}_real_{r}.npy'; y=f'{d}_{m}_null_{r}.npy'
                if any(x in g and y in g for g in cross_mode): same_method_cross_mode.append(f'{d}|{m}|{r}')
    maxdiff={f'max_abs_{k}_cell_error':max(c[{'stability':'stability_abs_error','external_ari':'ari_abs_error','null_stability':'null_abs_error'}[k]] for c in cells) for k in ('stability','external_ari','null_stability')}
    def aggregate(rows):
        return {'n':len(rows),'mean_stability':float(np.mean([x['mean_stability'] for x in rows])),'mean_external_ari':float(np.mean([x['mean_external_ari'] for x in rows])),'mean_gap':float(np.mean([x['mean_gap'] for x in rows])),'median_gap':float(np.median([x['mean_gap'] for x in rows]))}
    report={'datasets':6,'methods':12,'cells':len(cells),'partition_files':n_part,'fit_records':n_run,'repeat_rows':len(raw),'missing_partition_files':max(0,6*12*30*2-n_part),'missing_fit_records':max(0,6*12*30*2-n_run),'malformed_or_failed_checks':len(errors),'failed_fit_records':sum(x['status']!='success' for x in raw),'errors':errors,'partition_unique_hashes':len(part_digest_map),'partition_duplicate_hash_groups':len(duplicate_groups),'partition_files_in_duplicate_groups':sum(map(len,duplicate_groups)),'parquet_duplicate_hash_groups':sum(1 for n in parquet_hashes.values() if n>1),'cross_mode_same_byte_partition_groups':cross_mode,'same_method_cross_mode_exact_matches':same_method_cross_mode,'aggregate':{k:float(np.mean([x[k] for x in cells])) for k in ('mean_stability','mean_external_ari','mean_gap','mean_null_stability')},'median_gap':float(np.median([x['mean_gap'] for x in cells])),'nondegenerate_60_cells':aggregate(nondeg_cells),'rule_i_20':aggregate([x for x in cells if x['rule_i']]),'rule_i_prime_18':aggregate([x for x in cells if x['rule_i_prime']]),'rule_iii_nine':{**aggregate(selected),'cells':[x['row_id'] for x in selected]},'bootstrap_reassessment':boot,'maximum_errors':maxdiff,'benchmark':benchmark,'execution_time_local':datetime.now().astimezone().isoformat(timespec='seconds')}
    (OUT/'independent_reconstruction_summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'cells':len(cells),'repeat_records':len(raw),'errors':len(errors),'benchmark':benchmark,'aggregate':report['aggregate']},indent=2))
if __name__=='__main__': main()
