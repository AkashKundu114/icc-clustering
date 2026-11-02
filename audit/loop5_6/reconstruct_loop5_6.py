#!/usr/bin/env python3
"""Recompute Loop 5.6 summaries from local cache/aggregate artifacts only.

Run at repository root: python audit/loop5_6/reconstruct_loop5_6.py
This script does not rerun clustering or fabricate repeats. It requires the
ignored local inputs listed in its output manifests and verifies known hashes.
"""
from pathlib import Path
import csv, hashlib, json, subprocess
from collections import Counter
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'audit'/'loop5_6'
SUMMARY=ROOT/'results/evidence_recovery/recovered/subsample_stability_summary.csv'
SEED_SUMMARY=ROOT/'results/evidence_recovery/recovered/real_data_stability_summary.csv'
RUNS=ROOT/'results/evidence_recovery/recovered/results.json'
CACHE=ROOT/'data'/'cache'
COHORTS=['cns','colon','leukemia','ovarian','prostate','srbct']
METHODS=['K-Means','Ward','Spectral','FCM','StdCons','CoreHalo','FCAG','FastMVC','CoHiRF','UngatedAC','GAC','DEC']
NINE={'colon':['FCM','FCAG','FastMVC'],'cns':['FCM','FCAG','FastMVC'],'prostate':['FCAG','FastMVC'],'ovarian':['FCM']}

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def tracked(path):
    rel=str(path.relative_to(ROOT)).replace('\\','/')
    return subprocess.run(['git','ls-files','--error-unmatch',rel],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
def write(name,rows,fields=None):
    p=OUT/name
    if fields is None: fields=list(rows[0]) if rows else []
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    prior=json.loads((ROOT/'audit/loop5_4/execution_manifest.json').read_text(encoding='utf-8'))
    exp=prior.get('input_artifacts',{})
    known={SUMMARY:'results/evidence_recovery/recovered/subsample_stability_summary.csv',RUNS:'results/evidence_recovery/recovered/results.json'}
    hash_rows=[]
    paths=[SUMMARY,SEED_SUMMARY,RUNS]+[CACHE/f'{d}.npz' for d in COHORTS]
    for p in paths:
        exists=p.is_file(); actual=sha(p) if exists else ''
        expected=exp.get(known[p],{}).get('sha256','') if p in known else ''
        ok=(actual==expected) if expected else None
        hash_rows.append({'path':str(p.relative_to(ROOT)).replace('\\','/'),'size_bytes':p.stat().st_size if exists else '', 'expected_sha256':expected,'actual_sha256':actual,'verification_status':'MATCH' if ok is True else 'MISMATCH' if ok is False else 'NO_EXPECTED_HASH','tracked':tracked(p) if exists else False,'fresh_clone_available':tracked(p) if exists else False})
        if expected and not ok: raise RuntimeError(f"SHA256 mismatch for {p}: expected={expected}, actual={actual}")
        if not exists and p in (SUMMARY,SEED_SUMMARY,RUNS): raise FileNotFoundError(p)
    write('hash_verification_results.csv',hash_rows)

    # Local cached X/y fingerprints: contents, dimensions and labels, no IDs.
    cohort_rows=[]
    for d in COHORTS:
        p=CACHE/f'{d}.npz'
        if not p.exists(): cohort_rows.append({'dataset':d,'artifact_path':str(p.relative_to(ROOT)),'exists':False,'sha256':'','bytes':'','keys':'','N':'','D':'','K':'','class_counts':'','nonfinite_X':'','exact_duplicate_rows':'','sample_ids':'MISSING','artifact_status':'MISSING'});continue
        with np.load(p,allow_pickle=False) as z:
            X=z['X'];y=z['y']; labs,cnt=np.unique(y,return_counts=True)
            ndup=int(len(X)-len(np.unique(X,axis=0))) if X.ndim==2 else -1
            cohort_rows.append({'dataset':d,'artifact_path':str(p.relative_to(ROOT)),'exists':True,'sha256':sha(p),'bytes':p.stat().st_size,'keys':';'.join(z.files),'N':X.shape[0],'D':X.shape[1],'K':len(labs),'class_counts':';'.join(f'{a}:{b}' for a,b in zip(labs,cnt)),'nonfinite_X':int((~np.isfinite(X)).sum()),'exact_duplicate_rows':ndup,'sample_ids':'MISSING','artifact_status':'local preprocessed cache; source commit and exact benchmark identity unverified'})
    write('cohort_cache_inventory.csv',cohort_rows)

    df=pd.read_csv(SUMMARY).copy()
    df.insert(0,'row_id',[f"{r.dataset}|{r.model}" for r in df.itertuples()])
    df['recomputed_gap']=df['subsample_stability']-df['subsample_accuracy']
    df['gap_minus_stored']=df['recomputed_gap']-df['subsample_gap']
    df['n_aggregate_rows']=1
    df['repeat_count_for_stability']=30 # protocol-declared, not recovered observation count
    df['repeat_count_for_accuracy']=30 # protocol-declared, not recovered observation count
    df['repeat_records_present']=False
    df['stability_accuracy_pairing']='same aggregate row; paired repeats not auditable'
    df['resampling_config']='PLAN_STAB historical spec: 30 stratified 80% splits; seeds 5000..5029; model seed 0'
    df['selection_rule_i_prime_verified']=False
    df.to_csv(OUT/'recomputed_stability_accuracy.csv',index=False)
    recompute={k:float(v) for k,v in {'mean_stability':df.subsample_stability.mean(),'mean_external_ari':df.subsample_accuracy.mean(),'mean_gap':df.recomputed_gap.mean(),'median_gap':df.recomputed_gap.median(),'gap_sd_across_aggregate_cells':df.recomputed_gap.std(ddof=1)}.items()}
    comparisons=[]
    for name,orig,calc in [('mean_stability',0.516586,recompute['mean_stability']),('mean_external_ari',0.052312,recompute['mean_external_ari']),('mean_gap',0.464274,recompute['mean_gap']),('median_gap',0.448407,recompute['median_gap'])]:
        comparisons.append({'estimand':name,'loop5_5_reported':orig,'current_recomputed_from_same_aggregate':calc,'difference':calc-orig,'independent_raw_reproduction':'NO; aggregate input only'})
    write('recomputation_comparison.csv',comparisons)

    # Per-cohort / per-method estimates and subset reconstructions.
    per=[]
    for d,g in df.groupby('dataset',sort=True): per.append({'level':'dataset','group':d,'n_cells':len(g),'mean_stability':g.subsample_stability.mean(),'mean_external_ari':g.subsample_accuracy.mean(),'mean_gap':g.recomputed_gap.mean(),'median_gap':g.recomputed_gap.median()})
    for m,g in df.groupby('model',sort=True): per.append({'level':'method','group':m,'n_cells':len(g),'mean_stability':g.subsample_stability.mean(),'mean_external_ari':g.subsample_accuracy.mean(),'mean_gap':g.recomputed_gap.mean(),'median_gap':g.recomputed_gap.median()})
    write('cohort_and_method_results.csv',per)
    subsets=[]
    def addset(name,g,rule,status):
        ds=g.dataset.value_counts().to_dict(); ms=g.model.value_counts().to_dict()
        for _,r in g.iterrows(): subsets.append({'subset':name,'row_id':r.row_id,'selection_rule':rule,'selection_status':status,'n_rows_in_subset':len(g),'mean_stability':g.subsample_stability.mean(),'mean_ari':g.subsample_accuracy.mean(),'mean_gap':g.recomputed_gap.mean(),'median_gap':g.recomputed_gap.median(),'dataset_distribution':json.dumps(ds,sort_keys=True),'method_distribution':json.dumps(ms,sort_keys=True),'flag_rule_i':r.rule_i_stable_but_wrong})
    addset('all72',df,'All rows in original aggregate summary','DESCRIPTIVE ONLY')
    flag=df[df.rule_i_stable_but_wrong.astype(bool)]
    addset('boolean_rule_i_20',flag,'Stored Boolean from protocol Rule (i): Stab>=0.50 and Acc<=0.05','RECOMPUTED FROM AGGREGATE; no underlying repeats')
    nine=df[df.apply(lambda r:r.model in NINE.get(r.dataset,[]),axis=1)]
    addset('manuscript_nine_claim',nine,'Manuscript-listed cells said to pass Rule (i\u2032); 5% minority in >=90% of draws. Membership cross-referenced from manuscript, screen not auditable.','CONDITIONAL DESCRIPTION; post hoc; threshold pass UNVERIFIABLE')
    # Transparent exploratory alternative: all rows satisfying stored Rule i (same 20), no additional threshold substitute.
    write('subset_reconstruction.csv',subsets)
    loo=[]
    for d in sorted(df.dataset.unique()):
        g=df[df.dataset!=d];loo.append({'type':'leave_one_dataset_out','omitted':d,'n_cells':len(g),'mean_gap':g.recomputed_gap.mean(),'median_gap':g.recomputed_gap.median()})
    for m in sorted(df.model.unique()):
        g=df[df.model!=m];loo.append({'type':'leave_one_method_out','omitted':m,'n_cells':len(g),'mean_gap':g.recomputed_gap.mean(),'median_gap':g.recomputed_gap.median()})
    for name,g in [('all72',df),('rule_i20',flag),('manuscript_nine',nine)]:
        loo.append({'type':'subset_summary','omitted':name,'n_cells':len(g),'mean_gap':g.recomputed_gap.mean(),'median_gap':g.recomputed_gap.median()})
    write('statistical_sensitivity_results.csv',loo)
    (OUT/'recomputed_summary.json').write_text(json.dumps({'source':'local ignored aggregate CSV','n_cells':len(df),'datasets':sorted(df.dataset.unique()),'methods':sorted(df.model.unique()),'per_cell_raw_repetitions_available':False,'aggregate_metrics':recompute,'rule_i_flag_count':int(flag.shape[0]),'manuscript_nine_named_cells_count':int(nine.shape[0]),'nine_claim_mean_stability':float(nine.subsample_stability.mean()),'nine_claim_mean_ari':float(nine.subsample_accuracy.mean()),'nine_claim_mean_gap':float(nine.recomputed_gap.mean()),'nine_claim_median_gap':float(nine.recomputed_gap.median()),'important':'All recomputations operate on aggregate rows. They do not independently reproduce the original clustering or resampling experiment.'},indent=2)+'\n',encoding='utf-8')

    # Cohort-level inventory distinguishes local inputs from missing run evidence.
    ev=[]
    for d in COHORTS:
        cache=CACHE/f'{d}.npz'; row=next(x for x in cohort_rows if x['dataset']==d)
        ev.append({'cohort':d,'artifact_type':'preprocessed feature matrix and labels','path':str(cache.relative_to(ROOT)).replace('\\','/'),'artifact_level':'preprocessed input','local_exists':cache.exists(),'git_tracked':tracked(cache),'sha256':row.get('sha256',''),'status':'PARTIALLY VERIFIED: X/y arrays, dims/classes match; IDs/preprocessing provenance absent' if cache.exists() else 'MISSING'})
        for typ,rel in [('sample identifiers',f'data/processed/{d}_sample_ids.csv'),('per-repeat fit records',f'results/stability/runs/{d}_*.parquet'),('per-repeat partition labels',f'results/stability/partitions/{d}_*.npy')]:
            p=ROOT/rel
            exists=(list((ROOT/'results/stability/runs').glob(f'{d}_*.parquet')) if typ=='per-repeat fit records' and (ROOT/'results/stability/runs').exists() else list((ROOT/'results/stability/partitions').glob(f'{d}_*.npy')) if typ=='per-repeat partition labels' and (ROOT/'results/stability/partitions').exists() else [])
            ev.append({'cohort':d,'artifact_type':typ,'path':rel,'artifact_level':'identifier / run-level output','local_exists':bool(exists) if '*' in rel else p.exists(),'git_tracked':False,'sha256':'','status':'MISSING; expected outputs not recovered'})
    for rel,kind,level,status in [
       ('results/evidence_recovery/recovered/subsample_stability_summary.csv','stability and ARI aggregate','aggregate summary','72 rows; local ignored; reproduced arithmetically only'),
       ('results/evidence_recovery/recovered/real_data_stability_summary.csv','legacy full-data seed summary','aggregate summary','133 rows; seed-based, not subsampling stability'),
       ('results/evidence_recovery/recovered/results.json','13-dataset benchmark ARI records','per-seed benchmark records','separate benchmark; not paired stability evidence'),
       ('results/stability/runs/','original real/null per-fit records','per-repeat observations','MISSING'),
       ('results/stability/partitions/','original cluster labels and sub_idx arrays','per-repeat partitions','MISSING'),
    ]:
        p=ROOT/rel; ev.append({'cohort':'ALL SIX' if 'stability' in rel else 'ALL 13 / benchmark','artifact_type':kind,'path':rel,'artifact_level':level,'local_exists':p.exists(),'git_tracked':tracked(p) if p.exists() and p.is_file() else False,'sha256':sha(p) if p.exists() and p.is_file() else '', 'status':status})
    write('evidence_recovery_inventory.csv',ev)

    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    identities=[
      {'identity':'code_under_audit','commit':head,'timestamp':subprocess.check_output(['git','log','-1','--format=%cI','HEAD'],cwd=ROOT,text=True).strip(),'evidence':'current fetched origin/main HEAD'},
      {'identity':'original_protocol_initial','commit':'f3a973738ee2959e44bd92ce108f229b61399f06','timestamp':'2026-10-29T13:37:18+05:30','evidence':'PLAN_STAB.md first added; historical Git object available'},
      {'identity':'original_protocol_amended_rule_i_prime','commit':'3631abc0e0f77c959c9e3b8f5441dc28e4964f32','timestamp':'2026-10-30T12:12:38+05:30','evidence':'PLAN_STAB.md amended after Prostate CoreHalo observation; historical Git object available'},
      {'identity':'original_experiment_script','commit':'436d1e8a7cdef5aa3f028c5f79c1700baa27a73b','timestamp':'2026-10-29T15:33:36+05:30','evidence':'stability_subsample.py added; historical source available'},
      {'identity':'original_experiment_execution_claim','commit':'49f3882 (short hash only)','timestamp':'UNVERIFIABLE','evidence':'claimed in manuscript/archive; Git object not present; no run artifacts'},
      {'identity':'audit_execution','commit':head,'timestamp':'2026-11-02 local execution','evidence':'Loop 5.6 scripts recorded in execution_manifest.json'},
      {'identity':'final_audit_deliverables','commit':'NOT COMMITTED','timestamp':'NOT APPLICABLE','evidence':'deliverables currently working-tree files'},
    ]
    write('provenance_manifest.csv',identities)
    execinfo={'code_under_audit_commit':head,'audit_execution_commit':head,'final_audit_deliverables_commit':'NOT COMMITTED','original_protocol_commit':'f3a973738ee2959e44bd92ce108f229b61399f06','protocol_amendment_commit':'3631abc0e0f77c959c9e3b8f5441dc28e4964f32','original_script_commit':'436d1e8a7cdef5aa3f028c5f79c1700baa27a73b','original_experiment_execution_commit':'49f3882 only cited as short hash; object not recovered','executed_scripts':['python audit/loop5_6/reconstruct_loop5_6.py','python audit/loop5_6/build_minimum_package.py'],'full_clustering_experiment_rerun':False,'reason_not_rerun':'4320 fits (6x12x30x2); historical per-fit outputs absent; no reliable runtime estimate and user requires authorization before full-scale rerun','inputs_checked':[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'exists':p.exists(),'bytes':p.stat().st_size if p.is_file() else None,'sha256':sha(p) if p.is_file() else None,'tracked':tracked(p) if p.is_file() else False} for p in paths]}
    (OUT/'execution_manifest.json').write_text(json.dumps(execinfo,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
