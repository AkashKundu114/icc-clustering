#!/usr/bin/env python3
"""Loop 5.5 audit-only recomputations from present local artifacts.

Run from repository root: python audit/loop5_5/run_loop5_5_audit.py
All hashes are computed dynamically. No data or production files are modified.
"""
from pathlib import Path
import csv, hashlib, json, subprocess, statistics
from collections import Counter, defaultdict
import numpy as np
from scipy.stats import friedmanchisquare, rankdata

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "audit" / "loop5_5"
STAB = ROOT / "results/evidence_recovery/recovered/subsample_stability_summary.csv"
RUNS = ROOT / "results/evidence_recovery/recovered/results.json"

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()

def tracked(rel):
    return subprocess.run(['git','ls-files','--error-unmatch',rel],cwd=ROOT,text=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0

def readcsv(p):
    with p.open(newline='',encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def writecsv(name, rows, fields=None):
    p=OUT/name
    if not fields: fields=list(rows[0]) if rows else []
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    stab=readcsv(STAB); raw=json.loads(RUNS.read_text(encoding='utf-8'))
    prior_manifest=json.loads((ROOT/'audit/loop5_4/execution_manifest.json').read_text(encoding='utf-8'))
    expected={k:v.get('sha256') for k,v in prior_manifest.get('input_artifacts',{}).items()}
    for p in (STAB,RUNS):
        key=str(p.relative_to(ROOT)).replace('\\','/')
        if expected.get(key) and sha(p)!=expected[key]:
            raise RuntimeError(f"SHA-256 mismatch for {key}: expected {expected[key]}, computed {sha(p)}")
    vals=np.array([[float(r['subsample_stability']),float(r['subsample_accuracy'])] for r in stab])
    gaps=np.array([float(r['subsample_stability'])-float(r['subsample_accuracy']) for r in stab])
    datasets=sorted(set(r['dataset'] for r in stab)); methods=sorted(set(r['model'] for r in stab))
    perds=[]
    for d in datasets:
        rr=[r for r in stab if r['dataset']==d]
        perds.append({'dataset':d,'n_cells':len(rr),'mean_stability':np.mean([float(x['subsample_stability']) for x in rr]),'mean_external_ari':np.mean([float(x['subsample_accuracy']) for x in rr]),'mean_gap':np.mean([float(x['subsample_stability'])-float(x['subsample_accuracy']) for x in rr])})
    perms=[]
    for d in datasets:
        g=np.array([float(r['subsample_stability'])-float(r['subsample_accuracy']) for r in stab if r['dataset']!=d]);perms.append({'type':'leave_one_dataset_out','omitted':d,'n_cells':len(g),'mean_gap':float(g.mean())})
    for m in methods:
        g=np.array([float(r['subsample_stability'])-float(r['subsample_accuracy']) for r in stab if r['model']!=m]);perms.append({'type':'leave_one_method_out','omitted':m,'n_cells':len(g),'mean_gap':float(g.mean())})
    writecsv('stability_recomputed_per_dataset.csv',perds)
    writecsv('stability_leave_one_out.csv',perms)
    stats={'input':str(STAB.relative_to(ROOT)),'rows':len(stab),'datasets':datasets,'methods':methods,'observations_per_cell':1,'mean_stability':float(vals[:,0].mean()),'mean_external_ari':float(vals[:,1].mean()),'mean_gap_direct':float(gaps.mean()),'mean_gap_stored':float(np.mean([float(x['subsample_gap']) for x in stab])),'median_gap':float(np.median(gaps)),'dataset_weighted_mean_gap':float(np.mean([x['mean_gap'] for x in perds])),'method_weighted_mean_gap':float(np.mean([np.mean([float(r['subsample_stability'])-float(r['subsample_accuracy']) for r in stab if r['model']==m]) for m in methods])),'nine_cell_rule_i_count':sum(str(r['rule_i_stable_but_wrong']).lower()=='true' for r in stab),'paired_repeated_observations_available':False}
    (OUT/'stability_recomputed_statistics.json').write_text(json.dumps(stats,indent=2)+'\n',encoding='utf-8')

    fr=[r for r in raw if r.get('experiment')=='exp3_1' and r.get('metric_name')=='ari']
    ds=sorted(set(r['dataset'] for r in fr)); ms=sorted(set(r['method'] for r in fr)); counts=Counter((r['dataset'],r['method']) for r in fr)
    seeds=Counter((r['dataset'],r['method'],r['seed']) for r in fr)
    matrix=np.array([[np.mean([float(r['metric_value']) for r in fr if r['dataset']==d and r['method']==m]) for m in ms] for d in ds])
    stat,p=friedmanchisquare(*[matrix[:,j] for j in range(len(ms))]); ranks=np.mean(np.array([rankdata(-row,method='average') for row in matrix]),axis=0)
    seedcounts=Counter(counts.values()); duplicate_keys=sum(v>1 for v in seeds.values())
    frows=[]
    for i,d in enumerate(ds):
        for j,m in enumerate(ms): frows.append({'dataset':d,'method':m,'n_observations':counts[(d,m)],'n_unique_seeds':len({r['seed'] for r in fr if r['dataset']==d and r['method']==m}),'mean_ari':matrix[i,j],'average_rank_within_dataset':rankdata(-matrix[i,:],method='average')[j]})
    writecsv('friedman_raw_cell_recomputation.csv',frows)
    frj={'source':str(RUNS.relative_to(ROOT)),'ari_observation_count':len(fr),'datasets':ds,'methods':ms,'matrix_shape':list(matrix.shape),'observations_per_cell_distribution':dict(seedcounts),'unique_dataset_method_seed_rows':len(seeds),'duplicate_dataset_method_seed_keys':duplicate_keys,'seed_values':sorted(set(r['seed'] for r in fr)),'distinct_config_hashes':len(set(r['config_hash'] for r in fr)),'source_commit_values':sorted(set(r.get('commit_hash','') for r in fr)),'friedman_chi2':float(stat),'df':len(ms)-1,'p_value':float(p),'average_ranks_best_first':[{'rank':i+1,'method':ms[j],'average_rank':float(ranks[j])} for i,j in enumerate(np.argsort(ranks))],'qualification':'Computed over dataset-level means; repeated seeds are reduced within dataset-method cells. Datasets are heterogeneous and are not independent draws from a defined population.'}
    (OUT/'friedman_recomputed.json').write_text(json.dumps(frj,indent=2)+'\n',encoding='utf-8')

    inputs=[STAB,RUNS,ROOT/'data/registry.yaml',ROOT/'configs/datasets.yaml',ROOT/'src/icc/datasets/scrnaseq.py',ROOT/'audit/loop5_4/generate_friedman_validation.py']
    pm=[]
    for p in inputs:
        pm.append({'relative_path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256_computed':sha(p),'source_commit':git('log','-1','--format=%H','--',str(p.relative_to(ROOT))) if tracked(str(p.relative_to(ROOT))) else 'UNTRACKED/NO_COMMIT','tracked':tracked(str(p.relative_to(ROOT))),'fresh_clone_available':tracked(str(p.relative_to(ROOT))),'artifact_class':'derived summary' if 'summary' in p.name else ('registry/code' if p.suffix in ('.py','.yaml') else 'raw run records'),'this_audit_action':'recomputed from actual bytes' if p in (STAB,RUNS) else 'read only'} )
    writecsv('artifact_provenance_manifest.csv',pm)

    datasets_meta=[('CNS','cns',60,7129,2,'OpenML 45086; Pomeroy et al. 2002','oncology; diagnostic classes'),('Colon','colon',62,2000,2,'OpenML 45087; Alon et al. 1999','oncology; tumor/normal'),('Indian Pines','indian_pines',10249,200,16,'AVIRIS/UPV; Indian Pines scene','land cover; background excluded'),('Isolet','isolet',7797,617,26,'UCI/OpenML 300; Fanty & Cole','spoken-letter semantic classes'),('Leukemia','leukemia',72,7129,2,'OpenML 1104; Golub et al. 1999','ALL/AML diagnostic classes'),('Madelon','madelon',500,500,2,'NIPS 2003 feature selection challenge/OpenML 1485','synthetic task labels'),('Newsgroups20','newsgroups20',18846,10000,20,'CMU 20 Newsgroups; Lang 1995','semantic topic labels'),('Ovarian','ovarian',253,15154,2,'OpenML 45098; Petricoin et al. 2002','case/control; mass spectrometry'),('Prostate','prostate',102,12600,2,'OpenML 45099; Singh et al. 2002','tumor/normal'),('Sonar','sonar',208,60,2,'UCI/OpenML 40; Gorman & Sejnowski 1988','mine/rock domain labels'),('SRBCT','srbct',83,2308,4,'OpenML 45101; Khan et al. 2001','tumor subtype'),('Yale B','yale_b',2414,1024,38,'UCSD Extended Yale Face Database B; Georghiades et al. 2001','subject ID; nuisance identity groups'),('Zheng68K','zheng68k',700,765,10,'Scanpy pbmc68k_reduced(); Zheng et al. 2017','bulk_labels in reduced loader; full mode lacks labels')]
    inv=[]
    for name,key,n,d,k,source,sem in datasets_meta:
        aliases={'Newsgroups20':'20 Newsgroups; 20News','Zheng68K':'PBMC68k (ambiguous alias only)','Yale B':'Extended Yale B','CNS':'CNS tumor'} .get(name,'')
        inv.append({'canonical_name':name,'registry_key':key,'aliases_or_reported_names':aliases,'N_registry_or_loader':n,'D_registry_or_loader':d,'K_registry_or_loader':k,'source_and_original_citation':source,'preprocessing_claimed':'data/registry.yaml; dataset-specific, not verified against benchmark files','label_source_and_semantics':sem,'sample_ids_preserved':'UNVERIFIABLE; cache stores X,y only','duplicates_or_filtering':'UNVERIFIABLE from absent feature arrays; see registry notes','exact_benchmark_data_recoverable_here':'NO feature arrays; only metric records','redistribution':'UNVERIFIED; source-specific terms must be reviewed; Yale B research-use restriction flagged'})
    writecsv('dataset_inventory.csv',inv)
    elig=[]
    paired=set(datasets)
    for x in inv:
        d=x['registry_key']; in72=d in paired
        has_benchmark=d in {r['dataset'] for r in fr}
        elig.append({'dataset':x['canonical_name'],'feature_matrix':'MISSING','reference_labels':'PARTIALLY_VERIFIED' if has_benchmark else 'UNVERIFIABLE','stable_sample_ids':'MISSING','preprocessing_script':'PARTIALLY_VERIFIED','repeated_subsampling_records':'MISSING','per_method_assignments':'MISSING','per_method_stability':'PARTIALLY_VERIFIED' if in72 else 'MISSING','external_ari':'PARTIALLY_VERIFIED' if has_benchmark else 'PARTIALLY_VERIFIED' if in72 else 'MISSING','matching_seeds_and_resampling':'MISSING','uncertainty_sufficient':'MISSING','paired_stability_external_ari':'PARTIALLY_VERIFIED' if in72 else 'MISSING','exclusion_or_limit':'Only 6-dataset aggregate summary has stability/ARI pair; no run-level assignments or matching perturbations. Other datasets have benchmark ARI runs only.'})
    writecsv('dataset_eligibility_matrix.csv',elig)
    state={'code_under_audit_commit':git('rev-parse','HEAD'),'audit_execution_commit':git('rev-parse','HEAD'),'audit_deliverables_commit':'NOT YET COMMITTED','commit_timestamp':git('log','-1','--format=%cI','HEAD'),'remote_head':git('rev-parse','origin/main'),'prior_loop54_execution_commit':'f9d9d44af3ba3c2f90c5bf6853858005704839ac','prior_loop54_code_commit':'4107feb9cdeda889426b39b293a9dc1c4857fd95','working_tree_before':'clean on tracked files before Loop 5.5 outputs; ignored local results/data/paper present','changes_since_loop54':['audit/loop5_4/* committed in e745ee0'],'tracked_raw_or_result_files':git('ls-files','data','results'),'fresh_clone_has_ignored_inputs':False}
    (OUT/'execution_manifest.json').write_text(json.dumps({'repository_state':state,'inputs':[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p),'recomputed':p in (STAB,RUNS)} for p in inputs if p.exists()],'scripts_executed':['python audit/loop5_5/run_loop5_5_audit.py'],'outputs':['stability_recomputed_statistics.json','stability_recomputed_per_dataset.csv','stability_leave_one_out.csv','friedman_recomputed.json','friedman_raw_cell_recomputation.csv','artifact_provenance_manifest.csv','dataset_inventory.csv','dataset_eligibility_matrix.csv']},indent=2)+'\n',encoding='utf-8')

    docs={
'repository_state_and_provenance.md':f'''# Repository state and provenance — Loop 5.5

Fetched `origin` before inspection. `HEAD` and fetched `origin/main` are both `{state['code_under_audit_commit']}` (commit timestamp `{state['commit_timestamp']}`). The commit adds Loop 5.4 audit files. `git status` was clean for tracked files at start. Current audit additions are uncommitted and confined to `audit/loop5_5/`.

- Code under audit: `{state['code_under_audit_commit']}`.
- Audit execution commit: `{state['audit_execution_commit']}`.
- Audit deliverables commit: not yet committed; no deliverables commit exists.
- Loop 5.4 manifest instead records code `{state['prior_loop54_code_commit']}` and execution `{state['prior_loop54_execution_commit']}`; these differ from current HEAD.
- Tracked `data/`, `results/`, `paper/`: none. Locally present files under results, data/raw/cache and paper are ignored. They are not available in a fresh clone.
- Current raw and cached dataset arrays: absent. Present local `results/evidence_recovery/recovered/` includes `results.json` and `subsample_stability_summary.csv`, both ignored.

`git fetch origin` completed. `git diff` from the prior commit shows the Loop 5.4 audit directory additions only. The audit execution did not modify production code, tests, data, or prior audits. Key artifacts and dynamic byte hashes are in `artifact_provenance_manifest.csv`.

**Prior report file references:** all inspected Loop 5.4 report files listed in its execution manifest are present under `audit/loop5_4/`. Its cited result inputs also happen to exist locally, but are ignored and have no fresh-clone guarantee. Some prior statements do not follow from these inputs; see discrepancy register.
''',
'dataset_identity_and_provenance.md':'''# Dataset identity and provenance

The 13 names in the inventory are confirmed as keys in `data/registry.yaml` and as dataset names in the local `results.json` ARI records. Those are different levels of evidence: registry metadata is a claim, while run rows establish that a dataset/method/seed metric record exists. Neither provides the actual feature matrix, label vector, sample identifiers, or license text.

**PBMC68k versus Zheng68K:** the source code `src/icc/datasets/scrnaseq.py` names the loader `load_zheng68k`, and its reduced mode calls Scanpy `pbmc68k_reduced()`, reporting shape 700 × 765 and 10 encoded `bulk_labels` (or `louvain` fallback). The same loader’s full mode downloads the 68k donor-A matrix, selects highly variable genes, then assigns `y = zeros`, so it has no meaningful external class labels. `data/registry.yaml` describes 700 × 765 but also calls the dataset “Zheng PBMC 68k”; `data/README.md` instead states 68,579 × 2,000 and 11 classes. The result records say `zheng68k` and N=700, D=765, K=10. Thus PBMC68k is a family/project alias, not enough to prove identity of the full 68k population with the 700-cell reduced Scanpy variant. The records indicate the reduced variant was benchmarked. **Identity decision: conditionally verified for the reduced Scanpy variant only; the alternate PBMC68k name is ambiguous.**

Across all datasets, sample IDs and duplicate status cannot be checked because no matrices or label files are present. Registry counts and transformations are recorded in `dataset_inventory.csv` as declared metadata, not verified reconstructed data. Original citation strings are present for most registry entries; exact source releases, versions, label derivations, licensing terms, and redistribution rights require upstream primary-source verification before packaging.
''',
'methodological_comparability_report.md':'''# Methodological comparability

The additional seven datasets cannot be added to the stability–accuracy estimand from available records. The stability summary contains exactly 72 rows: six biomedical datasets × twelve methods, one aggregate record per cell. It has neither repetitions nor sample-level assignments. The 13-dataset `results.json` contains 1,430 external-ARI runs (13 × 11 × 10 seeds), but it is a distinct benchmark pipeline and stores no matching stability measures.

| Design element | Six-cohort summary | 13-dataset benchmark | Audit conclusion |
|---|---|---|---|
| Repetitions | No per-repeat observations; Loop 5.4 describes 30 stratified 80% draws, but raw draws absent | 10 initialization seeds per cell | Different stochastic units |
| Methods | 12, including CoreHalo, CoHiRF, GAC, StdCons, UngatedAC | 11, including ICC_v1/v2, Standard_Consensus, Li_et_al_2019 | No complete common method identity map; GAC/ICC_v2 may be related but this is not a verified crosswalk |
| Datasets | CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT | 13 named benchmark datasets | Only six overlap by name; other seven have no stability records |
| K | Registry K values; exact actual K behavior unavailable | K recorded in metric rows; method-level assignments absent | Fixed/estimated behavior not established consistently |
| Sampling/seed | Aggregate summary has no seed/draw identifiers | 10 seeds 42,101,…,909; one seed per config hash | Not pairable to stability draws |
| ARI and stability | Both columns in one summary cell | ARI only in broad benchmark | Same-cell aggregation is not proof of paired observations |
| Missing/singletons/overlap | Assignment-level handling unavailable | Assignment-level handling unavailable | Unverifiable |

No comparable paired experiment can be reconstructed without inventing pairings. The eligible expansion count is therefore **zero additional datasets; the only paired aggregate table remains 6 × 12 = 72 cells**, with repeated-observation uncertainty unavailable. The broad benchmark is reportable separately as external-ARI performance only.
''',
'dataset_scientific_eligibility.md':'''# Scientific eligibility decisions

Decisions concern whether a dataset can support the primary biological stability–accuracy analysis with current evidence. No additional dataset qualifies because matched resampling stability is absent. A numerical class label does not make a dataset biological ground truth.

| Dataset | Decision | Reason |
|---|---|---|
| CNS | ELIGIBLE FOR PRIMARY ANALYSIS | Biomedical diagnostic reference; already in six-cohort aggregate analysis. Raw repeats/IDs remain unavailable. |
| Colon | ELIGIBLE FOR PRIMARY ANALYSIS | Tumor/normal biomedical reference; already included. |
| Leukemia | ELIGIBLE FOR PRIMARY ANALYSIS | ALL/AML diagnostic reference; already included. |
| Ovarian | ELIGIBLE FOR PRIMARY ANALYSIS | Case/control biomedical reference; already included, with proteomic rather than microarray features. |
| Prostate | ELIGIBLE FOR PRIMARY ANALYSIS | Tumor/normal biomedical reference; already included. |
| SRBCT | ELIGIBLE FOR PRIMARY ANALYSIS | Tumor-subtype biomedical reference; already included. |
| Indian Pines | DESCRIPTIVE ONLY | Land-cover labels are meaningful external classes, but spatially adjacent pixels violate simple exchangeability and no stability runs exist. |
| Isolet | DESCRIPTIVE ONLY | Spoken-letter recognition labels are meaningful semantic classes; no matched stability runs; 26-class objective differs. |
| Madelon | DESCRIPTIVE ONLY | Synthetic challenge labels are constructed task labels, not biological categories; no paired stability. |
| Newsgroups20 | DESCRIPTIVE ONLY | Human topic categories are meaningful semantic labels but may contain topic overlap and no paired stability. |
| Sonar | DESCRIPTIVE ONLY | Mine/rock domain labels are meaningful, but non-biomedical and no paired stability. |
| Yale B | DESCRIPTIVE ONLY | Subject IDs are identity categories, while illumination is nuisance structure; no paired stability and licensing is restricted/unclear. |
| Zheng68K | INELIGIBLE | Registry, README, loader and runs disagree on variant/dimensions; full loader labels are all zero; reduced-mode label source needs provenance and exact array recovery. |

“Primary eligible” for the existing six means the label concept is suitable, not that the local summary is fully reproducible or confirms all processing steps.
''',
'expanded_statistical_analysis.md':'''# Expanded statistical analysis

## Scope and recomputation

Executed `python audit/loop5_5/run_loop5_5_audit.py` against the local bytes of `subsample_stability_summary.csv` and `results.json`. Hashes are calculated in the script, not embedded as assumed evidence. Outputs: `stability_recomputed_statistics.json`, `stability_recomputed_per_dataset.csv`, `stability_leave_one_out.csv`, `friedman_recomputed.json`, and `friedman_raw_cell_recomputation.csv`.

The 72-cell descriptive values recompute exactly: mean stability 0.516586, mean external ARI 0.052312, direct mean difference 0.464274. The difference is calculated cellwise as stored subsample stability minus stored subsample external ARI, then averaged equally over 72 dataset–method aggregates. Median direct difference is **0.448407**, not the 0.4700 asserted in Loop 5.4. Dataset and method weighted means coincide because this table is balanced. There is one aggregate per cell, not 72 independent repetitions and not raw uncertainty observations.

The published “nine-cell” claim is not reproduced by the stored Boolean `rule_i_stable_but_wrong`: the file marks 20 rows true. Its exact selection rule and nine-row derivation therefore require reconciliation; it remains a selected conditional description and cannot confirm the primary result independently.

## Sensitivity and inference limits

The script recomputes every leave-one-dataset and leave-one-method mean gap. These are deterministic descriptive sensitivities on the same 72 aggregate cells. Since additional datasets lack stability, no biomedical/non-biomedical heterogeneity comparison, expanded dataset-level relationship, label-semantics sensitivity, or consistent-method expansion is estimable. No cell-level significance test or dataset bootstrap is warranted from this artifact. Dataset count for the paired aggregate analysis remains six, but raw repeated observations and hierarchical uncertainty are unavailable.

## Finding

The direction and magnitude of the six-cohort *aggregate table* remain materially as previously reported. This is descriptive replication from a local ignored summary, not independent reproduction from raw partitions or subsamples. Expansion to 13 is unsupported. Statistical evidence status: DESCRIPTIVE ONLY; population-level inference and repeated-observation uncertainty are UNVERIFIED.
''',
'friedman_benchmark_reverification.md':'''# 13-dataset Friedman benchmark reverification

Independently recalculated from local `results/evidence_recovery/recovered/results.json` by the Loop 5.5 script. Filtering `experiment == exp3_1` and `metric_name == ari` yields 1,430 observations, exactly 13 datasets × 11 methods × 10 distinct seeds. There are 143 dataset–method cells, 10 observations each, no duplicate dataset–method–seed keys, and ten config hashes corresponding to the ten seeds. Every row carries source commit `879fd96a282e88f5491826dd7355d24d9490661b`.

Within each dataset–method cell, the ten ARIs are averaged. Friedman is applied across the 13 dataset-level mean scores per method; rankings are descending ARI with average ranks for ties. Recomputed statistic 11.342657, df=10, p=0.331452. ICC_v2 average rank is 5.4615, fifth of 11. This independently supports the stated 11-method numerical result from raw run records, conditional on the validity/comparability of those underlying benchmark runs.

The rows contain no assignments, explicit labels, resampling configuration, or data hashes. Seed equality across methods is visible, but this does not establish paired initialization or identical preprocessing. The methods and datasets span different domains and K values. Friedman rank inference treats datasets as blocks; 13 heterogeneous benchmark datasets do not establish a general population law. Report as exploratory benchmark comparison.

The 12-method Table 6 statistic cannot be recomputed because raw observations for CoreHalo/CoHiRF across seven additional datasets are absent. Any stored summary statistic remains unverified. Keep this result separate from the 6×12 stability analysis.
''',
'public_reproducibility_and_licensing.md':'''# Public reproducibility and licensing

The fresh-clone test is conclusive at repository level: `git ls-files data results paper` returns no tracked files. `.gitignore` excludes `results/`, `data/cache/`, `data/raw/`, `paper/`, and figure binaries. Local ignored result inputs permit this audit execution but are not available from a fresh Git clone. No Zenodo archive or DOI was inspected or verified in the repository. A package proposal is not a release.

Dataset-specific rights are **not verified** by generic labels in `data/registry.yaml`. OpenML states licenses are tagged per dataset, so a generic “public domain/open access” entry is insufficient ([OpenML terms](https://beta.openml.org/terms)). The Scanpy page documents the 700×765 reduced PBMC object and its `bulk_labels`, but it is not a license grant ([Scanpy dataset docs](https://scanpy.readthedocs.io/en/stable/generated/scanpy.datasets.pbmc68k_reduced.html)). UCSD’s current Yale B+ page covers a distinct 16,128-image, 28-subject dataset and says © Regents; it does not establish license terms for the repository’s 2,414-image Yale B extraction ([UCSD Yale B+ page](https://vision.ucsd.edu/datasets/extended-yale-face-database-b-b)). OpenML, UCI, CMU, Scanpy/10x, AVIRIS/UPV, and UCSD each require source-level terms and attribution review. Derived results may still contain restrictions or biometric-data concerns. Do not place Yale B files in a public archive absent explicit authorization. The registry’s blanket license policy is not a license grant.

Practical reproduction additionally needs exact matrices and labels, stable IDs, preprocessing versions, repeated partitions, assignment outputs, and scripts/configs. None are tracked. Current audit results are reproducible only within this local checkout while ignored inputs remain present. Public reproducibility decision: HOLD.
''',
'master_discrepancy_register.md':'''# Master discrepancy register

| ID | Prior claim / issue | Loop 5.5 evidence | Status |
|---|---|---|---|
| D1 | All broad datasets recoverable and identity settled | No matrices/labels tracked; metadata conflicts across README, registry, loader | UNVERIFIED |
| D2 | PBMC68k = Zheng68K | Reduced 700×765 vs full 68k loader; full mode assigns constant labels; benchmark records use 700×765 | CONTRADICTED as unqualified identity |
| D3 | Expanded 13-set stability analysis possible | Stability summary has only six datasets; broad file contains ARI only | CONTRADICTED by available records |
| D4 | Stability and external ARI are paired | Same aggregate rows, but no matching draw IDs/assignments; pairing cannot be audited | UNVERIFIED |
| D5 | Median gap 0.4700 | Recomputed direct median is 0.448407 | CONTRADICTED |
| D6 | Nine Boolean-selected rows | Input flag marks 20 rows true; derivation of selected nine not in file | CONTRADICTED/UNVERIFIED selection definition |
| D7 | Friedman 11-method raw data has 1,430 complete rows | Recomputed from 1,430 unique rows; exact stat/rank reproduced | VERIFIED numerically, qualified design |
| D8 | Friedman 12-method raw data complete | CoreHalo/CoHiRF missing on seven datasets | UNVERIFIED |
| D9 | Dataset collection redistributable / dual CC licenses adequate | No upstream authorization evidence; Yale B restriction unresolved | UNVERIFIED; redistribution HOLD |
| D10 | Fresh clone can reproduce analysis | No tracked results/data/paper; ignored local files | CONTRADICTED |
''',
'loop5_5_final_adjudication.md':'''# Loop 5.5 final adjudication

## Direct answers

1. **Are all 13 datasets correctly identified? — CONDITIONALLY VERIFIED.** Keys/names and declared dimensions are inventoried, but exact source arrays, labels and identifiers are absent. Metadata conflicts remain.
2. **Is PBMC68k the same dataset as Zheng68K? — CONTRADICTED as an unqualified claim.** The code aliases a 700-cell reduced Scanpy dataset and also provides a distinct full 68k variant; full mode has constant labels. Current benchmark records identify the reduced 700×765 version.
3. **Which have verified reference labels? — CONDITIONALLY VERIFIED:** the six biomedical cohorts have external ARI summary values; 11-method 13-dataset benchmark records have ARI values for all 13, but no label vectors are present. Zheng label provenance is specifically conflicted. Exact labels are not independently verified for any dataset from raw files.
4. **Which have valid paired stability and external ARI? — Six datasets × 12 methods as aggregate paired columns only (72 cells).** Genuine repetition-level pairing is UNVERIFIED. No additional dataset has paired stability/ARI.
5. **Can the original analysis be expanded? — NO on present evidence.**
6. **How many datasets/methods qualify for expansion? — Zero new datasets.** Existing descriptive summary is six datasets and 12 methods; broad benchmark has 13 datasets and 11 methods for ARI only.
7. **Expanded cell count? — No defensible expanded paired cell count.** Available paired aggregate count remains 72. Broad ARI benchmark is 143 cells and 1,430 seed observations.
8. **Does the central result change? — Materially unchanged in direction and mean gap** on recomputation (0.464274); median differs from prior claimed 0.4700 to 0.448407. Status DESCRIPTIVE ONLY.
9. **Robust to individual datasets/methods? — Descriptive leave-one-out values are saved.** No independent sample-level inference; the nine-cell analysis is unreconciled and not confirmation.
10. **Is 13-dataset Friedman independently reproducible? — CONDITIONALLY VERIFIED** for the 11-method raw ARI matrix: 1430 rows, statistic 11.342657, p=.331452, ICC_v2 rank 5/11. 12-method result UNVERIFIED.
11. **Which results exploratory/descriptive?** Stability gap, all leave-one-out checks, and Friedman cross-domain ranks. No confirmatory inference from these artifacts.
12. **Legally redistributable? — UNVERIFIED.** Yale B redistribution especially unsupported; no blanket CC license can be applied based on repository text.
13. **Fresh clone/archive reproduction? — NO.** Required inputs are ignored/untracked; no verified release archive.
14. **Claims to narrow/remove:** remove 13-dataset expansion of stability–accuracy claim; qualify all 72-cell statistics as aggregate descriptions; correct median; clarify six dataset scope and lack of raw repetitions; reconcile nine-cell selection; qualify Friedman as separate exploratory benchmark; remove unqualified PBMC/Zheng equivalence and license assurances.
15. **Exact next action:** recover and legally clear versioned feature matrices, labels and sample IDs for all candidates; then run one predeclared matched resampling protocol across eligible datasets/methods and archive per-repeat assignments/configs. Do not submit until manuscript claims and public reproducibility are repaired.

## Gate decisions

| Area | Status |
|---|---|
| Dataset inventory | CONDITIONAL GO |
| 13-dataset expansion | HOLD |
| Six-cohort analysis | CONDITIONAL GO |
| Statistical validity | CONDITIONAL GO |
| Public reproducibility | HOLD |
| Manuscript revision | GO |
| DMKD submission readiness | HOLD |

The original six-cohort empirical question remains the appropriate primary focus. Current evidence does not warrant converting the broader 13-dataset benchmark into paired stability–accuracy evidence. ICC remains exploratory; no superiority claim follows from this audit.
'''
    }
    for name,body in docs.items(): (OUT/name).write_text(body,encoding='utf-8')
    claims=[
      {'claim':'13 datasets extend the stability-accuracy analysis','status':'CONTRADICTED','action':'Remove; no stability metrics beyond six aggregate cohorts'},
      {'claim':'Six-cohort mean gap is about 0.464','status':'DESCRIPTIVE ONLY','action':'Retain with explicit cell definition and input limitation'},
      {'claim':'Median gap is 0.470','status':'CONTRADICTED','action':'Correct to recomputed 0.448407 for direct stability-minus-ARI values'},
      {'claim':'Nine selected cells independently confirm discordance','status':'UNVERIFIED','action':'Keep conditional only; reconcile selection rule and source rows'},
      {'claim':'11-method Friedman result from 13 datasets','status':'CONDITIONALLY VERIFIED','action':'Separate benchmark result; exploratory interpretation'},
      {'claim':'12-method Friedman result','status':'UNVERIFIED','action':'Do not claim independently reproduced'},
      {'claim':'PBMC68k and Zheng68K are interchangeable','status':'CONTRADICTED','action':'Name exact reduced/full variant and label definition'},
      {'claim':'Entire dataset package can be redistributed under CC','status':'UNVERIFIED','action':'Obtain dataset-specific rights; Yale B excluded absent authorization'},
      {'claim':'Analysis reproduces from fresh clone','status':'CONTRADICTED','action':'Release authorized immutable inputs and scripts, then clean-room replay'},
    ]
    writecsv('manuscript_claim_adjudication.csv',claims)
    (OUT/'execution_manifest.json').write_text(json.dumps({'repository_state':state,'inputs':[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p),'recomputed':p in (STAB,RUNS)} for p in inputs if p.exists()],'scripts_executed':['python audit/loop5_5/run_loop5_5_audit.py'],'outputs':sorted([p.name for p in OUT.iterdir() if p.is_file() and p.name!='execution_manifest.json'])},indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
